#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools


def disable(func):
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''

    return func


def decorator(func):
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def countcalls(func):
    '''Decorator that counts calls made to the function decorated.'''

    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


def memo(func):
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''
    
    cache = {}

    def wrapper(*args, **kwargs):
        key = hash(args + tuple(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    functools.update_wrapper(wrapper, func)
    return wrapper


def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''

    def wrapper(*args):
        if len(args) > 2:
            return func(args[0], wrapper(*args[1:]))
        return func(*args)
    return wrapper


def trace(tab='----'):
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    '''

    def deco(func):
        def wrapper(*args, **kwargs):
            arg_str = ', '.join(map(str, args))
            ctx = {'tab': tab * context['count'], 'name': func.__name__, 'arg_str': arg_str}
            print('{tab} --> {name}({arg_str})'.format(**ctx))
            context['count'] += 1
            ctx['result'] = func(*args, **kwargs)
            print('{tab} <-- {name}({arg_str}) == {result}'.format(**ctx))
            context['count'] -= 1
            return ctx['result']

        context = {'count': 0}
        return wrapper
    return deco


@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace("####")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print foo(4, 3)
    print foo(4, 3, 2)
    print foo(4, 3)
    print "foo was called", foo.calls, "times"

    print bar(4, 3)
    print bar(4, 3, 2)
    print bar(4, 3, 2, 1)
    print "bar was called", bar.calls, "times"

    print fib.__doc__
    fib(3)
    print fib.calls, 'calls made'


if __name__ == '__main__':
    main()
