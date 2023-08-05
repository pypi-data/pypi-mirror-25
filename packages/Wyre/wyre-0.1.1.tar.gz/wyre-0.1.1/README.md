# wyre

Lightweight dependency injection for pure, testable OOP.

## Install

Wyre is available on **pypi** !
Add `wyre == 0.1` to your `requirements.txt` file or just install it with `pip install wyre`.

## Philosophy

Injecting class dependencies comes in 3 distinct ways :
* using class attributes (okay)
* using setters (better)
* using constructor (best)

Wyre allows you to declare the dependencies of a given class using kwargs on a constructor.
A single decorator `@inject` does the trick. This is particularly handy when your dependency tree grows large and deep.
For example, this dependency chain : `A < B < C < D < E`, would require you to write `a = A(B(C(D(E()))))` in order to create an instance of your class.

Using Wyre, you keep :
* your production code clean by writing just `A()` since it works recursively
* your unit tests simple : `A(b=Mock())` is all you need to mock out dependencies

## Usage

Ok, let's see how to use it.

### In production code

```python
class C:
    name = 'Bob'
    
    
class B:
    @inject
    def __init__(self, other_dependency=C):
        self.c = other_dependency
    
    def say_hello(self):
        return 'Hello %s !' % self.c.name
    

class A:
    @inject
    def __init__(self, dependency=B):
        self.b = dependency
        
    def greetings(self):
        return self.b.say_hello()
        
a = A()
a.greetings() # returns 'Hello Bob !'
```

Since `__init__` is decorated with `@inject`, `B` instance will be created and injected in `A` at instantiation time.

### In unit tests

If you want to write a test on `A` with a real instance of `B`, you basically have nothing to do but write the test.
```python
def test_say_hello():
    # given
    a = A()
    
    # when
    result = a.greetings()
    
    # then
    assert result == 'Hello !'
```

If you want to write a test on `A` with a mocked instance of `B`, you simply provide this mock using `A`'s constructor.
```python
def test_say_hello():
    # given
    mocked_b = Mock(spec=B)
    mocked_b.greetings.return_value = 'Hi there !'
    a = A(dependency=mocked_b)
    
    # when
    result = a.greetings()
    
    # then
    assert result == 'Hi there !'
```

### Limitations

Important notes on what `@inject` does :
* If an instance of a dependency is provided in `kwargs`, it will be preserved and not overridden by a new instance.
* Circular dependencies are detected at instantiation time : an `InjectionError` will be raised.
* You can only use it on `__init__()`. If you decorate any other function : an `InjectionError` will be raised.
* If no dependency is found among declared `kwargs` : an `InjectionError` will be raised.
* Wyre is strongly opinionated about dependency injection. As a matter of fact, singletons are not even considered.
