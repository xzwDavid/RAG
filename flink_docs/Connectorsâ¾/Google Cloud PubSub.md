# Google Cloud PubSub


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Google Cloud PubSub#


This connector provides a Source and Sink that can read from and write to
Google Cloud PubSub. To use this connector, add the
following dependency to your project:


Only available for stable versions.


> 
Note: This connector has been added to Flink recently. It has not received widespread testing yet.



Note that the streaming connectors are currently not part of the binary
distribution. See
here
for information about how to package the program with the libraries for
cluster execution.


## Consuming or Producing PubSubMessages#


The connector provides a connectors for receiving and sending messages from and to Google PubSub.
Google PubSub has an at-least-once guarantee and as such the connector delivers the same guarantees.

`at-least-once`

### PubSub SourceFunction#


The class PubSubSource has a builder to create PubSubsources: PubSubSource.newBuilder(...)

`PubSubSource`
`PubSubSource.newBuilder(...)`

There are several optional methods to alter how the PubSubSource is created, the bare minimum is to provide a Google project, Pubsub subscription and a way to deserialize the PubSubMessages.


Example:


```
StreamExecutionEnvironment streamExecEnv = StreamExecutionEnvironment.getExecutionEnvironment();

DeserializationSchema<SomeObject> deserializer = (...);
SourceFunction<SomeObject> pubsubSource = PubSubSource.newBuilder()
                                                      .withDeserializationSchema(deserializer)
                                                      .withProjectName("project")
                                                      .withSubscriptionName("subscription")
                                                      .build();

streamExecEnv.addSource(pubsubSource);

```

`StreamExecutionEnvironment streamExecEnv = StreamExecutionEnvironment.getExecutionEnvironment();

DeserializationSchema<SomeObject> deserializer = (...);
SourceFunction<SomeObject> pubsubSource = PubSubSource.newBuilder()
                                                      .withDeserializationSchema(deserializer)
                                                      .withProjectName("project")
                                                      .withSubscriptionName("subscription")
                                                      .build();

streamExecEnv.addSource(pubsubSource);
`

Currently the source functions pulls messages from PubSub, push endpoints are not supported.


### PubSub Sink#


The class PubSubSink has a builder to create PubSubSinks. PubSubSink.newBuilder(...)

`PubSubSink`
`PubSubSink.newBuilder(...)`

This builder works in a similar way to the PubSubSource.


Example:


```
DataStream<SomeObject> dataStream = (...);

SerializationSchema<SomeObject> serializationSchema = (...);
SinkFunction<SomeObject> pubsubSink = PubSubSink.newBuilder()
                                                .withSerializationSchema(serializationSchema)
                                                .withProjectName("project")
                                                .withSubscriptionName("subscription")
                                                .build()

dataStream.addSink(pubsubSink);

```

`DataStream<SomeObject> dataStream = (...);

SerializationSchema<SomeObject> serializationSchema = (...);
SinkFunction<SomeObject> pubsubSink = PubSubSink.newBuilder()
                                                .withSerializationSchema(serializationSchema)
                                                .withProjectName("project")
                                                .withSubscriptionName("subscription")
                                                .build()

dataStream.addSink(pubsubSink);
`

### Google Credentials#


Google uses Credentials to authenticate and authorize applications so that they can use Google Cloud Platform resources (such as PubSub).


Both builders allow you to provide these credentials but by default the connectors will look for an environment variable: GOOGLE_APPLICATION_CREDENTIALS which should point to a file containing the credentials.


If you want to provide Credentials manually, for instance if you read the Credentials yourself from an external system, you can use PubSubSource.newBuilder(...).withCredentials(...).

`PubSubSource.newBuilder(...).withCredentials(...)`

### Integration testing#


When running integration tests you might not want to connect to PubSub directly but use a docker container to read and write to. (See: PubSub testing locally)


The following example shows how you would create a source to read messages from the emulator and send them back:


```
String hostAndPort = "localhost:1234";
DeserializationSchema<SomeObject> deserializationSchema = (...);
SourceFunction<SomeObject> pubsubSource = PubSubSource.newBuilder()
                                                      .withDeserializationSchema(deserializationSchema)
                                                      .withProjectName("my-fake-project")
                                                      .withSubscriptionName("subscription")
                                                      .withPubSubSubscriberFactory(new PubSubSubscriberFactoryForEmulator(hostAndPort, "my-fake-project", "subscription", 10, Duration.ofSeconds(15), 100))
                                                      .build();
SerializationSchema<SomeObject> serializationSchema = (...);
SinkFunction<SomeObject> pubsubSink = PubSubSink.newBuilder()
                                                .withSerializationSchema(serializationSchema)
                                                .withProjectName("my-fake-project")
                                                .withSubscriptionName("subscription")
                                                .withHostAndPortForEmulator(hostAndPort)
                                                .build();

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.addSource(pubsubSource)
   .addSink(pubsubSink);

```

`String hostAndPort = "localhost:1234";
DeserializationSchema<SomeObject> deserializationSchema = (...);
SourceFunction<SomeObject> pubsubSource = PubSubSource.newBuilder()
                                                      .withDeserializationSchema(deserializationSchema)
                                                      .withProjectName("my-fake-project")
                                                      .withSubscriptionName("subscription")
                                                      .withPubSubSubscriberFactory(new PubSubSubscriberFactoryForEmulator(hostAndPort, "my-fake-project", "subscription", 10, Duration.ofSeconds(15), 100))
                                                      .build();
SerializationSchema<SomeObject> serializationSchema = (...);
SinkFunction<SomeObject> pubsubSink = PubSubSink.newBuilder()
                                                .withSerializationSchema(serializationSchema)
                                                .withProjectName("my-fake-project")
                                                .withSubscriptionName("subscription")
                                                .withHostAndPortForEmulator(hostAndPort)
                                                .build();

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.addSource(pubsubSource)
   .addSink(pubsubSink);
`

### At least once guarantee#


#### SourceFunction#


There are several reasons why a message might be send multiple times, such as failure scenarios on Google PubSub’s side.


Another reason is when the acknowledgement deadline has passed. This is the time between receiving the message and acknowledging the message. The PubSubSource will only acknowledge a message on successful checkpoints to guarantee at-least-once. This does mean if the time between successful checkpoints is larger than the acknowledgment deadline of your subscription messages will most likely be processed multiple times.


For this reason it’s recommended to have a (much) lower checkpoint interval than acknowledgement deadline.


See PubSub for details on how to increase the acknowledgment deadline of your subscription.


Note: The metric PubSubMessagesProcessedNotAcked shows how many messages are waiting for the next checkpoint before they will be acknowledged.

`PubSubMessagesProcessedNotAcked`

#### SinkFunction#


The sink function buffers messages that are to be send to PubSub for a short amount of time for performance reasons. Before each checkpoint this buffer is flushed and the checkpoint will not succeed unless the messages have been delivered to PubSub.


 Back to top
