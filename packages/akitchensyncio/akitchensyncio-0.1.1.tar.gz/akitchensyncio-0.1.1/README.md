# akitchensyncio
Utility functions for asyncio which Stephan wished where in the stdlib but aren't.

Requires a Python version which supports the `async` syntax (Python 3.5 or higher).


# Installation

To install akitchensyncio, simply:

```bash
$ pip install akitchensyncio
```

## Function `wrap_future(f)`

Takes a callable `f` which returns an awaitable,
and returns a callable which wraps the awaitable in
`asyncio.ensure_future`.

Can also be used as a decorator, especially
with coroutine functions:

```python
@wrap_future
async def foo(arg1, arg2):
    ...
```

This is especially useful in combination with `functools.lru_cache`.
Suppose you have a coroutine function which does an asynchronous query,
and you decide you want to introduce some caching. Just add two decorators
as follows.

```python
@functools.lru_cache(100)
@wrap_future
async def do_some_query(arg1, arg2):
    ...
```


## Function `transform_future(f, awaitable)`

Apply a function to the result of an awaitable,
return a future which delivers the result.

As an example, suppose you have a way to query addresses
given names. The API takes a bunch of names rather than a single
one to reduce overhead. However, to your callers you would like
to hand out futures representing results for individual names.

Essentially you want to turn a "future resulting in a dict"
into a "dict containing futures". Kind of the opposite of `async.gather`.

```python
from operator import itemgetter

def query_addresses(names):
   fut = do_bunched_address_query(names)
   # fut is a single future which resolves
   # into a dict mapping names to addresses.
   return {name: transform_future(itemgetter(name), fut) for name in names}
```

## Function `iawait(awaitable)`

"Interactive await" -- Run default eventloop until awaitable has completed.
Mainly useful for interactive experimentation.

Then remove the "i" from `iawait` to get code which you can use in 
an `async def` function.

An alternative is to put this in your `~/.pythonrc.py`:

```python
def iawait(x):
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(x)
```

This will only import `asyncio` on first use of `iawait`, so
it won't slow down your startup in general.
