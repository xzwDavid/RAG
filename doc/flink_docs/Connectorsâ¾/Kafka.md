# Kafka


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Apache Kafka SQL Connector#



Scan Source: Unbounded
Sink: Streaming Append Mode


The Kafka connector allows for reading data from and writing data into Kafka topics.


## Dependencies#


Only available for stable versions.


The Kafka connector is not part of the binary distribution.
See how to link with it for cluster execution here.


## How to create a Kafka table#


The example below shows how to create a Kafka table:


```
CREATE TABLE KafkaTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING,
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp'
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'csv'
)

```

`CREATE TABLE KafkaTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING,
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp'
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'csv'
)
`

## Available Metadata#


The following connector metadata can be accessed as metadata columns in a table definition.


The R/W column defines whether a metadata field is readable (R) and/or writable (W).
Read-only columns must be declared VIRTUAL to exclude them during an INSERT INTO operation.

`R/W`
`R`
`W`
`VIRTUAL`
`INSERT INTO`
`topic`
`STRING NOT NULL`
`R/W`
`partition`
`INT NOT NULL`
`R`
`headers`
`MAP NOT NULL`
`R/W`
`leader-epoch`
`INT NULL`
`R`
`offset`
`BIGINT NOT NULL`
`R`
`timestamp`
`TIMESTAMP_LTZ(3) NOT NULL`
`R/W`
`timestamp-type`
`STRING NOT NULL`
`R`

The extended CREATE TABLE example demonstrates the syntax for exposing these metadata fields:

`CREATE TABLE`

```
CREATE TABLE KafkaTable (
  `event_time` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `partition` BIGINT METADATA VIRTUAL,
  `offset` BIGINT METADATA VIRTUAL,
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'csv'
);

```

`CREATE TABLE KafkaTable (
  `event_time` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `partition` BIGINT METADATA VIRTUAL,
  `offset` BIGINT METADATA VIRTUAL,
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'csv'
);
`

Format Metadata


The connector is able to expose metadata of the value format for reading. Format metadata keys
are prefixed with 'value.'.

`'value.'`

The following example shows how to access both Kafka and Debezium metadata fields:


```
CREATE TABLE KafkaTable (
  `event_time` TIMESTAMP_LTZ(3) METADATA FROM 'value.source.timestamp' VIRTUAL,  -- from Debezium format
  `origin_table` STRING METADATA FROM 'value.source.table' VIRTUAL, -- from Debezium format
  `partition_id` BIGINT METADATA FROM 'partition' VIRTUAL,  -- from Kafka connector
  `offset` BIGINT METADATA VIRTUAL,  -- from Kafka connector
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'debezium-json'
);

```

`CREATE TABLE KafkaTable (
  `event_time` TIMESTAMP_LTZ(3) METADATA FROM 'value.source.timestamp' VIRTUAL,  -- from Debezium format
  `origin_table` STRING METADATA FROM 'value.source.table' VIRTUAL, -- from Debezium format
  `partition_id` BIGINT METADATA FROM 'partition' VIRTUAL,  -- from Kafka connector
  `offset` BIGINT METADATA VIRTUAL,  -- from Kafka connector
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'user_behavior',
  'properties.bootstrap.servers' = 'localhost:9092',
  'properties.group.id' = 'testGroup',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'debezium-json'
);
`

## Connector Options#


##### connector

`'kafka'`

##### topic

`'topic-1;topic-2'`

##### topic-pattern


##### properties.bootstrap.servers


##### properties.group.id


##### properties.*

`'properties.allow.auto.create.topics' = 'false'`
`'auto.offset.reset'`

##### format

`'value.format'`

##### key.format

`'key.fields'`

##### key.fields

`'field1;field2'`

##### key.fields-prefix

`'key.fields'`
`'value.fields-include'`
`'EXCEPT_KEY'`

##### value.format

`'format'`

##### value.fields-include


Enum

`'ALL'`

##### scan.startup.mode

`'earliest-offset'`
`'latest-offset'`
`'group-offsets'`
`'timestamp'`
`'specific-offsets'`

##### scan.startup.specific-offsets

`'specific-offsets'`
`'partition:0,offset:42;partition:1,offset:300'`

##### scan.startup.timestamp-millis

`'timestamp'`

##### scan.bounded.mode

`'latest-offset'`
`'group-offsets'`
`'timestamp'`
`'specific-offsets'`

##### scan.bounded.specific-offsets

`'specific-offsets'`
`'partition:0,offset:42;partition:1,offset:300'. If an offset
       for a partition is not provided it will not consume from that partition.`

##### scan.bounded.timestamp-millis

`'timestamp'`

##### scan.topic-partition-discovery.interval


##### sink.partitioner

* default: use the kafka default partitioner to partition records.
* fixed: each Flink partition ends up in at most one Kafka partition.
* round-robin: a Flink partition is distributed to Kafka partitions sticky round-robin. It only works when record's keys are not specified.
* Custom FlinkKafkaPartitioner subclass: e.g. 'org.mycompany.MyPartitioner'.
`default`
`fixed`
`round-robin`
`FlinkKafkaPartitioner`
`'org.mycompany.MyPartitioner'`

##### sink.semantic

`sink.delivery-guarantee`

##### sink.delivery-guarantee

`'at-least-once'`
`'exactly-once'`
`'none'`

##### sink.transactional-id-prefix

`'exactly-once'`

##### sink.parallelism


## Features#


### Key and Value Formats#


Both the key and value part of a Kafka record can be serialized to and deserialized from raw bytes using
one of the given formats.


Value Format


Since a key is optional in Kafka records, the following statement reads and writes records with a configured
value format but without a key format. The 'format' option is a synonym for 'value.format'. All format
options are prefixed with the format identifier.

`'format'`
`'value.format'`

```
CREATE TABLE KafkaTable (
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING
) WITH (
  'connector' = 'kafka',
  ...

  'format' = 'json',
  'json.ignore-parse-errors' = 'true'
)

```

`CREATE TABLE KafkaTable (
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING
) WITH (
  'connector' = 'kafka',
  ...

  'format' = 'json',
  'json.ignore-parse-errors' = 'true'
)
`

The value format will be configured with the following data type:


```
ROW<`user_id` BIGINT, `item_id` BIGINT, `behavior` STRING>

```

`ROW<`user_id` BIGINT, `item_id` BIGINT, `behavior` STRING>
`

Key and Value Format


The following example shows how to specify and configure key and value formats. The format options are
prefixed with either the 'key' or 'value' plus format identifier.

`'key'`
`'value'`

```
CREATE TABLE KafkaTable (
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING
) WITH (
  'connector' = 'kafka',
  ...

  'key.format' = 'json',
  'key.json.ignore-parse-errors' = 'true',
  'key.fields' = 'user_id;item_id',

  'value.format' = 'json',
  'value.json.fail-on-missing-field' = 'false',
  'value.fields-include' = 'ALL'
)

```

`CREATE TABLE KafkaTable (
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING
) WITH (
  'connector' = 'kafka',
  ...

  'key.format' = 'json',
  'key.json.ignore-parse-errors' = 'true',
  'key.fields' = 'user_id;item_id',

  'value.format' = 'json',
  'value.json.fail-on-missing-field' = 'false',
  'value.fields-include' = 'ALL'
)
`

The key format includes the fields listed in 'key.fields' (using ';' as the delimiter) in the same
order. Thus, it will be configured with the following data type:

`'key.fields'`
`';'`

```
ROW<`user_id` BIGINT, `item_id` BIGINT>

```

`ROW<`user_id` BIGINT, `item_id` BIGINT>
`

Since the value format is configured with 'value.fields-include' = 'ALL', key fields will also end up in
the value format’s data type:

`'value.fields-include' = 'ALL'`

```
ROW<`user_id` BIGINT, `item_id` BIGINT, `behavior` STRING>

```

`ROW<`user_id` BIGINT, `item_id` BIGINT, `behavior` STRING>
`

Overlapping Format Fields


The connector cannot split the table’s columns into key and value fields based on schema information
if both key and value formats contain fields of the same name. The 'key.fields-prefix' option allows
to give key columns a unique name in the table schema while keeping the original names when configuring
the key format.

`'key.fields-prefix'`

The following example shows a key and value format that both contain a version field:

`version`

```
CREATE TABLE KafkaTable (
  `k_version` INT,
  `k_user_id` BIGINT,
  `k_item_id` BIGINT,
  `version` INT,
  `behavior` STRING
) WITH (
  'connector' = 'kafka',
  ...

  'key.format' = 'json',
  'key.fields-prefix' = 'k_',
  'key.fields' = 'k_version;k_user_id;k_item_id',

  'value.format' = 'json',
  'value.fields-include' = 'EXCEPT_KEY'
)

```

`CREATE TABLE KafkaTable (
  `k_version` INT,
  `k_user_id` BIGINT,
  `k_item_id` BIGINT,
  `version` INT,
  `behavior` STRING
) WITH (
  'connector' = 'kafka',
  ...

  'key.format' = 'json',
  'key.fields-prefix' = 'k_',
  'key.fields' = 'k_version;k_user_id;k_item_id',

  'value.format' = 'json',
  'value.fields-include' = 'EXCEPT_KEY'
)
`

The value format must be configured in 'EXCEPT_KEY' mode. The formats will be configured with
the following data types:

`'EXCEPT_KEY'`

```
key format:
ROW<`version` INT, `user_id` BIGINT, `item_id` BIGINT>

value format:
ROW<`version` INT, `behavior` STRING>

```

`key format:
ROW<`version` INT, `user_id` BIGINT, `item_id` BIGINT>

value format:
ROW<`version` INT, `behavior` STRING>
`

### Topic and Partition Discovery#


The config option topic and topic-pattern specifies the topics or topic pattern to consume for source. The config option topic can accept topic list using semicolon separator like ’topic-1;topic-2’.
The config option topic-pattern  will use regular expression to discover the matched topic. For example, if the topic-pattern is test-topic-[0-9], then all topics with names that match the specified regular expression (starting with test-topic- and ending with a single digit)) will be subscribed by the consumer when the job starts running.

`topic`
`topic-pattern`
`topic`
`topic-pattern`
`topic-pattern`
`test-topic-[0-9]`
`test-topic-`

To allow the consumer to discover dynamically created topics after the job started running, set a non-negative value for scan.topic-partition-discovery.interval. This allows the consumer to discover partitions of new topics with names that also match the specified pattern.

`scan.topic-partition-discovery.interval`

Please refer to Kafka DataStream Connector documentation for more about topic and partition discovery.


Note that topic list and topic pattern only work in sources. In sinks, Flink currently only supports a single topic.


### Start Reading Position#


The config option scan.startup.mode specifies the startup mode for Kafka consumer. The valid enumerations are:

`scan.startup.mode`
* group-offsets: start from committed offsets in ZK / Kafka brokers of a specific consumer group.
* earliest-offset: start from the earliest offset possible.
* latest-offset: start from the latest offset.
* timestamp: start from user-supplied timestamp for each partition.
* specific-offsets: start from user-supplied specific offsets for each partition.
`group-offsets`
`earliest-offset`
`latest-offset`
`timestamp`
`specific-offsets`

The default option value is group-offsets which indicates to consume from last committed offsets in ZK / Kafka brokers.

`group-offsets`

If timestamp is specified, another config option scan.startup.timestamp-millis is required to specify a specific startup timestamp in milliseconds since January 1, 1970 00:00:00.000 GMT.

`timestamp`
`scan.startup.timestamp-millis`

If specific-offsets is specified, another config option scan.startup.specific-offsets is required to specify specific startup offsets for each partition,
e.g. an option value partition:0,offset:42;partition:1,offset:300 indicates offset 42 for partition 0 and offset 300 for partition 1.

`specific-offsets`
`scan.startup.specific-offsets`
`partition:0,offset:42;partition:1,offset:300`
`42`
`0`
`300`
`1`

### Bounded Ending Position#


The config option scan.bounded.mode specifies the bounded mode for Kafka consumer. The valid enumerations are:

`scan.bounded.mode`
* `group-offsets`: bounded by committed offsets in ZooKeeper / Kafka brokers of a specific consumer group. This is evaluated at the start of consumption from a given partition.
* `latest-offset`: bounded by latest offsets. This is evaluated at the start of consumption from a given partition.
* `timestamp`: bounded by a user-supplied timestamp.
* `specific-offsets`: bounded by user-supplied specific offsets for each partition.

If config option value scan.bounded.mode is not set the default is an unbounded table.

`scan.bounded.mode`

If timestamp is specified, another config option scan.bounded.timestamp-millis is required to specify a specific bounded timestamp in milliseconds since January 1, 1970 00:00:00.000 GMT.

`timestamp`
`scan.bounded.timestamp-millis`

If specific-offsets is specified, another config option scan.bounded.specific-offsets is required to specify specific bounded offsets for each partition,
e.g. an option value partition:0,offset:42;partition:1,offset:300 indicates offset 42 for partition 0 and offset 300 for partition 1. If an offset for a partition is not provided it will not consume from that partition.

`specific-offsets`
`scan.bounded.specific-offsets`
`partition:0,offset:42;partition:1,offset:300`
`42`
`0`
`300`
`1`

### CDC Changelog Source#


Flink natively supports Kafka as a CDC changelog source. If messages in a Kafka topic are change event captured from other databases using a CDC tool, you can use the corresponding Flink CDC format to interpret the messages as INSERT/UPDATE/DELETE statements into a Flink SQL table.


The changelog source is a very useful feature in many cases, such as synchronizing incremental data from databases to other systems, auditing logs, materialized views on databases, temporal join changing history of a database table and so on.


Flink provides several CDC formats:

* debezium
* canal
* maxwell

### Sink Partitioning#


The config option sink.partitioner specifies output partitioning from Flink’s partitions into Kafka’s partitions.
By default, Flink uses the Kafka default partitioner to partition records. It uses the sticky partition strategy for records with null keys and uses a murmur2 hash to compute the partition for a record with the key defined.

`sink.partitioner`

In order to control the routing of rows into partitions, a custom sink partitioner can be provided. The ‘fixed’ partitioner will write the records in the same Flink partition into the same Kafka partition, which could reduce the cost of the network connections.


### Consistency guarantees#


By default, a Kafka sink ingests data with at-least-once guarantees into a Kafka topic if the query is executed with checkpointing enabled.


With Flink’s checkpointing enabled, the kafka connector can provide exactly-once delivery guarantees.

`kafka`

Besides enabling Flink’s checkpointing, you can also choose three different modes of operating chosen by passing appropriate sink.delivery-guarantee option:

`sink.delivery-guarantee`
* none: Flink will not guarantee anything. Produced records can be lost or they can be duplicated.
* at-least-once (default setting): This guarantees that no records will be lost (although they can be duplicated).
* exactly-once: Kafka transactions will be used to provide exactly-once semantic. Whenever you write
to Kafka using transactions, do not forget about setting desired isolation.level (read_uncommitted
or read_committed - the latter one is the default value) for any application consuming records
from Kafka.
`none`
`at-least-once`
`exactly-once`
`isolation.level`
`read_uncommitted`
`read_committed`

Please refer to Kafka documentation for more caveats about delivery guarantees.


### Source Per-Partition Watermarks#


Flink supports to emit per-partition watermarks for Kafka. Watermarks are generated inside the Kafka
consumer. The per-partition watermarks are merged in the same way as watermarks are merged during streaming
shuffles. The output watermark of the source is determined by the minimum watermark among the partitions
it reads. If some partitions in the topics are idle, the watermark generator will not advance. You can
alleviate this problem by setting the 'table.exec.source.idle-timeout'
option in the table configuration.

`'table.exec.source.idle-timeout'`

Please refer to Kafka watermark strategies
for more details.


### Security#


In order to enable security configurations including encryption and authentication, you just need to setup security
configurations with “properties.” prefix in table options. The code snippet below shows configuring Kafka table to
use PLAIN as SASL mechanism and provide JAAS configuration when using SQL client JAR :


```
CREATE TABLE KafkaTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING,
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp'
) WITH (
  'connector' = 'kafka',
  ...
  'properties.security.protocol' = 'SASL_PLAINTEXT',
  'properties.sasl.mechanism' = 'PLAIN',
  'properties.sasl.jaas.config' = 'org.apache.kafka.common.security.plain.PlainLoginModule required username=\"username\" password=\"password\";'
)

```

`CREATE TABLE KafkaTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING,
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp'
) WITH (
  'connector' = 'kafka',
  ...
  'properties.security.protocol' = 'SASL_PLAINTEXT',
  'properties.sasl.mechanism' = 'PLAIN',
  'properties.sasl.jaas.config' = 'org.apache.kafka.common.security.plain.PlainLoginModule required username=\"username\" password=\"password\";'
)
`

For a more complex example, use SASL_SSL as the security protocol and use SCRAM-SHA-256 as SASL mechanism when using SQL client JAR :


```
CREATE TABLE KafkaTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING,
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp'
) WITH (
  'connector' = 'kafka',
  ...
  'properties.security.protocol' = 'SASL_SSL',
  /* SSL configurations */
  /* Configure the path of truststore (CA) provided by the server */
  'properties.ssl.truststore.location' = '/path/to/kafka.client.truststore.jks',
  'properties.ssl.truststore.password' = 'test1234',
  /* Configure the path of keystore (private key) if client authentication is required */
  'properties.ssl.keystore.location' = '/path/to/kafka.client.keystore.jks',
  'properties.ssl.keystore.password' = 'test1234',
  /* SASL configurations */
  /* Set SASL mechanism as SCRAM-SHA-256 */
  'properties.sasl.mechanism' = 'SCRAM-SHA-256',
  /* Set JAAS configurations */
  'properties.sasl.jaas.config' = 'org.apache.kafka.common.security.scram.ScramLoginModule required username=\"username\" password=\"password\";'
)

```

`CREATE TABLE KafkaTable (
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING,
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp'
) WITH (
  'connector' = 'kafka',
  ...
  'properties.security.protocol' = 'SASL_SSL',
  /* SSL configurations */
  /* Configure the path of truststore (CA) provided by the server */
  'properties.ssl.truststore.location' = '/path/to/kafka.client.truststore.jks',
  'properties.ssl.truststore.password' = 'test1234',
  /* Configure the path of keystore (private key) if client authentication is required */
  'properties.ssl.keystore.location' = '/path/to/kafka.client.keystore.jks',
  'properties.ssl.keystore.password' = 'test1234',
  /* SASL configurations */
  /* Set SASL mechanism as SCRAM-SHA-256 */
  'properties.sasl.mechanism' = 'SCRAM-SHA-256',
  /* Set JAAS configurations */
  'properties.sasl.jaas.config' = 'org.apache.kafka.common.security.scram.ScramLoginModule required username=\"username\" password=\"password\";'
)
`

Please note that the class path of the login module in sasl.jaas.config might be different if you relocate Kafka
client dependencies, so you may need to rewrite it with the actual class path of the module in the JAR.
SQL client JAR has relocated Kafka client dependencies to org.apache.flink.kafka.shaded.org.apache.kafka,
then the path of plain login module in code snippets above need to be
org.apache.flink.kafka.shaded.org.apache.kafka.common.security.plain.PlainLoginModule when using SQL client JAR.

`sasl.jaas.config`
`org.apache.flink.kafka.shaded.org.apache.kafka`
`org.apache.flink.kafka.shaded.org.apache.kafka.common.security.plain.PlainLoginModule`

For detailed explanations of security configurations, please refer to
the “Security” section in Apache Kafka documentation.


## Data Type Mapping#


Kafka stores message keys and values as bytes, so Kafka doesn’t have schema or data types. The Kafka messages are deserialized and serialized by formats, e.g. csv, json, avro.
Thus, the data type mapping is determined by specific formats. Please refer to Formats pages for more details.


 Back to top
