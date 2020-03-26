
# keys

Keys are used to add, update and retrieve JSON objects in your
dataset collection. Individual keys must be unique.  But how
do you know what keys are in the collection? Use the `keys()`
method.

```python
    c_name = "characters.ds"
    keys = dataset.keys(c_name)
```

Keys would now have all the keys in the collection named "characters.ds".
It is important to know that keys just returns the whole list.
If you want a sorted list or a filtered list then you'll want to 
use the `key_filter()` and `key_sort()` methods.


