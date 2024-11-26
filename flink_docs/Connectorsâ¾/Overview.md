# Overview


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Apache Hive#


Apache Hive has established itself as a focal point of the data warehousing ecosystem.
It serves as not only a SQL engine for big data analytics and ETL, but also a data management platform, where data is discovered, defined, and evolved.


Flink offers a two-fold integration with Hive.


The first is to leverage Hive’s Metastore as a persistent catalog with Flink’s HiveCatalog for storing Flink specific metadata across sessions.
For example, users can store their Kafka or Elasticsearch tables in Hive Metastore by using HiveCatalog, and reuse them later on in SQL queries.

`HiveCatalog`
`HiveCatalog`

The second is to offer Flink as an alternative engine for reading and writing Hive tables.


The HiveCatalog is designed to be âout of the boxâ compatible with existing Hive installations.
You do not need to modify your existing Hive Metastore or change the data placement or partitioning of your tables.

`HiveCatalog`

## Supported Hive Versions#


Flink supports the following Hive versions.

* 2.3

2.3.0
2.3.1
2.3.2
2.3.3
2.3.4
2.3.5
2.3.6
2.3.7
2.3.8
2.3.9
2.3.10


* 3.1

3.1.0
3.1.1
3.1.2
3.1.3


* 2.3.0
* 2.3.1
* 2.3.2
* 2.3.3
* 2.3.4
* 2.3.5
* 2.3.6
* 2.3.7
* 2.3.8
* 2.3.9
* 2.3.10
* 3.1.0
* 3.1.1
* 3.1.2
* 3.1.3

Please note Hive itself have different features available for different versions, and these issues are not caused by Flink:

* Hive built-in functions are supported in 1.2.0 and later.
* Column constraints, i.e. PRIMARY KEY and NOT NULL, are supported in 3.1.0 and later.
* Altering table statistics is supported in 1.2.0 and later.
* DATE column statistics are supported in 1.2.0 and later.
* Writing to ORC tables is not supported in 2.0.x.
`DATE`

### Dependencies#


To integrate with Hive, you need to add some extra dependencies to the /lib/ directory in Flink distribution
to make the integration work in Table API program or SQL in SQL Client.
Alternatively, you can put these dependencies in a dedicated folder, and add them to classpath with the -C
or -l option for Table API program or SQL Client respectively.

`/lib/`
`-C`
`-l`

Apache Hive is built on Hadoop, so you need to provide Hadoop dependencies, by setting the HADOOP_CLASSPATH
environment variable:

`HADOOP_CLASSPATH`

```
export HADOOP_CLASSPATH=`hadoop classpath`

```

`export HADOOP_CLASSPATH=`hadoop classpath`
`

There are two ways to add Hive dependencies. First is to use Flink’s bundled Hive jars. You can choose a bundled Hive jar according to the version of the metastore you use. Second is to add each of the required jars separately. The second way can be useful if the Hive version you’re using is not listed here.


NOTE: the recommended way to add dependency is to use a bundled jar. Separate jars should be used only if bundled jars don’t meet your needs.


#### Using bundled hive jar#


The following tables list all available bundled hive jars. You can pick one to the /lib/ directory in Flink distribution.

`/lib/`
`flink-sql-connector-hive-2.3.10`
`flink-sql-connector-hive-3.1.3`

#### User defined dependencies#


Please find the required dependencies for different Hive major versions below.


```

/flink-2.0-SNAPSHOT
   /lib

       // Flink's Hive connector.Contains flink-hadoop-compatibility and flink-orc jars
       flink-connector-hive-2.0-SNAPSHOT.jar

       // Hive dependencies
       hive-exec-2.3.4.jar

       // add antlr-runtime if you need to use hive dialect
       antlr-runtime-3.5.2.jar

```

`
/flink-2.0-SNAPSHOT
   /lib

       // Flink's Hive connector.Contains flink-hadoop-compatibility and flink-orc jars
       flink-connector-hive-2.0-SNAPSHOT.jar

       // Hive dependencies
       hive-exec-2.3.4.jar

       // add antlr-runtime if you need to use hive dialect
       antlr-runtime-3.5.2.jar
`

```
/flink-2.0-SNAPSHOT
   /lib

       // Flink's Hive connector
       flink-connector-hive-2.0-SNAPSHOT.jar

       // Hive dependencies
       hive-exec-3.1.0.jar
       libfb303-0.9.3.jar // libfb303 is not packed into hive-exec in some versions, need to add it separately

       // add antlr-runtime if you need to use hive dialect
       antlr-runtime-3.5.2.jar

```

`/flink-2.0-SNAPSHOT
   /lib

       // Flink's Hive connector
       flink-connector-hive-2.0-SNAPSHOT.jar

       // Hive dependencies
       hive-exec-3.1.0.jar
       libfb303-0.9.3.jar // libfb303 is not packed into hive-exec in some versions, need to add it separately

       // add antlr-runtime if you need to use hive dialect
       antlr-runtime-3.5.2.jar
`

### Program maven#


If you are building your own program, you need the following dependencies in your mvn file.
It’s recommended not to include these dependencies in the resulting jar file.
You’re supposed to add dependencies as stated above at runtime.


```
<!-- Flink Dependency -->
<dependency>
  <groupId>org.apache.flink</groupId>
  <artifactId>flink-connector-hive</artifactId>
  <version>2.0-SNAPSHOT</version>
  <scope>provided</scope>
</dependency>

<dependency>
  <groupId>org.apache.flink</groupId>
  <artifactId>flink-table-api-java-bridge_2.12</artifactId>
  <version>2.0-SNAPSHOT</version>
  <scope>provided</scope>
</dependency>

<!-- Hive Dependency -->
<dependency>
    <groupId>org.apache.hive</groupId>
    <artifactId>hive-exec</artifactId>
    <version>${hive.version}</version>
    <scope>provided</scope>
</dependency>

```

`<!-- Flink Dependency -->
<dependency>
  <groupId>org.apache.flink</groupId>
  <artifactId>flink-connector-hive</artifactId>
  <version>2.0-SNAPSHOT</version>
  <scope>provided</scope>
</dependency>

<dependency>
  <groupId>org.apache.flink</groupId>
  <artifactId>flink-table-api-java-bridge_2.12</artifactId>
  <version>2.0-SNAPSHOT</version>
  <scope>provided</scope>
</dependency>

<!-- Hive Dependency -->
<dependency>
    <groupId>org.apache.hive</groupId>
    <artifactId>hive-exec</artifactId>
    <version>${hive.version}</version>
    <scope>provided</scope>
</dependency>
`

## Connecting To Hive#


Connect to an existing Hive installation using the catalog interface
and HiveCatalog through the table environment or YAML configuration.


Following is an example of how to connect to Hive:


```

EnvironmentSettings settings = EnvironmentSettings.inStreamingMode();
TableEnvironment tableEnv = TableEnvironment.create(settings);

String name            = "myhive";
String defaultDatabase = "mydatabase";
String hiveConfDir     = "/opt/hive-conf";

HiveCatalog hive = new HiveCatalog(name, defaultDatabase, hiveConfDir);
tableEnv.registerCatalog("myhive", hive);

// set the HiveCatalog as the current catalog of the session
tableEnv.useCatalog("myhive");

```

`
EnvironmentSettings settings = EnvironmentSettings.inStreamingMode();
TableEnvironment tableEnv = TableEnvironment.create(settings);

String name            = "myhive";
String defaultDatabase = "mydatabase";
String hiveConfDir     = "/opt/hive-conf";

HiveCatalog hive = new HiveCatalog(name, defaultDatabase, hiveConfDir);
tableEnv.registerCatalog("myhive", hive);

// set the HiveCatalog as the current catalog of the session
tableEnv.useCatalog("myhive");
`

```

val settings = EnvironmentSettings.inStreamingMode()
val tableEnv = TableEnvironment.create(settings)

val name            = "myhive"
val defaultDatabase = "mydatabase"
val hiveConfDir     = "/opt/hive-conf"

val hive = new HiveCatalog(name, defaultDatabase, hiveConfDir)
tableEnv.registerCatalog("myhive", hive)

// set the HiveCatalog as the current catalog of the session
tableEnv.useCatalog("myhive")

```

`
val settings = EnvironmentSettings.inStreamingMode()
val tableEnv = TableEnvironment.create(settings)

val name            = "myhive"
val defaultDatabase = "mydatabase"
val hiveConfDir     = "/opt/hive-conf"

val hive = new HiveCatalog(name, defaultDatabase, hiveConfDir)
tableEnv.registerCatalog("myhive", hive)

// set the HiveCatalog as the current catalog of the session
tableEnv.useCatalog("myhive")
`

```
from pyflink.table import *
from pyflink.table.catalog import HiveCatalog

settings = EnvironmentSettings.in_batch_mode()
t_env = TableEnvironment.create(settings)

catalog_name = "myhive"
default_database = "mydatabase"
hive_conf_dir = "/opt/hive-conf"

hive_catalog = HiveCatalog(catalog_name, default_database, hive_conf_dir)
t_env.register_catalog("myhive", hive_catalog)

# set the HiveCatalog as the current catalog of the session
tableEnv.use_catalog("myhive")

```

`from pyflink.table import *
from pyflink.table.catalog import HiveCatalog

settings = EnvironmentSettings.in_batch_mode()
t_env = TableEnvironment.create(settings)

catalog_name = "myhive"
default_database = "mydatabase"
hive_conf_dir = "/opt/hive-conf"

hive_catalog = HiveCatalog(catalog_name, default_database, hive_conf_dir)
t_env.register_catalog("myhive", hive_catalog)

# set the HiveCatalog as the current catalog of the session
tableEnv.use_catalog("myhive")
`

```

execution:
    ...
    current-catalog: myhive  # set the HiveCatalog as the current catalog of the session
    current-database: mydatabase
    
catalogs:
   - name: myhive
     type: hive
     hive-conf-dir: /opt/hive-conf

```

`
execution:
    ...
    current-catalog: myhive  # set the HiveCatalog as the current catalog of the session
    current-database: mydatabase
    
catalogs:
   - name: myhive
     type: hive
     hive-conf-dir: /opt/hive-conf
`

```

CREATE CATALOG myhive WITH (
    'type' = 'hive',
    'default-database' = 'mydatabase',
    'hive-conf-dir' = '/opt/hive-conf'
);
-- set the HiveCatalog as the current catalog of the session
USE CATALOG myhive;

```

`
CREATE CATALOG myhive WITH (
    'type' = 'hive',
    'default-database' = 'mydatabase',
    'hive-conf-dir' = '/opt/hive-conf'
);
-- set the HiveCatalog as the current catalog of the session
USE CATALOG myhive;
`

Below are the options supported when creating a HiveCatalog instance with YAML file or DDL.

`HiveCatalog`

##### type

`'hive'`

##### name


##### hive-conf-dir


##### default-database


##### hive-version


##### hadoop-conf-dir


## DDL#


It’s recommended to use Hive dialect to execute DDLs to create
Hive tables, views, partitions, functions within Flink.


## DML#


Flink supports DML writing to Hive tables. Please refer to details in Reading & Writing Hive Tables
