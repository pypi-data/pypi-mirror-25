akitchensyncio
==============

Utility functions for asyncio which Stephan wished where in the stdlib
but aren't.

wrap_future(f)
--------------

Takes a callable f which returns an awaitable, and returns a callable
which wraps the awaitable in asyncio.ensure_future.

Can also be used as a decorator, especially with coroutine functions:

        @wrap_future
        async def foo(arg1, arg2):
            ...

transform_future(f, awaitable)
------------------------------

Apply a function to the result of an awaitable, return a future which
delivers the result.

iawait(awaitable)
-----------------

"Interactive await" -- Run default eventloop until awaitable has
completed. Mainly useful for interactive experimentation.



