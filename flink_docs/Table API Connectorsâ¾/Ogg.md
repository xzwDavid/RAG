# Ogg


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Ogg Format#



Changelog-Data-Capture Format
Format: Serialization Schema
Format: Deserialization Schema


Oracle GoldenGate (a.k.a ogg) is a managed service
providing a real-time data mesh platform, which uses replication to keep data highly available, and
enabling real-time analysis. Customers can design, execute, and monitor their data replication and
stream data processing solutions without the need to allocate or manage compute environments. Ogg
provides a format schema for changelog and supports to serialize messages using JSON.


Flink supports to interpret Ogg JSON as INSERT/UPDATE/DELETE messages into Flink SQL system. This is
useful in many cases to leverage this feature, such as

* synchronizing incremental data from databases to other systems
* auditing logs
* real-time materialized views on databases
* temporal join changing history of a database table and so on.

Flink also supports to encode the INSERT/UPDATE/DELETE messages in Flink SQL as Ogg JSON, and emit
to external systems like Kafka. However, currently Flink can’t combine UPDATE_BEFORE and
UPDATE_AFTER into a single UPDATE message. Therefore, Flink encodes UPDATE_BEFORE and UPDATE_AFTER
as DELETE and INSERT Ogg messages.


## Dependencies#


#### Ogg Json#


In order to use the Ogg  the following
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

Note: please refer
to Ogg Kafka Handler documentation
about how to set up an Ogg Kafka handler to synchronize changelog to Kafka topics.


## How to use Ogg format#


Ogg provides a unified format for changelog, here is a simple example for an update operation
captured from an Oracle PRODUCTS table in JSON format:

`PRODUCTS`

```
{
  "before": {
    "id": 111,
    "name": "scooter",
    "description": "Big 2-wheel scooter",
    "weight": 5.18
  },
  "after": {
    "id": 111,
    "name": "scooter",
    "description": "Big 2-wheel scooter",
    "weight": 5.15
  },
  "op_type": "U",
  "op_ts": "2020-05-13 15:40:06.000000",
  "current_ts": "2020-05-13 15:40:07.000000",
  "primary_keys": [
    "id"
  ],
  "pos": "00000000000000000000143",
  "table": "PRODUCTS"
}

```

`{
  "before": {
    "id": 111,
    "name": "scooter",
    "description": "Big 2-wheel scooter",
    "weight": 5.18
  },
  "after": {
    "id": 111,
    "name": "scooter",
    "description": "Big 2-wheel scooter",
    "weight": 5.15
  },
  "op_type": "U",
  "op_ts": "2020-05-13 15:40:06.000000",
  "current_ts": "2020-05-13 15:40:07.000000",
  "primary_keys": [
    "id"
  ],
  "pos": "00000000000000000000143",
  "table": "PRODUCTS"
}
`

Note: please refer
to Debezium documentation
about the meaning of each field.


The Oracle PRODUCTS table has 4 columns (id, name, description and weight). The above JSON
message is an update change event on the PRODUCTS table where the weight value of the row
with id = 111 is changed from 5.18 to 5.15. Assuming this messages is synchronized to Kafka
topic products_ogg, then we can use the following DDL to consume this topic and interpret the
change events.

`PRODUCTS`
`id`
`name`
`description`
`weight`
`PRODUCTS`
`weight`
`id = 111`
`5.18`
`5.15`
`products_ogg`

```
CREATE TABLE topic_products (
  -- schema is totally the same to the Oracle "products" table
  id BIGINT,
  name STRING,
  description STRING,
  weight DECIMAL(10, 2)
) WITH (
  'connector' = 'kafka',
  'topic' = 'products_ogg',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'format' = 'ogg-json'
)

```

`CREATE TABLE topic_products (
  -- schema is totally the same to the Oracle "products" table
  id BIGINT,
  name STRING,
  description STRING,
  weight DECIMAL(10, 2)
) WITH (
  'connector' = 'kafka',
  'topic' = 'products_ogg',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'format' = 'ogg-json'
)
`

After registering the topic as a Flink table, then you can consume the Ogg messages as a changelog
source.


```
-- a real-time materialized view on the Oracle "PRODUCTS"
-- which calculate the latest average of weight for the same products
SELECT name, AVG(weight)
FROM topic_products
GROUP BY name;

-- synchronize all the data and incremental changes of Oracle "PRODUCTS" table to
-- Elasticsearch "products" index for future searching
INSERT INTO elasticsearch_products
SELECT *
FROM topic_products;

```

`-- a real-time materialized view on the Oracle "PRODUCTS"
-- which calculate the latest average of weight for the same products
SELECT name, AVG(weight)
FROM topic_products
GROUP BY name;

-- synchronize all the data and incremental changes of Oracle "PRODUCTS" table to
-- Elasticsearch "products" index for future searching
INSERT INTO elasticsearch_products
SELECT *
FROM topic_products;
`

## Available Metadata#


The following format metadata can be exposed as read-only (VIRTUAL) columns in a table definition.

`VIRTUAL`

Attention Format metadata fields are only available if the
corresponding connector forwards format metadata. Currently, only the Kafka connector is able to
expose metadata fields for its value format.

`table`
`STRING NULL `
`primary-keys`
`ARRAY<STRING> NULL`
`ingestion-timestamp`
`TIMESTAMP_LTZ(6) NULL`
`event-timestamp`
`TIMESTAMP_LTZ(6) NULL`

The following example shows how to access Ogg metadata fields in Kafka:


```
CREATE TABLE KafkaTable (
  origin_ts TIMESTAMP(3) METADATA FROM 'value.ingestion-timestamp' VIRTUAL,
  event_time TIMESTAMP(3) METADATA FROM 'value.event-timestamp' VIRTUAL,
  origin_table STRING METADATA FROM 'value.table' VIRTUAL,
  primary_keys ARRAY<STRING> METADATA FROM 'value.primary-keys' VIRTUAL,
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'ogg-json'
);

```

`CREATE TABLE KafkaTable (
  origin_ts TIMESTAMP(3) METADATA FROM 'value.ingestion-timestamp' VIRTUAL,
  event_time TIMESTAMP(3) METADATA FROM 'value.event-timestamp' VIRTUAL,
  origin_table STRING METADATA FROM 'value.table' VIRTUAL,
  primary_keys ARRAY<STRING> METADATA FROM 'value.primary-keys' VIRTUAL,
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'ogg-json'
);
`

## Format Options#


##### format

`'ogg-json'`

##### ogg-json.ignore-parse-errors


##### ogg-json.timestamp-format.standard

`'SQL'`
`'ISO-8601'`
* Option 'SQL' will parse input timestamp in "yyyy-MM-dd HH:mm:ss.s{precision}" format, e.g '2020-12-30 12:13:14.123' and output timestamp in the same format.
* Option 'ISO-8601'will parse input timestamp in "yyyy-MM-ddTHH:mm:ss.s{precision}" format, e.g '2020-12-30T12:13:14.123' and output timestamp in the same format.
`'SQL'`
`'ISO-8601'`

##### ogg-json.map-null-key.mode

`'FAIL'`
`'FAIL'`
`'DROP'`
`'LITERAL'`
* Option 'FAIL' will throw exception when encountering map with null key.
* Option 'DROP' will drop null key entries for map data.
* Option 'LITERAL' will replace null key with string literal. The string literal is defined by ogg-json.map-null-key.literal option.
`'FAIL'`
`'DROP'`
`'LITERAL'`
`ogg-json.map-null-key.literal`

##### ogg-json.map-null-key.literal

`'ogg-json.map-null-key.mode'`

##### ogg-json.encode.ignore-null-fields


## Data Type Mapping#


Currently, the Ogg format uses JSON format for serialization and deserialization. Please refer
to JSON Format documentation for more details about the data type mapping.
