# SQS


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Amazon SQS Sink#


The SQS sink writes to Amazon SQS using the AWS v2 SDK for Java. Follow the instructions from the Amazon SQS Developer Guide
to setup a SQS message queue.


To use the connector, add the following Maven dependency to your project:


Only available for stable versions.


```
Properties sinkProperties = new Properties();
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1");
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");

// Optional, use following if you want to provide access via AssumeRole, Please make sure given IAM role has "sqs:SendMessage" permission
sinkProperties.setProperty(AWSConfigConstants.AWS_CREDENTIALS_PROVIDER, "ASSUME_ROLE");
sinkProperties.setProperty(AWSConfigConstants.AWS_ROLE_ARN, "replace-this-with-IAMRole-arn");
sinkProperties.setProperty(AWSConfigConstants.AWS_ROLE_SESSION_NAME, "any-session-name-string");

SqsSink<String> sqsSink =
        SqsSink.<String>builder()
                .setSerializationSchema(new SimpleStringSchema())                // Required
                .setSqsUrl("https://sqs.us-east-1.amazonaws.com/xxxx/test-sqs")  // Required
                .setSqsClientProperties(sinkProperties)                          // Required
                .setFailOnError(false)                                           // Optional
                .setMaxBatchSize(10)                                             // Optional
                .setMaxInFlightRequests(50)                                      // Optional
                .setMaxBufferedRequests(1_000)                                   // Optional
                .setMaxBatchSizeInBytes(256 * 1024)                         // Optional
                .setMaxTimeInBufferMS(5000)                                      // Optional
                .setMaxRecordSizeInBytes(256 * 1024)                            // Optional
                .build();

flinkStream.sinkTo(sqsSink)

```

`Properties sinkProperties = new Properties();
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1");
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id");
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key");

// Optional, use following if you want to provide access via AssumeRole, Please make sure given IAM role has "sqs:SendMessage" permission
sinkProperties.setProperty(AWSConfigConstants.AWS_CREDENTIALS_PROVIDER, "ASSUME_ROLE");
sinkProperties.setProperty(AWSConfigConstants.AWS_ROLE_ARN, "replace-this-with-IAMRole-arn");
sinkProperties.setProperty(AWSConfigConstants.AWS_ROLE_SESSION_NAME, "any-session-name-string");

SqsSink<String> sqsSink =
        SqsSink.<String>builder()
                .setSerializationSchema(new SimpleStringSchema())                // Required
                .setSqsUrl("https://sqs.us-east-1.amazonaws.com/xxxx/test-sqs")  // Required
                .setSqsClientProperties(sinkProperties)                          // Required
                .setFailOnError(false)                                           // Optional
                .setMaxBatchSize(10)                                             // Optional
                .setMaxInFlightRequests(50)                                      // Optional
                .setMaxBufferedRequests(1_000)                                   // Optional
                .setMaxBatchSizeInBytes(256 * 1024)                         // Optional
                .setMaxTimeInBufferMS(5000)                                      // Optional
                .setMaxRecordSizeInBytes(256 * 1024)                            // Optional
                .build();

flinkStream.sinkTo(sqsSink)
`

```
val sinkProperties = new Properties()
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1")
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")

val SqsSink<String> sqsSink =
                SqsSink.<String>builder()
                        .setSerializationSchema(new SimpleStringSchema())                // Required
                        .setSqsUrl("https://sqs.us-east-1.amazonaws.com/xxxx/test-sqs")  // Required
                        .setSqsClientProperties(sinkProperties)                          // Required
                        .setFailOnError(false)                                           // Optional
                        .setMaxBatchSize(10)                                             // Optional
                        .setMaxInFlightRequests(50)                                      // Optional
                        .setMaxBufferedRequests(1_000)                                   // Optional
                        .setMaxBatchSizeInBytes(256 * 1024)                              // Optional
                        .setMaxTimeInBufferMS(5000)                                      // Optional
                        .setMaxRecordSizeInBytes(256 * 1024)                             // Optional
                        .build();
                        
                       
flinkStream.sinkTo(sqsSink)

```

`val sinkProperties = new Properties()
// Required
sinkProperties.put(AWSConfigConstants.AWS_REGION, "eu-west-1")
// Optional, provide via alternative routes e.g. environment variables
sinkProperties.put(AWSConfigConstants.AWS_ACCESS_KEY_ID, "aws_access_key_id")
sinkProperties.put(AWSConfigConstants.AWS_SECRET_ACCESS_KEY, "aws_secret_access_key")

val SqsSink<String> sqsSink =
                SqsSink.<String>builder()
                        .setSerializationSchema(new SimpleStringSchema())                // Required
                        .setSqsUrl("https://sqs.us-east-1.amazonaws.com/xxxx/test-sqs")  // Required
                        .setSqsClientProperties(sinkProperties)                          // Required
                        .setFailOnError(false)                                           // Optional
                        .setMaxBatchSize(10)                                             // Optional
                        .setMaxInFlightRequests(50)                                      // Optional
                        .setMaxBufferedRequests(1_000)                                   // Optional
                        .setMaxBatchSizeInBytes(256 * 1024)                              // Optional
                        .setMaxTimeInBufferMS(5000)                                      // Optional
                        .setMaxRecordSizeInBytes(256 * 1024)                             // Optional
                        .build();
                        
                       
flinkStream.sinkTo(sqsSink)
`

## Configurations#


Flink’s SQS sink is created by using the static builder SqsSink.<String>builder().

`SqsSink.<String>builder()`
1. setSqsClientProperties(Properties sinkProperties)

Required.
Supplies credentials, region and other parameters to the SQS client.


2. setSerializationSchema(SerializationSchema serializationSchema)

Required.
Supplies a serialization schema to the Sink. This schema is used to serialize elements before sending to SQS.


3. setSqsUrl(String sqsUrl)

Required.
Url of the SQS to sink to.


4. setFailOnError(boolean failOnError)

Optional. Default: false.
Whether failed requests to write records to SQS are treated as fatal exceptions in the sink that cause a Flink Job to restart


5. setMaxBatchSize(int maxBatchSize)

Optional. Default: 10.
Maximum size of a batch to write to SQS.


6. setMaxInFlightRequests(int maxInFlightRequests)

Optional. Default: 50.
The maximum number of in flight requests allowed before the sink applies backpressure.


7. setMaxBufferedRequests(int maxBufferedRequests)

Optional. Default: 5_000.
The maximum number of records that may be buffered in the sink before backpressure is applied.


8. setMaxBatchSizeInBytes(int maxBatchSizeInBytes)

Optional. Default: 256 * 1024.
The maximum size (in bytes) a batch may become. All batches sent will be smaller than or equal to this size.


9. setMaxTimeInBufferMS(int maxTimeInBufferMS)

Optional. Default: 5000.
The maximum time a record may stay in the sink before being flushed.


10. setMaxRecordSizeInBytes(int maxRecordSizeInBytes)
* Required.
* Supplies credentials, region and other parameters to the SQS client.
* Required.
* Supplies a serialization schema to the Sink. This schema is used to serialize elements before sending to SQS.
* Required.
* Url of the SQS to sink to.
* Optional. Default: false.
* Whether failed requests to write records to SQS are treated as fatal exceptions in the sink that cause a Flink Job to restart
`false`
* Optional. Default: 10.
* Maximum size of a batch to write to SQS.
`10`
* Optional. Default: 50.
* The maximum number of in flight requests allowed before the sink applies backpressure.
`50`
* Optional. Default: 5_000.
* The maximum number of records that may be buffered in the sink before backpressure is applied.
`5_000`
* Optional. Default: 256 * 1024.
* The maximum size (in bytes) a batch may become. All batches sent will be smaller than or equal to this size.
`256 * 1024`
* Optional. Default: 5000.
* The maximum time a record may stay in the sink before being flushed.
`5000`
* Optional. Default: 256 * 1024.
* The maximum record size that the sink will accept, records larger than this will be automatically rejected.
`256 * 1024`
1. build()
* Constructs and returns the SQS sink.