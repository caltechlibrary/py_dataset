
[up](./)

# How Attachments Work

The primary use case of the **dataset** tool is managing JSON documents.
There exist a common secondary use case of including support for "attached"
non-JSON documents. Example 1, when we harvest content from a system who
does not support JSON natively it is handy to keep a version of the 
harvested content for audit purposes. The EPrints system has a REST
API that returns XML.  Storing the original EPrint XML document gives
the developer an ability to verify  that their JSON rendering matches
the EPrint XML should their JSON needs change in the future. 

This raises questions of how to keep things simple while supporting
an arbitrary number of attachments for JSON object document? How do
you handle versioning when some types of collections need it for attachments
and others don't? 

The **dataset** command line tool and related Go package store the 
attachments based on the collection's version seetings. By default
collections do not version JSON records or attachments. The versions
are incremented based on wither collection level versioning is turned on as "patch", "minor" or "major" version increments. This setting, when set,
will impact future JSON document or attachment changes by incrementing the
semver accordingly.  The default version number is "v0.0.0", if patch level versioning is enabled it will mean the next version stored is "v0.0.1", if
minor versioning is inabled then the next version after "v0.0.0" is "v0.1.0",
if major version is inabled then the next version after "v0.0.0" is "v1.0.0".  Not with the changes to v2 of dataset you do not normally need to directly specify versions. It just happens automatically when you change something. To turn off versioning on the collection then you'd set the versioning value to an empty string. Any historic versions remaining but future actions will not be versioned.

## Working example

We have a dataset collection called "Sea-Mamals.ds" with versioning enabled at the patch level. We have a JSON object stored called "walrus".
We want to attach "notes-on-walrus.docx" which is on our local
drive under "/Users/fred/Documents/notes-on-walrus.docx".

Using the **py_dataset** you issue the follow command --

```shell
    from py_dataset import dataset
    c_name = "Sea-Mammals.ds"
    key = "walrus"
    # NOTE: the default version is 'v0.0.0', we'll be incrementing
    # the patch level with is the last zero.
    obj = '{"description": "may have tusks", "size": "impressive"}'
    if not dataset.status(c_name):
        dataset.init(c_name)
    if not dataset.create(c_name, key, obj)
        print(f'failed to create {key}, {dataset.error_message()}')
        exit()
    if not dataset.attach(c_name, key, [ '/Users/fred/Documents/notes-on-walrus.docx'])
        print(f'failed to attach to {key}, {dataset.error_message()}')
        exit()
```

If you looked on the file system where the collection resides you'll see an attachments sudirectory, a pair tree path ending in a directory holding the attachment base name, the value of the attach will be named "v0.0.1", "v0.0.2", etc depending up the updates made to it. It is a naive version system and does NOT perform diffs between the objects. This is really important because if you store a 2 Gig object then store new version of of a 2Gig object you need to have enough file system room for both copies!!!

```
    Sea-Mamanls/pairtree/wa/lr/us/walrus.json
    Sea-Mamanls/pairtree/wa/lr/us/notes-on-walrus.docs/v0.0.1
```

In this example the metadata for the attachment is updated in the walrus.json file.

If we had added our attachment including a semver the directory structure
will be slightly more complex.

```shell
    if not dataset.attach(c_name, key, [ '/Users/fred/Documents/notes-on-walrus.docx' ]):
        print(dataset.error_message())
```

This will cause additional sub directories to exist (if they haven't be created
before). When you detach the "notes-on-walrus.docx" file is detaches as "notes-on-walruls.docs" and does not include the version number.

```
    Sea-Mamanls/pairtree/wa/lr/us/walrus.json
    Sea-Mamanls/pairtree/wa/lr/us/notes-on-walrus.docx/v0.0.1
    Sea-Mamanls/pairtree/wa/lr/us/notes-on-walrus.docx/v0.0.2
```

If we later add a v0.0.3 of "notes-on-walrus.docx" it'd looks like

```
    Sea-Mamanls/pairtree/wa/lr/us/walrus.json
    Sea-Mamanls/pairtree/wa/lr/us/notes-on-walrus.docx/v0.0.1
    Sea-Mamanls/pairtree/wa/lr/us/notes-on-walrus.docx/v0.0.2
    Sea-Mamanls/pairtree/wa/lr/us/notes-on-walrus.docx/v0.0.3
```

All the metadata about the files attached are stored in 
the primary attachments sub directory in a pairtree. This is tree even
when you use a SQL store for storing JSON documents.

NOTE: As of v2 **dataset** attachment versioning is automatic if set for the collection.

If you want good version control is is recommended NOT to use dataset versioning but instead opt for a proven solution like Git, Subversion or ZFS. Dataset versioning is highly experimental.

NOTE: The href in the attachments metadata always points at the last attached version.


