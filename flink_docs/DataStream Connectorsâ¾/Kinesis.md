# Kinesis


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Amazon Kinesis Data Streams Connector#


The Kinesis connector allows users to read from and write to Amazon Kinesis Data Streams.


## Dependency#


To use this connector, add the below dependency to your project:


Only available for stable versions.


For use in PyFlink jobs, use the following dependency:




In order to use the  in PyFlink jobs, the following
dependencies are required:



Version
PyFlink JAR



flink-connector-kinesis
Only available for stable releases.




See Python dependency management
for more details on how to use JARs in PyFlink.




## Kinesis Streams Source#


The KinesisStreamsSource is an exactly-once, parallel streaming data source based on the FLIP-27 source interface.
The source subscribes to a single Amazon Kinesis Data stream and reads events, maintaining order within a specific Kinesis partitionId. See Record ordering for more details.
The KinesisStreamsSource will discover the shards of the stream and start reading from each eligible shard in parallel, depending on the parallelism of the operator.
For more details on selecting the appropriate parallelism, see Parallelism and Number of Shards.
It also transparently handles discovery of new shards of the Kinesis Data stream if resharding of streams occurs while the job is running.
For more details, see section on Shard Discovery.

`KinesisStreamsSource`
`partitionId`
`KinesisStreamsSource`

> 
  Note: Before consuming data, ensure that the Kinesis Data Stream is created with ACTIVE status on the Amazon Kinesis Data Streams console.


`ACTIVE`

The KinesisStreamsSource provides a fluent builder to construct an instance of the KinesisStreamsSource.
The code snippet below illustrates how to do so.

`KinesisStreamsSource`
`KinesisStreamsSource`

```
// Configure the KinesisStreamsSource
Configuration sourceConfig = new Configuration();
sourceConfig.set(KinesisSourceConfigOptions.STREAM_INITIAL_POSITION, KinesisSourceConfigOptions.InitialPosition.TRIM_HORIZON); // This is optional, by default connector will read from LATEST

// Create a new KinesisStreamsSource to read from specified Kinesis Stream.
KinesisStreamsSource<String> kdsSource =
        KinesisStreamsSource.<String>builder()
                .setStreamArn("arn:aws:kinesis:us-east-1:123456789012:stream/test-stream")
                .setSourceConfig(sourceConfig)
                .setDeserializationSchema(new SimpleStringSchema())
                .setKinesisShardAssigner(ShardAssignerFactory.uniformShardAssigner()) // This is optional, by default uniformShardAssigner will be used.
                .build();

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Specify watermarking strategy and the name of the Kinesis Source operator.
// Specify return type using TypeInformation.
// Specify UID of operator in line with Flink best practice.
DataStream<String> kinesisRecordsWithEventTimeWatermarks = env.fromSource(kdsSource, WatermarkStrategy.<String>forMonotonousTimestamps().withIdleness(Duration.ofSeconds(1)), "Kinesis source")
        .returns(TypeInformation.of(String.class))
        .uid("custom-uid");

```

`// Configure the KinesisStreamsSource
Configuration sourceConfig = new Configuration();
sourceConfig.set(KinesisSourceConfigOptions.STREAM_INITIAL_POSITION, KinesisSourceConfigOptions.InitialPosition.TRIM_HORIZON); // This is optional, by default connector will read from LATEST

// Create a new KinesisStreamsSource to read from specified Kinesis Stream.
KinesisStreamsSource<String> kdsSource =
        KinesisStreamsSource.<String>builder()
                .setStreamArn("arn:aws:kinesis:us-east-1:123456789012:stream/test-stream")
                .setSourceConfig(sourceConfig)
                .setDeserializationSchema(new SimpleStringSchema())
                .setKinesisShardAssigner(ShardAssignerFactory.uniformShardAssigner()) // This is optional, by default uniformShardAssigner will be used.
                .build();

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Specify watermarking strategy and the name of the Kinesis Source operator.
// Specify return type using TypeInformation.
// Specify UID of operator in line with Flink best practice.
DataStream<String> kinesisRecordsWithEventTimeWatermarks = env.fromSource(kdsSource, WatermarkStrategy.<String>forMonotonousTimestamps().withIdleness(Duration.ofSeconds(1)), "Kinesis source")
        .returns(TypeInformation.of(String.class))
        .uid("custom-uid");
`

```
val sourceConfig = new Configuration()
sourceConfig.set(KinesisSourceConfigOptions.STREAM_INITIAL_POSITION, KinesisSourceConfigOptions.InitialPosition.TRIM_HORIZON) // This is optional, by default connector will read from LATEST

val env = StreamExecutionEnvironment.getExecutionEnvironment()

val kdsSource = KinesisStreamsSource.builder[String]()
            .setStreamArn("arn:aws:kinesis:us-east-1:123456789012:stream/test-stream")
            .setSourceConfig(sourceConfig)
            .setDeserializationSchema(new SimpleStringSchema())
            .setKinesisShardAssigner(ShardAssignerFactory.uniformShardAssigner()) // This is optional, by default uniformShardAssigner will be used.
            .build()

val kinesisEvents = env.fromSource(kdsSource, WatermarkStrategy.forMonotonousTimestamps().withIdleness(Duration.ofSeconds(1)), "Kinesis source")
            .uid("custom-uid")

```

`val sourceConfig = new Configuration()
sourceConfig.set(KinesisSourceConfigOptions.STREAM_INITIAL_POSITION, KinesisSourceConfigOptions.InitialPosition.TRIM_HORIZON) // This is optional, by default connector will read from LATEST

val env = StreamExecutionEnvironment.getExecutionEnvironment()

val kdsSource = KinesisStreamsSource.builder[String]()
            .setStreamArn("arn:aws:kinesis:us-east-1:123456789012:stream/test-stream")
            .setSourceConfig(sourceConfig)
            .setDeserializationSchema(new SimpleStringSchema())
            .setKinesisShardAssigner(ShardAssignerFactory.uniformShardAssigner()) // This is optional, by default uniformShardAssigner will be used.
            .build()

val kinesisEvents = env.fromSource(kdsSource, WatermarkStrategy.forMonotonousTimestamps().withIdleness(Duration.ofSeconds(1)), "Kinesis source")
            .uid("custom-uid")
`

The above is a simple example of using the KinesisStreamsSource.

`KinesisStreamsSource`
* The Kinesis stream being read from is specified using the Kinesis Stream ARN.
* Configuration for the Source is supplied using an instance of Flink’s Configuration class.
The configuration keys can be taken from AWSConfigOptions (AWS-specific configuration) and KinesisSourceConfigOptions (Kinesis Source configuration).
* The example specifies the starting position as TRIM_HORIZON (see Configuring Starting Position for more information).
* The deserialization format is as SimpleStringSchema (see Deserialization Schema for more information).
* The distribution of shards across subtasks is controlled using the UniformShardAssigner  (see Shard Assignment Strategy for more information).
* The example also specifies an increasing WatermarkStrategy, which means each record will be tagged with event time specified using approximateArrivalTimestamp.
Monotonically increasing watermarks will be generated, and subtasks will be considered idle if no record is emitted after 1 second.
`Source`
`Configuration`
`AWSConfigOptions`
`KinesisSourceConfigOptions`
`TRIM_HORIZON`
`SimpleStringSchema`
`UniformShardAssigner`
`WatermarkStrategy`
`approximateArrivalTimestamp`

### Configuring Access to Kinesis with IAM#


Access to Kinesis streams are controlled via IAM identities. Make sure to create the appropriate IAM policy to allow reading / writing to / from the Kinesis streams. See examples here.


Depending on your deployment, you can select a suitable AWS Credentials Provider.
By default, the AUTO Credentials Provider is used.
If the access key ID and secret key are set in the configuration, the BASIC provider is used.

`AUTO`
`BASIC`

A specific Credentials Provider can optionally be set by using the AWSConfigConstants.AWS_CREDENTIALS_PROVIDER setting.

`AWSConfigConstants.AWS_CREDENTIALS_PROVIDER`

Supported Credential Providers are:

* AUTO(default): Using the default AWS Credentials Provider chain that searches for credentials in the following order: ENV_VARS, SYS_PROPS, WEB_IDENTITY_TOKEN, PROFILE and EC2/ECS credentials provider.
* BASIC: Using access key ID and secret key supplied as configuration.
* ENV_VAR: Using AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY environment variables.
* SYS_PROP: Using Java system properties aws.accessKeyId and aws.secretKey.
* CUSTOM: Use a custom user class as credential provider.
* PROFILE: Use AWS credentials profile file to create the AWS credentials.
* ASSUME_ROLE: Create AWS credentials by assuming a role. The credentials for assuming the role must be supplied.
* WEB_IDENTITY_TOKEN: Create AWS credentials by assuming a role using Web Identity Token.
`AUTO`
`ENV_VARS`
`SYS_PROPS`
`WEB_IDENTITY_TOKEN`
`PROFILE`
`BASIC`
`ENV_VAR`
`AWS_ACCESS_KEY_ID`
`AWS_SECRET_ACCESS_KEY`
`SYS_PROP`
`CUSTOM`
`PROFILE`
`ASSUME_ROLE`
`WEB_IDENTITY_TOKEN`

### Configuring Starting Position#


To specify where the KinesisStreamsSource starts reading from the Kinesis stream, users can set the KinesisSourceConfigOptions.STREAM_INITIAL_POSITION in configuration.
The values used follow the namings used by the AWS Kinesis Data Streams service:

`KinesisStreamsSource`
`KinesisSourceConfigOptions.STREAM_INITIAL_POSITION`
* LATEST(default): read all shards of the stream starting from the latest record.
* TRIM_HORIZON: read all shards of the stream starting from the earliest record possible (data may be trimmed by Kinesis depending on the retention settings).
* AT_TIMESTAMP: read all shards of the stream starting from a specified timestamp. The timestamp must also be specified in the configuration
properties by providing a value for KinesisSourceConfigOptions.STREAM_INITIAL_TIMESTAMP, in one of the following date pattern :

a non-negative double value representing the number of seconds that has elapsed since the Unix epoch (for example, 1459799926.480).
a user-defined pattern, specified as a valid SimpleDateFormat pattern provided by KinesisSourceConfigOptions.STREAM_TIMESTAMP_DATE_FORMAT.
If KinesisSourceConfigOptions.STREAM_TIMESTAMP_DATE_FORMAT is not defined then the default pattern will be yyyy-MM-dd'T'HH:mm:ss.SSSXXX
(for example, timestamp value is 2016-04-04 and pattern is yyyy-MM-dd given by user or timestamp value is 2016-04-04T19:58:46.480-00:00 without given a pattern).


`LATEST`
`TRIM_HORIZON`
`AT_TIMESTAMP`
`KinesisSourceConfigOptions.STREAM_INITIAL_TIMESTAMP`
* a non-negative double value representing the number of seconds that has elapsed since the Unix epoch (for example, 1459799926.480).
* a user-defined pattern, specified as a valid SimpleDateFormat pattern provided by KinesisSourceConfigOptions.STREAM_TIMESTAMP_DATE_FORMAT.
If KinesisSourceConfigOptions.STREAM_TIMESTAMP_DATE_FORMAT is not defined then the default pattern will be yyyy-MM-dd'T'HH:mm:ss.SSSXXX
(for example, timestamp value is 2016-04-04 and pattern is yyyy-MM-dd given by user or timestamp value is 2016-04-04T19:58:46.480-00:00 without given a pattern).
`1459799926.480`
`SimpleDateFormat`
`KinesisSourceConfigOptions.STREAM_TIMESTAMP_DATE_FORMAT`
`KinesisSourceConfigOptions.STREAM_TIMESTAMP_DATE_FORMAT`
`yyyy-MM-dd'T'HH:mm:ss.SSSXXX`
`2016-04-04`
`yyyy-MM-dd`
`2016-04-04T19:58:46.480-00:00`

> 
  The configured starting position is ignored if application is restarting from checkpoint or savepoint. For more details, see section on Fault tolerance.



### Fault Tolerance for Exactly-Once User-Defined State Update Semantics#


With Flink’s checkpointing enabled, the KinesisStreamsSource will consume records from shards in Kinesis streams and
periodically checkpoint each shard’s progress. In case of a job failure, Flink will restore the streaming program to the
state of the latest complete checkpoint and re-consume the records from Kinesis shards, starting from the progress that
was stored in the checkpoint.

`KinesisStreamsSource`

Note that when restoring from a checkpoint or savepoint, the configured starting positions will be ignored.
The KinesisStreamsSource will proceed to read from where it left off in the checkpoint or savepoint.
If the restored checkpoint or savepoint is stale (e.g. the shards saved are now expired and past the retention period of the Kinesis stream),
the source does not fail, and will start reading from the earliest possible event (effectively a TRIM_HORIZON).

`KinesisStreamsSource`
`TRIM_HORIZON`

If users want to restore a Flink job from an existing checkpoint or savepoint but want to respect the configured starting position of
the stream, users can change the uid of the KinesisStreamsSource operator to effectively restore this operator without state.
This is in line with Flink best practices.

`uid`
`KinesisStreamsSource`

### Shard Assignment Strategy#


For most use cases, users would prefer a uniform distribution of records across parallel subtasks. This prevents data skew if data is evenly distributed in the Kinesis Data Stream.
This is achieved by the UniformShardAssigner, which is the default shard assignment strategy. Users can implement their own custom strategy by implementing the interface for KinesisShardAssigner.

`UniformShardAssigner`
`KinesisShardAssigner`

Uniformly distributing shards across parallel subtasks is non-trivial when the stream has been resharded.
Amazon Kinesis Data streams distributes partitionIds evenly across the entire HashKeyRange of a given stream, and these ranges are evenly distributed across all open shards if UNIFORM_SCALING is used.
However, there will be a mixture of Open and Closed shards on the Kinesis Data Stream, and the status of each shard can change during a rescaling operation.

`partitionId`
`HashKeyRange`
`UNIFORM_SCALING`

To ensure a uniform distribution of partitionIds across each parallel subtask, the UniformShardAssigner uses the HashKeyRange of each shard to decide which parallel subtask will read from the discovered shard.

`partitionId`
`UniformShardAssigner`
`HashKeyRange`

### Record ordering#


Kinesis maintains the write order of records per partitionId within a Kinesis stream. The KinesisStreamsSource reads
records in the same order within a given partitionId, even through resharding operations. It does this by first checking if
a given shard’s parents (up to 2 shards) have been completely read, before proceeding to read from the given shard.

`partitionId`
`KinesisStreamsSource`
`partitionId`

### Deserialization Schema#


The KinesisStreamsSource retrieves binary data from the Kinesis Data Stream, and needs a schema to convert it into Java objects.
Both Flink’s DeserializationSchema and the custom KinesisDeserializationSchema are accepted by the KinesisStreamsSource.
The KinesisDeserializationSchema provides additional Kinesis-specific metadata per record to allow users to make serialization decisions based off the metadata.

`KinesisStreamsSource`
`DeserializationSchema`
`KinesisDeserializationSchema`
`KinesisStreamsSource`
`KinesisDeserializationSchema`

For convenience, Flink provides the following schemas out of the box:

1. 
SimpleStringSchema and JsonSerializationSchema.

2. 
TypeInformationSerializationSchema which creates a schema based on a Flink’s TypeInformation.
This is useful if the data is both written and read by Flink.
This schema is a performant Flink-specific alternative to other generic serialization approaches.

3. 
GlueSchemaRegistryJsonDeserializationSchema offers the ability to lookup the writer’s schema (schema which was used to write the record)
in AWS Glue Schema Registry. Using this, deserialization schema record will be
read with the schema retrieved from AWS Glue Schema Registry and transformed to either com.amazonaws.services.schemaregistry.serializers.json.JsonDataWithSchema
that represents generic record with a manually provided schema or a JAVA POJO generated by mbknor-jackson-jsonSchema.
To use this deserialization schema one has to add the following additional dependency:


SimpleStringSchema and JsonSerializationSchema.

`SimpleStringSchema`
`JsonSerializationSchema`

TypeInformationSerializationSchema which creates a schema based on a Flink’s TypeInformation.
This is useful if the data is both written and read by Flink.
This schema is a performant Flink-specific alternative to other generic serialization approaches.

`TypeInformationSerializationSchema`
`TypeInformation`

GlueSchemaRegistryJsonDeserializationSchema offers the ability to lookup the writer’s schema (schema which was used to write the record)
in AWS Glue Schema Registry. Using this, deserialization schema record will be
read with the schema retrieved from AWS Glue Schema Registry and transformed to either com.amazonaws.services.schemaregistry.serializers.json.JsonDataWithSchema
that represents generic record with a manually provided schema or a JAVA POJO generated by mbknor-jackson-jsonSchema.

`GlueSchemaRegistryJsonDeserializationSchema`
`com.amazonaws.services.schemaregistry.serializers.json.JsonDataWithSchema`

To use this deserialization schema one has to add the following additional dependency:


Only available for stable versions.

1. 
AvroDeserializationSchema which reads data serialized with Avro format using a statically provided schema. It can
infer the schema from Avro generated classes (AvroDeserializationSchema.forSpecific(...)) or it can work with GenericRecords
with a manually provided schema (with AvroDeserializationSchema.forGeneric(...)). When deserializing Avro GenericRecords,
the deserialization schema expects the records DO NOT contain an embedded schema.

You can use AWS Glue Schema Registry
to retrieve the writerâs schema. Similarly, the deserialization record will be read with the schema from AWS Glue Schema Registry and transformed
(either through GlueSchemaRegistryAvroDeserializationSchema.forGeneric(...) or GlueSchemaRegistryAvroDeserializationSchema.forSpecific(...)).
For more information on integrating the AWS Glue Schema Registry with Apache Flink see
Use Case: Amazon Kinesis Data Analytics for Apache Flink.

To use this deserialization schema one has to add the following additional dependency:


AvroDeserializationSchema which reads data serialized with Avro format using a statically provided schema. It can
infer the schema from Avro generated classes (AvroDeserializationSchema.forSpecific(...)) or it can work with GenericRecords
with a manually provided schema (with AvroDeserializationSchema.forGeneric(...)). When deserializing Avro GenericRecords,
the deserialization schema expects the records DO NOT contain an embedded schema.

`AvroDeserializationSchema`
`AvroDeserializationSchema.forSpecific(...)`
`GenericRecords`
`AvroDeserializationSchema.forGeneric(...)`
`GenericRecords`
* You can use AWS Glue Schema Registry
to retrieve the writerâs schema. Similarly, the deserialization record will be read with the schema from AWS Glue Schema Registry and transformed
(either through GlueSchemaRegistryAvroDeserializationSchema.forGeneric(...) or GlueSchemaRegistryAvroDeserializationSchema.forSpecific(...)).
For more information on integrating the AWS Glue Schema Registry with Apache Flink see
Use Case: Amazon Kinesis Data Analytics for Apache Flink.
`GlueSchemaRegistryAvroDeserializationSchema.forGeneric(...)`
`GlueSchemaRegistryAvroDeserializationSchema.forSpecific(...)`

To use this deserialization schema one has to add the following additional dependency:


```
&ltdependency>
    &ltgroupId>org.apache.flink</groupId>
    &ltartifactId>flink-avro</artifactId>
    &ltversion>2.0-SNAPSHOT</version>
</dependency>
```

`&ltdependency>
    &ltgroupId>org.apache.flink</groupId>
    &ltartifactId>flink-avro</artifactId>
    &ltversion>2.0-SNAPSHOT</version>
</dependency>`

Only available for stable versions.


### Parallelism and Number of Shards#


The configured parallelism of the KinesisStreamsSource is independent of the total number of shards in the Kinesis streams.

`KinesisStreamsSource`
* If the parallelism of the KinesisStreamsSource is less than the total number of shards, then a single parallel subtask would handle multiple shards.
* If the parallelism of the KinesisStreamsSource is more than the total number of shards, then there will be some parallel subtasks that do not read from any shards. If this is the case, users will need to set up withIdleness on the WatermarkStrategy. Failing to do so will mean watermark generation will get blocked due to idle subtasks.
`KinesisStreamsSource`
`KinesisStreamsSource`
`withIdleness`
`WatermarkStrategy`

### Watermark Handling in the source#


The KinesisStreamsSource supplies the approximateArrivalTimestamp provided by Kinesis as the event time associated with each record read.
For more information on event time handling in Flink, see Event time.
Note that this timestamp is typically referred to as a Kinesis server-side timestamp, and there are no guarantees
about the accuracy or order correctness (i.e., the timestamps may not always be ascending).

`KinesisStreamsSource`
`approximateArrivalTimestamp`

### Event Time Alignment for Shard Readers#


Since the shards are being consumed in parallel, some shards might be reading records far ahead from other shards.
Flink supports synchronization between these reading speed using split-specific watermark alignment. The KinesisStreamsSource
supports split-specific watermark alignment, and will pause reading from specific shards if the watermark from that shard
is too far ahead of others. It will resume reading from that specific split once the other shards catch up.

`KinesisStreamsSource`

### Threading Model#


The KinesisStreamsSource uses multiple threads for shard discovery and data consumption.

`KinesisStreamsSource`

#### Shard Discovery#


For shard discovery, the SplitEnumerator runs on the JobManager to periodically discover new shards using the ListShard API.
Once new shards are discovered, it will confirm if the parent shards have been completed. If all parents have been completed,
the shards will be assigned to the SplitReader on the TaskManagers to be read.

`SplitEnumerator`
`ListShard`
`SplitReader`

#### Polling (default) Split Reader#


For POLLING data consumption, a single thread will be created per-parallel subtask to consume allocated shards. This means
that the number of open threads scale with the parallelism of the Flink operator.

`POLLING`

#### Enhanced Fan-Out Split Reader#


For EFO data consumption the threading model is the same as POLLING - one thread per-parallel subtask. However,
there are additional thread pools to handle asynchronous communication with Kinesis. AWS SDK v2.x KinesisAsyncClient
uses additional threads for Netty to handle IO and asynchronous response. Each parallel subtask will have their own
instance of the KinesisAsyncClient. In other words, if the consumer is run with a parallelism of 10, there will be a
total of 10 KinesisAsyncClient instances. A separate client will be created and subsequently destroyed when
registering and deregistering stream consumers.

`EFO`
`POLLING`
`KinesisAsyncClient`
`KinesisAsyncClient`
`KinesisAsyncClient`

### Using Enhanced Fan-Out#


Enhanced Fan-Out (EFO) increases the maximum number of concurrent consumers per Kinesis stream.
Without EFO, all concurrent consumers share a single read quota per shard.
Using EFO, each consumer gets a distinct dedicated read quota per shard, allowing read throughput to scale with the number of consumers.
Using EFO will incur additional cost.


In order to enable EFO two additional configuration parameters are required:

* READER_TYPE: Determines whether to use EFO or POLLING. The default ReaderType is POLLING.
* EFO_CONSUMER_NAME: A name to identify the consumer.
For a given Kinesis data stream, each consumer must have a unique name.
However, consumer names do not have to be unique across data streams.
Reusing a consumer name will terminate existing subscriptions.
`READER_TYPE`
`EFO`
`POLLING`
`ReaderType`
`POLLING`
`EFO_CONSUMER_NAME`

The code snippet below shows a simple example configuring an EFO consumer.


```
Configuration sourceConfig = new Configuration();
sourceConfig.set(KinesisSourceConfigOptions.READER_TYPE, KinesisSourceConfigOptions.ReaderType.EFO);
sourceConfig.set(KinesisSourceConfigOptions.EFO_CONSUMER_NAME, "my-flink-efo-consumer");

```

`Configuration sourceConfig = new Configuration();
sourceConfig.set(KinesisSourceConfigOptions.READER_TYPE, KinesisSourceConfigOptions.ReaderType.EFO);
sourceConfig.set(KinesisSourceConfigOptions.EFO_CONSUMER_NAME, "my-flink-efo-consumer");
`

```
val sourceConfig = new Configuration()
sourceConfig.set(KinesisSourceConfigOptions.READER_TYPE, KinesisSourceConfigOptions.ReaderType.EFO)
sourceConfig.set(KinesisSourceConfigOptions.EFO_CONSUMER_NAME, "my-flink-efo-consumer")

```

`val sourceConfig = new Configuration()
sourceConfig.set(KinesisSourceConfigOptions.READER_TYPE, KinesisSourceConfigOptions.ReaderType.EFO)
sourceConfig.set(KinesisSourceConfigOptions.EFO_CONSUMER_NAME, "my-flink-efo-consumer")
`

#### EFO Stream Consumer Lifecycle Management#


In order to use EFO, a stream consumer must be registered against the stream you wish to consume.
By default, the KinesisStreamsSource will manage the lifecycle of the stream consumer automatically when the Flink job starts/stops.
The stream consumer will be registered using the name provided by the EFO_CONSUMER_NAME configuration, and de-registered when job stops gracefully.
KinesisStreamsSource provides two lifecycle options for KinesisSourceConfigOptions.EFO_CONSUMER_LIFECYCLE:

`KinesisStreamsSource`
`EFO_CONSUMER_NAME`
`KinesisStreamsSource`
`KinesisSourceConfigOptions.EFO_CONSUMER_LIFECYCLE`
* JOB_MANAGED (default): Stream consumers are registered when the Flink job starts running.
If the stream consumer already exists, it will be reused.
When the job stops gracefully, the consumer will be de-registered.
This is the preferred strategy for the majority of applications.
* SELF_MANAGED: Stream consumer registration/de-registration will not be performed by the KinesisStreamsSource.
Registration must be performed externally using the AWS CLI or SDK
to invoke RegisterStreamConsumer.
Stream consumer ARNs should be provided to the job via the consumer configuration.
`JOB_MANAGED`
`SELF_MANAGED`
`KinesisStreamsSource`

### Internally Used Kinesis APIs#


The KinesisStreamsSource uses the AWS v2 SDK for Java internally to call Kinesis APIs
for shard discovery and data consumption. Due to Amazon’s service limits for Kinesis Streams,
the KinesisStreamsSource will compete with other non-Flink consuming applications that the user may be running.
Below is a list of APIs called by the consumer with description of how the consumer uses the API, as well as information
on how to deal with any errors or warnings that the KinesisStreamsSource may have due to these service limits.

`KinesisStreamsSource`
`KinesisStreamsSource`
`KinesisStreamsSource`

#### Retry Strategy#


The retry strategy used by the AWS SDK client can be tuned using the following configuration options:

* AWSConfigOptions.RETRY_STRATEGY_MAX_ATTEMPTS_OPTION: Maximum of API retries on retryable errors, before it will restart the Flink job.
* AWSConfigOptions.RETRY_STRATEGY_MIN_DELAY_OPTION: The base delay used for calculation of the exponential backoff.
* AWSConfigOptions.RETRY_STRATEGY_MAX_DELAY_OPTION: The maximum delay for exponential backoff.
`AWSConfigOptions.RETRY_STRATEGY_MAX_ATTEMPTS_OPTION`
`AWSConfigOptions.RETRY_STRATEGY_MIN_DELAY_OPTION`
`AWSConfigOptions.RETRY_STRATEGY_MAX_DELAY_OPTION`

The retry strategy is used for all API requests, except for DescribeStreamConsumer.
To configure the retry strategy for DescribeStreamConsumer use instead KinesisSourceConfigOptions.EFO_DESCRIBE_CONSUMER_RETRY_STRATEGY* options.
This API call has a separate retry strategy, as it is only called during job startup to validate EFO consumer registration.
This may require a different retry strategy compared to other API calls used during normal operation.

`DescribeStreamConsumer`
`DescribeStreamConsumer`
`KinesisSourceConfigOptions.EFO_DESCRIBE_CONSUMER_RETRY_STRATEGY*`

#### Shard Discovery#

* ListShards: this is periodically called
by the SplitEnumerator, one per Flink job, to discover any new shards as a result of stream resharding. By default,
the SplitEnumerator performs the shard discovery at an interval of 10 seconds. If this interferes with other non-Flink
consuming applications, users can slow down the calls to this API by setting a value for
KinesisSourceConfigOptions.SHARD_DISCOVERY_INTERVAL in the supplied Configuration.
This sets the discovery interval to a different value. Note that this setting directly impacts
the maximum delay of discovering a new shard and starting to consume it, as shards will not be discovered during the interval.
`SplitEnumerator`
`SplitEnumerator`
`KinesisSourceConfigOptions.SHARD_DISCOVERY_INTERVAL`
`Configuration`

#### Polling (default) Split Reader#

* 
GetShardIterator: this is called once per shard, Note that since the rate limit for this API is per shard (not per stream),
the split reader itself should not exceed the limit.

* 
GetRecords: this is constantly called to fetch records from Kinesis. When a shard has multiple concurrent consumers (when there
are any other non-Flink consuming applications running), the per shard rate limit may be exceeded. By default, on each call
of this API, the consumer will retry if Kinesis complains that the data size / transaction limit for the API has exceeded.


GetShardIterator: this is called once per shard, Note that since the rate limit for this API is per shard (not per stream),
the split reader itself should not exceed the limit.


GetRecords: this is constantly called to fetch records from Kinesis. When a shard has multiple concurrent consumers (when there
are any other non-Flink consuming applications running), the per shard rate limit may be exceeded. By default, on each call
of this API, the consumer will retry if Kinesis complains that the data size / transaction limit for the API has exceeded.


#### Enhanced Fan-Out Split Reader#

* 
SubscribeToShard: this is called per shard to obtain shard subscriptions. A shard subscription is typically active for 5 minutes,
but subscriptions will be re-acquired if any recoverable errors are thrown. Once a subscription is acquired, the consumer
will receive a stream of SubscribeToShardEventss.

* 
DescribeStreamConsumer:
this is called only during application startup per parallel subtask of the operator. This is to retrieve the consumerArn
for the ACTIVE consumer attached to the stream. The retry strategy can be configured using KinesisSourceConfigOptions.EFO_DESCRIBE_CONSUMER_RETRY_STRATEGY* options

* 
RegisterStreamConsumer:
this is called once per stream during stream consumer registration, unless the SELF_MANAGED consumer lifecycle is configured.

* 
DeregisterStreamConsumer:
this is called once per stream during stream consumer deregistration, unless the SELF_MANAGED registration strategy is configured.


SubscribeToShard: this is called per shard to obtain shard subscriptions. A shard subscription is typically active for 5 minutes,
but subscriptions will be re-acquired if any recoverable errors are thrown. Once a subscription is acquired, the consumer
will receive a stream of SubscribeToShardEventss.


DescribeStreamConsumer:
this is called only during application startup per parallel subtask of the operator. This is to retrieve the consumerArn
for the ACTIVE consumer attached to the stream. The retry strategy can be configured using KinesisSourceConfigOptions.EFO_DESCRIBE_CONSUMER_RETRY_STRATEGY* options

`consumerArn`
`ACTIVE`
`KinesisSourceConfigOptions.EFO_DESCRIBE_CONSUMER_RETRY_STRATEGY*`

RegisterStreamConsumer:
this is called once per stream during stream consumer registration, unless the SELF_MANAGED consumer lifecycle is configured.

`SELF_MANAGED`

DeregisterStreamConsumer:
this is called once per stream during stream consumer deregistration, unless the SELF_MANAGED registration strategy is configured.

`SELF_MANAGED`

## Kinesis Consumer#


> 
  The old Kinesis source org.apache.flink.streaming.connectors.kinesis.FlinkKinesisConsumer is deprecated and may be removed with a future release of Flink, please use Kinesis Source instead.


`org.apache.flink.streaming.connectors.kinesis.FlinkKinesisConsumer`

Note that there is no state compatibility between the FlinkKinesisConsumer and KinesisStreamsSource.
See section on migration for more details.

`FlinkKinesisConsumer`
`KinesisStreamsSource`

### Migrating existing jobs to new Kinesis Streams Source from Kinesis Consumer#


There is no state compatibility between the FlinkKinesisConsumer and KinesisStreamsSource.
This means that the starting position is lost when migrating from the FlinkKinesisConsumer to the KinesisStreamsSource.
Consider starting the KinesisStreamsSource from AT_TIMESTAMP slightly before the time when the FlinkKinesisConsumer was stopped.
Note that this may result in some re-processed some records.

`FlinkKinesisConsumer`
`KinesisStreamsSource`
`FlinkKinesisConsumer`
`KinesisStreamsSource`
`KinesisStreamsSource`
`AT_TIMESTAMP`
`FlinkKinesisConsumer`

If you are following best practices and specifying the source operator uid, the uid needs to be changed, and allowNonRestoredState needs to be enabled
when restoring the Flink job from the savepoint.

`uid`
`uid`
`allowNonRestoredState`

## Kinesis Streams Sink#


The Kinesis Streams sink (hereafter “Kinesis sink”) uses the AWS v2 SDK for Java to write data from a Flink stream into a Kinesis stream.


To write data into a Kinesis stream, make sure the stream is marked as “ACTIVE” in the Amazon Kinesis Data Stream console.


For the monitoring to work, the user accessing the stream needs access to the CloudWatch service.


```
Properties sinkProperties = new Properties();
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "us-east-1");

// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");

KinesisStreamsSink<String> kdsSink =
    KinesisStreamsSink.<String>builder()
        .setKinesisClientProperties(sinkProperties)                               // Required
        .setSerializationSchema(new SimpleStringSchema())                         // Required
        .setPartitionKeyGenerator(element -> String.valueOf(element.hashCode()))  // Required
        .setStreamName("your-stream-name")                                        // Required
        .setFailOnError(false)                                                    // Optional
        .setMaxBatchSize(500)                                                     // Optional
        .setMaxInFlightRequests(50)                                               // Optional
        .setMaxBufferedRequests(10_000)                                           // Optional
        .setMaxBatchSizeInBytes(5 * 1024 * 1024)                                  // Optional
        .setMaxTimeInBufferMS(5000)                                               // Optional
        .setMaxRecordSizeInBytes(1 * 1024 * 1024)                                 // Optional
        .build();

DataStream<String> simpleStringStream = ...;
simpleStringStream.sinkTo(kdsSink);

```

`Properties sinkProperties = new Properties();
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "us-east-1");

// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");

KinesisStreamsSink<String> kdsSink =
    KinesisStreamsSink.<String>builder()
        .setKinesisClientProperties(sinkProperties)                               // Required
        .setSerializationSchema(new SimpleStringSchema())                         // Required
        .setPartitionKeyGenerator(element -> String.valueOf(element.hashCode()))  // Required
        .setStreamName("your-stream-name")                                        // Required
        .setFailOnError(false)                                                    // Optional
        .setMaxBatchSize(500)                                                     // Optional
        .setMaxInFlightRequests(50)                                               // Optional
        .setMaxBufferedRequests(10_000)                                           // Optional
        .setMaxBatchSizeInBytes(5 * 1024 * 1024)                                  // Optional
        .setMaxTimeInBufferMS(5000)                                               // Optional
        .setMaxRecordSizeInBytes(1 * 1024 * 1024)                                 // Optional
        .build();

DataStream<String> simpleStringStream = ...;
simpleStringStream.sinkTo(kdsSink);
`

```
val sinkProperties = new Properties()
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "us-east-1")

// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")

val kdsSink = KinesisStreamsSink.<String>builder()
    .setKinesisClientProperties(sinkProperties)                               // Required
    .setSerializationSchema(new SimpleStringSchema())                         // Required
    .setPartitionKeyGenerator(element -> String.valueOf(element.hashCode()))  // Required
    .setStreamName("your-stream-name")                                        // Required
    .setFailOnError(false)                                                    // Optional
    .setMaxBatchSize(500)                                                     // Optional
    .setMaxInFlightRequests(50)                                               // Optional
    .setMaxBufferedRequests(10000)                                            // Optional
    .setMaxBatchSizeInBytes(5 * 1024 * 1024)                                  // Optional
    .setMaxTimeInBufferMS(5000)                                               // Optional
    .setMaxRecordSizeInBytes(1 * 1024 * 1024)                                 // Optional
    .build()

val simpleStringStream = ...
simpleStringStream.sinkTo(kdsSink)

```

`val sinkProperties = new Properties()
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "us-east-1")

// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")

val kdsSink = KinesisStreamsSink.<String>builder()
    .setKinesisClientProperties(sinkProperties)                               // Required
    .setSerializationSchema(new SimpleStringSchema())                         // Required
    .setPartitionKeyGenerator(element -> String.valueOf(element.hashCode()))  // Required
    .setStreamName("your-stream-name")                                        // Required
    .setFailOnError(false)                                                    // Optional
    .setMaxBatchSize(500)                                                     // Optional
    .setMaxInFlightRequests(50)                                               // Optional
    .setMaxBufferedRequests(10000)                                            // Optional
    .setMaxBatchSizeInBytes(5 * 1024 * 1024)                                  // Optional
    .setMaxTimeInBufferMS(5000)                                               // Optional
    .setMaxRecordSizeInBytes(1 * 1024 * 1024)                                 // Optional
    .build()

val simpleStringStream = ...
simpleStringStream.sinkTo(kdsSink)
`

```
# Required
sink_properties = {
    # Required
    'aws.region': 'us-east-1',
    # Optional, provide via alternative routes e.g. environment variables
    'aws.credentials.provider.basic.accesskeyid': 'aws_access_key_id',
    'aws.credentials.provider.basic.secretkey': 'aws_secret_access_key',
    'aws.endpoint': 'http://localhost:4567'
}

kds_sink = KinesisStreamsSink.builder() \
    .set_kinesis_client_properties(sink_properties) \                      # Required
    .set_serialization_schema(SimpleStringSchema()) \                      # Required
    .set_partition_key_generator(PartitionKeyGenerator.fixed()) \          # Required
    .set_stream_name("your-stream-name") \                                 # Required
    .set_fail_on_error(False) \                                            # Optional
    .set_max_batch_size(500) \                                             # Optional
    .set_max_in_flight_requests(50) \                                      # Optional
    .set_max_buffered_requests(10000) \                                    # Optional
    .set_max_batch_size_in_bytes(5 * 1024 * 1024) \                        # Optional
    .set_max_time_in_buffer_ms(5000) \                                     # Optional
    .set_max_record_size_in_bytes(1 * 1024 * 1024) \                       # Optional
    .build()

simple_string_stream = ...
simple_string_stream.sink_to(kds_sink)

```

`# Required
sink_properties = {
    # Required
    'aws.region': 'us-east-1',
    # Optional, provide via alternative routes e.g. environment variables
    'aws.credentials.provider.basic.accesskeyid': 'aws_access_key_id',
    'aws.credentials.provider.basic.secretkey': 'aws_secret_access_key',
    'aws.endpoint': 'http://localhost:4567'
}

kds_sink = KinesisStreamsSink.builder() \
    .set_kinesis_client_properties(sink_properties) \                      # Required
    .set_serialization_schema(SimpleStringSchema()) \                      # Required
    .set_partition_key_generator(PartitionKeyGenerator.fixed()) \          # Required
    .set_stream_name("your-stream-name") \                                 # Required
    .set_fail_on_error(False) \                                            # Optional
    .set_max_batch_size(500) \                                             # Optional
    .set_max_in_flight_requests(50) \                                      # Optional
    .set_max_buffered_requests(10000) \                                    # Optional
    .set_max_batch_size_in_bytes(5 * 1024 * 1024) \                        # Optional
    .set_max_time_in_buffer_ms(5000) \                                     # Optional
    .set_max_record_size_in_bytes(1 * 1024 * 1024) \                       # Optional
    .build()

simple_string_stream = ...
simple_string_stream.sink_to(kds_sink)
`

The above is a simple example of using the Kinesis sink. Begin by creating a java.util.Properties instance with the AWS_REGION, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY configured. You can then construct the sink with the builder. The default values for the optional configurations are shown above. Some of these values have been set as a result of configuration on KDS.

`java.util.Properties`
`AWS_REGION`
`AWS_ACCESS_KEY_ID`
`AWS_SECRET_ACCESS_KEY`

You will always need to specify your serialization schema and logic for generating a partition key from a record.


Some or all of the records in a request may fail to be persisted by Kinesis Data Streams for a number of reasons. If failOnError is on, then a runtime exception will be raised. Otherwise those records will be requeued in the buffer for retry.

`failOnError`

The Kinesis Sink provides some metrics through Flink’s metrics system to analyze the behavior of the connector. A list of all exposed metrics may be found here.


The sink default maximum record size is 1MB and maximum batch size is 5MB in line with the Kinesis Data Streams maximums. The AWS documentation detailing these maximums may be found here.


### Kinesis Sinks and Fault Tolerance#


The sink is designed to participate in Flink’s checkpointing to provide at-least-once processing guarantees. It does this by completing any in-flight requests while taking a checkpoint. This effectively assures all requests that were triggered before the checkpoint have been successfully delivered to Kinesis Data Streams, before proceeding to process more records.


If Flink needs to restore from a checkpoint (or savepoint), data that has been written since that checkpoint will be written to Kinesis again, leading to duplicates in the stream. Moreover, the sink uses the PutRecords API call internally, which does not guarantee to maintain the order of events.

`PutRecords`

### Backpressure#


Backpressure in the sink arises as the sink buffer fills up and writes to the sink
begins to exhibit blocking behaviour. More information on the rate restrictions of Kinesis Data Streams may be
found at Quotas and Limits.


You generally reduce backpressure by increasing the size of the internal queue:


```
KinesisStreamsSink<String> kdsSink =
    KinesisStreamsSink.<String>builder()
        ...
        .setMaxBufferedRequests(10_000)
        ...

```

`KinesisStreamsSink<String> kdsSink =
    KinesisStreamsSink.<String>builder()
        ...
        .setMaxBufferedRequests(10_000)
        ...
`

```
kds_sink = KinesisStreamsSink.builder() \
    .set_max_buffered_requests(10000) \
    .build()

```

`kds_sink = KinesisStreamsSink.builder() \
    .set_max_buffered_requests(10000) \
    .build()
`

## Kinesis Producer#


> 
  The old Kinesis sink org.apache.flink.streaming.connectors.kinesis.FlinkKinesisProducer is deprecated and may be removed with a future release of Flink, please use Kinesis Sink instead.


`org.apache.flink.streaming.connectors.kinesis.FlinkKinesisProducer`

The new sink uses the AWS v2 SDK for Java whereas the old sink uses the Kinesis Producer Library. Because of this, the new Kinesis sink does not support aggregation.


## Using Custom Kinesis Endpoints#


It is sometimes desirable to have Flink operate as a source or sink against a Kinesis VPC endpoint or a non-AWS
Kinesis endpoint such as Kinesalite; this is especially useful when performing
functional testing of a Flink application. The AWS endpoint that would normally be inferred by the AWS region set in the
Flink configuration must be overridden via a configuration property.


To override the AWS endpoint, set the AWSConfigConstants.AWS_ENDPOINT and AWSConfigConstants.AWS_REGION properties. The region will be used to sign the endpoint URL.

`AWSConfigConstants.AWS_ENDPOINT`
`AWSConfigConstants.AWS_REGION`

```
Properties config = new Properties();
config.put(AWSConfigConstants.AWS_REGION, "us-east-1");
config.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
config.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");
config.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4567");

```

`Properties config = new Properties();
config.put(AWSConfigConstants.AWS_REGION, "us-east-1");
config.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
config.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");
config.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4567");
`

```
val config = new Properties()
config.put(AWSConfigConstants.AWS_REGION, "us-east-1")
config.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
config.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")
config.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4567")

```

`val config = new Properties()
config.put(AWSConfigConstants.AWS_REGION, "us-east-1")
config.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
config.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")
config.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4567")
`

```
config = {
    'aws.region': 'us-east-1',
    'aws.credentials.provider.basic.accesskeyid': 'aws_access_key_id',
    'aws.credentials.provider.basic.secretkey': 'aws_secret_access_key',
    'aws.endpoint': 'http://localhost:4567'
}

```

`config = {
    'aws.region': 'us-east-1',
    'aws.credentials.provider.basic.accesskeyid': 'aws_access_key_id',
    'aws.credentials.provider.basic.secretkey': 'aws_secret_access_key',
    'aws.endpoint': 'http://localhost:4567'
}
`

 Back to top
