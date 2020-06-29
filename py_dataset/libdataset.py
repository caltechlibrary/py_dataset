#!/usr/bin/env python3
# 
# libdataet.py is a C type wrapper for our libdataset.go is a C shared.
# It is used to test our dataset functions exported from the C-Shared
# library libdataset.so, libdataset.dynlib or libdataset.dll.
# 
# @author R. S. Doiel, <rsdoiel@library.caltech.edu>
#
# Copyright (c) 2019, Caltech
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
import sys
import os
import json
from ctypes import CDLL, c_char_p, c_int, c_bool

# Figure out shared library extension
go_basename = 'lib/libdataset'
ext = '.so'
if sys.platform.startswith('win'):
    ext = '.dll'
if sys.platform.startswith('darwin'):
    ext = '.dylib'
if sys.platform.startswith('linux'):
    ext = '.so'

# Find our shared library and load it
dir_path = os.path.dirname(os.path.realpath(__file__))
libdataset = CDLL(os.path.join(dir_path, go_basename+ext))

#
# Setup our Go functions to be nicely wrapped
#

# NOTE: we use a horrible hack in this library. It is a royal pain
# to pass dynamic dataset structures between C and Python let alone
# between Go and C. As a result I've chosen the easy programing path
# of passing JSON source between the code spaces. This has proven
# simple, reliable and *inefficent* in memory usage. I've opted for 
# reliability and simplicity. RSD, 2020-03-18


# error_clear() clears the error values
#
# It takes no args and returns no value.

# error_message() returns the error messages aggregated
# in previously envoked shared library functions.
#
# Return: error message text (string)
libdataset.error_message.restype = c_char_p


# use_strict_dotpath() sets the state of the strict dotpath
# interpretation. Strict dot paths expect a period at the 
# beginning, non strict will prefix a period automatigally. 
# This is useful where you're using labels in a report 
# (the period is annoying) and also in generating transformed 
# object attributes (the period is useful).
#
# Args: is True (1) or False (0)
libdataset.use_strict_dotpath.argtypes = [ c_bool ]
# Return: True (1) or False (0)
libdataset.use_strict_dotpath.restype = c_bool

# dataset_version() returns the version number of the libdataset
# used.
#
# Return: semver (string)
libdataset.dataset_version.restype = c_char_p

# is_verbose() returns the state of the verbose flag.
#
# Returns: True (1) or False (0)
libdataset.is_verbose.restype = c_bool

# verbose_on() sets the verbose flag to True.
#
# Returns: True (1) or False (0)
libdataset.verbose_on.restype = c_bool

# verbose_off() sets the verbose flag to False
#
# Returns: True (1) or False (0)
libdataset.verbose_off.restype = c_bool

# init_collection() creates a dataset collection.
#
# Args: collection_name (string)
libdataset.init_collection.argtypes = [ c_char_p ]
# Returns: True (1) or False (0)
libdataset.init_collection.restype = c_bool

# is_collection_open() checks to see if the collection
# is already open and in the list of open collections.
#
# Args: collection_name (string)
libdataset.is_collection_open.argtypes = [ c_char_p ]
# Returns: Ture (1) or False (0)
libdataset.is_collection_open.restype = c_bool

# collections() returns a list of opened collections.
#
# Returns: string (names of collections)
libdataset.collections.restype = c_char_p

# open_collcetion() explicitly opens a collection.
#
# Args: collection_name (string)
libdataset.open_collection.argtypes = [ c_char_p ]
# Returns: True (1) or False (0)
libdataset.open_collection.restype = c_bool

# close_collection() closes a previously opened collection.
# Most libdataset commands auto-magically open the collection.
#
# Args: collection_name (string)
libdataset.close_collection.argtypes = [ c_char_p ]
# Returns: True (1) or False (0)
libdataset.close_collection.restype = c_bool

# close_all_collections closes all opened collections.
#
# Returns: True (1) or False (0)
libdataset.close_all_collections.restype = c_bool

# create_object() creates a JSON object in a collection.
#
# Args: collection_name (string), key (string), value (JSON source)
libdataset.create_object.argtypes = [ c_char_p, c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.create_object.restype = c_bool

# read_object() retrieves a JSON object from a collection.
#
# Args: collection_name (string), key (string), clean_object (bool)
libdataset.read_object.argtypes = [ c_char_p, c_char_p, c_bool ]
# Returns: string (JSON source)
libdataset.read_object.restype = c_char_p

# read_object_list() returns a list of objects for the provided keys 
# in the collection.
#
# Args: collection_name (string), keys (list of key strings AS JSON), 
#       clean_object (bool)
libdataset.read_object_list.argtypes = [ c_char_p, c_char_p, c_bool ]
# Returns: string (JSON source)
libdataset.read_object_list.restype = c_char_p

# update_object() updates an object in the collection given a key
# and new object.
#
# Args: collection_name (string), key (string), value (JSON sourc)
libdataset.update_object.argtypes = [ c_char_p, c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.update_object.restype = c_bool

# delete_object() removes an object from a collection.
#
# Args: collection_name (string), key (string)
libdataset.delete_object.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1), False (0)
libdataset.delete_object.restype = c_bool

# key_exists() tests for a key in a collection.
#
# Args: collection_name (string), key (string)
libdataset.key_exists.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1), False (0)
libdataset.key_exists.restype = c_bool

# keys() returns a list of all keys in a collection.
#
# Args: collection_name (string)
libdataset.keys.argtypes = [ c_char_p ]
# Returns: string (JSON source)
libdataset.keys.restype = c_char_p

# key_filter() takes a list of keys and filters the objects to return
# a new filtered list of keys.
#
# Args: collection_name (string), key_list (JSON array source), filter_expr (string)
libdataset.key_filter.argtypes = [ c_char_p, c_char_p, c_char_p ]
# Returns: string (JSON source)
libdataset.key_filter.restype = c_char_p

# key_sort() takes a list of keys and a sort expression return a sorted
# list of keys.
#
# Args: collection_name (string), key_list (JSON array source), sort order (string)
libdataset.key_sort.argtypes = [ c_char_p, c_char_p, c_char_p ]
# Returns: string (JSON source)
libdataset.key_sort.restype = c_char_p

# count_objects() returns the number of objects in a collection.
#
# Args: collection_name (string)
libdataset.count_objects.argtypes = [ c_char_p ]
# Returns: integer (int)
libdataset.count_objects.restype = c_int

# NOTE: this diverges from cli and reflects low level dataset organization
#
# import_csv - import a CSV file into a collection
# syntax: COLLECTION CSV_FILENAME ID_COL
# 
# options that should support sensible defaults:
#
#      UseHeaderRow (bool, 1 true, 0 false)
#      Overwrite (bool, 1 true, 0 false)
# Args: collection_name (string), csv_filename (string), id_column_no (int), use_header_row (bool), overwrite (bool)
libdataset.import_csv.argtypes = [ c_char_p, c_char_p, c_int, c_bool, c_bool ]
# Returns: True (1), False (0)
libdataset.import_csv.restype = c_bool

# export_csv() exports a dataset collection objects into a CSV file
# based on the contents of a frame.
# 
# Args: collection_name (string), frame_name (string), csv_filename (string)
libdataset.export_csv.argtypes = [ c_char_p, c_char_p, c_char_p ]
# Returns: True (1), False (0)
libdataset.export_csv.restype = c_bool


# sync_receive_csv() retrieves data in a CSV file and updates a collection
# using a frame.
#
# Args: collection_name (string), frame_name (string), csv_filename (string), overwrite (bool)
libdataset.sync_recieve_csv.argtypes = [ c_char_p, c_char_p, c_char_p, c_bool]
# Returns: True (1) or False (0)
libdataset.sync_recieve_csv.restype = c_bool

# sync_send_csv() updates a CSV file based on the objects in a collection
# using a frame.
#
# Args: collection_name (string), frame_name (string), csv_filename (string), ovewrite (bool)
libdataset.sync_send_csv.argtypes = [ c_char_p, c_char_p, c_char_p, c_bool ]
# Returns: True (1) or False (0)
libdataset.sync_send_csv.restype = c_bool

# collection_exists() returns True if a collection exists, False otherwise.
# NOTE: This will be renamed collection_exists() in a coming release
# of libdataset.
#
# Returns: True (1) or False (0)
libdataset.collection_exists.restype = c_bool

# list_objects() returns a list of objects for a list of keys.
#
# Args: collection_name (string), key list (JSON array source)
libdataset.list_objects.argtypes = [ c_char_p, c_char_p ]
# Returns: string (JSON Array of Objects source)
libdataset.list_objects.restype = c_char_p

# object_path() returns the file system path to an object in a 
# collection.
#
# Args: collection_name (string), key (string)
libdataset.object_path.argtypes = [ c_char_p, c_char_p ]
# Return: string
libdataset.object_path.restype = c_char_p

# check_collection() checks a collection for structural errors.
#
# Args: collection_name (string)
libdataset.check_collection.argtypes = [ c_char_p ]
# Returns: True (1) or False (0)
libdataset.check_collection.restype = c_bool

# repair_collection() trys to repair a collection when it has
# structural errors.
#
# Args: collection_name (string)
libdataset.repair_collection.argtypes = [ c_char_p ]
# Returns: True (1) or False (0)
libdataset.repair_collection.restype = c_bool

# attach() adds a file to a JSON object record.
#
# Args: collection_name (string), key (string), semver (string), filenames (string)
libdataset.attach.argtypes = [ c_char_p, c_char_p, c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.attach.restype = c_bool

# attachments() lists the files attached to a JSON object record.
#
# Args: collection_name (string), key (string)
libdataset.attachments.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.attachments.restype = c_char_p

# detach() retrieves a file from an JSON object record.
#
# Args: collection_name (string), key (string), semver (string), basename (string)
libdataset.detach.argtypes = [ c_char_p, c_char_p, c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.detach.restype = c_bool

# prune() removes a file from a JSON object record.
#
# Args: collection_name (string), key (string), semver (string) basename (string)
libdataset.prune.argtypes = [ c_char_p, c_char_p, c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.prune.restype = c_bool

# join_objects() joins a new object with an object in a collection.
#
# Args: collection_name (string), key (string), value (JSON source), overwrite (bool)
libdataset.join_objects.argtypes = [ c_char_p, c_char_p, c_char_p, c_bool ]
# Returns: True (1) or False (0)
libdataset.join_objects.restype = c_bool

# clone_collection() takes collection and creates a copy of it.
#
# Args: collection_name (string), new_collection_name (string), ????
libdataset.clone_collection.argtypes = [ c_char_p, c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.clone_collection.restype = c_bool

# clone_sample() generates a random sample of objects split between 
# training and test collections.
# 
# Args: collection_name (string), new_sample_collection_name (string), new_rest_collection_name (string), sample size ????
libdataset.clone_sample.argtypes = [ c_char_p, c_char_p, c_char_p, c_bool ]
# Returns: True (1) or False (0)
libdataset.clone_sample.restype = c_bool

# frame() returns the full metadata and contents of a frame.
#
# Args: collection_name (string), frame_name (string)
libdataset.frame.argtypes = [ c_char_p, c_char_p ]
# Returns: value (JSON object source)
libdataset.frame.restype = c_char_p

# frame_create() generates a new data frame given a collection name,
# frame name, keys, dot paths and labels.
#
# Args: collection_name (string), frame_name (string), keys (JSON source), dotpaths (JSON source), labels (JSON source)
libdataset.frame_create.argtypes = [ c_char_p, c_char_p,  c_char_p, c_char_p, c_char_p]
# Returns: value (JSON object source)
libdataset.frame_create.restype = c_bool

# frame_exists() checks to see if a frame name has already been defined.
#
# Args: collection_name (string), frame_name (string)
libdataset.frame_exists.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.frame_exists.restype = c_bool

# frame_keys() returns a list of keys as JSON as defined in the
# data frame.
#
# Args: collection_name (string), frame_name (string)
libdataset.frame_keys.argtypes = [ c_char_p, c_char_p ]
# Returns: string (JSON object source)
libdataset.frame_keys.restype = c_char_p

# frame_objects() returns a list of objects as JSON currently defined
# in the data frame.
#
# Args: collection_name (string), frame_name (string)
libdataset.frame_objects.argtypes = [ c_char_p, c_char_p ]
# Returns: string (JSON object source)
libdataset.frame_objects.restype = c_char_p

# frames() returns a list of frames defined for the collection.
#
# Args: collection_name (string)
libdataset.frames.argtypes = [ c_char_p ]
# Returns: frame names (JSON Array Source)
libdataset.frames.restype = c_char_p

# frame_refresh() updates the objects in a data frame based on
# the current state of the collection. Any objects removed from
# the collection will be removed from the frame.
#
# Args: collection_name (string), frame_name (string)
libdataset.frame_refresh.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.frame_refresh.restype = c_bool

# frame_reframe() replaces the object list in a data frame.
#
# Args: collection_name (string), frame_name (string), keys (JSON source)
libdataset.frame_reframe.argtypes = [ c_char_p, c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.frame_reframe.restype = c_bool

# frame_delete() removes a frame from a collection.
#
# Args: collection_name (string), frame_name (string)
libdataset.frame_delete.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.frame_delete.restype = c_bool

# frame_clear() removes all objects from a frame.
#
# Args: collection_name (string), frame_name (string)
libdataset.frame_clear.argtypes = [ c_char_p, c_char_p]
# Returns: True (1) or False (0)
libdataset.frame_clear.restype = c_bool

# frame_grid() returns a frames object list as a 2D array of
# columns per field.
#
# Args: collection_name (string), frame_name (string), include header (bool)
libdataset.frame_grid.argtypes = [ c_char_p, c_char_p, c_bool ]
# Returns: string (JSON Array Source)
libdataset.frame_grid.restype = c_char_p

# create_objects() generates a batch of objects in a collection,
# used for testing libdataset.
#
# Args: collection_name (string), keys_as_json (string), objects_as_json (string)
libdataset.create_objects.argtypes = [ c_char_p, c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.create_objects.restype = c_bool

# update_objects()  updates a set of objects in a collections, used in
# testing a counter part to make_objects.
#
# Args: collection_name (string), keys_as_json (string), objects_as_json (string)
libdataset.update_objects.argtypes = [ c_char_p, c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.update_objects.restype = c_bool

# set_who() sets the Namaste value for "Who".
#
# Args: collection_name (string), names_as_json (string)
libdataset.set_who.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.set_who.restype = c_bool

# set_what() sets the Namaste value for "What"
#
# Args: collection_name (string), what value (string)
libdataset.set_what.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.set_what.restype = c_bool

# set_when() sets the Namaste value for "When"
#
# Args: collection_name (string), when value (string)
libdataset.set_when.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.set_when.restype = c_bool

# set_where() sets the Namaste value for "Where"
#
# Args: collection_name (string), where value (string)
libdataset.set_where.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.set_where.restype = c_bool

# set_version() sets the version for the collection data.
# It is recommended you use a semver.
#
# Args: collection_name (string), version value (string)
libdataset.set_version.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.set_version.restype = c_bool

# set_contact() sets the contact info for a collection.
#
# Args: collection_name (string), contact value (string)
libdataset.set_contact.argtypes = [ c_char_p, c_char_p ]
# Returns: True (1) or False (0)
libdataset.set_contact.restype = c_bool

# get_who() returns the Namaste value for "Whot"
#
# Args: collection_name (string)
libdataset.get_who.argtypes = [ c_char_p ]
# Returns: string (JSON Array Source)
libdataset.get_who.restype = c_char_p

# get_what() returns the Namaste value for "What"
# Args: collection_name (string)
libdataset.get_what.argtypes = [ c_char_p ]
# Returns: string (JSON Array Source)
libdataset.get_what.restype = c_char_p

# get_where() returns the Namaste value for "Where"
#
# Args: collection_name (string)
libdataset.get_where.argtypes = [ c_char_p ]
# Returns: frame names (JSON Array Source)
libdataset.get_where.restype = c_char_p

# get_when() returns the Namaste value for "When"
#
# Args: collection_name (string)
libdataset.get_when.argtypes = [ c_char_p ]
# Returns: frame names (JSON Array Source)
libdataset.get_when.restype = c_char_p

# get_version() returns the version information for the collection.
#
# Args: collection_name (string)
libdataset.get_version.argtypes = [ c_char_p ]
# Returns: frame names (JSON Array Source)
libdataset.get_version.restype = c_char_p

# get_contact() returns the contact info for a collection.
#
# Args: collection_name (string)
libdataset.get_contact.argtypes = [ c_char_p ]
# Returns: frame names (JSON Array Source)
libdataset.get_contact.restype = c_char_p

