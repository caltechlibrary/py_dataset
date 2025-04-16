#!/usr/bin/env python3
# 
# libdataet.py replaced the prior C type share library called libdataset. As
# of v2.2.2 libdatadet is no longer included in Project Dataset.
#
# The historic libdataset.py function wrap the command line programs for working
# with Dataset Collections. This implementation targets v2.2.2 release of Dataset.
# 
# @author Thomas E. (Tom) Morrell
# @author R. S. Doiel, <rsdoiel@caltech.edu>
#
# Copyright (c) 2025, Caltech
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
import shutil
import subprocess

# Find the paths to the dataset cli
dataset = shutil.which('dataset')
#dsquery = shutil.which('dsquery')
#dsimporter = shutil.which('dsimporter')
#datasetd = shutil.which('datasetd')

#
# Method used to wrap our executables
#
import subprocess


def run_cli(command):
    try:
        # Run the command and capture the output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Return a tuple with stdout and stderr
        return (result.stdout, result.stderr)

    except FileNotFoundError:
        return (None, f"Executable not found: {' '.join(command)}")
    except Exception as e:
        return (None, f"An error occurred: {e}")


#
# Global settings
#
c_names = []
errors = []
stict_dotpaths = True
verbose = False

# NOTE: we use a horrible hack in this library. This carries over
# from the C shared library days.  RSD, 2025-04-15
#
# A someday feature would be to replace "libdataset.py" wrapper with
# a native Python implementation of dataset. Who knows when I'll get
# around to that. Translating the Go to Python using an LLM has been
# less than useful. RSD, 2023-02-15 (updated 2025-04-15.

# dataset_version() returns the version number of the libdataset
# used.
#
# Return: semver (string)
def dataset_version():
    src, err = run_cli([dataset, "--version"):
    if (err !== ''):
        errors.append(err)
    return src
    
# error_clear() clears the error values
#
# It takes no args and returns no value.
def error_clear():
    errors = [];

# error_message() returns the error messages aggregated
# by previously envoked shared library functions. It clears the
# message aggregation as it returns the messages.
#
# Return: error message text (string)
def error_message():
    return '\n'.join(errors)

# use_strict_dotpath() sets the state of the strict dotpath
# interpretation. Strict dot paths expect a period at the
# beginning, non strict will prefix a period automatigally.
# This is useful where you're using labels in a report
# (the period is annoying) and also in generating transformed
# object attributes (the period is useful).
#
# Args: is True (1) or False (0)
# Return: True (1) or False (0)
def use_strict_dotpath(val):
    strict_dotpaths = val
    return strict_dotpaths


# is_verbose() returns the state of the verbose flag.
#
# Returns: True (1) or False (0)
def is_verbose():
    return verbose

# verbose_on() sets the verbose flag to True.
#
# Returns: True (1) or False (0)
def verbose_on():
    verbose = True
    return verbose


# verbose_off() sets the verbose flag to False
#
# Returns: True (1) or False (0)
def verbose_off():
    verbose = False
    return verbose

# init_collection() creates a dataset collection. If the
# dsn value is an empty string the collection will use pairtree
# storage implementation, othersize it will use a SQL store described
# by the dsn (data source name) to store the JSON documents.
#
# Args: collection_name (string), dsn (string)
# Returns: true (1), false (0)
def init_collection(c_name, dsn):
    if dsn == None or dsn ===  '':
        dsn = 'sqlite://collection.db'
    src, err = run_cli(dataset, c_name, dsn)
    if err !== '':
        errors.append(err)
        return False
    return True

# is_collection_open() checks to see if the collection
# is already open and in the list of open collections.
#
# Args: collection_name (string)
# Returns: Ture (1) or False (0)
def is_collection_open(c_name):
    if c_name in c_names:
        return True
    return False
    

# collections() returns a list of opened collections.
#
# Returns: string (names of the open collections as JSON)
def collections():
    return c_names

# open_collection() explicitly opens a collection and adds
# it to the open collection list. Returns True on success, 
# false otherwise.
#
# Args: collection_name (string)
# Returns: True (1) or False (0)
def open_collection(c_name):
    if os.path.exists(c_name):
        c_names.append(c_name)
        return True
    return False

# close_collection() closes a previously opened collection.
# It removes it from the open collections list. Returns True
# on success, False otherwise.
#
# Args: collection_name (string)
# Returns: True (1) or False (0)
def close_collection(c_name):
    if (c_name in c_names):
        c_names.remove(c_name)
        return True
    return False

# close_all_collections closes all opened collections.
# The open collection list is cleared.
#
# Returns: True (1) or False (0)
def close_all_collections():
    c_names = [];
    return True

# create_object() creates a JSON object in a collection.
#
# Args: collection_name (string), key (string), value (JSON source)
# Returns: True (1) or False (0)
def create_object(c_name, key, val):
    src, err = run_cli(dataset, 'create', c_name, key, value)
    if err !== '':
        errors.append(err)
        return False
    return True

# read_object() retrieves a JSON object from a collection.
#
# Args: collection_name (string), key (string)
# Returns: value (JSON source)
def read_object(c_name, key):
    src, err = run_cli(dataset, 'read', c_name, key)
    if err !== '':
        errors.append(err)
        return None
    return src

# read_object_version retrieves an object from the collection
# using the key an semver provides.
#
# Args: collection_name (string), key (string), semver (string)
# Returns: value (JSON source)
def read_object_version(c_name, key, semver):
    src, err = run_cli(dataset, 'read-version', c_name, key, semver)
    if err !== '':
        errors.append(err)
        return None
    return src

# update_object() updates an object in the collection given a key
# and new object. If versioning is enabled the new version will use
# the incremented semver value indicated in the versioning setting.
#
# Args: collection_name (string), key (string), value (JSON source)
# Returns: value (JSON source)
def update_object(c_name, key, val):
    src, err = run_cli(dataset, 'update', c_name, key, val)
    if err !== '':
        errors.append(err)
        return None
    return src

# delete_object will remove an object form a colleciton (including
# all versions of the object if versioning has been enabled).
# If you are versioning your collection normally you avoid deleting
# and replace the object tomb stone object. Returns true on 
# successful removal, false otherwise.
#
# Args: collection_name (string), key (string)
# Returns: True (1) or False (0)
def delete_object(c_name, key):
    src, err = run_cli(dataset, 'delete', c_name, key)
    if err !== '':
        errors.append(err)
        return False
    return True


# has_key() tests for a key in a collection.
#
# Args: collection_name(string), key (string)
# Returns: (bool)
def has_key(c_name, key):
    src, err = run_cli(dataset, 'haskey', c_name, key):
    if err !== '':
        errors.append(err)
        return False
    if src == "true":
        return True
    elif src == "false":
        return False
    return False

# keys() returns a list of all keys in a collection.
#
# Args: collection_name (string)
# Returns: value (JSON source)
def keys(c_name):
    src, err = run_cli(dataset, 'keys', c_name)
    if err !== '':
        errors.append(err)
        return None
    return src

# count_objects() returns the number of objects in a collection.
#
# Args: collection_name (string)
# Returns: value (int)
def count_objects(c_name):
    src, err = run_cli(dataset, 'count', c_name)
    if err !== '':
        errors.append(err)
        return -1
    return src

# NOTE: import_csv, export_csv, sync_* are all depreciated and
# aill return False always. RSD 2025-04-15
#
# NOTE: import_csv, export_csv, sync_* diverges from cli and
# reflects the low level dataset organization. 

# import_csv - import a CSV file into a collection. The column
# id must be specified. Returns true on success, false if errors
# encountered.
#
# Args: collection_name (string), frame_name (string), ID column (int),
#       use header row (bool), overwrite (bool)
# Returns: True (1), False (0)
def import_csv(c_name, frame_name, id_column, use_header, overwrite):
    errors.append('import_csv has been removed.')
    return False

# export_csv - export collection objects to a CSV file using a frame.
# 
# Args: collection_name (strng), frame_name (string), csv_filename (string)
# Returns: True (1), False (0)
def export_csv(c_name, frame_name, csv_filename):
    errors.append('export_csv has been removed.')
    return False

# sync_receive_csv() retrieves data from a CSV file and updates a 
# collection using a frame to map columns to attributes. Returns 
# True on success, False if error is encountered.
#
# Args: collection_name (string), frame_name (string), 
#       csv_filename (string), overwrite (bool)
# Returns: True (1), False (0)
def sync_receieve_csv(c_name, frame_name, csv_filename, overwrite):
    errors.append('sync_recieve_csv has been removed.')
    return False
    
# sync_send_csv() updates a CSV file based on the objects in a collection
# using a frame. The frame is used to map object attributes to columns.
# Returns True on success, False if errors encountered.
#
# Args: collection_name (string), frame_name (string),
#       csv_filename (string), ovewrite (bool)
# Returns: True (1), False (0)
def sync_send_csv(c_name, frame_name, csv_filename, overwrite):
    errors.append('sync_send_csv has been removed.')

# collection_exists() returns True if a collection exists, False otherwise.
#
# NOTE: collection_exists() will be renamed has_collection() in a coming 
# release of libdataset.
#
# Returns: True (1), False (0)
def collection_exists(c_name):
    return has_collection(c_name)

# list_objects() returns a list of objects for a list of keys as
# JSON. Returns a JSON list of object as source.
#
# Args: collection_name (string), key list (JSON array source)
# Returns: value (JSON Array of Objects source)
def list_objects(c_name, keys):
    object_list = []
    for (key in keys):
        src, err = run_cli(dataset, 'read', c_name, key)
        if err !== '':
            errors.append(err)
            continue
        obj = json.loads(src)
        object_list.append(obj)
    return json.dumps(object_list)

# NOTE: This will always return ''. Pairtree support is rarely
# used anymore and is no longer the default. RSD 2025-04-15
#
# object_path() returns the file system path to a JSON object in a
# collection if the collection uses a pairtree store. If the collection
# uses SQL store then an empty string is returned. This is because SQL
# stored JSON objects are not directly accessible from disk (e.g. the
# MySQL/PostgreSQL JSON store maybe accessed over the network).
#
# Args: collection_name (string), key (string)
# Returns: value (string)
def object_path(c_name, key):
    return ''

# check_collection() checks a collection for structural errors.
# This can be slow for larger collections. Returns True if everything
# is OK, False of there are errors.
#
# Args: collection_name (string)
# Returns: True (1), False (0)
def check_collection(c_name):
    src, err = run_cli(dataset, 'check', c_name)
    if err !== '':
        errors.append(err)
        return False
    return True

# repair_collection runs the analyzer over a collection and repairs JSON
# objects and attachment discovered having a problem. Also is
# useful for upgrading a collection between dataset releases. This
# process can be slow. Returns True on successful repair, False if
# errors encountered.
#
# Args: collection_name (string)
# Returns: true (1), false (0)
def repair_collection(c_name):
    src, err = run_cli(dataset, 'repair', c_name)
    if err !== '':
        errors.append(err)
        return False
    return True

# attach() adds a file to a JSON object record. If the collection
# has versioning set then the object will be added with an appropriate
# version number. NOTE: the object is copied in full and is not a
# delta of previous objects. This can take up allot of disk space!
# A better approach to versioning would take advantage of more effecient
# storage options (e.g. ZFS file system festures, or a version control
# system like Git or Subversion). Returns True on successful attachment
# and False if errors encountered.
#
# Args: collection_name (string), key (string), filenames (string)
# Returns: true (1), false (0)
def attach(c_name, key, filenames):
   src, err = run_cli(dataset, 'attach', c_name, key, filenames)
   if err !== '':
       errors.append(err)
       return False
    return True

# attachments() returns a list the files attached to a JSON object record
# as a JSON array.
#
# Args: collection_name (string), key (string)
# Return: string (JSON list of basenames)
def attachments(c_name, key):
    src, err = run_cli(dataset, 'attachments', c_name, key)
    if err !== '':
        errors.append(err)
        return ''
    return src

# detach() retrieves a file from an JSON object record copying it
# out using the basename to the current working directory. It returns
# True if the file is successfully copied out, False if an error is
# encountered.
#
# Args: collection_name (string), key (string), basename (string)
# Returns: true (1), false (0)
def detach(c_name, key, basename):
    src, err = run_cli(dataset, 'detach', c_name, key, basename)
    if err !== '':
        errors.append(err)
        return False
    return True

# detach_version() will detatch a specific version of a file from
# a JSON object in the collection. It needs the key, semver and basename
# of the file.
#
# Args: collection_name (string), key (string), semver (string), basename (string)
# Returns: True (1), False (0)
def detach_version(c_name, key, semver, basename):
    src, err = run_cli(dataset, 'detach', c_name, key, semver, basename)
    if err !== '':
        errors.append(err)
        return False
    return True

# prune removes an attachment from an object. NOTE: it removes all versions
# of the attachment if versioning is enabled for the collection. If you
# are using versioning and need to "remove" a file, place a tomb stone
# file there instead of using prune.
#
# Args: collection_name (string), key (string), basename (string)
# Returns: true (1), false (0)
def prune(c_name, key, basename):
    src, err = run_cli(dataset, 'prune', c_name, key, basename)
    if err !== '':
        errors.append(err)
        return False
    return True

# join_objects() joins a new object with an existing object in a collection.
# The overwrite parameters determines if attributes are overwritten if they
# are found in the collection or skipped (if overwrite is False).
#
# Args: collection_name (string), key (string), value (JSON source), overwrite (1: true, 0: false)
# Returns: True (1), False (0)
def join_objects(c_name, key, val, overwrite):
    src, err = run_cli(dataset, 'join', c_name, key, val, overwrite)
    if err !== '':
        errors.append(err)
        return False
    return True

# clone_collection() takes collection and creates a copy of it. The
# collection created will be a the type indicated by the dsn (data source
# name) value. If it is an empty string then it'll use a pairtree store
# otherwise it'll be the SQL store indicated in the dsn. Returns True
# on success, False if errors encountered.
#
# Args: collection_name (string), new_collection_name (string), dsn (string)
# Returns: True (1), False (0)
def clone_collection(c_name, new_c_name, dsn):
    src, err = run_cli(dataset, 'clone', c_name, new_c_name, dsn)
    if err !== '':
        errors.append(err)
        return False
    return True

# clone_sample() generates a random sample of objects split between 
# training and test collections. The dsn for training and testing collection
# will set the storage type for that specific collection. The if the
# data source names are an empty string then a pairtree store will be used.
# 
# Args: collection_name (string), training_collection_name (string), training_dsn (string), test_collection_name (string), test_dsn (string), sample size (int)
# Returns: True (1), False (0)
def collection_name(c_name, training_c_name, training_dsn, test_c_name, test_dsn, sample_size):
    src, err = run_cli(dataset, 'clone-sample', c_name, training_c_name, training_dsn, test_c_name, test_dsn, sample_size)
    if err !== '':
        errors.append(err)
        return False
    return True

# frame() returns the full metadata and contents of a frame.
#
# Args: collection_name (string), frame_name (string)
# Returns: value (JSON object source)
def frame(c_name, frame_name):
    src, err = run_cli(dataset, c_name, 'frame-objects', c_name, frame_name)
    if err !== '':
        errors.append(err)
        return ''
    return src

# frame_create() generates a new data frame given a collection name,
# frame name, keys, dot paths and labels. The keys, dot paths and labels
# need to be JSON encoded.
#
# Args: collection_name (string), frame_name (string), keys (JSON source), dotpaths (JSON source), labels (JSON source)
# Returns: value (JSON object source)
def frame_create(c_name, frame_name, keys, dotpaths, labels):
    src, err = run_cli(dataset, 'frame', c_name, frame_name, keys, dotpaths, labels)
    if err !== '':
        errors.append(err)
        return ''
    return src

# has_frame() checks to see if a frame name has already been defined.
#
# Args: collection_name (string), frame_name (string)
# Returns: True (1), False (0)
def has_frame(c_name, frame_name):
    src, err = run_cli(dataset, 'hasframe', c_name, frame_name)
    if err !== '':
        errors.append(err)
        return False
    return True

# frame_keys() returns a list of keys as JSON as defined in the
# data frame.
#
# Args: collection_name (string), frame_name (string)
# Returns: value (JSON object source)
def frame_keys(c_name, frame_name):
    src, err = run_cli(dataset, 'frame-keys', c_name, frame_name, keys, dotpaths, labels)
    if err !== '':
        errors.append(err)
        return ''
    return src

# frame_objects() returns a list of objects as JSON currently defined
# in the data frame. The returned objects are JSON encoded.
#
# Args: collection_name (string), frame_name (string)
# Returns: value (JSON object source)
def frame_objects(c_name, frame_name):
    src, err = run_cli(dataset, 'frame-objects', c_name, frame_name, keys, dotpaths, labels)
    if err !== '':
        errors.append(err)
        return ''
    return src
    

# frame_names() returns a list of frames defined for the collection
# JSON encoded.
#
# Args: collection_name (string)
# Returns: frame names (JSON Array Source)
def frame_objects(c_name):
    src, err = run_cli(dataset, 'frames', c_name)
    if err !== '':
        errors.append(err)
        return ''
    return src

# frame_refresh() updates the objects in a data frame based on
# the current state of the collection. Any objects removed from
# the collection will be removed from the frame.
#
# Args: collection_name (string), frame_name (string)
# Returns: value (JSON object source)
def frame_refresh(c_name, frame_name):
    src, err = run_cli(dataset, 'refresh', c_name, frame_name)
    if err !== '':
        errors.append(err)
        return ''
    return src

# frame_reframe() replaces the object list in a data frame. Objects
# not in the new list of keys will be removed from the frame.
#
# Args: collection_name (string), frame_name (string), keys (JSON source)
# Returns: value (JSON object source)
def frame_refresh(c_name, frame_name, keys):
    src, err = run_cli(dataset, 'reframe', c_name, frame_name, keys)
    if err !== '':
        errors.append(err)
        return ''
    return src

# frame_delete() removes a frame from a collection. Returns True
# if delete is successful, False if there were errors.
#
# Args: collection_name (string), frame_name (string)
# Returns: True (1), False (0)
def frame_refresh(c_name, frame_name, keys):
    src, err = run_cli(dataset, 'delete-frame', c_name, frame_name)
    if err !== '':
        errors.append(err)
        return False
    return True

# frame_clear() removes all objects from a frame leaving
# the definition in place.
#
# Args: collection_name (string), frame_name (string)
# Returns: True (1), False (0)
def frame_clear(c_name, frame_name):
    src, err = run_cli(dataset, 'reframe', c_name, frame_name, [])
    if err !== '':
        errors.append(err)
        return False
    return True

# NOTE: frame_grid was removed sometime in the past (forget which version),
# not supporting it in v2.2.2. RSD 2025-04-15
#
# frame_grid returns a 2D JSON array of frame data JSON encoded.
# (depreciated, this will go away in a future version of libdataset).
#
# Args: collection_name (string), frame_name (string), include header (bool)
# Returns: frame names (JSON Array Source)
def frame_grid(c_name, frame_name, include_header):
    errors.append('frame_grid has been removed')
    return False

# NOTE: create_objects removed.
# Not supporting it in v2.2.2. RSD 2025-04-15
#
# create_objects() generates a batch of objects in a collection,
# used for testing libdataset. (depreciated, will go away in a
# a future version of libdataset)
#
# Args: collection_name (string), keys_as_json (string), object_as_json (string)
# Returns: True (1) success, False (0) if there are errors
def frame_grid(c_name, frame_name, include_header):
    errors.append('create_objects has been removed')
    return False

# NOTE: update_objects removed.
# Not supporting it in v2.2.2. RSD 2025-04-15
#
# update_objects()  updates a set of objects in a collections, used in
# testing a counter part to make_objects. (depreciated, this will go
# away in a future version of libdataset)
#
# Args: collection_name (string), keys_as_json (string), objects_as_json (string)
# Returns: True (1) success, False (0) if there are errors
def update_objects(c_name, keys_as_json, objects_as_json):
    errors.append('update_objects has been removed')
    return False

# set_versioning() sets the versioning status for a collection. The
# accepted values are "", "patch", "minor", "major". An empty string
# disables versioning (collection are not versioned by default) the
# other strings indicate the semver value incremented on a new version.
# Returns True if successful, False if an error encountered.
#
# Args: collection_name (string), versioning_setting (string)
# Returns: True (1), False 0)
def set_versioning(c_name, versioning_setting):
    src, err = run_cli(dataset, 'set-versioning', c_name, versioning_setting)
    if err !== '':
        errors.append(err)
        return False
    return True

# get_versioning() returns the current setting of versioning for a
# collection. The values are "" (versioning disabled), "patch",
# "minor" and "major" for semver values to be incremented on
# create, update, and attach.
#
# Args: collection_name (string)
# Returns: value (string)
def get_versioning(c_name):
    src, err = run_cli(dataset, 'get-versioning', c_name)
    if err !== '':
        errors.append(err)
        return ''
    return src

