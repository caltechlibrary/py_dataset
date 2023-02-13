#!/usr/bin/env python3

import os
from py_dataset import dataset


c_name = 't3.ds'
key = 'a1'
obj = {'key': key, 'one':key}
f_name = 'README.md'
if not os.path.exists(c_name):
    dataset.init(c_name, '')
dataset.create(c_name, key, obj)
keys = dataset.keys(c_name)
print(keys)

o, err = dataset.read(c_name, key)
print(o)

dataset.attach(c_name, key, [ f_name ])
dataset.attachments(c_name, key)
o , err = dataset.read(c_name, key)
print(o)

