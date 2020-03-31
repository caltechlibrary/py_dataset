
[up](./)

# delete

Remove an object from a dataset collection.

We need our usual pre-amble before using dataset.

```python
    from py_dataset import dataset
```

Assuming that was done then our Python code is pretty simple to
remove an object from a collection.

```python
    c_name = 'things.ds'
    key = 'thing-one'
    if not dataset.delete(c_name, key):
        err = dataset.error_message()
        print(f'failed to delete {key} from {c_name}, {err}')
```

Note that 'thing-one' must exist in the collection 'things.ds'.
If not the `delete()` method returns False and you should
hanlde the error.

We can confirm the deletion with `has_key()`

```python
    if not dataset.has_key(c_name, key):
        print('somthing went wrong')
```

