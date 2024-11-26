# DynamoDB


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Amazon DynamoDB Connector#


The DynamoDB connector allows users to read/write from Amazon DynamoDB.


As a source, the connector allows users to read change data capture stream from DynamoDB tables using Amazon DynamoDB Streams.


As a sink, the connector allows users to write directly to Amazon DynamoDB tables using the BatchWriteItem API.


## Dependency#


Apache Flink ships the connector for users to utilize.


To use the connector, add the following Maven dependency to your project:


Only available for stable versions.


## Amazon DynamoDB Streams Source#


The DynamoDB Streams source reads from Amazon DynamoDB Streams using the AWS v2 SDK for Java.
Follow the instructions from the AWS docs to set up and configure the change data capture stream.


The actual events streamed to the DynamoDB Stream depend on the StreamViewType specified by the DynamoDB Stream itself.
See AWS docs for more information.

`StreamViewType`

### Usage#


The DynamoDbStreamsSource provides a fluent builder to construct an instance of the DynamoDbStreamsSource.
The code snippet below illustrates how to do so.

`DynamoDbStreamsSource`
`DynamoDbStreamsSource`

```
// Configure the DynamodbStreamsSource
Configuration sourceConfig = new Configuration();
sourceConfig.set(DynamodbStreamsSourceConfigConstants.STREAM_INITIAL_POSITION, DynamodbStreamsSourceConfigConstants.InitialPosition.TRIM_HORIZON); // This is optional, by default connector will read from LATEST

// Create a new DynamoDbStreamsSource to read from the specified DynamoDB Stream.
DynamoDbStreamsSource<String> dynamoDbStreamsSource = 
        DynamoDbStreamsSource.<String>builder()
                .setStreamArn("arn:aws:dynamodb:us-east-1:1231231230:table/test/stream/2024-04-11T07:14:19.380")
                .setSourceConfig(sourceConfig)
                // User must implement their own deserialization schema to translate change data capture events into custom data types    
                .setDeserializationSchema(dynamodbDeserializationSchema) 
                .build();

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Specify watermarking strategy and the name of the DynamoDB Streams Source operator.
// Specify return type using TypeInformation.
// Specify UID of operator in line with Flink best practice.
DataStream<String> cdcEventsWithEventTimeWatermarks = env.fromSource(dynamoDbStreamsSource, WatermarkStrategy.<String>forMonotonousTimestamps().withIdleness(Duration.ofSeconds(1)), "DynamoDB Streams source")
        .returns(TypeInformation.of(String.class))
        .uid("custom-uid");

```

`// Configure the DynamodbStreamsSource
Configuration sourceConfig = new Configuration();
sourceConfig.set(DynamodbStreamsSourceConfigConstants.STREAM_INITIAL_POSITION, DynamodbStreamsSourceConfigConstants.InitialPosition.TRIM_HORIZON); // This is optional, by default connector will read from LATEST

// Create a new DynamoDbStreamsSource to read from the specified DynamoDB Stream.
DynamoDbStreamsSource<String> dynamoDbStreamsSource = 
        DynamoDbStreamsSource.<String>builder()
                .setStreamArn("arn:aws:dynamodb:us-east-1:1231231230:table/test/stream/2024-04-11T07:14:19.380")
                .setSourceConfig(sourceConfig)
                // User must implement their own deserialization schema to translate change data capture events into custom data types    
                .setDeserializationSchema(dynamodbDeserializationSchema) 
                .build();

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Specify watermarking strategy and the name of the DynamoDB Streams Source operator.
// Specify return type using TypeInformation.
// Specify UID of operator in line with Flink best practice.
DataStream<String> cdcEventsWithEventTimeWatermarks = env.fromSource(dynamoDbStreamsSource, WatermarkStrategy.<String>forMonotonousTimestamps().withIdleness(Duration.ofSeconds(1)), "DynamoDB Streams source")
        .returns(TypeInformation.of(String.class))
        .uid("custom-uid");
`

```
// Configure the DynamodbStreamsSource
val sourceConfig = new Configuration()
sourceConfig.set(DynamodbStreamsSourceConfigConstants.STREAM_INITIAL_POSITION, DynamodbStreamsSourceConfigConstants.InitialPosition.TRIM_HORIZON) // This is optional, by default connector will read from LATEST

// Create a new DynamoDbStreamsSource to read from the specified DynamoDB Stream.
val dynamoDbStreamsSource = DynamoDbStreamsSource.builder[String]()
  .setStreamArn("arn:aws:dynamodb:us-east-1:1231231230:table/test/stream/2024-04-11T07:14:19.380")
  .setSourceConfig(sourceConfig)
  // User must implement their own deserialization schema to translate change data capture events into custom data types    
  .setDeserializationSchema(dynamodbDeserializationSchema)
  .build()

val env = StreamExecutionEnvironment.getExecutionEnvironment()

// Specify watermarking strategy and the name of the DynamoDB Streams Source operator.
// Specify return type using TypeInformation.
// Specify UID of operator in line with Flink best practice.
val cdcEventsWithEventTimeWatermarks = env.fromSource(dynamoDbStreamsSource, WatermarkStrategy.<String>forMonotonousTimestamps().withIdleness(Duration.ofSeconds(1)), "DynamoDB Streams source")
  .uid("custom-uid")

```

`// Configure the DynamodbStreamsSource
val sourceConfig = new Configuration()
sourceConfig.set(DynamodbStreamsSourceConfigConstants.STREAM_INITIAL_POSITION, DynamodbStreamsSourceConfigConstants.InitialPosition.TRIM_HORIZON) // This is optional, by default connector will read from LATEST

// Create a new DynamoDbStreamsSource to read from the specified DynamoDB Stream.
val dynamoDbStreamsSource = DynamoDbStreamsSource.builder[String]()
  .setStreamArn("arn:aws:dynamodb:us-east-1:1231231230:table/test/stream/2024-04-11T07:14:19.380")
  .setSourceConfig(sourceConfig)
  // User must implement their own deserialization schema to translate change data capture events into custom data types    
  .setDeserializationSchema(dynamodbDeserializationSchema)
  .build()

val env = StreamExecutionEnvironment.getExecutionEnvironment()

// Specify watermarking strategy and the name of the DynamoDB Streams Source operator.
// Specify return type using TypeInformation.
// Specify UID of operator in line with Flink best practice.
val cdcEventsWithEventTimeWatermarks = env.fromSource(dynamoDbStreamsSource, WatermarkStrategy.<String>forMonotonousTimestamps().withIdleness(Duration.ofSeconds(1)), "DynamoDB Streams source")
  .uid("custom-uid")
`

The above is a simple example of using the DynamoDbStreamsSource.

`DynamoDbStreamsSource`
* The DynamoDB Stream being read from is specified using the stream ARN.
* Configuration for the Source is supplied using an instance of Flink’s Configuration class.
The configuration keys can be taken from AWSConfigOptions (AWS-specific configuration) and DynamodbStreamsSourceConfigConstants (DynamoDB Streams Source configuration).
* The example specifies the starting position as TRIM_HORIZON (see Configuring Starting Position for more information).
* The deserialization format is as SimpleStringSchema (see Deserialization Schema for more information).
* The distribution of shards across subtasks is controlled using the UniformShardAssigner (see Shard Assignment Strategy for more information).
* The example also specifies an increasing WatermarkStrategy, which means each record will be tagged with event time specified using approximateCreationDateTime.
Monotonically increasing watermarks will be generated, and subtasks will be considered idle if no record is emitted after 1 second.
`Source`
`Configuration`
`AWSConfigOptions`
`DynamodbStreamsSourceConfigConstants`
`TRIM_HORIZON`
`SimpleStringSchema`
`UniformShardAssigner`
`WatermarkStrategy`
`approximateCreationDateTime`

### Configuring Starting Position#


To specify the starting position of the DynamodbStreamsSource, users can set the DynamodbStreamsSourceConfigConstants.STREAM_INITIAL_POSITION in configuration.

`DynamodbStreamsSource`
`DynamodbStreamsSourceConfigConstants.STREAM_INITIAL_POSITION`
* LATEST: read all shards of the stream starting from the latest record.
* TRIM_HORIZON: read all shards of the stream starting from the earliest record possible (data is trimmed by DynamoDB after 24 hours).
`LATEST`
`TRIM_HORIZON`

### Deserialization Schema#


The DynamoDbStreamsSource provides the DynamoDbStreamsDeserializationSchema<T> interface to allow users to implement their own
deserialization schema to convert DynamoDB change data capture events into custom event types.

`DynamoDbStreamsSource`
`DynamoDbStreamsDeserializationSchema<T>`

The DynamoDbStreamsDeserializationSchema<T>#deserialize method takes in an instance of Record from the DynamoDB model.
The Record can contain different content, depending on the configuration of the DynamoDB Stream. See AWS docs for more information.

`DynamoDbStreamsDeserializationSchema<T>#deserialize`
`Record`
`Record`

### Event Ordering#


Events are written into DynamoDB Streams, maintaining ordering within the same primary key.
This is done by ensuring that events within the same primary key are written to the same shard lineage.
When there are shard splits (one parent shard splitting into two child shards), the ordering will be maintained as long as the parent shard is read completely before starting to read from the child shards.


The DynamoDbStreamsSource ensures that shards are assigned in a manner that respects parent-child shard ordering.
This means that the shard will only be passed to the shard assigner if the parent shard has been completely read.
This helps to ensure that the events from the change data capture stream are read in-order within the same DynamoDB primary key.

`DynamoDbStreamsSource`

### Shard Assignment Strategy#


The UniformShardAssigner allocates the shards of the DynamoDB Stream evenly across the parallel subtasks of the source operator.
DynamoDB Stream shards are ephemeral and are created and deleted automatically, as required.
The UniformShardAssigner allocates new shards to the subtask with the lowest number of currently allocated shards.

`UniformShardAssigner`
`UniformShardAssigner`

Users can also implement their own shard assignment strategy by implementing the DynamoDbStreamsShardAssigner interface.

`DynamoDbStreamsShardAssigner`

### Configuration#


#### Retry Strategy#


The DynamoDbStreamsSource interacts with Amazon DynamoDB using the AWS v2 SDK for Java.

`DynamoDbStreamsSource`

The retry strategy used by the AWS SDK client can be tuned using the following configuration options:

* DYNAMODB_STREAMS_RETRY_COUNT: Maximum number of API retries on retryable errors, before it will restart the Flink job.
* DYNAMODB_STREAMS_EXPONENTIAL_BACKOFF_MIN_DELAY: The base delay used for calculation of the exponential backoff.
* DYNAMODB_STREAMS_EXPONENTIAL_BACKOFF_MAX_DELAY: The maximum delay for exponential backoff.
`DYNAMODB_STREAMS_RETRY_COUNT`
`DYNAMODB_STREAMS_EXPONENTIAL_BACKOFF_MIN_DELAY`
`DYNAMODB_STREAMS_EXPONENTIAL_BACKOFF_MAX_DELAY`

#### Shard Discovery#


The DynamoDbStreamsSource periodically discovers newly created shards on the DynamoDB Stream. This can come from shard splitting, or shard rotations.
By default this is set to discover shards every 60 seconds. However, users can customize this to a smaller value by configuring the SHARD_DISCOVERY_INTERVAL.

`DynamoDbStreamsSource`
`SHARD_DISCOVERY_INTERVAL`

There is an issue for shard discovery where the shard graph returned from DynamoDB might have inconsistencies.
In this case, the DynamoDbStreamsSource automatically detects the inconsistency and retries the shard discovery process.
The maximum number of retries can be configured using DESCRIBE_STREAM_INCONSISTENCY_RESOLUTION_RETRY_COUNT.

`DynamoDbStreamsSource`
`DESCRIBE_STREAM_INCONSISTENCY_RESOLUTION_RETRY_COUNT`

## Amazon DynamoDB Sink#


The DynamoDB sink writes to Amazon DynamoDB using the AWS v2 SDK for Java. Follow the instructions from the Amazon DynamoDB Developer Guide
to setup a table.


```
Properties sinkProperties = new Properties();
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1");
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");

ElementConverter<InputType, DynamoDbWriteRequest> elementConverter = new CustomElementConverter();

DynamoDbSink<String> dynamoDbSink = 
    DynamoDbSink.<InputType>builder()
        .setDynamoDbProperties(sinkProperties)              // Required
        .setTableName("my-dynamodb-table")                  // Required
        .setElementConverter(elementConverter)              // Required
        .setOverwriteByPartitionKeys(singletonList("key"))  // Optional  
        .setFailOnError(false)                              // Optional
        .setMaxBatchSize(25)                                // Optional
        .setMaxInFlightRequests(50)                         // Optional
        .setMaxBufferedRequests(10_000)                     // Optional
        .setMaxTimeInBufferMS(5000)                         // Optional
        .build();

flinkStream.sinkTo(dynamoDbSink);

```

`Properties sinkProperties = new Properties();
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1");
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");

ElementConverter<InputType, DynamoDbWriteRequest> elementConverter = new CustomElementConverter();

DynamoDbSink<String> dynamoDbSink = 
    DynamoDbSink.<InputType>builder()
        .setDynamoDbProperties(sinkProperties)              // Required
        .setTableName("my-dynamodb-table")                  // Required
        .setElementConverter(elementConverter)              // Required
        .setOverwriteByPartitionKeys(singletonList("key"))  // Optional  
        .setFailOnError(false)                              // Optional
        .setMaxBatchSize(25)                                // Optional
        .setMaxInFlightRequests(50)                         // Optional
        .setMaxBufferedRequests(10_000)                     // Optional
        .setMaxTimeInBufferMS(5000)                         // Optional
        .build();

flinkStream.sinkTo(dynamoDbSink);
`

```
val sinkProperties = new Properties()
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1")
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")

val elementConverter = new CustomElementConverter();

val dynamoDbSink =
    DynamoDbSink.<InputType>builder()
        .setDynamoDbProperties(sinkProperties)              // Required
        .setTableName("my-dynamodb-table")                  // Required
        .setElementConverter(elementConverter)              // Required
        .setOverwriteByPartitionKeys(singletonList("key"))  // Optional    
        .setFailOnError(false)                              // Optional
        .setMaxBatchSize(25)                                // Optional
        .setMaxInFlightRequests(50)                         // Optional
        .setMaxBufferedRequests(10_000)                     // Optional
        .setMaxTimeInBufferMS(5000)                         // Optional
        .build()

flinkStream.sinkTo(dynamoDbSink)

```

`val sinkProperties = new Properties()
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1")
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")

val elementConverter = new CustomElementConverter();

val dynamoDbSink =
    DynamoDbSink.<InputType>builder()
        .setDynamoDbProperties(sinkProperties)              // Required
        .setTableName("my-dynamodb-table")                  // Required
        .setElementConverter(elementConverter)              // Required
        .setOverwriteByPartitionKeys(singletonList("key"))  // Optional    
        .setFailOnError(false)                              // Optional
        .setMaxBatchSize(25)                                // Optional
        .setMaxInFlightRequests(50)                         // Optional
        .setMaxBufferedRequests(10_000)                     // Optional
        .setMaxTimeInBufferMS(5000)                         // Optional
        .build()

flinkStream.sinkTo(dynamoDbSink)
`

### Configurations#


Flink’s DynamoDB sink is created by using the static builder DynamoDBSink.<InputType>builder().

`DynamoDBSink.<InputType>builder()`
1. setDynamoDbProperties(Properties sinkProperties)

Required.
Supplies credentials, region and other parameters to the DynamoDB client.


2. setTableName(String tableName)

Required.
Name of the table to sink to.


3. setElementConverter(ElementConverter<InputType, DynamoDbWriteRequest> elementConverter)

Required.
Converts generic records of type InputType to DynamoDbWriteRequest.


4. setOverwriteByPartitionKeys(List partitionKeys)

Optional. Default: [].
Used to deduplicate write requests within each batch pushed to DynamoDB.


5. setFailOnError(boolean failOnError)

Optional. Default: false.
Whether failed requests to write records are treated as fatal exceptions in the sink.


6. setMaxBatchSize(int maxBatchSize)

Optional. Default: 25.
Maximum size of a batch to write.


7. setMaxInFlightRequests(int maxInFlightRequests)

Optional. Default: 50.
The maximum number of in flight requests allowed before the sink applies backpressure.


8. setMaxBufferedRequests(int maxBufferedRequests)

Optional. Default: 10_000.
The maximum number of records that may be buffered in the sink before backpressure is applied.


9. setMaxBatchSizeInBytes(int maxBatchSizeInBytes)

N/A.
This configuration is not supported, see FLINK-29854.


10. setMaxTimeInBufferMS(int maxTimeInBufferMS)

Optional. Default: 5000.
The maximum time a record may stay in the sink before being flushed.


11. setMaxRecordSizeInBytes(int maxRecordSizeInBytes)

N/A.
This configuration is not supported, see FLINK-29854.


12. build()

Constructs and returns the DynamoDB sink.


* Required.
* Supplies credentials, region and other parameters to the DynamoDB client.
* Required.
* Name of the table to sink to.
* Required.
* Converts generic records of type InputType to DynamoDbWriteRequest.
`InputType`
`DynamoDbWriteRequest`
* Optional. Default: [].
* Used to deduplicate write requests within each batch pushed to DynamoDB.
* Optional. Default: false.
* Whether failed requests to write records are treated as fatal exceptions in the sink.
`false`
* Optional. Default: 25.
* Maximum size of a batch to write.
`25`
* Optional. Default: 50.
* The maximum number of in flight requests allowed before the sink applies backpressure.
`50`
* Optional. Default: 10_000.
* The maximum number of records that may be buffered in the sink before backpressure is applied.
`10_000`
* N/A.
* This configuration is not supported, see FLINK-29854.
* Optional. Default: 5000.
* The maximum time a record may stay in the sink before being flushed.
`5000`
* N/A.
* This configuration is not supported, see FLINK-29854.
* Constructs and returns the DynamoDB sink.

### Element Converter#


An element converter is used to convert from a record in the DataStream to a DynamoDbWriteRequest which the sink will write to the destination DynamoDB table. The DynamoDB sink allows the user to supply a custom element converter, or use the provided
DefaultDynamoDbElementConverter which extracts item schema from element class, this requires the element class to be of composite type (i.e. Pojo, Tuple or Row). In case TypeInformation of the elements is present the schema is eagerly constructed by using DynamoDbTypeInformedElementConverter as in new DynamoDbTypeInformedElementConverter(TypeInformation.of(MyPojo.class)).

`DefaultDynamoDbElementConverter`
`DynamoDbTypeInformedElementConverter`
`new DynamoDbTypeInformedElementConverter(TypeInformation.of(MyPojo.class))`

Alternatively when you are working with @DynamoDbBean objects you can use DynamoDbBeanElementConverter. For more information on supported
annotations see here.

`@DynamoDbBean`
`DynamoDbBeanElementConverter`

A sample application using a custom ElementConverter can be found here. A sample application using the DynamoDbBeanElementConverter can be found here.

`ElementConverter`
`DynamoDbBeanElementConverter`

### Using Custom DynamoDB Endpoints#


It is sometimes desirable to have Flink operate as a consumer or producer against a DynamoDB VPC endpoint or a non-AWS
DynamoDB endpoint such as Localstack; this is especially useful when performing
functional testing of a Flink application. The AWS endpoint that would normally be inferred by the AWS region set in the
Flink configuration must be overridden via a configuration property.


To override the AWS endpoint, set the AWSConfigConstants.AWS_ENDPOINT and AWSConfigConstants.AWS_REGION properties. The region will be used to sign the endpoint URL.

`AWSConfigConstants.AWS_ENDPOINT`
`AWSConfigConstants.AWS_REGION`

```
Properties producerConfig = new Properties();
producerConfig.put(AWSConfigConstants.AWS_REGION, "eu-west-1");
producerConfig.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
producerConfig.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");
producerConfig.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4566");

```

`Properties producerConfig = new Properties();
producerConfig.put(AWSConfigConstants.AWS_REGION, "eu-west-1");
producerConfig.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
producerConfig.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");
producerConfig.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4566");
`

```
val producerConfig = new Properties()
producerConfig.put(AWSConfigConstants.AWS_REGION, "eu-west-1")
producerConfig.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
producerConfig.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")
producerConfig.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4566")

```

`val producerConfig = new Properties()
producerConfig.put(AWSConfigConstants.AWS_REGION, "eu-west-1")
producerConfig.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
producerConfig.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")
producerConfig.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4566")
`

 Back to top
