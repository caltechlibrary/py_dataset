
# Release note for v0.1.3 release

## Dropped integrations

The following features were dropped in recent versions
of dataset and that is now reflected in py_dataset.

+ Google Sheet integration
+ S3 and Google Cloud Storage support

## Dropped functions

+ `grid()` has been dropped for effeciency reasons, instead create a frame and use `frame_grid()`

## Changed function names

+ `frame()` (for creation) became `frame_create()`
+ `frame()` (for reading) returns whole frame with all metadata
+ `frame_objects()` returns the a list of objects in the frame
+ `frame_grid()` returns a 2D list of a frames objects.
+ `keys()` now returns all keys in the collection
+ `keys()` for filtering and sorting became `key_filter()` and `key_sort()`

## Changes in return values

For functions that returned only an error message the return values
have changed to True for success and False otherwise. You can retrieve
the error text using the `error_message()` function. This was a
simplification.

Old code shape

```
    err = dataset.init('things.ds')
    if err != '':
        print(err)
```

New code shape

```
    if dataset.init('things.ds') == False:
        print(dataset.error_message())
```

Changed functions include `init()`, `create()`, `update()`, `delete()`,
`detach()`, `prune()`, `join()`, `frame_reframe()`, `frame_refresh()`, 

Functions that returned a touple of object and err string will work the
same as before (e.g. `read()`, `read_list()`, `frame_objects()`).

