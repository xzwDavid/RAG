# Builtin Watermark Generators


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Builtin Watermark Generators#


As described in Generating Watermarks, Flink provides abstractions that
allow the programmer to assign their own timestamps and emit their own
watermarks. More specifically, one can do so by implementing the
WatermarkGenerator interface.

`WatermarkGenerator`

In order to further ease the programming effort for such tasks, Flink comes
with some pre-implemented timestamp assigners.  This section provides a list of
them. Apart from their out-of-the-box functionality, their implementation can
serve as an example for custom implementations.


## Monotonously Increasing Timestamps#


The simplest special case for periodic watermark generation is the when
timestamps seen by a given source task occur in ascending order. In that case,
the current timestamp can always act as a watermark, because no earlier
timestamps will arrive.


Note that it is only necessary that timestamps are ascending per parallel data
source task. For example, if in a specific setup one Kafka partition is read
by one parallel data source instance, then it is only necessary that timestamps
are ascending within each Kafka partition. Flink’s watermark merging mechanism
will generate correct watermarks whenever parallel streams are shuffled,
unioned, connected, or merged.


```
WatermarkStrategy.forMonotonousTimestamps();

```

`WatermarkStrategy.forMonotonousTimestamps();
`

```
WatermarkStrategy.forMonotonousTimestamps()

```

`WatermarkStrategy.forMonotonousTimestamps()
`

```
WatermarkStrategy.for_monotonous_timestamps()

```

`WatermarkStrategy.for_monotonous_timestamps()
`

## Fixed Amount of Lateness#


Another example of periodic watermark generation is when the watermark lags
behind the maximum (event-time) timestamp seen in the stream by a fixed amount
of time. This case covers scenarios where the maximum lateness that can be
encountered in a stream is known in advance, e.g. when creating a custom source
containing elements with timestamps spread within a fixed period of time for
testing. For these cases, Flink provides the BoundedOutOfOrdernessWatermarks
generator which takes as an argument the maxOutOfOrderness, i.e. the maximum
amount of time an element is allowed to be late before being ignored when
computing the final result for the given window. Lateness corresponds to the
result of t - t_w, where t is the (event-time) timestamp of an element, and
t_w that of the previous watermark.  If lateness > 0 then the element is
considered late and is, by default, ignored when computing the result of the
job for its corresponding window. See the documentation about allowed
lateness for more information
about working with late elements.

`BoundedOutOfOrdernessWatermarks`
`maxOutOfOrderness`
`t - t_w`
`t`
`t_w`
`lateness > 0`

```
WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(10));

```

`WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(10));
`

```
WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(10))

```

`WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(10))
`

```
WatermarkStrategy.for_bounded_out_of_orderness(Duration.of_seconds(10))

```

`WatermarkStrategy.for_bounded_out_of_orderness(Duration.of_seconds(10))
`

 Back to top
