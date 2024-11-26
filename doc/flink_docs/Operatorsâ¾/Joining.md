# Joining


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Joining#


## Window Join#


A window join joins the elements of two streams that share a common key and lie in the same window. These windows can be defined by using a window assigner and are evaluated on elements from both of the streams.


The elements from both sides are then passed to a user-defined JoinFunction or FlatJoinFunction where the user can emit results that meet the join criteria.

`JoinFunction`
`FlatJoinFunction`

The general usage can be summarized as follows:


```
stream.join(otherStream)
    .where(<KeySelector>)
    .equalTo(<KeySelector>)
    .window(<WindowAssigner>)
    .apply(<JoinFunction>);

```

`stream.join(otherStream)
    .where(<KeySelector>)
    .equalTo(<KeySelector>)
    .window(<WindowAssigner>)
    .apply(<JoinFunction>);
`

Some notes on semantics:

* The creation of pairwise combinations of elements of the two streams behaves like an inner-join, meaning elements from one stream will not be emitted if they don’t have a corresponding element from the other stream to be joined with.
* Those elements that do get joined will have as their timestamp the largest timestamp that still lies in the respective window. For example a window with [5, 10) as its boundaries would result in the joined elements having 9 as their timestamp.
`[5, 10)`

In the following section we are going to give an overview over how different kinds of window joins behave using some exemplary scenarios.


### Tumbling Window Join#


When performing a tumbling window join, all elements with a common key and a common tumbling window are joined as pairwise combinations and passed on to a JoinFunction or FlatJoinFunction. Because this behaves like an inner join, elements of one stream that do not have elements from another stream in their tumbling window are not emitted!

`JoinFunction`
`FlatJoinFunction`

As illustrated in the figure, we define a tumbling window with the size of 2 milliseconds, which results in windows of the form [0,1], [2,3], .... The image shows the pairwise combinations of all elements in each window which will be passed on to the JoinFunction. Note that in the tumbling window [6,7] nothing is emitted because no elements exist in the green stream to be joined with the orange elements â¥ and â¦.

`[0,1], [2,3], ...`
`JoinFunction`
`[6,7]`

```
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import java.time.Duration;
 
...

DataStream<Integer> orangeStream = ...;
DataStream<Integer> greenStream = ...;

orangeStream.join(greenStream)
    .where(<KeySelector>)
    .equalTo(<KeySelector>)
    .window(TumblingEventTimeWindows.of(Duration.ofMillis(2)))
    .apply (new JoinFunction<Integer, Integer, String> (){
        @Override
        public String join(Integer first, Integer second) {
            return first + "," + second;
        }
    });

```

`import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import java.time.Duration;
 
...

DataStream<Integer> orangeStream = ...;
DataStream<Integer> greenStream = ...;

orangeStream.join(greenStream)
    .where(<KeySelector>)
    .equalTo(<KeySelector>)
    .window(TumblingEventTimeWindows.of(Duration.ofMillis(2)))
    .apply (new JoinFunction<Integer, Integer, String> (){
        @Override
        public String join(Integer first, Integer second) {
            return first + "," + second;
        }
    });
`

```
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows
import java.time.Duration

...

val orangeStream: DataStream[Integer] = ...
val greenStream: DataStream[Integer] = ...

orangeStream.join(greenStream)
    .where(elem => /* select key */)
    .equalTo(elem => /* select key */)
    .window(TumblingEventTimeWindows.of(Duration.ofMillis(2)))
    .apply { (e1, e2) => e1 + "," + e2 }

```

`import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows
import java.time.Duration

...

val orangeStream: DataStream[Integer] = ...
val greenStream: DataStream[Integer] = ...

orangeStream.join(greenStream)
    .where(elem => /* select key */)
    .equalTo(elem => /* select key */)
    .window(TumblingEventTimeWindows.of(Duration.ofMillis(2)))
    .apply { (e1, e2) => e1 + "," + e2 }
`

### Sliding Window Join#


When performing a sliding window join, all elements with a common key and common sliding window are joined as pairwise combinations and passed on to the JoinFunction or FlatJoinFunction. Elements of one stream that do not have elements from the other stream in the current sliding window are not emitted! Note that some elements might be joined in one sliding window but not in another!

`JoinFunction`
`FlatJoinFunction`

In this example we are using sliding windows with a size of two milliseconds and slide them by one millisecond, resulting in the sliding windows [-1, 0],[0,1],[1,2],[2,3], â¦. The joined elements below the x-axis are the ones that are passed to the JoinFunction for each sliding window. Here you can also see how for example the orange â¡ is joined with the green â¢ in the window [2,3], but is not joined with anything in the window [1,2].

`[-1, 0],[0,1],[1,2],[2,3], â¦`
`JoinFunction`
`[2,3]`
`[1,2]`

```
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;
import java.time.Duration;

...

DataStream<Integer> orangeStream = ...;
DataStream<Integer> greenStream = ...;

orangeStream.join(greenStream)
    .where(<KeySelector>)
    .equalTo(<KeySelector>)
    .window(SlidingEventTimeWindows.of(Duration.ofMillis(2) /* size */, Duration.ofMillis(1) /* slide */))
    .apply (new JoinFunction<Integer, Integer, String> (){
        @Override
        public String join(Integer first, Integer second) {
            return first + "," + second;
        }
    });

```

`import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows;
import java.time.Duration;

...

DataStream<Integer> orangeStream = ...;
DataStream<Integer> greenStream = ...;

orangeStream.join(greenStream)
    .where(<KeySelector>)
    .equalTo(<KeySelector>)
    .window(SlidingEventTimeWindows.of(Duration.ofMillis(2) /* size */, Duration.ofMillis(1) /* slide */))
    .apply (new JoinFunction<Integer, Integer, String> (){
        @Override
        public String join(Integer first, Integer second) {
            return first + "," + second;
        }
    });
`

```
import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows
import java.time.Duration

...

val orangeStream: DataStream[Integer] = ...
val greenStream: DataStream[Integer] = ...

orangeStream.join(greenStream)
    .where(elem => /* select key */)
    .equalTo(elem => /* select key */)
    .window(SlidingEventTimeWindows.of(Duration.ofMillis(2) /* size */, Duration.ofMillis(1) /* slide */))
    .apply { (e1, e2) => e1 + "," + e2 }

```

`import org.apache.flink.streaming.api.windowing.assigners.SlidingEventTimeWindows
import java.time.Duration

...

val orangeStream: DataStream[Integer] = ...
val greenStream: DataStream[Integer] = ...

orangeStream.join(greenStream)
    .where(elem => /* select key */)
    .equalTo(elem => /* select key */)
    .window(SlidingEventTimeWindows.of(Duration.ofMillis(2) /* size */, Duration.ofMillis(1) /* slide */))
    .apply { (e1, e2) => e1 + "," + e2 }
`

### Session Window Join#


When performing a session window join, all elements with the same key that when “combined” fulfill the session criteria are joined in pairwise combinations and passed on to the JoinFunction or FlatJoinFunction. Again this performs an inner join, so if there is a session window that only contains elements from one stream, no output will be emitted!

`JoinFunction`
`FlatJoinFunction`

Here we define a session window join where each session is divided by a gap of at least 1ms. There are three sessions, and in the first two sessions the joined elements from both streams are passed to the JoinFunction. In the third session there are no elements in the green stream, so â§ and â¨ are not joined!

`JoinFunction`

```
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows;
import java.time.Duration;
 
...

DataStream<Integer> orangeStream = ...;
DataStream<Integer> greenStream = ...;

orangeStream.join(greenStream)
    .where(<KeySelector>)
    .equalTo(<KeySelector>)
    .window(EventTimeSessionWindows.withGap(Duration.ofMillis(1)))
    .apply (new JoinFunction<Integer, Integer, String> (){
        @Override
        public String join(Integer first, Integer second) {
            return first + "," + second;
        }
    });

```

`import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows;
import java.time.Duration;
 
...

DataStream<Integer> orangeStream = ...;
DataStream<Integer> greenStream = ...;

orangeStream.join(greenStream)
    .where(<KeySelector>)
    .equalTo(<KeySelector>)
    .window(EventTimeSessionWindows.withGap(Duration.ofMillis(1)))
    .apply (new JoinFunction<Integer, Integer, String> (){
        @Override
        public String join(Integer first, Integer second) {
            return first + "," + second;
        }
    });
`

```
import org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows
import java.time.Duration

...

val orangeStream: DataStream[Integer] = ...
val greenStream: DataStream[Integer] = ...

orangeStream.join(greenStream)
    .where(elem => /* select key */)
    .equalTo(elem => /* select key */)
    .window(EventTimeSessionWindows.withGap(Duration.ofMillis(1)))
    .apply { (e1, e2) => e1 + "," + e2 }

```

`import org.apache.flink.streaming.api.windowing.assigners.EventTimeSessionWindows
import java.time.Duration

...

val orangeStream: DataStream[Integer] = ...
val greenStream: DataStream[Integer] = ...

orangeStream.join(greenStream)
    .where(elem => /* select key */)
    .equalTo(elem => /* select key */)
    .window(EventTimeSessionWindows.withGap(Duration.ofMillis(1)))
    .apply { (e1, e2) => e1 + "," + e2 }
`

## Interval Join#


The interval join joins elements of two streams (we’ll call them A & B for now) with a common key and where elements of stream B have timestamps that lie in a relative time interval to timestamps of elements in stream A.


This can also be expressed more formally as
b.timestamp â [a.timestamp + lowerBound; a.timestamp + upperBound] or
a.timestamp + lowerBound <= b.timestamp <= a.timestamp + upperBound

`b.timestamp â [a.timestamp + lowerBound; a.timestamp + upperBound]`
`a.timestamp + lowerBound <= b.timestamp <= a.timestamp + upperBound`

where a and b are elements of A and B that share a common key. Both the lower and upper bound can be either negative or positive as long as the lower bound is always smaller or equal to the upper bound. The interval join currently only performs inner joins.


When a pair of elements are passed to the ProcessJoinFunction, they will be assigned with the larger timestamp (which can be accessed via the ProcessJoinFunction.Context) of the two elements.

`ProcessJoinFunction`
`ProcessJoinFunction.Context`

> 
  The interval join currently only supports event time.



In the example above, we join two streams ‘orange’ and ‘green’ with a lower bound of -2 milliseconds and an upper bound of +1 millisecond. Be default, these boundaries are inclusive, but .lowerBoundExclusive() and .upperBoundExclusive() can be applied to change the behaviour.

`.lowerBoundExclusive()`
`.upperBoundExclusive()`

Using the more formal notation again this will translate to


orangeElem.ts + lowerBound <= greenElem.ts <= orangeElem.ts + upperBound

`orangeElem.ts + lowerBound <= greenElem.ts <= orangeElem.ts + upperBound`

as indicated by the triangles.


```
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.streaming.api.functions.co.ProcessJoinFunction;
import java.time.Duration;

...

DataStream<Integer> orangeStream = ...;
DataStream<Integer> greenStream = ...;

orangeStream
    .keyBy(<KeySelector>)
    .intervalJoin(greenStream.keyBy(<KeySelector>))
    .between(Duration.ofMillis(-2), Duration.ofMillis(1))
    .process (new ProcessJoinFunction<Integer, Integer, String>(){

        @Override
        public void processElement(Integer left, Integer right, Context ctx, Collector<String> out) {
            out.collect(left + "," + right);
        }
    });

```

`import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.streaming.api.functions.co.ProcessJoinFunction;
import java.time.Duration;

...

DataStream<Integer> orangeStream = ...;
DataStream<Integer> greenStream = ...;

orangeStream
    .keyBy(<KeySelector>)
    .intervalJoin(greenStream.keyBy(<KeySelector>))
    .between(Duration.ofMillis(-2), Duration.ofMillis(1))
    .process (new ProcessJoinFunction<Integer, Integer, String>(){

        @Override
        public void processElement(Integer left, Integer right, Context ctx, Collector<String> out) {
            out.collect(left + "," + right);
        }
    });
`

```
import org.apache.flink.streaming.api.functions.co.ProcessJoinFunction
import java.time.Duration

...

val orangeStream: DataStream[Integer] = ...
val greenStream: DataStream[Integer] = ...

orangeStream
    .keyBy(elem => /* select key */)
    .intervalJoin(greenStream.keyBy(elem => /* select key */))
    .between(Duration.ofMillis(-2), Duration.ofMillis(1))
    .process(new ProcessJoinFunction[Integer, Integer, String] {
        override def processElement(left: Integer, right: Integer, ctx: ProcessJoinFunction[Integer, Integer, String]#Context, out: Collector[String]): Unit = {
            out.collect(left + "," + right)
        }
    })

```

`import org.apache.flink.streaming.api.functions.co.ProcessJoinFunction
import java.time.Duration

...

val orangeStream: DataStream[Integer] = ...
val greenStream: DataStream[Integer] = ...

orangeStream
    .keyBy(elem => /* select key */)
    .intervalJoin(greenStream.keyBy(elem => /* select key */))
    .between(Duration.ofMillis(-2), Duration.ofMillis(1))
    .process(new ProcessJoinFunction[Integer, Integer, String] {
        override def processElement(left: Integer, right: Integer, ctx: ProcessJoinFunction[Integer, Integer, String]#Context, out: Collector[String]): Unit = {
            out.collect(left + "," + right)
        }
    })
`

 Back to top
