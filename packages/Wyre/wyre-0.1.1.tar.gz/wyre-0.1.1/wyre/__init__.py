from wyre.wyre import inject, InjectionError

"""
Wyre : Lightweight dependency injection for pure OOP.

Wyre allows you to declare the dependencies of a given class using kwargs on a constructor.
A single decorator `@inject` does the trick. This is particularly handy when your dependency tree grows large and deep.
For example, this dependency chain : `A < B < C < D < E`, would require you to write `a = A(B(C(D(E()))))`
in order to create an instance of your class.

Using Wyre, you keep :
* your production code clean by writing just `A()` since it works recursively
* your unit tests simple : `A(b=Mock())` is all you need to mock out dependencies
"""

__version__ = '0.1.1'
__all__ = ['inject', 'InjectionError']
