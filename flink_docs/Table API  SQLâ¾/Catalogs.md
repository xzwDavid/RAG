# Catalogs


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Catalogs#


Catalogs provide metadata, such as databases, tables, partitions, views, and functions and information needed to access data stored in a database or other external systems.


One of the most crucial aspects of data processing is managing metadata.
It may be transient metadata like temporary tables, or UDFs registered against the table environment.
Or permanent metadata, like that in a Hive Metastore. Catalogs provide a unified API for managing metadata and making it accessible from the Table API and SQL Queries.


Catalog enables users to reference existing metadata in their data systems, and automatically maps them to Flink’s corresponding metadata.
For example, Flink can map JDBC tables to Flink table automatically, and users don’t have to manually re-writing DDLs in Flink.
Catalog greatly simplifies steps required to get started with Flink with users’ existing system, and greatly enhanced user experiences.


## Catalog Types#


### GenericInMemoryCatalog#


The GenericInMemoryCatalog is an in-memory implementation of a catalog. All objects will be available only for the lifetime of the session.

`GenericInMemoryCatalog`

### JdbcCatalog#


The JdbcCatalog enables users to connect Flink to relational databases over JDBC protocol. Postgres Catalog and MySQL Catalog are the only two implementations of JDBC Catalog at the moment.
See JdbcCatalog documentation for more details on setting up the catalog.

`JdbcCatalog`

### HiveCatalog#


The HiveCatalog serves two purposes; as persistent storage for pure Flink metadata, and as an interface for reading and writing existing Hive metadata.
Flink’s Hive documentation provides full details on setting up the catalog and interfacing with an existing Hive installation.

`HiveCatalog`

> 
  The Hive Metastore stores all meta-object names in lower case. This is unlike GenericInMemoryCatalog which is case-sensitive


`GenericInMemoryCatalog`

### User-Defined Catalog#


Catalogs are pluggable and users can develop custom catalogs by implementing the Catalog interface.

`Catalog`

In order to use custom catalogs with Flink SQL, users should implement a corresponding catalog factory by implementing the CatalogFactory interface.
The factory is discovered using Java’s Service Provider Interfaces (SPI).
Classes that implement this interface can be added to  META_INF/services/org.apache.flink.table.factories.Factory in JAR files.
The provided factory identifier will be used for matching against the required type property in a SQL CREATE CATALOG DDL statement.

`CatalogFactory`
`META_INF/services/org.apache.flink.table.factories.Factory`
`type`
`CREATE CATALOG`

> 
  Since Flink v1.16, TableEnvironment introduces a user class loader to have a consistent class loading behavior in table programs, SQL Client and SQL Gateway. The user classloader manages all user jars such as jar added by ADD JAR or CREATE FUNCTION .. USING JAR .. statements.
User-defined catalogs should replace Thread.currentThread().getContextClassLoader() with the user class loader to load classes. Otherwise, ClassNotFoundException maybe thrown. The user class loader can be accessed via CatalogFactory.Context#getClassLoader.


`ADD JAR`
`CREATE FUNCTION .. USING JAR ..`
`Thread.currentThread().getContextClassLoader()`
`ClassNotFoundException`
`CatalogFactory.Context#getClassLoader`

#### Interface in Catalog for supporting time travel#


Starting from version 1.18, the Flink framework supports time travel to query historical data of a table. To query the historical data of a table, users should implement getTable(ObjectPath tablePath, long timestamp) method for the catalog that the table belongs to.

`getTable(ObjectPath tablePath, long timestamp)`

```
public class MyCatalogSupportTimeTravel implements Catalog {

    @Override
    public CatalogBaseTable getTable(ObjectPath tablePath, long timestamp)
            throws TableNotExistException {
        // Build a schema corresponding to the specific time point.
        Schema schema = buildSchema(timestamp);
        // Set parameters to read data at the corresponding time point.
        Map<String, String> options = buildOptions(timestamp);
        // Build CatalogTable
        CatalogTable catalogTable =
                CatalogTable.of(schema, "", Collections.emptyList(), options, timestamp);
        return catalogTable;
    }
}

public class MyDynamicTableFactory implements DynamicTableSourceFactory {
    @Override
    public DynamicTableSource createDynamicTableSource(Context context) {
        final ReadableConfig configuration =
                Configuration.fromMap(context.getCatalogTable().getOptions());

        // Get snapshot from CatalogTable
        final Optional<Long> snapshot = context.getCatalogTable().getSnapshot();

        // Build DynamicTableSource using snapshot options.
        final DynamicTableSource dynamicTableSource = buildDynamicSource(configuration, snapshot);

        return dynamicTableSource;
    }
}

```

`public class MyCatalogSupportTimeTravel implements Catalog {

    @Override
    public CatalogBaseTable getTable(ObjectPath tablePath, long timestamp)
            throws TableNotExistException {
        // Build a schema corresponding to the specific time point.
        Schema schema = buildSchema(timestamp);
        // Set parameters to read data at the corresponding time point.
        Map<String, String> options = buildOptions(timestamp);
        // Build CatalogTable
        CatalogTable catalogTable =
                CatalogTable.of(schema, "", Collections.emptyList(), options, timestamp);
        return catalogTable;
    }
}

public class MyDynamicTableFactory implements DynamicTableSourceFactory {
    @Override
    public DynamicTableSource createDynamicTableSource(Context context) {
        final ReadableConfig configuration =
                Configuration.fromMap(context.getCatalogTable().getOptions());

        // Get snapshot from CatalogTable
        final Optional<Long> snapshot = context.getCatalogTable().getSnapshot();

        // Build DynamicTableSource using snapshot options.
        final DynamicTableSource dynamicTableSource = buildDynamicSource(configuration, snapshot);

        return dynamicTableSource;
    }
}
`

## How to Create and Register Flink Tables to Catalog#


### Using SQL DDL#


Users can use SQL DDL to create tables in catalogs in both Table API and SQL.


```
TableEnvironment tableEnv = ...;

// Create a HiveCatalog 
Catalog catalog = new HiveCatalog("myhive", null, "<path_of_hive_conf>");

// Register the catalog
tableEnv.registerCatalog("myhive", catalog);

// Create a catalog database
tableEnv.executeSql("CREATE DATABASE mydb WITH (...)");

// Create a catalog table
tableEnv.executeSql("CREATE TABLE mytable (name STRING, age INT) WITH (...)");

tableEnv.listTables(); // should return the tables in current catalog and database.

```

`TableEnvironment tableEnv = ...;

// Create a HiveCatalog 
Catalog catalog = new HiveCatalog("myhive", null, "<path_of_hive_conf>");

// Register the catalog
tableEnv.registerCatalog("myhive", catalog);

// Create a catalog database
tableEnv.executeSql("CREATE DATABASE mydb WITH (...)");

// Create a catalog table
tableEnv.executeSql("CREATE TABLE mytable (name STRING, age INT) WITH (...)");

tableEnv.listTables(); // should return the tables in current catalog and database.
`

```
val tableEnv = ...

// Create a HiveCatalog 
val catalog = new HiveCatalog("myhive", null, "<path_of_hive_conf>")

// Register the catalog
tableEnv.registerCatalog("myhive", catalog)

// Create a catalog database
tableEnv.executeSql("CREATE DATABASE mydb WITH (...)")

// Create a catalog table
tableEnv.executeSql("CREATE TABLE mytable (name STRING, age INT) WITH (...)")

tableEnv.listTables() // should return the tables in current catalog and database.

```

`val tableEnv = ...

// Create a HiveCatalog 
val catalog = new HiveCatalog("myhive", null, "<path_of_hive_conf>")

// Register the catalog
tableEnv.registerCatalog("myhive", catalog)

// Create a catalog database
tableEnv.executeSql("CREATE DATABASE mydb WITH (...)")

// Create a catalog table
tableEnv.executeSql("CREATE TABLE mytable (name STRING, age INT) WITH (...)")

tableEnv.listTables() // should return the tables in current catalog and database.
`

```
from pyflink.table.catalog import HiveCatalog

# Create a HiveCatalog
catalog = HiveCatalog("myhive", None, "<path_of_hive_conf>")

# Register the catalog
t_env.register_catalog("myhive", catalog)

# Create a catalog database
t_env.execute_sql("CREATE DATABASE mydb WITH (...)")

# Create a catalog table
t_env.execute_sql("CREATE TABLE mytable (name STRING, age INT) WITH (...)")

# should return the tables in current catalog and database.
t_env.list_tables()

```

`from pyflink.table.catalog import HiveCatalog

# Create a HiveCatalog
catalog = HiveCatalog("myhive", None, "<path_of_hive_conf>")

# Register the catalog
t_env.register_catalog("myhive", catalog)

# Create a catalog database
t_env.execute_sql("CREATE DATABASE mydb WITH (...)")

# Create a catalog table
t_env.execute_sql("CREATE TABLE mytable (name STRING, age INT) WITH (...)")

# should return the tables in current catalog and database.
t_env.list_tables()
`

```
// the catalog should have been registered via yaml file
Flink SQL> CREATE DATABASE mydb WITH (...);

Flink SQL> CREATE TABLE mytable (name STRING, age INT) WITH (...);

Flink SQL> SHOW TABLES;
mytable

```

`// the catalog should have been registered via yaml file
Flink SQL> CREATE DATABASE mydb WITH (...);

Flink SQL> CREATE TABLE mytable (name STRING, age INT) WITH (...);

Flink SQL> SHOW TABLES;
mytable
`

For detailed information, please check out Flink SQL CREATE DDL.


### Using Java, Scala or Python#


Users can use Java, Scala or Python to create catalog tables programmatically.


```
import org.apache.flink.table.api.*;
import org.apache.flink.table.catalog.*;
import org.apache.flink.table.catalog.hive.HiveCatalog;

TableEnvironment tableEnv = TableEnvironment.create(EnvironmentSettings.inStreamingMode());

// Create a HiveCatalog 
Catalog catalog = new HiveCatalog("myhive", null, "<path_of_hive_conf>");

// Register the catalog
tableEnv.registerCatalog("myhive", catalog);

// Create a catalog database 
catalog.createDatabase("mydb", new CatalogDatabaseImpl(...));

// Create a catalog table
final Schema schema = Schema.newBuilder()
    .column("name", DataTypes.STRING())
    .column("age", DataTypes.INT())
    .build();

tableEnv.createTable("myhive.mydb.mytable", TableDescriptor.forConnector("kafka")
    .schema(schema)
    // â¦
    .build());

List<String> tables = catalog.listTables("mydb"); // tables should contain "mytable"

```

`import org.apache.flink.table.api.*;
import org.apache.flink.table.catalog.*;
import org.apache.flink.table.catalog.hive.HiveCatalog;

TableEnvironment tableEnv = TableEnvironment.create(EnvironmentSettings.inStreamingMode());

// Create a HiveCatalog 
Catalog catalog = new HiveCatalog("myhive", null, "<path_of_hive_conf>");

// Register the catalog
tableEnv.registerCatalog("myhive", catalog);

// Create a catalog database 
catalog.createDatabase("mydb", new CatalogDatabaseImpl(...));

// Create a catalog table
final Schema schema = Schema.newBuilder()
    .column("name", DataTypes.STRING())
    .column("age", DataTypes.INT())
    .build();

tableEnv.createTable("myhive.mydb.mytable", TableDescriptor.forConnector("kafka")
    .schema(schema)
    // â¦
    .build());

List<String> tables = catalog.listTables("mydb"); // tables should contain "mytable"
`

```
import org.apache.flink.table.api._
import org.apache.flink.table.catalog._
import org.apache.flink.table.catalog.hive.HiveCatalog

val tableEnv = TableEnvironment.create(EnvironmentSettings.inStreamingMode())

// Create a HiveCatalog 
val catalog = new HiveCatalog("myhive", null, "<path_of_hive_conf>")

// Register the catalog
tableEnv.registerCatalog("myhive", catalog)

// Create a catalog database 
catalog.createDatabase("mydb", new CatalogDatabaseImpl(...))

// Create a catalog table
val schema = Schema.newBuilder()
    .column("name", DataTypes.STRING())
    .column("age", DataTypes.INT())
    .build()

tableEnv.createTable("myhive.mydb.mytable", TableDescriptor.forConnector("kafka")
    .schema(schema)
    // â¦
    .build())
    
val tables = catalog.listTables("mydb") // tables should contain "mytable"

```

`import org.apache.flink.table.api._
import org.apache.flink.table.catalog._
import org.apache.flink.table.catalog.hive.HiveCatalog

val tableEnv = TableEnvironment.create(EnvironmentSettings.inStreamingMode())

// Create a HiveCatalog 
val catalog = new HiveCatalog("myhive", null, "<path_of_hive_conf>")

// Register the catalog
tableEnv.registerCatalog("myhive", catalog)

// Create a catalog database 
catalog.createDatabase("mydb", new CatalogDatabaseImpl(...))

// Create a catalog table
val schema = Schema.newBuilder()
    .column("name", DataTypes.STRING())
    .column("age", DataTypes.INT())
    .build()

tableEnv.createTable("myhive.mydb.mytable", TableDescriptor.forConnector("kafka")
    .schema(schema)
    // â¦
    .build())
    
val tables = catalog.listTables("mydb") // tables should contain "mytable"
`

```
from pyflink.table import *
from pyflink.table.catalog import HiveCatalog, CatalogDatabase, ObjectPath, CatalogBaseTable

settings = EnvironmentSettings.in_batch_mode()
t_env = TableEnvironment.create(settings)

# Create a HiveCatalog
catalog = HiveCatalog("myhive", None, "<path_of_hive_conf>")

# Register the catalog
t_env.register_catalog("myhive", catalog)

# Create a catalog database
database = CatalogDatabase.create_instance({"k1": "v1"}, None)
catalog.create_database("mydb", database)

# Create a catalog table
schema = Schema.new_builder() \
    .column("name", DataTypes.STRING()) \
    .column("age", DataTypes.INT()) \
    .build()
    
catalog_table = t_env.create_table("myhive.mydb.mytable", TableDescriptor.for_connector("kafka")
    .schema(schema)
    # â¦
    .build())

# tables should contain "mytable"
tables = catalog.list_tables("mydb")

```

`from pyflink.table import *
from pyflink.table.catalog import HiveCatalog, CatalogDatabase, ObjectPath, CatalogBaseTable

settings = EnvironmentSettings.in_batch_mode()
t_env = TableEnvironment.create(settings)

# Create a HiveCatalog
catalog = HiveCatalog("myhive", None, "<path_of_hive_conf>")

# Register the catalog
t_env.register_catalog("myhive", catalog)

# Create a catalog database
database = CatalogDatabase.create_instance({"k1": "v1"}, None)
catalog.create_database("mydb", database)

# Create a catalog table
schema = Schema.new_builder() \
    .column("name", DataTypes.STRING()) \
    .column("age", DataTypes.INT()) \
    .build()
    
catalog_table = t_env.create_table("myhive.mydb.mytable", TableDescriptor.for_connector("kafka")
    .schema(schema)
    # â¦
    .build())

# tables should contain "mytable"
tables = catalog.list_tables("mydb")
`

## Catalog API#


Note: only catalog program APIs are listed here. Users can achieve many of the same functionalities with SQL DDL.
For detailed DDL information, please refer to SQL CREATE DDL.


### Database operations#


```
// create database
catalog.createDatabase("mydb", new CatalogDatabaseImpl(...), false);

// drop database
catalog.dropDatabase("mydb", false);

// alter database
catalog.alterDatabase("mydb", new CatalogDatabaseImpl(...), false);

// get database
catalog.getDatabase("mydb");

// check if a database exist
catalog.databaseExists("mydb");

// list databases in a catalog
catalog.listDatabases();

```

`// create database
catalog.createDatabase("mydb", new CatalogDatabaseImpl(...), false);

// drop database
catalog.dropDatabase("mydb", false);

// alter database
catalog.alterDatabase("mydb", new CatalogDatabaseImpl(...), false);

// get database
catalog.getDatabase("mydb");

// check if a database exist
catalog.databaseExists("mydb");

// list databases in a catalog
catalog.listDatabases();
`

```
from pyflink.table.catalog import CatalogDatabase

# create database
catalog_database = CatalogDatabase.create_instance({"k1": "v1"}, None)
catalog.create_database("mydb", catalog_database, False)

# drop database
catalog.drop_database("mydb", False)

# alter database
catalog.alter_database("mydb", catalog_database, False)

# get database
catalog.get_database("mydb")

# check if a database exist
catalog.database_exists("mydb")

# list databases in a catalog
catalog.list_databases()

```

`from pyflink.table.catalog import CatalogDatabase

# create database
catalog_database = CatalogDatabase.create_instance({"k1": "v1"}, None)
catalog.create_database("mydb", catalog_database, False)

# drop database
catalog.drop_database("mydb", False)

# alter database
catalog.alter_database("mydb", catalog_database, False)

# get database
catalog.get_database("mydb")

# check if a database exist
catalog.database_exists("mydb")

# list databases in a catalog
catalog.list_databases()
`

### Table operations#


```
// create table
catalog.createTable(new ObjectPath("mydb", "mytable"), new CatalogTableImpl(...), false);

// drop table
catalog.dropTable(new ObjectPath("mydb", "mytable"), false);

// alter table
catalog.alterTable(new ObjectPath("mydb", "mytable"), new CatalogTableImpl(...), false);

// rename table
catalog.renameTable(new ObjectPath("mydb", "mytable"), "my_new_table");

// get table
catalog.getTable("mytable");

// check if a table exist or not
catalog.tableExists("mytable");

// list tables in a database
catalog.listTables("mydb");

```

`// create table
catalog.createTable(new ObjectPath("mydb", "mytable"), new CatalogTableImpl(...), false);

// drop table
catalog.dropTable(new ObjectPath("mydb", "mytable"), false);

// alter table
catalog.alterTable(new ObjectPath("mydb", "mytable"), new CatalogTableImpl(...), false);

// rename table
catalog.renameTable(new ObjectPath("mydb", "mytable"), "my_new_table");

// get table
catalog.getTable("mytable");

// check if a table exist or not
catalog.tableExists("mytable");

// list tables in a database
catalog.listTables("mydb");
`

```
from pyflink.table import *
from pyflink.table.catalog import CatalogBaseTable, ObjectPath
from pyflink.table.descriptors import Kafka

table_schema = TableSchema.builder() \
    .field("name", DataTypes.STRING()) \
    .field("age", DataTypes.INT()) \
    .build()

table_properties = Kafka() \
    .version("0.11") \
    .start_from_earlist() \
    .to_properties()

catalog_table = CatalogBaseTable.create_table(schema=table_schema, properties=table_properties, comment="my comment")

# create table
catalog.create_table(ObjectPath("mydb", "mytable"), catalog_table, False)

# drop table
catalog.drop_table(ObjectPath("mydb", "mytable"), False)

# alter table
catalog.alter_table(ObjectPath("mydb", "mytable"), catalog_table, False)

# rename table
catalog.rename_table(ObjectPath("mydb", "mytable"), "my_new_table")

# get table
catalog.get_table("mytable")

# check if a table exist or not
catalog.table_exists("mytable")

# list tables in a database
catalog.list_tables("mydb")

```

`from pyflink.table import *
from pyflink.table.catalog import CatalogBaseTable, ObjectPath
from pyflink.table.descriptors import Kafka

table_schema = TableSchema.builder() \
    .field("name", DataTypes.STRING()) \
    .field("age", DataTypes.INT()) \
    .build()

table_properties = Kafka() \
    .version("0.11") \
    .start_from_earlist() \
    .to_properties()

catalog_table = CatalogBaseTable.create_table(schema=table_schema, properties=table_properties, comment="my comment")

# create table
catalog.create_table(ObjectPath("mydb", "mytable"), catalog_table, False)

# drop table
catalog.drop_table(ObjectPath("mydb", "mytable"), False)

# alter table
catalog.alter_table(ObjectPath("mydb", "mytable"), catalog_table, False)

# rename table
catalog.rename_table(ObjectPath("mydb", "mytable"), "my_new_table")

# get table
catalog.get_table("mytable")

# check if a table exist or not
catalog.table_exists("mytable")

# list tables in a database
catalog.list_tables("mydb")
`

### View operations#


```
// create view
catalog.createTable(new ObjectPath("mydb", "myview"), new CatalogViewImpl(...), false);

// drop view
catalog.dropTable(new ObjectPath("mydb", "myview"), false);

// alter view
catalog.alterTable(new ObjectPath("mydb", "mytable"), new CatalogViewImpl(...), false);

// rename view
catalog.renameTable(new ObjectPath("mydb", "myview"), "my_new_view", false);

// get view
catalog.getTable("myview");

// check if a view exist or not
catalog.tableExists("mytable");

// list views in a database
catalog.listViews("mydb");

```

`// create view
catalog.createTable(new ObjectPath("mydb", "myview"), new CatalogViewImpl(...), false);

// drop view
catalog.dropTable(new ObjectPath("mydb", "myview"), false);

// alter view
catalog.alterTable(new ObjectPath("mydb", "mytable"), new CatalogViewImpl(...), false);

// rename view
catalog.renameTable(new ObjectPath("mydb", "myview"), "my_new_view", false);

// get view
catalog.getTable("myview");

// check if a view exist or not
catalog.tableExists("mytable");

// list views in a database
catalog.listViews("mydb");
`

```
from pyflink.table import *
from pyflink.table.catalog import CatalogBaseTable, ObjectPath

table_schema = TableSchema.builder() \
    .field("name", DataTypes.STRING()) \
    .field("age", DataTypes.INT()) \
    .build()

catalog_table = CatalogBaseTable.create_view(
    original_query="select * from t1",
    expanded_query="select * from test-catalog.db1.t1",
    schema=table_schema,
    properties={},
    comment="This is a view"
)

catalog.create_table(ObjectPath("mydb", "myview"), catalog_table, False)

# drop view
catalog.drop_table(ObjectPath("mydb", "myview"), False)

# alter view
catalog.alter_table(ObjectPath("mydb", "mytable"), catalog_table, False)

# rename view
catalog.rename_table(ObjectPath("mydb", "myview"), "my_new_view", False)

# get view
catalog.get_table("myview")

# check if a view exist or not
catalog.table_exists("mytable")

# list views in a database
catalog.list_views("mydb")

```

`from pyflink.table import *
from pyflink.table.catalog import CatalogBaseTable, ObjectPath

table_schema = TableSchema.builder() \
    .field("name", DataTypes.STRING()) \
    .field("age", DataTypes.INT()) \
    .build()

catalog_table = CatalogBaseTable.create_view(
    original_query="select * from t1",
    expanded_query="select * from test-catalog.db1.t1",
    schema=table_schema,
    properties={},
    comment="This is a view"
)

catalog.create_table(ObjectPath("mydb", "myview"), catalog_table, False)

# drop view
catalog.drop_table(ObjectPath("mydb", "myview"), False)

# alter view
catalog.alter_table(ObjectPath("mydb", "mytable"), catalog_table, False)

# rename view
catalog.rename_table(ObjectPath("mydb", "myview"), "my_new_view", False)

# get view
catalog.get_table("myview")

# check if a view exist or not
catalog.table_exists("mytable")

# list views in a database
catalog.list_views("mydb")
`

### Partition operations#


```
// create view
catalog.createPartition(
    new ObjectPath("mydb", "mytable"),
    new CatalogPartitionSpec(...),
    new CatalogPartitionImpl(...),
    false);

// drop partition
catalog.dropPartition(new ObjectPath("mydb", "mytable"), new CatalogPartitionSpec(...), false);

// alter partition
catalog.alterPartition(
    new ObjectPath("mydb", "mytable"),
    new CatalogPartitionSpec(...),
    new CatalogPartitionImpl(...),
    false);

// get partition
catalog.getPartition(new ObjectPath("mydb", "mytable"), new CatalogPartitionSpec(...));

// check if a partition exist or not
catalog.partitionExists(new ObjectPath("mydb", "mytable"), new CatalogPartitionSpec(...));

// list partitions of a table
catalog.listPartitions(new ObjectPath("mydb", "mytable"));

// list partitions of a table under a give partition spec
catalog.listPartitions(new ObjectPath("mydb", "mytable"), new CatalogPartitionSpec(...));

// list partitions of a table by expression filter
catalog.listPartitionsByFilter(new ObjectPath("mydb", "mytable"), Arrays.asList(epr1, ...));

```

`// create view
catalog.createPartition(
    new ObjectPath("mydb", "mytable"),
    new CatalogPartitionSpec(...),
    new CatalogPartitionImpl(...),
    false);

// drop partition
catalog.dropPartition(new ObjectPath("mydb", "mytable"), new CatalogPartitionSpec(...), false);

// alter partition
catalog.alterPartition(
    new ObjectPath("mydb", "mytable"),
    new CatalogPartitionSpec(...),
    new CatalogPartitionImpl(...),
    false);

// get partition
catalog.getPartition(new ObjectPath("mydb", "mytable"), new CatalogPartitionSpec(...));

// check if a partition exist or not
catalog.partitionExists(new ObjectPath("mydb", "mytable"), new CatalogPartitionSpec(...));

// list partitions of a table
catalog.listPartitions(new ObjectPath("mydb", "mytable"));

// list partitions of a table under a give partition spec
catalog.listPartitions(new ObjectPath("mydb", "mytable"), new CatalogPartitionSpec(...));

// list partitions of a table by expression filter
catalog.listPartitionsByFilter(new ObjectPath("mydb", "mytable"), Arrays.asList(epr1, ...));
`

```
from pyflink.table.catalog import ObjectPath, CatalogPartitionSpec, CatalogPartition

catalog_partition = CatalogPartition.create_instance({}, "my partition")

catalog_partition_spec = CatalogPartitionSpec({"third": "2010", "second": "bob"})
catalog.create_partition(
    ObjectPath("mydb", "mytable"),
    catalog_partition_spec,
    catalog_partition,
    False)

# drop partition
catalog.drop_partition(ObjectPath("mydb", "mytable"), catalog_partition_spec, False)

# alter partition
catalog.alter_partition(
    ObjectPath("mydb", "mytable"),
    CatalogPartitionSpec(...),
    catalog_partition,
    False)

# get partition
catalog.get_partition(ObjectPath("mydb", "mytable"), catalog_partition_spec)

# check if a partition exist or not
catalog.partition_exists(ObjectPath("mydb", "mytable"), catalog_partition_spec)

# list partitions of a table
catalog.list_partitions(ObjectPath("mydb", "mytable"))

# list partitions of a table under a give partition spec
catalog.list_partitions(ObjectPath("mydb", "mytable"), catalog_partition_spec)

```

`from pyflink.table.catalog import ObjectPath, CatalogPartitionSpec, CatalogPartition

catalog_partition = CatalogPartition.create_instance({}, "my partition")

catalog_partition_spec = CatalogPartitionSpec({"third": "2010", "second": "bob"})
catalog.create_partition(
    ObjectPath("mydb", "mytable"),
    catalog_partition_spec,
    catalog_partition,
    False)

# drop partition
catalog.drop_partition(ObjectPath("mydb", "mytable"), catalog_partition_spec, False)

# alter partition
catalog.alter_partition(
    ObjectPath("mydb", "mytable"),
    CatalogPartitionSpec(...),
    catalog_partition,
    False)

# get partition
catalog.get_partition(ObjectPath("mydb", "mytable"), catalog_partition_spec)

# check if a partition exist or not
catalog.partition_exists(ObjectPath("mydb", "mytable"), catalog_partition_spec)

# list partitions of a table
catalog.list_partitions(ObjectPath("mydb", "mytable"))

# list partitions of a table under a give partition spec
catalog.list_partitions(ObjectPath("mydb", "mytable"), catalog_partition_spec)
`

### Function operations#


```
// create function
catalog.createFunction(new ObjectPath("mydb", "myfunc"), new CatalogFunctionImpl(...), false);

// drop function
catalog.dropFunction(new ObjectPath("mydb", "myfunc"), false);

// alter function
catalog.alterFunction(new ObjectPath("mydb", "myfunc"), new CatalogFunctionImpl(...), false);

// get function
catalog.getFunction("myfunc");

// check if a function exist or not
catalog.functionExists("myfunc");

// list functions in a database
catalog.listFunctions("mydb");

```

`// create function
catalog.createFunction(new ObjectPath("mydb", "myfunc"), new CatalogFunctionImpl(...), false);

// drop function
catalog.dropFunction(new ObjectPath("mydb", "myfunc"), false);

// alter function
catalog.alterFunction(new ObjectPath("mydb", "myfunc"), new CatalogFunctionImpl(...), false);

// get function
catalog.getFunction("myfunc");

// check if a function exist or not
catalog.functionExists("myfunc");

// list functions in a database
catalog.listFunctions("mydb");
`

```
from pyflink.table.catalog import ObjectPath, CatalogFunction

catalog_function = CatalogFunction.create_instance(class_name="my.python.udf")

# create function
catalog.create_function(ObjectPath("mydb", "myfunc"), catalog_function, False)

# drop function
catalog.drop_function(ObjectPath("mydb", "myfunc"), False)

# alter function
catalog.alter_function(ObjectPath("mydb", "myfunc"), catalog_function, False)

# get function
catalog.get_function("myfunc")

# check if a function exist or not
catalog.function_exists("myfunc")

# list functions in a database
catalog.list_functions("mydb")

```

`from pyflink.table.catalog import ObjectPath, CatalogFunction

catalog_function = CatalogFunction.create_instance(class_name="my.python.udf")

# create function
catalog.create_function(ObjectPath("mydb", "myfunc"), catalog_function, False)

# drop function
catalog.drop_function(ObjectPath("mydb", "myfunc"), False)

# alter function
catalog.alter_function(ObjectPath("mydb", "myfunc"), catalog_function, False)

# get function
catalog.get_function("myfunc")

# check if a function exist or not
catalog.function_exists("myfunc")

# list functions in a database
catalog.list_functions("mydb")
`

## Table API and SQL for Catalog#


### Registering a Catalog#


Users have access to a default in-memory catalog named default_catalog, that is always created by default. This catalog by default has a single database called default_database.
Users can also register additional catalogs into an existing Flink session.

`default_catalog`
`default_database`

```
tableEnv.registerCatalog(new CustomCatalog("myCatalog"));

```

`tableEnv.registerCatalog(new CustomCatalog("myCatalog"));
`

```
t_env.register_catalog(catalog)

```

`t_env.register_catalog(catalog)
`

All catalogs defined using YAML must provide a type property that specifies the type of catalog.
The following types are supported out of the box.

`type`

```
catalogs:
   - name: myCatalog
     type: custom_catalog
     hive-conf-dir: ...

```

`catalogs:
   - name: myCatalog
     type: custom_catalog
     hive-conf-dir: ...
`

### Changing the Current Catalog And Database#


Flink will always search for tables, views, and UDF’s in the current catalog and database.


```
tableEnv.useCatalog("myCatalog");
tableEnv.useDatabase("myDb");

```

`tableEnv.useCatalog("myCatalog");
tableEnv.useDatabase("myDb");
`

```
t_env.use_catalog("myCatalog")
t_env.use_database("myDb")

```

`t_env.use_catalog("myCatalog")
t_env.use_database("myDb")
`

```
Flink SQL> USE CATALOG myCatalog;
Flink SQL> USE myDB;

```

`Flink SQL> USE CATALOG myCatalog;
Flink SQL> USE myDB;
`

Metadata from catalogs that are not the current catalog are accessible by providing fully qualified names in the form catalog.database.object.

`catalog.database.object`

```
tableEnv.from("not_the_current_catalog.not_the_current_db.my_table");

```

`tableEnv.from("not_the_current_catalog.not_the_current_db.my_table");
`

```
t_env.from_path("not_the_current_catalog.not_the_current_db.my_table")

```

`t_env.from_path("not_the_current_catalog.not_the_current_db.my_table")
`

```
Flink SQL> SELECT * FROM not_the_current_catalog.not_the_current_db.my_table;

```

`Flink SQL> SELECT * FROM not_the_current_catalog.not_the_current_db.my_table;
`

### List Available Catalogs#


```
tableEnv.listCatalogs();

```

`tableEnv.listCatalogs();
`

```
t_env.list_catalogs()

```

`t_env.list_catalogs()
`

```
Flink SQL> show catalogs;

```

`Flink SQL> show catalogs;
`

### List Available Databases#


```
tableEnv.listDatabases();

```

`tableEnv.listDatabases();
`

```
t_env.list_databases()

```

`t_env.list_databases()
`

```
Flink SQL> show databases;

```

`Flink SQL> show databases;
`

### List Available Tables#


```
tableEnv.listTables();

```

`tableEnv.listTables();
`

```
t_env.list_tables()

```

`t_env.list_tables()
`

```
Flink SQL> show tables;

```

`Flink SQL> show tables;
`

## Catalog Modification Listener#


Flink supports registering customized listener for catalog modification, such as database and table ddl. Flink will create
a CatalogModificationEvent event for ddl and notify CatalogModificationListener. You can implement a listener
and do some customized operations when receiving the event, such as report the information to some external meta-data systems.

`CatalogModificationEvent`
`CatalogModificationListener`

### Implement Catalog Listener#


There are two interfaces for the catalog modification listener: CatalogModificationListenerFactory to create the listener and CatalogModificationListener
to receive and process the event. You need to implement these interfaces and below is an example.

`CatalogModificationListenerFactory`
`CatalogModificationListener`

```
/** Factory used to create a {@link CatalogModificationListener} instance. */
public class YourCatalogListenerFactory implements CatalogModificationListenerFactory {
    /** The identifier for the customized listener factory, you can named it yourself. */
    private static final String IDENTIFIER = "your_factory";

    @Override
    public String factoryIdentifier() {
        return IDENTIFIER;
    }

    @Override
    public CatalogModificationListener createListener(Context context) {
        return new YourCatalogListener(Create http client from context);
    }
}

/** Customized catalog modification listener. */
public class YourCatalogListener implements CatalogModificationListener {
    private final HttpClient client;

    YourCatalogListener(HttpClient client) {
        this.client = client;
    }
    
    @Override
    public void onEvent(CatalogModificationEvent event) {
        // Report the database and table information via http client.
    }
}

```

`/** Factory used to create a {@link CatalogModificationListener} instance. */
public class YourCatalogListenerFactory implements CatalogModificationListenerFactory {
    /** The identifier for the customized listener factory, you can named it yourself. */
    private static final String IDENTIFIER = "your_factory";

    @Override
    public String factoryIdentifier() {
        return IDENTIFIER;
    }

    @Override
    public CatalogModificationListener createListener(Context context) {
        return new YourCatalogListener(Create http client from context);
    }
}

/** Customized catalog modification listener. */
public class YourCatalogListener implements CatalogModificationListener {
    private final HttpClient client;

    YourCatalogListener(HttpClient client) {
        this.client = client;
    }
    
    @Override
    public void onEvent(CatalogModificationEvent event) {
        // Report the database and table information via http client.
    }
}
`

You need to create a file org.apache.flink.table.factories.Factory in META-INF/services
with the content of the full name of YourCatalogListenerFactory for your
customized catalog listener factory. After that, you can package the codes into a jar file
and add it to lib of Flink cluster.

`org.apache.flink.table.factories.Factory`
`META-INF/services`
`the full name of YourCatalogListenerFactory`
`lib`

### Register Catalog Listener#


After implemented above catalog modification factory and listener, you can register it to the table environment.


```
Configuration configuration = new Configuration();

// Add the factory identifier, you can set multiple listeners in the configuraiton.
configuration.set(TableConfigOptions.TABLE_CATALOG_MODIFICATION_LISTENERS, Arrays.asList("your_factory"));
TableEnvironment env = TableEnvironment.create(
            EnvironmentSettings.newInstance()
                .withConfiguration(configuration)
                .build());

// Create/Alter/Drop database and table.
env.executeSql("CREATE TABLE ...").wait();

```

`Configuration configuration = new Configuration();

// Add the factory identifier, you can set multiple listeners in the configuraiton.
configuration.set(TableConfigOptions.TABLE_CATALOG_MODIFICATION_LISTENERS, Arrays.asList("your_factory"));
TableEnvironment env = TableEnvironment.create(
            EnvironmentSettings.newInstance()
                .withConfiguration(configuration)
                .build());

// Create/Alter/Drop database and table.
env.executeSql("CREATE TABLE ...").wait();
`

For sql-gateway, you can add the option table.catalog-modification.listeners in the Flink configuration file
and start the gateway, or you can also start sql-gateway with dynamic parameter, then you can use sql-client to perform ddl directly.

`table.catalog-modification.listeners`

## Catalog Store#


Catalog Store is used to store the configuration of catalogs. When using Catalog Store, the configurations
of catalogs created in the session will be persisted in the corresponding external system of Catalog Store.
Even if the session is reconstructed, previously created catalogs can still be retrieved from Catalog Store.


### Configure Catalog Store#


Users can configure the Catalog Store in different ways, one is to use the Table API, and another is to use YAML configuration.


Register a catalog store using catalog store instance:


```
// Initialize a catalog Store instance
CatalogStore catalogStore = new FileCatalogStore("file:///path/to/catalog/store/");

// set up the catalog store
final EnvironmentSettings settings =
        EnvironmentSettings.newInstance().inBatchMode()
        .withCatalogStore(catalogStore)
        .build();

```

`// Initialize a catalog Store instance
CatalogStore catalogStore = new FileCatalogStore("file:///path/to/catalog/store/");

// set up the catalog store
final EnvironmentSettings settings =
        EnvironmentSettings.newInstance().inBatchMode()
        .withCatalogStore(catalogStore)
        .build();
`

Register a catalog store using configuration:


```
// Set up configuration
Configuration configuration = new Configuration();
configuration.set("table.catalog-store.kind", "file");
configuration.set("table.catalog-store.file.path", "file:///path/to/catalog/store/");
// set up the configuration.
final EnvironmentSettings settings =
        EnvironmentSettings.newInstance().inBatchMode()
        .withConfiguration(configuration)
        .build();

final TableEnvironment tableEnv = TableEnvironment.create(settings);

```

`// Set up configuration
Configuration configuration = new Configuration();
configuration.set("table.catalog-store.kind", "file");
configuration.set("table.catalog-store.file.path", "file:///path/to/catalog/store/");
// set up the configuration.
final EnvironmentSettings settings =
        EnvironmentSettings.newInstance().inBatchMode()
        .withConfiguration(configuration)
        .build();

final TableEnvironment tableEnv = TableEnvironment.create(settings);
`

In SQL Gateway, it is recommended to configure the settings in a yaml file so that all sessions can automatically
use the pre-created Catalog. Usually, you need to configure the kind of Catalog Store and other
required parameters for the Catalog Store.


```
table.catalog-store.kind: file
table.catalog-store.file.path: file:///path/to/catalog/store/

```

`table.catalog-store.kind: file
table.catalog-store.file.path: file:///path/to/catalog/store/
`

### Catalog Store Type#


Flink has two built-in Catalog Stores, namely GenericInMemoryCatalogStore and FileCatalogStore,
but the Catalog Store model is extendable, so users can also implement their own custom Catalog Store.

`GenericInMemoryCatalogStore`
`FileCatalogStore`

#### GenericInMemoryCatalogStore#


GenericInMemoryCatalogStore is an implementation of CatalogStore that saves configuration information in memory.
All catalog configurations are only available within the sessions’ lifecycle, and the stored catalog configurations will be
automatically cleared after the session is closed.

`GenericInMemoryCatalogStore`
`CatalogStore`

> 
  By default, if no Catalog Store related configuration is specified, the system uses this implementation.



#### FileCatalogStore#


FileCatalogStore can save the Catalog configuration to a file. To use FileCatalogStore, you need to specify the directory where the Catalog configurations
needs to be saved. Each Catalog will have its own file named the same as the Catalog Name.

`FileCatalogStore`
`FileCatalogStore`

The FileCatalogStore implementation supports both local and remote file systems that are available via the Flink FileSystem abstraction.
If the given Catalog Store path does not exist either completely or partly, FileCatalogStore will try to create the missing directories.

`FileCatalogStore`
`FileSystem`
`FileCatalogStore`

> 
  If the given Catalog Store path does not exist and FileCatalogStore fails to create a directory, the Catalog Store cannot be initialized, hence an exception will be thrown.
In case the FileCatalogstore initialization is not successful, both SQL Client and SQL Gateway will be broken.


`FileCatalogStore`
`FileCatalogstore`

Here is an example directory structure representing the storage of Catalog configurations using FileCatalogStore:

`FileCatalogStore`

```
- /path/to/save/the/catalog/
  - catalog1.yaml
  - catalog2.yaml
  - catalog3.yaml

```

`- /path/to/save/the/catalog/
  - catalog1.yaml
  - catalog2.yaml
  - catalog3.yaml
`

#### Catalog Store Configuration#


The following options can be used to adjust the Catalog Store behavior.


##### table.catalog-store.kind


##### table.catalog-store.file.path


#### Custom Catalog Store#


Catalog Store is extensible, and users can customize Catalog Store by implementing its interface.
If SQL CLI or SQL Gateway needs to use Catalog Store, the corresponding CatalogStoreFactory interface
also needs to be implemented for this Catalog Store.


```
public class CustomCatalogStoreFactory implements CatalogStoreFactory {

    public static final String IDENTIFIER = "custom-kind";
    
    // Used to connect external storage systems
    private CustomClient client;
    
    @Override
    public CatalogStore createCatalogStore() {
        return new CustomCatalogStore();
    }

    @Override
    public void open(Context context) throws CatalogException {
        // initialize the resources, such as http client
        client = initClient(context);
    }

    @Override
    public void close() throws CatalogException {
        // release the resources
    }

    @Override
    public String factoryIdentifier() {
        // table store kind identifier
        return IDENTIFIER;
    }
    
    public Set<ConfigOption<?>> requiredOptions() {
        // define the required options
        Set<ConfigOption> options = new HashSet();
        options.add(OPTION_1);
        options.add(OPTION_2);
        
        return options;
    }

    @Override
    public Set<ConfigOption<?>> optionalOptions() {
        // define the optional options
    }
}

public class CustomCatalogStore extends AbstractCatalogStore {

    private Client client;
    
    public CustomCatalogStore(Client client) {
        this.client = client;
    }

    @Override
    public void storeCatalog(String catalogName, CatalogDescriptor catalog)
            throws CatalogException {
        // store the catalog
    }

    @Override
    public void removeCatalog(String catalogName, boolean ignoreIfNotExists)
            throws CatalogException {
        // remove the catalog descriptor
    }

    @Override
    public Optional<CatalogDescriptor> getCatalog(String catalogName) {
        // retrieve the catalog configuration and build the catalog descriptor
    }

    @Override
    public Set<String> listCatalogs() {
        // list all catalogs
    }

    @Override
    public boolean contains(String catalogName) {
    }
}

```

`public class CustomCatalogStoreFactory implements CatalogStoreFactory {

    public static final String IDENTIFIER = "custom-kind";
    
    // Used to connect external storage systems
    private CustomClient client;
    
    @Override
    public CatalogStore createCatalogStore() {
        return new CustomCatalogStore();
    }

    @Override
    public void open(Context context) throws CatalogException {
        // initialize the resources, such as http client
        client = initClient(context);
    }

    @Override
    public void close() throws CatalogException {
        // release the resources
    }

    @Override
    public String factoryIdentifier() {
        // table store kind identifier
        return IDENTIFIER;
    }
    
    public Set<ConfigOption<?>> requiredOptions() {
        // define the required options
        Set<ConfigOption> options = new HashSet();
        options.add(OPTION_1);
        options.add(OPTION_2);
        
        return options;
    }

    @Override
    public Set<ConfigOption<?>> optionalOptions() {
        // define the optional options
    }
}

public class CustomCatalogStore extends AbstractCatalogStore {

    private Client client;
    
    public CustomCatalogStore(Client client) {
        this.client = client;
    }

    @Override
    public void storeCatalog(String catalogName, CatalogDescriptor catalog)
            throws CatalogException {
        // store the catalog
    }

    @Override
    public void removeCatalog(String catalogName, boolean ignoreIfNotExists)
            throws CatalogException {
        // remove the catalog descriptor
    }

    @Override
    public Optional<CatalogDescriptor> getCatalog(String catalogName) {
        // retrieve the catalog configuration and build the catalog descriptor
    }

    @Override
    public Set<String> listCatalogs() {
        // list all catalogs
    }

    @Override
    public boolean contains(String catalogName) {
    }
}
`