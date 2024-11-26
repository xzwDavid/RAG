# Parquet


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Parquet Format#



Format: Serialization Schema
Format: Deserialization Schema


The Apache Parquet format allows to read and write Parquet data.


## Dependencies#


In order to use the Parquet format the following
dependencies are required for both projects using a build automation tool (such as Maven or SBT)
and SQL Client with SQL JAR bundles.


```
&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-parquet</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>
```

`&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-parquet</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>`

## How to create a table with Parquet format#


Here is an example to create a table using Filesystem connector and Parquet format.


```
CREATE TABLE user_behavior (
  user_id BIGINT,
  item_id BIGINT,
  category_id BIGINT,
  behavior STRING,
  ts TIMESTAMP(3),
  dt STRING
) PARTITIONED BY (dt) WITH (
 'connector' = 'filesystem',
 'path' = '/tmp/user_behavior',
 'format' = 'parquet'
)

```

`CREATE TABLE user_behavior (
  user_id BIGINT,
  item_id BIGINT,
  category_id BIGINT,
  behavior STRING,
  ts TIMESTAMP(3),
  dt STRING
) PARTITIONED BY (dt) WITH (
 'connector' = 'filesystem',
 'path' = '/tmp/user_behavior',
 'format' = 'parquet'
)
`

## Format Options#


##### format


##### parquet.utc-timezone


##### timestamp.time.unit


##### write.int64.timestamp


Parquet format also supports configuration from ParquetOutputFormat.
For example, you can configure parquet.compression=GZIP to enable gzip compression.

`parquet.compression=GZIP`

## Data Type Mapping#


Currently, Parquet format type mapping is compatible with Apache Hive, but by default not with Apache Spark:

* Timestamp: mapping timestamp type to int96 whatever the precision is.
* Spark compatibility requires int64 via config option write.int64.timestamp (see above).
* Decimal: mapping decimal type to fixed length byte array according to the precision.
`write.int64.timestamp`

The following table lists the type mapping from Flink type to Parquet type.
