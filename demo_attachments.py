#!/usr/bin/env python3

from py_dataset import dataset

c_name = 't3.ds'
key = 'a1'
v = 'v0.1.1'
obj = {'one':key}
f_name = 'README.md'
dataset.init(c_name)
dataset.create(c_name, key, obj)
keys = dataset.keys(c_name)
print(keys)

o, err = dataset.read(c_name, key)
print(o)

dataset.attach(c_name, key, [ f_name ])
dataset.attachments(c_name, key)
o , err = dataset.read(c_name, key)
print(o)

