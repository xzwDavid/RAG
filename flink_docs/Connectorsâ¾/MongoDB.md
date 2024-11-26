# MongoDB


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# MongoDB SQL Connector#



Scan Source: Bounded
Lookup Source: Sync Mode
Sink: Batch
Sink: Streaming Append & Upsert Mode


The MongoDB connector allows for reading data from and writing data into MongoDB.
This document describes how to set up the MongoDB connector to run SQL queries against MongoDB.


The connector can operate in upsert mode for exchanging UPDATE/DELETE messages with the external
system using the primary key defined on the DDL.


If no primary key is defined on the DDL, the connector can only operate in append mode for
exchanging INSERT only messages with external system.


## Dependencies#


In order to use the MongoDB connector the following dependencies are required for both projects
using a build automation tool (such as Maven or SBT) and SQL Client with SQL JAR bundles.


Only available for stable versions.


The MongoDB connector is not part of the binary distribution.
See how to link with it for cluster execution here.


## How to create a MongoDB table#


The MongoDB table can be defined as following:


```
-- register a MongoDB table 'users' in Flink SQL
CREATE TABLE MyUserTable (
  _id STRING,
  name STRING,
  age INT,
  status BOOLEAN,
  PRIMARY KEY (_id) NOT ENFORCED
) WITH (
   'connector' = 'mongodb',
   'uri' = 'mongodb://user:password@127.0.0.1:27017',
   'database' = 'my_db',
   'collection' = 'users'
);

-- write data into the MongoDB table from the other table "T"
INSERT INTO MyUserTable
SELECT _id, name, age, status FROM T;

-- scan data from the MongoDB table
SELECT id, name, age, status FROM MyUserTable;

-- temporal join the MongoDB table as a dimension table
SELECT * FROM myTopic
LEFT JOIN MyUserTable FOR SYSTEM_TIME AS OF myTopic.proctime
ON myTopic.key = MyUserTable._id;

```

`-- register a MongoDB table 'users' in Flink SQL
CREATE TABLE MyUserTable (
  _id STRING,
  name STRING,
  age INT,
  status BOOLEAN,
  PRIMARY KEY (_id) NOT ENFORCED
) WITH (
   'connector' = 'mongodb',
   'uri' = 'mongodb://user:password@127.0.0.1:27017',
   'database' = 'my_db',
   'collection' = 'users'
);

-- write data into the MongoDB table from the other table "T"
INSERT INTO MyUserTable
SELECT _id, name, age, status FROM T;

-- scan data from the MongoDB table
SELECT id, name, age, status FROM MyUserTable;

-- temporal join the MongoDB table as a dimension table
SELECT * FROM myTopic
LEFT JOIN MyUserTable FOR SYSTEM_TIME AS OF myTopic.proctime
ON myTopic.key = MyUserTable._id;
`

## Connector Options#


##### connector

`'mongodb'`

##### uri


##### database


##### collection


##### scan.fetch-size


##### scan.cursor.no-timeout


##### scan.partition.strategy


##### scan.partition.size


##### scan.partition.samples


##### lookup.cache


Enum


##### lookup.partial-cache.max-rows


##### lookup.partial-cache.expire-after-write


##### lookup.partial-cache.expire-after-access


##### lookup.partial-cache.caching-missing-key


##### lookup.max-retries


##### lookup.retry.interval


##### sink.buffer-flush.max-rows


##### sink.buffer-flush.interval


##### sink.max-retries


##### sink.retry.interval


##### sink.parallelism


##### sink.delivery-guarantee


Enum


## Features#


### Key handling#


The MongoDB sink can work in either upsert mode or append mode, depending on whether a primary key
is defined. If a primary key is defined, the MongoDB sink works in upsert mode which can consume
queries containing UPDATE/DELETE messages. If a primary key is not defined, the MongoDB sink works
in append mode which can only consume queries containing INSERT only messages.


In MongoDB the primary key is used to calculate the MongoDB document _id.
Its value must be unique and immutable in the collection, and may be of any
BSON Type other than an Array.
If the _id contains subfields, the subfield names cannot begin with a ($) symbol.


There are also some constraints on the primary key index.
Before MongoDB 4.2, the total size of an index entry, which can include structural overhead
depending on the BSON type, must be less than 1024 bytes.
Starting in version 4.2, MongoDB removes the Index Key Limit.
For more detailed introduction, you can refer to Index Key Limit.


The MongoDB connector generates a document _id for every row by compositing all primary key
fields in the order defined in the DDL.

* When there’s only a single field in the specified primary key, we convert the field data to bson
value as _id of the corresponding document.
* When there’s multiple fields in the specified primary key, we convert and composite these fields
into a bson document as the _id of the corresponding document.
For example, if have a primary key statement PRIMARY KEY (f1, f2) NOT ENFORCED,
the extracted _id will be the form like _id: {f1: v1, f2: v2}.
`PRIMARY KEY (f1, f2) NOT ENFORCED`
`_id: {f1: v1, f2: v2}`

Notice that it will be ambiguous if the _id field exists in DDL, but the primary key is not declared as _id.
Either use the _id column as the key, or rename the _id column.


See CREATE TABLE DDL for more details about PRIMARY KEY syntax.


### Partitioned Scan#


To accelerate reading data in parallel Source task instances, Flink provides partitioned scan
feature for MongoDB collection. The following partition strategies are provided:

`Source`
* single: treats the entire collection as a single partition.
* sample: samples the collection and generate partitions which is fast but possibly uneven.
* split-vector: uses the splitVector command to generate partitions for non-sharded
collections which is fast and even. The splitVector permission is required.
* sharded: reads config.chunks (MongoDB splits a sharded collection into chunks, and the
range of the chunks are stored within the collection) as the partitions directly. The
sharded strategy only used for sharded collection which is fast and even. Read permission
of config database is required.
* default: uses sharded strategy for sharded collections otherwise using split vector
strategy.
`single`
`sample`
`split-vector`
`sharded`
`config.chunks`
`default`

### Lookup Cache#


MongoDB connector can be used in temporal join as a lookup source (aka. dimension table).
Currently, only sync lookup mode is supported.


By default, lookup cache is not enabled. You can enable it by setting lookup.cache to PARTIAL.

`lookup.cache`
`PARTIAL`

The lookup cache is used to improve performance of temporal join the MongoDB connector.
By default, lookup cache is not enabled, so all the requests are sent to external database.
When lookup cache is enabled, each process (i.e. TaskManager) will hold a cache.
Flink will lookup the cache first, and only send requests to external database when cache missing,
and update cache with the rows returned.
The oldest rows in cache will be expired when the cache hit to the max cached rows
lookup.partial-cache.max-rows or when the row exceeds the max time to live specified by
lookup.partial-cache.expire-after-write or lookup.partial-cache.expire-after-access.
The cached rows might not be the latest, users can tune expiration options to a smaller value to
have a better fresh data, but this may increase the number of requests send to database.
So this is a balance between throughput and correctness.

`lookup.partial-cache.max-rows`
`lookup.partial-cache.expire-after-write`
`lookup.partial-cache.expire-after-access`

By default, flink will cache the empty query result for a Primary key, you can toggle the behaviour
by setting lookup.partial-cache.caching-missing-key to false.

`lookup.partial-cache.caching-missing-key`

### Idempotent Writes#


MongoDB sink will use upsert semantics rather than plain INSERT statements if primary key is defined
in DDL. We composite the primary key fields as the document _id which is the reserved primary key of
MongoDB. Use upsert mode to write rows into MongoDB, which provides idempotence.


If there are failures, the Flink job will recover and re-process from last successful checkpoint,
which can lead to re-processing messages during recovery. The upsert mode is highly recommended as
it helps avoid constraint violations or duplicate data if records need to be re-processed.


### Filters Pushdown#


MongoDB supports pushing down simple comparisons and logical filters to optimize queries.
The mappings from Flink SQL filters to MongoDB query operators are listed in the following table.

`=`
`$eq`
`<>`
`$ne`
`>`
`$gt`
`>=`
`$gte`
`<`
`$lt`
`<=`
`$lte`
`IS NULL`
`$eq : null`
`IS NOT NULL`
`$ne : null`
`OR`
`$or`
`AND`
`$and`

## Data Type Mapping#


The field data type mappings from MongoDB BSON types to Flink SQL data types are listed in the following table.

`ObjectId`
`STRING`
`String`
`STRING`
`Boolean`
`BOOLEAN`
`Binary`
`BINARY`
`VARBINARY`
`Int32`
`INTEGER`
`-`
`TINYINT`
`SMALLINT`
`FLOAT`
`Int64`
`BIGINT`
`Double`
`DOUBLE`
`Decimal128`
`DECIMAL`
`DateTime`
`TIMESTAMP_LTZ(3)`
`Timestamp`
`TIMESTAMP_LTZ(0)`
`Object`
`ROW`
`Array`
`ARRAY`

For specific types in MongoDB, we use Extended JSON format
to map them to Flink SQL STRING type.

`Symbol`
`{"_value": {"$symbol": "12"}}`
`RegularExpression`
`{"_value": {"$regularExpression": {"pattern": "^9$", "options": "i"}}}`
`JavaScript`
`{"_value": {"$code": "function() { return 10; }"}}`
`DbPointer`
`{"_value": {"$dbPointer": {"$ref": "db.coll", "$id": {"$oid": "63932a00da01604af329e33c"}}}}`

 Back to top
