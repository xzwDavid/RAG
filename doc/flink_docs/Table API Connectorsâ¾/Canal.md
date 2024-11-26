# Canal


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Canal Format#



Changelog-Data-Capture Format
Format: Serialization Schema
Format: Deserialization Schema


Canal is a CDC (Changelog Data Capture) tool that can stream changes in real-time from MySQL into other systems. Canal provides a unified format schema for changelog and supports to serialize messages using JSON and protobuf (protobuf is the default format for Canal).


Flink supports to interpret Canal JSON messages as INSERT/UPDATE/DELETE messages into Flink SQL system. This is useful in many cases to leverage this feature, such as

* synchronizing incremental data from databases to other systems
* auditing logs
* real-time materialized views on databases
* temporal join changing history of a database table and so on.

Flink also supports to encode the INSERT/UPDATE/DELETE messages in Flink SQL as Canal JSON messages, and emit to storage like Kafka.
However, currently Flink can’t combine UPDATE_BEFORE and UPDATE_AFTER into a single UPDATE message. Therefore, Flink encodes UPDATE_BEFORE and UPDATE_AFTER as DELETE and INSERT Canal messages.


Note: Support for interpreting Canal protobuf messages is on the roadmap.


## Dependencies#


In order to use the Canal format the following
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

Note: please refer to Canal documentation about how to deploy Canal to synchronize changelog to message queues.


## How to use Canal format#


Canal provides a unified format for changelog, here is a simple example for an update operation captured from a MySQL products table:

`products`

```
{
  "data": [
    {
      "id": "111",
      "name": "scooter",
      "description": "Big 2-wheel scooter",
      "weight": "5.18"
    }
  ],
  "database": "inventory",
  "es": 1589373560000,
  "id": 9,
  "isDdl": false,
  "mysqlType": {
    "id": "INTEGER",
    "name": "VARCHAR(255)",
    "description": "VARCHAR(512)",
    "weight": "FLOAT"
  },
  "old": [
    {
      "weight": "5.15"
    }
  ],
  "pkNames": [
    "id"
  ],
  "sql": "",
  "sqlType": {
    "id": 4,
    "name": 12,
    "description": 12,
    "weight": 7
  },
  "table": "products",
  "ts": 1589373560798,
  "type": "UPDATE"
}

```

`{
  "data": [
    {
      "id": "111",
      "name": "scooter",
      "description": "Big 2-wheel scooter",
      "weight": "5.18"
    }
  ],
  "database": "inventory",
  "es": 1589373560000,
  "id": 9,
  "isDdl": false,
  "mysqlType": {
    "id": "INTEGER",
    "name": "VARCHAR(255)",
    "description": "VARCHAR(512)",
    "weight": "FLOAT"
  },
  "old": [
    {
      "weight": "5.15"
    }
  ],
  "pkNames": [
    "id"
  ],
  "sql": "",
  "sqlType": {
    "id": 4,
    "name": 12,
    "description": 12,
    "weight": 7
  },
  "table": "products",
  "ts": 1589373560798,
  "type": "UPDATE"
}
`

Note: please refer to Canal documentation about the meaning of each fields.


The MySQL products table has 4 columns (id, name, description and weight). The above JSON message is an update change event on the products table where the weight value of the row with id = 111 is changed from 5.18 to 5.15.
Assuming the messages have been synchronized to Kafka topic products_binlog, then we can use the following DDL to consume this topic and interpret the change events.

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
 'format' = 'canal-json'  -- using canal-json as the format
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
 'format' = 'canal-json'  -- using canal-json as the format
)
`

After registering the topic as a Flink table, you can consume the Canal messages as a changelog source.


```
-- a real-time materialized view on the MySQL "products"
-- which calculates the latest average of weight for the same products
SELECT name, AVG(weight) FROM topic_products GROUP BY name;

-- synchronize all the data and incremental changes of MySQL "products" table to
-- Elasticsearch "products" index for future searching
INSERT INTO elasticsearch_products
SELECT * FROM topic_products;

```

`-- a real-time materialized view on the MySQL "products"
-- which calculates the latest average of weight for the same products
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
`sql-type`
`MAP<STRING, INT> NULL`
`sqlType`
`pk-names`
`ARRAY<STRING> NULL`
`pkNames`
`ingestion-timestamp`
`TIMESTAMP_LTZ(3) NULL`
`ts`

The following example shows how to access Canal metadata fields in Kafka:


```
CREATE TABLE KafkaTable (
  origin_database STRING METADATA FROM 'value.database' VIRTUAL,
  origin_table STRING METADATA FROM 'value.table' VIRTUAL,
  origin_sql_type MAP<STRING, INT> METADATA FROM 'value.sql-type' VIRTUAL,
  origin_pk_names ARRAY<STRING> METADATA FROM 'value.pk-names' VIRTUAL,
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
  'value.format' = 'canal-json'
);

```

`CREATE TABLE KafkaTable (
  origin_database STRING METADATA FROM 'value.database' VIRTUAL,
  origin_table STRING METADATA FROM 'value.table' VIRTUAL,
  origin_sql_type MAP<STRING, INT> METADATA FROM 'value.sql-type' VIRTUAL,
  origin_pk_names ARRAY<STRING> METADATA FROM 'value.pk-names' VIRTUAL,
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
  'value.format' = 'canal-json'
);
`

## Format Options#


##### format

`'canal-json'`

##### canal-json.ignore-parse-errors


##### canal-json.timestamp-format.standard

`'SQL'`
`'SQL'`
`'ISO-8601'`
* Option 'SQL' will parse input timestamp in "yyyy-MM-dd HH:mm:ss.s{precision}" format, e.g '2020-12-30 12:13:14.123' and output timestamp in the same format.
* Option 'ISO-8601' will parse input timestamp in "yyyy-MM-ddTHH:mm:ss.s{precision}" format, e.g '2020-12-30T12:13:14.123' and output timestamp in the same format.
`'SQL'`
`'ISO-8601'`

##### canal-json.map-null-key.mode

`'FAIL'`
`'FAIL'`
`'DROP'`
`'LITERAL'`
* Option 'FAIL' will throw exception when encountering map value with null key.
* Option 'DROP' will drop null key entries for map data.
* Option 'LITERAL' will replace null key with string literal. The string literal is defined by canal-json.map-null-key.literal option.
`'FAIL'`
`'DROP'`
`'LITERAL'`
`canal-json.map-null-key.literal`

##### canal-json.map-null-key.literal

`'canal-json.map-null-key.mode'`

##### canal-json.encode.decimal-as-plain-number

`0.000000027`
`2.7E-8`
`0.000000027`

##### canal-json.database.include


##### canal-json.table.include


## Caveats#


### Duplicate change events#


Under normal operating scenarios, the Canal application delivers every change event exactly-once. Flink works pretty well when consuming Canal produced events in this situation.
However, Canal application works in at-least-once delivery if any failover happens.
That means, in the abnormal situations, Canal may deliver duplicate change events to message queues and Flink will get the duplicate events.
This may cause Flink query to get wrong results or unexpected exceptions. Thus, it is recommended to set job configuration table.exec.source.cdc-events-duplicate to true and define PRIMARY KEY on the source in this situation.
Framework will generate an additional stateful operator, and use the primary key to deduplicate the change events and produce a normalized changelog stream.

`table.exec.source.cdc-events-duplicate`
`true`

## Data Type Mapping#


Currently, the Canal format uses JSON format for serialization and deserialization. Please refer to JSON format documentation for more details about the data type mapping.
