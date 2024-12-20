# CREATE Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# CREATE Statements#


With Hive dialect, the following CREATE statements are supported for now:

* CREATE DATABASE
* CREATE TABLE
* CREATE VIEW
* CREATE MARCO
* CREATE FUNCTION

## CREATE DATABASE#


### Description#


CREATE DATABASE statement is used to create a database with the specified name.

`CREATE DATABASE`

### Syntax#


```
CREATE (DATABASE|SCHEMA) [IF NOT EXISTS] database_name
  [COMMENT database_comment]
  [LOCATION hdfs_path]
  [WITH DBPROPERTIES (property_name=property_value, ...)];

```

`CREATE (DATABASE|SCHEMA) [IF NOT EXISTS] database_name
  [COMMENT database_comment]
  [LOCATION hdfs_path]
  [WITH DBPROPERTIES (property_name=property_value, ...)];
`

### Examples#


```
CREATE DATABASE db1;
CREATE DATABASE IF NOT EXISTS db1 COMMENT 'db1' LOCATION '/user/hive/warehouse/db1'
    WITH DBPROPERTIES ('name'='example-db');

```

`CREATE DATABASE db1;
CREATE DATABASE IF NOT EXISTS db1 COMMENT 'db1' LOCATION '/user/hive/warehouse/db1'
    WITH DBPROPERTIES ('name'='example-db');
`

## CREATE TABLE#


### Description#


CREATE TABLE statement is used to define a table in an existing database.

`CREATE TABLE`

### Syntax#


```
CREATE [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name
  [(col_name data_type [column_constraint] [COMMENT col_comment], ... [table_constraint])]
  [COMMENT table_comment]
  [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)]
  [
    [ROW FORMAT row_format]
    [STORED AS file_format]
  ]
  [LOCATION fs_path]
  [TBLPROPERTIES (property_name=property_value, ...)]
  [AS select_statment];
  
data_type
  : primitive_type
  | array_type
  | map_type
  | struct_type
primitive_type
  : TINYINT
  | SMALLINT
  | INT
  | BIGINT
  | BOOLEAN
  | FLOAT
  | DOUBLE
  | DOUBLE PRECISION
  | STRING
  | BINARY     
  | TIMESTAMP
  | DECIMAL
  | DECIMAL(precision, scale)
  | DATE
  | VARCHAR
  | CHAR 
array_type
  : ARRAY < data_type >
  
array_type
  : ARRAY < data_type >
struct_type
  : STRUCT < col_name : data_type [COMMENT col_comment], ...>
row_format:
  : DELIMITED [FIELDS TERMINATED BY char [ESCAPED BY char]] [COLLECTION ITEMS TERMINATED BY char]
      [MAP KEYS TERMINATED BY char] [LINES TERMINATED BY char]
      [NULL DEFINED AS char]
  | SERDE serde_name [WITH SERDEPROPERTIES (property_name=property_value, ...)]
file_format:
  : SEQUENCEFILE
  | TEXTFILE
  | RCFILE
  | ORC
  | PARQUET
  | AVRO
  | INPUTFORMAT input_format_classname OUTPUTFORMAT output_format_classname
column_constraint:
  : NOT NULL
table_constraint:
  : [CONSTRAINT constraint_name] PRIMARY KEY (col_name, ...)

```

`CREATE [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.]table_name
  [(col_name data_type [column_constraint] [COMMENT col_comment], ... [table_constraint])]
  [COMMENT table_comment]
  [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)]
  [
    [ROW FORMAT row_format]
    [STORED AS file_format]
  ]
  [LOCATION fs_path]
  [TBLPROPERTIES (property_name=property_value, ...)]
  [AS select_statment];
  
data_type
  : primitive_type
  | array_type
  | map_type
  | struct_type
primitive_type
  : TINYINT
  | SMALLINT
  | INT
  | BIGINT
  | BOOLEAN
  | FLOAT
  | DOUBLE
  | DOUBLE PRECISION
  | STRING
  | BINARY     
  | TIMESTAMP
  | DECIMAL
  | DECIMAL(precision, scale)
  | DATE
  | VARCHAR
  | CHAR 
array_type
  : ARRAY < data_type >
  
array_type
  : ARRAY < data_type >
struct_type
  : STRUCT < col_name : data_type [COMMENT col_comment], ...>
row_format:
  : DELIMITED [FIELDS TERMINATED BY char [ESCAPED BY char]] [COLLECTION ITEMS TERMINATED BY char]
      [MAP KEYS TERMINATED BY char] [LINES TERMINATED BY char]
      [NULL DEFINED AS char]
  | SERDE serde_name [WITH SERDEPROPERTIES (property_name=property_value, ...)]
file_format:
  : SEQUENCEFILE
  | TEXTFILE
  | RCFILE
  | ORC
  | PARQUET
  | AVRO
  | INPUTFORMAT input_format_classname OUTPUTFORMAT output_format_classname
column_constraint:
  : NOT NULL
table_constraint:
  : [CONSTRAINT constraint_name] PRIMARY KEY (col_name, ...)
`

> 
NOTE:

Create temporary table is not supported yet.




NOTE:

* Create temporary table is not supported yet.

### Examples#


```
-- creaet non-partition table
CREATE TABLE t1(key string, value string);

-- creaet partitioned table
CREATE TABLE pt1(key string, value string) PARTITIONED BY (year int, month int);

-- creaet table with specifc format
CREATE TABLE t1(key string, value string) STORED AS ORC;

-- create table with specifc rowfromat
CREATE TABLE t1(m MAP<BIGINT, STRING>) 
  ROW FROMAT DELIMITED COLLECTION ITEMS TERMINATED BY ';'
  MAP KEYS TERMINATED BY ':';

-- create table as select
CREATE TABLE t2 AS SELECT key, COUNT(1) FROM t1 GROUP BY key;

```

`-- creaet non-partition table
CREATE TABLE t1(key string, value string);

-- creaet partitioned table
CREATE TABLE pt1(key string, value string) PARTITIONED BY (year int, month int);

-- creaet table with specifc format
CREATE TABLE t1(key string, value string) STORED AS ORC;

-- create table with specifc rowfromat
CREATE TABLE t1(m MAP<BIGINT, STRING>) 
  ROW FROMAT DELIMITED COLLECTION ITEMS TERMINATED BY ';'
  MAP KEYS TERMINATED BY ':';

-- create table as select
CREATE TABLE t2 AS SELECT key, COUNT(1) FROM t1 GROUP BY key;
`

## CREATE VIEW#


### Description#


CREATE VIEW creates a view with the given name.
If no column names are supplied, the names of the view’s columns will be derived automatically from the defining SELECT expression.
(If the SELECT contains un-aliased scalar expressions such as x+y, the resulting view column names will be generated in the form _C0, _C1, etc.)
When renaming columns, column comments can also optionally be supplied. (Comments are not automatically inherited from underlying columns.)

`CREATE VIEW`

Note that a view is a purely logical object with no associated storage. When a query references a view, the view’s definition is evaluated in order to produce a set of rows for further processing by the query.


### Syntax#


```
CREATE VIEW [IF NOT EXISTS] [db_name.]view_name [(column_name, ...) ]
  [COMMENT view_comment]
  [TBLPROPERTIES (property_name = property_value, ...)]
  AS SELECT ...;

```

`CREATE VIEW [IF NOT EXISTS] [db_name.]view_name [(column_name, ...) ]
  [COMMENT view_comment]
  [TBLPROPERTIES (property_name = property_value, ...)]
  AS SELECT ...;
`

### Examples#


```
CREATE VIEW IF NOT EXISTS v1
    (key COMMENT 'key') 
    COMMENT 'View for key=1'
    AS SELECT key FROM src
        WHERE key = '1';

```

`CREATE VIEW IF NOT EXISTS v1
    (key COMMENT 'key') 
    COMMENT 'View for key=1'
    AS SELECT key FROM src
        WHERE key = '1';
`

## CREATE MARCO#


### Description#


CREATE TEMPORARY MACRO statement creates a macro using the given optional list of columns as inputs to the expression.
Macros exists for the duration of the current session.

`CREATE TEMPORARY MACRO`

### Syntax#


```
CREATE TEMPORARY MACRO macro_name([col_name col_type, ...]) expression;

```

`CREATE TEMPORARY MACRO macro_name([col_name col_type, ...]) expression;
`

### Examples#


```
CREATE TEMPORARY MACRO fixed_number() 42;
CREATE TEMPORARY MACRO string_len_plus_two(x string) length(x) + 2;
CREATE TEMPORARY MACRO simple_add (x int, y int) x + y;

```

`CREATE TEMPORARY MACRO fixed_number() 42;
CREATE TEMPORARY MACRO string_len_plus_two(x string) length(x) + 2;
CREATE TEMPORARY MACRO simple_add (x int, y int) x + y;
`

## CREATE FUNCTION#


### Description#


 CREATE FUNCTION statement creates a function that is implemented by the class_name.

` CREATE FUNCTION`

### Syntax#


#### Create Temporary Function#


```
CREATE TEMPORARY FUNCTION function_name AS class_name [USING JAR 'file_uri'];

```

`CREATE TEMPORARY FUNCTION function_name AS class_name [USING JAR 'file_uri'];
`

The function exists for the duration of the current session.


#### Create Permanent Function#


```
CREATE FUNCTION [db_name.]function_name AS class_name
  [USING JAR 'file_uri'];

```

`CREATE FUNCTION [db_name.]function_name AS class_name
  [USING JAR 'file_uri'];
`

The function is registered to metastore and will exist in all session unless the function is dropped.


### Parameter#

* 
[USING JAR 'file_uri']
User can use the clause to add Jar that contains the implementation of the function along with its dependencies while creating the function.
The file_uri can be on local file or distributed file system.
Flink will automatically download the jars for remote jars when the function is used in queries. The downloaded jars will be removed when the session exits.


[USING JAR 'file_uri']

`[USING JAR 'file_uri']`

User can use the clause to add Jar that contains the implementation of the function along with its dependencies while creating the function.
The file_uri can be on local file or distributed file system.
Flink will automatically download the jars for remote jars when the function is used in queries. The downloaded jars will be removed when the session exits.

`file_uri`

### Examples#


```
-- create a function assuming the class `SimpleUdf` has existed in class path
CREATE FUNCTION simple_udf AS 'SimpleUdf';

-- create function using jar assuming the class `SimpleUdf` hasn't existed in class path
CREATE FUNCTION simple_udf AS 'SimpleUdf' USING JAR '/tmp/SimpleUdf.jar';

-- create function using remote jar
CREATE FUNCTION simple_udf AS 'SimpleUdf' USING JAR 'hdfs://namenode-host:port/path/SimpleUdf.jar';

```

`-- create a function assuming the class `SimpleUdf` has existed in class path
CREATE FUNCTION simple_udf AS 'SimpleUdf';

-- create function using jar assuming the class `SimpleUdf` hasn't existed in class path
CREATE FUNCTION simple_udf AS 'SimpleUdf' USING JAR '/tmp/SimpleUdf.jar';

-- create function using remote jar
CREATE FUNCTION simple_udf AS 'SimpleUdf' USING JAR 'hdfs://namenode-host:port/path/SimpleUdf.jar';
`