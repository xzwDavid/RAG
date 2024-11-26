# Elasticsearch


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Elasticsearch SQL Connector#



Sink: Batch
Sink: Streaming Append & Upsert Mode


The Elasticsearch connector allows for writing into an index of the Elasticsearch engine. This document describes how to setup the Elasticsearch Connector to run SQL queries against Elasticsearch.


The connector can operate in upsert mode for exchanging UPDATE/DELETE messages with the external system using the primary key defined on the DDL.


If no primary key is defined on the DDL, the connector can only operate in append mode for exchanging INSERT only messages with external system.


## Dependencies#


Only available for stable versions.


The Elasticsearch connector is not part of the binary distribution.
See how to link with it for cluster execution here.


## How to create an Elasticsearch table#


The example below shows how to create an Elasticsearch sink table:


```
CREATE TABLE myUserTable (
  user_id STRING,
  user_name STRING,
  uv BIGINT,
  pv BIGINT,
  PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
  'connector' = 'elasticsearch-7',
  'hosts' = 'http://localhost:9200',
  'index' = 'users'
);

```

`CREATE TABLE myUserTable (
  user_id STRING,
  user_name STRING,
  uv BIGINT,
  pv BIGINT,
  PRIMARY KEY (user_id) NOT ENFORCED
) WITH (
  'connector' = 'elasticsearch-7',
  'hosts' = 'http://localhost:9200',
  'index' = 'users'
);
`

## Connector Options#


##### connector

* elasticsearch-6: connect to Elasticsearch 6.x cluster.
* elasticsearch-7: connect to Elasticsearch 7.x cluster.
`elasticsearch-6`
`elasticsearch-7`

##### hosts

`'http://host_name:9092;http://host_name:9093'`

##### index

`'myIndex'`
`'index-{log_ts|yyyy-MM-dd}'`

##### document-type

`elasticsearch-7`

##### document-id.key-delimiter


##### username


##### password

`username`

##### failure-handler

* fail: throws an exception if a request fails and thus causes a job failure.
* ignore: ignores failures and drops the request.
* retry-rejected: re-adds requests that have failed due to queue capacity saturation.
* custom class name: for failure handling with a ActionRequestFailureHandler subclass.
`fail`
`ignore`
`retry-rejected`

##### sink.delivery-guarantee

* EXACTLY_ONCE: records are only delivered exactly-once also under failover scenarios.
* AT_LEAST_ONCE: records are ensured to be delivered but it may happen that the same record is delivered multiple times.
* NONE:  records are delivered on a best effort basis.
`EXACTLY_ONCE`
`AT_LEAST_ONCE`
`NONE`

##### sink.flush-on-checkpoint


##### sink.bulk-flush.max-actions

`'0'`

##### sink.bulk-flush.max-size

`'0'`

##### sink.bulk-flush.interval

`'0'`
`'sink.bulk-flush.max-size'`
`'sink.bulk-flush.max-actions'`
`'0'`

##### sink.bulk-flush.backoff.strategy

* DISABLED: no retry performed, i.e. fail after the first request error.
* CONSTANT: wait for backoff delay between retries.
* EXPONENTIAL: initially wait for backoff delay and increase exponentially between retries.
`DISABLED`
`CONSTANT`
`EXPONENTIAL`

##### sink.bulk-flush.backoff.max-retries


##### sink.bulk-flush.backoff.delay

`CONSTANT`
`EXPONENTIAL`

##### connection.path-prefix

`'/v1'`

##### connection.request-timeout


##### connection.timeout


##### socket.timeout


##### format

`'json'`

## Features#


### Key Handling#


The Elasticsearch sink can work in either upsert mode or append mode, depending on whether a primary key is defined.
If a primary key is defined, the Elasticsearch sink works in upsert mode which can consume queries containing UPDATE/DELETE messages.
If a primary key is not defined, the Elasticsearch sink works in append mode which can only consume queries containing INSERT only messages.


In the Elasticsearch connector, the primary key is used to calculate the Elasticsearch document id, which is a string of up to 512 bytes. It cannot have whitespaces.
The Elasticsearch connector generates a document ID string for every row by concatenating all primary key fields in the order defined in the DDL using a key delimiter specified by document-id.key-delimiter.
Certain types are not allowed as a primary key field as they do not have a good string representation, e.g. BYTES, ROW, ARRAY, MAP, etc.
If no primary key is specified, Elasticsearch will generate a document id automatically.

`document-id.key-delimiter`
`BYTES`
`ROW`
`ARRAY`
`MAP`

See CREATE TABLE DDL for more details about the PRIMARY KEY syntax.


### Dynamic Index#


The Elasticsearch sink supports both static index and dynamic index.


If you want to have a static index, the index option value should be a plain string, e.g. 'myusers', all the records will be consistently written into “myusers” index.

`index`
`'myusers'`

If you want to have a dynamic index, you can use {field_name} to reference a field value in the record to dynamically generate a target index.
You can also use '{field_name|date_format_string}' to convert a field value of TIMESTAMP/DATE/TIME type into the format specified by the date_format_string.
The date_format_string is compatible with Java’s DateTimeFormatter.
For example, if the option value is 'myusers-{log_ts|yyyy-MM-dd}', then a record with log_ts field value 2020-03-27 12:25:55 will be written into “myusers-2020-03-27” index.

`{field_name}`
`'{field_name|date_format_string}'`
`TIMESTAMP/DATE/TIME`
`date_format_string`
`date_format_string`
`'myusers-{log_ts|yyyy-MM-dd}'`
`log_ts`
`2020-03-27 12:25:55`

You can also use '{now()|date_format_string}' to convert the current system time to the format specified by date_format_string. The corresponding time type of now() is TIMESTAMP_WITH_LTZ.
When formatting the system time as a string, the time zone configured in the session through table.local-time-zone will be used. You can use NOW(), now(), CURRENT_TIMESTAMP, current_timestamp.

`'{now()|date_format_string}'`
`date_format_string`
`now()`
`TIMESTAMP_WITH_LTZ`
`table.local-time-zone`
`NOW()`
`now()`
`CURRENT_TIMESTAMP`
`current_timestamp`

NOTE:  When using the dynamic index generated by the current system time, for changelog stream, there is no guarantee that the records with the same primary key can generate the same index name.
Therefore, the dynamic index based on the system time can only support append only stream.


## Data Type Mapping#


Elasticsearch stores document in a JSON string. So the data type mapping is between Flink data type and JSON data type.
Flink uses built-in 'json' format for Elasticsearch connector. Please refer to JSON Format page for more type mapping details.

`'json'`

 Back to top
