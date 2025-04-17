
# query

# SYNOPSIS

query(C_NAME, SQL_STATEMENT, [PARAMS])

# DESCRIPTION

__query__ let's your query a dataset collection using SQL. The SQLite
dialect depends on the SQL store you chose when initializing the collection.
If you used a SQLite3 protocol then it is the SQLite3 SQL dialect. If
you chose Postgres then that dialect is expected.

If you are have stored content using the venerable Pairtree then you need
to "index" your collection before query will work. See the `-index` option
on the [dsqery](https://caltechlibrary.github.io/dataset/dsquery.1.md) tool
for details.

The schema is the same for all storage engines.  The scheme for the JSON
stored documents have a four column scheme.  The columns are "_key", 
"created", "updated" and "src". "_key" is a string (aka VARCHAR),
"created" and "updated" are timestamps while "src" is a JSON column holding
the JSON document. The table name reflects the collection
name without the ".ds" extension (e.g. data.ds is stored in a database called
data having a table also called data).

The output of __query__ is a list of objects. The order of the
objects is determined by the your SQL statement and SQL engine.

# PARAMETERS

C_NAME
: If harvesting the dataset collection name to harvest the records to.

SQL_STATEMENT
: The SQL statement should conform to the SQL dialect used for the
JSON store for the JSON store (e.g.  Postgres, MySQL and SQLite 3).
The SELECT clause should return a single JSON object type per row.
__dsquery__ returns an JSON array of JSON objects returned
by the SQL query.

PARAMS
: Is optional, it is any values you want to pass to the SQL_STATEMENT.

# SQL Store Scheme

_key
: The key or id used to identify the JSON documented stored.

src
: This is a JSON column holding the JSON document

created
: The date the JSON document was created in the table

updated
: The date the JSON document was updated


# EXAMPLES

Generate a list of JSON objects with the `_key` value
merged with the object stored as the `._Key` attribute.
The colllection name "data.ds" which is implemented using Postgres
as the JSON store. (note: in Postgres the `||` is very helpful).

~~~
c_name = "data.ds"
sql_stmt = "SELECT jsonb_build_object('_Key', _key)::jsonb || src::jsonb FROM data"
l = dataset.query(c_name, sql_stmt)
if l == None:
    err = dataset.error_messag()
    print(f'''error {err}''', file = sys.stderr, flush=True)
    # handle the error
print(l)
~~~

In this example we're returning the "src" in our collection by querying
for a "id" attribute in the "src" column. The id is passed in as an attribute
using the Postgres positional notatation in the statement.

~~~
c_name = "data.ds"
sql_stmt = "SELECT src FROM data WHERE src->>'id' = $1 LIMIT 1" "xx103-3stt9"
l = dataset.query(c_name, sql_stmt)
if l == None:
    err = dataset.error_messag()
    print(f'''error {err}''', file = sys.stderr, flush=True)
    # handle the error
print(l)
~~~


