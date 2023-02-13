
[up](./)

# frame_create() and frame(), has_frame(), frame_names()

Data frames are a way of creating ordered subsets of JSON objects
in a dataset collection. A data frame is defined by a list of keys
from the collection, a list of dot paths into the objects of the collection
and a list of labels for the objects aggregated inside the frame.

The order of the objects in the frame match the order of the keys
provided.  The dot paths define the set of values to be applied
to the labels provided. This provides a mechanism to change
attribute names if desired.

Frames can be retrieved in three ways, a full frame including
its metadata, as a list of objects (more useful), or a 2D
array where the object labels form the column headers (also
useful).


This command will define a data frame or return the contents and
metadata of a defined frame.  To define a new frame you need to 
provide a collection name, a frame name followed by a list of 
dotpath/label pairs. The labels are used as object attribute names 
and the dot paths as the source of data. You also need a list of keys.  
By default the keys are read from standard input. With options you 
can include a specific file or even indicate to use all the keys 
in a collection.  In this example we are creating a frame 
called "title-authors-year" based on the titles, authors and 
publication year from a dataset collection called `pubs.ds`. 
Note the labels of "Title", "Authors", "PubYear" are on the right 
side the an equal sign and the dot paths to the left. 

```python
    c_name = 'pubs.ds'
    f_name = 'title-authors-year'
    dot_paths = [ '.title', '.authors', '.publication_year' ]
    labels = [ 'Title', 'Authors', 'PubYear' ]
    keys = dataset.keys(c_name)
    dataset.frame_create(c_name,  f_name, keys, dot_paths, labels)
```

The objects in the frame's object list will look like

```json
    {
        "Title": ...,
        "Authors": ...,
        "PubYear": ...,
    }
```

This allows you to create convient names for otherwise deep dot paths.

If you want to see the full frame with all its metadata you can use the
`frame()` method. 

```python
    f = dataset.frame(c_name, f_name)
    print(f)
```

Sometimes you want to see if a frame exists. Like checking for
a key in a collection you can use the `has_frame()` to see if 
a frame exists in a collection.

```python
    if dataset.has_frame(c_name, "my-frame"):
        print('Frame exists')
    else:
        print("Frame is missing")
```



To get a list of frames associated with a collection use `frame_names()`.

```python
    for i, frame_name in enumerate(dataset.frame_names(c_name)):
        print(f"{i} - {frame_name}")
```

