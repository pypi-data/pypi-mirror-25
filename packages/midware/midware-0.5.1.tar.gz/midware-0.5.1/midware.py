# -*- coding: utf-8 -*-
"""
Middleware can always be defined in this straightforward manner:

    def wrap_smth(handler):
        def new_handler(ctx):
            # do smth with ctx
            # prime it with some values
            new_ctx = handler(ctx)
            # do some post-processing with new_ctx
            return new_ctx

        return handler

The first indentation level is not really necessary.
Also, wrapping a handlers into a lot of middleware layers
requires a lot of unnecessary brackets.

This module provides means to work with middleware in a more convinient way.

Since context is usually a nested `dict`, functions `midware.core.get_in` and
`midware.core.assoc_in` are provided for easier manipulation of values.

For no-op handlers and middleware there is `midware.core.identity`.

`midware.core.compose` allows for piping functions while not using any brackets,
but `midware.core.wrap_and_call` is suited specifically for the most
frequent one-handler-many-layers use case.

The function called `midware.core.middleware` turns generators into middleware. With
this function the previous example turns into:

    @midware.core.middleware('wrap_smth')
    def wrap_smth(ctx):
        # do smth with ctx
        # prime it with some values
        new_ctx = yield ctx
        # do some post-processing with new_ctx
        yield new_ctx

Here `'wrap_smth'` stands for the name of the middleware and it's used when
middleware is layered with `midware.core.wrap_and_call` and `verbose` is passed as `True`.
If middleware is defined without the usage of generators, then the name can be set
using `midware.core.named`. Again the following is better than the first example:

    @midware.core.named('wrap_smth')
    def wrap_smth(handler):
        def new_handler(ctx):
            # do smth with ctx
            # prime it with some values
            new_ctx = handler(ctx)
            # do some post-processing with new_ctx
            return new_ctx

        return handler

Some middleware can don't require a teardown step. These can be defined with regular functions
using `midware.core.pre`:

    @midware.core.pre('wrap_smth')
    def wrap_smth(ctx):
        # do smth with ctx
        # prime it with some values
        return ctx

To omit the setup step there is a `midware.core.post`:

    @midware.core.post('wrap_smth')
    def wrap_smth(ctx):
        # do smth with ctx
        # examine ctx contents
        return ctx

## Context managers

If you have a function like `open`, that returns a context manager, do this:

    @midware.core.middleware('wrap_open', key='some_path')
    def wrap_open(ctx, key):
        with open(ctx[key]) as f:
            ctx['some_file'] = f
            new_ctx = yield ctx
        yield new_ctx
"""

__version__ = '0.5.1'

import functools


def identity(x):
    return x


def _evalform_front(val, form):
    if callable(form):
        return form(val)
    if isinstance(form, tuple):
        fn = form[0]
        args = form[1:]
        return fn(val, *args)


def thread_first(val, *forms):
    return functools.reduce(_evalform_front, forms, val)


def _evalform_back(val, form):
    if callable(form):
        return form(val)
    if isinstance(form, tuple):
        fn = form[0]
        args = list(form[1:])
        args.append(val)
        return fn(*args)


def thread_last(val, *forms):
    return functools.reduce(_evalform_back, forms, val)


def compose(*fns):
    if not fns:
        return identity

    def wrapper(*args, **kwargs):
        rev = list(reversed(fns))
        fst = rev[0]
        rest = rev[1:]
        return functools.reduce(lambda v, f: f(v), rest, fst(*args, **kwargs))

    return wrapper


def get_in(d, ks, default=None):
    """
    Returns a value in a nested associative structure,
    where `ks` is a sequence of keys. Returns `None`, if the key
    is not present, or the `default` value, if supplied.
    """
    ks_ = ks[:-1]
    last = ks[-1]
    d_ = d

    for k in ks_:
        if type(d_) != dict or k not in d_:
            return default
        d_ = d_[k]

    if type(d_) == dict:
        return d_.get(last, default)

    return default


def assoc_in(d, ks, v):
    """
    Associates a value in a nested associative structure, where `ks` is a
    sequence of keys and `v` is the new value, and returns a nested structure.
    If any levels do not exist, `dict`s will be created.
    """
    ks_ = ks[:-1]
    last = ks[-1]
    d_ = d

    for k in ks_:
        if k not in d_:
            d_[k] = {}
        d_ = d_[k]

    d_[last] = v
    return d


class Midware:
    def __init__(self, pre, post):
        self.pre = pre
        self.post = post

    def __call__(self, handle):
        def new_handle(ctx):
            pre_ctx = self.pre(ctx)
            handled_ctx = handle(pre_ctx)
            post_ctx = self.post(handled_ctx)

            return post_ctx

        return new_handle


def pre(handle):
    return Midware(pre=handle, post=identity)


def post(handle):
    return Midware(pre=identity, post=handle)


def middleware(pre, post):
    return Midware(pre, post)


def wrap(handle, *middleware):
    return compose(*middleware)(handle)
