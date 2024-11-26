# Raw


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Raw Format#



Format: Serialization Schema
Format: Deserialization Schema


The Raw format allows to read and write raw (byte based) values as a single column.


Note: this format encodes null values as null of byte[] type. This may have limitation when used in upsert-kafka, because upsert-kafka treats null values as a tombstone message (DELETE on the key). Therefore, we recommend avoiding using upsert-kafka connector and the raw format as a value.format if the field can have a null value.

`null`
`null`
`byte[]`
`upsert-kafka`
`upsert-kafka`
`null`
`upsert-kafka`
`raw`
`value.format`
`null`

The Raw connector is built-in, no additional dependencies are required.


## Example#


For example, you may have following raw log data in Kafka and want to read and analyse such data using Flink SQL.


```
47.29.201.179 - - [28/Feb/2019:13:17:10 +0000] "GET /?p=1 HTTP/2.0" 200 5316 "https://domain.com/?p=1" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36" "2.75"

```

`47.29.201.179 - - [28/Feb/2019:13:17:10 +0000] "GET /?p=1 HTTP/2.0" 200 5316 "https://domain.com/?p=1" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36" "2.75"
`

The following creates a table where it reads from (and can writes to) the underlying Kafka topic as an anonymous string value in UTF-8 encoding by using raw format:

`raw`

```
CREATE TABLE nginx_log (
  log STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'nginx_log',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'format' = 'raw'
)

```

`CREATE TABLE nginx_log (
  log STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'nginx_log',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'format' = 'raw'
)
`

Then you can read out the raw data as a pure string, and split it into multiple fields using an user-defined-function for further analysing, e.g. my_split in the example.

`my_split`

```
SELECT t.hostname, t.datetime, t.url, t.browser, ...
FROM(
  SELECT my_split(log) as t FROM nginx_log
);

```

`SELECT t.hostname, t.datetime, t.url, t.browser, ...
FROM(
  SELECT my_split(log) as t FROM nginx_log
);
`

In contrast, you can also write a single column of STRING type into this Kafka topic as an anonymous string value in UTF-8 encoding.


## Format Options#


##### format


##### raw.charset


##### raw.endianness


## Data Type Mapping#


The table below details the SQL types the format supports, including details of the serializer and deserializer class for encoding and decoding.

`CHAR / VARCHAR / STRING`
`BINARY / VARBINARY / BYTES`
`BOOLEAN`
`TINYINT`
`SMALLINT`
`INT`
`BIGINT`
`FLOAT`
`DOUBLE`
`RAW`