# JDBC


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# JDBC SQL Connector#



Scan Source: Bounded
Lookup Source: Sync Mode
Sink: Batch
Sink: Streaming Append & Upsert Mode


The JDBC connector allows for reading data from and writing data into any relational databases with a JDBC driver. This document describes how to setup the JDBC connector to run SQL queries against relational databases.


The JDBC sink operate in upsert mode for exchange UPDATE/DELETE messages with the external system if a primary key is defined on the DDL, otherwise, it operates in append mode and doesn’t support to consume UPDATE/DELETE messages.


## Dependencies#


Only available for stable versions.


The JDBC connector is not part of the binary distribution.
See how to link with it for cluster execution here.


A driver dependency is also required to connect to a specified database. Here are drivers currently supported:

`mysql`
`mysql-connector-java`
`com.oracle.database.jdbc`
`ojdbc8`
`org.postgresql`
`postgresql`
`org.apache.derby`
`derby`
`com.microsoft.sqlserver`
`mssql-jdbc`

JDBC connector and drivers are not part of Flink’s binary distribution. See how to link with them for cluster execution here.


## How to create a JDBC table#


The JDBC table can be defined as following:


```
-- register a MySQL table 'users' in Flink SQL
CREATE TABLE MyUserTable (
  id BIGINT,
  name STRING,
  age INT,
  status BOOLEAN,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
   'connector' = 'jdbc',
   'url' = 'jdbc:mysql://localhost:3306/mydatabase',
   'table-name' = 'users'
);

-- write data into the JDBC table from the other table "T"
INSERT INTO MyUserTable
SELECT id, name, age, status FROM T;

-- scan data from the JDBC table
SELECT id, name, age, status FROM MyUserTable;

-- temporal join the JDBC table as a dimension table
SELECT * FROM myTopic
LEFT JOIN MyUserTable FOR SYSTEM_TIME AS OF myTopic.proctime
ON myTopic.key = MyUserTable.id;

```

`-- register a MySQL table 'users' in Flink SQL
CREATE TABLE MyUserTable (
  id BIGINT,
  name STRING,
  age INT,
  status BOOLEAN,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
   'connector' = 'jdbc',
   'url' = 'jdbc:mysql://localhost:3306/mydatabase',
   'table-name' = 'users'
);

-- write data into the JDBC table from the other table "T"
INSERT INTO MyUserTable
SELECT id, name, age, status FROM T;

-- scan data from the JDBC table
SELECT id, name, age, status FROM MyUserTable;

-- temporal join the JDBC table as a dimension table
SELECT * FROM myTopic
LEFT JOIN MyUserTable FOR SYSTEM_TIME AS OF myTopic.proctime
ON myTopic.key = MyUserTable.id;
`

## Connector Options#


##### connector

`'jdbc'`

##### url


##### table-name


##### driver


##### username

`'username'`
`'password'`

##### password


##### connection.max-retry-timeout


##### scan.partition.column


##### scan.partition.num


##### scan.partition.lower-bound


##### scan.partition.upper-bound


##### scan.fetch-size


##### scan.auto-commit


##### lookup.cache


Enum


##### lookup.partial-cache.max-rows


##### lookup.partial-cache.expire-after-write


##### lookup.partial-cache.expire-after-access


##### lookup.partial-cache.cache-missing-key


##### lookup.max-retries


##### sink.buffer-flush.max-rows


##### sink.buffer-flush.interval

`'0'`
`'sink.buffer-flush.max-rows'`
`'0'`

##### sink.max-retries


##### sink.parallelism


### Deprecated Options#


These deprecated options has been replaced by new options listed above and will be removed eventually. Please consider using new options first.


##### lookup.cache.max-rows


##### lookup.cache.ttl


##### lookup.cache.caching-missing-key


## Features#


### Key handling#


Flink uses the primary key that was defined in DDL when writing data to external databases. The connector operates in upsert mode if the primary key was defined, otherwise, the connector operates in append mode.


In upsert mode, Flink will insert a new row or update the existing row according to the primary key, Flink can ensure the idempotence in this way. To guarantee the output result is as expected, it’s recommended to define primary key for the table and make sure the primary key is one of the unique key sets or primary key of the underlying database table. In append mode, Flink will interpret all records as INSERT messages, the INSERT operation may fail if a primary key or unique constraint violation happens in the underlying database.


See CREATE TABLE DDL for more details about PRIMARY KEY syntax.


### Partitioned Scan#


To accelerate reading data in parallel Source task instances, Flink provides partitioned scan feature for JDBC table.

`Source`

All the following scan partition options must all be specified if any of them is specified. They describe how to partition the table when reading in parallel from multiple tasks.
The scan.partition.column must be a numeric, date, or timestamp column from the table in question. Notice that scan.partition.lower-bound and scan.partition.upper-bound are used to decide the partition stride and filter the rows in table. If it is a batch job, it also doable to get the max and min value first before submitting the flink job.

`scan.partition.column`
`scan.partition.lower-bound`
`scan.partition.upper-bound`
* scan.partition.column: The column name used for partitioning the input.
* scan.partition.num: The number of partitions.
* scan.partition.lower-bound: The smallest value of the first partition.
* scan.partition.upper-bound: The largest value of the last partition.
`scan.partition.column`
`scan.partition.num`
`scan.partition.lower-bound`
`scan.partition.upper-bound`

### Lookup Cache#


JDBC connector can be used in temporal join as a lookup source (aka. dimension table). Currently, only sync lookup mode is supported.


By default, lookup cache is not enabled. You can enable it by setting lookup.cache to PARTIAL.

`lookup.cache`
`PARTIAL`

The lookup cache is used to improve performance of temporal join the JDBC connector. By default, lookup cache is not enabled, so all the requests are sent to external database.
When lookup cache is enabled, each process (i.e. TaskManager) will hold a cache. Flink will lookup the cache first, and only send requests to external database when cache missing, and update cache with the rows returned.
The oldest rows in cache will be expired when the cache hit to the max cached rows lookup.partial-cache.max-rows or when the row exceeds the max time to live specified by lookup.partial-cache.expire-after-write or lookup.partial-cache.expire-after-access.
The cached rows might not be the latest, users can tune expiration options to a smaller value to have a better fresh data, but this may increase the number of requests send to database. So this is a balance between throughput and correctness.

`lookup.partial-cache.max-rows`
`lookup.partial-cache.expire-after-write`
`lookup.partial-cache.expire-after-access`

By default, flink will cache the empty query result for a Primary key, you can toggle the behaviour by setting lookup.partial-cache.cache-missing-key to false.

`lookup.partial-cache.cache-missing-key`

### Idempotent Writes#


JDBC sink will use upsert semantics rather than plain INSERT statements if primary key is defined in DDL. Upsert semantics refer to atomically adding a new row or updating the existing row if there is a unique constraint violation in the underlying database, which provides idempotence.


If there are failures, the Flink job will recover and re-process from last successful checkpoint, which can lead to re-processing messages during recovery. The upsert mode is highly recommended as it helps avoid constraint violations or duplicate data if records need to be re-processed.


Aside from failure recovery, the source topic may also naturally contain multiple records over time with the same primary key, making upserts desirable.


As there is no standard syntax for upsert, the following table describes the database-specific DML that is used.


## JDBC Catalog#


The JdbcCatalog enables users to connect Flink to relational databases over JDBC protocol.

`JdbcCatalog`

Currently, there are two JDBC catalog implementations, Postgres Catalog and MySQL Catalog. They support the following catalog methods. Other methods are currently not supported.


```
// The supported methods by Postgres & MySQL Catalog.
databaseExists(String databaseName);
listDatabases();
getDatabase(String databaseName);
listTables(String databaseName);
getTable(ObjectPath tablePath);
tableExists(ObjectPath tablePath);

```

`// The supported methods by Postgres & MySQL Catalog.
databaseExists(String databaseName);
listDatabases();
getDatabase(String databaseName);
listTables(String databaseName);
getTable(ObjectPath tablePath);
tableExists(ObjectPath tablePath);
`

Other Catalog methods are currently not supported.

`Catalog`

### Usage of JDBC Catalog#


The section mainly describes how to create and use a Postgres Catalog or MySQL Catalog.
Please refer to Dependencies section for how to setup a JDBC connector and the corresponding driver.


The JDBC catalog supports the following options:

* name: required, name of the catalog.
* default-database: required, default database to connect to.
* username: required, username of Postgres/MySQL account.
* password: required, password of the account.
* base-url: required (should not contain the database name)

for Postgres Catalog this should be "jdbc:postgresql://<ip>:<port>"
for MySQL Catalog this should be "jdbc:mysql://<ip>:<port>"


`name`
`default-database`
`username`
`password`
`base-url`
* for Postgres Catalog this should be "jdbc:postgresql://<ip>:<port>"
* for MySQL Catalog this should be "jdbc:mysql://<ip>:<port>"
`"jdbc:postgresql://<ip>:<port>"`
`"jdbc:mysql://<ip>:<port>"`

```
CREATE CATALOG my_catalog WITH(
    'type' = 'jdbc',
    'default-database' = '...',
    'username' = '...',
    'password' = '...',
    'base-url' = '...'
);

USE CATALOG my_catalog;

```

`CREATE CATALOG my_catalog WITH(
    'type' = 'jdbc',
    'default-database' = '...',
    'username' = '...',
    'password' = '...',
    'base-url' = '...'
);

USE CATALOG my_catalog;
`

```

EnvironmentSettings settings = EnvironmentSettings.inStreamingMode();
TableEnvironment tableEnv = TableEnvironment.create(settings);

String name            = "my_catalog";
String defaultDatabase = "mydb";
String username        = "...";
String password        = "...";
String baseUrl         = "..."

JdbcCatalog catalog = new JdbcCatalog(name, defaultDatabase, username, password, baseUrl);
tableEnv.registerCatalog("my_catalog", catalog);

// set the JdbcCatalog as the current catalog of the session
tableEnv.useCatalog("my_catalog");

```

`
EnvironmentSettings settings = EnvironmentSettings.inStreamingMode();
TableEnvironment tableEnv = TableEnvironment.create(settings);

String name            = "my_catalog";
String defaultDatabase = "mydb";
String username        = "...";
String password        = "...";
String baseUrl         = "..."

JdbcCatalog catalog = new JdbcCatalog(name, defaultDatabase, username, password, baseUrl);
tableEnv.registerCatalog("my_catalog", catalog);

// set the JdbcCatalog as the current catalog of the session
tableEnv.useCatalog("my_catalog");
`

```

val settings = EnvironmentSettings.inStreamingMode()
val tableEnv = TableEnvironment.create(settings)

val name            = "my_catalog"
val defaultDatabase = "mydb"
val username        = "..."
val password        = "..."
val baseUrl         = "..."

val catalog = new JdbcCatalog(name, defaultDatabase, username, password, baseUrl)
tableEnv.registerCatalog("my_catalog", catalog)

// set the JdbcCatalog as the current catalog of the session
tableEnv.useCatalog("my_catalog")

```

`
val settings = EnvironmentSettings.inStreamingMode()
val tableEnv = TableEnvironment.create(settings)

val name            = "my_catalog"
val defaultDatabase = "mydb"
val username        = "..."
val password        = "..."
val baseUrl         = "..."

val catalog = new JdbcCatalog(name, defaultDatabase, username, password, baseUrl)
tableEnv.registerCatalog("my_catalog", catalog)

// set the JdbcCatalog as the current catalog of the session
tableEnv.useCatalog("my_catalog")
`

```
from pyflink.table.catalog import JdbcCatalog

environment_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(environment_settings)

name = "my_catalog"
default_database = "mydb"
username = "..."
password = "..."
base_url = "..."

catalog = JdbcCatalog(name, default_database, username, password, base_url)
t_env.register_catalog("my_catalog", catalog)

# set the JdbcCatalog as the current catalog of the session
t_env.use_catalog("my_catalog")

```

`from pyflink.table.catalog import JdbcCatalog

environment_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(environment_settings)

name = "my_catalog"
default_database = "mydb"
username = "..."
password = "..."
base_url = "..."

catalog = JdbcCatalog(name, default_database, username, password, base_url)
t_env.register_catalog("my_catalog", catalog)

# set the JdbcCatalog as the current catalog of the session
t_env.use_catalog("my_catalog")
`

```

execution:
    ...
    current-catalog: my_catalog  # set the target JdbcCatalog as the current catalog of the session
    current-database: mydb

catalogs:
   - name: my_catalog
     type: jdbc
     default-database: mydb
     username: ...
     password: ...
     base-url: ...

```

`
execution:
    ...
    current-catalog: my_catalog  # set the target JdbcCatalog as the current catalog of the session
    current-database: mydb

catalogs:
   - name: my_catalog
     type: jdbc
     default-database: mydb
     username: ...
     password: ...
     base-url: ...
`

### JDBC Catalog for PostgreSQL#


#### PostgreSQL Metaspace Mapping#


PostgreSQL has an additional namespace as schema besides database. A Postgres instance can have multiple databases, each database can have multiple schemas with a default one named “public”, each schema can have multiple tables.
In Flink, when querying tables registered by Postgres catalog, users can use either schema_name.table_name or just table_name. The schema_name is optional and defaults to “public”.

`schema`
`schema_name.table_name`
`table_name`
`schema_name`

Therefore, the metaspace mapping between Flink Catalog and Postgres is as following:


The full path of Postgres table in Flink should be "<catalog>.<db>.`<schema.table>`" if schema is specified, note the <schema.table> should be escaped.

`"<catalog>.<db>.`<schema.table>`"`
`<schema.table>`

Here are some examples to access Postgres tables:


```
-- scan table 'test_table' of 'public' schema (i.e. the default schema), the schema name can be omitted
SELECT * FROM mypg.mydb.test_table;
SELECT * FROM mydb.test_table;
SELECT * FROM test_table;

-- scan table 'test_table2' of 'custom_schema' schema,
-- the custom schema can not be omitted and must be escaped with table.
SELECT * FROM mypg.mydb.`custom_schema.test_table2`
SELECT * FROM mydb.`custom_schema.test_table2`;
SELECT * FROM `custom_schema.test_table2`;

```

`-- scan table 'test_table' of 'public' schema (i.e. the default schema), the schema name can be omitted
SELECT * FROM mypg.mydb.test_table;
SELECT * FROM mydb.test_table;
SELECT * FROM test_table;

-- scan table 'test_table2' of 'custom_schema' schema,
-- the custom schema can not be omitted and must be escaped with table.
SELECT * FROM mypg.mydb.`custom_schema.test_table2`
SELECT * FROM mydb.`custom_schema.test_table2`;
SELECT * FROM `custom_schema.test_table2`;
`

### JDBC Catalog for MySQL#


#### MySQL Metaspace Mapping#


The databases in a MySQL instance are at the same mapping level as the databases under the catalog registered with MySQL Catalog. A MySQL instance can have multiple databases, each database can have multiple tables.
In Flink, when querying tables registered by MySQL catalog, users can use either database.table_name or just table_name. The default value is the default database specified when MySQL Catalog was created.

`database.table_name`
`table_name`

Therefore, the metaspace mapping between Flink Catalog and MySQL Catalog is as following:


The full path of MySQL table in Flink should be "`<catalog>`.`<db>`.`<table>`".

`"`<catalog>`.`<db>`.`<table>`"`

Here are some examples to access MySQL tables:


```
-- scan table 'test_table', the default database is 'mydb'.
SELECT * FROM mysql_catalog.mydb.test_table;
SELECT * FROM mydb.test_table;
SELECT * FROM test_table;

-- scan table 'test_table' with the given database.
SELECT * FROM mysql_catalog.given_database.test_table2;
SELECT * FROM given_database.test_table2;

```

`-- scan table 'test_table', the default database is 'mydb'.
SELECT * FROM mysql_catalog.mydb.test_table;
SELECT * FROM mydb.test_table;
SELECT * FROM test_table;

-- scan table 'test_table' with the given database.
SELECT * FROM mysql_catalog.given_database.test_table2;
SELECT * FROM given_database.test_table2;
`

## Data Type Mapping#


Flink supports connect to several databases which uses dialect like MySQL, Oracle, PostgreSQL, Derby. The Derby dialect usually used for testing purpose. The field data type mappings from relational databases data types to Flink SQL data types are listed in the following table, the mapping table can help define JDBC table in Flink easily.

`TINYINT`
`TINYINT`
`TINYINT`
`SMALLINT`
`TINYINT UNSIGNED`
`SMALLINT`
`INT2`
`SMALLSERIAL`
`SERIAL2`
`SMALLINT`
`SMALLINT`
`INT`
`MEDIUMINT`
`SMALLINT UNSIGNED`
`INTEGER`
`SERIAL`
`INT`
`INT`
`BIGINT`
`INT UNSIGNED`
`BIGINT`
`BIGSERIAL`
`BIGINT`
`BIGINT`
`BIGINT UNSIGNED`
`DECIMAL(20, 0)`
`FLOAT`
`BINARY_FLOAT`
`REAL`
`FLOAT4`
`REAL`
`FLOAT`
`DOUBLE`
`DOUBLE PRECISION`
`BINARY_DOUBLE`
`FLOAT8`
`DOUBLE PRECISION`
`FLOAT`
`DOUBLE`
`NUMERIC(p, s)`
`DECIMAL(p, s)`
`SMALLINT`
`FLOAT(s)`
`DOUBLE PRECISION`
`REAL`
`NUMBER(p, s)`
`NUMERIC(p, s)`
`DECIMAL(p, s)`
`DECIMAL(p, s)`
`DECIMAL(p, s)`
`BOOLEAN`
`TINYINT(1)`
`BOOLEAN`
`BIT`
`BOOLEAN`
`DATE`
`DATE`
`DATE`
`DATE`
`DATE`
`TIME [(p)]`
`DATE`
`TIME [(p)] [WITHOUT TIMEZONE]`
`TIME(0)`
`TIME [(p)] [WITHOUT TIMEZONE]`
`DATETIME [(p)]`
`TIMESTAMP [(p)] [WITHOUT TIMEZONE]`
`TIMESTAMP [(p)] [WITHOUT TIMEZONE]`
`DATETIME`
`DATETIME2`
`TIMESTAMP [(p)] [WITHOUT TIMEZONE]`
`CHAR(n)`
`VARCHAR(n)`
`TEXT`
`CHAR(n)`
`VARCHAR(n)`
`CLOB`
`CHAR(n)`
`CHARACTER(n)`
`VARCHAR(n)`
`CHARACTER VARYING(n)`
`TEXT`
`CHAR(n)`
`NCHAR(n)`
`VARCHAR(n)`
`NVARCHAR(n)`
`TEXT`
`NTEXT`
`STRING`
`BINARY`
`VARBINARY`
`BLOB`
`RAW(s)`
`BLOB`
`BYTEA`
`BINARY(n)`
`VARBINARY(n)`
`BYTES`
`ARRAY`
`ARRAY`

 Back to top
