# Orc


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Orc Format#



Format: Serialization Schema
Format: Deserialization Schema


The Apache Orc format allows to read and write Orc data.


## Dependencies#


In order to use the ORC format the following
dependencies are required for both projects using a build automation tool (such as Maven or SBT)
and SQL Client with SQL JAR bundles.


```
&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-orc</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>
```

`&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-orc</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>`

## How to create a table with Orc format#


Here is an example to create a table using Filesystem connector and Orc format.


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
 'format' = 'orc'
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
 'format' = 'orc'
)
`

## Format Options#


##### format


Orc format also supports table properties from Table properties.
For example, you can configure orc.compress=SNAPPY to enable snappy compression.

`orc.compress=SNAPPY`

## Data Type Mapping#


Orc format type mapping is compatible with Apache Hive.
The following table lists the type mapping from Flink type to Orc type.
