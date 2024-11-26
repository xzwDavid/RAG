# JSON


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# JSON Format#



Format: Serialization Schema
Format: Deserialization Schema


The JSON format allows to read and write JSON data based on an JSON schema. Currently, the JSON schema is derived from table schema.


The JSON format supports append-only streams, unless you’re using a connector that explicitly support retract streams and/or upsert streams like the Upsert Kafka connector. If you need to write retract streams and/or upsert streams, we suggest you to look at CDC JSON formats like Debezium JSON and Canal JSON.


## Dependencies#


In order to use the Json format the following
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

## How to create a table with JSON format#


Here is an example to create a table using Kafka connector and JSON format.


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
 'format' = 'json',
 'json.fail-on-missing-field' = 'false',
 'json.ignore-parse-errors' = 'true'
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
 'format' = 'json',
 'json.fail-on-missing-field' = 'false',
 'json.ignore-parse-errors' = 'true'
)
`

## Format Options#


##### format

`'json'`

##### json.fail-on-missing-field


##### json.ignore-parse-errors


##### json.timestamp-format.standard

`'SQL'`
`TIMESTAMP`
`TIMESTAMP_LTZ`
`'SQL'`
`'ISO-8601'`
* Option 'SQL' will parse input TIMESTAMP values in "yyyy-MM-dd HH:mm:ss.s{precision}" format, e.g "2020-12-30 12:13:14.123", 
        parse input TIMESTAMP_LTZ values in "yyyy-MM-dd HH:mm:ss.s{precision}'Z'" format, e.g "2020-12-30 12:13:14.123Z" and output timestamp in the same format.
* Option 'ISO-8601'will parse input TIMESTAMP in "yyyy-MM-ddTHH:mm:ss.s{precision}" format, e.g "2020-12-30T12:13:14.123" 
        parse input TIMESTAMP_LTZ in "yyyy-MM-ddTHH:mm:ss.s{precision}'Z'" format, e.g "2020-12-30T12:13:14.123Z" and output timestamp in the same format.
`'SQL'`
`'ISO-8601'`

##### json.map-null-key.mode

`'FAIL'`
`'FAIL'`
`'DROP'`
`'LITERAL'`
* Option 'FAIL' will throw exception when encountering map with null key.
* Option 'DROP' will drop null key entries for map data.
* Option 'LITERAL' will replace null key with string literal. The string literal is defined by json.map-null-key.literal option.
`'FAIL'`
`'DROP'`
`'LITERAL'`
`json.map-null-key.literal`

##### json.map-null-key.literal

`'json.map-null-key.mode'`

##### json.encode.decimal-as-plain-number

`0.000000027`
`2.7E-8`
`0.000000027`

##### json.encode.ignore-null-fields


##### decode.json-parser.enabled

`JsonParser`
`JsonParser`
`JsonNode`
`JsonParser`
`JsonNode`

## Data Type Mapping#


Currently, the JSON schema is always derived from table schema. Explicitly defining an JSON schema is not supported yet.


Flink JSON format uses jackson databind API to parse and generate JSON string.


The following table lists the type mapping from Flink type to JSON type.

`CHAR / VARCHAR / STRING`
`string`
`BOOLEAN`
`boolean`
`BINARY / VARBINARY`
`string with encoding: base64`
`DECIMAL`
`number`
`TINYINT`
`number`
`SMALLINT`
`number`
`INT`
`number`
`BIGINT`
`number`
`FLOAT`
`number`
`DOUBLE`
`number`
`DATE`
`string with format: date`
`TIME`
`string with format: time`
`TIMESTAMP`
`string with format: date-time`
`TIMESTAMP_WITH_LOCAL_TIME_ZONE`
`string with format: date-time (with UTC time zone)`
`INTERVAL`
`number`
`ARRAY`
`array`
`MAP / MULTISET`
`object`
`ROW`
`object`