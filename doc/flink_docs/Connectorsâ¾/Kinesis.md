# Kinesis


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Amazon Kinesis Data Streams SQL Connector#



Scan Source: Unbounded
Sink: Batch
Sink: Streaming Append Mode


The Kinesis connector allows for reading data from and writing data into Amazon Kinesis Data Streams (KDS).


## Dependencies#


Only available for stable versions.


The Kinesis connector is not part of the binary distribution.
See how to link with it for cluster execution here.


### Versioning#


There are two available Table API and SQL distributions for the Kinesis connector.
This has resulted from an ongoing migration from the deprecated SourceFunction and SinkFunction interfaces to the new Source and Sink interfaces.

`SourceFunction`
`SinkFunction`
`Source`
`Sink`

The Table API and SQL interfaces in Flink only allow one TableFactory for each connector identifier.
Only one TableFactory with identifier kinesis can be included in your application’s dependencies.

`kinesis`

The following table clarifies the underlying interface that is used depending on the distribution selected:

`flink-sql-connector-aws-kinesis-streams`
`5.x`
`kinesis`
`Source`
`kinesis`
`Sink`
`flink-sql-connector-aws-kinesis-streams`
`4.x`
`kinesis`
`Sink`
`flink-sql-connector-kinesis`
`5.x`
`kinesis`
`Source`
`kinesis-legacy`
`SourceFunction`
`kinesis`
`Sink`
`flink-sql-connector-kinesis`
`4.x`
`kinesis`
`SourceFunction`
`kinesis`
`Sink`

> 
  Only include one artifact, either flink-sql-connector-aws-kinesis-streams or flink-sql-connector-kinesis. Including both will result in clashing TableFactory names.


`flink-sql-connector-aws-kinesis-streams`
`flink-sql-connector-kinesis`

These docs are targeted for versions 5.x onwards. The main configuration section targets kinesis identifier.
For legacy configuration, please see Configuration (kinesis-legacy)

`kinesis`
`kinesis-legacy`

### Migrating from v4.x to v5.x#


There is no state compatibility between Table API and SQL API between 4.x and 5.x.
This is due to the underlying implementation being changed.


Consider starting the job with v5.x kinesis table with source.init.position of AT_TIMESTAMP slightly before the time when the job with v4.x kinesis table was stopped.
Note that this may result in some re-processed some records.

`kinesis`
`source.init.position`
`AT_TIMESTAMP`
`kinesis`

## How to create a Kinesis data stream table#


Follow the instructions from the Amazon KDS Developer Guide to set up a Kinesis stream.
The following example shows how to create a table backed by a Kinesis data stream:


```
CREATE TABLE KinesisTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `category_id` BIGINT,
  `behavior` STRING,
  `ts` TIMESTAMP(3)
)
PARTITIONED BY (user_id, item_id)
WITH (
  'connector' = 'kinesis',
  'stream.arn' = 'arn:aws:kinesis:us-east-1:012345678901:stream/my-stream-name',
  'aws.region' = 'us-east-1',
  'source.init.position' = 'LATEST',
  'format' = 'csv'
);

```

`CREATE TABLE KinesisTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `category_id` BIGINT,
  `behavior` STRING,
  `ts` TIMESTAMP(3)
)
PARTITIONED BY (user_id, item_id)
WITH (
  'connector' = 'kinesis',
  'stream.arn' = 'arn:aws:kinesis:us-east-1:012345678901:stream/my-stream-name',
  'aws.region' = 'us-east-1',
  'source.init.position' = 'LATEST',
  'format' = 'csv'
);
`

## Available Metadata#


> 
  The kinesis table Source has a known bug that means VIRTUAL columns are not supported.
Please use kinesis-legacy until the fix is completed.


`kinesis`
`VIRTUAL`
`kinesis-legacy`

The following metadata can be exposed as read-only (VIRTUAL) columns in a table definition. This is only available in the kinesis-legacy connector only.

`VIRTUAL`
`kinesis-legacy`
`timestamp`
`TIMESTAMP_LTZ(3) NOT NULL`
`shard-id`
`VARCHAR(128) NOT NULL`
`sequence-number`
`VARCHAR(128) NOT NULL`

The extended CREATE TABLE example demonstrates the syntax for exposing these metadata fields:

`CREATE TABLE`

```
CREATE TABLE KinesisTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `category_id` BIGINT,
  `behavior` STRING,
  `ts` TIMESTAMP(3),
  `arrival_time` TIMESTAMP(3) METADATA FROM 'timestamp' VIRTUAL,
  `shard_id` VARCHAR(128) NOT NULL METADATA FROM 'shard-id' VIRTUAL,
  `sequence_number` VARCHAR(128) NOT NULL METADATA FROM 'sequence-number' VIRTUAL
)
PARTITIONED BY (user_id, item_id)
WITH (
  'connector' = 'kinesis-legacy',
  'stream' = 'user_behavior',
  'aws.region' = 'us-east-2',
  'scan.stream.initpos' = 'LATEST',
  'format' = 'csv'
);

```

`CREATE TABLE KinesisTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `category_id` BIGINT,
  `behavior` STRING,
  `ts` TIMESTAMP(3),
  `arrival_time` TIMESTAMP(3) METADATA FROM 'timestamp' VIRTUAL,
  `shard_id` VARCHAR(128) NOT NULL METADATA FROM 'shard-id' VIRTUAL,
  `sequence_number` VARCHAR(128) NOT NULL METADATA FROM 'sequence-number' VIRTUAL
)
PARTITIONED BY (user_id, item_id)
WITH (
  'connector' = 'kinesis-legacy',
  'stream' = 'user_behavior',
  'aws.region' = 'us-east-2',
  'scan.stream.initpos' = 'LATEST',
  'format' = 'csv'
);
`

## Connector Options#


##### connector

`'kinesis'`
`'kinesis-legacy'`

##### stream.arn


##### format


##### aws.region


##### aws.endpoint


##### aws.trust.all.certificates


##### aws.credentials.provider


##### aws.credentials.basic.accesskeyid


##### aws.credentials.basic.secretkey


##### aws.credentials.profile.path


##### aws.credentials.profile.name


##### aws.credentials.role.arn


##### aws.credentials.role.sessionName


##### aws.credentials.role.externalId


##### aws.credentials.role.stsEndpoint


##### aws.credentials.role.provider


##### aws.credentials.webIdentityToken.file


##### aws.credentials.custom.class


##### source.init.position


##### source.init.timestamp

`scan.stream.initpos`

##### source.init.timestamp.format

`scan.stream.initpos`

##### source.shard.discovery.interval


##### source.reader.type

`ReaderType`
`POLLING|EFO`

##### source.shard.get-records.max-record-count

`ReaderType`

##### source.efo.consumer.name

`ReaderType`

##### source.efo.lifecycle

`ReaderType`
`JOB_MANAGED|SELF_MANAGED`

##### source.efo.subscription.timeout

`ReaderType`

##### source.efo.deregister.timeout

`ReaderType`

##### source.efo.describe.retry-strategy.attempts.max

`ReaderType`
`DescribeStreamConsumer`

##### source.efo.describe.retry-strategy.delay.min

`ReaderType`
`DescribeStreamConsumer`

##### source.efo.describe.retry-strategy.delay.max

`ReaderType`
`DescribeStreamConsumer`

##### sink.partitioner


##### sink.partitioner-field-delimiter


##### sink.producer.*

`KinesisStreamsSink`

##### sink.http-client.max-concurrency

`KinesisAsyncClient`

##### sink.http-client.read-timeout

`KinesisAsyncClient`

##### sink.http-client.protocol.version


##### sink.batch.max-size

`KinesisAsyncClient`

##### sink.requests.max-inflight

`KinesisAsyncClient`

##### sink.requests.max-buffered

`KinesisAsyncClient`

##### sink.flush-buffer.size

`KinesisAsyncClient`

##### sink.flush-buffer.timeout

`KinesisAsyncClient`

##### sink.fail-on-error


## Features#


> 
  Refer to the Kinesis Datastream API documentation for more detailed description of features.



### Sink Partitioning#


Kinesis data streams consist of one or more shards, and the sink.partitioner option allows you to control how records written into a multi-shard Kinesis-backed table will be partitioned between its shards.
Valid values are:

`sink.partitioner`
* fixed: Kinesis PartitionKey values derived from the Flink subtask index, so each Flink partition ends up in at most one Kinesis partition (assuming that no re-sharding takes place at runtime).
* random: Kinesis PartitionKey values are assigned randomly. This is the default value for tables not defined with a PARTITION BY clause.
* Custom FixedKinesisPartitioner subclass: e.g. 'org.mycompany.MyPartitioner'.
`fixed`
`PartitionKey`
`random`
`PartitionKey`
`PARTITION BY`
`FixedKinesisPartitioner`
`'org.mycompany.MyPartitioner'`

> 
  Records written into tables defining a PARTITION BY clause will always be partitioned based on a concatenated projection of the PARTITION BY fields.
In this case, the sink.partitioner field cannot be used to modify this behavior (attempting to do this results in a configuration error).
You can, however, use the sink.partitioner-field-delimiter option to set the delimiter of field values in the concatenated PartitionKey string (an empty string is also a valid delimiter).


`PARTITION BY`
`PARTITION BY`
`sink.partitioner`
`sink.partitioner-field-delimiter`

# Data Type Mapping#


Kinesis stores records as Base64-encoded binary data objects, so it doesn’t have a notion of internal record structure.
Instead, Kinesis records are deserialized and serialized by formats, e.g. ‘avro’, ‘csv’, or ‘json’.
To determine the data type of the messages in your Kinesis-backed tables, pick a suitable Flink format with the format keyword.
Please refer to the Formats pages for more details.

`format`

## Connector Options (kinesis-legacy)#

`kinesis-legacy`

##### connector

`'kinesis'`

##### stream


##### format


##### aws.region

`aws.endpoint`

##### aws.endpoint

`aws.region`

##### aws.trust.all.certificates


##### aws.credentials.provider


##### aws.credentials.basic.accesskeyid


##### aws.credentials.basic.secretkey


##### aws.credentials.profile.path


##### aws.credentials.profile.name


##### aws.credentials.role.arn


##### aws.credentials.role.sessionName


##### aws.credentials.role.externalId


##### aws.credentials.role.stsEndpoint


##### aws.credentials.role.provider


##### aws.credentials.webIdentityToken.file


##### aws.credentials.custom.class


##### scan.stream.initpos


##### scan.stream.initpos-timestamp

`scan.stream.initpos`

##### scan.stream.initpos-timestamp-format

`scan.stream.initpos`

##### scan.stream.recordpublisher

`RecordPublisher`

##### scan.stream.efo.consumername


##### scan.stream.efo.registration


##### scan.stream.efo.consumerarn


##### scan.stream.efo.http-client.max-concurrency


##### scan.shard-assigner


##### scan.stream.describe.maxretries

`describeStream`

##### scan.stream.describe.backoff.base

`describeStream`

##### scan.stream.describe.backoff.max

`describeStream`

##### scan.stream.describe.backoff.expconst

`describeStream`

##### scan.list.shards.maxretries

`listShards`

##### scan.list.shards.backoff.base

`listShards`

##### scan.list.shards.backoff.max

`listShards`

##### scan.list.shards.backoff.expconst

`listShards`

##### scan.stream.describestreamconsumer.maxretries

`describeStreamConsumer`

##### scan.stream.describestreamconsumer.backoff.base

`describeStreamConsumer`

##### scan.stream.describestreamconsumer.backoff.max

`describeStreamConsumer`

##### scan.stream.describestreamconsumer.backoff.expconst

`describeStreamConsumer`

##### scan.stream.registerstreamconsumer.maxretries

`registerStream`

##### scan.stream.registerstreamconsumer.timeout


##### scan.stream.registerstreamconsumer.backoff.base

`registerStream`

##### scan.stream.registerstreamconsumer.backoff.max

`registerStream`

##### scan.stream.registerstreamconsumer.backoff.expconst

`registerStream`

##### scan.stream.deregisterstreamconsumer.maxretries

`deregisterStream`

##### scan.stream.deregisterstreamconsumer.timeout


##### scan.stream.deregisterstreamconsumer.backoff.base

`deregisterStream`

##### scan.stream.deregisterstreamconsumer.backoff.max

`deregisterStream`

##### scan.stream.deregisterstreamconsumer.backoff.expconst

`deregisterStream`

##### scan.shard.subscribetoshard.maxretries

`subscribeToShard`

##### scan.shard.subscribetoshard.backoff.base

`subscribeToShard`

##### scan.shard.subscribetoshard.backoff.max

`subscribeToShard`

##### scan.shard.subscribetoshard.backoff.expconst

`subscribeToShard`

##### scan.shard.getrecords.maxrecordcount


##### scan.shard.getrecords.maxretries

`getRecords`

##### scan.shard.getrecords.backoff.base

`getRecords`

##### scan.shard.getrecords.backoff.max

`getRecords`

##### scan.shard.getrecords.backoff.expconst

`getRecords`

##### scan.shard.getrecords.intervalmillis

`getRecords`

##### scan.shard.getiterator.maxretries

`getShardIterator`

##### scan.shard.getiterator.backoff.base

`getShardIterator`

##### scan.shard.getiterator.backoff.max

`getShardIterator`

##### scan.shard.getiterator.backoff.expconst

`getShardIterator`

##### scan.shard.discovery.intervalmillis


##### scan.shard.adaptivereads

`AdaptivePollingRecordPublisher`

##### scan.shard.idle.interval


##### shard.consumer.error.recoverable[0].exception


##### scan.watermark.sync.interval


##### scan.watermark.lookahead.millis


##### scan.watermark.sync.queue.capacity


##### sink.partitioner


##### sink.partitioner-field-delimiter


##### sink.producer.*

`KinesisStreamsSink`

##### sink.http-client.max-concurrency

`KinesisAsyncClient`

##### sink.http-client.read-timeout

`KinesisAsyncClient`

##### sink.http-client.protocol.version


##### sink.batch.max-size

`KinesisAsyncClient`

##### sink.requests.max-inflight

`KinesisAsyncClient`

##### sink.requests.max-buffered

`KinesisAsyncClient`

##### sink.flush-buffer.size

`KinesisAsyncClient`

##### sink.flush-buffer.timeout

`KinesisAsyncClient`

##### sink.fail-on-error


 Back to top
