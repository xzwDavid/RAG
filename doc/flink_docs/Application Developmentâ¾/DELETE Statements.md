# DELETE Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# DELETE Statements#


DELETE statement is used to perform row-level deletion on the target table according to the filter if provided.

`DELETE`

Attention Currently, DELETE statement only supports in batch mode, and it requires the target table connector implements the  

    SupportsRowLevelDelete


interface to support the row-level delete. An exception will be thrown if trying to DELETE the table which has not implements the related interface. Currently, there is no existing connector maintained by flink has supported DELETE yet.

`DELETE`
`DELETE`

## Run a DELETE statement#


DELETE statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() will submit a Flink job immediately, and return a TableResult instance which associates the submitted job.

`executeSql()`
`TableEnvironment`
`executeSql()`
`TableResult`

The following examples show how to run a single DELETE statement in TableEnvironment.

`TableEnvironment`

DELETE statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() will submit a Flink job immediately, and return a TableResult instance which associates the submitted job.

`executeSql()`
`TableEnvironment`
`executeSql()`
`TableResult`

The following examples show how to run a single DELETE statement in TableEnvironment.

`TableEnvironment`

DELETE statements can be executed with the execute_sql() method of the TableEnvironment. The executeSql() will submit a Flink job immediately, and return a TableResult instance which associates the submitted job.

`execute_sql()`
`TableEnvironment`
`executeSql()`
`TableResult`

The following examples show how to run a single DELETE statement in TableEnvironment.

`TableEnvironment`

DELETE statements can be executed in SQL CLI.


The following examples show how to run a DELETE statement in SQL CLI.


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
// delete by filter
tEnv.executeSql("DELETE FROM Orders WHERE `user` = 'Lili'").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// +--------------------------------+--------------------------------+-------------+
// |                           user |                        product |      amount |
// +--------------------------------+--------------------------------+-------------+
// |                        Jessica |                         Banana |           2 |
// |                       Mr.White |                        Chicken |           3 |
// +--------------------------------+--------------------------------+-------------+
// 2 rows in set
// delete entire table
tEnv.executeSql("DELETE FROM Orders").await();
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
// delete by filter
tEnv.executeSql("DELETE FROM Orders WHERE `user` = 'Lili'").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// +--------------------------------+--------------------------------+-------------+
// |                           user |                        product |      amount |
// +--------------------------------+--------------------------------+-------------+
// |                        Jessica |                         Banana |           2 |
// |                       Mr.White |                        Chicken |           3 |
// +--------------------------------+--------------------------------+-------------+
// 2 rows in set
// delete entire table
tEnv.executeSql("DELETE FROM Orders").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// Empty set
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
val settings = EnvironmentSettings.newInstance().inBatchMode().build()
val tEnv = StreamTableEnvironment.create(env, settings)

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
// delete by filter
tEnv.executeSql("DELETE FROM Orders WHERE `user` = 'Lili'").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// +--------------------------------+--------------------------------+-------------+
// |                           user |                        product |      amount |
// +--------------------------------+--------------------------------+-------------+
// |                        Jessica |                         Banana |           2 |
// |                       Mr.White |                        Chicken |           3 |
// +--------------------------------+--------------------------------+-------------+
// 2 rows in set
// delete entire table
tEnv.executeSql("DELETE FROM Orders").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// Empty set

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
val settings = EnvironmentSettings.newInstance().inBatchMode().build()
val tEnv = StreamTableEnvironment.create(env, settings)

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
// delete by filter
tEnv.executeSql("DELETE FROM Orders WHERE `user` = 'Lili'").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// +--------------------------------+--------------------------------+-------------+
// |                           user |                        product |      amount |
// +--------------------------------+--------------------------------+-------------+
// |                        Jessica |                         Banana |           2 |
// |                       Mr.White |                        Chicken |           3 |
// +--------------------------------+--------------------------------+-------------+
// 2 rows in set
// delete entire table
tEnv.executeSql("DELETE FROM Orders").await();
tEnv.executeSql("SELECT * FROM Orders").print();
// Empty set
`

```
env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

# register a table named "Orders"
table_env.executeSql("CREATE TABLE Orders (`user` STRING, product STRING, amount INT) WITH (...)");
# insert values
table_env.executeSql("INSERT INTO Orders VALUES ('Lili', 'Apple', 1), ('Jessica', 'Banana', 2), ('Mr.White', 'Chicken', 3)").wait();
table_env.executeSql("SELECT * FROM Orders").print();
# +--------------------------------+--------------------------------+-------------+
# |                           user |                        product |      amount |
# +--------------------------------+--------------------------------+-------------+
# |                           Lili |                          Apple |           1 |
# |                        Jessica |                         Banana |           2 |
# |                       Mr.White |                        Chicken |           3 |
# +--------------------------------+--------------------------------+-------------+
# 3 rows in set
# delete by filter
table_env.executeSql("DELETE FROM Orders WHERE `user` = 'Lili'").wait();
table_env.executeSql("SELECT * FROM Orders").print();
# +--------------------------------+--------------------------------+-------------+
# |                           user |                        product |      amount |
# +--------------------------------+--------------------------------+-------------+
# |                        Jessica |                         Banana |           2 |
# |                       Mr.White |                        Chicken |           3 |
# +--------------------------------+--------------------------------+-------------+
# 2 rows in set
# delete entire table
table_env.executeSql("DELETE FROM Orders").wait();
table_env.executeSql("SELECT * FROM Orders").print();
# Empty set

```

`env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

# register a table named "Orders"
table_env.executeSql("CREATE TABLE Orders (`user` STRING, product STRING, amount INT) WITH (...)");
# insert values
table_env.executeSql("INSERT INTO Orders VALUES ('Lili', 'Apple', 1), ('Jessica', 'Banana', 2), ('Mr.White', 'Chicken', 3)").wait();
table_env.executeSql("SELECT * FROM Orders").print();
# +--------------------------------+--------------------------------+-------------+
# |                           user |                        product |      amount |
# +--------------------------------+--------------------------------+-------------+
# |                           Lili |                          Apple |           1 |
# |                        Jessica |                         Banana |           2 |
# |                       Mr.White |                        Chicken |           3 |
# +--------------------------------+--------------------------------+-------------+
# 3 rows in set
# delete by filter
table_env.executeSql("DELETE FROM Orders WHERE `user` = 'Lili'").wait();
table_env.executeSql("SELECT * FROM Orders").print();
# +--------------------------------+--------------------------------+-------------+
# |                           user |                        product |      amount |
# +--------------------------------+--------------------------------+-------------+
# |                        Jessica |                         Banana |           2 |
# |                       Mr.White |                        Chicken |           3 |
# +--------------------------------+--------------------------------+-------------+
# 2 rows in set
# delete entire table
table_env.executeSql("DELETE FROM Orders").wait();
table_env.executeSql("SELECT * FROM Orders").print();
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

Flink SQL> DELETE FROM Orders WHERE `user` = 'Lili';

    user                         product      amount
 Jessica                          Banana           2
Mr.White                         Chicken           3

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

Flink SQL> DELETE FROM Orders WHERE `user` = 'Lili';

    user                         product      amount
 Jessica                          Banana           2
Mr.White                         Chicken           3
`

 Back to top


## DELETE ROWS#


```
DELETE FROM [catalog_name.][db_name.]table_name [ WHERE condition ]

```

`DELETE FROM [catalog_name.][db_name.]table_name [ WHERE condition ]
`