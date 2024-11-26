# Debezium


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Debezium Format#



Changelog-Data-Capture Format
Format: Serialization Schema
Format: Deserialization Schema


Debezium is a CDC (Changelog Data Capture) tool that can stream changes in real-time from MySQL, PostgreSQL, Oracle, Microsoft SQL Server and many other databases into Kafka. Debezium provides a unified format schema for changelog and supports to serialize messages using JSON and Apache Avro.


Flink supports to interpret Debezium JSON and Avro messages as INSERT/UPDATE/DELETE messages into Flink SQL system. This is useful in many cases to leverage this feature, such as

* synchronizing incremental data from databases to other systems
* auditing logs
* real-time materialized views on databases
* temporal join changing history of a database table and so on.

Flink also supports to encode the INSERT/UPDATE/DELETE messages in Flink SQL as Debezium JSON or Avro messages, and emit to external systems like Kafka.
However, currently Flink can’t combine UPDATE_BEFORE and UPDATE_AFTER into a single UPDATE message. Therefore, Flink encodes UPDATE_BEFORE and UDPATE_AFTER as DELETE and INSERT Debezium messages.


## Dependencies#


#### Debezium Confluent Avro#


In order to use the Debezium format the following
dependencies are required for both projects using a build automation tool (such as Maven or SBT)
and SQL Client with SQL JAR bundles.


```
&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-avro-confluent-registry</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>
```

`&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-avro-confluent-registry</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>`

#### Debezium Json#


In order to use the Debezium format the following
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

Note: please refer to Debezium documentation about how to setup a Debezium Kafka Connect to synchronize changelog to Kafka topics.


## How to use Debezium format#


Debezium provides a unified format for changelog, here is a simple example for an update operation captured from a MySQL products table in JSON format:

`products`

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
  "source": {...},
  "op": "u",
  "ts_ms": 1589362330904,
  "transaction": null
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
  "source": {...},
  "op": "u",
  "ts_ms": 1589362330904,
  "transaction": null
}
`

Note: please refer to Debezium documentation about the meaning of each fields.


The MySQL products table has 4 columns (id, name, description and weight). The above JSON message is an update change event on the products table where the weight value of the row with id = 111 is changed from 5.18 to 5.15.
Assuming this messages is synchronized to Kafka topic products_binlog, then we can use the following DDLs (for Debezium JSON and Debezium Confluent Avro) to consume this topic and interpret the change events.

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

#### Debezium JSON DDL#


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
 -- using 'debezium-json' as the format to interpret Debezium JSON messages
 'format' = 'debezium-json'
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
 -- using 'debezium-json' as the format to interpret Debezium JSON messages
 'format' = 'debezium-json'
)
`

In some cases, users may setup the Debezium Kafka Connect with the Kafka configuration 'value.converter.schemas.enable' enabled to include schema in the message. Then the Debezium JSON message may look like this:

`'value.converter.schemas.enable'`

```
{
  "schema": {...},
  "payload": {
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
    "source": {...},
    "op": "u",
    "ts_ms": 1589362330904,
    "transaction": null
  }
}

```

`{
  "schema": {...},
  "payload": {
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
    "source": {...},
    "op": "u",
    "ts_ms": 1589362330904,
    "transaction": null
  }
}
`

In order to interpret such messages, you need to add the option 'debezium-json.schema-include' = 'true' into above DDL WITH clause (false by default). Usually, this is not recommended to include schema because this makes the messages very verbose and reduces parsing performance.

`'debezium-json.schema-include' = 'true'`
`false`

#### Debezium Confluent Avro DDL#


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
 -- using 'debezium-avro-confluent' as the format to interpret Debezium Avro messages
 'format' = 'debezium-avro-confluent',
 -- the URL to the schema registry for Kafka
 'debezium-avro-confluent.url' = 'http://localhost:8081'
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
 -- using 'debezium-avro-confluent' as the format to interpret Debezium Avro messages
 'format' = 'debezium-avro-confluent',
 -- the URL to the schema registry for Kafka
 'debezium-avro-confluent.url' = 'http://localhost:8081'
)
`

#### Producing Results#


For every data format, after registering the topic as a Flink table, you can consume the Debezium messages as a changelog source.


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

Attention Format metadata fields are only available if the
corresponding connector forwards format metadata. Currently, only the Kafka connector is able to expose
metadata fields for its value format.

`schema`
`STRING NULL`
`ingestion-timestamp`
`TIMESTAMP_LTZ(3) NULL`
`ts_ms`
`source.timestamp`
`TIMESTAMP_LTZ(3) NULL`
`source.ts_ms`
`source.database`
`STRING NULL`
`source.db`
`source.schema`
`STRING NULL`
`source.schema`
`source.table`
`STRING NULL`
`source.table`
`source.collection`
`source.properties`
`MAP<STRING, STRING> NULL`
`source`

The following example shows how to access Debezium metadata fields in Kafka:


```
CREATE TABLE KafkaTable (
  origin_ts TIMESTAMP(3) METADATA FROM 'value.ingestion-timestamp' VIRTUAL,
  event_time TIMESTAMP(3) METADATA FROM 'value.source.timestamp' VIRTUAL,
  origin_database STRING METADATA FROM 'value.source.database' VIRTUAL,
  origin_schema STRING METADATA FROM 'value.source.schema' VIRTUAL,
  origin_table STRING METADATA FROM 'value.source.table' VIRTUAL,
  origin_properties MAP<STRING, STRING> METADATA FROM 'value.source.properties' VIRTUAL,
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'debezium-json'
);

```

`CREATE TABLE KafkaTable (
  origin_ts TIMESTAMP(3) METADATA FROM 'value.ingestion-timestamp' VIRTUAL,
  event_time TIMESTAMP(3) METADATA FROM 'value.source.timestamp' VIRTUAL,
  origin_database STRING METADATA FROM 'value.source.database' VIRTUAL,
  origin_schema STRING METADATA FROM 'value.source.schema' VIRTUAL,
  origin_table STRING METADATA FROM 'value.source.table' VIRTUAL,
  origin_properties MAP<STRING, STRING> METADATA FROM 'value.source.properties' VIRTUAL,
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'debezium-json'
);
`

## Format Options#


Flink provides debezium-avro-confluent and debezium-json formats to interpret Avro or JSON messages produced by Debezium.
Use format debezium-avro-confluent to interpret Debezium Avro messages and format debezium-json to interpret Debezium JSON messages.

`debezium-avro-confluent`
`debezium-json`
`debezium-avro-confluent`
`debezium-json`

##### format

`'debezium-avro-confluent'`

##### debezium-avro-confluent.basic-auth.credentials-source


##### debezium-avro-confluent.basic-auth.user-info


##### debezium-avro-confluent.bearer-auth.credentials-source


##### debezium-avro-confluent.bearer-auth.token


##### debezium-avro-confluent.properties


##### debezium-avro-confluent.ssl.keystore.location


##### debezium-avro-confluent.ssl.keystore.password


##### debezium-avro-confluent.ssl.truststore.location


##### debezium-avro-confluent.ssl.truststore.password


##### debezium-avro-confluent.schema


##### debezium-avro-confluent.subject


##### debezium-avro-confluent.url


##### format

`'debezium-json'`

##### debezium-json.schema-include

`'value.converter.schemas.enable'`

##### debezium-json.ignore-parse-errors


##### debezium-json.timestamp-format.standard

`'SQL'`
`'SQL'`
`'ISO-8601'`
* Option 'SQL' will parse input timestamp in "yyyy-MM-dd HH:mm:ss.s{precision}" format, e.g '2020-12-30 12:13:14.123' and output timestamp in the same format.
* Option 'ISO-8601'will parse input timestamp in "yyyy-MM-ddTHH:mm:ss.s{precision}" format, e.g '2020-12-30T12:13:14.123' and output timestamp in the same format.
`'SQL'`
`'ISO-8601'`

##### debezium-json.map-null-key.mode

`'FAIL'`
`'FAIL'`
`'DROP'`
`'LITERAL'`
* Option 'FAIL' will throw exception when encountering map with null key.
* Option 'DROP' will drop null key entries for map data.
* Option 'LITERAL' will replace null key with string literal. The string literal is defined by debezium-json.map-null-key.literal option.
`'FAIL'`
`'DROP'`
`'LITERAL'`
`debezium-json.map-null-key.literal`

##### debezium-json.map-null-key.literal

`'debezium-json.map-null-key.mode'`

##### debezium-json.encode.decimal-as-plain-number

`0.000000027`
`2.7E-8`
`0.000000027`

##### debezium-json.encode.ignore-null-fields


## Caveats#


### Duplicate change events#


Under normal operating scenarios, the Debezium application delivers every change event exactly-once. Flink works pretty well when consuming Debezium produced events in this situation.
However, Debezium application works in at-least-once delivery if any failover happens. See more details about delivery guarantee from Debezium documentation.
That means, in the abnormal situations, Debezium may deliver duplicate change events to Kafka and Flink will get the duplicate events.
This may cause Flink query to get wrong results or unexpected exceptions. Thus, it is recommended to set job configuration table.exec.source.cdc-events-duplicate to true and define PRIMARY KEY on the source in this situation.
Framework will generate an additional stateful operator, and use the primary key to deduplicate the change events and produce a normalized changelog stream.

`table.exec.source.cdc-events-duplicate`
`true`

### Consuming data produced by Debezium Postgres Connector#


If you are using Debezium Connector for PostgreSQL to capture the changes to Kafka, please make sure the REPLICA IDENTITY configuration of the monitored PostgreSQL table has been set to FULL which is by default DEFAULT.
Otherwise, Flink SQL currently will fail to interpret the Debezium data.

`FULL`
`DEFAULT`

In FULL strategy, the UPDATE and DELETE events will contain the previous values of all the tableâs columns. In other strategies, the “before” field of UPDATE and DELETE events will only contain primary key columns or null if no primary key.
You can change the REPLICA IDENTITY by running ALTER TABLE <your-table-name> REPLICA IDENTITY FULL.
See more details in Debezium Documentation for PostgreSQL REPLICA IDENTITY.

`FULL`
`REPLICA IDENTITY`
`ALTER TABLE <your-table-name> REPLICA IDENTITY FULL`

## Data Type Mapping#


Currently, the Debezium format uses JSON and Avro format for serialization and deserialization. Please refer to JSON Format documentation and [Confluent Avro Format documentation]({< ref “docs/connectors/table/formats/avro-confluent” >}}#data-type-mapping) for more details about the data type mapping.
