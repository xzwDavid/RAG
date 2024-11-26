# DROP Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# CREATE Statements#


With Hive dialect, the following DROP statements are supported for now:

* DROP DATABASE
* DROP TABLE
* DROP VIEW
* DROP MARCO
* DROP FUNCTION

## DROP DATABASE#


### Description#


DROP DATABASE statement is used to drop a database as well as the tables/directories associated with the database.

`DROP DATABASE`

### Syntax#


```
DROP (DATABASE|SCHEMA) [IF EXISTS] database_name [RESTRICT|CASCADE];

```

`DROP (DATABASE|SCHEMA) [IF EXISTS] database_name [RESTRICT|CASCADE];
`

The use of SCHEMA and DATABASE are interchangeable - they mean the same thing.
The default behavior is RESTRICT, where DROP DATABASE will fail if the database is not empty.
To drop the tables in the database as well, use DROP DATABASE ... CASCADE.

`SCHEMA`
`DATABASE`
`RESTRICT`
`DROP DATABASE`
`DROP DATABASE ... CASCADE`

DROP returns an error if the database doesn’t exist, unless IF EXISTS is specified
or the configuration variable hive.exec.drop.ignorenonexistent
is set to true.

`DROP`
`IF EXISTS`

### Examples#


```
DROP DATABASE db1 CASCADE;

```

`DROP DATABASE db1 CASCADE;
`

## DROP TABLE#


### Description#


DROP TABLE statement removes metadata and data for this table.
The data is actually moved to the .Trash/Current directory if Trash is configured.
The metadata is completely lost.

`DROP TABLE`
`.Trash/Current`

When drop an EXTERNAL table, data in the table will not be deleted from the filesystem.

`EXTERNAL`

### Syntax#


```
DROP TABLE [IF EXISTS] table_name;

```

`DROP TABLE [IF EXISTS] table_name;
`

DROP returns an error if the table doesn’t exist, unless IF EXISTS is specified
or the configuration variable hive.exec.drop.ignorenonexistent
is set to true.

`DROP`
`IF EXISTS`

### Examples#


```
DROP TABLE IF EXISTS t1;

```

`DROP TABLE IF EXISTS t1;
`

## DROP VIEW#


### Description#


DROP VIEW statement is used to removed metadata for the specified view.

`DROP VIEW`

### Syntax#


```
DROP VIEW [IF EXISTS] [db_name.]view_name;

```

`DROP VIEW [IF EXISTS] [db_name.]view_name;
`

DROP returns an error if the view doesn’t exist, unless IF EXISTS is specified
or the configuration variable hive.exec.drop.ignorenonexistent
is set to true.

`DROP`
`IF EXISTS`

### Examples#


```
DROP VIEW IF EXISTS v1;

```

`DROP VIEW IF EXISTS v1;
`

## DROP MARCO#


DROP MARCO statement is used to drop the existing MARCO.
Please refer to CREATE MARCO for how to create MARCO.

`DROP MARCO`
`MARCO`
`MARCO`

### Syntax#


```
DROP TEMPORARY MACRO [IF EXISTS] macro_name;

```

`DROP TEMPORARY MACRO [IF EXISTS] macro_name;
`

DROP returns an error if the macro doesn’t exist, unless IF EXISTS is specified.

`DROP`
`IF EXISTS`

### Examples#


```
DROP TEMPORARY MACRO IF EXISTS m1;

```

`DROP TEMPORARY MACRO IF EXISTS m1;
`

## DROP FUNCTION#


DROP FUNCTION statement is used to drop the existing FUNCTION.

`DROP FUNCTION`
`FUNCTION`

### Syntax#


```
--- Drop temporary function
DROP TEMPORARY FUNCTION [IF EXISTS] function_name;

--- Drop permanent function
DROP FUNCTION [IF EXISTS] function_name;

```

`--- Drop temporary function
DROP TEMPORARY FUNCTION [IF EXISTS] function_name;

--- Drop permanent function
DROP FUNCTION [IF EXISTS] function_name;
`

DROP returns an error if the function doesn’t exist, unless IF EXISTS is specified
or the configuration variable hive.exec.drop.ignorenonexistent
is set to true.

`DROP`
`IF EXISTS`

### Examples#


```
DROP FUNCTION IF EXISTS f1;

```

`DROP FUNCTION IF EXISTS f1;
`