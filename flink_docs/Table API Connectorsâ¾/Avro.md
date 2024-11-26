# Avro


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Avro Format#



Format: Serialization Schema
Format: Deserialization Schema


The Apache Avro format allows to read and write Avro data based on an Avro schema. Currently, the Avro schema is derived from table schema.


## Dependencies#


In order to use the Avro format the following
dependencies are required for both projects using a build automation tool (such as Maven or SBT)
and SQL Client with SQL JAR bundles.


```
&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-avro</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>
```

`&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-avro</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>`

## How to create a table with Avro format#


Here is an example to create a table using Kafka connector and Avro format.


```
CREATE TABLE user_behavior (
  user_id BIGINT,
  item_id BIGINT,
  category_id BIGINT,
  behavior STRING,
  ts TIMESTAMP(3)
) WITH (
 'connector' = 'kafka',
 'topic' = 'user_behavior',
 'properties.bootstrap.servers' = 'localhost:9092',
 'properties.group.id' = 'testGroup',
 'format' = 'avro'
)

```

`CREATE TABLE user_behavior (
  user_id BIGINT,
  item_id BIGINT,
  category_id BIGINT,
  behavior STRING,
  ts TIMESTAMP(3)
) WITH (
 'connector' = 'kafka',
 'topic' = 'user_behavior',
 'properties.bootstrap.servers' = 'localhost:9092',
 'properties.group.id' = 'testGroup',
 'format' = 'avro'
)
`

## Format Options#


##### format

`'avro'`

##### avro.encoding

`binary`
`json`

##### avro.codec


##### timestamp_mapping.legacy


## Data Type Mapping#


Currently, the Avro schema is always derived from table schema. Explicitly defining an Avro schema is not supported yet.
So the following table lists the type mapping from Flink type to Avro type.

`BOOLEAN`
`boolean`
`BINARY / VARBINARY`
`bytes`
`DECIMAL`
`fixed`
`decimal`
`TINYINT`
`int`
`SMALLINT`
`int`
`INT`
`int`
`BIGINT`
`long`
`FLOAT`
`float`
`DOUBLE`
`double`
`DATE`
`int`
`date`
`TIME`
`int`
`time-millis`
`TIMESTAMP`
`long`
`timestamp-millis`
`ARRAY`
`array`
`MAP`
`map`
`MULTISET`
`map`
`ROW`
`record`

In addition to the types listed above, Flink supports reading/writing nullable types. Flink maps nullable types to Avro union(something, null), where something is the Avro type converted from Flink type.

`union(something, null)`
`something`

You can refer to Avro Specification for more information about Avro types.
