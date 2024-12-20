# DataGen


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# DataGen Connector#


The DataGen connector provides a Source implementation that allows for generating input data for
Flink pipelines.
It is useful when developing locally or demoing without access to external systems such as Kafka.
The DataGen connector is built-in, no additional dependencies are required.

`Source`

## Usage#


The DataGeneratorSource produces N data points in parallel. The source splits the sequence
into as many parallel sub-sequences as there are parallel source subtasks. It drives the data
generation process by supplying “index” values of type Long to the user-provided


    GeneratorFunction

.

`DataGeneratorSource`
`Long`

The GeneratorFunction is then used for mapping the (sub-)sequences of Long values
into the generated events of an arbitrary data type. For instance, the following code will produce the sequence of
["Number: 0", "Number: 1", ... , "Number: 999"] records.

`GeneratorFunction`
`Long`
`["Number: 0", "Number: 1", ... , "Number: 999"]`

```
GeneratorFunction<Long, String> generatorFunction = index -> "Number: " + index;
long numberOfRecords = 1000;

DataGeneratorSource<String> source =
        new DataGeneratorSource<>(generatorFunction, numberOfRecords, Types.STRING);

DataStreamSource<String> stream =
        env.fromSource(source,
        WatermarkStrategy.noWatermarks(),
        "Generator Source");

```

`GeneratorFunction<Long, String> generatorFunction = index -> "Number: " + index;
long numberOfRecords = 1000;

DataGeneratorSource<String> source =
        new DataGeneratorSource<>(generatorFunction, numberOfRecords, Types.STRING);

DataStreamSource<String> stream =
        env.fromSource(source,
        WatermarkStrategy.noWatermarks(),
        "Generator Source");
`

The order of elements depends on the parallelism. Each sub-sequence will be produced in order.
Consequently, if the parallelism is limited to one, this will produce one sequence in order from
"Number: 0" to "Number: 999".

`"Number: 0"`
`"Number: 999"`

## Rate Limiting#


DataGeneratorSource has built-in support for rate limiting. The following code will produce a stream of
String values at the overall source rate (across all source subtasks) not exceeding 100 events per second.

`DataGeneratorSource`
`String`

```
GeneratorFunction<Long, String> generatorFunction = index -> "Number: " + index;

DataGeneratorSource<String> source =
        new DataGeneratorSource<>(
             generatorFunction,
             Long.MAX_VALUE,
             RateLimiterStrategy.perSecond(100),
             Types.STRING);

```

`GeneratorFunction<Long, String> generatorFunction = index -> "Number: " + index;

DataGeneratorSource<String> source =
        new DataGeneratorSource<>(
             generatorFunction,
             Long.MAX_VALUE,
             RateLimiterStrategy.perSecond(100),
             Types.STRING);
`

Additional rate limiting strategies, such as limiting the number of records emitted per checkpoint, can
be found in 

    RateLimiterStrategy

.


## Boundedness#


This source is always bounded. From a practical perspective, however, setting the number of records
to Long.MAX_VALUE turns it into an effectively unbounded source (the end will never be reached). For finite sequences users may want to consider running the application in BATCH execution mode
.

`Long.MAX_VALUE`
`BATCH`

## Notes#


> 
Note: DataGeneratorSource can be used to implement Flink jobs with at-least-once and
end-to-end exactly-once processing guarantees under the condition that the output of the GeneratorFunction
is deterministic with respect to its input, in other words supplying the same Long number always
leads to generating the same output.


`DataGeneratorSource`
`GeneratorFunction`
`Long`

> 
Note:  it is possible to also produce deterministic watermarks right at the
source based on the generated events and a custom

WatermarkStrategy

.

