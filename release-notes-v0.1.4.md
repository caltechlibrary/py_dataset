
# Release note for v0.1.4

This release is done to match changes in v0.1.8 of dataset.
Changes include adding missing functions from libdataset.go
such as `is_collection_open()`, `frames()`, `close_collection()`,
`close_all_collections()` and `collections()`
and renamed `make_objects()` to `create_objects()` to reflect
name change in libdataset.go.

Some tests fail on Windows 10 for libdataset. These will be addressed 
in future releases.

