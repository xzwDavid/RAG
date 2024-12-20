# Experimental Features


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Experimental Features#


This section describes experimental features in the DataStream API. Experimental features are still evolving and can be either unstable,
incomplete, or subject to heavy change in future versions.


## Reinterpreting a pre-partitioned data stream as keyed stream#


We can re-interpret a pre-partitioned data stream as a keyed stream to avoid shuffling.


> 
WARNING: The re-interpreted data stream MUST already be pre-partitioned in EXACTLY the same way Flink’s keyBy would partition
the data in a shuffle w.r.t. key-group assignment.



One use-case for this could be a materialized shuffle between two jobs: the first job performs a keyBy shuffle and materializes
each output into a partition. A second job has sources that, for each parallel instance, reads from the corresponding partitions
created by the first job. Those sources can now be re-interpreted as keyed streams, e.g. to apply windowing. Notice that this trick
makes the second job embarrassingly parallel, which can be helpful for a fine-grained recovery scheme.


This re-interpretation functionality is exposed through DataStreamUtils:

`DataStreamUtils`

```
static <T, K> KeyedStream<T, K> reinterpretAsKeyedStream(
    DataStream<T> stream,
    KeySelector<T, K> keySelector,
    TypeInformation<K> typeInfo)

```

`static <T, K> KeyedStream<T, K> reinterpretAsKeyedStream(
    DataStream<T> stream,
    KeySelector<T, K> keySelector,
    TypeInformation<K> typeInfo)
`

Given a base stream, a key selector, and type information,
the method creates a keyed stream from the base stream.


Code example:


```
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
DataStreamSource<Integer> source = ...;
DataStreamUtils.reinterpretAsKeyedStream(source, (in) -> in, TypeInformation.of(Integer.class))
    .window(TumblingEventTimeWindows.of(Duration.ofSeconds(1)))
    .reduce((a, b) -> a + b)
    .addSink(new DiscardingSink<>());
env.execute();

```

`StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
DataStreamSource<Integer> source = ...;
DataStreamUtils.reinterpretAsKeyedStream(source, (in) -> in, TypeInformation.of(Integer.class))
    .window(TumblingEventTimeWindows.of(Duration.ofSeconds(1)))
    .reduce((a, b) -> a + b)
    .addSink(new DiscardingSink<>());
env.execute();
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment
env.setParallelism(1)
val source = ...
new DataStreamUtils(source).reinterpretAsKeyedStream((in) => in)
  .window(TumblingEventTimeWindows.of(Duration.ofSeconds(1)))
  .reduce((a, b) => a + b)
  .addSink(new DiscardingSink[Int])
env.execute()

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment
env.setParallelism(1)
val source = ...
new DataStreamUtils(source).reinterpretAsKeyedStream((in) => in)
  .window(TumblingEventTimeWindows.of(Duration.ofSeconds(1)))
  .reduce((a, b) => a + b)
  .addSink(new DiscardingSink[Int])
env.execute()
`

 Back to top
