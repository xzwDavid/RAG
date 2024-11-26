# CSV


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# CSV Format#



Format: Serialization Schema
Format: Deserialization Schema


The CSV format allows to read and write CSV data based on an CSV schema. Currently, the CSV schema is derived from table schema.


## Dependencies#


In order to use the CSV format the following
dependencies are required for both projects using a build automation tool (such as Maven or SBT)
and SQL Client with SQL JAR bundles.


```
&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-csv</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>
```

`&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-csv</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>`

## How to create a table with CSV format#


Here is an example to create a table using Kafka connector and CSV format.


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
 'format' = 'csv',
 'csv.ignore-parse-errors' = 'true',
 'csv.allow-comments' = 'true'
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
 'format' = 'csv',
 'csv.ignore-parse-errors' = 'true',
 'csv.allow-comments' = 'true'
)
`

## Format Options#


##### format

`'csv'`

##### csv.field-delimiter

`,`
`','`
`'\t'`
`'csv.field-delimiter' = U&'\0001'`
`0x01`

##### csv.disable-quote-character

`'csv.quote-character'`

##### csv.quote-character

`"`
`"`

##### csv.allow-comments

`'#'`

##### csv.ignore-parse-errors


##### csv.array-element-delimiter

`;`
`';'`

##### csv.escape-character


##### csv.null-literal


##### csv.write-bigdecimal-in-scientific-notation


## Data Type Mapping#


Currently, the CSV schema is always derived from table schema. Explicitly defining an CSV schema is not supported yet.


Flink CSV format uses jackson databind API to parse and generate CSV string.


The following table lists the type mapping from Flink type to CSV type.

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
`INTERVAL`
`number`
`ARRAY`
`array`
`ROW`
`object`