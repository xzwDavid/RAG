# Firehose


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Amazon Kinesis Data Firehose Sink#


The Firehose sink writes to Amazon Kinesis Data Firehose.


Follow the instructions from the Amazon Kinesis Data Firehose Developer Guide
to setup a Kinesis Data Firehose delivery stream.


To use the connector, add the following Maven dependency to your project:


Only available for stable versions.




In order to use the  in PyFlink jobs, the following
dependencies are required:



Version
PyFlink JAR



flink-connector-aws-kinesis-firehose
Only available for stable releases.




See Python dependency management
for more details on how to use JARs in PyFlink.




The KinesisFirehoseSink uses AWS v2 SDK for Java to write data from a Flink stream into a Firehose delivery stream.

`KinesisFirehoseSink`

```
Properties sinkProperties = new Properties();
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1");
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");

KinesisFirehoseSink<String> kdfSink =
    KinesisFirehoseSink.<String>builder()
        .setFirehoseClientProperties(sinkProperties)      // Required
        .setSerializationSchema(new SimpleStringSchema()) // Required
        .setDeliveryStreamName("your-stream-name")        // Required
        .setFailOnError(false)                            // Optional
        .setMaxBatchSize(500)                             // Optional
        .setMaxInFlightRequests(50)                       // Optional
        .setMaxBufferedRequests(10_000)                   // Optional
        .setMaxBatchSizeInBytes(4 * 1024 * 1024)          // Optional
        .setMaxTimeInBufferMS(5000)                       // Optional
        .setMaxRecordSizeInBytes(1000 * 1024)             // Optional
        .build();

flinkStream.sinkTo(kdfSink);

```

`Properties sinkProperties = new Properties();
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1");
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");

KinesisFirehoseSink<String> kdfSink =
    KinesisFirehoseSink.<String>builder()
        .setFirehoseClientProperties(sinkProperties)      // Required
        .setSerializationSchema(new SimpleStringSchema()) // Required
        .setDeliveryStreamName("your-stream-name")        // Required
        .setFailOnError(false)                            // Optional
        .setMaxBatchSize(500)                             // Optional
        .setMaxInFlightRequests(50)                       // Optional
        .setMaxBufferedRequests(10_000)                   // Optional
        .setMaxBatchSizeInBytes(4 * 1024 * 1024)          // Optional
        .setMaxTimeInBufferMS(5000)                       // Optional
        .setMaxRecordSizeInBytes(1000 * 1024)             // Optional
        .build();

flinkStream.sinkTo(kdfSink);
`

```
val sinkProperties = new Properties()
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1")
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")

val kdfSink =
    KinesisFirehoseSink.<String>builder()
        .setFirehoseClientProperties(sinkProperties)      // Required
        .setSerializationSchema(new SimpleStringSchema()) // Required
        .setDeliveryStreamName("your-stream-name")        // Required
        .setFailOnError(false)                            // Optional
        .setMaxBatchSize(500)                             // Optional
        .setMaxInFlightRequests(50)                       // Optional
        .setMaxBufferedRequests(10_000)                   // Optional
        .setMaxBatchSizeInBytes(4 * 1024 * 1024)          // Optional
        .setMaxTimeInBufferMS(5000)                       // Optional
        .setMaxRecordSizeInBytes(1000 * 1024)             // Optional
        .build()

flinkStream.sinkTo(kdfSink)

```

`val sinkProperties = new Properties()
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1")
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")

val kdfSink =
    KinesisFirehoseSink.<String>builder()
        .setFirehoseClientProperties(sinkProperties)      // Required
        .setSerializationSchema(new SimpleStringSchema()) // Required
        .setDeliveryStreamName("your-stream-name")        // Required
        .setFailOnError(false)                            // Optional
        .setMaxBatchSize(500)                             // Optional
        .setMaxInFlightRequests(50)                       // Optional
        .setMaxBufferedRequests(10_000)                   // Optional
        .setMaxBatchSizeInBytes(4 * 1024 * 1024)          // Optional
        .setMaxTimeInBufferMS(5000)                       // Optional
        .setMaxRecordSizeInBytes(1000 * 1024)             // Optional
        .build()

flinkStream.sinkTo(kdfSink)
`

```
sink_properties = {
    # Required
    'aws.region': 'eu-west-1',
    # Optional, provide via alternative routes e.g. environment variables
    'aws.credentials.provider.basic.accesskeyid': 'aws_access_key_id',
    'aws.credentials.provider.basic.secretkey': 'aws_secret_access_key'
}

kdf_sink = KinesisFirehoseSink.builder() \
    .set_firehose_client_properties(sink_properties) \     # Required
    .set_serialization_schema(SimpleStringSchema()) \      # Required
    .set_delivery_stream_name('your-stream-name') \        # Required
    .set_fail_on_error(False) \                            # Optional
    .set_max_batch_size(500) \                             # Optional
    .set_max_in_flight_requests(50) \                      # Optional
    .set_max_buffered_requests(10000) \                    # Optional
    .set_max_batch_size_in_bytes(5 * 1024 * 1024) \        # Optional
    .set_max_time_in_buffer_ms(5000) \                     # Optional
    .set_max_record_size_in_bytes(1 * 1024 * 1024) \       # Optional
    .build()

```

`sink_properties = {
    # Required
    'aws.region': 'eu-west-1',
    # Optional, provide via alternative routes e.g. environment variables
    'aws.credentials.provider.basic.accesskeyid': 'aws_access_key_id',
    'aws.credentials.provider.basic.secretkey': 'aws_secret_access_key'
}

kdf_sink = KinesisFirehoseSink.builder() \
    .set_firehose_client_properties(sink_properties) \     # Required
    .set_serialization_schema(SimpleStringSchema()) \      # Required
    .set_delivery_stream_name('your-stream-name') \        # Required
    .set_fail_on_error(False) \                            # Optional
    .set_max_batch_size(500) \                             # Optional
    .set_max_in_flight_requests(50) \                      # Optional
    .set_max_buffered_requests(10000) \                    # Optional
    .set_max_batch_size_in_bytes(5 * 1024 * 1024) \        # Optional
    .set_max_time_in_buffer_ms(5000) \                     # Optional
    .set_max_record_size_in_bytes(1 * 1024 * 1024) \       # Optional
    .build()
`

## Configurations#


Flink’s Firehose sink is created by using the static builder KinesisFirehoseSink.<InputType>builder().

`KinesisFirehoseSink.<InputType>builder()`
1. setFirehoseClientProperties(Properties sinkProperties)

Required.
Supplies credentials, region and other parameters to the Firehose client.


2. setSerializationSchema(SerializationSchema serializationSchema)

Required.
Supplies a serialization schema to the Sink. This schema is used to serialize elements before sending to Firehose.


3. setDeliveryStreamName(String deliveryStreamName)

Required.
Name of the delivery stream to sink to.


4. setFailOnError(boolean failOnError)

Optional. Default: false.
Whether failed requests to write records to Firehose are treated as fatal exceptions in the sink.


5. setMaxBatchSize(int maxBatchSize)

Optional. Default: 500.
Maximum size of a batch to write to Firehose.


6. setMaxInFlightRequests(int maxInFlightRequests)

Optional. Default: 50.
The maximum number of in flight requests allowed before the sink applies backpressure.


7. setMaxBufferedRequests(int maxBufferedRequests)

Optional. Default: 10_000.
The maximum number of records that may be buffered in the sink before backpressure is applied.


8. setMaxBatchSizeInBytes(int maxBatchSizeInBytes)

Optional. Default: 4 * 1024 * 1024.
The maximum size (in bytes) a batch may become. All batches sent will be smaller than or equal to this size.


9. setMaxTimeInBufferMS(int maxTimeInBufferMS)

Optional. Default: 5000.
The maximum time a record may stay in the sink before being flushed.


10. setMaxRecordSizeInBytes(int maxRecordSizeInBytes)

Optional. Default: 1000 * 1024.
The maximum record size that the sink will accept, records larger than this will be automatically rejected.


11. build()

Constructs and returns the Firehose sink.


* Required.
* Supplies credentials, region and other parameters to the Firehose client.
* Required.
* Supplies a serialization schema to the Sink. This schema is used to serialize elements before sending to Firehose.
* Required.
* Name of the delivery stream to sink to.
* Optional. Default: false.
* Whether failed requests to write records to Firehose are treated as fatal exceptions in the sink.
`false`
* Optional. Default: 500.
* Maximum size of a batch to write to Firehose.
`500`
* Optional. Default: 50.
* The maximum number of in flight requests allowed before the sink applies backpressure.
`50`
* Optional. Default: 10_000.
* The maximum number of records that may be buffered in the sink before backpressure is applied.
`10_000`
* Optional. Default: 4 * 1024 * 1024.
* The maximum size (in bytes) a batch may become. All batches sent will be smaller than or equal to this size.
`4 * 1024 * 1024`
* Optional. Default: 5000.
* The maximum time a record may stay in the sink before being flushed.
`5000`
* Optional. Default: 1000 * 1024.
* The maximum record size that the sink will accept, records larger than this will be automatically rejected.
`1000 * 1024`
* Constructs and returns the Firehose sink.

## Using Custom Firehose Endpoints#


It is sometimes desirable to have Flink operate as a consumer or producer against a Firehose VPC endpoint or a non-AWS
Firehose endpoint such as Localstack; this is especially useful when performing
functional testing of a Flink application. The AWS endpoint that would normally be inferred by the AWS region set in the
Flink configuration must be overridden via a configuration property.


To override the AWS endpoint, set the AWSConfigConstants.AWS_ENDPOINT and AWSConfigConstants.AWS_REGION properties. The region will be used to sign the endpoint URL.

`AWSConfigConstants.AWS_ENDPOINT`
`AWSConfigConstants.AWS_REGION`

```
Properties producerConfig = new Properties();
producerConfig.put(AWSConfigConstants.AWS_REGION, "us-east-1");
producerConfig.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
producerConfig.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");
producerConfig.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4566");

```

`Properties producerConfig = new Properties();
producerConfig.put(AWSConfigConstants.AWS_REGION, "us-east-1");
producerConfig.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
producerConfig.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");
producerConfig.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4566");
`

```
val producerConfig = new Properties()
producerConfig.put(AWSConfigConstants.AWS_REGION, "us-east-1")
producerConfig.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
producerConfig.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")
producerConfig.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4566")

```

`val producerConfig = new Properties()
producerConfig.put(AWSConfigConstants.AWS_REGION, "us-east-1")
producerConfig.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
producerConfig.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")
producerConfig.put(AWSConfigConstants.AWS_ENDPOINT, "http://localhost:4566")
`

```
producer_config = {
    'aws.region': 'us-east-1',
    'aws.credentials.provider.basic.accesskeyid': 'aws_access_key_id',
    'aws.credentials.provider.basic.secretkey': 'aws_secret_access_key',
    'aws.endpoint': 'http://localhost:4566'
}

```

`producer_config = {
    'aws.region': 'us-east-1',
    'aws.credentials.provider.basic.accesskeyid': 'aws_access_key_id',
    'aws.credentials.provider.basic.secretkey': 'aws_secret_access_key',
    'aws.endpoint': 'http://localhost:4566'
}
`

 Back to top
