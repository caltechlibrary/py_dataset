
# Developer notes for py_dataset

py_dataset wraps [dataset](https://github.com/caltechlibrary/dataset)'s libdataset. We try to keep the version of py_dataset in sync with the current release of dataset. ~~libdataset. When a new version of _dataset_ and _libdataset_ are release fetch the `libdataset-*.zip` archives and unzip them in `py_dataset/lib`. This should leave you with `libdataset.so` (Linux), `libdataset.dylib` (Mac OS X) and `libdataset.dll` (Windows) as well as `libdataset.h` (same for all three platforms). You will need to update `py_dataset/dataset.py` to include any changes you want to reflect in the shared library (e.g. add new functions). Once those twothings have been done you can use `python setup.py` to install your updates locally and test.~~

For patches between dataset release we append a period and patch value to the semver that matched dataset's release. E.g. the first patch to py_dataset paired with dataset 2.2.3 release would be 2.2.3.1. The second 2.2.3.2, etc.

py_dataset is now built/managed using [uv](https://docs.astral.sh/uv/).

## Release process

+ ~~Update shared libraries in `py_dataset/lib` (e.g. `libdataset.so`, `libdataset.dynlib` and `libdataset.dll`)~~
+ Update `py_dataset/dataset.py` and `py_dataset/libdataset.py` as needed
+ Update version info in `codemeta.json` (e.g. `cme version releaseNotes dateModified datePublished -e`)
+ Update README.md and DEVELOPER-NOTES.md
+ Test and commit changes to the master branch in the git repo
    + `uv run python3 test_dataset.py`
+ Make a github release if you're happy with everything
+ [optional] Push changes up to pypy

