# User-Defined Functions


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# User-Defined Functions#


Most operations require a user-defined function. This section lists different
ways of how they can be specified. We also cover Accumulators, which can be
used to gain insights into your Flink application.

`Accumulators`

## Implementing an interface#


The most basic way is to implement one of the provided interfaces:


```
class MyMapFunction implements MapFunction<String, Integer> {
  public Integer map(String value) { return Integer.parseInt(value); }
}
data.map(new MyMapFunction());

```

`class MyMapFunction implements MapFunction<String, Integer> {
  public Integer map(String value) { return Integer.parseInt(value); }
}
data.map(new MyMapFunction());
`

## Anonymous classes#


You can pass a function as an anonymous class:


```
data.map(new MapFunction<String, Integer> () {
  public Integer map(String value) { return Integer.parseInt(value); }
});

```

`data.map(new MapFunction<String, Integer> () {
  public Integer map(String value) { return Integer.parseInt(value); }
});
`

## Java 8 Lambdas#


Flink also supports Java 8 Lambdas in the Java API.


```
data.filter(s -> s.startsWith("http://"));

```

`data.filter(s -> s.startsWith("http://"));
`

```
data.reduce((i1,i2) -> i1 + i2);

```

`data.reduce((i1,i2) -> i1 + i2);
`

## Rich functions#


All transformations that require a user-defined function can
instead take as argument a rich function. For example, instead of


```
class MyMapFunction implements MapFunction<String, Integer> {
  public Integer map(String value) { return Integer.parseInt(value); }
}

```

`class MyMapFunction implements MapFunction<String, Integer> {
  public Integer map(String value) { return Integer.parseInt(value); }
}
`

you can write


```
class MyMapFunction extends RichMapFunction<String, Integer> {
  public Integer map(String value) { return Integer.parseInt(value); }
}

```

`class MyMapFunction extends RichMapFunction<String, Integer> {
  public Integer map(String value) { return Integer.parseInt(value); }
}
`

and pass the function as usual to a map transformation:

`map`

```
data.map(new MyMapFunction());

```

`data.map(new MyMapFunction());
`

Rich functions can also be defined as an anonymous class:


```
data.map (new RichMapFunction<String, Integer>() {
  public Integer map(String value) { return Integer.parseInt(value); }
});

```

`data.map (new RichMapFunction<String, Integer>() {
  public Integer map(String value) { return Integer.parseInt(value); }
});
`

## Lambda Functions#


As already seen in previous examples all operations accept lambda functions for describing
the operation:


```
val data: DataStream[String] = // [...]
data.filter { _.startsWith("http://") }

```

`val data: DataStream[String] = // [...]
data.filter { _.startsWith("http://") }
`

```
val data: DataStream[Int] = // [...]
data.reduce { (i1,i2) => i1 + i2 }
// or
data.reduce { _ + _ }

```

`val data: DataStream[Int] = // [...]
data.reduce { (i1,i2) => i1 + i2 }
// or
data.reduce { _ + _ }
`

## Rich functions#


All transformations that take as argument a lambda function can
instead take as argument a rich function. For example, instead of


```
data.map { x => x.toInt }

```

`data.map { x => x.toInt }
`

you can write


```
class MyMapFunction extends RichMapFunction[String, Int] {
  def map(in: String): Int = in.toInt
}

```

`class MyMapFunction extends RichMapFunction[String, Int] {
  def map(in: String): Int = in.toInt
}
`

and pass the function to a map transformation:

`map`

```
data.map(new MyMapFunction())

```

`data.map(new MyMapFunction())
`

Rich functions can also be defined as an anonymous class:


```
data.map (new RichMapFunction[String, Int] {
  def map(in: String): Int = in.toInt
})

```

`data.map (new RichMapFunction[String, Int] {
  def map(in: String): Int = in.toInt
})
`

 Back to top


## Accumulators & Counters#


Accumulators are simple constructs with an add operation and a final accumulated result,
which is available after the job ended.


The most straightforward accumulator is a counter: You can increment it using the
Accumulator.add(V value) method. At the end of the job Flink will sum up (merge) all partial
results and send the result to the client. Accumulators are useful during debugging or if you
quickly want to find out more about your data.

`Accumulator.add(V value)`

Flink currently has the following built-in accumulators. Each of them implements the


    Accumulator


interface.

* 

IntCounter

,

  
LongCounter


and 

DoubleCounter

:
See below for an example using a counter.
* 

Histogram

:
A histogram implementation for a discrete number of bins. Internally it is just a map from Integer
to Integer. You can use this to compute distributions of values, e.g. the distribution of
words-per-line for a word count program.

How to use accumulators:


First you have to create an accumulator object (here a counter) in the user-defined transformation
function where you want to use it.


```
private IntCounter numLines = new IntCounter();

```

`private IntCounter numLines = new IntCounter();
`

Second you have to register the accumulator object, typically in the open() method of the
rich function. Here you also define the name.

`open()`

```
getRuntimeContext().addAccumulator("num-lines", this.numLines);

```

`getRuntimeContext().addAccumulator("num-lines", this.numLines);
`

You can now use the accumulator anywhere in the operator function, including in the open() and
close() methods.

`open()`
`close()`

```
this.numLines.add(1);

```

`this.numLines.add(1);
`

The overall result will be stored in the JobExecutionResult object which is
returned from the execute() method of the execution environment
(currently this only works if the execution waits for the
completion of the job).

`JobExecutionResult`
`execute()`

```
myJobExecutionResult.getAccumulatorResult("num-lines");

```

`myJobExecutionResult.getAccumulatorResult("num-lines");
`

All accumulators share a single namespace per job. Thus you can use the same accumulator in
different operator functions of your job. Flink will internally merge all accumulators with the same
name.


Custom accumulators:


To implement your own accumulator you simply have to write your implementation of the Accumulator
interface. Feel free to create a pull request if you think your custom accumulator should be shipped
with Flink.


You have the choice to implement either


    Accumulator


or 

    SimpleAccumulator

.


Accumulator<V,R> is most flexible: It defines a type V for the value to add, and a
result type R for the final result. E.g. for a histogram, V is a number and R is
a histogram. SimpleAccumulator is for the cases where both types are the same, e.g. for counters.

`Accumulator<V,R>`
`V`
`R`
`V`
`R`
`SimpleAccumulator`

 Back to top
