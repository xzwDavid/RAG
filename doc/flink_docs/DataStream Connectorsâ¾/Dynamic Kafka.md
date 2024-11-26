# Dynamic Kafka


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Dynamic Kafka SourceExperimental#

`Experimental`

Flink provides an Apache Kafka connector for reading data from Kafka topics from one or more Kafka clusters.
The Dynamic Kafka connector discovers the clusters and topics using a Kafka metadata service and can achieve reading in a dynamic fashion, facilitating changes in
topics and/or clusters, without requiring a job restart. This is especially useful when you need to read a new Kafka cluster/topic and/or stop reading
an existing Kafka cluster/topic (cluster migration/failover/other infrastructure changes) and when you need direct integration with Hybrid Source. The solution
makes these operations automated so that they are transparent to Kafka consumers.


## Dependency#


For details on Kafka compatibility, please refer to the official Kafka documentation.


Only available for stable versions.


Flink’s streaming connectors are not part of the binary distribution.
See how to link with them for cluster execution here.


## Dynamic Kafka Source#


> 
  This part describes the Dynamic Kafka Source based on the new
data source API.



### Usage#


Dynamic Kafka Source provides a builder class to initialize the DynamicKafkaSource. The code snippet
below shows how to build a DynamicKafkaSource to consume messages from the earliest offset of the
stream “input-stream” and deserialize only the value of the
ConsumerRecord as a string, using “MyKafkaMetadataService” to resolve the cluster(s) and topic(s)
corresponding to “input-stream”.




Java

DynamicKafkaSource<String> source = DynamicKafkaSource.<String>builder()
    .setKafkaMetadataService(new MyKafkaMetadataService())
    .setStreamIds(Collections.singleton("input-stream"))
    .setStartingOffsets(OffsetsInitializer.earliest())
    .setDeserializer(KafkaRecordDeserializationSchema.valueOnly(StringDeserializer.class))
    .setProperties(properties)
    .build();

env.fromSource(source, WatermarkStrategy.noWatermarks(), "Dynamic Kafka Source");


The following properties are required for building a DynamicKafkaSource:


```

DynamicKafkaSource<String> source = DynamicKafkaSource.<String>builder()
    .setKafkaMetadataService(new MyKafkaMetadataService())
    .setStreamIds(Collections.singleton("input-stream"))
    .setStartingOffsets(OffsetsInitializer.earliest())
    .setDeserializer(KafkaRecordDeserializationSchema.valueOnly(StringDeserializer.class))
    .setProperties(properties)
    .build();

env.fromSource(source, WatermarkStrategy.noWatermarks(), "Dynamic Kafka Source");

```

`
DynamicKafkaSource<String> source = DynamicKafkaSource.<String>builder()
    .setKafkaMetadataService(new MyKafkaMetadataService())
    .setStreamIds(Collections.singleton("input-stream"))
    .setStartingOffsets(OffsetsInitializer.earliest())
    .setDeserializer(KafkaRecordDeserializationSchema.valueOnly(StringDeserializer.class))
    .setProperties(properties)
    .build();

env.fromSource(source, WatermarkStrategy.noWatermarks(), "Dynamic Kafka Source");
`

The Kafka metadata service, configured by setKafkaMetadataService(KafkaMetadataService)
The stream ids to subscribe, see the following Kafka stream subscription section for more details.
Deserializer to parse Kafka messages, see the Kafka Source Documentation for more details.


### Kafka Stream Subscription#


The Dynamic Kafka Source provides 2 ways of subscribing to Kafka stream(s).

* A set of Kafka stream ids. For example:






Java
DynamicKafkaSource.builder().setStreamIds(Set.of("stream-a", "stream-b"));


* A regex pattern that subscribes to all Kafka stream ids that match the provided regex. For example:






Java
DynamicKafkaSource.builder().setStreamPattern(Pattern.of("stream.*"));



```
DynamicKafkaSource.builder().setStreamIds(Set.of("stream-a", "stream-b"));

```

`DynamicKafkaSource.builder().setStreamIds(Set.of("stream-a", "stream-b"));
`

```
DynamicKafkaSource.builder().setStreamPattern(Pattern.of("stream.*"));

```

`DynamicKafkaSource.builder().setStreamPattern(Pattern.of("stream.*"));
`

### Kafka Metadata Service#


An interface is provided to resolve the logical Kafka stream(s) into the corresponding physical
topic(s) and cluster(s). Typically, these implementations are based on services that align well
with internal Kafka infrastructure–if that is not available, an in-memory implementation
would also work. An example of in-memory implementation can be found in our tests.


This source achieves its dynamic characteristic by periodically polling this Kafka metadata service
for any changes to the Kafka stream(s) and reconciling the reader tasks to subscribe to the new
Kafka metadata returned by the service. For example, in the case of a Kafka migration, the source would
swap from one cluster to the new cluster when the service makes that change in the Kafka stream metadata.


### Additional Properties#


There are configuration options in DynamicKafkaSourceOptions that can be configured in the properties through the builder:


##### stream-metadata-discovery-interval-ms


##### stream-metadata-discovery-failure-threshold


In addition to this list, see the regular Kafka connector for
a list of applicable properties.


### Metrics#

`currentEmitEventTimeLag = EmitTime - EventTime.`
`watermarkLag = CurrentTime - Watermark`
`sourceIdleTime = CurrentTime - LastRecordProcessTime`

In addition to this list, see the regular Kafka connector for
the KafkaSourceReader metrics that are also reported.


### Additional Details#


For additional details on deserialization, event time and watermarks, idleness, consumer offset
committing, security, and more, you can refer to the Kafka Source documentation. This is possible because the
Dynamic Kafka Source leverages components of the Kafka Source, and the implementation will be
discussed in the next section.


### Behind the Scene#


> 
  If you are interested in how Kafka source works under the design of new data source API, you may
want to read this part as a reference. For details about the new data source API,
documentation of data source and
FLIP-27
provide more descriptive discussions.



Under the abstraction of the new data source API, Dynamic Kafka Source consists of the following components:


#### Source Split#


A source split in Dynamic Kafka Source represents a partition of a Kafka topic, with cluster information. It
consists of:

* A Kafka cluster id that can be resolved by the Kafka metadata service.
* A Kafka Source Split (TopicPartition, starting offset, stopping offset).

You can check the class DynamicKafkaSourceSplit for more details.

`DynamicKafkaSourceSplit`

#### Split Enumerator#


This enumerator is responsible for discovering and assigning splits from one or more clusters. At startup, the
enumerator will discover metadata belonging to the Kafka stream ids. Using the metadata, it can
initialize KafkaSourceEnumerators to handle the functions of assigning splits to the readers. In addition,
source events will be sent to the source reader to reconcile the metadata. This enumerator has the ability to poll the
KafkaMetadataService, periodically for stream discovery. In addition, restarting enumerators when metadata changes involve
clearing outdated metrics since clusters may be removed and so should their metrics.


#### Source Reader#


This reader is responsible for reading from one or more clusters and using the KafkaSourceReader to fetch
records from topics and clusters based on the metadata. When new metadata is discovered by the enumerator,
the reader will reconcile metadata changes to possibly restart the KafkaSourceReader to read from the new
set of topics and clusters.


#### Kafka Metadata Service#


This interface represents the source of truth for the current metadata for the configured Kafka stream ids.
Metadata that is removed in between polls is considered non-active (e.g. removing a cluster from the
return value, means that a cluster is non-active and should not be read from). The cluster metadata
contains an immutable Kafka cluster id, the set of topics, and properties needed to connect to the
Kafka cluster.


#### FLIP 246#


To understand more behind the scenes, please read FLIP-246
for more details and discussion.


 Back to top
