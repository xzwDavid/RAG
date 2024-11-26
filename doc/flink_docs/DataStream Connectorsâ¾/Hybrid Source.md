# Hybrid Source


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Hybrid Source#


HybridSource is a source that contains a list of concrete sources.
It solves the problem of sequentially reading input from heterogeneous sources to produce a single input stream.

`HybridSource`

For example, a bootstrap use case may need to read several days worth of bounded input from S3 before continuing with the latest unbounded input from Kafka.
HybridSource switches from FileSource to KafkaSource when the bounded file input finishes without  interrupting the application.

`HybridSource`
`FileSource`
`KafkaSource`

Prior to HybridSource, it was necessary to create a topology with multiple sources and define a switching mechanism in user land, which leads to operational complexity and inefficiency.

`HybridSource`

With HybridSource the multiple sources appear as a single source in the Flink job graph and from DataStream API perspective.

`HybridSource`
`DataStream`

For more background see FLIP-150


To use the connector, add the flink-connector-base dependency to your project:

`flink-connector-base`

```
&ltdependency>
    &ltgroupId>org.apache.flink</groupId>
    &ltartifactId>flink-connector-base</artifactId>
    &ltversion>2.0-SNAPSHOT</version>
</dependency>
```

`&ltdependency>
    &ltgroupId>org.apache.flink</groupId>
    &ltartifactId>flink-connector-base</artifactId>
    &ltversion>2.0-SNAPSHOT</version>
</dependency>`

(Typically comes as transitive dependency with concrete sources.)


## Start position for next source#


To arrange multiple sources in a HybridSource, all sources except the last one need to be bounded. Therefore, the sources typically need to be assigned a start and end position. The last source may be bounded in which case the HybridSource is bounded and unbounded otherwise.
Details depend on the specific source and the external storage systems.

`HybridSource`
`HybridSource`

Here we cover the most basic and then a more complex scenario, following the File/Kafka example.


#### Fixed start position at graph construction time#


Example: Read till pre-determined switch time from files and then continue reading from Kafka.
Each source covers an upfront known range and therefore the contained sources can be created upfront as if they were used directly:


```
long switchTimestamp = ...; // derive from file input paths
FileSource<String> fileSource =
  FileSource.forRecordStreamFormat(new TextLineInputFormat(), Path.fromLocalFile(testDir)).build();
KafkaSource<String> kafkaSource =
          KafkaSource.<String>builder()
                  .setStartingOffsets(OffsetsInitializer.timestamp(switchTimestamp + 1))
                  .build();
HybridSource<String> hybridSource =
          HybridSource.builder(fileSource)
                  .addSource(kafkaSource)
                  .build();

```

`long switchTimestamp = ...; // derive from file input paths
FileSource<String> fileSource =
  FileSource.forRecordStreamFormat(new TextLineInputFormat(), Path.fromLocalFile(testDir)).build();
KafkaSource<String> kafkaSource =
          KafkaSource.<String>builder()
                  .setStartingOffsets(OffsetsInitializer.timestamp(switchTimestamp + 1))
                  .build();
HybridSource<String> hybridSource =
          HybridSource.builder(fileSource)
                  .addSource(kafkaSource)
                  .build();
`

```
switch_timestamp = ... # derive from file input paths
file_source = FileSource \
    .for_record_stream_format(StreamFormat.text_line_format(), test_dir) \
    .build()
kafka_source = KafkaSource \
    .builder() \
    .set_bootstrap_servers('localhost:9092') \
    .set_group_id('MY_GROUP') \
    .set_topics('quickstart-events') \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .set_starting_offsets(KafkaOffsetsInitializer.timestamp(switch_timestamp)) \
    .build()
hybrid_source = HybridSource.builder(file_source).add_source(kafka_source).build()

```

`switch_timestamp = ... # derive from file input paths
file_source = FileSource \
    .for_record_stream_format(StreamFormat.text_line_format(), test_dir) \
    .build()
kafka_source = KafkaSource \
    .builder() \
    .set_bootstrap_servers('localhost:9092') \
    .set_group_id('MY_GROUP') \
    .set_topics('quickstart-events') \
    .set_value_only_deserializer(SimpleStringSchema()) \
    .set_starting_offsets(KafkaOffsetsInitializer.timestamp(switch_timestamp)) \
    .build()
hybrid_source = HybridSource.builder(file_source).add_source(kafka_source).build()
`

#### Dynamic start position at switch time#


Example: File source reads a very large backlog, taking potentially longer than retention available for next source.
Switch needs to occur at “current time - X”. This requires the start time for the next source to be set at switch time.
Here we require transfer of end position from the previous file enumerator for deferred construction of KafkaSource
by implementing SourceFactory.

`KafkaSource`
`SourceFactory`

Note that enumerators need to support getting the end timestamp. This may currently require a source customization.
Adding support for dynamic end position to FileSource is tracked in FLINK-23633.

`FileSource`

```
FileSource<String> fileSource = CustomFileSource.readTillOneDayFromLatest();
HybridSource<String> hybridSource =
    HybridSource.<String, CustomFileSplitEnumerator>builder(fileSource)
        .addSource(
            switchContext -> {
              CustomFileSplitEnumerator previousEnumerator =
                  switchContext.getPreviousEnumerator();
              // how to get timestamp depends on specific enumerator
              long switchTimestamp = previousEnumerator.getEndTimestamp();
              KafkaSource<String> kafkaSource =
                  KafkaSource.<String>builder()
                      .setStartingOffsets(OffsetsInitializer.timestamp(switchTimestamp + 1))
                      .build();
              return kafkaSource;
            },
            Boundedness.CONTINUOUS_UNBOUNDED)
        .build();

```

`FileSource<String> fileSource = CustomFileSource.readTillOneDayFromLatest();
HybridSource<String> hybridSource =
    HybridSource.<String, CustomFileSplitEnumerator>builder(fileSource)
        .addSource(
            switchContext -> {
              CustomFileSplitEnumerator previousEnumerator =
                  switchContext.getPreviousEnumerator();
              // how to get timestamp depends on specific enumerator
              long switchTimestamp = previousEnumerator.getEndTimestamp();
              KafkaSource<String> kafkaSource =
                  KafkaSource.<String>builder()
                      .setStartingOffsets(OffsetsInitializer.timestamp(switchTimestamp + 1))
                      .build();
              return kafkaSource;
            },
            Boundedness.CONTINUOUS_UNBOUNDED)
        .build();
`