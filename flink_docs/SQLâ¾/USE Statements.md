# USE Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# USE Statements#


USE statements are used to set the current database or catalog, or change the resolution order and enabled status of module.


## Run a USE statement#


USE statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns ‘OK’ for a successful USE operation, otherwise will throw an exception.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run a USE statement in TableEnvironment.

`TableEnvironment`

USE statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns ‘OK’ for a successful USE operation, otherwise will throw an exception.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run a USE statement in TableEnvironment.

`TableEnvironment`

USE statements can be executed with the execute_sql() method of the TableEnvironment. The execute_sql() method returns ‘OK’ for a successful USE operation, otherwise will throw an exception.

`execute_sql()`
`TableEnvironment`
`execute_sql()`

The following examples show how to run a USE statement in TableEnvironment.

`TableEnvironment`

USE statements can be executed in SQL CLI.


The following examples show how to run a USE statement in SQL CLI.


```
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

// create a catalog
tEnv.executeSql("CREATE CATALOG cat1 WITH (...)");
tEnv.executeSql("SHOW CATALOGS").print();
// +-----------------+
// |    catalog name |
// +-----------------+
// | default_catalog |
// | cat1            |
// +-----------------+

// change default catalog
tEnv.executeSql("USE CATALOG cat1");

tEnv.executeSql("SHOW DATABASES").print();
// databases are empty
// +---------------+
// | database name |
// +---------------+
// +---------------+

// create a database
tEnv.executeSql("CREATE DATABASE db1 WITH (...)");
tEnv.executeSql("SHOW DATABASES").print();
// +---------------+
// | database name |
// +---------------+
// |        db1    |
// +---------------+

// change default database
tEnv.executeSql("USE db1");

// change module resolution order and enabled status
tEnv.executeSql("USE MODULES hive");
tEnv.executeSql("SHOW FULL MODULES").print();
// +-------------+-------+
// | module name |  used |
// +-------------+-------+
// |        hive |  true |
// |        core | false |
// +-------------+-------+

```

`StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

// create a catalog
tEnv.executeSql("CREATE CATALOG cat1 WITH (...)");
tEnv.executeSql("SHOW CATALOGS").print();
// +-----------------+
// |    catalog name |
// +-----------------+
// | default_catalog |
// | cat1            |
// +-----------------+

// change default catalog
tEnv.executeSql("USE CATALOG cat1");

tEnv.executeSql("SHOW DATABASES").print();
// databases are empty
// +---------------+
// | database name |
// +---------------+
// +---------------+

// create a database
tEnv.executeSql("CREATE DATABASE db1 WITH (...)");
tEnv.executeSql("SHOW DATABASES").print();
// +---------------+
// | database name |
// +---------------+
// |        db1    |
// +---------------+

// change default database
tEnv.executeSql("USE db1");

// change module resolution order and enabled status
tEnv.executeSql("USE MODULES hive");
tEnv.executeSql("SHOW FULL MODULES").print();
// +-------------+-------+
// | module name |  used |
// +-------------+-------+
// |        hive |  true |
// |        core | false |
// +-------------+-------+
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
val tEnv = StreamTableEnvironment.create(env)

// create a catalog
tEnv.executeSql("CREATE CATALOG cat1 WITH (...)")
tEnv.executeSql("SHOW CATALOGS").print()
// +-----------------+
// |    catalog name |
// +-----------------+
// | default_catalog |
// | cat1            |
// +-----------------+

// change default catalog
tEnv.executeSql("USE CATALOG cat1")

tEnv.executeSql("SHOW DATABASES").print()
// databases are empty
// +---------------+
// | database name |
// +---------------+
// +---------------+

// create a database
tEnv.executeSql("CREATE DATABASE db1 WITH (...)")
tEnv.executeSql("SHOW DATABASES").print()
// +---------------+
// | database name |
// +---------------+
// |        db1    |
// +---------------+

// change default database
tEnv.executeSql("USE db1")

// change module resolution order and enabled status
tEnv.executeSql("USE MODULES hive")
tEnv.executeSql("SHOW FULL MODULES").print()
// +-------------+-------+
// | module name |  used |
// +-------------+-------+
// |        hive |  true |
// |        core | false |
// +-------------+-------+

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
val tEnv = StreamTableEnvironment.create(env)

// create a catalog
tEnv.executeSql("CREATE CATALOG cat1 WITH (...)")
tEnv.executeSql("SHOW CATALOGS").print()
// +-----------------+
// |    catalog name |
// +-----------------+
// | default_catalog |
// | cat1            |
// +-----------------+

// change default catalog
tEnv.executeSql("USE CATALOG cat1")

tEnv.executeSql("SHOW DATABASES").print()
// databases are empty
// +---------------+
// | database name |
// +---------------+
// +---------------+

// create a database
tEnv.executeSql("CREATE DATABASE db1 WITH (...)")
tEnv.executeSql("SHOW DATABASES").print()
// +---------------+
// | database name |
// +---------------+
// |        db1    |
// +---------------+

// change default database
tEnv.executeSql("USE db1")

// change module resolution order and enabled status
tEnv.executeSql("USE MODULES hive")
tEnv.executeSql("SHOW FULL MODULES").print()
// +-------------+-------+
// | module name |  used |
// +-------------+-------+
// |        hive |  true |
// |        core | false |
// +-------------+-------+
`

```
table_env = StreamTableEnvironment.create(...)

# create a catalog
table_env.execute_sql("CREATE CATALOG cat1 WITH (...)")
table_env.execute_sql("SHOW CATALOGS").print()
# +-----------------+
# |    catalog name |
# +-----------------+
# | default_catalog |
# | cat1            |
# +-----------------+

# change default catalog
table_env.execute_sql("USE CATALOG cat1")

table_env.execute_sql("SHOW DATABASES").print()
# databases are empty
# +---------------+
# | database name |
# +---------------+
# +---------------+

# create a database
table_env.execute_sql("CREATE DATABASE db1 WITH (...)")
table_env.execute_sql("SHOW DATABASES").print()
# +---------------+
# | database name |
# +---------------+
# |           db1 |
# +---------------+

# change default database
table_env.execute_sql("USE db1")

# change module resolution order and enabled status
table_env.execute_sql("USE MODULES hive")
table_env.execute_sql("SHOW FULL MODULES").print()
# +-------------+-------+
# | module name |  used |
# +-------------+-------+
# |        hive |  true |
# |        core | false |
# +-------------+-------+

```

`table_env = StreamTableEnvironment.create(...)

# create a catalog
table_env.execute_sql("CREATE CATALOG cat1 WITH (...)")
table_env.execute_sql("SHOW CATALOGS").print()
# +-----------------+
# |    catalog name |
# +-----------------+
# | default_catalog |
# | cat1            |
# +-----------------+

# change default catalog
table_env.execute_sql("USE CATALOG cat1")

table_env.execute_sql("SHOW DATABASES").print()
# databases are empty
# +---------------+
# | database name |
# +---------------+
# +---------------+

# create a database
table_env.execute_sql("CREATE DATABASE db1 WITH (...)")
table_env.execute_sql("SHOW DATABASES").print()
# +---------------+
# | database name |
# +---------------+
# |           db1 |
# +---------------+

# change default database
table_env.execute_sql("USE db1")

# change module resolution order and enabled status
table_env.execute_sql("USE MODULES hive")
table_env.execute_sql("SHOW FULL MODULES").print()
# +-------------+-------+
# | module name |  used |
# +-------------+-------+
# |        hive |  true |
# |        core | false |
# +-------------+-------+
`

```
Flink SQL> CREATE CATALOG cat1 WITH (...);
[INFO] Catalog has been created.

Flink SQL> SHOW CATALOGS;
default_catalog
cat1

Flink SQL> USE CATALOG cat1;

Flink SQL> SHOW DATABASES;

Flink SQL> CREATE DATABASE db1 WITH (...);
[INFO] Database has been created.

Flink SQL> SHOW DATABASES;
db1

Flink SQL> USE db1;

Flink SQL> USE MODULES hive;
[INFO] Use modules succeeded!
Flink SQL> SHOW FULL MODULES;
+-------------+-------+
| module name |  used |
+-------------+-------+
|        hive |  true |
|        core | false |
+-------------+-------+
2 rows in set

```

`Flink SQL> CREATE CATALOG cat1 WITH (...);
[INFO] Catalog has been created.

Flink SQL> SHOW CATALOGS;
default_catalog
cat1

Flink SQL> USE CATALOG cat1;

Flink SQL> SHOW DATABASES;

Flink SQL> CREATE DATABASE db1 WITH (...);
[INFO] Database has been created.

Flink SQL> SHOW DATABASES;
db1

Flink SQL> USE db1;

Flink SQL> USE MODULES hive;
[INFO] Use modules succeeded!
Flink SQL> SHOW FULL MODULES;
+-------------+-------+
| module name |  used |
+-------------+-------+
|        hive |  true |
|        core | false |
+-------------+-------+
2 rows in set
`

 Back to top


## USE CATALOG#


```
USE CATALOG catalog_name

```

`USE CATALOG catalog_name
`

Set the current catalog. All subsequent commands that do not explicitly specify a catalog will use this one. If the provided catalog does not exist, an exception is thrown. The default current catalog is default_catalog.

`default_catalog`

## USE MODULES#


```
USE MODULES module_name1[, module_name2, ...]

```

`USE MODULES module_name1[, module_name2, ...]
`

Set the enabled modules with declared order. All subsequent commands will resolve metadata(functions/user-defined types/rules, etc.) within enabled modules and follow resolution order. A module is used by default when it is loaded. Loaded modules will become disabled if not used by USE MODULES statement. The default loaded and enabled module is core.

`USE MODULES`
`core`

## USE#


```
USE [catalog_name.]database_name

```

`USE [catalog_name.]database_name
`

Set the current database. All subsequent commands that do not explicitly specify a database will use this one. If the provided database does not exist, an exception is thrown. The default current database is default_database.

`default_database`