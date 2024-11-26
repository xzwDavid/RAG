# Upsert Kafka


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Upsert Kafka SQL Connector#



Scan Source: Unbounded
Sink: Streaming Upsert Mode


The Upsert Kafka connector allows for reading data from and writing data into Kafka topics in the upsert fashion.


As a source, the upsert-kafka connector produces a changelog stream, where each data record represents
an update or delete event. More precisely, the value in a data record is interpreted as an UPDATE of
the last value for the same key, if any (if a corresponding key doesnât exist yet, the update will
be considered an INSERT). Using the table analogy, a data record in a changelog stream is interpreted
as an UPSERT aka INSERT/UPDATE because any existing row with the same key is overwritten. Also, null
values are interpreted in a special way: a record with a null value represents a âDELETEâ.


As a sink, the upsert-kafka connector can consume a changelog stream. It will write INSERT/UPDATE_AFTER
data as normal Kafka messages value, and write DELETE data as Kafka messages with null values
(indicate tombstone for the key). Flink will guarantee the message ordering on the primary key by
partition data on the values of the primary key columns, so the update/deletion messages on the same
key will fall into the same partition.


## Dependencies#


Only available for stable versions.


The Upsert Kafka connector is not part of the binary distribution.
See how to link with it for cluster execution here.


## Full Example#


The example below shows how to create and use an Upsert Kafka table:


```
CREATE TABLE pageviews_per_region (
  user_region STRING,
  pv BIGINT,
  uv BIGINT,
  PRIMARY KEY (user_region) NOT ENFORCED
) WITH (
  'connector' = 'upsert-kafka',
  'topic' = 'pageviews_per_region',
  'properties.bootstrap.servers' = '...',
  'key.format' = 'avro',
  'value.format' = 'avro'
);

CREATE TABLE pageviews (
  user_id BIGINT,
  page_id BIGINT,
  viewtime TIMESTAMP,
  user_region STRING,
  WATERMARK FOR viewtime AS viewtime - INTERVAL '2' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'pageviews',
  'properties.bootstrap.servers' = '...',
  'format' = 'json'
);

-- calculate the pv, uv and insert into the upsert-kafka sink
INSERT INTO pageviews_per_region
SELECT
  user_region,
  COUNT(*),
  COUNT(DISTINCT user_id)
FROM pageviews
GROUP BY user_region;

```

`CREATE TABLE pageviews_per_region (
  user_region STRING,
  pv BIGINT,
  uv BIGINT,
  PRIMARY KEY (user_region) NOT ENFORCED
) WITH (
  'connector' = 'upsert-kafka',
  'topic' = 'pageviews_per_region',
  'properties.bootstrap.servers' = '...',
  'key.format' = 'avro',
  'value.format' = 'avro'
);

CREATE TABLE pageviews (
  user_id BIGINT,
  page_id BIGINT,
  viewtime TIMESTAMP,
  user_region STRING,
  WATERMARK FOR viewtime AS viewtime - INTERVAL '2' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'pageviews',
  'properties.bootstrap.servers' = '...',
  'format' = 'json'
);

-- calculate the pv, uv and insert into the upsert-kafka sink
INSERT INTO pageviews_per_region
SELECT
  user_region,
  COUNT(*),
  COUNT(DISTINCT user_id)
FROM pageviews
GROUP BY user_region;
`

Attention Make sure to define the primary key in the DDL.


## Available Metadata#


See the regular Kafka connector for a list
of all available metadata fields.


## Connector Options#


##### connector

`'upsert-kafka'`

##### topic

`'topic-1;topic-2'`

##### properties.bootstrap.servers


##### properties.*

`'properties.allow.auto.create.topics' = 'false'`
`'auto.offset.reset'`

##### key.format


The format used to deserialize and serialize the key part of Kafka messages.
      Please refer to the formats page
      for more details and more format options.

`PRIMARY KEY`

##### key.fields-prefix

`'key.fields'`
`'value.fields-include'`
`'EXCEPT_KEY'`

##### value.format


##### value.fields-include


Enum

`'ALL'`

##### sink.parallelism


##### sink.buffer-flush.max-rows

`'sink.buffer-flush.max-rows'`
`'sink.buffer-flush.interval'`

##### sink.buffer-flush.interval

`'sink.buffer-flush.max-rows'`
`'sink.buffer-flush.interval'`

##### sink.delivery-guarantee

`'at-least-once'`
`'exactly-once'`
`'none'`

##### sink.transactional-id-prefix

`'exactly-once'`

## Features#


### Key and Value Formats#


See the regular Kafka connector for more
explanation around key and value formats. However, note that this connector requires both a key and
value format where the key fields are derived from the PRIMARY KEY constraint.

`PRIMARY KEY`

The following example shows how to specify and configure key and value formats. The format options are
prefixed with either the 'key' or 'value' plus format identifier.

`'key'`
`'value'`

```
CREATE TABLE KafkaTable (
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING,
  PRIMARY KEY (`user_id`) NOT ENFORCED
) WITH (
  'connector' = 'upsert-kafka',
  ...

  'key.format' = 'json',
  'key.json.ignore-parse-errors' = 'true',

  'value.format' = 'json',
  'value.json.fail-on-missing-field' = 'false',
  'value.fields-include' = 'EXCEPT_KEY'
)

```

`CREATE TABLE KafkaTable (
  `ts` TIMESTAMP_LTZ(3) METADATA FROM 'timestamp',
  `user_id` BIGINT,
  `item_id` BIGINT,
  `behavior` STRING,
  PRIMARY KEY (`user_id`) NOT ENFORCED
) WITH (
  'connector' = 'upsert-kafka',
  ...

  'key.format' = 'json',
  'key.json.ignore-parse-errors' = 'true',

  'value.format' = 'json',
  'value.json.fail-on-missing-field' = 'false',
  'value.fields-include' = 'EXCEPT_KEY'
)
`

### Primary Key Constraints#


The Upsert Kafka always works in the upsert fashion and requires to define the primary key in the DDL.
With the assumption that records with the same key should be ordered in the same partition, the
primary key semantic on the changelog source means the materialized changelog is unique on the primary
keys. The primary key definition will also control which fields should end up in Kafkaâs key.


### Consistency Guarantees#


By default, an Upsert Kafka sink ingests data with at-least-once guarantees into a Kafka topic if
the query is executed with checkpointing enabled.


This means, Flink may write duplicate records with the same key into the Kafka topic. But as the
connector is working in the upsert mode, the last record on the same key will take effect when
reading back as a source. Therefore, the upsert-kafka connector achieves idempotent writes just like
the HBase sink.


With Flink’s checkpointing enabled, the upsert-kafka connector can provide exactly-once delivery guarantees.

`upsert-kafka`

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

Please refer to Kafka connector documentation for more caveats about delivery guarantees.


### Source Per-Partition Watermarks#


Flink supports to emit per-partition watermarks for Upsert Kafka. Watermarks are generated inside the Kafka
consumer. The per-partition watermarks are merged in the same way as watermarks are merged during streaming
shuffles. The output watermark of the source is determined by the minimum watermark among the partitions
it reads. If some partitions in the topics are idle, the watermark generator will not advance. You can
alleviate this problem by setting the 'table.exec.source.idle-timeout'
option in the table configuration.

`'table.exec.source.idle-timeout'`

Please refer to Kafka watermark strategies
for more details.


## Data Type Mapping#


Upsert Kafka stores message keys and values as bytes, so Upsert Kafka doesn’t have schema or data types.
The messages are serialized and deserialized by formats, e.g. csv, json, avro. Thus, the data type mapping
is determined by specific formats. Please refer to Formats
pages for more details.


 Back to top
