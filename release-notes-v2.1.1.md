

# changes

# function signatures and names

- `key_exists()` is renamed `has_key()`
- `frame_exists()` is renamed `has_frame()`
- `init()` now takes two parameters, the second one is a DSN (data name source, to use a SQL store instead of a pairtree)
- `version()` is renamed `dataset_version()` to get the dataset version used for the library
- `clone()`, `clone_sample()` now include dsn parameters after the collection names, you can clone into a different storage engine (e.g. Pairtree or SQL store).

# behaviors

- `delete()` removes all versions of an object
- `prune()` removes all attachment versions 
- `path()` will return the path to a JSON document for collections using pairtree storage, otherwise it'll return an empty string

# versioning has been overhauled in v2 of dataset

Versioning is handle very differently in dataset v2.x than v1.x. The JSON objects stored can be versioned automatically based on the collection's versioning setting. Versions are incremented automatically on create, update and attach for both JSON documents and attachments. Both `delete()` and `prune()` remove all objects including all versions of objects. This is because systems that version things tend to need "tomb stone" objects and placeholders.

# additions

- `read_version()` will retrieve a specific version of a JSON object
- `object_versions()` will retrieve a list of object versions available
- `attachment_versions()` will list of versions of an attachment
- `detach_version()` will retrieve a specific version of an attachment
- `set_versioning()` will set versioning for a collection
- `get_versioning()` will get the current versioning setting for a collection

# What was left out

The methods related to Namaste data have not be implememented as
v2 of dataset. Instead retrieve the codemeta.json file in the 
collection for metadata about the collection itself.


# Misc

Some tests fail on Windows 10 for libdataset. These will be addressed
in future releases.
