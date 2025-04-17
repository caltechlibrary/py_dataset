

# changes

The big change v2.2.1 was the last release supporting the C Shared library called libdataset. Starting with v2.2.2 libdataset.py wraps the dataset cli allowing the main dataset.py definition to remain the same.

This release of py_dataset no longer uses the C Shared library. Instead is requires that dataset v2.2.3 or better is installed on the system. It now wraps the command line dataset comment.

Several functions now return False due to the feature being depreciated in the past.  These include import/export of CSV data from frames, sync actions with csv data, frame grids, create_objects and update_objects (notice the plural). object_path always returns an empty string since Pairtree storage is no longer the default and will be phased out.

In the future additional support is planned to wrap the Dataset JSON API web service like was implemented in [ts_dataset](https://github.com/caltechlibrary/ts_dataset).

