
[up](./)

## Filters and sorts

(THIS WAS DEPRECIATED AND IS NO LONGER SUPPORTED)

`dataset.keys()` method returns all keys in a collection. It is
fast because it is part of the collection's metadata. Sometimes
you want a subset of the data and for that you can use `key_filter()`
or an ordering and which can be cone wiht `key_sort()` method.

Working with objects in memory takes resources so normally the
for flow for filtering and sorting is split into three steps.

1. Get a list of all keys in the collection
2. Create a subset based on a filter condition
3. Sort the filtered keys.

you almost always want to do the sort last so that you're 
limitting the number of objects in memory when you are evaluating
their order.

Here's is a simple case for match records in a collection named 
**characters.ds** where the given name is equal to "Mojo". We will 
save the result in a file called _mojo.keys_.

```python
   c_name = 'characters.ds'
   keys = dataset.keys(c_name)
   mojo_keys = dataset.key_filter(c_name, keys, '(eq .given "Mojo")')
```

You can also use an existing key list (e.g. `mojo_keys`)
to sub select based on a new filter and/or sort expression. 
We will filter for a family name of "Sam" and sort by the age field.

```python
   sam_keys = dataset.key_filter(c_name, mojo_keys, '(eq .family "Sam")')
```

We can sort either list of keys using `key_sort()` In this
example we'll sort all the characters named "Mojo" by age.

```python
    sorted_mojo_keys = dataset.key_filter(c_name, mojo_keys, '+.age')
```

You can improve the performance of filtering/sorting by
breaking it down to steps for large collections. First filter
the keys you want. Then sort the filtered list.

Wait, whats are filter expressions? What are sort expressions?


## filter expressions

A *filter expression* is based on the Go template conditional 
expressions. It uses a prefix notation for the logic (e.g. 
eq - equal, ne - not equal, lt - less than, gt greater than) 
and the value(s) to be compared in [dotpath notation](dotpath.html).

Filters can be simple expressions that result in "true" or 
"false" or compound expressions (e.g. expressions combined with 
_and_ and _or_) that evaluate to "true" or "false".  Simple 
expressions can isolated by parenthasis 
(e.g. `(and (eq .i 1) (ne .s "1") (ne .s "one"))`).

Example filter operators

+ eq - equal (must be same type and value, e.g. 1 does not equal "1")
+ nq - not equal (comparing same type but different values)
+ lt - less than
+ gt - greater than
+ match - given a regular expression and string data return true if they match
+ and - allows you to combine two expression and if both true the expression is true.
+ or - allows you to combine two or more expressions where one is true then expression is true.

#### Simple

A field, `.family_name`, matches a known value, "Feynman".

```
	'(eq .family_name "Feynman")'
```

A field, `.family_name`, does not match a known value, "Feynman".

A field, `.family_name`, does not match value

```
	'(ne .family_name "Feynman")'
```

A field, `.family_name`, match the regular expression `Feym*n`.

```
	'(match "Feynm*n" .family_name)'
```


#### Compound

Two fields match, `.family_name` and `.given_name`, known values "Feynman" and "Richard".

```
	'(and (eq .family_name "Feynman") (eq .given_name "Richard"))'
```

NOTE: That the filters experessions are data type aware. So 
"1" is not the same as 1. Likewise 1 is not the same as 1.0.

## sort expressions

The "keys" option provides for simple one level sorting.
Sorting is described by a plus or minus followed by a dotpath 
to a simple field type (i.e. string, int, or float JSON types). 
In our previous examples sorting ascending by `.family_name` would
be expressed as `+.family_name`. To sort by descending `.family_name` 
you would use the expression `-.family_name`.  By default we assume 
an ascending sort so in practice you can omit a leading "+".

In this example we listing last names of "Smith" sorting by ascending 
given name. The collection name is "people.ds".

```
    c_name = 'people.ds'
    keys = dataset.keys(c_name)
    filtered_keys = dataset.key_filter(c_name, keys, 
        '(eq "Smith" .family_name)')
    sorted_keys = dataset.key_sort(c_name, filtered_keys, '.given_name')
```

In this example we list last anes of "Smith" sorted by descending 
given name.


```
    sorted_keys = dataset.key_sort(c_name, filtered_keys, '-.given_name')
```

