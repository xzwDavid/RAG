# Side Outputs


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Side Outputs#


In addition to the main stream that results from DataStream operations, you can also produce any
number of additional side output result streams. The type of data in the result streams does not
have to match the type of data in the main stream and the types of the different side outputs can
also differ. This operation can be useful when you want to split a stream of data where you would
normally have to replicate the stream and then filter out from each stream the data that you don’t
want to have.

`DataStream`

When using side outputs, you first need to define an OutputTag that will be used to identify a
side output stream:

`OutputTag`

```
// this needs to be an anonymous inner class, so that we can analyze the type
OutputTag<String> outputTag = new OutputTag<String>("side-output") {};

```

`// this needs to be an anonymous inner class, so that we can analyze the type
OutputTag<String> outputTag = new OutputTag<String>("side-output") {};
`

```
val outputTag = OutputTag[String]("side-output")

```

`val outputTag = OutputTag[String]("side-output")
`

```
output_tag = OutputTag("side-output", Types.STRING())

```

`output_tag = OutputTag("side-output", Types.STRING())
`

Notice how the OutputTag is typed according to the type of elements that the side output stream
contains.

`OutputTag`

Emitting data to a side output is possible from the following functions:

* ProcessFunction
* KeyedProcessFunction
* CoProcessFunction
* KeyedCoProcessFunction
* ProcessWindowFunction
* ProcessAllWindowFunction

You can use the Context parameter, which is exposed to users in the above functions, to emit
data to a side output identified by an OutputTag. Here is an example of emitting side output
data from a ProcessFunction:

`Context`
`OutputTag`
`ProcessFunction`

```
DataStream<Integer> input = ...;

final OutputTag<String> outputTag = new OutputTag<String>("side-output"){};

SingleOutputStreamOperator<Integer> mainDataStream = input
  .process(new ProcessFunction<Integer, Integer>() {

      @Override
      public void processElement(
          Integer value,
          Context ctx,
          Collector<Integer> out) throws Exception {
        // emit data to regular output
        out.collect(value);

        // emit data to side output
        ctx.output(outputTag, "sideout-" + String.valueOf(value));
      }
    });

```

`DataStream<Integer> input = ...;

final OutputTag<String> outputTag = new OutputTag<String>("side-output"){};

SingleOutputStreamOperator<Integer> mainDataStream = input
  .process(new ProcessFunction<Integer, Integer>() {

      @Override
      public void processElement(
          Integer value,
          Context ctx,
          Collector<Integer> out) throws Exception {
        // emit data to regular output
        out.collect(value);

        // emit data to side output
        ctx.output(outputTag, "sideout-" + String.valueOf(value));
      }
    });
`

```

val input: DataStream[Int] = ...
val outputTag = OutputTag[String]("side-output")

val mainDataStream = input
  .process(new ProcessFunction[Int, Int] {
    override def processElement(
        value: Int,
        ctx: ProcessFunction[Int, Int]#Context,
        out: Collector[Int]): Unit = {
      // emit data to regular output
      out.collect(value)

      // emit data to side output
      ctx.output(outputTag, "sideout-" + String.valueOf(value))
    }
  })

```

`
val input: DataStream[Int] = ...
val outputTag = OutputTag[String]("side-output")

val mainDataStream = input
  .process(new ProcessFunction[Int, Int] {
    override def processElement(
        value: Int,
        ctx: ProcessFunction[Int, Int]#Context,
        out: Collector[Int]): Unit = {
      // emit data to regular output
      out.collect(value)

      // emit data to side output
      ctx.output(outputTag, "sideout-" + String.valueOf(value))
    }
  })
`

```
input = ...  # type: DataStream
output_tag = OutputTag("side-output", Types.STRING())

class MyProcessFunction(ProcessFunction):

    def process_element(self, value: int, ctx: ProcessFunction.Context):
        # emit data to regular output
        yield value

        # emit data to side output
        yield output_tag, "sideout-" + str(value)


main_data_stream = input \
    .process(MyProcessFunction(), Types.INT())

```

`input = ...  # type: DataStream
output_tag = OutputTag("side-output", Types.STRING())

class MyProcessFunction(ProcessFunction):

    def process_element(self, value: int, ctx: ProcessFunction.Context):
        # emit data to regular output
        yield value

        # emit data to side output
        yield output_tag, "sideout-" + str(value)


main_data_stream = input \
    .process(MyProcessFunction(), Types.INT())
`

For retrieving the side output stream you use getSideOutput(OutputTag)
on the result of the DataStream operation. This will give you a DataStream that is typed
to the result of the side output stream:

`getSideOutput(OutputTag)`
`DataStream`
`DataStream`

```
final OutputTag<String> outputTag = new OutputTag<String>("side-output"){};

SingleOutputStreamOperator<Integer> mainDataStream = ...;

DataStream<String> sideOutputStream = mainDataStream.getSideOutput(outputTag);

```

`final OutputTag<String> outputTag = new OutputTag<String>("side-output"){};

SingleOutputStreamOperator<Integer> mainDataStream = ...;

DataStream<String> sideOutputStream = mainDataStream.getSideOutput(outputTag);
`

```
val outputTag = OutputTag[String]("side-output")

val mainDataStream = ...

val sideOutputStream: DataStream[String] = mainDataStream.getSideOutput(outputTag)

```

`val outputTag = OutputTag[String]("side-output")

val mainDataStream = ...

val sideOutputStream: DataStream[String] = mainDataStream.getSideOutput(outputTag)
`

```
output_tag = OutputTag("side-output", Types.STRING())

main_data_stream = ...  # type: DataStream

side_output_stream = main_data_stream.get_side_output(output_tag)  # type: DataStream

```

`output_tag = OutputTag("side-output", Types.STRING())

main_data_stream = ...  # type: DataStream

side_output_stream = main_data_stream.get_side_output(output_tag)  # type: DataStream
`

Note If it produces side output, get_side_output(OutputTag)
must be called in Python API. Otherwise, the result of side output stream will be output into the
main stream which is unexpected and may fail the job when the data types are different.

`get_side_output(OutputTag)`

 Back to top
