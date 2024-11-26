# Overview


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Functions#


Flink Table API & SQL empowers users to do data transformations with functions.


## Types of Functions#


There are two dimensions to classify functions in Flink.


One dimension is system (or built-in) functions v.s. catalog functions. System functions have no namespace and can be
referenced with just their names. Catalog functions belong to a catalog and database therefore they have catalog and database
namespaces, they can be referenced by either fully/partially qualified name (catalog.db.func or db.func) or just the
function name.

`catalog.db.func`
`db.func`

The other dimension is temporary functions v.s. persistent functions. Temporary functions are volatile and only live up to
lifespan of a session, they are always created by users. Persistent functions live across lifespan of sessions, they are either
provided by the system or persisted in catalogs.


The two dimensions give Flink users 4 categories of functions:

1. Temporary system functions
2. System functions
3. Temporary catalog functions
4. Catalog functions

## Referencing Functions#


There are two ways users can reference a function in Flink - referencing function precisely or ambiguously.


### Precise Function Reference#


Precise function reference empowers users to use catalog functions specifically, and across catalog and across database,
e.g. select mycatalog.mydb.myfunc(x) from mytable and select mydb.myfunc(x) from mytable.

`select mycatalog.mydb.myfunc(x) from mytable`
`select mydb.myfunc(x) from mytable`

This is only supported starting from Flink 1.10.


### Ambiguous Function Reference#


In ambiguous function reference, users just specify the function’s name in SQL query, e.g. select myfunc(x) from mytable.

`select myfunc(x) from mytable`

## Function Resolution Order#


The resolution order only matters when there are functions of different types but the same name,
e.g. when thereâre three functions all named âmyfuncâ but are of temporary catalog, catalog, and system function respectively.
If thereâs no function name collision, functions will just be resolved to the sole one.


### Precise Function Reference#


Because system functions donât have namespaces, a precise function reference in Flink must be pointing to either a temporary catalog
function or a catalog function.


The resolution order is:

1. Temporary catalog function
2. Catalog function

### Ambiguous Function Reference#


The resolution order is:

1. Temporary system function
2. System function
3. Temporary catalog function, in the current catalog and current database of the session
4. Catalog function, in the current catalog and current database of the session