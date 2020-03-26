
# create

The `create()` method will add a new object to a collection.
The collection needs to exist and the "key" used for the object
needs to be unique.

We assume our standard preamble.

```python
   from py_dataset import dataset 
```

## Creating a new object.

We need three things, the collection name (e.g. "things.ds"),
a key (e.g. "thing-one"), and a python dict which will become
our JSON object on disc (e.g. `{"one": 1}`).

```python
    c_name = "things.ds"
    key = "thing-one"
    obj = {"one": 1}
    # let's create our object and display any errors
    if not dataset.create(c_name, key, obj):
        print(dataset.error_message())
    # Let's see if our object exists?
    if dataset.has_key(c_name, key):
        print("Our object exists!")
```

Note if you try to use the same key to store another object
you'll get an error.

```
    obj2 = {"two": 2}
    if not dataset.create(c_name, key, obj2):
        print(f"We should see an error {dataset.error_message()}")
```

