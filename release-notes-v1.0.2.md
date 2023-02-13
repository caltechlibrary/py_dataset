
# Release note for v1.0.2 release

## Changed integrations

The v2 development branch saw fundamental changed to the operation of dataset collection. It was a substantial rewrite of v1 abstracting how JSON objects are stored and versioned.  v2 of datasat supports storing the JSON objects in a pairtree as well as leveraging SQL JSON support in SQLite3, MySQL 8 and PostgreSQL 14. 

The v2 development branch of dataset supports a different approach to version. This versioning can happen for both dataset records and for attachments. Version if enabled isn't intended to be directly manipulated from libdataset derived libraries. The versioning approach is highly experimental and will likely change implementation in the v2 branch as it gets used or abandoned. Versioning itself is set at the collection level, impacts both attachments and the JSON objects stored and will increment the version numbers either at the patch, minor or major semver values across the collection. Ideally if versioning is enabled (it is not by default) versioning happens automatically.


The metadata JSON documents in the root collection folder have significantly changed between v1 and v2 of dataset.  Metadata about the collection itself is now stored as a codemeta.json file in the root folder. Metadata needed to operation dataset is stored in a document called "collection.json". There is a pairtree supporting storage of attachments called "attachments", attachments can be versioned. There is a directory called "frames" that stores data frames.

In dataset v2 the objects stored are no longer modified to include references to attachments and keys. If you need need explicit id attributes you need to modify the object before calling create or update. This means some of the conformance testing has changed.

Since the `_Key` value is no longer injected into the object you need to provide data frames with an explicit object id if you wish that data exposed in the frame.

## Dropped integrations

py_dataset no longer supports the v1.1 branch of dataset development. It now supports v2 branch of dataset development with the re-introduction of libdataset in v2.1.  This allows us to integrate both a pairtree storage system for curating JSON document collections as well as use SQL engines supporting JSON columns such as SQLite 3, MySQL 8 and recent versions of PostgreSQL.

## Changed function names

- `init()` now takes two parameters, the first is the name of collection the second is a "dsn" value (i.e data source name as URI). If the dsn value is an empty string init will create a pairtree store collection (similar to v1 dataset collections). If a dsn URL is passed then it store the JSON documents in a SQL JSON column. Currently SQLite3, MySQL 8 and PostgreSQL 14 are supported. The attachements and frames are defined in the file system but under different directories than in v1 dataset.
- `frames()` (for listing available frames) became `frame_names()`
- `frame_exists()` (for checking if a frame is defined) became `has_frame()`
- `key_exists()` (for checking if a key is defined) became `has_key()`
- `read()` nolonger takes a third parameter for `clean_object`, in v2 of dataset the JSON stored is NOT modified on create or update.

## Changes in return values

- `doc_path()` returns an empty string for non-pairtree dataset v2 collections (there is no document path since the JSON document is stored in a relational database).
- `get_version()` returns the dataset version used to create/manage a collection, not the collection's own version. Metadata for a collection is maintained in a codemeta.json document in the collection's root folder.

## Dropped functions

- `key_filter()` and `key_sort()` have been removed to changes in collections and additional storage systems (e.g. pairtree stores and sql JSON stores)
_ `make_objects()` is dropped, use `create_objects` instead
- `set_version()` is dropped, Namaste isn't being used for collection metadata, update the codemeta.json file instead
- `set_who()`, `set_what()`, `set_where()`, `get_who()`, `get_what()` and `get_when()` dropped, Namaste isn't being used for metadata on collections, update the codemeta.json file instread
- `frame_grid()` has been dropped, work with frame lists and do you table conversion in Python (e.g. use Python's excellent data science libraries)
