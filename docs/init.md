
# initailizing a dataset collection

You can create a dataset collection from Python using the `init()`
function.  You need to provided a file system friendly dataset name.
Additional metadata can be added to the collection if you need it.

## Preamble

The standard approach for using dataset is using the `from`
notation for your import.  The examples code assumes you've
done this.

```python
    from py_dataset import dataset
```


## init()

We need to have a collection name, e.g. `things.ds`. The extension
".ds" is a convension and is not enforced by the dataset library.

```
    # We're going to save our collection name for latter
    c_name = 'things.ds' 
    if not dataset.init(c_name):
        print(dataset.error_message())
```

At this point you should have a directory (folder) on your file
system called "things.ds" it will contain a collection.json file.

## Annotating your collection with metadata

The library will try to guess some metadata about the collection
based on the environment where your script is running. E.g. 
it will use the current date and time to record when the collection
was created. On Unix-like systems it'll also add the creating
user as a creator of the collection.

Metadata for the collection is based around the concept in
libraries and archival software called "namaste" or Name as text.
This was pioneered by the developers at the California Digital Library.
See [Namaste](https://confluence.ucop.edu/display/Curation/Namaste).

`py_dataset` supports the following namaste style attributes --
who, what, when, where

```python
    dataset.set_who(c_name, "Jane Doe")
```

You can retreive this metadata with `get_who()`

```python
    who = dataset.get_who(c_name)
```

"whats", "when", "where" work as follows

