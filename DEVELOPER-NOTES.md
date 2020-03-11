
# Developer notes for py_dataset

py_dataset wraps [dataset](https://github.com/caltechlibrary/dataset)'s
libdataset. We try to keep the version of py_dataset in sync with the
current release of libdataset. When a new version of _dataset_ and 
_libdataset_ are release fetch the `libdataset-*.tar.gz` tarballs and 
untar them in `py_dataset/lib`. This should leave you with `libdataset.so` 
(Linux), `libdataset.dynlib` (Mac OS X) and `libdataset.dll` (Windows) 
as well as `libdataset.h` (same for all three platforms). You will need 
to update `py_dataset/dataset.py` to include any changes you want to
reflect in the shared library (e.g. add new functions). Once those two
things have been done you can use `python setup.py` to install your
updates locally and test.

## Release process

+ Update shared libraries in `py_dataset/lib` (e.g. `libdataset.so`, `libdataset.dynlib` and `libdataset.dll`)
+ Update `py_dataset/dataset.py` as needed
+ Update version number in `codemeta.json`
+ Test and commit changes to the master branch in the git repo
    + `python3 test\dataset_test.py`
+ Make a github release
+ Push changes up to pypy

