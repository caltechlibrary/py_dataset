
[up](./)

## Joining Objects

You can augment JSON key/value pairs for a JSON document in your 
collection using the join operation. This works similar to the datatools 
cli called jsonjoin.

In this example our collection is called *people.ds*.  Let's assume you 
have a record in your collection with a key 'jane.doe'. It has three 
fields - name, email, age.

```json
    {"name":"Doe, Jane", "email": "jd@example.org", "age": 42}
```

You also have an external JSON document called profile.json. It looks 
like

```json
    {"name": "Doe, Jane", "email": "jane.doe@example.edu", "bio": "world renowned geophysist"}
```

You can merge the unique fields in profile.json with your existing 
jane.doe record

```python
    c_name = "people.ds"
    key = "jane.doe"
    profile = {"name":"Doe, Jane", "email": "jd@example.org", "age": 42}
    # First create our object, then we'll join more data.
    dataset.create(c_name, key, profile)
    new_profile = {"name": "Doe, Jane", "email": "jane.doe@example.edu", "bio": "world renowned geophysist"}
    dataset.join(c_name, key, new_profile)
```

The result would look like

```json
    {"name":"Doe, Jane", "email": "jd@example.org", "age": 42, "bio": "renowned geophysist"}
```

If you wanted to overwrite the common fields you would use 'join overwrite'

```python
    dataset.join(c_name, key, new_profile, overwrite = True)
```

Which would result in a record like

```json
    {"name":"Doe, Jane", "email": "jane.doe@example.edu", "age": 42, "bio": "renowned geophysist"}
```

