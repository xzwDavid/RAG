# DROP Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# DROP Statements#


DROP statements are used to remove a catalog with the given catalog name or to remove a registered table/view/function from the current or specified Catalog.


Flink SQL supports the following DROP statements for now:

* DROP CATALOG
* DROP TABLE
* DROP DATABASE
* DROP VIEW
* DROP FUNCTION

## Run a DROP statement#




Java
DROP statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns ‘OK’ for a successful DROP operation, otherwise will throw an exception.
The following examples show how to run a DROP statement in TableEnvironment.

Scala
DROP statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns ‘OK’ for a successful DROP operation, otherwise will throw an exception.
The following examples show how to run a DROP statement in TableEnvironment.

Python
DROP statements can be executed with the execute_sql() method of the TableEnvironment. The execute_sql() method returns ‘OK’ for a successful DROP operation, otherwise will throw an exception.
The following examples show how to run a DROP statement in TableEnvironment.

SQL CLI
DROP statements can be in SQL CLI.
The following examples show how to run a DROP statement in SQL CLI.


Java
TableEnvironment tableEnv = TableEnvironment.create(...);

// register a table named "Orders"
tableEnv.executeSql("CREATE TABLE Orders (`user` BIGINT, product STRING, amount INT) WITH (...)");

// a string array: ["Orders"]
String[] tables = tableEnv.listTables();
// or tableEnv.executeSql("SHOW TABLES").print();

// drop "Orders" table from catalog
tableEnv.executeSql("DROP TABLE Orders");

// an empty string array
String[] tables = tableEnv.listTables();
// or tableEnv.executeSql("SHOW TABLES").print();

Scala
val tableEnv = TableEnvironment.create(...)

// register a table named "Orders"
tableEnv.executeSql("CREATE TABLE Orders (`user` BIGINT, product STRING, amount INT) WITH (...)")

// a string array: ["Orders"]
val tables = tableEnv.listTables()
// or tableEnv.executeSql("SHOW TABLES").print()

// drop "Orders" table from catalog
tableEnv.executeSql("DROP TABLE Orders")

// an empty string array
val tables = tableEnv.listTables()
// or tableEnv.executeSql("SHOW TABLES").print()

Python
table_env = TableEnvironment.create(...)

# a string array: ["Orders"]
tables = table_env.list_tables()
# or table_env.execute_sql("SHOW TABLES").print()

# drop "Orders" table from catalog
table_env.execute_sql("DROP TABLE Orders")

# an empty string array
tables = table_env.list_tables()
# or table_env.execute_sql("SHOW TABLES").print()

SQL CLI
Flink SQL> CREATE TABLE Orders (`user` BIGINT, product STRING, amount INT) WITH (...);
[INFO] Table has been created.

Flink SQL> SHOW TABLES;
Orders

Flink SQL> DROP TABLE Orders;
[INFO] Table has been removed.

Flink SQL> SHOW TABLES;
[INFO] Result was empty.




DROP statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns ‘OK’ for a successful DROP operation, otherwise will throw an exception.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run a DROP statement in TableEnvironment.

`TableEnvironment`

DROP statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns ‘OK’ for a successful DROP operation, otherwise will throw an exception.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run a DROP statement in TableEnvironment.

`TableEnvironment`

DROP statements can be executed with the execute_sql() method of the TableEnvironment. The execute_sql() method returns ‘OK’ for a successful DROP operation, otherwise will throw an exception.

`execute_sql()`
`TableEnvironment`
`execute_sql()`

The following examples show how to run a DROP statement in TableEnvironment.

`TableEnvironment`

DROP statements can be in SQL CLI.


The following examples show how to run a DROP statement in SQL CLI.


```
TableEnvironment tableEnv = TableEnvironment.create(...);

// register a table named "Orders"
tableEnv.executeSql("CREATE TABLE Orders (`user` BIGINT, product STRING, amount INT) WITH (...)");

// a string array: ["Orders"]
String[] tables = tableEnv.listTables();
// or tableEnv.executeSql("SHOW TABLES").print();

// drop "Orders" table from catalog
tableEnv.executeSql("DROP TABLE Orders");

// an empty string array
String[] tables = tableEnv.listTables();
// or tableEnv.executeSql("SHOW TABLES").print();

```

`TableEnvironment tableEnv = TableEnvironment.create(...);

// register a table named "Orders"
tableEnv.executeSql("CREATE TABLE Orders (`user` BIGINT, product STRING, amount INT) WITH (...)");

// a string array: ["Orders"]
String[] tables = tableEnv.listTables();
// or tableEnv.executeSql("SHOW TABLES").print();

// drop "Orders" table from catalog
tableEnv.executeSql("DROP TABLE Orders");

// an empty string array
String[] tables = tableEnv.listTables();
// or tableEnv.executeSql("SHOW TABLES").print();
`

```
val tableEnv = TableEnvironment.create(...)

// register a table named "Orders"
tableEnv.executeSql("CREATE TABLE Orders (`user` BIGINT, product STRING, amount INT) WITH (...)")

// a string array: ["Orders"]
val tables = tableEnv.listTables()
// or tableEnv.executeSql("SHOW TABLES").print()

// drop "Orders" table from catalog
tableEnv.executeSql("DROP TABLE Orders")

// an empty string array
val tables = tableEnv.listTables()
// or tableEnv.executeSql("SHOW TABLES").print()

```

`val tableEnv = TableEnvironment.create(...)

// register a table named "Orders"
tableEnv.executeSql("CREATE TABLE Orders (`user` BIGINT, product STRING, amount INT) WITH (...)")

// a string array: ["Orders"]
val tables = tableEnv.listTables()
// or tableEnv.executeSql("SHOW TABLES").print()

// drop "Orders" table from catalog
tableEnv.executeSql("DROP TABLE Orders")

// an empty string array
val tables = tableEnv.listTables()
// or tableEnv.executeSql("SHOW TABLES").print()
`

```
table_env = TableEnvironment.create(...)

# a string array: ["Orders"]
tables = table_env.list_tables()
# or table_env.execute_sql("SHOW TABLES").print()

# drop "Orders" table from catalog
table_env.execute_sql("DROP TABLE Orders")

# an empty string array
tables = table_env.list_tables()
# or table_env.execute_sql("SHOW TABLES").print()

```

`table_env = TableEnvironment.create(...)

# a string array: ["Orders"]
tables = table_env.list_tables()
# or table_env.execute_sql("SHOW TABLES").print()

# drop "Orders" table from catalog
table_env.execute_sql("DROP TABLE Orders")

# an empty string array
tables = table_env.list_tables()
# or table_env.execute_sql("SHOW TABLES").print()
`

```
Flink SQL> CREATE TABLE Orders (`user` BIGINT, product STRING, amount INT) WITH (...);
[INFO] Table has been created.

Flink SQL> SHOW TABLES;
Orders

Flink SQL> DROP TABLE Orders;
[INFO] Table has been removed.

Flink SQL> SHOW TABLES;
[INFO] Result was empty.

```

`Flink SQL> CREATE TABLE Orders (`user` BIGINT, product STRING, amount INT) WITH (...);
[INFO] Table has been created.

Flink SQL> SHOW TABLES;
Orders

Flink SQL> DROP TABLE Orders;
[INFO] Table has been removed.

Flink SQL> SHOW TABLES;
[INFO] Result was empty.
`

## DROP CATALOG#


```
DROP CATALOG [IF EXISTS] catalog_name

```

`DROP CATALOG [IF EXISTS] catalog_name
`

Drop a catalog with the given catalog name.


IF EXISTS


If the catalog does not exist, nothing happens.


## DROP TABLE#


```
DROP [TEMPORARY] TABLE [IF EXISTS] [catalog_name.][db_name.]table_name

```

`DROP [TEMPORARY] TABLE [IF EXISTS] [catalog_name.][db_name.]table_name
`

Drop a table with the given table name. If the table to drop does not exist, an exception is thrown.


TEMPORARY


Drop temporary table that has catalog and database namespaces.


IF EXISTS


If the table does not exist, nothing happens.


## DROP DATABASE#


```
DROP DATABASE [IF EXISTS] [catalog_name.]db_name [ (RESTRICT | CASCADE) ]

```

`DROP DATABASE [IF EXISTS] [catalog_name.]db_name [ (RESTRICT | CASCADE) ]
`

Drop a database with the given database name. If the database to drop does not exist, an exception is thrown.


IF EXISTS


If the database does not exist, nothing happens.


RESTRICT


Dropping a non-empty database triggers an exception. Enabled by default.


CASCADE


Dropping a non-empty database also drops all associated tables and functions.


## DROP VIEW#


```
DROP [TEMPORARY] VIEW  [IF EXISTS] [catalog_name.][db_name.]view_name

```

`DROP [TEMPORARY] VIEW  [IF EXISTS] [catalog_name.][db_name.]view_name
`

Drop a view that has catalog and database namespaces. If the view to drop does not exist, an exception is thrown.


TEMPORARY


Drop temporary view that has catalog and database namespaces.


IF EXISTS


If the view does not exist, nothing happens.


MAINTAIN DEPENDENCIES
Flink does not maintain dependencies of view by CASCADE/RESTRICT keywords, the current way is producing postpone error message when user tries to use the view under the scenarios like the underlying table of view has been dropped.


## DROP FUNCTION#


```
DROP [TEMPORARY|TEMPORARY SYSTEM] FUNCTION [IF EXISTS] [catalog_name.][db_name.]function_name;

```

`DROP [TEMPORARY|TEMPORARY SYSTEM] FUNCTION [IF EXISTS] [catalog_name.][db_name.]function_name;
`

Drop a catalog function that has catalog and database namespaces. If the function to drop does not exist, an exception is thrown.


TEMPORARY


Drop temporary catalog function that has catalog and database namespaces.


TEMPORARY SYSTEM


Drop temporary system function that has no namespace.


IF EXISTS


If the function doesn’t exists, nothing happens.
