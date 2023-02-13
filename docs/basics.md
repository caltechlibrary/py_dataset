
[up](./)

## Basics

`py_dataset` is the python version of [dataset](https://caltechlibrary.github.io/dataset). dataset is a way of storing and organazing JSON documents
on disc. To use `py_dataset` we usually import it using Python's 
"from" syntax.

## A preamble to dataset usage

```
    from py_dataset import dataset
```

This provides a `dataset` object to work with dataset collections.


## An example

This is an example of creating a dataset called *fiends.ds*, saving
a record called "littlefreda.json" and reading it back.

```python
    import sys
    import json
    from py_dataset import dataset

    # Creating our friends.ds dataset collection for the first time.
    c_name = 'friends.ds'
    if not dataset.init(c_name, dsn = ""):
        print(dataset.error_message())
        sys.exit(1)

    # Now let's add something to our collection.
    key = 'littlefreda'
    record = {"name":"Freda","email":"little.freda@inverness.example.org"}
    if not dataset.create(c_name, key, record):
        print(dataset.error_message())
        sys.exit(1)

    # We should have at least one record in our collection.
    # This is the idiom for iterating and working with our collection
    # objects.
    keys = dataset.keys(c_name)
    for key in keys:
        p = dataset.path(c_name, key)
        print(p)
        # NOTE: the "read" method returns a touple!
        record, err := dataset.read(c_name, key)
        if err != '':
            print(f"read error, {err}")
            sys.exit(1)
        print(f"Doc: {record}")
```

The command `dataset.init(c_name, dsn = "")`, `dataset.keys(c_name)`, 
`dataset.read(c_name, key)` `dataset.create(c_name, key)` are the
main actors here.  Most dataset methods require 
the collection name as the first parameter.  Likewise many return
some sort of value. If it is a boolean value than True means
success and False means failure.  If the method returns data then
often it will be returned as a touple like with `read()`.
If an error has occurred (e.g. permissions on disc raising a problem)
you can retrieve the dataset error message by using the `error_message()`
function.  If you're done with the error you can use `error_clear()`
to reset the error message queue.

Now check to see if the key, littlefreda, is in the collection

```python
   dataset.has_key(c_name, 'littlefreda')
```

You can also read your JSON formatted data from a file 
but you need to convert it first to a Python dict.
In theses examples we are creating for Mojo Sam
and Capt. Jack then reading back all the keys
and displaying their paths and the JSON document
created.

```python
    with open("mojosam.json") as f:
        src = f.read().encoding('utf-8')
        dataset.create(c_name, "mojosam", json.loads(src))

   with open("capt-jack.json") as f:
      src = f.read()
      dataset.create("capt-jack", json.loads(src))

   for key in dataset.keys(c_name):
        print(f"Path: {dataset.path(c_name, key)}")
        print(f"Doc: {dataset.read(c_name, key)}")
        print("")
```

NOTE: In v2 of dataset there is no internal mechansim for filting
and sorta keys. If you need that you should create a data frame,
read the data frame out and manipulate it.  Internal sorting and
filtering just proved too slow.

