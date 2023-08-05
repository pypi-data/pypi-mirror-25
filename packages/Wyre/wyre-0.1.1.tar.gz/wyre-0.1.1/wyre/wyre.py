import functools
from inspect import isclass, getfullargspec


class InjectionError(Exception):
    """
    Exception raised when an error occurs during injection.
    """

    OUTSIDE_OF_INIT = 'You can only inject dependencies by decorating __init__().\nYou tried to inject on %s'
    NOTHING_TO_INJECT = 'Nothing to inject. Add dependencies or remove @inject decorator.'
    CIRCULAR_DEPENDENCIES = 'Circular dependency detected : %s'

    def __init__(self, message):
        self.message = message


dependency_chain = []


def inject(function):
    """
    This function wraps an __init__ function and replaces kwarg with classes as default values
    by kwargs with instantiated classes as values.
    :param function: the function to dependencies inject from. Must be __init__.
    :return: A wrapped __init__ function with instantiated dependencies as kwargs.
    """
    if _is_not_init(function):
        raise InjectionError(InjectionError.OUTSIDE_OF_INIT % function.__name__)

    if _has_no_dependencies(function):
        raise InjectionError(InjectionError.NOTHING_TO_INJECT)

    @functools.wraps(function)
    def _injector(*args, **kwargs):
        dependencies = {}
        default_kwargs = _find_default_kwargs(function)

        for kwarg_name, kwarg_value in default_kwargs.items():
            if _can_inject(kwargs, kwarg_name, kwarg_value):
                dependencies.update(_create_dependency(kwarg_name, kwarg_value))

        dependency_chain.clear()
        merged_kwargs = {**kwargs, **dependencies}
        return function(*args, **merged_kwargs)

    return _injector


def _can_inject(kwargs, arg_name, arg_value):
    provided_instances = kwargs.keys()
    instance_provided = arg_name in provided_instances
    instantiable = isclass(arg_value)
    return not instance_provided and instantiable


def _find_default_kwargs(function):
    all_arguments = getfullargspec(function)
    kwargs = all_arguments.defaults
    kwargs_position = len(all_arguments.args) - len(kwargs)
    return dict(zip(all_arguments.args[kwargs_position:], kwargs))


def _is_not_init(function):
    return function.__name__ != '__init__'


def _has_no_dependencies(function):
    return not getfullargspec(function).defaults


def _create_dependency(arg_name, arg_value):
    if arg_value in dependency_chain:
        raise InjectionError(InjectionError.CIRCULAR_DEPENDENCIES % _format_dependencies(dependency_chain))

    dependency_chain.append(arg_value)
    return {arg_name: arg_value()}


def _format_dependencies(chain):
    full_chain = [chain[-1]] + chain
    return ' -> '.join([str(cls.__name__) for cls in full_chain])
