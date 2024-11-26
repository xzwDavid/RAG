# CALL Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Call Statements#


Call statements are used to call a stored procedure which is usually provided to perform data manipulation or administrative tasks.

`Call`

Attention Currently, Call statements require the procedure called to exist in the corresponding catalog. So, please make sure the procedure exists in the catalog.
If it doesn’t exist, it’ll throw an exception. You may need to refer to the doc of the catalog to see the available procedures. To implement an procedure, please refer to Procedure.

`Call`

## Run a CALL statement#


CALL statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() will immediately call the procedure, and return a TableResult instance which associates the procedure.

`executeSql()`
`TableEnvironment`
`executeSql()`
`TableResult`

The following examples show how to execute a CALL statement in TableEnvironment.

`TableEnvironment`

CALL statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() will immediately call the procedure, and return a TableResult instance which associates the procedure.

`executeSql()`
`TableEnvironment`
`executeSql()`
`TableResult`

The following examples show how to execute a single CALL statement in TableEnvironment.

`TableEnvironment`

CALL statements can be executed with the execute_sql() method of the TableEnvironment. The executeSql() will immediately call the procedure, and return a TableResult instance which associates the procedure.

`execute_sql()`
`TableEnvironment`
`executeSql()`
`TableResult`

The following examples show how to execute a single CALL statement in TableEnvironment.

`TableEnvironment`

CALL statements can be executed in SQL CLI.


The following examples show how to execute a CALL statement in SQL CLI.


```
TableEnvironment tEnv = TableEnvironment.create(...);

// assuming the procedure `generate_n` has existed in `system` database of the current catalog
tEnv.executeSql("CALL `system`.generate_n(4)").print();

```

`TableEnvironment tEnv = TableEnvironment.create(...);

// assuming the procedure `generate_n` has existed in `system` database of the current catalog
tEnv.executeSql("CALL `system`.generate_n(4)").print();
`

```
val tEnv = TableEnvironment.create(...)

// assuming the procedure `generate_n` has existed in `system` database of the current catalog
tEnv.executeSql("CALL `system`.generate_n(4)").print()

```

`val tEnv = TableEnvironment.create(...)

// assuming the procedure `generate_n` has existed in `system` database of the current catalog
tEnv.executeSql("CALL `system`.generate_n(4)").print()
`

```
table_env = TableEnvironment.create(...)

# assuming the procedure `generate_n` has existed in `system` database of the current catalog
table_env.execute_sql().print()

```

`table_env = TableEnvironment.create(...)

# assuming the procedure `generate_n` has existed in `system` database of the current catalog
table_env.execute_sql().print()
`

```
// assuming the procedure `generate_n` has existed in `system` database of the current catalog
Flink SQL> CALL `system`.generate_n(4);
+--------+
| result |
+--------+
|      0 |
|      1 |
|      2 |
|      3 |    
+--------+
4 rows in set
!ok

```

`// assuming the procedure `generate_n` has existed in `system` database of the current catalog
Flink SQL> CALL `system`.generate_n(4);
+--------+
| result |
+--------+
|      0 |
|      1 |
|      2 |
|      3 |    
+--------+
4 rows in set
!ok
`

 Back to top


## Syntax#


```
CALL [catalog_name.][database_name.]procedure_name ([ expression [, expression]* ] )

```

`CALL [catalog_name.][database_name.]procedure_name ([ expression [, expression]* ] )
`