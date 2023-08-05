"""akitchensyncio -- Stephan's random bag of utilities for asyncio.
"""

from asyncio import ensure_future, get_event_loop
from functools import wraps

__all__ = ("wrap_future", "transform_future", "iawait")

def wrap_future(f):
    """Takes a callable `f` which returns an awaitable,
    and returns a callable which wraps the awaitable in
    asyncio.ensure_future.

    Can also be used as a decorator, especially
    with coroutine functions:

        @wrap_future
        async def foo(arg1, arg2):
            ...
    """
    return wraps(f)(lambda *args, **kws: ensure_future(f(*args, **kws)))

@wrap_future
async def transform_future(f, awaitable):
    """Apply a function to the result of an awaitable,
    return a future which delivers the result.
    """
    return f(await awaitable)

def iawait(awaitable):
    """"Interactive await" -- Run default eventloop until awaitable has completed.
    Mainly useful for interactive experimentation.
    """
    return get_event_loop().run_until_complete(awaitable)
