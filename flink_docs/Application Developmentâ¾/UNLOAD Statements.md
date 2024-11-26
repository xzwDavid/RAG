# UNLOAD Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# UNLOAD Statements#


UNLOAD statements are used to unload a built-in or user-defined module.


## Run a UNLOAD statement#


UNLOAD statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns ‘OK’ for a successful UNLOAD operation; otherwise it will throw an exception.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run a UNLOAD statement in TableEnvironment.

`TableEnvironment`

UNLOAD statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns ‘OK’ for a successful UNLOAD operation; otherwise it will throw an exception.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run a UNLOAD statement in TableEnvironment.

`TableEnvironment`

UNLOAD statements can be executed with the execute_sql() method of the TableEnvironment. The execute_sql() method returns ‘OK’ for a successful UNLOAD operation; otherwise it will throw an exception.

`execute_sql()`
`TableEnvironment`
`execute_sql()`

The following examples show how to run a UNLOAD statement in TableEnvironment.

`TableEnvironment`

UNLOAD statements can be executed in SQL CLI.


The following examples show how to run a UNLOAD statement in SQL CLI.


```
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

// unload a core module
tEnv.executeSql("UNLOAD MODULE core");
tEnv.executeSql("SHOW MODULES").print();
// Empty set

```

`StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

// unload a core module
tEnv.executeSql("UNLOAD MODULE core");
tEnv.executeSql("SHOW MODULES").print();
// Empty set
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
val tEnv = StreamTableEnvironment.create(env)

// unload a core module
tEnv.executeSql("UNLOAD MODULE core")
tEnv.executeSql("SHOW MODULES").print()
// Empty set

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
val tEnv = StreamTableEnvironment.create(env)

// unload a core module
tEnv.executeSql("UNLOAD MODULE core")
tEnv.executeSql("SHOW MODULES").print()
// Empty set
`

```
table_env = StreamTableEnvironment.create(...)

# unload a core module
table_env.execute_sql("UNLOAD MODULE core")
table_env.execute_sql("SHOW MODULES").print()
# Empty set

```

`table_env = StreamTableEnvironment.create(...)

# unload a core module
table_env.execute_sql("UNLOAD MODULE core")
table_env.execute_sql("SHOW MODULES").print()
# Empty set
`

```
Flink SQL> UNLOAD MODULE core;
[INFO] Unload module succeeded!

Flink SQL> SHOW MODULES;
Empty set

```

`Flink SQL> UNLOAD MODULE core;
[INFO] Unload module succeeded!

Flink SQL> SHOW MODULES;
Empty set
`

 Back to top


## UNLOAD MODULE#


The following grammar gives an overview of the available syntax:


```
UNLOAD MODULE module_name

```

`UNLOAD MODULE module_name
`