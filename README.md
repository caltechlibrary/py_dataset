
# py_dataset   [![DOI](https://data.caltech.edu/badge/175684474.svg)](https://data.caltech.edu/badge/latestdoi/175684474)

py_dataset is a Python wrapper for the [dataset](https://github.com/caltechlibrary/dataset) 
libdataset a C shared library for working with 
[JSON](https://en.wikipedia.org/wiki/JSON) objects as collections. 
Collections can be stored on disc or in Cloud Storage.  JSON objects 
are stored in collections using a pairtree as plain UTF-8 text files.
This means the objects can be accessed with common 
Unix text processing tools as well as most programming languages.

This package wraps all [dataset](docs/) operations such 
as initialization of collections, creation, 
reading, updating and deleting JSON objects in the collection. Some of 
its enhanced features include the ability to generate data 
[frames](docs/frame.html) as well as the ability to 
import and export JSON objects to and from CSV files.

py_dataset is release under a [BSD](LICENSE) style license.

## Features

[dataset](docs/) supports 

- Basic storage actions ([create](docs/create.html), [read](docs/read.html), [update](docs/update.html) and [delete](docs/delete.html))
- listing of collection [keys](docs/keys.html) (including filtering and sorting)
- import/export  of [CSV](docs/csv.html) files.
- The ability to reshape data by performing simple object [join](docs/join.html)
- The ability to create data [frames](docs/frames.html) from collections based on keys lists and [dot paths](docs/dotpath.html) into the JSON objects stored

See [docs](docs/) for detials.

### Limitations of _dataset_

_dataset_ has many limitations, some are listed below

- it is not a multi-process, multi-user data store (it's files on "disc" without locking)
- it is not a replacement for a repository management system
- it is not a general purpose database system
- it does not supply version control on collections or objects

## Install

Available via pip `pip install py_dataset` or by downloading this repo and
typing `python setup.py install`. This repo includes dataset shared C libraries
compiled for Windows, Mac, and Linux and the appripriate library will be used
automatically.

## Quick Tutorial

This module provides the functionality of the _dataset_ command line tool as a Python 3.8 module.
Once installed try out the following commands to see if everything is in order (or to get familier with
_dataset_).

The "#" comments don't have to be typed in, they are there to explain the commands as your type them.
Start the tour by launching Python3 in interactive mode.

```shell
    python3
```

Then run the following Python commands.

```python
    from py_dataset import dataset
    # Almost all the commands require the collection_name as first paramter, 
    # we're storing that name in c_name for convienence.
    c_name = "a_tour_of_dataset.ds"

    # Let's create our a dataset collection. We use the method called 
    # 'init' it returns True on success or False otherwise.
    dataset.init(c_name)

    # Let's check to see if our collection to exists, True it exists
    # False if it doesn't.
    dataset.status(c_name)

    # Let's count the records in our collection (should be zero)
    cnt = dataset.count(c_name)
    print(cnt)

    # Let's read all the keys in the collection (should be an empty list)
    keys = dataset.keys(c_name)
    print(keys)

    # Now let's add a record to our collection. To create a record we need to know
    # this collection name (e.g. c_name), the key (most be string) and have a 
    # record (i.e. a dict literal or variable)
    key = "one"
    record = {"one": 1}
    # If create returns False, we can check the last error message 
    # with the 'error_message' method
    if not dataset.create(c_name, key, record):
        print(dataset.error_message())

    # Let's count and list the keys in our collection, we should see a count of '1' and a key of 'one'
    dataset.count(c_name)
    keys = dataset.keys(c_name)
    print(keys)

    # We can read the record we stored using the 'read' method.
    new_record, err = dataset.read(c_name, key)
    if err != '':
        print(err)
    else:
        print(new_record)

    # Let's modify new_record and update the record in our collection
    new_record["two"] = 2
    if not dataset.update(c_name, key, new_record):
        print(dataset.error_message())

    # Let's print out the record we stored using read method
    # read returns a touple so we're printing the first one.
    print(dataset.read(c_name, key)[0])

    # Finally we can remove (delete) a record from our collection
    if not dataset.delete(c_name, key):
        print(dataset.error_message())

    # We should not have a count of Zero records
    cnt = dataset.count(c_name)
    print(cnt)
```
