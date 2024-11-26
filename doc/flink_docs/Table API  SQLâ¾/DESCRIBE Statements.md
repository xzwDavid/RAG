# DESCRIBE Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# DESCRIBE Statements#


DESCRIBE statements are used to describe the schema of a table or a view, or the metadata of a catalog or a function, or the specified job in the Flink cluster.


## Run a DESCRIBE statement#


DESCRIBE statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns objects for a successful DESCRIBE operation, otherwise will throw an exception.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run a DESCRIBE statement in TableEnvironment.

`TableEnvironment`

DESCRIBE statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns objects for a successful DESCRIBE operation, otherwise will throw an exception.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run a DESCRIBE statement in TableEnvironment.

`TableEnvironment`

DESCRIBE statements can be executed with the execute_sql() method of the TableEnvironment. The execute_sql() method returns objects for a successful DESCRIBE operation, otherwise will throw an exception.

`execute_sql()`
`TableEnvironment`
`execute_sql()`

The following examples show how to run a DESCRIBE statement in TableEnvironment.

`TableEnvironment`

DESCRIBE statements can be executed in SQL CLI.


The following examples show how to run a DESCRIBE statement in SQL CLI.


```
TableEnvironment tableEnv = TableEnvironment.create(...);

// register a table named "Orders"
tableEnv.executeSql(
        "CREATE TABLE Orders (" +
        " `user` BIGINT NOT NULl comment 'this is primary key'," +
        " product VARCHAR(32)," +
        " amount INT," +
        " ts TIMESTAMP(3) comment 'notice: watermark'," +
        " ptime AS PROCTIME() comment 'this is a computed column'," +
        " PRIMARY KEY(`user`) NOT ENFORCED," +
        " WATERMARK FOR ts AS ts - INTERVAL '1' SECONDS" +
        ") with (...)");

// print the schema
tableEnv.executeSql("DESCRIBE Orders").print();

// print the schema
tableEnv.executeSql("DESC Orders").print();

// register a catalog named "cat2"
tableEnv.executeSql("CREATE CATALOG cat2 WITH ('type'='generic_in_memory', 'default-database'='db')");

// print the metadata
tableEnv.executeSql("DESCRIBE CATALOG cat2").print();

// print the complete metadata
tableEnv.executeSql("DESC CATALOG EXTENDED cat2").print();

// register a function named "MySum"
tableEnv.executeSql("CREATE FUNCTION MySum as 'org.example.SumScalarFunction' USING JAR 'file://home/users/mysum-udf.jar';").print();

// print the metadata
tableEnv.executeSql("DESCRIBE FUNCTION MySum").print();

// print the complete metadata
tableEnv.executeSql("DESC FUNCTION EXTENDED MySum").print();

```

`TableEnvironment tableEnv = TableEnvironment.create(...);

// register a table named "Orders"
tableEnv.executeSql(
        "CREATE TABLE Orders (" +
        " `user` BIGINT NOT NULl comment 'this is primary key'," +
        " product VARCHAR(32)," +
        " amount INT," +
        " ts TIMESTAMP(3) comment 'notice: watermark'," +
        " ptime AS PROCTIME() comment 'this is a computed column'," +
        " PRIMARY KEY(`user`) NOT ENFORCED," +
        " WATERMARK FOR ts AS ts - INTERVAL '1' SECONDS" +
        ") with (...)");

// print the schema
tableEnv.executeSql("DESCRIBE Orders").print();

// print the schema
tableEnv.executeSql("DESC Orders").print();

// register a catalog named "cat2"
tableEnv.executeSql("CREATE CATALOG cat2 WITH ('type'='generic_in_memory', 'default-database'='db')");

// print the metadata
tableEnv.executeSql("DESCRIBE CATALOG cat2").print();

// print the complete metadata
tableEnv.executeSql("DESC CATALOG EXTENDED cat2").print();

// register a function named "MySum"
tableEnv.executeSql("CREATE FUNCTION MySum as 'org.example.SumScalarFunction' USING JAR 'file://home/users/mysum-udf.jar';").print();

// print the metadata
tableEnv.executeSql("DESCRIBE FUNCTION MySum").print();

// print the complete metadata
tableEnv.executeSql("DESC FUNCTION EXTENDED MySum").print();
`

```
val tableEnv = TableEnvironment.create(...)

// register a table named "Orders"
 tableEnv.executeSql(
        "CREATE TABLE Orders (" +
        " `user` BIGINT NOT NULl comment 'this is primary key'," +
        " product VARCHAR(32)," +
        " amount INT," +
        " ts TIMESTAMP(3) comment 'notice: watermark'," +
        " ptime AS PROCTIME() comment 'this is a computed column'," +
        " PRIMARY KEY(`user`) NOT ENFORCED," +
        " WATERMARK FOR ts AS ts - INTERVAL '1' SECONDS" +
        ") with (...)")

// print the schema
tableEnv.executeSql("DESCRIBE Orders").print()

// print the schema
tableEnv.executeSql("DESC Orders").print()

// register a catalog named "cat2"
tableEnv.executeSql("CREATE CATALOG cat2 WITH ('type'='generic_in_memory', 'default-database'='db')")

// print the metadata
tableEnv.executeSql("DESCRIBE CATALOG cat2").print()

// print the complete metadata
tableEnv.executeSql("DESC CATALOG EXTENDED cat2").print()


// register a function named "MySum"
tableEnv.executeSql("CREATE FUNCTION MySum as 'org.example.SumScalarFunction' USING JAR 'file://home/users/mysum-udf.jar';").print()

// print the metadata
tableEnv.executeSql("DESCRIBE FUNCTION MySum").print()

// print the complete metadata
tableEnv.executeSql("DESC FUNCTION EXTENDED MySum").print()

```

`val tableEnv = TableEnvironment.create(...)

// register a table named "Orders"
 tableEnv.executeSql(
        "CREATE TABLE Orders (" +
        " `user` BIGINT NOT NULl comment 'this is primary key'," +
        " product VARCHAR(32)," +
        " amount INT," +
        " ts TIMESTAMP(3) comment 'notice: watermark'," +
        " ptime AS PROCTIME() comment 'this is a computed column'," +
        " PRIMARY KEY(`user`) NOT ENFORCED," +
        " WATERMARK FOR ts AS ts - INTERVAL '1' SECONDS" +
        ") with (...)")

// print the schema
tableEnv.executeSql("DESCRIBE Orders").print()

// print the schema
tableEnv.executeSql("DESC Orders").print()

// register a catalog named "cat2"
tableEnv.executeSql("CREATE CATALOG cat2 WITH ('type'='generic_in_memory', 'default-database'='db')")

// print the metadata
tableEnv.executeSql("DESCRIBE CATALOG cat2").print()

// print the complete metadata
tableEnv.executeSql("DESC CATALOG EXTENDED cat2").print()


// register a function named "MySum"
tableEnv.executeSql("CREATE FUNCTION MySum as 'org.example.SumScalarFunction' USING JAR 'file://home/users/mysum-udf.jar';").print()

// print the metadata
tableEnv.executeSql("DESCRIBE FUNCTION MySum").print()

// print the complete metadata
tableEnv.executeSql("DESC FUNCTION EXTENDED MySum").print()
`

```
table_env = TableEnvironment.create(...)

# register a table named "Orders"
table_env.execute_sql( \
        "CREATE TABLE Orders (" 
        " `user` BIGINT NOT NULl comment 'this is primary key'," 
        " product VARCHAR(32),"
        " amount INT,"
        " ts TIMESTAMP(3) comment 'notice: watermark',"
        " ptime AS PROCTIME() comment 'this is a computed column',"
        " PRIMARY KEY(`user`) NOT ENFORCED,"
        " WATERMARK FOR ts AS ts - INTERVAL '1' SECONDS"
        ") with (...)");

# print the schema
table_env.execute_sql("DESCRIBE Orders").print()

# print the schema
table_env.execute_sql("DESC Orders").print()

# register a catalog named "cat2"
table_env.execute_sql("CREATE CATALOG cat2 WITH ('type'='generic_in_memory', 'default-database'='db')")

# print the metadata
table_env.execute_sql("DESCRIBE CATALOG cat2").print()

# print the complete metadata
table_env.execute_sql("DESC CATALOG EXTENDED cat2").print()


// register a function named "MySum"
table_env.execute_sql("CREATE FUNCTION MySum as 'org.example.SumScalarFunction' USING JAR 'file://home/users/mysum-udf.jar';").print()

// print the metadata
table_env.execute_sql("DESCRIBE FUNCTION MySum").print()

// print the complete metadata
table_env.execute_sql("DESC FUNCTION EXTENDED MySum").print()

```

`table_env = TableEnvironment.create(...)

# register a table named "Orders"
table_env.execute_sql( \
        "CREATE TABLE Orders (" 
        " `user` BIGINT NOT NULl comment 'this is primary key'," 
        " product VARCHAR(32),"
        " amount INT,"
        " ts TIMESTAMP(3) comment 'notice: watermark',"
        " ptime AS PROCTIME() comment 'this is a computed column',"
        " PRIMARY KEY(`user`) NOT ENFORCED,"
        " WATERMARK FOR ts AS ts - INTERVAL '1' SECONDS"
        ") with (...)");

# print the schema
table_env.execute_sql("DESCRIBE Orders").print()

# print the schema
table_env.execute_sql("DESC Orders").print()

# register a catalog named "cat2"
table_env.execute_sql("CREATE CATALOG cat2 WITH ('type'='generic_in_memory', 'default-database'='db')")

# print the metadata
table_env.execute_sql("DESCRIBE CATALOG cat2").print()

# print the complete metadata
table_env.execute_sql("DESC CATALOG EXTENDED cat2").print()


// register a function named "MySum"
table_env.execute_sql("CREATE FUNCTION MySum as 'org.example.SumScalarFunction' USING JAR 'file://home/users/mysum-udf.jar';").print()

// print the metadata
table_env.execute_sql("DESCRIBE FUNCTION MySum").print()

// print the complete metadata
table_env.execute_sql("DESC FUNCTION EXTENDED MySum").print()
`

```
Flink SQL> CREATE TABLE Orders (
>  `user` BIGINT NOT NULl comment 'this is primary key',
>  product VARCHAR(32),
>  amount INT,
>  ts TIMESTAMP(3) comment 'notice: watermark',
>  ptime AS PROCTIME() comment 'this is a computed column',
>  PRIMARY KEY(`user`) NOT ENFORCED,
>  WATERMARK FOR ts AS ts - INTERVAL '1' SECONDS
> ) with (
>  ...
> );
[INFO] Table has been created.

Flink SQL> DESCRIBE Orders;

Flink SQL> DESC Orders;

Flink SQL> CREATE CATALOG cat2 WITH ('type'='generic_in_memory', 'default-database'='db');
[INFO] Execute statement succeeded.

Flink SQL> DESCRIBE CATALOG cat2;

Flink SQL> DESC CATALOG EXTENDED cat2;

Flink SQL> CREATE FUNCTION MySum as 'org.example.SumScalarFunction' USING JAR 'file://home/users/mysum-udf.jar';

Flink SQL> DESCRIBE FUNCTION MySum;

Flink SQL> DESC FUNCTION EXTENDED MySum;
      
Flink SQL> DESCRIBE JOB '228d70913eab60dda85c5e7f78b5782c';
      
Flink SQL> DESC JOB '228d70913eab60dda85c5e7f78b5782c';

```

`Flink SQL> CREATE TABLE Orders (
>  `user` BIGINT NOT NULl comment 'this is primary key',
>  product VARCHAR(32),
>  amount INT,
>  ts TIMESTAMP(3) comment 'notice: watermark',
>  ptime AS PROCTIME() comment 'this is a computed column',
>  PRIMARY KEY(`user`) NOT ENFORCED,
>  WATERMARK FOR ts AS ts - INTERVAL '1' SECONDS
> ) with (
>  ...
> );
[INFO] Table has been created.

Flink SQL> DESCRIBE Orders;

Flink SQL> DESC Orders;

Flink SQL> CREATE CATALOG cat2 WITH ('type'='generic_in_memory', 'default-database'='db');
[INFO] Execute statement succeeded.

Flink SQL> DESCRIBE CATALOG cat2;

Flink SQL> DESC CATALOG EXTENDED cat2;

Flink SQL> CREATE FUNCTION MySum as 'org.example.SumScalarFunction' USING JAR 'file://home/users/mysum-udf.jar';

Flink SQL> DESCRIBE FUNCTION MySum;

Flink SQL> DESC FUNCTION EXTENDED MySum;
      
Flink SQL> DESCRIBE JOB '228d70913eab60dda85c5e7f78b5782c';
      
Flink SQL> DESC JOB '228d70913eab60dda85c5e7f78b5782c';
`

The result of the above example is:






Java
# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set

Scala
# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set

Python
# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set

SQL CLI
# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set

# DESCRIBE JOB '228d70913eab60dda85c5e7f78b5782c'
+----------------------------------+----------+---------+-------------------------+
|                           job id | job name |  status |              start time |
+----------------------------------+----------+---------+-------------------------+
| 228d70913eab60dda85c5e7f78b5782c |    myjob | RUNNING | 2023-02-11T05:03:51.523 |
+----------------------------------+----------+---------+-------------------------+
1 row in set




```
# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set

```

`# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set
`

```
# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set

```

`# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set
`

```
# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set

```

`# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set
`

```
# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set

# DESCRIBE JOB '228d70913eab60dda85c5e7f78b5782c'
+----------------------------------+----------+---------+-------------------------+
|                           job id | job name |  status |              start time |
+----------------------------------+----------+---------+-------------------------+
| 228d70913eab60dda85c5e7f78b5782c |    myjob | RUNNING | 2023-02-11T05:03:51.523 |
+----------------------------------+----------+---------+-------------------------+
1 row in set

```

`# DESCRIBE TABLE Orders
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    name |                        type |  null |       key |        extras |                  watermark |                   comment |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
|    user |                      BIGINT | FALSE | PRI(user) |               |                            |       this is primary key |
| product |                 VARCHAR(32) |  TRUE |           |               |                            |                           |
|  amount |                         INT |  TRUE |           |               |                            |                           |
|      ts |      TIMESTAMP(3) *ROWTIME* |  TRUE |           |               | `ts` - INTERVAL '1' SECOND |         notice: watermark |
|   ptime | TIMESTAMP_LTZ(3) *PROCTIME* | FALSE |           | AS PROCTIME() |                            | this is a computed column |
+---------+-----------------------------+-------+-----------+---------------+----------------------------+---------------------------+
5 rows in set

# DESCRIBE CATALOG cat2
+-----------+-------------------+
| info name |        info value |
+-----------+-------------------+
|      name |              cat2 |
|      type | generic_in_memory |
|   comment |                   |
+-----------+-------------------+
3 rows in set

# DESCRIBE CATALOG EXTENDED cat2
+-------------------------+-------------------+
|               info name |        info value |
+-------------------------+-------------------+
|                    name |              cat2 |
|                    type | generic_in_memory |
|                 comment |                   |
| option:default-database |                db |
+-------------------------+-------------------+
4 rows in set

# DESCRIBE FUNCTION MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
+-------------------+---------------------------------------------------------------------+
5 rows in set

# DESCRIBE FUNCTION EXTENDED MySum
+-------------------+---------------------------------------------------------------------+
|         info name |                                                          info value |
+-------------------+---------------------------------------------------------------------+
|   system function |                                                               false |
|         temporary |                                                               false |
|        class name |                                       org.example.SumScalarFunction |
| function language |                                                                JAVA |
|     resource uris | ResourceUri{resourceType=JAR, uri='file:/home/users/mysum-udf.jar'} |
|              kind |                                                              SCALAR |
|      requirements |                                                                  [] |
|     deterministic |                                                                true |
|  constant folding |                                                                true |
|         signature |                       MySum(<INTEGER NOT NULL>, <INTEGER NOT NULL>) |
+-------------------+---------------------------------------------------------------------+
10 rows in set

# DESCRIBE JOB '228d70913eab60dda85c5e7f78b5782c'
+----------------------------------+----------+---------+-------------------------+
|                           job id | job name |  status |              start time |
+----------------------------------+----------+---------+-------------------------+
| 228d70913eab60dda85c5e7f78b5782c |    myjob | RUNNING | 2023-02-11T05:03:51.523 |
+----------------------------------+----------+---------+-------------------------+
1 row in set
`

 Back to top


## Syntax#


### DESCRIBE TABLE#


```
{ DESCRIBE | DESC } [catalog_name.][db_name.]table_name

```

`{ DESCRIBE | DESC } [catalog_name.][db_name.]table_name
`

### DESCRIBE CATALOG#


```
{ DESCRIBE | DESC } CATALOG [EXTENDED] catalog_name

```

`{ DESCRIBE | DESC } CATALOG [EXTENDED] catalog_name
`

### DESCRIBE FUNCTION#


```
{ DESCRIBE | DESC } FUNCTION [EXTENDED] [catalog_name.][db_name.]function_name

```

`{ DESCRIBE | DESC } FUNCTION [EXTENDED] [catalog_name.][db_name.]function_name
`

### DESCRIBE JOB#


```
{ DESCRIBE | DESC } JOB '<job_id>'

```

`{ DESCRIBE | DESC } JOB '<job_id>'
`

Attention DESCRIBE JOB statements only work in SQL CLI or SQL Gateway.
