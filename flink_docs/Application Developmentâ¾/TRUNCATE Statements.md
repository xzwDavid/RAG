# TRUNCATE Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# TRUNCATE Statements#


TRUNCATE statements are used to delete all rows from a table without dropping the table itself.


Attention Currently, TRUNCATE statement is supported in batch mode, and it requires the target table connector implements the  

    SupportsTruncate


interface to support the row-level delete. An exception will be thrown if trying to TRUNCATE a table which has not implemented the related interface.

`TRUNCATE`
`TRUNCATE`

## Run a TRUNCATE statement#


TRUNCATE statement can be executed with the executeSql() method of the TableEnvironment. The executeSql() method will throw an exception when there is any error for the operation.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run a TRUNCATE statement in TableEnvironment.

`TableEnvironment`

TRUNCATE statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() will throw an exception when there is any error for the operation.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run a single TRUNCATE statement in TableEnvironment.

`TableEnvironment`

TRUNCATE statements can be executed with the execute_sql() method of the TableEnvironment. The execute_sql() will throw an exception when there is any error for the operation.

`execute_sql()`
`TableEnvironment`
`execute_sql()`

The following examples show how to run a single TRUNCATE statement in TableEnvironment.

`TableEnvironment`

TRUNCATE statement can be executed in SQL CLI.


The following examples show how to run a TRUNCATE statement in SQL CLI.


```
EnvironmentSettings settings = EnvironmentSettings.newInstance().inBatchMode().build();
TableEnvironment tEnv = TableEnvironment.create(settings);

// register a table named "Orders"
tEnv.executeSql("CREATE TABLE Orders (`user` STRING, product STRING, amount INT) WITH (...)");

// insert values
tEnv.executeSql("INSERT INTO Orders VALUES ('Lili', 'Apple', 1), ('Jessica', 'Banana', 2), ('Mr.White', 'Chicken', 3)").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// +--------------------------------+--------------------------------+-------------+
// |                           user |                        product |      amount |
// +--------------------------------+--------------------------------+-------------+
// |                           Lili |                          Apple |           1 |
// |                        Jessica |                         Banana |           2 |
// |                       Mr.White |                        Chicken |           3 |
// +--------------------------------+--------------------------------+-------------+
// 3 rows in set
        
// truncate the table "Orders"
tEnv.executeSql("TRUNCATE TABLE Orders").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// Empty set

```

`EnvironmentSettings settings = EnvironmentSettings.newInstance().inBatchMode().build();
TableEnvironment tEnv = TableEnvironment.create(settings);

// register a table named "Orders"
tEnv.executeSql("CREATE TABLE Orders (`user` STRING, product STRING, amount INT) WITH (...)");

// insert values
tEnv.executeSql("INSERT INTO Orders VALUES ('Lili', 'Apple', 1), ('Jessica', 'Banana', 2), ('Mr.White', 'Chicken', 3)").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// +--------------------------------+--------------------------------+-------------+
// |                           user |                        product |      amount |
// +--------------------------------+--------------------------------+-------------+
// |                           Lili |                          Apple |           1 |
// |                        Jessica |                         Banana |           2 |
// |                       Mr.White |                        Chicken |           3 |
// +--------------------------------+--------------------------------+-------------+
// 3 rows in set
        
// truncate the table "Orders"
tEnv.executeSql("TRUNCATE TABLE Orders").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// Empty set
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
val settings = EnvironmentSettings.newInstance().inBatchMode().build()
val tEnv = StreamTableEnvironment.create(env, settings)

// register a table named "Orders"
tEnv.executeSql("CREATE TABLE Orders (`user` STRING, product STRING, amount INT) WITH (...)")
// insert values
tEnv.executeSql("INSERT INTO Orders VALUES ('Lili', 'Apple', 1), ('Jessica', 'Banana', 2), ('Mr.White', 'Chicken', 3)").await()
tEnv.executeSql("SELECT * FROM Orders").print()
// +--------------------------------+--------------------------------+-------------+
// |                           user |                        product |      amount |
// +--------------------------------+--------------------------------+-------------+
// |                           Lili |                          Apple |           1 |
// |                        Jessica |                         Banana |           2 |
// |                       Mr.White |                        Chicken |           3 |
// +--------------------------------+--------------------------------+-------------+
// 3 rows in set
// truncate the table "Orders"
tEnv.executeSql("TRUNCATE TABLE Orders").await()
tEnv.executeSql("SELECT * FROM Orders").print()
// Empty set

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
val settings = EnvironmentSettings.newInstance().inBatchMode().build()
val tEnv = StreamTableEnvironment.create(env, settings)

// register a table named "Orders"
tEnv.executeSql("CREATE TABLE Orders (`user` STRING, product STRING, amount INT) WITH (...)")
// insert values
tEnv.executeSql("INSERT INTO Orders VALUES ('Lili', 'Apple', 1), ('Jessica', 'Banana', 2), ('Mr.White', 'Chicken', 3)").await()
tEnv.executeSql("SELECT * FROM Orders").print()
// +--------------------------------+--------------------------------+-------------+
// |                           user |                        product |      amount |
// +--------------------------------+--------------------------------+-------------+
// |                           Lili |                          Apple |           1 |
// |                        Jessica |                         Banana |           2 |
// |                       Mr.White |                        Chicken |           3 |
// +--------------------------------+--------------------------------+-------------+
// 3 rows in set
// truncate the table "Orders"
tEnv.executeSql("TRUNCATE TABLE Orders").await()
tEnv.executeSql("SELECT * FROM Orders").print()
// Empty set
`

```
env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

# register a table named "Orders"
table_env.execute_sql("CREATE TABLE Orders (`user` STRING, product STRING, amount INT) WITH (...)")
# insert values
table_env.execute_sql("INSERT INTO Orders VALUES ('Lili', 'Apple', 1), ('Jessica', 'Banana', 2), ('Mr.White', 'Chicken', 3)").wait()
table_env.execute_sql("SELECT * FROM Orders").print()
# +--------------------------------+--------------------------------+-------------+
# |                           user |                        product |      amount |
# +--------------------------------+--------------------------------+-------------+
# |                           Lili |                          Apple |           1 |
# |                        Jessica |                         Banana |           2 |
# |                       Mr.White |                        Chicken |           3 |
# +--------------------------------+--------------------------------+-------------+
# 3 rows in set
# truncate the table "Orders"
table_env.execute_sql("TRUNCATE TABLE Orders").wait()
table_env.execute_sql("SELECT * FROM Orders").print()
# Empty set

```

`env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

# register a table named "Orders"
table_env.execute_sql("CREATE TABLE Orders (`user` STRING, product STRING, amount INT) WITH (...)")
# insert values
table_env.execute_sql("INSERT INTO Orders VALUES ('Lili', 'Apple', 1), ('Jessica', 'Banana', 2), ('Mr.White', 'Chicken', 3)").wait()
table_env.execute_sql("SELECT * FROM Orders").print()
# +--------------------------------+--------------------------------+-------------+
# |                           user |                        product |      amount |
# +--------------------------------+--------------------------------+-------------+
# |                           Lili |                          Apple |           1 |
# |                        Jessica |                         Banana |           2 |
# |                       Mr.White |                        Chicken |           3 |
# +--------------------------------+--------------------------------+-------------+
# 3 rows in set
# truncate the table "Orders"
table_env.execute_sql("TRUNCATE TABLE Orders").wait()
table_env.execute_sql("SELECT * FROM Orders").print()
# Empty set
`

```
Flink SQL> SET 'execution.runtime-mode' = 'batch';
[INFO] Session property has been set.

Flink SQL> CREATE TABLE Orders (`user` STRING, product STRING, amount INT) with (...);
[INFO] Execute statement succeeded.

Flink SQL> INSERT INTO Orders VALUES ('Lili', 'Apple', 1), ('Jessica', 'Banana', 1), ('Mr.White', 'Chicken', 3);
[INFO] Submitting SQL update statement to the cluster...
[INFO] SQL update statement has been successfully submitted to the cluster:
Job ID: bd2c46a7b2769d5c559abd73ecde82e9

Flink SQL> SELECT * FROM Orders;
    user                         product      amount
    Lili                           Apple           1
 Jessica                          Banana           2
Mr.White                         Chicken           3

Flink SQL> TRUNCATE TABLE Orders;
[INFO] Execute statement succeeded.

Flink SQL> SELECT * FROM Orders;
// Empty set

```

`Flink SQL> SET 'execution.runtime-mode' = 'batch';
[INFO] Session property has been set.

Flink SQL> CREATE TABLE Orders (`user` STRING, product STRING, amount INT) with (...);
[INFO] Execute statement succeeded.

Flink SQL> INSERT INTO Orders VALUES ('Lili', 'Apple', 1), ('Jessica', 'Banana', 1), ('Mr.White', 'Chicken', 3);
[INFO] Submitting SQL update statement to the cluster...
[INFO] SQL update statement has been successfully submitted to the cluster:
Job ID: bd2c46a7b2769d5c559abd73ecde82e9

Flink SQL> SELECT * FROM Orders;
    user                         product      amount
    Lili                           Apple           1
 Jessica                          Banana           2
Mr.White                         Chicken           3

Flink SQL> TRUNCATE TABLE Orders;
[INFO] Execute statement succeeded.

Flink SQL> SELECT * FROM Orders;
// Empty set
`

 Back to top


## Syntax#


```
TRUNCATE TABLE [catalog_name.][db_name.]table_name

```

`TRUNCATE TABLE [catalog_name.][db_name.]table_name
`