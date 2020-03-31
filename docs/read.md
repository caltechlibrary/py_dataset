
[up](./)

# read

The `read()` method retrieves an existing object from a collection
returning the JSON document as a Python Dict. Actually `read()`
returns a touple made of a python dict and an error message.
If no error then the error message is an empty string.

An example we're assuming there is a JSON document with a KEY 
of "r1". Our collection name is "data.ds"

```shell
    c_name = 'data.ds'
    key = 'r1'
    obj, err = dataset.read(c_name, key)
    if err != '':
        print(err)
    else:
        print(obj)
```

