# DynamoDB


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Amazon DynamoDB SQL Connector#



Sink: Batch
Sink: Streaming Append & Upsert Mode


The DynamoDB connector allows for writing data into Amazon DynamoDB.


## Dependencies#


Only available for stable versions.


## How to create a DynamoDB table#


Follow the instructions from the Amazon DynamoDB Developer Guide
to set up a DynamoDB table. The following example shows how to create a table backed by a DynamoDB table with minimum required options:


```
CREATE TABLE DynamoDbTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `category_id` BIGINT,
  `behavior` STRING
)
WITH (
  'connector' = 'dynamodb',
  'table-name' = 'user_behavior',
  'aws.region' = 'us-east-2'
);

```

`CREATE TABLE DynamoDbTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `category_id` BIGINT,
  `behavior` STRING
)
WITH (
  'connector' = 'dynamodb',
  'table-name' = 'user_behavior',
  'aws.region' = 'us-east-2'
);
`

## Connector Options#


##### connector

`'dynamodb'`

##### table-name


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


##### aws.credentials.role.provider


##### aws.credentials.webIdentityToken.file


##### aws.credentials.custom.class


##### sink.batch.max-size


##### sink.requests.max-inflight


##### sink.requests.max-buffered


##### sink.flush-buffer.timeout


##### sink.fail-on-error


##### sink.ignore-nulls


##### sink.http-client.max-concurrency


##### sink.http-client.read-timeout


## Authorization#


Make sure to create an appropriate IAM policy to allow writing to the DynamoDB table.


## Authentication#


Depending on your deployment you would choose an appropriate Credentials Provider to allow access to DynamoDB.
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

## Sink Partitioning#


The DynamoDB sink supports client side deduplication of data via the PARTITIONED BY clause. You can specify a list of
partition keys, the sink will only send the latest record for each composite key within a batch. For example:

`PARTITIONED BY`

```
CREATE TABLE DynamoDbTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `category_id` BIGINT,
  `behavior` STRING
) PARTITIONED BY ( user_id )
WITH (
  'connector' = 'dynamodb',
  'table-name' = 'user_behavior',
  'aws.region' = 'us-east-2'
);

```

`CREATE TABLE DynamoDbTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `category_id` BIGINT,
  `behavior` STRING
) PARTITIONED BY ( user_id )
WITH (
  'connector' = 'dynamodb',
  'table-name' = 'user_behavior',
  'aws.region' = 'us-east-2'
);
`

## Notice#


The current implementation of the DynamoDB SQL connector is write-only and doesn’t provide an implementation for source queries.
Queries similar to:


```
SELECT * FROM DynamoDbTable;

```

`SELECT * FROM DynamoDbTable;
`

should result in an error similar to


```
Connector dynamodb can only be used as a sink. It cannot be used as a source.

```

`Connector dynamodb can only be used as a sink. It cannot be used as a source.
`

 Back to top
