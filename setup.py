#!/usr/bin/env python3

#from distutils.core import setup
#from site import getsitepackages
#site_package_location = os.path.join(getsitepackages()[0], "dataset")

from setuptools import setup, find_packages

import sys
import os
import shutil
import json

readme_md = "README.md"
readme_txt = "README.txt"

def read(fname):
    with open(fname, mode = "r", encoding = "utf-8") as f:
        src = f.read()
    return src

codemeta_json = "codemeta.json"
if os.path.exists(codemeta_json) == False:
    shutil.copyfile(os.path.join("..", codemeta_json), codemeta_json)

# If we're running sdist make sure our local codemeta.json is up to date!
if "sdist" in sys.argv:
    # Project Metadata and README
    shutil.copyfile(os.path.join("..", codemeta_json),  codemeta_json)
    shutil.copyfile(os.path.join("..", readme_md),  readme_txt)

# Let's pickup as much metadata as we need from codemeta.json
with open(codemeta_json, mode = "r", encoding = "utf-8") as f:
    src = f.read()
    meta = json.loads(src)

# Let's make our symvar string
version = meta["version"]

# Now we need to pull and format our author, author_email strings.
author = ""
author_email = ""
for obj in meta["author"]:
    given = obj["givenName"]
    family = obj["familyName"]
    email = obj["email"]
    if len(author) == 0:
        author = given + " " + family
    else:
        author = author + ", " + given + " " + family
    if len(author_email) == 0:
        author_email = email
    else:
        author_email = author_email + ", " + email
description = meta['description']
keywords = meta['keywords']
url = meta['codeRepository']
download = meta['downloadUrl']
license = meta['license']
name = meta['name']

# Setup for our Go based shared library as a "data_file" since Python doesn't grok Go.
platform = ""
if sys.platform.startswith('win'):
    shared_library_name = "lib/libdataset.dll"
    platform = "Windows"
    OS_Classifier = "Operating System :: Microsoft :: Windows :: Windows 10"
if sys.platform.startswith('linux'):
    shared_library_name = "lib/libdataset.so"
    OS_Classifier = "Operating System :: POSIX :: Linux"
if sys.platform.startswith("darwin"):
    shared_library_name = "lib/libdataset.dylib"
    platform = "Mac OS X"
    OS_Classifier = "Operating System :: MacOS :: MacOS X"
        
if os.path.exists(os.path.join(shared_library_name)) == False:
    print("Missing compiled shared library " + shared_library_name )
    sys.exit(1)

# Now that we know everything configure out setup
setup(name = name,
    version = version,
    description = description,
    long_description = read(readme_txt),
    author = author,
    author_email = author_email,
    url = url,
    download_url = download,
    license = license,
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "*_test.py"]),
    data_files = [(name,[ shared_library_name, 'lib/libdataset.h'])],
    keywords = keywords,
    include_package_data = True,
    classifiers = [
        "Development Status :: Alpha",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Other",
        "Programming Language :: Go",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X"
    ]
)
