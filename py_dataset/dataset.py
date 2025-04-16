#!/usr/bin/env python3
# 
# libdataset is a wrapper around our C-Shared library of libdataset.go
# used for testing the C-Shared library functions.
# 
# @author Thomas E. (Tom) Morrell
# @author R. S. Doiel, <rsdoiel@caltech.edu>
#
# Copyright (c) 2023, Caltech
# All rights not granted herein are expressly reserved by Caltech.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
import json
import sys
import os
from . import libdataset

#
# These are our Python idiomatic functions
# calling the C type wrapped functions in libdataset.py
#

# error_clear() clears the errors previously set.
def error_clear():
    libdataset.error_clear()

# error_message() returns the current error message(s)
# accumulated.
def error_message():
    value = libdataset.error_message()
    if not isinstance(value, bytes):
        value = value.encode('utf-8')
    return value.decode()

# use_strict_dotpath() will trigger if False will prefix a root period
# for dot paths and labels when specified in function calls.
def use_strict_dotpath(on_off = True):
    return libdataset.use_strict_dotpath(True)

# is_verbose() returns true is verbose is enabled, false otherwise
def is_verbose():
    return libdataset.is_verbose()

# verbose_on() turns verboseness off
def verbose_on():
    return libdataset.verbose_on()

# verbose_off() turns verboseness on
def verbose_off():
    return libdataset.verbose_off()

# dataset_version() returns version of dataset 
# shared library semver.
def dataset_version():
    value = libdataset.dataset_version()
    if not isinstance(value, bytes):
        value = value.encode('utf-8')
    return value.decode() 

#
# Now write our Python idiomatic function
#

def collections():
    '''returns a list of open collections'''
    value = libdataset.collections()
    if not isinstance(value, bytes):
        value = value.encode('utf8')
    return json.loads(value.decode())


# Initializes a Dataset Collection
def init(collection_name, dsn = ""):
    '''initialize a dataset collection with the given name'''
    return libdataset.init_collection(collection_name, dsn)

# is_open checks to see if a dataset collection is already open
def is_open(collection_name):
    return libdataset.is_collection_open(c_char_p(collection_name.encode('utf8')))

# open opens a dataset collection (it needs to exist)
def open(collection_name):
    if libdataset.open_collection(c_char_p(collection_name.encode('utf8'))):
        return ''
    return error_message()

# close closes a dataset collection.
# NOTE: This function is here for legacy reasons.
# returns any accumulated error messages. RSD 2025-05-16
def close(collection_name):
    return error_message()

# close_all closes all open dataset collection. 
# NOTE: This function is here for legacy reasons.
# returns any accumulated error messages.  RSD 2025-05-16
def close_all():
    return error_message()

# Has key, checks if a key is in the dataset collection
def has_key(collection_name, key):
    return libdataset.has_key(collection_name, key)

# Create a JSON record in a Dataset Collectin
def create(collection_name, key, value):
    '''create a new JSON record in the collection based on collection name, record key and JSON string, returns True/False'''
    if isinstance(key, str) == False:
        key = f"{key}"
    if libdataset.create_object(collection_name, key, json.dumps(value)):
        return ''
    return error_message()
    
# Read a JSON record from a Dataset collection
def read(collection_name, key):
    '''read a JSON record from a collection with the given name and record key, returns a dict and an error string'''
    if not isinstance(key, str) == True:
        key = f"{key}"
    value = libdataset.read_object(collection_name, key)
    if not isinstance(value, bytes):
        value = value.encode('utf-8')
    rval = value.decode()
    if type(rval) is str:
        if rval == "":
            return {}, error_message()
        return json.loads(rval), ''
    return {}, f"Can't read {key} from {collection_name}, {error_message()}"
  

# object_versions returns a list of versions of a JSON record 
# in a dataset collection
def object_versions(collection_name, key):
    '''read a JSON record from a collection with the given name and record key, returns a dict and an error string'''
    if not isinstance(key, str) == True:
        key = f"{key}"
    value = libdataset.read_object_versions(collection_name, key)
    if not isinstance(value, bytes):
        value = value.encode('utf-8')
    rval = value.decode()
    if type(rval) is str:
        if rval == "":
            return {}, error_message()
        return json.loads(rval), ''
    return {}, f"Can't read {key} from {collection_name}, {error_message()}"
  

# read_version reads a JSON record from a Dataset collection using
# key and semver
def read_version(collection_name, key, semver):
    '''read a JSON record from a collection with the given key and semver, returns a dict and an error string'''
    if not isinstance(key, str) == True:
        key = f"{key}"
    value = libdataset.read_object(collection_name, key, semver)
    if not isinstance(value, bytes):
        value = value.encode('utf-8')
    rval = value.decode()
    if type(rval) is str:
        if rval == "":
            return {}, error_message()
        return json.loads(rval), ''
    return {}, f"Can't read {key} from {collection_name}, {error_message()}"
    
# Read a list of JSON records from a Dataset collection
# NOTE: this provides dataset cli behavior for reading back a list
# of records effeciently ...
def read_list(collection_name, keys, clean_object = False):
    # Pack our keys as an array of string
    l = []
    for key in keys:
        if not isinstance(key, str):
            key = f"{key}"
        l.append(key)
    # Generate our JSON version of they key list
    keys_as_json = json.dumps(l)
    value = libdataset.read_object_list(collection_name, keys_as_json, clean_object)
    if not isinstance(value, bytes):
        value = value.encode('utf-8')
    rval = value.decode()
    if isinstance(rval, str):
        if rval == "":
            return [], error_message()
        return json.loads(rval), error_message()
    return [], f"Can't read {keys} from {collection_name}, {error_message()}"



# Update a JSON record from a Dataset collection
def update(collection_name, key, value):
    '''update a JSON record from a collection with the given name, record key, JSON string returning True/False'''
    if not isinstance(key, str) == True:
        key = f"{key}"
    if libdataset.update_object(collection_name, key, json.dumps(value)):
        return ''
    return error_message()

# Delete a JSON record from a Dataset collection
def delete(collection_name, key):
    '''delete a JSON record (and any attachments) from a collection with the collectin name and record key, returning True/False'''
    if not isinstance(key, str) == True:
        key = f"{key}"
    if libdataset.delete_object(collection_name, key.encode('utf8')):
        return ''
    return error_message()

# Keys returns a list of keys from a collection optionally applying a filter or sort expression
def keys(collection_name):
    '''keys returns an unsorted list of keys for a collection'''
    return libdataset.keys(collection_name)
    
# Count returns an integer of the number of keys in a collection
def count(collection_name, filter = ''):
    '''count returns an integer of the number of keys in a collection'''
    return libdataset.count_objects(collection_name, filter)



#
# import_csv - import a CSV file into a collection
# syntax: COLLECTION CSV_FILENAME ID_COL
# 
# options:
#
#      use_header_row (bool)
#      overwrite (bool)
# 
# Returns: error string
def import_csv(collection_name, csv_name, id_col, use_header_row = True, overwrite = False):
    if libdataset.import_csv(collection_name, csv_name, id_col, use_header_row, overwrite):
        return ''
    return error_message()

#
# export_csv - export collection objects as a frame to a CSV file
# syntax: COLLECTION FRAME CSV_FILENAME
# 
# Returns: error string
def export_csv(collection_name, frame_name, csv_name):
    if libdataset.export_csv(collection_name, frame_name, csv_name):
        return ''
    return error_message()

def status(collection_name):
    return libdataset.collection_exists(collection_name)

def list(collection_name, keys = []):
    return libdataset.list_objects(collection_name, keys)
 
def path(collection_name, key):
    value = libdataset.object_path(collection_name, key)
    if not isinstance(value, bytes):
        value = value.encode('utf8')
    return value.decode()

def check(collection_name):
    ok = libdataset.check_collection(collection_name)
    return (ok == True)

def repair(collection_name):
    return libdataset.repair_collection(collection_name)

def attach(collection_name, key, filenames = []):
    return libdataset.attach(collection_name, key, filenames)
    
def attachments(collection_name, key):
    return libdataset.attachments(collection_name, key)

def detach(collection_name, key, filenames = []):
    '''Get attachments for a specific key.  If the version semver is not provided, it will default to the current version.  Provide [] as filenames if you want to get all attachments'''
    if len(filenames) == 0:
        filenames = attachments(collection_name, key)
    return libdataset.detach(collection_name, key, filenames)

def detach_version(collection_name, key, filenames = [], semver = ''):
    '''Get attachments for a specific key.  If the version semver is not provided, it will default to the current version.  Provide [] as filenames if you want to get all attachments'''
    if len(filenames) == 0:
        filenames = attachments(collection_name, key)
    return libdataset.detach_version(collection_name, key, semver, filenames)


def prune(collection_name, key, filenames = []):
    '''Delete attachments for a specific key.  If the version semver is not provided, it will default to the current version.  Provide [] as filenames if you want to delete all attachments'''
    if len(filenames) == 0:
        filenames = attachments(collection_name, key)
    return libdataset.prune(collection_name, key, filenames)

def join(collection_name, key, obj = {}, overwrite = False):
    return libdataset.join_objects(collection_name, key, obj, overwrite)

def clone(collection_name, keys, destination_name):
    return libdataset.clone_collection(collection_name, keys, destination_name)

def clone_sample(collection_name, training_name, training_dsn = "", test_name = "", test_dsn = "", sample_size = 0):
    return libdataset.clone_sample(collection_name, training_name, training_dsn, test_name, test_dsn, sample_size)

def frame_create(collection_name, frame_name, keys, dot_paths, labels):
    return libdataset.frame_create(collection_name, frame_name, keys, dot_paths, labels)

def has_frame(collection_name, frame_name):
    return libdataset.has_frame(collection_name, frame_name)

def frame_keys(collection_name, frame_name):
    return libdataset.frame_keys(collection_name, frame_name)


def frame(collection_name, frame_name):
    return libdataset.frame(collection_name, frame_name)
    
def frame_objects(collection_name, frame_name):
    return libdataset.frame_objects(collection_name, frame_name)

def frame_names(collection_name):
    return libdataset.frame_names(collection_name)

def frame_reframe(collection_name, frame_name, keys = []):
    return libdataset.frame_reframe(collection_name, frame_name, keys)

def frame_refresh(collection_name, frame_name):
    return libdataset.frame_refresh(collection_name, frame_name)

def frame_clear(collection_name, frame_name):
    return libdataset.frame_clear(collection_name, frame_name)

def delete_frame(collection_name, frame_name):
    return libdataset.frame_delete(collection_name, frame_name)

def frame_grid(collection_name, frame_name, include_headers = True):
    throw('frame_grid has been removed.')

def sync_recieve_csv(collection_name, frame_name, csv_filename, overwrite = False):
    return libdataset.sync_recieve_csv(collection_name, frame_name, csv_filename, overwrite)

def sync_send_csv(collection_name, frame_name, csv_filename, overwrite = False):
    return libdataset.sync_send_csv(collection_name, frame_name, csv_filename, overwrite)

def create_objects(collection_name, keys, default_object):
    c_name = collection_name
    keys_as_json = json.dumps(keys)
    object_as_json = json.dumps(default_object)
    return libdataset.create_objects(c_name, keys_as_json, object_as_json)

def update_objects(collection_name, keys, objects):
    c_name = collection_name
    keys_as_json = json.dumps(keys)
    objects_as_json = json.dumps(objects)
    return libdataset.update_objects(c_name, keys_as_json, objects_as_json)

# get_version gets the versioning status of a collection
# returned values are "", "patch", "minor" or "major"
# An empty string means the collection isn't using versioning.
def get_version(collection_name):
    return libdataset.get_version(collection_name)

# set_version sets the versioning status for a collection
# Accepted values for versioning are  "", "none", "patch", 
# "minor" or "major"
def set_version(collection_name, versioning = ""):
    return libdataset.set_version(collection_name, versioning)

