# Pulsar


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Apache Pulsar Connector#


Flink provides an Apache Pulsar connector for reading and writing data from and to Pulsar topics with exactly-once guarantees.


## Dependency#


You can use the connector with the Pulsar 2.10.0 or higher. It is recommended to always use the latest Pulsar version.
The details on Pulsar compatibility can be found in PIP-72.


Only available for stable versions.




In order to use the  in PyFlink jobs, the following
dependencies are required:



Version
PyFlink JAR



flink-connector-pulsar
Only available for stable releases.




See Python dependency management
for more details on how to use JARs in PyFlink.




Flink’s streaming connectors are not part of the binary distribution.
See how to link with them for cluster execution here.


## Pulsar Source#


> 
  This part describes the Pulsar source based on the new
data source API.



### Usage#


The Pulsar source provides a builder class for constructing a PulsarSource instance. The code snippet below builds a PulsarSource instance. It consumes messages from the earliest cursor of the topic
“persistent://public/default/my-topic” in Exclusive subscription type (my-subscription)
and deserializes the raw payload of the messages as strings.

`my-subscription`

```
PulsarSource<String> source = PulsarSource.builder()
    .setServiceUrl(serviceUrl)
    .setAdminUrl(adminUrl)
    .setStartCursor(StartCursor.earliest())
    .setTopics("my-topic")
    .setDeserializationSchema(new SimpleStringSchema())
    .setSubscriptionName("my-subscription")
    .build();

env.fromSource(source, WatermarkStrategy.noWatermarks(), "Pulsar Source");

```

`PulsarSource<String> source = PulsarSource.builder()
    .setServiceUrl(serviceUrl)
    .setAdminUrl(adminUrl)
    .setStartCursor(StartCursor.earliest())
    .setTopics("my-topic")
    .setDeserializationSchema(new SimpleStringSchema())
    .setSubscriptionName("my-subscription")
    .build();

env.fromSource(source, WatermarkStrategy.noWatermarks(), "Pulsar Source");
`

```
pulsar_source = PulsarSource.builder() \
    .set_service_url('pulsar://localhost:6650') \
    .set_admin_url('http://localhost:8080') \
    .set_start_cursor(StartCursor.earliest()) \
    .set_topics("my-topic") \
    .set_deserialization_schema(SimpleStringSchema()) \
    .set_subscription_name('my-subscription') \
    .build()

env.from_source(source=pulsar_source,
                watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
                source_name="pulsar source")

```

`pulsar_source = PulsarSource.builder() \
    .set_service_url('pulsar://localhost:6650') \
    .set_admin_url('http://localhost:8080') \
    .set_start_cursor(StartCursor.earliest()) \
    .set_topics("my-topic") \
    .set_deserialization_schema(SimpleStringSchema()) \
    .set_subscription_name('my-subscription') \
    .build()

env.from_source(source=pulsar_source,
                watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
                source_name="pulsar source")
`

The following properties are required for building a PulsarSource:

* Pulsar service URL, configured by setServiceUrl(String)
* Pulsar service HTTP URL (also known as admin URL), configured by setAdminUrl(String)
* Pulsar subscription name, configured by setSubscriptionName(String)
* Topics / partitions to subscribe, see the following
topic-partition subscription for more details.
* Deserializer to parse Pulsar messages, see the following
deserializer for more details.
`setServiceUrl(String)`
`setAdminUrl(String)`
`setSubscriptionName(String)`

It is recommended to set the consumer name in Pulsar Source by setConsumerName(String).
This sets a unique name for the Flink connector in the Pulsar statistic dashboard.
You can use it to monitor the performance of your Flink connector and applications.

`setConsumerName(String)`

### Topic-partition Subscription#


Pulsar source provide two ways of topic-partition subscription:

* 
Topic list, subscribing messages from all partitions in a list of topics. For example:






Java
PulsarSource.builder().setTopics("some-topic1", "some-topic2");

// Partition 0 and 2 of topic "topic-a"
PulsarSource.builder().setTopics("topic-a-partition-0", "topic-a-partition-2");

Python
PulsarSource.builder().set_topics(["some-topic1", "some-topic2"])

# Partition 0 and 2 of topic "topic-a"
PulsarSource.builder().set_topics(["topic-a-partition-0", "topic-a-partition-2"])



* 
Topic pattern, subscribing messages from all topics whose name matches the provided regular expression. For example:






Java
PulsarSource.builder().setTopicPattern("topic-.*");

Python
PulsarSource.builder().set_topic_pattern("topic-.*")




Topic list, subscribing messages from all partitions in a list of topics. For example:






Java
PulsarSource.builder().setTopics("some-topic1", "some-topic2");

// Partition 0 and 2 of topic "topic-a"
PulsarSource.builder().setTopics("topic-a-partition-0", "topic-a-partition-2");

Python
PulsarSource.builder().set_topics(["some-topic1", "some-topic2"])

# Partition 0 and 2 of topic "topic-a"
PulsarSource.builder().set_topics(["topic-a-partition-0", "topic-a-partition-2"])




```
PulsarSource.builder().setTopics("some-topic1", "some-topic2");

// Partition 0 and 2 of topic "topic-a"
PulsarSource.builder().setTopics("topic-a-partition-0", "topic-a-partition-2");

```

`PulsarSource.builder().setTopics("some-topic1", "some-topic2");

// Partition 0 and 2 of topic "topic-a"
PulsarSource.builder().setTopics("topic-a-partition-0", "topic-a-partition-2");
`

```
PulsarSource.builder().set_topics(["some-topic1", "some-topic2"])

# Partition 0 and 2 of topic "topic-a"
PulsarSource.builder().set_topics(["topic-a-partition-0", "topic-a-partition-2"])

```

`PulsarSource.builder().set_topics(["some-topic1", "some-topic2"])

# Partition 0 and 2 of topic "topic-a"
PulsarSource.builder().set_topics(["topic-a-partition-0", "topic-a-partition-2"])
`

Topic pattern, subscribing messages from all topics whose name matches the provided regular expression. For example:






Java
PulsarSource.builder().setTopicPattern("topic-.*");

Python
PulsarSource.builder().set_topic_pattern("topic-.*")




```
PulsarSource.builder().setTopicPattern("topic-.*");

```

`PulsarSource.builder().setTopicPattern("topic-.*");
`

```
PulsarSource.builder().set_topic_pattern("topic-.*")

```

`PulsarSource.builder().set_topic_pattern("topic-.*")
`

#### Flexible Topic Naming#


Since Pulsar 2.0, all topic names internally are in a form of {persistent|non-persistent}://tenant/namespace/topic.
Now, for partitioned topics, you can use short names in many cases (for the sake of simplicity).
The flexible naming system stems from the fact that there is now a default topic type, tenant, and namespace in a Pulsar cluster.

`{persistent|non-persistent}://tenant/namespace/topic`
`persistent`
`public`
`default`

This table lists a mapping relationship between your input topic name and the translated topic name:

`my-topic`
`persistent://public/default/my-topic`
`my-tenant/my-namespace/my-topic`
`persistent://my-tenant/my-namespace/my-topic`

> 
  For non-persistent topics, you need to specify the entire topic name,
as the default-based rules do not apply for non-partitioned topics.
Thus, you cannot use a short name like non-persistent://my-topic and need to use non-persistent://public/default/my-topic instead.


`non-persistent://my-topic`
`non-persistent://public/default/my-topic`

#### Subscribing Pulsar Topic Partition#


Internally, Pulsar divides a partitioned topic as a set of non-partitioned topics according to the partition size.


For example, if a simple-string topic with 3 partitions is created under the sample tenant with the flink namespace.
The topics on Pulsar would be:

`simple-string`
`sample`
`flink`
`persistent://sample/flink/simple-string`
`persistent://sample/flink/simple-string-partition-0`
`persistent://sample/flink/simple-string-partition-1`
`persistent://sample/flink/simple-string-partition-2`

You can directly consume messages from the topic partitions by using the non-partitioned topic names above.
For example, use PulsarSource.builder().setTopics("sample/flink/simple-string-partition-1", "sample/flink/simple-string-partition-2")
would consume the partitions 1 and 2 of the sample/flink/simple-string topic.

`PulsarSource.builder().setTopics("sample/flink/simple-string-partition-1", "sample/flink/simple-string-partition-2")`
`sample/flink/simple-string`

#### Setting Topic Patterns#


The Pulsar source can subscribe to a set of topics under only one tenant and one namespace by using regular expression.
But the topic type (persistent or non-persistent) isn’t determined by the regular expression.
Even if you use PulsarSource.builder().setTopicPattern("non-persistent://public/default/my-topic.*"), we will subscribe both
persistent and non-persistent topics which its name matches public/default/my-topic.*.

`persistent`
`non-persistent`
`PulsarSource.builder().setTopicPattern("non-persistent://public/default/my-topic.*")`
`persistent`
`non-persistent`
`public/default/my-topic.*`

In order to subscribe only non-persistent topics. You need to set the RegexSubscriptionMode to RegexSubscriptionMode.NonPersistentOnly.
For example, setTopicPattern("topic-.*", RegexSubscriptionMode.NonPersistentOnly).
And use setTopicPattern("topic-.*", RegexSubscriptionMode.PersistentOnly) will only subscribe to the persistent topics.

`non-persistent`
`RegexSubscriptionMode`
`RegexSubscriptionMode.NonPersistentOnly`
`setTopicPattern("topic-.*", RegexSubscriptionMode.NonPersistentOnly)`
`setTopicPattern("topic-.*", RegexSubscriptionMode.PersistentOnly)`
`persistent`

The regular expression should follow the topic naming pattern. Only the topic name part can be
a regular expression. For example, if you provide a simple topic regular expression like some-topic-\d,
we will filter all the topics under the public tenant with the default namespace.
And if the topic regular expression is flink/sample/topic-.*, we will filter all the topics under the flink tenant with the sample namespace.

`some-topic-\d`
`public`
`default`
`flink/sample/topic-.*`
`flink`
`sample`

> 
Currently, the latest released Pulsar 2.11.0 didn’t return the non-persistent topics correctly.
You can’t use regular expression for filtering non-persistent topics in Pulsar 2.11.0.
See this issue: https://github.com/apache/pulsar/issues/19316 for the detailed context of this bug.



Currently, the latest released Pulsar 2.11.0 didn’t return the non-persistent topics correctly.
You can’t use regular expression for filtering non-persistent topics in Pulsar 2.11.0.

`non-persistent`
`non-persistent`

See this issue: https://github.com/apache/pulsar/issues/19316 for the detailed context of this bug.


### Deserializer#


A deserializer (PulsarDeserializationSchema) is for decoding Pulsar messages from bytes.
You can configure the deserializer using setDeserializationSchema(PulsarDeserializationSchema).
The PulsarDeserializationSchema defines how to deserialize a Pulsar Message<byte[]>.

`PulsarDeserializationSchema`
`setDeserializationSchema(PulsarDeserializationSchema)`
`PulsarDeserializationSchema`
`Message<byte[]>`

If only the raw payload of a message (message data in bytes) is needed,
you can use the predefined PulsarDeserializationSchema. Pulsar connector provides three implementation methods.

`PulsarDeserializationSchema`
* Decode the message by using Pulsar’s Schema.
If using KeyValue type or Struct types, the pulsar Schema does not contain type class info. But it is
still needed to construct PulsarSchemaTypeInformation. So we provide two more APIs to pass the type info.
// Primitive types
PulsarSourceBuilder.setDeserializationSchema(Schema);

// Struct types (JSON, Protobuf, Avro, etc.)
PulsarSourceBuilder.setDeserializationSchema(Schema, Class);

// KeyValue type
PulsarSourceBuilder.setDeserializationSchema(Schema, Class, Class);

* Decode the message by using Flink’s DeserializationSchema
PulsarSourceBuilder.setDeserializationSchema(DeserializationSchema);

* Decode the message by using Flink’s TypeInformation
PulsarSourceBuilder.setDeserializationSchema(TypeInformation, ExecutionConfig);

`Schema`
`PulsarSchemaTypeInformation`

```
// Primitive types
PulsarSourceBuilder.setDeserializationSchema(Schema);

// Struct types (JSON, Protobuf, Avro, etc.)
PulsarSourceBuilder.setDeserializationSchema(Schema, Class);

// KeyValue type
PulsarSourceBuilder.setDeserializationSchema(Schema, Class, Class);

```

`// Primitive types
PulsarSourceBuilder.setDeserializationSchema(Schema);

// Struct types (JSON, Protobuf, Avro, etc.)
PulsarSourceBuilder.setDeserializationSchema(Schema, Class);

// KeyValue type
PulsarSourceBuilder.setDeserializationSchema(Schema, Class, Class);
`
`DeserializationSchema`

```
PulsarSourceBuilder.setDeserializationSchema(DeserializationSchema);

```

`PulsarSourceBuilder.setDeserializationSchema(DeserializationSchema);
`
`TypeInformation`

```
PulsarSourceBuilder.setDeserializationSchema(TypeInformation, ExecutionConfig);

```

`PulsarSourceBuilder.setDeserializationSchema(TypeInformation, ExecutionConfig);
`

Pulsar Message<byte[]> contains some extra properties,
such as message key, message publish time, message time, and application-defined key/value pairs etc.
These properties could be defined in the Message<byte[]> interface.

`Message<byte[]>`
`Message<byte[]>`

If you want to deserialize the Pulsar message by these properties, you need to implement PulsarDeserializationSchema.
Ensure that the TypeInformation from the PulsarDeserializationSchema.getProducedType() is correct.
Flink uses this TypeInformation to pass the messages to downstream operators.

`PulsarDeserializationSchema`
`TypeInformation`
`PulsarDeserializationSchema.getProducedType()`
`TypeInformation`

#### Schema Evolution in Source#


Schema evolution can be enabled by users using Pulsar’s Schema and
PulsarSourceBuilder.enableSchemaEvolution(). This means that any broker schema validation is in place.

`Schema`
`PulsarSourceBuilder.enableSchemaEvolution()`

```
Schema<SomePojo> schema = Schema.AVRO(SomePojo.class);

PulsarSource<SomePojo> source = PulsarSource.builder()
    ...
    .setDeserializationSchema(schema, SomePojo.class)
    .enableSchemaEvolution()
    .build();

```

`Schema<SomePojo> schema = Schema.AVRO(SomePojo.class);

PulsarSource<SomePojo> source = PulsarSource.builder()
    ...
    .setDeserializationSchema(schema, SomePojo.class)
    .enableSchemaEvolution()
    .build();
`

If you use Pulsar schema without enabling schema evolution, we will bypass the schema check. This may cause some
errors when you use a wrong schema to deserialize the messages.


#### Use Auto Consume Schema#


Pulsar provides Schema.AUTO_CONSUME() for consuming message without a predefined schema. This is always used when
the topic has multiple schemas and may not be compatible with each other. Pulsar will auto decode the message into a
GenericRecord for the user.

`Schema.AUTO_CONSUME()`
`GenericRecord`

But the PulsarSourceBuilder.setDeserializationSchema(Schema) method doesn’t support the Schema.AUTO_CONSUME().
Instead, we provide the GenericRecordDeserializer for deserializing the GenericRecord. You can implement this
interface and set it in the PulsarSourceBuilder.setDeserializationSchema(GenericRecordDeserializer).

`PulsarSourceBuilder.setDeserializationSchema(Schema)`
`Schema.AUTO_CONSUME()`
`GenericRecordDeserializer`
`GenericRecord`
`PulsarSourceBuilder.setDeserializationSchema(GenericRecordDeserializer)`

```
GenericRecordDeserializer<SomePojo> deserializer = ...
PulsarSource<SomePojo> source = PulsarSource.builder()
    ...
    .setDeserializationSchema(deserializer)
    .build();

```

`GenericRecordDeserializer<SomePojo> deserializer = ...
PulsarSource<SomePojo> source = PulsarSource.builder()
    ...
    .setDeserializationSchema(deserializer)
    .build();
`

> 
  Currently, auto consume schema only supports AVRO, JSON and Protobuf schemas.



### Define a RangeGenerator#


Ensure that you have provided a RangeGenerator implementation if you want to consume a subset of keys on the Pulsar connector.
The RangeGenerator generates a set of key hash ranges so that a respective reader subtask only dispatches
messages where the hash of the message key is contained in the specified range.

`RangeGenerator`
`RangeGenerator`

Since the Pulsar didn’t expose the key hash range method. We have to provide an FixedKeysRangeGenerator for end-user.
You can add the keys you want to consume, no need to calculate any hash ranges.
The key’s hash isn’t specified to only one key, so the consuming results may contain the messages with
different keys comparing the keys you have defined in this range generator.
Remember to use flink’s DataStream.filter() method after the Pulsar source.

`FixedKeysRangeGenerator`
`DataStream.filter()`

```
FixedKeysRangeGenerator.builder()
    .supportNullKey()
    .key("someKey")
    .keys(Arrays.asList("key1", "key2"))
    .build()

```

`FixedKeysRangeGenerator.builder()
    .supportNullKey()
    .key("someKey")
    .keys(Arrays.asList("key1", "key2"))
    .build()
`

### Starting Position#


The Pulsar source is able to consume messages starting from different positions by setting the setStartCursor(StartCursor) option.
Built-in start cursors include:

`setStartCursor(StartCursor)`
* 
Start from the earliest available message in the topic.






Java
StartCursor.earliest();

Python
StartCursor.earliest()



* 
Start from the latest available message in the topic.






Java
StartCursor.latest();

Python
StartCursor.latest()



* 
Start from a specified message between the earliest and the latest.
The Pulsar connector consumes from the latest available message if the message ID does not exist.
The start message is included in consuming result.






Java
StartCursor.fromMessageId(MessageId);

Python
StartCursor.from_message_id(message_id)



* 
Start from a specified message between the earliest and the latest.
The Pulsar connector consumes from the latest available message if the message ID doesn’t exist.
Include or exclude the start message by using the second boolean parameter.






Java
StartCursor.fromMessageId(MessageId, boolean);

Python
StartCursor.from_message_id(message_id, boolean)



* 
Start from the specified message publish time by Message<byte[]>.getPublishTime().
This method is deprecated because the name is totally wrong which may cause confuse.
You can use StartCursor.fromPublishTime(long) instead.

Java
StartCursor.fromMessageTime(long);

Python
StartCursor.from_message_time(int)


* 
Start from the specified message publish time by Message<byte[]>.getPublishTime().






Java
StartCursor.fromPublishTime(long);

Python
StartCursor.from_publish_time(int)




Start from the earliest available message in the topic.






Java
StartCursor.earliest();

Python
StartCursor.earliest()




```
StartCursor.earliest();

```

`StartCursor.earliest();
`

```
StartCursor.earliest()

```

`StartCursor.earliest()
`

Start from the latest available message in the topic.






Java
StartCursor.latest();

Python
StartCursor.latest()




```
StartCursor.latest();

```

`StartCursor.latest();
`

```
StartCursor.latest()

```

`StartCursor.latest()
`

Start from a specified message between the earliest and the latest.
The Pulsar connector consumes from the latest available message if the message ID does not exist.


The start message is included in consuming result.






Java
StartCursor.fromMessageId(MessageId);

Python
StartCursor.from_message_id(message_id)




```
StartCursor.fromMessageId(MessageId);

```

`StartCursor.fromMessageId(MessageId);
`

```
StartCursor.from_message_id(message_id)

```

`StartCursor.from_message_id(message_id)
`

Start from a specified message between the earliest and the latest.
The Pulsar connector consumes from the latest available message if the message ID doesn’t exist.


Include or exclude the start message by using the second boolean parameter.






Java
StartCursor.fromMessageId(MessageId, boolean);

Python
StartCursor.from_message_id(message_id, boolean)




```
StartCursor.fromMessageId(MessageId, boolean);

```

`StartCursor.fromMessageId(MessageId, boolean);
`

```
StartCursor.from_message_id(message_id, boolean)

```

`StartCursor.from_message_id(message_id, boolean)
`

Start from the specified message publish time by Message<byte[]>.getPublishTime().
This method is deprecated because the name is totally wrong which may cause confuse.
You can use StartCursor.fromPublishTime(long) instead.

`Message<byte[]>.getPublishTime()`
`StartCursor.fromPublishTime(long)`

```
StartCursor.fromMessageTime(long);

```

`StartCursor.fromMessageTime(long);
`

```
StartCursor.from_message_time(int)

```

`StartCursor.from_message_time(int)
`

Start from the specified message publish time by Message<byte[]>.getPublishTime().






Java
StartCursor.fromPublishTime(long);

Python
StartCursor.from_publish_time(int)



`Message<byte[]>.getPublishTime()`

```
StartCursor.fromPublishTime(long);

```

`StartCursor.fromPublishTime(long);
`

```
StartCursor.from_publish_time(int)

```

`StartCursor.from_publish_time(int)
`

The StartCursor is used when the corresponding subscription is not created in Pulsar by default.
The priority of the consumption start position is, checkpoint > existed subscription position > StartCursor.
Sometimes, the end user may want to force the start position by using StartCursor. You should enable the pulsar.source.resetSubscriptionCursor
option and start the pipeline without the saved checkpoint files.
It is important to note that the given consumption position in the checkpoint is always the highest priority.

`StartCursor`
`StartCursor`
`StartCursor`
`pulsar.source.resetSubscriptionCursor`

> 
  Each Pulsar message belongs to an ordered sequence on its topic.
The sequence ID (MessageId) of the message is ordered in that sequence.
The MessageId contains some extra information (the ledger, entry, partition) about how the message is stored,
you can create a MessageId by using DefaultImplementation.newMessageId(long ledgerId, long entryId, int partitionIndex).


`MessageId`
`MessageId`
`MessageId`
`DefaultImplementation.newMessageId(long ledgerId, long entryId, int partitionIndex)`

### Boundedness#


The Pulsar source supports streaming and batch execution mode.
By default, the PulsarSource is configured for unbounded data.

`PulsarSource`

For unbounded data the Pulsar source never stops until a Flink job is stopped or failed.
You can use the setUnboundedStopCursor(StopCursor) to set the Pulsar source to stop at a specific stop position.

`setUnboundedStopCursor(StopCursor)`

You can use setBoundedStopCursor(StopCursor) to specify a stop position for bounded data.

`setBoundedStopCursor(StopCursor)`

Built-in stop cursors include:

* 
The Pulsar source never stops consuming messages.






Java
StopCursor.never();

Python
StopCursor.never()



* 
Stop at the latest available message when the Pulsar source starts consuming messages.






Java
StopCursor.latest();

Python
StopCursor.latest()



* 
Stop when the connector meets a given message, or stop at a message which is produced after this given message.






Java
StopCursor.atMessageId(MessageId);

Python
StopCursor.at_message_id(message_id)



* 
Stop but include the given message in the consuming result.






Java
StopCursor.afterMessageId(MessageId);

Python
StopCursor.after_message_id(message_id)



* 
Stop at the specified event time by Message<byte[]>.getEventTime(). The message with the
given event time won’t be included in the consuming result.






Java
StopCursor.atEventTime(long);

Python
StopCursor.at_event_time(int)



* 
Stop after the specified event time by Message<byte[]>.getEventTime(). The message with the
given event time will be included in the consuming result.






Java
StopCursor.afterEventTime(long);

Python
StopCursor.after_event_time(int)



* 
Stop at the specified publish time by Message<byte[]>.getPublishTime(). The message with the
given publish time won’t be included in the consuming result.






Java
StopCursor.atPublishTime(long);

Python
StopCursor.at_publish_time(int)



* 
Stop after the specified publish time by Message<byte[]>.getPublishTime(). The message with the
given publish time will be included in the consuming result.






Java
StopCursor.afterPublishTime(long);

Python
StopCursor.after_publish_time(int)




The Pulsar source never stops consuming messages.






Java
StopCursor.never();

Python
StopCursor.never()




```
StopCursor.never();

```

`StopCursor.never();
`

```
StopCursor.never()

```

`StopCursor.never()
`

Stop at the latest available message when the Pulsar source starts consuming messages.






Java
StopCursor.latest();

Python
StopCursor.latest()




```
StopCursor.latest();

```

`StopCursor.latest();
`

```
StopCursor.latest()

```

`StopCursor.latest()
`

Stop when the connector meets a given message, or stop at a message which is produced after this given message.






Java
StopCursor.atMessageId(MessageId);

Python
StopCursor.at_message_id(message_id)




```
StopCursor.atMessageId(MessageId);

```

`StopCursor.atMessageId(MessageId);
`

```
StopCursor.at_message_id(message_id)

```

`StopCursor.at_message_id(message_id)
`

Stop but include the given message in the consuming result.






Java
StopCursor.afterMessageId(MessageId);

Python
StopCursor.after_message_id(message_id)




```
StopCursor.afterMessageId(MessageId);

```

`StopCursor.afterMessageId(MessageId);
`

```
StopCursor.after_message_id(message_id)

```

`StopCursor.after_message_id(message_id)
`

Stop at the specified event time by Message<byte[]>.getEventTime(). The message with the
given event time won’t be included in the consuming result.






Java
StopCursor.atEventTime(long);

Python
StopCursor.at_event_time(int)



`Message<byte[]>.getEventTime()`

```
StopCursor.atEventTime(long);

```

`StopCursor.atEventTime(long);
`

```
StopCursor.at_event_time(int)

```

`StopCursor.at_event_time(int)
`

Stop after the specified event time by Message<byte[]>.getEventTime(). The message with the
given event time will be included in the consuming result.






Java
StopCursor.afterEventTime(long);

Python
StopCursor.after_event_time(int)



`Message<byte[]>.getEventTime()`

```
StopCursor.afterEventTime(long);

```

`StopCursor.afterEventTime(long);
`

```
StopCursor.after_event_time(int)

```

`StopCursor.after_event_time(int)
`

Stop at the specified publish time by Message<byte[]>.getPublishTime(). The message with the
given publish time won’t be included in the consuming result.






Java
StopCursor.atPublishTime(long);

Python
StopCursor.at_publish_time(int)



`Message<byte[]>.getPublishTime()`

```
StopCursor.atPublishTime(long);

```

`StopCursor.atPublishTime(long);
`

```
StopCursor.at_publish_time(int)

```

`StopCursor.at_publish_time(int)
`

Stop after the specified publish time by Message<byte[]>.getPublishTime(). The message with the
given publish time will be included in the consuming result.






Java
StopCursor.afterPublishTime(long);

Python
StopCursor.after_publish_time(int)



`Message<byte[]>.getPublishTime()`

```
StopCursor.afterPublishTime(long);

```

`StopCursor.afterPublishTime(long);
`

```
StopCursor.after_publish_time(int)

```

`StopCursor.after_publish_time(int)
`

### Source Configurable Options#


In addition to configuration options described above, you can set arbitrary options for PulsarClient,
PulsarAdmin, Pulsar Consumer and PulsarSource by using setConfig(ConfigOption<T>, T),
setConfig(Configuration) and setConfig(Properties).

`PulsarClient`
`PulsarAdmin`
`Consumer`
`PulsarSource`
`setConfig(ConfigOption<T>, T)`
`setConfig(Configuration)`
`setConfig(Properties)`

#### PulsarClient Options#


The Pulsar connector uses the client API
to create the Consumer instance. The Pulsar connector extracts most parts of Pulsar’s ClientConfigurationData,
which is required for creating a PulsarClient, as Flink configuration options in PulsarOptions.

`Consumer`
`ClientConfigurationData`
`PulsarClient`
`PulsarOptions`

##### pulsar.client.authParamMap


##### pulsar.client.authParams

`key1:val1,key2:val2`

##### pulsar.client.authPluginClassName


##### pulsar.client.concurrentLookupRequest

`PulsarClient`

##### pulsar.client.connectionMaxIdleSeconds


##### pulsar.client.connectionTimeoutMs


##### pulsar.client.connectionsPerBroker


##### pulsar.client.dnsLookupBindAddress

`0.0.0.0:0`
`0`
`65535`
`host:port`

##### pulsar.client.enableBusyWait


##### pulsar.client.enableTransaction

`transactionCoordinatorClient`
`PulsarClient`

##### pulsar.client.initialBackoffIntervalNanos


##### pulsar.client.keepAliveIntervalSeconds


##### pulsar.client.listenerName

`listenerName`
`advertisedListener`

##### pulsar.client.lookupTimeoutMs


##### pulsar.client.maxBackoffIntervalNanos


##### pulsar.client.maxLookupRedirects


##### pulsar.client.maxLookupRequest

`pulsar.client.concurrentLookupRequest`
`pulsar.client.concurrentLookupRequest`
`pulsar.client.concurrentLookupRequest`
`maxLookupRequests`

##### pulsar.client.maxNumberOfRejectedRequestPerConnection


##### pulsar.client.memoryLimitBytes

`0`

##### pulsar.client.numIoThreads


##### pulsar.client.numListenerThreads

`listener`

##### pulsar.client.operationTimeoutMs


##### pulsar.client.proxyProtocol


Enum

`pulsar.client.proxyServiceUrl`
* "SNI"

##### pulsar.client.proxyServiceUrl


##### pulsar.client.requestTimeoutMs


##### pulsar.client.serviceUrl

* This is an example of localhost: pulsar://localhost:6650.
* If you have multiple brokers, the URL is as: pulsar://localhost:6550,localhost:6651,localhost:6652
* A URL for a production Pulsar cluster is as: pulsar://pulsar.us-west.example.com:6650
* If you use TLS authentication, the URL is as pulsar+ssl://pulsar.us-west.example.com:6651
`localhost`
`pulsar://localhost:6650`
`pulsar://localhost:6550,localhost:6651,localhost:6652`
`pulsar://pulsar.us-west.example.com:6650`
`pulsar+ssl://pulsar.us-west.example.com:6651`

##### pulsar.client.socks5ProxyAddress

`host:port`

##### pulsar.client.socks5ProxyPassword


##### pulsar.client.socks5ProxyUsername


##### pulsar.client.sslProvider


##### pulsar.client.statsIntervalSeconds

* Stats is activated with positive statsInterval
* Set statsIntervalSeconds to 1 second at least.
`statsInterval`
`statsIntervalSeconds`

##### pulsar.client.tlsAllowInsecureConnection


##### pulsar.client.tlsCertificateFilePath


##### pulsar.client.tlsCiphers


##### pulsar.client.tlsHostnameVerificationEnable


##### pulsar.client.tlsKeyFilePath


##### pulsar.client.tlsKeyStorePassword


##### pulsar.client.tlsKeyStorePath


##### pulsar.client.tlsKeyStoreType


##### pulsar.client.tlsProtocols


##### pulsar.client.tlsTrustCertsFilePath


##### pulsar.client.tlsTrustStorePassword


##### pulsar.client.tlsTrustStorePath


##### pulsar.client.tlsTrustStoreType


##### pulsar.client.useKeyStoreTls

`false`

##### pulsar.client.useTcpNoDelay

`false`
`true`

#### PulsarAdmin Options#


The admin API is used for querying topic metadata
and for discovering the desired topics when the Pulsar connector uses topic-pattern subscription.
It shares most part of the configuration options with the client API.
The configuration options listed here are only used in the admin API.
They are also defined in PulsarOptions.

`PulsarOptions`

##### pulsar.admin.adminUrl

`http://my-broker.example.com:8080`
`https://my-broker.example.com:8443`

##### pulsar.admin.autoCertRefreshTime


##### pulsar.admin.connectTimeout


##### pulsar.admin.readTimeout


##### pulsar.admin.requestRates


##### pulsar.admin.requestRetries


##### pulsar.admin.requestTimeout


##### pulsar.admin.requestWaitMillis


#### Pulsar Consumer Options#


In general, Pulsar provides the Reader API and Consumer API for consuming messages in different scenarios.
The Pulsar connector uses the Consumer API. It extracts most parts of Pulsar’s ConsumerConfigurationData as Flink configuration options in PulsarSourceOptions.

`ConsumerConfigurationData`
`PulsarSourceOptions`

##### pulsar.consumer.ackReceiptEnabled


##### pulsar.consumer.ackTimeoutMillis


##### pulsar.consumer.acknowledgementsGroupTimeMicros

`100Î¼s`
`0`

##### pulsar.consumer.autoAckOldestChunkedMessageOnQueueFull

`pulsar.consumer.maxPendingChunkedMessage`
`pulsar.consumer.autoAckOldestChunkedMessageOnQueueFull`

##### pulsar.consumer.autoScaledReceiverQueueSizeEnabled

`pulsar.consumer.receiverQueueSize`

##### pulsar.consumer.consumerName


##### pulsar.consumer.cryptoFailureAction


Enum

* FAIL: this is the default option to fail messages until crypto succeeds.
* DISCARD: silently acknowledge but do not deliver messages to an application.
* CONSUME: deliver encrypted messages to applications. It is the application's responsibility to decrypt the message.
`FAIL`
`DISCARD`
`CONSUME`
`EncryptionContext`
* "FAIL"
* "DISCARD"
* "CONSUME"

##### pulsar.consumer.deadLetterPolicy.deadLetterTopic


##### pulsar.consumer.deadLetterPolicy.maxRedeliverCount


##### pulsar.consumer.deadLetterPolicy.retryLetterTopic


##### pulsar.consumer.expireTimeOfIncompleteChunkedMessageMillis


##### pulsar.consumer.maxPendingChunkedMessage

`pulsar.consumer.maxPendingChunkedMessage`
`pulsar.consumer.autoAckOldestChunkedMessageOnQueueFull`

##### pulsar.consumer.maxTotalReceiverQueueSizeAcrossPartitions


##### pulsar.consumer.negativeAckRedeliveryDelayMicros

`Consumer.negativeAcknowledge(Message)`

##### pulsar.consumer.poolMessages


##### pulsar.consumer.priorityLevel

`priorityLevel`
`priorityLevel`

##### pulsar.consumer.properties

`properties`

##### pulsar.consumer.readCompacted

`readCompacted`
`readCompacted`
`PulsarClientException`

##### pulsar.consumer.receiverQueueSize

`Receive`

##### pulsar.consumer.replicateSubscriptionState

`replicateSubscriptionState`

##### pulsar.consumer.retryEnable


##### pulsar.consumer.subscriptionMode


Enum

* Durable: Make the subscription to be backed by a durable cursor that will retain messages and persist the current position.
* NonDurable: Lightweight subscription mode that doesn't have a durable cursor associated
`Durable`
`NonDurable`
* "Durable"
* "NonDurable"

##### pulsar.consumer.subscriptionName


##### pulsar.consumer.subscriptionProperties


##### pulsar.consumer.tickDurationMillis

`tickDurationMillis`

#### PulsarSource Options#


The configuration options below are mainly used for customizing the performance and message acknowledgement behavior.
You can ignore them if you do not have any performance issues.


##### pulsar.source.allowKeySharedOutOfOrderDelivery


##### pulsar.source.autoCommitCursorInterval


##### pulsar.source.enableAutoAcknowledgeMessage

`true`

##### pulsar.source.enableMetrics

`pulsar.client.statsIntervalSeconds`

##### pulsar.source.enableSchemaEvolution

`PulsarSourceBuilder.setDeserializationSchema(Schema)`
`Schema`

##### pulsar.source.fetchOneMessageTime

`pulsar.source.maxFetchTime`

##### pulsar.source.maxFetchRecords

`pulsar.source.maxFetchTime`

##### pulsar.source.maxFetchTime

`pulsar.source.maxFetchRecords`

##### pulsar.source.partitionDiscoveryIntervalMs


##### pulsar.source.resetSubscriptionCursor

`StartCursor`
`StartCursor`

##### pulsar.source.verifyInitialOffsets


Enum

* "FAIL_ON_MISMATCH": Fail the consuming from Pulsar when we don't find the related cursor.
* "WARN_ON_MISMATCH": Print a warn message and start consuming from the valid offset.

### Dynamic Partition Discovery#


To handle scenarios like topic scaling-out or topic creation without restarting the Flink
job, the Pulsar source periodically discover new partitions under a provided
topic-partition subscription pattern. To enable partition discovery, you can set a non-negative value for
the PulsarSourceOptions.PULSAR_PARTITION_DISCOVERY_INTERVAL_MS option:

`PulsarSourceOptions.PULSAR_PARTITION_DISCOVERY_INTERVAL_MS`

```
// discover new partitions per 10 seconds
PulsarSource.builder()
    .setConfig(PulsarSourceOptions.PULSAR_PARTITION_DISCOVERY_INTERVAL_MS, 10000);

```

`// discover new partitions per 10 seconds
PulsarSource.builder()
    .setConfig(PulsarSourceOptions.PULSAR_PARTITION_DISCOVERY_INTERVAL_MS, 10000);
`

```
# discover new partitions per 10 seconds
PulsarSource.builder()
    .set_config("pulsar.source.partitionDiscoveryIntervalMs", 10000)

```

`# discover new partitions per 10 seconds
PulsarSource.builder()
    .set_config("pulsar.source.partitionDiscoveryIntervalMs", 10000)
`

> 

Partition discovery is enabled by default. The Pulsar connector queries the topic metadata every 5 minutes.
To disable partition discovery, you need to set a negative partition discovery interval.
Partition discovery is disabled for bounded data even if you set this option with a non-negative value.



* Partition discovery is enabled by default. The Pulsar connector queries the topic metadata every 5 minutes.
* To disable partition discovery, you need to set a negative partition discovery interval.
* Partition discovery is disabled for bounded data even if you set this option with a non-negative value.

### Event Time and Watermarks#


By default, the message uses the timestamp embedded in Pulsar Message<byte[]> as the event time.
You can define your own WatermarkStrategy to extract the event time from the message,
and emit the watermark downstream:

`Message<byte[]>`
`WatermarkStrategy`

```
env.fromSource(pulsarSource, new CustomWatermarkStrategy(), "Pulsar Source With Custom Watermark Strategy");

```

`env.fromSource(pulsarSource, new CustomWatermarkStrategy(), "Pulsar Source With Custom Watermark Strategy");
`

```
env.from_source(pulsar_source, CustomWatermarkStrategy(), "Pulsar Source With Custom Watermark Strategy")

```

`env.from_source(pulsar_source, CustomWatermarkStrategy(), "Pulsar Source With Custom Watermark Strategy")
`

This documentation describes
details about how to define a WatermarkStrategy.

`WatermarkStrategy`

### Message Acknowledgement#


When a subscription is created, Pulsar retains all messages,
even if the consumer is disconnected. The retained messages are discarded only when the connector acknowledges that all these messages are processed successfully.


We use Exclusive subscription as the default subscription type. It supports cumulative acknowledgment. In this subscription type,
Flink only needs to acknowledge the latest successfully consumed message. All the message before the given message are marked
with a consumed status.

`Exclusive`

The Pulsar source acknowledges the current consuming message when checkpoints are completed,
to ensure the consistency between Flink’s checkpoint state and committed position on the Pulsar brokers.


If checkpointing is disabled, Pulsar source periodically acknowledges messages.
You can use the PulsarSourceOptions.PULSAR_AUTO_COMMIT_CURSOR_INTERVAL option to set the acknowledgement period.

`PulsarSourceOptions.PULSAR_AUTO_COMMIT_CURSOR_INTERVAL`

Pulsar source does NOT rely on committed positions for fault tolerance.
Acknowledging messages is only for exposing the progress of consumers and monitoring on these two subscription types.


## Pulsar Sink#


The Pulsar Sink supports writing records into one or more Pulsar topics or a specified list of Pulsar partitions.


> 
This part describes the Pulsar sink based on the new
data sink API.
If you still want to use the legacy SinkFunction or on Flink 1.14 or previous releases, just use the StreamNative’s
pulsar-flink.



This part describes the Pulsar sink based on the new
data sink API.


If you still want to use the legacy SinkFunction or on Flink 1.14 or previous releases, just use the StreamNative’s
pulsar-flink.

`SinkFunction`

### Usage#


The Pulsar Sink uses a builder class to construct the PulsarSink instance.
This example writes a String record to a Pulsar topic with at-least-once delivery guarantee.

`PulsarSink`

```
DataStream<String> stream = ...

PulsarSink<String> sink = PulsarSink.builder()
    .setServiceUrl(serviceUrl)
    .setAdminUrl(adminUrl)
    .setTopics("topic1")
    .setSerializationSchema(new SimpleStringSchema())
    .setDeliveryGuarantee(DeliveryGuarantee.AT_LEAST_ONCE)
    .build();

stream.sinkTo(sink);

```

`DataStream<String> stream = ...

PulsarSink<String> sink = PulsarSink.builder()
    .setServiceUrl(serviceUrl)
    .setAdminUrl(adminUrl)
    .setTopics("topic1")
    .setSerializationSchema(new SimpleStringSchema())
    .setDeliveryGuarantee(DeliveryGuarantee.AT_LEAST_ONCE)
    .build();

stream.sinkTo(sink);
`

```
stream = ...

pulsar_sink = PulsarSink.builder() \
    .set_service_url('pulsar://localhost:6650') \
    .set_admin_url('http://localhost:8080') \
    .set_topics("topic1") \
    .set_serialization_schema(SimpleStringSchema()) \
    .set_delivery_guarantee(DeliveryGuarantee.AT_LEAST_ONCE) \
    .build()

stream.sink_to(pulsar_sink)

```

`stream = ...

pulsar_sink = PulsarSink.builder() \
    .set_service_url('pulsar://localhost:6650') \
    .set_admin_url('http://localhost:8080') \
    .set_topics("topic1") \
    .set_serialization_schema(SimpleStringSchema()) \
    .set_delivery_guarantee(DeliveryGuarantee.AT_LEAST_ONCE) \
    .build()

stream.sink_to(pulsar_sink)
`

The following properties are required for building PulsarSink:

* Pulsar service url, configured by setServiceUrl(String)
* Pulsar service http url (aka. admin url), configured by setAdminUrl(String)
* Topics / partitions to write, see Producing to topics for more details.
* Serializer to generate Pulsar messages, see serializer for more details.
`setServiceUrl(String)`
`setAdminUrl(String)`

It is recommended to set the producer name in Pulsar Source by setProducerName(String).
This sets a unique name for the Flink connector in the Pulsar statistic dashboard.
You can use it to monitor the performance of your Flink connector and applications.

`setProducerName(String)`

### Producing to topics#


Defining the topics for producing is similar to the topic-partition subscription
in the Pulsar source. We support a mix-in style of topic setting. You can provide a list of topics,
partitions, or both of them.


```
// Topic "some-topic1" and "some-topic2"
PulsarSink.builder().setTopics("some-topic1", "some-topic2")

// Partition 0 and 2 of topic "topic-a"
PulsarSink.builder().setTopics("topic-a-partition-0", "topic-a-partition-2")

// Partition 0 and 2 of topic "topic-a" and topic "some-topic2"
PulsarSink.builder().setTopics("topic-a-partition-0", "topic-a-partition-2", "some-topic2")

```

`// Topic "some-topic1" and "some-topic2"
PulsarSink.builder().setTopics("some-topic1", "some-topic2")

// Partition 0 and 2 of topic "topic-a"
PulsarSink.builder().setTopics("topic-a-partition-0", "topic-a-partition-2")

// Partition 0 and 2 of topic "topic-a" and topic "some-topic2"
PulsarSink.builder().setTopics("topic-a-partition-0", "topic-a-partition-2", "some-topic2")
`

```
# Topic "some-topic1" and "some-topic2"
PulsarSink.builder().set_topics(["some-topic1", "some-topic2"])

# Partition 0 and 2 of topic "topic-a"
PulsarSink.builder().set_topics(["topic-a-partition-0", "topic-a-partition-2"])

# Partition 0 and 2 of topic "topic-a" and topic "some-topic2"
PulsarSink.builder().set_topics(["topic-a-partition-0", "topic-a-partition-2", "some-topic2"])

```

`# Topic "some-topic1" and "some-topic2"
PulsarSink.builder().set_topics(["some-topic1", "some-topic2"])

# Partition 0 and 2 of topic "topic-a"
PulsarSink.builder().set_topics(["topic-a-partition-0", "topic-a-partition-2"])

# Partition 0 and 2 of topic "topic-a" and topic "some-topic2"
PulsarSink.builder().set_topics(["topic-a-partition-0", "topic-a-partition-2", "some-topic2"])
`

The topics you provide support auto partition discovery. We query the topic metadata from the Pulsar in a fixed interval.
You can use the PulsarSinkOptions.PULSAR_TOPIC_METADATA_REFRESH_INTERVAL option to change the discovery interval option.

`PulsarSinkOptions.PULSAR_TOPIC_METADATA_REFRESH_INTERVAL`

Configuring writing targets can be replaced by using a custom [TopicRouter]
message routing. Configuring partitions on the Pulsar connector is explained in the flexible topic naming section.

`TopicRouter`

> 
If you build the Pulsar sink based on both the topic and its corresponding partitions, Pulsar sink merges them and only uses the topic.
For example, when using the PulsarSink.builder().setTopics("some-topic1", "some-topic1-partition-0") option to build the Pulsar sink,
this is simplified to PulsarSink.builder().setTopics("some-topic1").



If you build the Pulsar sink based on both the topic and its corresponding partitions, Pulsar sink merges them and only uses the topic.


For example, when using the PulsarSink.builder().setTopics("some-topic1", "some-topic1-partition-0") option to build the Pulsar sink,
this is simplified to PulsarSink.builder().setTopics("some-topic1").

`PulsarSink.builder().setTopics("some-topic1", "some-topic1-partition-0")`
`PulsarSink.builder().setTopics("some-topic1")`

#### Dynamic Topics by incoming messages#


Topics could be defined by the incoming messages instead of providing the fixed topic set in builder. You can dynamically
provide the topic by in a custom TopicRouter. The topic metadata can be queried by using PulsarSinkContext.topicMetadata(String)
and the query result would be cached and expire in PulsarSinkOptions.PULSAR_TOPIC_METADATA_REFRESH_INTERVAL milliseconds.

`TopicRouter`
`PulsarSinkContext.topicMetadata(String)`
`PulsarSinkOptions.PULSAR_TOPIC_METADATA_REFRESH_INTERVAL`

If you want to write to a non-existed topic, just return it in TopicRouter. Pulsar connector will try to create it.

`TopicRouter`

> 
You need to enable the topic auto creation in Pulsar’s broker.conf when you want to write messages to a non-existed topic.
Set the allowAutoTopicCreation=true to enable it.
The allowAutoTopicCreationType option in broker.conf is used to control the type of topic that is allowed to be automatically created.

non-partitioned: The default type for the auto-created topic.
It doesn’t have any partition and can’t be converted to a partitioned topic.
partitioned: The topic will be created as a partitioned topic.
Set the defaultNumPartitions option to control the auto created partition size.




You need to enable the topic auto creation in Pulsar’s broker.conf when you want to write messages to a non-existed topic.
Set the allowAutoTopicCreation=true to enable it.

`broker.conf`
`allowAutoTopicCreation=true`

The allowAutoTopicCreationType option in broker.conf is used to control the type of topic that is allowed to be automatically created.

`allowAutoTopicCreationType`
`broker.conf`
* non-partitioned: The default type for the auto-created topic.
It doesn’t have any partition and can’t be converted to a partitioned topic.
* partitioned: The topic will be created as a partitioned topic.
Set the defaultNumPartitions option to control the auto created partition size.
`non-partitioned`
`partitioned`
`defaultNumPartitions`

### Serializer#


A serializer (PulsarSerializationSchema) is required for serializing the record instance into bytes.
Similar to PulsarSource, Pulsar sink supports both Flink’s SerializationSchema and
Pulsar’s Schema. But Pulsar’s Schema.AUTO_PRODUCE_BYTES() is not supported.

`PulsarSerializationSchema`
`PulsarSource`
`SerializationSchema`
`Schema`
`Schema.AUTO_PRODUCE_BYTES()`

If you do not need the message key and other message properties in Pulsar’s
Message interface,
you can use the predefined PulsarSerializationSchema. The Pulsar sink provides two implementation methods.

`PulsarSerializationSchema`
* Encode the message by using Pulsar’s Schema.
// Primitive types
PulsarSinkBuilder.setSerializationSchema(Schema)

// Struct types (JSON, Protobuf, Avro, etc.)
PulsarSinkBuilder.setSerializationSchema(Schema, Class)

// KeyValue type
PulsarSinkBuilder.setSerializationSchema(Schema, Class, Class)

* Encode the message by using Flink’s SerializationSchema
PulsarSinkBuilder.setSerializationSchema(SerializationSchema)


```
// Primitive types
PulsarSinkBuilder.setSerializationSchema(Schema)

// Struct types (JSON, Protobuf, Avro, etc.)
PulsarSinkBuilder.setSerializationSchema(Schema, Class)

// KeyValue type
PulsarSinkBuilder.setSerializationSchema(Schema, Class, Class)

```

`// Primitive types
PulsarSinkBuilder.setSerializationSchema(Schema)

// Struct types (JSON, Protobuf, Avro, etc.)
PulsarSinkBuilder.setSerializationSchema(Schema, Class)

// KeyValue type
PulsarSinkBuilder.setSerializationSchema(Schema, Class, Class)
`
`SerializationSchema`

```
PulsarSinkBuilder.setSerializationSchema(SerializationSchema)

```

`PulsarSinkBuilder.setSerializationSchema(SerializationSchema)
`

#### Schema Evolution in Sink#


Schema evolution can be enabled by users using Pulsar’s Schema
and PulsarSinkBuilder.enableSchemaEvolution(). This means that any broker schema validation is in place.

`Schema`
`PulsarSinkBuilder.enableSchemaEvolution()`

```
Schema<SomePojo> schema = Schema.AVRO(SomePojo.class);

PulsarSink<SomePojo> sink = PulsarSink.builder()
    ...
    .setSerializationSchema(schema, SomePojo.class)
    .enableSchemaEvolution()
    .build();

```

`Schema<SomePojo> schema = Schema.AVRO(SomePojo.class);

PulsarSink<SomePojo> sink = PulsarSink.builder()
    ...
    .setSerializationSchema(schema, SomePojo.class)
    .enableSchemaEvolution()
    .build();
`

> 
If you use Pulsar schema without enabling schema evolution, the target topic will have a Schema.BYTES schema.
But Schema.BYTES isn’t stored in any Pulsar’s topic. An auto-created topic in this way will present no schema.
Consumers will need to handle deserialization without Pulsar’s Schema (if needed) themselves.
For example, if you set PulsarSinkBuilder.setSerializationSchema(Schema.STRING) without enabling schema evolution,
the schema stored in Pulsar topics is Schema.BYTES.



If you use Pulsar schema without enabling schema evolution, the target topic will have a Schema.BYTES schema.
But Schema.BYTES isn’t stored in any Pulsar’s topic. An auto-created topic in this way will present no schema.
Consumers will need to handle deserialization without Pulsar’s Schema (if needed) themselves.

`Schema.BYTES`
`Schema.BYTES`
`Schema`

For example, if you set PulsarSinkBuilder.setSerializationSchema(Schema.STRING) without enabling schema evolution,
the schema stored in Pulsar topics is Schema.BYTES.

`PulsarSinkBuilder.setSerializationSchema(Schema.STRING)`
`Schema.BYTES`

#### PulsarMessage<byte[]> validation#


Pulsar topic always has at least one schema. The Schema.BYTES is the default one for any topic without schema being set.
But sending messages bytes with Schema.BYTES bypass the schema validate. So the message sent with SerializationSchema
and Schema which doesn’t enable the schema evolution may save the invalid messages in the topic.

`Schema.BYTES`
`Schema.BYTES`
`SerializationSchema`
`Schema`

You can enable the pulsar.sink.validateSinkMessageBytes option to let the connector use the Pulsar’s Schema.AUTO_PRODUCE_BYTES()
which supports extra check for the message bytes before sending. It will query the latest schema in topic and use it to
validate the message bytes.

`pulsar.sink.validateSinkMessageBytes`
`Schema.AUTO_PRODUCE_BYTES()`

But some schemas in Pulsar don’t support validation, so we disable this option by default. you should use it at your own risk.


#### Custom serializer#


You can have your own serialization logic by implementing the PulsarSerializationSchema interface. The return type
for this interface is PulsarMessage which you can’t create it directly. Instead, we use builder method for creating
three types of the Pulsar messages.

`PulsarSerializationSchema`
`PulsarMessage`
* Create a message with a Pulsar Scheme. This is always when you know the schema in topic.
We will check if the given schema is compatible in the correspond topic.
PulsarMessage.builder(Schema<M> schema, M message)
    ...
    .build();

* Create the message without any Pulsar Scheme. The message type can only be the byte array.
It won’t validate the message bytes by default.
PulsarMessage.builder(byte[] bytes)
    ...
    .build();

* Create a tombstone message with empty payloads. Tombstone is a special message which is
supported in Pulsar.
PulsarMessage.builder()
    ...
    .build();

`Scheme`

```
PulsarMessage.builder(Schema<M> schema, M message)
    ...
    .build();

```

`PulsarMessage.builder(Schema<M> schema, M message)
    ...
    .build();
`
`Scheme`

```
PulsarMessage.builder(byte[] bytes)
    ...
    .build();

```

`PulsarMessage.builder(byte[] bytes)
    ...
    .build();
`

```
PulsarMessage.builder()
    ...
    .build();

```

`PulsarMessage.builder()
    ...
    .build();
`

### Message Routing#


Routing in Pulsar Sink is operated on the partition level. For a list of partitioned topics,
the routing algorithm first collects all partitions from different topics, and then calculates routing within all the partitions.
By default, Pulsar Sink supports two router implementations.

* 
KeyHashTopicRouter: use the hashcode of the message’s key to decide the topic partition that messages are sent to.
The message key is provided by PulsarSerializationSchema.key(IN, PulsarSinkContext)
You need to implement this interface and extract the message key when you want to send the message with the same key to the same topic partition.
If you do not provide the message key. A topic  partition is randomly chosen from the topic list.
The message key can be hashed in two ways: MessageKeyHash.JAVA_HASH and MessageKeyHash.MURMUR3_32_HASH.
You can use the PulsarSinkOptions.PULSAR_MESSAGE_KEY_HASH option to choose the hash method.

* 
RoundRobinRouter: Round-robin among all the partitions.
All messages are sent to the first partition, and switch to the next partition after sending
a fixed number of messages. The batch size can be customized by the PulsarSinkOptions.PULSAR_BATCHING_MAX_MESSAGES option.


KeyHashTopicRouter: use the hashcode of the message’s key to decide the topic partition that messages are sent to.

`KeyHashTopicRouter`

The message key is provided by PulsarSerializationSchema.key(IN, PulsarSinkContext)
You need to implement this interface and extract the message key when you want to send the message with the same key to the same topic partition.

`PulsarSerializationSchema.key(IN, PulsarSinkContext)`

If you do not provide the message key. A topic  partition is randomly chosen from the topic list.


The message key can be hashed in two ways: MessageKeyHash.JAVA_HASH and MessageKeyHash.MURMUR3_32_HASH.
You can use the PulsarSinkOptions.PULSAR_MESSAGE_KEY_HASH option to choose the hash method.

`MessageKeyHash.JAVA_HASH`
`MessageKeyHash.MURMUR3_32_HASH`
`PulsarSinkOptions.PULSAR_MESSAGE_KEY_HASH`

RoundRobinRouter: Round-robin among all the partitions.

`RoundRobinRouter`

All messages are sent to the first partition, and switch to the next partition after sending
a fixed number of messages. The batch size can be customized by the PulsarSinkOptions.PULSAR_BATCHING_MAX_MESSAGES option.

`PulsarSinkOptions.PULSAR_BATCHING_MAX_MESSAGES`

Letâs assume there are ten messages and two topics. Topic A has two partitions while topic B has three partitions.
The batch size is set to five messages. In this case, topic A has 5 messages per partition which topic B does not receive any messages.


You can configure custom routers by using the TopicRouter interface.
If you implement a TopicRouter, ensure that it is serializable.
And you can return partitions which are not available in the pre-discovered partition list.

`TopicRouter`
`TopicRouter`

Thus, you do not need to specify topics using the PulsarSinkBuilder.setTopics option when you implement the custom topic router.

`PulsarSinkBuilder.setTopics`

```
@PublicEvolving
public interface TopicRouter<IN> extends Serializable {

    TopicPartition route(IN in, List<TopicPartition> partitions, PulsarSinkContext context);

    default void open(SinkConfiguration sinkConfiguration) {
        // Nothing to do by default.
    }
}

```

`@PublicEvolving
public interface TopicRouter<IN> extends Serializable {

    TopicPartition route(IN in, List<TopicPartition> partitions, PulsarSinkContext context);

    default void open(SinkConfiguration sinkConfiguration) {
        // Nothing to do by default.
    }
}
`

> 
Internally, a Pulsar partition is implemented as a topic. The Pulsar client provides APIs to hide this
implementation detail and handles routing under the hood automatically. Pulsar Sink uses a lower client
API to implement its own routing layer to support multiple topics routing.
For details, see partitioned topics.



Internally, a Pulsar partition is implemented as a topic. The Pulsar client provides APIs to hide this
implementation detail and handles routing under the hood automatically. Pulsar Sink uses a lower client
API to implement its own routing layer to support multiple topics routing.


For details, see partitioned topics.


### Delivery Guarantee#


PulsarSink supports three delivery guarantee semantics.

`PulsarSink`
* NONE: Data loss can happen even when the pipeline is running.
Basically, we use a fire-and-forget strategy to send records to Pulsar topics in this mode.
It means that this mode has the highest throughput.
* AT_LEAST_ONCE: No data loss happens, but data duplication can happen after a restart from checkpoint.
* EXACTLY_ONCE: No data loss happens. Each record is sent to the Pulsar broker only once.
Pulsar Sink uses Pulsar transaction
and two-phase commit (2PC) to ensure records are sent only once even after the pipeline restarts.
`NONE`
`AT_LEAST_ONCE`
`EXACTLY_ONCE`

> 
If you want to use EXACTLY_ONCE, make sure you have enabled the checkpoint on Flink and enabled the transaction on Pulsar.
The Pulsar sink will write all the messages in a pending transaction and commit it after the successfully checkpointing.
The messages written to Pulsar after a pending transaction won’t be obtained based on the design of the Pulsar.
You can acquire these messages only when the corresponding transaction is committed.



If you want to use EXACTLY_ONCE, make sure you have enabled the checkpoint on Flink and enabled the transaction on Pulsar.
The Pulsar sink will write all the messages in a pending transaction and commit it after the successfully checkpointing.

`EXACTLY_ONCE`

The messages written to Pulsar after a pending transaction won’t be obtained based on the design of the Pulsar.
You can acquire these messages only when the corresponding transaction is committed.


### Delayed message delivery#


Delayed message delivery
enables you to delay the possibility to consume a message. With delayed message enabled, the Pulsar sink sends a message to the Pulsar topic
immediately, but the message is delivered to a consumer once the specified delay is over.


Delayed message delivery only works in the Shared subscription type. In Exclusive and Failover
subscription types, the delayed message is dispatched immediately.

`Shared`
`Exclusive`
`Failover`

You can configure the MessageDelayer to define when to send the message to the consumer.
The default option is to never delay the message dispatching. You can use the MessageDelayer.fixed(Duration) option to
Configure delaying all messages in a fixed duration. You can also implement the MessageDelayer
interface to dispatch messages at different time.

`MessageDelayer`
`MessageDelayer.fixed(Duration)`
`MessageDelayer`

> 
  The dispatch time should be calculated by the PulsarSinkContext.processTime().


`PulsarSinkContext.processTime()`

### Sink Configurable Options#


You can set options for PulsarClient, PulsarAdmin, Pulsar Producer and PulsarSink
by using setConfig(ConfigOption<T>, T), setConfig(Configuration) and setConfig(Properties).

`PulsarClient`
`PulsarAdmin`
`Producer`
`PulsarSink`
`setConfig(ConfigOption<T>, T)`
`setConfig(Configuration)`
`setConfig(Properties)`

#### PulsarClient and PulsarAdmin Options#


For details, refer to PulsarAdmin options.


#### Pulsar Producer Options#


The Pulsar connector uses the Producer API to send messages. It extracts most parts of
Pulsar’s ProducerConfigurationData as Flink configuration options in PulsarSinkOptions.

`ProducerConfigurationData`
`PulsarSinkOptions`

##### pulsar.producer.batchingEnabled


##### pulsar.producer.batchingMaxBytes


##### pulsar.producer.batchingMaxMessages


##### pulsar.producer.batchingMaxPublishDelayMicros


##### pulsar.producer.batchingPartitionSwitchFrequencyByPublishDelay


##### pulsar.producer.chunkMaxMessageSize


##### pulsar.producer.chunkingEnabled


##### pulsar.producer.compressionType


Enum

* LZ4
* ZLIB
* ZSTD
* SNAPPY
* "NONE"
* "LZ4"
* "ZLIB"
* "ZSTD"
* "SNAPPY"

##### pulsar.producer.initialSequenceId


##### pulsar.producer.producerCryptoFailureAction


Enum

* "FAIL"
* "SEND"

##### pulsar.producer.producerName


##### pulsar.producer.properties

`properties`

##### pulsar.producer.sendTimeoutMs

`sendTimeout`

#### PulsarSink Options#


The configuration options below are mainly used for customizing the performance and message
sending behavior. You can just leave them alone if you do not have any performance issues.


##### pulsar.sink.deliveryGuarantee


Enum

* "exactly-once": Records are only delivered exactly-once also under failover scenarios. To build a complete exactly-once pipeline is required that the source and sink support exactly-once and are properly configured.
* "at-least-once": Records are ensured to be delivered but it may happen that the same record is delivered multiple times. Usually, this guarantee is faster than the exactly-once delivery.
* "none": Records are delivered on a best effort basis. It is often the fastest way to process records but it may happen that records are lost or duplicated.

##### pulsar.sink.enableMetrics

`pulsar.client.statsIntervalSeconds`

##### pulsar.sink.enableSchemaEvolution

`PulsarSinkBuilder.setSerializationSchema(Schema)`
`Schema`

##### pulsar.sink.maxRecommitTimes


##### pulsar.sink.messageKeyHash


Enum

* "java-hash": This hash would use String.hashCode() to calculate the message key string's hash code.
* "murmur-3-32-hash": This hash would calculate message key's hash code by using Murmur3 algorithm.
`String.hashCode()`

##### pulsar.sink.topicMetadataRefreshInterval


##### pulsar.sink.transactionTimeoutMillis

`DeliveryGuarantee.EXACTLY_ONCE`

##### pulsar.sink.validateSinkMessageBytes


### Brief Design Rationale#


Pulsar sink follow the Sink API defined in
FLIP-191.


#### Stateless SinkWriter#


In EXACTLY_ONCE mode, the Pulsar sink does not store transaction information in a checkpoint.
That means that new transactions will be created after a restart.
Therefore, any message in previous pending transactions is either aborted or timed out
(They are never visible to the downstream Pulsar consumer).
The Pulsar team is working to optimize the needed resources by unfinished pending transactions.

`EXACTLY_ONCE`

#### Pulsar Schema Evolution#


Pulsar Schema Evolution allows
you to reuse the same Flink job after certain “allowed” data model changes, like adding or deleting
a field in a AVRO-based Pojo class. Please note that you can specify Pulsar schema validation rules
and define an auto schema update. For details, refer to Pulsar Schema Evolution.


## Monitor the Metrics#


The Pulsar client refreshes its stats every 60 seconds by default. To increase the metrics refresh frequency,
you can change the Pulsar client stats refresh interval to a smaller value (minimum 1 second), as shown below.


```
builder.setConfig(PulsarOptions.PULSAR_STATS_INTERVAL_SECONDS, 1L);

```

`builder.setConfig(PulsarOptions.PULSAR_STATS_INTERVAL_SECONDS, 1L);
`

```
builder.set_config("pulsar.client.statsIntervalSeconds", "1")

```

`builder.set_config("pulsar.client.statsIntervalSeconds", "1")
`

### Source Metrics#


Flink defines common source metrics in FLIP-33: Standardize Connector Metrics. Pulsar connector will
expose some client metrics if you enable the pulsar.source.enableMetrics option. All the custom source metrics are
listed in below table.

`pulsar.source.enableMetrics`

```
builder.setConfig(PulsarSourceOptions.PULSAR_ENABLE_SOURCE_METRICS, true);

```

`builder.setConfig(PulsarSourceOptions.PULSAR_ENABLE_SOURCE_METRICS, true);
`

```
builder.set_config("pulsar.source.enableMetrics", "true")

```

`builder.set_config("pulsar.source.enableMetrics", "true")
`

### Sink Metrics#


The below table lists supported sink metrics. The first 6 metrics are standard Pulsar Sink metrics as described in
FLIP-33: Standardize Connector Metrics.


The first 5 metrics are exposed to the flink metric system by default.
You should enable the pulsar.sink.enableMetrics option to get the remaining metrics exposed.

`pulsar.sink.enableMetrics`

```
builder.setConfig(PulsarSinkOptions.PULSAR_ENABLE_SINK_METRICS, true);

```

`builder.setConfig(PulsarSinkOptions.PULSAR_ENABLE_SINK_METRICS, true);
`

```
builder.set_config("pulsar.sink.enableMetrics", "true")

```

`builder.set_config("pulsar.sink.enableMetrics", "true")
`

> 


numBytesOut, numRecordsOut and numRecordsOutErrors are retrieved from Pulsar client metrics.


numBytesOutPerSecond and numRecordsOutPerSecond are calculated based on the numBytesOut and numRecordsOUt
counter respectively. Flink internally uses a fixed 60-seconds window to calculate the rates.


currentSendTime tracks the time from when the producer calls sendAync() to
the time when the broker acknowledges the message. This metric is not available in NONE delivery guarantee.




* 
numBytesOut, numRecordsOut and numRecordsOutErrors are retrieved from Pulsar client metrics.

* 
numBytesOutPerSecond and numRecordsOutPerSecond are calculated based on the numBytesOut and numRecordsOUt
counter respectively. Flink internally uses a fixed 60-seconds window to calculate the rates.

* 
currentSendTime tracks the time from when the producer calls sendAync() to
the time when the broker acknowledges the message. This metric is not available in NONE delivery guarantee.


numBytesOut, numRecordsOut and numRecordsOutErrors are retrieved from Pulsar client metrics.

`numBytesOut`
`numRecordsOut`
`numRecordsOutErrors`

numBytesOutPerSecond and numRecordsOutPerSecond are calculated based on the numBytesOut and numRecordsOUt
counter respectively. Flink internally uses a fixed 60-seconds window to calculate the rates.

`numBytesOutPerSecond`
`numRecordsOutPerSecond`
`numBytesOut`
`numRecordsOUt`

currentSendTime tracks the time from when the producer calls sendAync() to
the time when the broker acknowledges the message. This metric is not available in NONE delivery guarantee.

`currentSendTime`
`sendAync()`
`NONE`

## End-to-end encryption#


Flink can use Pulsar’s encryption to encrypt messages on the sink side and decrypt messages on the source side.
Users should provide the public and private key pair to perform the encryption.
Only with a valid key pair can decrypt the encrypted messages.


### How to enable end-to-end encryption#

1. 
Generate a set of key pairs.
Pulsar supports multiple ECDSA or RSA key pairs in the meantime, you can provide
multiple key pairs. We will randomly choose a key pair to encrypt the message which makes the encryption more secure.
# ECDSA (for Java clients only)
openssl ecparam -name secp521r1 -genkey -param_enc explicit -out test_ecdsa_privkey.pem
openssl ec -in test_ecdsa_privkey.pem -pubout -outform pem -out test_ecdsa_pubkey.pem

# RSA
openssl genrsa -out test_rsa_privkey.pem 2048
openssl rsa -in test_rsa_privkey.pem -pubout -outform pkcs8 -out test_rsa_pubkey.pem

2. 
Implement the CryptoKeyReader interface.
Each key pair should have a unique key name. Implement the CryptoKeyReader interface and make sure
CryptoKeyReader.getPublicKey() and CryptoKeyReader.getPrivateKey() can return the corresponding key by the
key name.
Pulsar provided a default CryptoKeyReader implementation named DefaultCryptoKeyReader. You can create it by using
the DefaultCryptoKeyReader.builder(). And make sure the key pair files should be placed on the Flink running environment.
// defaultPublicKey and defaultPrivateKey should be provided in this implementation.
// The file:///path/to/default-public.key should be a valid path on Flink's running environment.
CryptoKeyReader keyReader = DefaultCryptoKeyReader.builder()
    .defaultPublicKey("file:///path/to/default-public.key")
    .defaultPrivateKey("file:///path/to/default-private.key")
    .publicKey("key1", "file:///path/to/public1.key").privateKey("key1", "file:///path/to/private1.key")
    .publicKey("key2", "file:///path/to/public2.key").privateKey("key2", "file:///path/to/private2.key")
    .build();

3. 
(Optional) Implement the MessageCrypto<MessageMetadata, MessageMetadata> interface.
Pulsar supports the ECDSA, RSA out of box. You don’t need to implement this interface if you use the common
existing encryption methods. If you want to define a custom key pair based crypto method, just implement the
MessageCrypto<MessageMetadata, MessageMetadata> interface. You can read the Pulsar’s default implementation, the
MessageCryptoBc, for how to implement this crypto interface.

4. 
Create PulsarCrypto instance.
PulsarCrypto is used for providing all the required information for encryption and decryption. You can use the builder
method to create the instance.
CryptoKeyReader keyReader = DefaultCryptoKeyReader.builder()
    .defaultPublicKey("file:///path/to/public1.key")
    .defaultPrivateKey("file:///path/to/private2.key")
    .publicKey("key1", "file:///path/to/public1.key").privateKey("key1", "file:///path/to/private1.key")
    .publicKey("key2", "file:///path/to/public2.key").privateKey("key2", "file:///path/to/private2.key")
    .build();

// This line is only used as an example. It returns the default implementation of the MessageCrypto.
SerializableSupplier<MessageCrypto<MessageMetadata, MessageMetadata>> cryptoSupplier = () -> new MessageCryptoBc();

PulsarCrypto pulsarCrypto = PulsarCrypto.builder()
    .cryptoKeyReader(keyReader)
    // All the key name should be provided here, you can't encrypt the message with any non-existed key names.
    .addEncryptKeys("key1", "key2")
    // You don't have to provide the MessageCrypto.
    .messageCrypto(cryptoSupplier)
    .build()


Generate a set of key pairs.


Pulsar supports multiple ECDSA or RSA key pairs in the meantime, you can provide
multiple key pairs. We will randomly choose a key pair to encrypt the message which makes the encryption more secure.


```
# ECDSA (for Java clients only)
openssl ecparam -name secp521r1 -genkey -param_enc explicit -out test_ecdsa_privkey.pem
openssl ec -in test_ecdsa_privkey.pem -pubout -outform pem -out test_ecdsa_pubkey.pem

# RSA
openssl genrsa -out test_rsa_privkey.pem 2048
openssl rsa -in test_rsa_privkey.pem -pubout -outform pkcs8 -out test_rsa_pubkey.pem

```

`# ECDSA (for Java clients only)
openssl ecparam -name secp521r1 -genkey -param_enc explicit -out test_ecdsa_privkey.pem
openssl ec -in test_ecdsa_privkey.pem -pubout -outform pem -out test_ecdsa_pubkey.pem

# RSA
openssl genrsa -out test_rsa_privkey.pem 2048
openssl rsa -in test_rsa_privkey.pem -pubout -outform pkcs8 -out test_rsa_pubkey.pem
`

Implement the CryptoKeyReader interface.

`CryptoKeyReader`

Each key pair should have a unique key name. Implement the CryptoKeyReader interface and make sure
CryptoKeyReader.getPublicKey() and CryptoKeyReader.getPrivateKey() can return the corresponding key by the
key name.

`CryptoKeyReader`
`CryptoKeyReader.getPublicKey()`
`CryptoKeyReader.getPrivateKey()`

Pulsar provided a default CryptoKeyReader implementation named DefaultCryptoKeyReader. You can create it by using
the DefaultCryptoKeyReader.builder(). And make sure the key pair files should be placed on the Flink running environment.

`CryptoKeyReader`
`DefaultCryptoKeyReader`
`DefaultCryptoKeyReader.builder()`

```
// defaultPublicKey and defaultPrivateKey should be provided in this implementation.
// The file:///path/to/default-public.key should be a valid path on Flink's running environment.
CryptoKeyReader keyReader = DefaultCryptoKeyReader.builder()
    .defaultPublicKey("file:///path/to/default-public.key")
    .defaultPrivateKey("file:///path/to/default-private.key")
    .publicKey("key1", "file:///path/to/public1.key").privateKey("key1", "file:///path/to/private1.key")
    .publicKey("key2", "file:///path/to/public2.key").privateKey("key2", "file:///path/to/private2.key")
    .build();

```

`// defaultPublicKey and defaultPrivateKey should be provided in this implementation.
// The file:///path/to/default-public.key should be a valid path on Flink's running environment.
CryptoKeyReader keyReader = DefaultCryptoKeyReader.builder()
    .defaultPublicKey("file:///path/to/default-public.key")
    .defaultPrivateKey("file:///path/to/default-private.key")
    .publicKey("key1", "file:///path/to/public1.key").privateKey("key1", "file:///path/to/private1.key")
    .publicKey("key2", "file:///path/to/public2.key").privateKey("key2", "file:///path/to/private2.key")
    .build();
`

(Optional) Implement the MessageCrypto<MessageMetadata, MessageMetadata> interface.

`MessageCrypto<MessageMetadata, MessageMetadata>`

Pulsar supports the ECDSA, RSA out of box. You don’t need to implement this interface if you use the common
existing encryption methods. If you want to define a custom key pair based crypto method, just implement the
MessageCrypto<MessageMetadata, MessageMetadata> interface. You can read the Pulsar’s default implementation, the
MessageCryptoBc, for how to implement this crypto interface.

`MessageCrypto<MessageMetadata, MessageMetadata>`
`MessageCryptoBc`

Create PulsarCrypto instance.

`PulsarCrypto`

PulsarCrypto is used for providing all the required information for encryption and decryption. You can use the builder
method to create the instance.

`PulsarCrypto`

```
CryptoKeyReader keyReader = DefaultCryptoKeyReader.builder()
    .defaultPublicKey("file:///path/to/public1.key")
    .defaultPrivateKey("file:///path/to/private2.key")
    .publicKey("key1", "file:///path/to/public1.key").privateKey("key1", "file:///path/to/private1.key")
    .publicKey("key2", "file:///path/to/public2.key").privateKey("key2", "file:///path/to/private2.key")
    .build();

// This line is only used as an example. It returns the default implementation of the MessageCrypto.
SerializableSupplier<MessageCrypto<MessageMetadata, MessageMetadata>> cryptoSupplier = () -> new MessageCryptoBc();

PulsarCrypto pulsarCrypto = PulsarCrypto.builder()
    .cryptoKeyReader(keyReader)
    // All the key name should be provided here, you can't encrypt the message with any non-existed key names.
    .addEncryptKeys("key1", "key2")
    // You don't have to provide the MessageCrypto.
    .messageCrypto(cryptoSupplier)
    .build()

```

`CryptoKeyReader keyReader = DefaultCryptoKeyReader.builder()
    .defaultPublicKey("file:///path/to/public1.key")
    .defaultPrivateKey("file:///path/to/private2.key")
    .publicKey("key1", "file:///path/to/public1.key").privateKey("key1", "file:///path/to/private1.key")
    .publicKey("key2", "file:///path/to/public2.key").privateKey("key2", "file:///path/to/private2.key")
    .build();

// This line is only used as an example. It returns the default implementation of the MessageCrypto.
SerializableSupplier<MessageCrypto<MessageMetadata, MessageMetadata>> cryptoSupplier = () -> new MessageCryptoBc();

PulsarCrypto pulsarCrypto = PulsarCrypto.builder()
    .cryptoKeyReader(keyReader)
    // All the key name should be provided here, you can't encrypt the message with any non-existed key names.
    .addEncryptKeys("key1", "key2")
    // You don't have to provide the MessageCrypto.
    .messageCrypto(cryptoSupplier)
    .build()
`

### Decrypt the message on the Pulsar source#


Follow the previous instruction to create a PulsarCrypto instance and pass it to the PulsarSource.builder().
You need to choose the decrypt failure action in the meantime. Pulsar has three types of failure action which defines in
ConsumerCryptoFailureAction.

`PulsarCrypto`
`PulsarSource.builder()`
`ConsumerCryptoFailureAction`
* 
ConsumerCryptoFailureAction.FAIL: The Flink pipeline will crash and turn into a failed state.

* 
ConsumerCryptoFailureAction.DISCARD: Message is silently drop and not delivered to the downstream.

* 
ConsumerCryptoFailureAction.CONSUME
The message will not be decrypted and directly passed to downstream. You can decrypt the message in
PulsarDeserializationSchema, the encryption information can be retrieved from Message.getEncryptionCtx().


ConsumerCryptoFailureAction.FAIL: The Flink pipeline will crash and turn into a failed state.

`ConsumerCryptoFailureAction.FAIL`

ConsumerCryptoFailureAction.DISCARD: Message is silently drop and not delivered to the downstream.

`ConsumerCryptoFailureAction.DISCARD`

ConsumerCryptoFailureAction.CONSUME

`ConsumerCryptoFailureAction.CONSUME`

The message will not be decrypted and directly passed to downstream. You can decrypt the message in
PulsarDeserializationSchema, the encryption information can be retrieved from Message.getEncryptionCtx().

`PulsarDeserializationSchema`
`Message.getEncryptionCtx()`

```
PulsarCrypto pulsarCrypto = ...

PulsarSource<String> sink = PulsarSource.builder()
    ...
    .setPulsarCrypto(pulsarCrypto, ConsumerCryptoFailureAction.FAIL)
    .build();

```

`PulsarCrypto pulsarCrypto = ...

PulsarSource<String> sink = PulsarSource.builder()
    ...
    .setPulsarCrypto(pulsarCrypto, ConsumerCryptoFailureAction.FAIL)
    .build();
`

### Encrypt the message on the Pulsar sink#


Follow the previous instruction to create a PulsarCrypto instance and pass it to the PulsarSink.builder().
You need to choose the encrypt failure action in the meantime. Pulsar has two types of failure action which defines in
ProducerCryptoFailureAction.

`PulsarCrypto`
`PulsarSink.builder()`
`ProducerCryptoFailureAction`
* ProducerCryptoFailureAction.FAIL: The Flink pipeline will crash and turn into a failed state.
* ProducerCryptoFailureAction.SEND: Send the unencrypted messages.
`ProducerCryptoFailureAction.FAIL`
`ProducerCryptoFailureAction.SEND`

```
PulsarCrypto pulsarCrypto = ...

PulsarSink<String> sink = PulsarSink.builder()
    ...
    .setPulsarCrypto(pulsarCrypto, ProducerCryptoFailureAction.FAIL)
    .build();

```

`PulsarCrypto pulsarCrypto = ...

PulsarSink<String> sink = PulsarSink.builder()
    ...
    .setPulsarCrypto(pulsarCrypto, ProducerCryptoFailureAction.FAIL)
    .build();
`

## Upgrading to the Latest Connector Version#


The generic upgrade steps are outlined in upgrading jobs and Flink versions guide.
The Pulsar connector does not store any state on the Flink side. The Pulsar connector pushes and stores all the states on the Pulsar side.
For Pulsar, you additionally need to know these limitations:

* Do not upgrade the Pulsar connector and Pulsar broker version at the same time.
* Always use a newer Pulsar client with Pulsar connector to consume messages from Pulsar.

## Troubleshooting#


If you have a problem with Pulsar when using Flink, keep in mind that Flink only wraps
PulsarClient or
PulsarAdmin
and your problem might be independent of Flink and sometimes can be solved by upgrading Pulsar brokers,
reconfiguring Pulsar brokers or reconfiguring Pulsar connector in Flink.


## Known Issues#


This section describes some known issues about the Pulsar connectors.


### Unstable on Java 11#


Pulsar connector has some known issues on Java 11. It is recommended to run Pulsar connector
on Java 8.


### No TransactionCoordinatorNotFound, but automatic reconnect#


Pulsar transactions are still in active development and are not stable. Pulsar 2.9.2
introduces a break change in transactions.
If you use Pulsar 2.9.2 or higher with an older Pulsar client, you might get a TransactionCoordinatorNotFound exception.

`TransactionCoordinatorNotFound`

You can use the latest pulsar-client-all release to resolve this issue.

`pulsar-client-all`

 Back to top
