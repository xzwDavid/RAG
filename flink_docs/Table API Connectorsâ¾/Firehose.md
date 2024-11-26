# Firehose


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Amazon Kinesis Data Firehose SQL Connector#



Sink: Batch
Sink: Streaming Append Mode


The Kinesis Data Firehose connector allows for writing data into Amazon Kinesis Data Firehose (KDF).


## Dependencies#


Only available for stable versions.


## How to create a Kinesis Data Firehose table#


Follow the instructions from the Amazon Kinesis Data Firehose Developer Guide to set up a Kinesis Data Firehose delivery stream.
The following example shows how to create a table backed by a Kinesis Data Firehose delivery stream with minimum required options:


```
CREATE TABLE FirehoseTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `category_id` BIGINT,
  `behavior` STRING
)
WITH (
  'connector' = 'firehose',
  'delivery-stream' = 'user_behavior',
  'aws.region' = 'us-east-2',
  'format' = 'csv'
);

```

`CREATE TABLE FirehoseTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `category_id` BIGINT,
  `behavior` STRING
)
WITH (
  'connector' = 'firehose',
  'delivery-stream' = 'user_behavior',
  'aws.region' = 'us-east-2',
  'format' = 'csv'
);
`

## Connector Options#


##### connector

`'firehose'`

##### delivery-stream


##### format


##### aws.region

`KinesisFirehoseSink`

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


##### sink.http-client.max-concurrency

`FirehoseAsyncClient`

##### sink.http-client.read-timeout

`FirehoseAsyncClient`

##### sink.http-client.protocol.version

`FirehoseAsyncClient`

##### sink.batch.max-size

`FirehoseAsyncClient`

##### sink.requests.max-inflight

`FirehoseAsyncClient`

##### sink.requests.max-buffered

`FirehoseAsyncClient`

##### sink.flush-buffer.size

`FirehoseAsyncClient`

##### sink.flush-buffer.timeout

`FirehoseAsyncClient`

##### sink.fail-on-error


## Authorization#


Make sure to create an appropriate IAM policy to allow reading writing to the Kinesis Data Firehose delivery stream.


## Authentication#


Depending on your deployment you would choose a different Credentials Provider to allow access to Kinesis Data Firehose.
By default, the AUTO Credentials Provider is used.
If the access key ID and secret key are set in the deployment configuration, this results in using the BASIC provider.

`AUTO`
`BASIC`

A specific AWSCredentialsProvider can be optionally set using the aws.credentials.provider setting.
Supported values are:

`aws.credentials.provider`
* AUTO - Use the default AWS Credentials Provider chain that searches for credentials in the following order: ENV_VARS, SYS_PROPS, WEB_IDENTITY_TOKEN, PROFILE, and EC2/ECS credentials provider.
* BASIC - Use access key ID and secret key supplied as configuration.
* ENV_VAR - Use AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY environment variables.
* SYS_PROP - Use Java system properties aws.accessKeyId and aws.secretKey.
* PROFILE - Use an AWS credentials profile to create the AWS credentials.
* ASSUME_ROLE - Create AWS credentials by assuming a role. The credentials for assuming the role must be supplied.
* WEB_IDENTITY_TOKEN - Create AWS credentials by assuming a role using Web Identity Token.
* CUSTOM - Provide a custom class that implements the interface AWSCredentialsProvider and has a constructor MyCustomClass(java.util.Properties config). All connector properties will be passed down to this custom
credential provider class via the constructor.
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
`aws.accessKeyId`
`aws.secretKey`
`PROFILE`
`ASSUME_ROLE`
`WEB_IDENTITY_TOKEN`
`CUSTOM`
`AWSCredentialsProvider`
`MyCustomClass(java.util.Properties config)`

## Data Type Mapping#


Kinesis Data Firehose stores records as Base64-encoded binary data objects, so it doesn’t have a notion of internal record structure.
Instead, Kinesis Data Firehose records are deserialized and serialized by formats, e.g. ‘avro’, ‘csv’, or ‘json’.
To determine the data type of the messages in your Kinesis Data Firehose backed tables, pick a suitable Flink format with the format keyword.
Please refer to the Formats pages for more details.

`format`

## Notice#


The current implementation for the Kinesis Data Firehose SQL connector only supports Kinesis Data Firehose backed sinks and doesn’t provide an implementation for source queries.
Queries similar to:


```
SELECT * FROM FirehoseTable;

```

`SELECT * FROM FirehoseTable;
`

should result in an error similar to


```
Connector firehose can only be used as a sink. It cannot be used as a source.

```

`Connector firehose can only be used as a sink. It cannot be used as a source.
`

 Back to top
