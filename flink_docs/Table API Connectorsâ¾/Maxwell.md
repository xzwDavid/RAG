# Maxwell


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Maxwell Format#



Changelog-Data-Capture Format
Format: Serialization Schema
Format: Deserialization Schema


Maxwell is a CDC (Changelog Data Capture) tool that can stream changes in real-time from MySQL into Kafka, Kinesis and other streaming connectors. Maxwell provides a unified format schema for changelog and supports to serialize messages using JSON.


Flink supports to interpret Maxwell JSON messages as INSERT/UPDATE/DELETE messages into Flink SQL system. This is useful in many cases to leverage this feature, such as

* synchronizing incremental data from databases to other systems
* auditing logs
* real-time materialized views on databases
* temporal join changing history of a database table and so on.

Flink also supports to encode the INSERT/UPDATE/DELETE messages in Flink SQL as Maxwell JSON messages, and emit to external systems like Kafka.
However, currently Flink can’t combine UPDATE_BEFORE and UPDATE_AFTER into a single UPDATE message. Therefore, Flink encodes UPDATE_BEFORE and UDPATE_AFTER as DELETE and INSERT Maxwell messages.


## Dependencies#


In order to use the Maxwell format the following
dependencies are required for both projects using a build automation tool (such as Maven or SBT)
and SQL Client with SQL JAR bundles.


```
&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-json</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>
```

`&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-json</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>`

Note: please refer to Maxwell documentation about how to synchronize changelog to Kafka topics with Maxwell JSON.


## How to use Maxwell format#


Maxwell provides a unified format for changelog, here is a simple example for an update operation captured from a MySQL products table in JSON format:

`products`

```
{
   "database":"test",
   "table":"e",
   "type":"insert",
   "ts":1477053217,
   "xid":23396,
   "commit":true,
   "position":"master.000006:800911",
   "server_id":23042,
   "thread_id":108,
   "primary_key": [1, "2016-10-21 05:33:37.523000"],
   "primary_key_columns": ["id", "c"],
   "data":{
     "id":111,
     "name":"scooter",
     "description":"Big 2-wheel scooter",
     "weight":5.15
   },
   "old":{
     "weight":5.18,
   }
}

```

`{
   "database":"test",
   "table":"e",
   "type":"insert",
   "ts":1477053217,
   "xid":23396,
   "commit":true,
   "position":"master.000006:800911",
   "server_id":23042,
   "thread_id":108,
   "primary_key": [1, "2016-10-21 05:33:37.523000"],
   "primary_key_columns": ["id", "c"],
   "data":{
     "id":111,
     "name":"scooter",
     "description":"Big 2-wheel scooter",
     "weight":5.15
   },
   "old":{
     "weight":5.18,
   }
}
`

Note: please refer to Maxwell documentation about the meaning of each fields.


The MySQL products table has 4 columns (id, name, description and weight). The above JSON message is an update change event on the products table where the weight value of the row with id = 111 is changed from 5.18 to 5.15.
Assuming this messages is synchronized to Kafka topic products_binlog, then we can use the following DDL to consume this topic and interpret the change events.

`products`
`id`
`name`
`description`
`weight`
`products`
`weight`
`id = 111`
`5.18`
`5.15`
`products_binlog`

```
CREATE TABLE topic_products (
  -- schema is totally the same to the MySQL "products" table
  id BIGINT,
  name STRING,
  description STRING,
  weight DECIMAL(10, 2)
) WITH (
 'connector' = 'kafka',
 'topic' = 'products_binlog',
 'properties.bootstrap.servers' = 'localhost:9092',
 'properties.group.id' = 'testGroup',
 'format' = 'maxwell-json'
)

```

`CREATE TABLE topic_products (
  -- schema is totally the same to the MySQL "products" table
  id BIGINT,
  name STRING,
  description STRING,
  weight DECIMAL(10, 2)
) WITH (
 'connector' = 'kafka',
 'topic' = 'products_binlog',
 'properties.bootstrap.servers' = 'localhost:9092',
 'properties.group.id' = 'testGroup',
 'format' = 'maxwell-json'
)
`

After registering the topic as a Flink table, then you can consume the Maxwell messages as a changelog source.


```
-- a real-time materialized view on the MySQL "products"
-- which calculate the latest average of weight for the same products
SELECT name, AVG(weight) FROM topic_products GROUP BY name;

-- synchronize all the data and incremental changes of MySQL "products" table to
-- Elasticsearch "products" index for future searching
INSERT INTO elasticsearch_products
SELECT * FROM topic_products;

```

`-- a real-time materialized view on the MySQL "products"
-- which calculate the latest average of weight for the same products
SELECT name, AVG(weight) FROM topic_products GROUP BY name;

-- synchronize all the data and incremental changes of MySQL "products" table to
-- Elasticsearch "products" index for future searching
INSERT INTO elasticsearch_products
SELECT * FROM topic_products;
`

## Available Metadata#


The following format metadata can be exposed as read-only (VIRTUAL) columns in a table definition.

`VIRTUAL`

> 
  Format metadata fields are only available if the
corresponding connector forwards format metadata. Currently, only the Kafka connector is able to expose
metadata fields for its value format.


`database`
`STRING NULL`
`database`
`table`
`STRING NULL`
`table`
`primary-key-columns`
`ARRAY<STRING> NULL`
`primary_key_columns`
`ingestion-timestamp`
`TIMESTAMP_LTZ(3) NULL`
`ts`

The following example shows how to access Maxwell metadata fields in Kafka:


```
CREATE TABLE KafkaTable (
  origin_database STRING METADATA FROM 'value.database' VIRTUAL,
  origin_table STRING METADATA FROM 'value.table' VIRTUAL,
  origin_primary_key_columns ARRAY<STRING> METADATA FROM 'value.primary-key-columns' VIRTUAL,
  origin_ts TIMESTAMP(3) METADATA FROM 'value.ingestion-timestamp' VIRTUAL,
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'maxwell-json'
);

```

`CREATE TABLE KafkaTable (
  origin_database STRING METADATA FROM 'value.database' VIRTUAL,
  origin_table STRING METADATA FROM 'value.table' VIRTUAL,
  origin_primary_key_columns ARRAY<STRING> METADATA FROM 'value.primary-key-columns' VIRTUAL,
  origin_ts TIMESTAMP(3) METADATA FROM 'value.ingestion-timestamp' VIRTUAL,
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'maxwell-json'
);
`

## Format Options#


##### format

`'maxwell-json'`

##### maxwell-json.ignore-parse-errors


##### maxwell-json.timestamp-format.standard

`'SQL'`
`'SQL'`
`'ISO-8601'`
* Option 'SQL' will parse input timestamp in "yyyy-MM-dd HH:mm:ss.s{precision}" format, e.g '2020-12-30 12:13:14.123' and output timestamp in the same format.
* Option 'ISO-8601'will parse input timestamp in "yyyy-MM-ddTHH:mm:ss.s{precision}" format, e.g '2020-12-30T12:13:14.123' and output timestamp in the same format.
`'SQL'`
`'ISO-8601'`

##### maxwell-json.map-null-key.mode

`'FAIL'`
`'FAIL'`
`'DROP'`
`'LITERAL'`
* Option 'FAIL' will throw exception when encountering map with null key.
* Option 'DROP' will drop null key entries for map data.
* Option 'LITERAL' will replace null key with string literal. The string literal is defined by maxwell-json.map-null-key.literal option.
`'FAIL'`
`'DROP'`
`'LITERAL'`
`maxwell-json.map-null-key.literal`

##### maxwell-json.map-null-key.literal

`'maxwell-json.map-null-key.mode'`

##### maxwell-json.encode.decimal-as-plain-number

`0.000000027`
`2.7E-8`
`0.000000027`

##### maxwell-json.encode.ignore-null-fields


## Caveats#


### Duplicate change events#


The Maxwell application allows to deliver every change event exactly-once. Flink works pretty well when consuming Maxwell produced events in this situation.
If Maxwell application works in at-least-once delivery, it may deliver duplicate change events to Kafka and Flink will get the duplicate events.
This may cause Flink query to get wrong results or unexpected exceptions. Thus, it is recommended to set job configuration table.exec.source.cdc-events-duplicate to true and define PRIMARY KEY on the source in this situation.
Framework will generate an additional stateful operator, and use the primary key to deduplicate the change events and produce a normalized changelog stream.

`table.exec.source.cdc-events-duplicate`
`true`

## Data Type Mapping#


Currently, the Maxwell format uses JSON for serialization and deserialization. Please refer to JSON Format documentation for more details about the data type mapping.
