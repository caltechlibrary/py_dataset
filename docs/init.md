
[up](./)

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
    dsn = "" # Use a pairtree to store the collection.
    if not dataset.init(c_name, dsn):
        print(dataset.error_message())
```

At this point you should have a directory (folder) on your file
system called "things.ds" it will contain a collection.json file and
several other JSON documents for managing the collection.

## Annotating your collection with metadata

When you create a new collection a "codemeta.json" file is created
and placed in the root folder along side the "collection.json" file.
You can edit the codemeta.json file directory to maintain metadata
about the collection itself.

