
# update


`update()` method will replace a JSON document in a dataset collection 
for a given KEY.  

Let's assume our JSON document contains `{"name":"Jane Doe"}` and the 
KEY is "jane.doe" and our collection name is "people.ds". 

```python
    c_name = "people.ds"
    key = "jane.doe"
    obj = {"name":"Jane Doiel"}
    if not dataset.update(c_name, key_obj):
        print(dataset.error_message()
```

The `update()` method returns True on success or False otherwise.


