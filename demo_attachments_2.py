#!/usr/bin/env python3

from py_dataset import dataset

c_name = 't3.ds'
key = 'a2'
v = 'v0.1.2'
obj = {'one':key}
f_name = 'DEVELOPER-NOTES.md'
#dataset.init(c_name)
dataset.create(c_name, key, obj)
keys = dataset.keys(c_name)
print(keys)

o, err = dataset.read(c_name, key)
print(o)

dataset.attach(c_name, key, [ f_name ], v)
dataset.attachments(c_name, key)
o , err = dataset.read(c_name, key)
print(o)


o, err = dataset.read(c_name, key)
print(o)

dataset.read_list(c_name, keys)

