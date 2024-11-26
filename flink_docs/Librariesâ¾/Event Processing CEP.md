# Event Processing (CEP)


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# FlinkCEP - Complex event processing for Flink#


FlinkCEP is the Complex Event Processing (CEP) library implemented on top of Flink.
It allows you to detect event patterns in an endless stream of events, giving you the opportunity to get hold of what’s important in your
data.


This page describes the API calls available in Flink CEP. We start by presenting the Pattern API,
which allows you to specify the patterns that you want to detect in your stream, before presenting how you can
detect and act upon matching event sequences. We then present the assumptions the CEP
library makes when dealing with lateness in event time and how you can
migrate your job from an older Flink version to Flink-1.13.


## Getting Started#


If you want to jump right in, set up a Flink program and
add the FlinkCEP dependency to the pom.xml of your project.

`pom.xml`

```
&ltdependency>
    &ltgroupId>org.apache.flink</groupId>
    &ltartifactId>flink-cep</artifactId>
    &ltversion>2.0-SNAPSHOT</version>
</dependency>
```

`&ltdependency>
    &ltgroupId>org.apache.flink</groupId>
    &ltartifactId>flink-cep</artifactId>
    &ltversion>2.0-SNAPSHOT</version>
</dependency>`

FlinkCEP is not part of the binary distribution. See how to link with it for cluster execution
here.


Now you can start writing your first CEP program using the Pattern API.


> 
  The events in the DataStream to which
you want to apply pattern matching must implement proper equals() and hashCode() methods
because FlinkCEP uses them for comparing and matching events.


`DataStream`
`equals()`
`hashCode()`

```
DataStream<Event> input = ...;

Pattern<Event, ?> pattern = Pattern.<Event>begin("start")
    .where(SimpleCondition.of(event -> event.getId() == 42))
    .next("middle")
    .subtype(SubEvent.class)
    .where(SimpleCondition.of(subEvent -> subEvent.getVolume() >= 10.0))
    .followedBy("end")
    .where(SimpleCondition.of(event -> event.getName().equals("end")));

PatternStream<Event> patternStream = CEP.pattern(input, pattern);

DataStream<Alert> result = patternStream.process(
    new PatternProcessFunction<Event, Alert>() {
        @Override
        public void processMatch(
                Map<String, List<Event>> pattern,
                Context ctx,
                Collector<Alert> out) throws Exception {
            out.collect(createAlertFrom(pattern));
        }
    });

```

`DataStream<Event> input = ...;

Pattern<Event, ?> pattern = Pattern.<Event>begin("start")
    .where(SimpleCondition.of(event -> event.getId() == 42))
    .next("middle")
    .subtype(SubEvent.class)
    .where(SimpleCondition.of(subEvent -> subEvent.getVolume() >= 10.0))
    .followedBy("end")
    .where(SimpleCondition.of(event -> event.getName().equals("end")));

PatternStream<Event> patternStream = CEP.pattern(input, pattern);

DataStream<Alert> result = patternStream.process(
    new PatternProcessFunction<Event, Alert>() {
        @Override
        public void processMatch(
                Map<String, List<Event>> pattern,
                Context ctx,
                Collector<Alert> out) throws Exception {
            out.collect(createAlertFrom(pattern));
        }
    });
`

```
val input: DataStream[Event] = ...

val pattern = Pattern.begin[Event]("start").where(_.getId == 42)
  .next("middle").subtype(classOf[SubEvent]).where(_.getVolume >= 10.0)
  .followedBy("end").where(_.getName == "end")

val patternStream = CEP.pattern(input, pattern)

val result: DataStream[Alert] = patternStream.process(
    new PatternProcessFunction[Event, Alert]() {
        override def processMatch(
              `match`: util.Map[String, util.List[Event]],
              ctx: PatternProcessFunction.Context,
              out: Collector[Alert]): Unit = {
            out.collect(createAlertFrom(pattern))
        }
    })

```

`val input: DataStream[Event] = ...

val pattern = Pattern.begin[Event]("start").where(_.getId == 42)
  .next("middle").subtype(classOf[SubEvent]).where(_.getVolume >= 10.0)
  .followedBy("end").where(_.getName == "end")

val patternStream = CEP.pattern(input, pattern)

val result: DataStream[Alert] = patternStream.process(
    new PatternProcessFunction[Event, Alert]() {
        override def processMatch(
              `match`: util.Map[String, util.List[Event]],
              ctx: PatternProcessFunction.Context,
              out: Collector[Alert]): Unit = {
            out.collect(createAlertFrom(pattern))
        }
    })
`

## The Pattern API#


The pattern API allows you to define complex pattern sequences that you want to extract from your input stream.


Each complex pattern sequence consists of multiple simple patterns, i.e. patterns looking for individual events with the same properties. From now on, we will call these simple patterns patterns, and the final complex pattern sequence we are searching for in the stream, the pattern sequence. You can see a pattern sequence as a graph of such patterns, where transitions from one pattern to the next occur based on user-specified
conditions, e.g. event.getName().equals("end"). A match is a sequence of input events which visits all
patterns of the complex pattern graph, through a sequence of valid pattern transitions.

`event.getName().equals("end")`

> 
  Each pattern must have a unique name, which you use later to identify the matched events.



> 
  Pattern names CANNOT contain the character ":".


`":"`

In the rest of this section we will first describe how to define Individual Patterns, and then how you can combine individual patterns into Complex Patterns.


### Individual Patterns#


A Pattern can be either a singleton or a looping pattern. Singleton patterns accept a single
event, while looping patterns can accept more than one. In pattern matching symbols, the pattern "a b+ c? d" (or "a", followed by one or more "b"’s, optionally followed by a "c", followed by a "d"), a, c?, and d are
singleton patterns, while b+ is a looping one. By default, a pattern is a singleton pattern and you can transform
it to a looping one by using Quantifiers. Each pattern can have one or more
Conditions based on which it accepts events.

`"a b+ c? d"`
`"a"`
`"b"`
`"c"`
`"d"`
`a`
`c?`
`d`
`b+`

#### Quantifiers#


In FlinkCEP, you can specify looping patterns using these methods: pattern.oneOrMore(), for patterns that expect one or more occurrences of a given event (e.g. the b+ mentioned before); and pattern.times(#ofTimes), for patterns that
expect a specific number of occurrences of a given type of event, e.g. 4 a’s; and pattern.times(#fromTimes, #toTimes), for patterns that expect a specific minimum number of occurrences and a maximum number of occurrences of a given type of event, e.g. 2-4 as.

`pattern.oneOrMore()`
`b+`
`pattern.times(#ofTimes)`
`a`
`pattern.times(#fromTimes, #toTimes)`
`a`

You can make looping patterns greedy using the pattern.greedy() method, but you cannot yet make group patterns greedy. You can make all patterns, looping or not, optional using the pattern.optional() method.

`pattern.greedy()`
`pattern.optional()`

For a pattern named start, the following are valid quantifiers:

`start`

```
// expecting 4 occurrences
start.times(4);

// expecting 0 or 4 occurrences
start.times(4).optional();

// expecting 2, 3 or 4 occurrences
start.times(2, 4);

// expecting 2, 3 or 4 occurrences and repeating as many as possible
start.times(2, 4).greedy();

// expecting 0, 2, 3 or 4 occurrences
start.times(2, 4).optional();

// expecting 0, 2, 3 or 4 occurrences and repeating as many as possible
start.times(2, 4).optional().greedy();

// expecting 1 or more occurrences
start.oneOrMore();

// expecting 1 or more occurrences and repeating as many as possible
start.oneOrMore().greedy();

// expecting 0 or more occurrences
start.oneOrMore().optional();

// expecting 0 or more occurrences and repeating as many as possible
start.oneOrMore().optional().greedy();

// expecting 2 or more occurrences
start.timesOrMore(2);

// expecting 2 or more occurrences and repeating as many as possible
start.timesOrMore(2).greedy();

// expecting 0, 2 or more occurrences
start.timesOrMore(2).optional()

// expecting 0, 2 or more occurrences and repeating as many as possible
start.timesOrMore(2).optional().greedy();

```

`// expecting 4 occurrences
start.times(4);

// expecting 0 or 4 occurrences
start.times(4).optional();

// expecting 2, 3 or 4 occurrences
start.times(2, 4);

// expecting 2, 3 or 4 occurrences and repeating as many as possible
start.times(2, 4).greedy();

// expecting 0, 2, 3 or 4 occurrences
start.times(2, 4).optional();

// expecting 0, 2, 3 or 4 occurrences and repeating as many as possible
start.times(2, 4).optional().greedy();

// expecting 1 or more occurrences
start.oneOrMore();

// expecting 1 or more occurrences and repeating as many as possible
start.oneOrMore().greedy();

// expecting 0 or more occurrences
start.oneOrMore().optional();

// expecting 0 or more occurrences and repeating as many as possible
start.oneOrMore().optional().greedy();

// expecting 2 or more occurrences
start.timesOrMore(2);

// expecting 2 or more occurrences and repeating as many as possible
start.timesOrMore(2).greedy();

// expecting 0, 2 or more occurrences
start.timesOrMore(2).optional()

// expecting 0, 2 or more occurrences and repeating as many as possible
start.timesOrMore(2).optional().greedy();
`

```
// expecting 4 occurrences
start.times(4)

// expecting 0 or 4 occurrences
start.times(4).optional()

// expecting 2, 3 or 4 occurrences
start.times(2, 4)

// expecting 2, 3 or 4 occurrences and repeating as many as possible
start.times(2, 4).greedy()

// expecting 0, 2, 3 or 4 occurrences
start.times(2, 4).optional()

// expecting 0, 2, 3 or 4 occurrences and repeating as many as possible
start.times(2, 4).optional().greedy()

// expecting 1 or more occurrences
start.oneOrMore()

// expecting 1 or more occurrences and repeating as many as possible
start.oneOrMore().greedy()

// expecting 0 or more occurrences
start.oneOrMore().optional()

// expecting 0 or more occurrences and repeating as many as possible
start.oneOrMore().optional().greedy()

// expecting 2 or more occurrences
start.timesOrMore(2)

// expecting 2 or more occurrences and repeating as many as possible
start.timesOrMore(2).greedy()

// expecting 0, 2 or more occurrences
start.timesOrMore(2).optional()

// expecting 0, 2 or more occurrences and repeating as many as possible
start.timesOrMore(2).optional().greedy()

```

`// expecting 4 occurrences
start.times(4)

// expecting 0 or 4 occurrences
start.times(4).optional()

// expecting 2, 3 or 4 occurrences
start.times(2, 4)

// expecting 2, 3 or 4 occurrences and repeating as many as possible
start.times(2, 4).greedy()

// expecting 0, 2, 3 or 4 occurrences
start.times(2, 4).optional()

// expecting 0, 2, 3 or 4 occurrences and repeating as many as possible
start.times(2, 4).optional().greedy()

// expecting 1 or more occurrences
start.oneOrMore()

// expecting 1 or more occurrences and repeating as many as possible
start.oneOrMore().greedy()

// expecting 0 or more occurrences
start.oneOrMore().optional()

// expecting 0 or more occurrences and repeating as many as possible
start.oneOrMore().optional().greedy()

// expecting 2 or more occurrences
start.timesOrMore(2)

// expecting 2 or more occurrences and repeating as many as possible
start.timesOrMore(2).greedy()

// expecting 0, 2 or more occurrences
start.timesOrMore(2).optional()

// expecting 0, 2 or more occurrences and repeating as many as possible
start.timesOrMore(2).optional().greedy()
`

#### Conditions#


For every pattern you can specify a condition that an incoming event has to meet in order to be “accepted” into the pattern e.g. its value should be larger than 5,
or larger than the average value of the previously accepted events.
You can specify conditions on the event properties via the pattern.where(), pattern.or() or pattern.until() methods.
These can be either IterativeConditions or SimpleConditions.

`pattern.where()`
`pattern.or()`
`pattern.until()`
`IterativeCondition`
`SimpleCondition`

Iterative Conditions: This is the most general type of condition. This is how you can specify a condition that
accepts subsequent events based on properties of the previously accepted events or a statistic over a subset of them.


Below is the code for an iterative condition that accepts the next event for a pattern named “middle” if its name starts
with “foo”, and if the sum of the prices of the previously accepted events for that pattern plus the price of the current event do not exceed the value of 5.0. Iterative conditions can be powerful, especially in combination with looping patterns, e.g. oneOrMore().

`oneOrMore()`

```
middle.oneOrMore()
    .subtype(SubEvent.class)
    .where(new IterativeCondition<SubEvent>() {
        @Override
        public boolean filter(SubEvent value, Context<SubEvent> ctx) throws Exception {
            if (!value.getName().startsWith("foo")) {
                return false;
            }
    
            double sum = value.getPrice();
            for (Event event : ctx.getEventsForPattern("middle")) {
                sum += event.getPrice();
            }
            return Double.compare(sum, 5.0) < 0;
        }
    });

```

`middle.oneOrMore()
    .subtype(SubEvent.class)
    .where(new IterativeCondition<SubEvent>() {
        @Override
        public boolean filter(SubEvent value, Context<SubEvent> ctx) throws Exception {
            if (!value.getName().startsWith("foo")) {
                return false;
            }
    
            double sum = value.getPrice();
            for (Event event : ctx.getEventsForPattern("middle")) {
                sum += event.getPrice();
            }
            return Double.compare(sum, 5.0) < 0;
        }
    });
`

```
middle.oneOrMore()
    .subtype(classOf[SubEvent])
    .where(
        (value, ctx) => {
            lazy val sum = ctx.getEventsForPattern("middle").map(_.getPrice).sum
            value.getName.startsWith("foo") && sum + value.getPrice < 5.0
        }
    )

```

`middle.oneOrMore()
    .subtype(classOf[SubEvent])
    .where(
        (value, ctx) => {
            lazy val sum = ctx.getEventsForPattern("middle").map(_.getPrice).sum
            value.getName.startsWith("foo") && sum + value.getPrice < 5.0
        }
    )
`

> 
  The call to ctx.getEventsForPattern(...) finds all the
previously accepted events for a given potential match. The cost of this operation can vary, so when implementing
your condition, try to minimize its use.


`ctx.getEventsForPattern(...)`

Described context gives one access to event time characteristics as well. For more info see Time context.


Simple Conditions: This type of condition extends the aforementioned IterativeCondition class and decides
whether to accept an event or not, based only on properties of the event itself.

`IterativeCondition`

```
start.where(SimpleCondition.of(value -> value.getName().startsWith("foo")));

```

`start.where(SimpleCondition.of(value -> value.getName().startsWith("foo")));
`

```
start.where(event => event.getName.startsWith("foo"))

```

`start.where(event => event.getName.startsWith("foo"))
`

Finally, you can also restrict the type of the accepted event to a subtype of the initial event type (here Event)
via the pattern.subtype(subClass) method.

`Event`
`pattern.subtype(subClass)`

```
start.subtype(SubEvent.class)
        .where(SimpleCondition.of(value -> ... /*some condition*/));

```

`start.subtype(SubEvent.class)
        .where(SimpleCondition.of(value -> ... /*some condition*/));
`

```
start.subtype(classOf[SubEvent]).where(subEvent => ... /* some condition */)

```

`start.subtype(classOf[SubEvent]).where(subEvent => ... /* some condition */)
`

Combining Conditions: As shown above, you can combine the subtype condition with additional conditions. This holds for every condition. You can arbitrarily combine conditions by sequentially calling where(). The final result will be the logical AND of the results of the individual conditions. To combine conditions using OR, you can use the or() method, as shown below.

`subtype`
`where()`
`or()`

```
pattern.where(SimpleCondition.of(value -> ... /*some condition*/))
        .or(SimpleCondition.of(value -> ... /*some condition*/));

```

`pattern.where(SimpleCondition.of(value -> ... /*some condition*/))
        .or(SimpleCondition.of(value -> ... /*some condition*/));
`

```
pattern.where(event => ... /* some condition */).or(event => ... /* or condition */)

```

`pattern.where(event => ... /* some condition */).or(event => ... /* or condition */)
`

Stop condition: In case of looping patterns (oneOrMore() and oneOrMore().optional()) you can
also specify a stop condition, e.g. accept events with value larger than 5 until the sum of values is smaller than 50.

`oneOrMore()`
`oneOrMore().optional()`

To better understand it, have a look at the following example. Given

* 
pattern like "(a+ until b)" (one or more "a" until "b")

* 
a sequence of incoming events "a1" "c" "a2" "b" "a3"

* 
the library will output results: {a1 a2} {a1} {a2} {a3}.


pattern like "(a+ until b)" (one or more "a" until "b")

`"(a+ until b)"`
`"a"`
`"b"`

a sequence of incoming events "a1" "c" "a2" "b" "a3"

`"a1" "c" "a2" "b" "a3"`

the library will output results: {a1 a2} {a1} {a2} {a3}.

`{a1 a2} {a1} {a2} {a3}`

As you can see {a1 a2 a3} or {a2 a3} are not returned due to the stop condition.

`{a1 a2 a3}`
`{a2 a3}`

#### where(condition)#

`where(condition)`

Defines a condition for the current pattern. To match the pattern, an event must satisfy the condition.
Multiple consecutive where() clauses lead to their conditions being ANDed.

`AND`

```
pattern.where(new IterativeCondition<Event>() {
    @Override
    public boolean filter(Event value, Context ctx) throws Exception {
        return ...; // some condition
    }
});

```

`pattern.where(new IterativeCondition<Event>() {
    @Override
    public boolean filter(Event value, Context ctx) throws Exception {
        return ...; // some condition
    }
});
`

```
pattern.where(event => ... /* some condition */)

```

`pattern.where(event => ... /* some condition */)
`

#### or(condition)#

`or(condition)`

Adds a new condition which is ORed with an existing one. An event can match the pattern only if it passes at least one of the conditions.

`OR`

```
pattern.where(new IterativeCondition<Event>() {
    @Override
    public boolean filter(Event value, Context ctx) throws Exception {
        return ...; // some condition
    }
}).or(new IterativeCondition<Event>() {
    @Override
    public boolean filter(Event value, Context ctx) throws Exception {
        return ...; // alternative condition
    }
});

```

`pattern.where(new IterativeCondition<Event>() {
    @Override
    public boolean filter(Event value, Context ctx) throws Exception {
        return ...; // some condition
    }
}).or(new IterativeCondition<Event>() {
    @Override
    public boolean filter(Event value, Context ctx) throws Exception {
        return ...; // alternative condition
    }
});
`

```
pattern.where(event => ... /* some condition */)
    .or(event => ... /* alternative condition */)

```

`pattern.where(event => ... /* some condition */)
    .or(event => ... /* alternative condition */)
`

#### until(condition)#

`until(condition)`

Specifies a stop condition for a looping pattern. Meaning if event matching the given condition occurs, no more
events will be accepted into the pattern. Applicable only in conjunction with oneOrMore()
NOTE: It allows for cleaning state for corresponding pattern on event-based condition.

`oneOrMore()`
`NOTE:`

```
pattern.oneOrMore().until(new IterativeCondition<Event>() {
    @Override
    public boolean filter(Event value, Context ctx) throws Exception {
        return ...; // alternative condition
    }
});

```

`pattern.oneOrMore().until(new IterativeCondition<Event>() {
    @Override
    public boolean filter(Event value, Context ctx) throws Exception {
        return ...; // alternative condition
    }
});
`

```
pattern.oneOrMore().until(event => ... /* some condition */)

```

`pattern.oneOrMore().until(event => ... /* some condition */)
`

#### subtype(subClass)#

`subtype(subClass)`

Defines a subtype condition for the current pattern. An event can only match the pattern if it is of this subtype.


```
pattern.subtype(SubEvent.class);

```

`pattern.subtype(SubEvent.class);
`

```
pattern.subtype(classOf[SubEvent])

```

`pattern.subtype(classOf[SubEvent])
`

#### oneOrMore()#

`oneOrMore()`

Specifies that this pattern expects at least one occurrence of a matching event.
By default a relaxed internal contiguity (between subsequent events) is used. For more info on
internal contiguity see consecutive.
It is advised to use either until() or within() to enable state clearing.

`until()`
`within()`

```
pattern.oneOrMore();

```

`pattern.oneOrMore();
`

```
pattern.oneOrMore()

```

`pattern.oneOrMore()
`

#### timesOrMore(#times)#

`timesOrMore(#times)`

Specifies that this pattern expects at least #times occurrences of a matching event.
By default a relaxed internal contiguity (between subsequent events) is used. For more info on
internal contiguity see consecutive.

`#times`

```
pattern.timesOrMore(2);

```

`pattern.timesOrMore(2);
`

#### times(#ofTimes)#

`times(#ofTimes)`

Specifies that this pattern expects an exact number of occurrences of a matching event.
By default a relaxed internal contiguity (between subsequent events) is used.
For more info on internal contiguity see consecutive.


```
pattern.times(2);

```

`pattern.times(2);
`

```
pattern.times(2)

```

`pattern.times(2)
`

#### times(#fromTimes, #toTimes)#

`times(#fromTimes, #toTimes)`

Specifies that this pattern expects occurrences between #fromTimes
and #toTimes of a matching event.
By default a relaxed internal contiguity (between subsequent events) is used. For more info on
internal contiguity see consecutive.

`#fromTimes`
`#toTimes`

```
pattern.times(2, 4);

```

`pattern.times(2, 4);
`

```
pattern.times(2, 4)

```

`pattern.times(2, 4)
`

#### optional()#

`optional()`

Specifies that this pattern is optional, i.e. it may not occur at all. This is applicable to all aforementioned quantifiers.


```
pattern.oneOrMore().optional();

```

`pattern.oneOrMore().optional();
`

```
pattern.oneOrMore().optional()

```

`pattern.oneOrMore().optional()
`

#### greedy()#

`greedy()`

Specifies that this pattern is greedy, i.e. it will repeat as many as possible. This is only applicable
to quantifiers and it does not support group pattern currently.


```
pattern.oneOrMore().greedy();

```

`pattern.oneOrMore().greedy();
`

```
pattern.oneOrMore().greedy()

```

`pattern.oneOrMore().greedy()
`

### Combining Patterns#


Now that you’ve seen what an individual pattern can look like, it is time to see how to combine them
into a full pattern sequence.


A pattern sequence has to start with an initial pattern, as shown below:


```
Pattern<Event, ?> start = Pattern.<Event>begin("start");

```

`Pattern<Event, ?> start = Pattern.<Event>begin("start");
`

```
val start : Pattern[Event, _] = Pattern.begin("start")

```

`val start : Pattern[Event, _] = Pattern.begin("start")
`

Next, you can append more patterns to your pattern sequence by specifying the desired contiguity conditions between
them. FlinkCEP supports the following forms of contiguity between events:

1. 
Strict Contiguity: Expects all matching events to appear strictly one after the other, without any non-matching events in-between.

2. 
Relaxed Contiguity: Ignores non-matching events appearing in-between the matching ones.

3. 
Non-Deterministic Relaxed Contiguity: Further relaxes contiguity, allowing additional matches
that ignore some matching events.


Strict Contiguity: Expects all matching events to appear strictly one after the other, without any non-matching events in-between.


Relaxed Contiguity: Ignores non-matching events appearing in-between the matching ones.


Non-Deterministic Relaxed Contiguity: Further relaxes contiguity, allowing additional matches
that ignore some matching events.


To apply them between consecutive patterns, you can use:

1. next(), for strict,
2. followedBy(), for relaxed, and
3. followedByAny(), for non-deterministic relaxed contiguity.
`next()`
`followedBy()`
`followedByAny()`

or

1. notNext(), if you do not want an event type to directly follow another
2. notFollowedBy(), if you do not want an event type to be anywhere between two other event types.
`notNext()`
`notFollowedBy()`

> 
  A pattern sequence cannot end with notFollowedBy() if the time interval is not defined via withIn().


`notFollowedBy()`
`withIn()`

> 
  A NOT pattern cannot be preceded by an optional one.



```

// strict contiguity
Pattern<Event, ?> strict = start.next("middle").where(...);

// relaxed contiguity
Pattern<Event, ?> relaxed = start.followedBy("middle").where(...);

// non-deterministic relaxed contiguity
Pattern<Event, ?> nonDetermin = start.followedByAny("middle").where(...);

// NOT pattern with strict contiguity
Pattern<Event, ?> strictNot = start.notNext("not").where(...);

// NOT pattern with relaxed contiguity
Pattern<Event, ?> relaxedNot = start.notFollowedBy("not").where(...);

```

`
// strict contiguity
Pattern<Event, ?> strict = start.next("middle").where(...);

// relaxed contiguity
Pattern<Event, ?> relaxed = start.followedBy("middle").where(...);

// non-deterministic relaxed contiguity
Pattern<Event, ?> nonDetermin = start.followedByAny("middle").where(...);

// NOT pattern with strict contiguity
Pattern<Event, ?> strictNot = start.notNext("not").where(...);

// NOT pattern with relaxed contiguity
Pattern<Event, ?> relaxedNot = start.notFollowedBy("not").where(...);
`

```

// strict contiguity
val strict: Pattern[Event, _] = start.next("middle").where(...)

// relaxed contiguity
val relaxed: Pattern[Event, _] = start.followedBy("middle").where(...)

// non-deterministic relaxed contiguity
val nonDetermin: Pattern[Event, _] = start.followedByAny("middle").where(...)

// NOT pattern with strict contiguity
val strictNot: Pattern[Event, _] = start.notNext("not").where(...)

// NOT pattern with relaxed contiguity
val relaxedNot: Pattern[Event, _] = start.notFollowedBy("not").where(...)

```

`
// strict contiguity
val strict: Pattern[Event, _] = start.next("middle").where(...)

// relaxed contiguity
val relaxed: Pattern[Event, _] = start.followedBy("middle").where(...)

// non-deterministic relaxed contiguity
val nonDetermin: Pattern[Event, _] = start.followedByAny("middle").where(...)

// NOT pattern with strict contiguity
val strictNot: Pattern[Event, _] = start.notNext("not").where(...)

// NOT pattern with relaxed contiguity
val relaxedNot: Pattern[Event, _] = start.notFollowedBy("not").where(...)
`

Relaxed contiguity means that only the first succeeding matching event will be matched, while
with non-deterministic relaxed contiguity, multiple matches will be emitted for the same beginning. As an example,
a pattern "a b", given the event sequence "a", "c", "b1", "b2", will give the following results:

`"a b"`
`"a", "c", "b1", "b2"`
1. 
Strict Contiguity between "a" and "b": {} (no match), the "c" after "a" causes "a" to be discarded.

2. 
Relaxed Contiguity between "a" and "b": {a b1}, as relaxed continuity is viewed as “skip non-matching events
till the next matching one”.

3. 
Non-Deterministic Relaxed Contiguity between "a" and "b": {a b1}, {a b2}, as this is the most general form.


Strict Contiguity between "a" and "b": {} (no match), the "c" after "a" causes "a" to be discarded.

`"a"`
`"b"`
`{}`
`"c"`
`"a"`
`"a"`

Relaxed Contiguity between "a" and "b": {a b1}, as relaxed continuity is viewed as “skip non-matching events
till the next matching one”.

`"a"`
`"b"`
`{a b1}`

Non-Deterministic Relaxed Contiguity between "a" and "b": {a b1}, {a b2}, as this is the most general form.

`"a"`
`"b"`
`{a b1}`
`{a b2}`

It’s also possible to define a temporal constraint for the pattern to be valid.
For example, you can define that a pattern should occur within 10 seconds via the pattern.within() method.
Temporal patterns are supported for both processing and event time.

`pattern.within()`

> 
  A pattern sequence can only have one temporal constraint. If multiple such constraints are defined on different individual patterns, then the smallest is applied.



```
next.within(Duration.ofSeconds(10));

```

`next.within(Duration.ofSeconds(10));
`

```
next.within(Duration.ofSeconds(10))

```

`next.within(Duration.ofSeconds(10))
`

Notice that a pattern sequence can end with notFollowedBy() with temporal constraint
E.g. a pattern like:

`notFollowedBy()`

```
Pattern.<Event>begin("start")
    .next("middle")
    .where(SimpleCondition.of(value -> value.getName().equals("a")))
    .notFollowedBy("end")
    .where(SimpleCondition.of(value -> value.getName().equals("b")))
    .within(Duration.ofSeconds(10));

```

`Pattern.<Event>begin("start")
    .next("middle")
    .where(SimpleCondition.of(value -> value.getName().equals("a")))
    .notFollowedBy("end")
    .where(SimpleCondition.of(value -> value.getName().equals("b")))
    .within(Duration.ofSeconds(10));
`

```
Pattern.begin("start").where(_.getName().equals("a"))
.notFollowedBy("end").where(_.getName == "b")
.within(Duration.ofSeconds(10))

```

`Pattern.begin("start").where(_.getName().equals("a"))
.notFollowedBy("end").where(_.getName == "b")
.within(Duration.ofSeconds(10))
`

#### Contiguity within looping patterns#


You can apply the same contiguity condition as discussed in the previous section within a looping pattern.
The contiguity will be applied between elements accepted into such a pattern.
To illustrate the above with an example, a pattern sequence "a b+ c" ("a" followed by any(non-deterministic relaxed) sequence of one or more "b"’s followed by a "c") with
input "a", "b1", "d1", "b2", "d2", "b3" "c" will have the following results:

`"a b+ c"`
`"a"`
`"b"`
`"c"`
`"a", "b1", "d1", "b2", "d2", "b3" "c"`
1. 
Strict Contiguity: {a b1 c}, {a b2 c}, {a b3 c} - there are no adjacent "b"s.

2. 
Relaxed Contiguity: {a b1 c}, {a b1 b2 c}, {a b1 b2 b3 c}, {a b2 c}, {a b2 b3 c}, {a b3 c} - "d"’s are ignored.

3. 
Non-Deterministic Relaxed Contiguity: {a b1 c}, {a b1 b2 c}, {a b1 b3 c}, {a b1 b2 b3 c}, {a b2 c}, {a b2 b3 c}, {a b3 c} -
notice the {a b1 b3 c}, which is the result of relaxing contiguity between "b"’s.


Strict Contiguity: {a b1 c}, {a b2 c}, {a b3 c} - there are no adjacent "b"s.

`{a b1 c}`
`{a b2 c}`
`{a b3 c}`
`"b"`

Relaxed Contiguity: {a b1 c}, {a b1 b2 c}, {a b1 b2 b3 c}, {a b2 c}, {a b2 b3 c}, {a b3 c} - "d"’s are ignored.

`{a b1 c}`
`{a b1 b2 c}`
`{a b1 b2 b3 c}`
`{a b2 c}`
`{a b2 b3 c}`
`{a b3 c}`
`"d"`

Non-Deterministic Relaxed Contiguity: {a b1 c}, {a b1 b2 c}, {a b1 b3 c}, {a b1 b2 b3 c}, {a b2 c}, {a b2 b3 c}, {a b3 c} -
notice the {a b1 b3 c}, which is the result of relaxing contiguity between "b"’s.

`{a b1 c}`
`{a b1 b2 c}`
`{a b1 b3 c}`
`{a b1 b2 b3 c}`
`{a b2 c}`
`{a b2 b3 c}`
`{a b3 c}`
`{a b1 b3 c}`
`"b"`

For looping patterns (e.g. oneOrMore() and times()) the default is relaxed contiguity. If you want
strict contiguity, you have to explicitly specify it by using the consecutive() call, and if you want
non-deterministic relaxed contiguity you can use the allowCombinations() call.

`oneOrMore()`
`times()`
`consecutive()`
`allowCombinations()`

#### consecutive()#

`consecutive()`

Works in conjunction with oneOrMore() and times() and imposes strict contiguity between the matching
events, i.e. any non-matching element breaks the match (as in next()).
If not applied a relaxed contiguity (as in followedBy()) is used.

`oneOrMore()`
`times()`
`next()`
`followedBy()`

E.g. a pattern like:


```
Pattern.<Event>begin("start")
    .where(SimpleCondition.of(value -> value.getName().equals("c")))
    .followedBy("middle")
    .where(SimpleCondition.of(value -> value.getName().equals("a")))
    .oneOrMore()
    .consecutive()
    .followedBy("end1")
    .where(SimpleCondition.of(value -> value.getName().equals("b")));

```

`Pattern.<Event>begin("start")
    .where(SimpleCondition.of(value -> value.getName().equals("c")))
    .followedBy("middle")
    .where(SimpleCondition.of(value -> value.getName().equals("a")))
    .oneOrMore()
    .consecutive()
    .followedBy("end1")
    .where(SimpleCondition.of(value -> value.getName().equals("b")));
`

```
Pattern.begin("start").where(_.getName().equals("c"))
  .followedBy("middle").where(_.getName().equals("a"))
                       .oneOrMore().consecutive()
  .followedBy("end1").where(_.getName().equals("b"))

```

`Pattern.begin("start").where(_.getName().equals("c"))
  .followedBy("middle").where(_.getName().equals("a"))
                       .oneOrMore().consecutive()
  .followedBy("end1").where(_.getName().equals("b"))
`

Will generate the following matches for an input sequence: C D A1 A2 A3 D A4 B
with consecutive applied: {C A1 B}, {C A1 A2 B}, {C A1 A2 A3 B}
without consecutive applied: {C A1 B}, {C A1 A2 B}, {C A1 A2 A3 B}, {C A1 A2 A3 A4 B}.

`C D A1 A2 A3 D A4 B`
`{C A1 B}`
`{C A1 A2 B}`
`{C A1 A2 A3 B}`
`{C A1 B}`
`{C A1 A2 B}`
`{C A1 A2 A3 B}`
`{C A1 A2 A3 A4 B}`

#### allowCombinations()#

`allowCombinations()`

Works in conjunction with oneOrMore() and times() and imposes non-deterministic relaxed contiguity
between the matching events (as in followedByAny()).
If not applied a relaxed contiguity (as in followedBy()) is used.

`oneOrMore()`
`times()`
`followedByAny()`
`followedBy()`

E.g. a pattern like:


```
Pattern.<Event>begin("start")
    .where(SimpleCondition.of(value -> value.getName().equals("c")))
    .followedBy("middle")
    .where(SimpleCondition.of(value -> value.getName().equals("a")))
    .oneOrMore()
    .allowCombinations()
    .followedBy("end1")
    .where(SimpleCondition.of(value -> value.getName().equals("b")));

```

`Pattern.<Event>begin("start")
    .where(SimpleCondition.of(value -> value.getName().equals("c")))
    .followedBy("middle")
    .where(SimpleCondition.of(value -> value.getName().equals("a")))
    .oneOrMore()
    .allowCombinations()
    .followedBy("end1")
    .where(SimpleCondition.of(value -> value.getName().equals("b")));
`

```
Pattern.begin("start").where(_.getName().equals("c"))
  .followedBy("middle").where(_.getName().equals("a"))
                       .oneOrMore().allowCombinations()
  .followedBy("end1").where(_.getName().equals("b"))

```

`Pattern.begin("start").where(_.getName().equals("c"))
  .followedBy("middle").where(_.getName().equals("a"))
                       .oneOrMore().allowCombinations()
  .followedBy("end1").where(_.getName().equals("b"))
`

Will generate the following matches for an input sequence: C D A1 A2 A3 D A4 B.
with combinations enabled: {C A1 B}, {C A1 A2 B}, {C A1 A3 B}, {C A1 A4 B}, {C A1 A2 A3 B}, {C A1 A2 A4 B}, {C A1 A3 A4 B}, {C A1 A2 A3 A4 B}
without combinations enabled: {C A1 B}, {C A1 A2 B}, {C A1 A2 A3 B}, {C A1 A2 A3 A4 B}.

`C D A1 A2 A3 D A4 B`
`{C A1 B}`
`{C A1 A2 B}`
`{C A1 A3 B}`
`{C A1 A4 B}`
`{C A1 A2 A3 B}`
`{C A1 A2 A4 B}`
`{C A1 A3 A4 B}`
`{C A1 A2 A3 A4 B}`
`{C A1 B}`
`{C A1 A2 B}`
`{C A1 A2 A3 B}`
`{C A1 A2 A3 A4 B}`

### Groups of patterns#


It’s also possible to define a pattern sequence as the condition for begin, followedBy, followedByAny and
next. The pattern sequence will be considered as the matching condition logically and a GroupPattern will be
returned and it is possible to apply oneOrMore(), times(#ofTimes), times(#fromTimes, #toTimes), optional(),
consecutive(), allowCombinations() to the GroupPattern.

`begin`
`followedBy`
`followedByAny`
`next`
`GroupPattern`
`oneOrMore()`
`times(#ofTimes)`
`times(#fromTimes, #toTimes)`
`optional()`
`consecutive()`
`allowCombinations()`
`GroupPattern`

```

Pattern<Event, ?> start = Pattern.begin(
    Pattern.<Event>begin("start").where(...).followedBy("start_middle").where(...)
);

// strict contiguity
Pattern<Event, ?> strict = start.next(
    Pattern.<Event>begin("next_start").where(...).followedBy("next_middle").where(...)
).times(3);

// relaxed contiguity
Pattern<Event, ?> relaxed = start.followedBy(
    Pattern.<Event>begin("followedby_start").where(...).followedBy("followedby_middle").where(...)
).oneOrMore();

// non-deterministic relaxed contiguity
Pattern<Event, ?> nonDetermin = start.followedByAny(
    Pattern.<Event>begin("followedbyany_start").where(...).followedBy("followedbyany_middle").where(...)
).optional();

```

`
Pattern<Event, ?> start = Pattern.begin(
    Pattern.<Event>begin("start").where(...).followedBy("start_middle").where(...)
);

// strict contiguity
Pattern<Event, ?> strict = start.next(
    Pattern.<Event>begin("next_start").where(...).followedBy("next_middle").where(...)
).times(3);

// relaxed contiguity
Pattern<Event, ?> relaxed = start.followedBy(
    Pattern.<Event>begin("followedby_start").where(...).followedBy("followedby_middle").where(...)
).oneOrMore();

// non-deterministic relaxed contiguity
Pattern<Event, ?> nonDetermin = start.followedByAny(
    Pattern.<Event>begin("followedbyany_start").where(...).followedBy("followedbyany_middle").where(...)
).optional();
`

```

val start: Pattern[Event, _] = Pattern.begin(
    Pattern.begin[Event]("start").where(...).followedBy("start_middle").where(...)
)

// strict contiguity
val strict: Pattern[Event, _] = start.next(
    Pattern.begin[Event]("next_start").where(...).followedBy("next_middle").where(...)
).times(3)

// relaxed contiguity
val relaxed: Pattern[Event, _] = start.followedBy(
    Pattern.begin[Event]("followedby_start").where(...).followedBy("followedby_middle").where(...)
).oneOrMore()

// non-deterministic relaxed contiguity
val nonDetermin: Pattern[Event, _] = start.followedByAny(
    Pattern.begin[Event]("followedbyany_start").where(...).followedBy("followedbyany_middle").where(...)
).optional()

```

`
val start: Pattern[Event, _] = Pattern.begin(
    Pattern.begin[Event]("start").where(...).followedBy("start_middle").where(...)
)

// strict contiguity
val strict: Pattern[Event, _] = start.next(
    Pattern.begin[Event]("next_start").where(...).followedBy("next_middle").where(...)
).times(3)

// relaxed contiguity
val relaxed: Pattern[Event, _] = start.followedBy(
    Pattern.begin[Event]("followedby_start").where(...).followedBy("followedby_middle").where(...)
).oneOrMore()

// non-deterministic relaxed contiguity
val nonDetermin: Pattern[Event, _] = start.followedByAny(
    Pattern.begin[Event]("followedbyany_start").where(...).followedBy("followedbyany_middle").where(...)
).optional()
`

#### begin(#name)#

`begin(#name)`

Defines a starting pattern.


```
Pattern<Event, ?> start = Pattern.<Event>begin("start");

```

`Pattern<Event, ?> start = Pattern.<Event>begin("start");
`

```
val start = Pattern.begin[Event]("start")

```

`val start = Pattern.begin[Event]("start")
`

#### begin(#pattern_sequence)#

`begin(#pattern_sequence)`

Defines a starting pattern


```
Pattern<Event, ?> start = Pattern.<Event>begin(
    Pattern.<Event>begin("start").where(...).followedBy("middle").where(...)
);

```

`Pattern<Event, ?> start = Pattern.<Event>begin(
    Pattern.<Event>begin("start").where(...).followedBy("middle").where(...)
);
`

```
val start = Pattern.begin(
    Pattern.begin[Event]("start").where(...).followedBy("middle").where(...)
)

```

`val start = Pattern.begin(
    Pattern.begin[Event]("start").where(...).followedBy("middle").where(...)
)
`

#### next(#name)#

`next(#name)`

Appends a new pattern. A matching event has to directly succeed the previous matching event (strict contiguity).


```
Pattern<Event, ?> next = start.next("middle");

```

`Pattern<Event, ?> next = start.next("middle");
`

```
val next = start.next("middle")

```

`val next = start.next("middle")
`

#### next(#pattern_sequence)#

`next(#pattern_sequence)`

Appends a new pattern. A sequence of matching events have to directly succeed the previous matching event (strict contiguity).


```
Pattern<Event, ?> next = start.next(
    Pattern.<Event>begin("start").where(...).followedBy("middle").where(...)
);

```

`Pattern<Event, ?> next = start.next(
    Pattern.<Event>begin("start").where(...).followedBy("middle").where(...)
);
`

```
val next = start.next(
    Pattern.begin[Event]("start").where(...).followedBy("middle").where(...)
)

```

`val next = start.next(
    Pattern.begin[Event]("start").where(...).followedBy("middle").where(...)
)
`

#### followedBy(#name)#

`followedBy(#name)`

Appends a new pattern. Other events can occur between a matching event and the previous matching event (relaxed contiguity).


```
Pattern<Event, ?> followedBy = start.followedBy("middle");

```

`Pattern<Event, ?> followedBy = start.followedBy("middle");
`

```
val followedBy = start.followedBy("middle")

```

`val followedBy = start.followedBy("middle")
`

#### followedBy(#pattern_sequence)#

`followedBy(#pattern_sequence)`

Appends a new pattern. Other events can occur between a matching event and the previous matching event (relaxed contiguity).


```
Pattern<Event, ?> followedBy = start.followedBy(
    Pattern.<Event>begin("start").where(...).followedBy("middle").where(...)
);

```

`Pattern<Event, ?> followedBy = start.followedBy(
    Pattern.<Event>begin("start").where(...).followedBy("middle").where(...)
);
`

```
val followedBy = start.followedBy(
    Pattern.begin[Event]("start").where(...).followedBy("middle").where(...)
)

```

`val followedBy = start.followedBy(
    Pattern.begin[Event]("start").where(...).followedBy("middle").where(...)
)
`

#### followedByAny(#name)#

`followedByAny(#name)`

Appends a new pattern. Other events can occur between a matching event and the previous
matching event, and alternative matches will be presented for every alternative matching event
(non-deterministic relaxed contiguity).


```
Pattern<Event, ?> followedByAny = start.followedByAny("middle");

```

`Pattern<Event, ?> followedByAny = start.followedByAny("middle");
`

```
val followedByAny = start.followedByAny("middle")

```

`val followedByAny = start.followedByAny("middle")
`

#### followedByAny(#pattern_sequence)#

`followedByAny(#pattern_sequence)`

Appends a new pattern. Other events can occur between a matching event and the previous
matching event, and alternative matches will be presented for every alternative matching event
(non-deterministic relaxed contiguity).


```
Pattern<Event, ?> next = start.next(
    Pattern.<Event>begin("start").where(...).followedBy("middle").where(...)
);

```

`Pattern<Event, ?> next = start.next(
    Pattern.<Event>begin("start").where(...).followedBy("middle").where(...)
);
`

```
val followedByAny = start.followedByAny(
    Pattern.begin[Event]("start").where(...).followedBy("middle").where(...)
)

```

`val followedByAny = start.followedByAny(
    Pattern.begin[Event]("start").where(...).followedBy("middle").where(...)
)
`

#### notNext()#

`notNext()`

Appends a new negative pattern.
A matching (negative) event has to directly succeed the previous matching event (strict contiguity) for the partial match to be discarded.


```
Pattern<Event, ?> notNext = start.notNext("not");

```

`Pattern<Event, ?> notNext = start.notNext("not");
`

```
val notNext = start.notNext("not")

```

`val notNext = start.notNext("not")
`

#### notFollowedBy()#

`notFollowedBy()`

Appends a new negative pattern. A partial matching event sequence will be discarded even if other events occur between the matching (negative) event and the previous matching event (relaxed contiguity).


```
Pattern<Event, ?> notFollowedBy = start.notFollowedBy("not");

```

`Pattern<Event, ?> notFollowedBy = start.notFollowedBy("not");
`

```
val notFollowedBy = start.notFollowedBy("not")

```

`val notFollowedBy = start.notFollowedBy("not")
`

#### within(time)#

`within(time)`

Defines the maximum time interval for an event sequence to match the pattern.
If a non-completed event sequence exceeds this time, it is discarded.


```
pattern.within(Duration.ofSeconds(10));

```

`pattern.within(Duration.ofSeconds(10));
`

```
pattern.within(Duration.ofSeconds(10))

```

`pattern.within(Duration.ofSeconds(10))
`

### After Match Skip Strategy#


For a given pattern, the same event may be assigned to multiple successful matches. To control to how many matches an event will be assigned, you need to specify the skip strategy called AfterMatchSkipStrategy. There are five types of skip strategies, listed as follows:

`AfterMatchSkipStrategy`
* NO_SKIP: Every possible match will be emitted.
* SKIP_TO_NEXT: Discards every partial match that started with the same event, emitted match was started.
* SKIP_PAST_LAST_EVENT: Discards every partial match that started after the match started but before it ended.
* SKIP_TO_FIRST: Discards every partial match that started after the match started but before the first event of PatternName occurred.
* SKIP_TO_LAST: Discards every partial match that started after the match started but before the last event of PatternName occurred.

Notice that when using SKIP_TO_FIRST and SKIP_TO_LAST skip strategy, a valid PatternName should also be specified.


For example, for a given pattern b+ c and a data stream b1 b2 b3 c, the differences between these four skip strategies are as follows:

`b+ c`
`b1 b2 b3 c`
`b1 b2 b3 c`
`b2 b3 c`
`b3 c`
`b1 b2 b3 c`
`b1 b2 b3 c`
`b2 b3 c`
`b3 c`
`b1 b2 b3 c`
`b1 b2 b3 c`
`b1 b2 b3 c`
`b`
`b1 b2 b3 c`
`b2 b3 c`
`b3 c`
`b1 b2 b3 c`
`b1`
`b`
`b1 b2 b3 c`
`b3 c`
`b1 b2 b3 c`
`b3`
`b2 b3 c`

Have a look also at another example to better see the difference between NO_SKIP and SKIP_TO_FIRST:
Pattern: (a | b | c) (b | c) c+.greedy d and sequence: a b c1 c2 c3 d Then the results will be:

`(a | b | c) (b | c) c+.greedy d`
`a b c1 c2 c3 d`
`a b c1 c2 c3 d`
`b c1 c2 c3 d`
`c1 c2 c3 d`
`a b c1 c2 c3 d`
`c*`
`a b c1 c2 c3 d`
`c1 c2 c3 d`
`a b c1 c2 c3 d`
`c1`
`b c1 c2 c3 d`

To better understand the difference between NO_SKIP and SKIP_TO_NEXT take a look at following example:
Pattern: a b+ and sequence: a b1 b2 b3 Then the results will be:

`a b+`
`a b1 b2 b3`
`a b1`
`a b1 b2`
`a b1 b2 b3`
`a b1`
`a b1`
`a b1`
`a`
`a b1 b2`
`a b1 b2 b3`

To specify which skip strategy to use, just create an AfterMatchSkipStrategy by calling:

`AfterMatchSkipStrategy`
`AfterMatchSkipStrategy.noSkip()`
`AfterMatchSkipStrategy.skipToNext()`
`AfterMatchSkipStrategy.skipPastLastEvent()`
`AfterMatchSkipStrategy.skipToFirst(patternName)`
`AfterMatchSkipStrategy.skipToLast(patternName)`

Then apply the skip strategy to a pattern by calling:


```
AfterMatchSkipStrategy skipStrategy = ...;
Pattern.begin("patternName", skipStrategy);

```

`AfterMatchSkipStrategy skipStrategy = ...;
Pattern.begin("patternName", skipStrategy);
`

```
val skipStrategy = ...
Pattern.begin("patternName", skipStrategy)

```

`val skipStrategy = ...
Pattern.begin("patternName", skipStrategy)
`

> 
  For SKIP_TO_FIRST/LAST there are two options how to handle cases when there are no events mapped to the PatternName. By default a NO_SKIP strategy will be used in this case. The other option is to throw exception in such situation.
One can enable this option by:


`SKIP_TO_FIRST`
`LAST`

```
AfterMatchSkipStrategy.skipToFirst(patternName).throwExceptionOnMiss();

```

`AfterMatchSkipStrategy.skipToFirst(patternName).throwExceptionOnMiss();
`

```
AfterMatchSkipStrategy.skipToFirst(patternName).throwExceptionOnMiss()

```

`AfterMatchSkipStrategy.skipToFirst(patternName).throwExceptionOnMiss()
`

## Detecting Patterns#


After specifying the pattern sequence you are looking for, it is time to apply it to your input stream to detect
potential matches. To run a stream of events against your pattern sequence, you have to create a PatternStream.
Given an input stream input, a pattern pattern and an optional comparator comparator used to sort events with the same timestamp in case of EventTime or that arrived at the same moment, you create the PatternStream by calling:

`PatternStream`
`input`
`pattern`
`comparator`
`PatternStream`

```
DataStream<Event> input = ...;
Pattern<Event, ?> pattern = ...;
EventComparator<Event> comparator = ...; // optional

PatternStream<Event> patternStream = CEP.pattern(input, pattern, comparator);

```

`DataStream<Event> input = ...;
Pattern<Event, ?> pattern = ...;
EventComparator<Event> comparator = ...; // optional

PatternStream<Event> patternStream = CEP.pattern(input, pattern, comparator);
`

```
val input : DataStream[Event] = ...
val pattern : Pattern[Event, _] = ...
var comparator : EventComparator[Event] = ... // optional

val patternStream: PatternStream[Event] = CEP.pattern(input, pattern, comparator)

```

`val input : DataStream[Event] = ...
val pattern : Pattern[Event, _] = ...
var comparator : EventComparator[Event] = ... // optional

val patternStream: PatternStream[Event] = CEP.pattern(input, pattern, comparator)
`

The input stream can be keyed or non-keyed depending on your use-case.


> 
  Applying your pattern on a non-keyed stream will result in a job with parallelism equal to 1.



### Selecting from Patterns#


Once you have obtained a PatternStream you can apply transformation to detected event sequences. The suggested way of doing that
is by PatternProcessFunction.

`PatternStream`
`PatternProcessFunction`

A PatternProcessFunction has a processMatch method which is called for each matching event sequence.
It receives a match in the form of Map<String, List<IN>> where the key is the name of each pattern in your pattern
sequence and the value is a list of all accepted events for that pattern (IN is the type of your input elements).
The events for a given pattern are ordered by timestamp. The reason for returning a list of accepted events for each
pattern is that when using looping patterns (e.g. oneToMany() and times()), more than one event may be accepted for a given pattern.

`PatternProcessFunction`
`processMatch`
`Map<String, List<IN>>`
`IN`
`oneToMany()`
`times()`

```
class MyPatternProcessFunction<IN, OUT> extends PatternProcessFunction<IN, OUT> {
    @Override
    public void processMatch(Map<String, List<IN>> match, Context ctx, Collector<OUT> out) throws Exception;
        IN startEvent = match.get("start").get(0);
        IN endEvent = match.get("end").get(0);
        out.collect(OUT(startEvent, endEvent));
    }
}

```

`class MyPatternProcessFunction<IN, OUT> extends PatternProcessFunction<IN, OUT> {
    @Override
    public void processMatch(Map<String, List<IN>> match, Context ctx, Collector<OUT> out) throws Exception;
        IN startEvent = match.get("start").get(0);
        IN endEvent = match.get("end").get(0);
        out.collect(OUT(startEvent, endEvent));
    }
}
`

The PatternProcessFunction gives access to a Context object. Thanks to it, one can access time related
characteristics such as currentProcessingTime or timestamp of current match (which is the timestamp of the last element assigned to the match).
For more info see Time context.
Through this context one can also emit results to a side-output.

`PatternProcessFunction`
`Context`
`currentProcessingTime`
`timestamp`

#### Handling Timed Out Partial Patterns#


Whenever a pattern has a window length attached via the within keyword, it is possible that partial event sequences
are discarded because they exceed the window length. To act upon a timed out partial match one can use TimedOutPartialMatchHandler interface.
The interface is supposed to be used in a mixin style. This mean you can additionally implement this interface with your PatternProcessFunction.
The TimedOutPartialMatchHandler provides the additional processTimedOutMatch method which will be called for every timed out partial match.

`within`
`TimedOutPartialMatchHandler`
`PatternProcessFunction`
`TimedOutPartialMatchHandler`
`processTimedOutMatch`

```
class MyPatternProcessFunction<IN, OUT> extends PatternProcessFunction<IN, OUT> implements TimedOutPartialMatchHandler<IN> {
    @Override
    public void processMatch(Map<String, List<IN>> match, Context ctx, Collector<OUT> out) throws Exception;
        ...
    }

    @Override
    public void processTimedOutMatch(Map<String, List<IN>> match, Context ctx) throws Exception;
        IN startEvent = match.get("start").get(0);
        ctx.output(outputTag, T(startEvent));
    }
}

```

`class MyPatternProcessFunction<IN, OUT> extends PatternProcessFunction<IN, OUT> implements TimedOutPartialMatchHandler<IN> {
    @Override
    public void processMatch(Map<String, List<IN>> match, Context ctx, Collector<OUT> out) throws Exception;
        ...
    }

    @Override
    public void processTimedOutMatch(Map<String, List<IN>> match, Context ctx) throws Exception;
        IN startEvent = match.get("start").get(0);
        ctx.output(outputTag, T(startEvent));
    }
}
`

Note The processTimedOutMatch does not give one access to the main output. You can still emit results
through side-outputs though, through the Context object.

`processTimedOutMatch`
`Context`

#### Convenience API#


The aforementioned PatternProcessFunction was introduced in Flink 1.8 and since then it is the recommended way to interact with matches.
One can still use the old style API like select/flatSelect, which internally will be translated into a PatternProcessFunction.

`PatternProcessFunction`
`select`
`flatSelect`
`PatternProcessFunction`

```
PatternStream<Event> patternStream = CEP.pattern(input, pattern);

OutputTag<String> outputTag = new OutputTag<String>("side-output"){};

SingleOutputStreamOperator<ComplexEvent> flatResult = patternStream.flatSelect(
    outputTag,
    new PatternFlatTimeoutFunction<Event, TimeoutEvent>() {
        public void timeout(
                Map<String, List<Event>> pattern,
                long timeoutTimestamp,
                Collector<TimeoutEvent> out) throws Exception {
            out.collect(new TimeoutEvent());
        }
    },
    new PatternFlatSelectFunction<Event, ComplexEvent>() {
        public void flatSelect(Map<String, List<IN>> pattern, Collector<OUT> out) throws Exception {
            out.collect(new ComplexEvent());
        }
    }
);

DataStream<TimeoutEvent> timeoutFlatResult = flatResult.getSideOutput(outputTag);

```

`PatternStream<Event> patternStream = CEP.pattern(input, pattern);

OutputTag<String> outputTag = new OutputTag<String>("side-output"){};

SingleOutputStreamOperator<ComplexEvent> flatResult = patternStream.flatSelect(
    outputTag,
    new PatternFlatTimeoutFunction<Event, TimeoutEvent>() {
        public void timeout(
                Map<String, List<Event>> pattern,
                long timeoutTimestamp,
                Collector<TimeoutEvent> out) throws Exception {
            out.collect(new TimeoutEvent());
        }
    },
    new PatternFlatSelectFunction<Event, ComplexEvent>() {
        public void flatSelect(Map<String, List<IN>> pattern, Collector<OUT> out) throws Exception {
            out.collect(new ComplexEvent());
        }
    }
);

DataStream<TimeoutEvent> timeoutFlatResult = flatResult.getSideOutput(outputTag);
`

```

val patternStream: PatternStream[Event] = CEP.pattern(input, pattern)

val outputTag = OutputTag[String]("side-output")

val result: SingleOutputStreamOperator[ComplexEvent] = patternStream.flatSelect(outputTag){
    (pattern: Map[String, Iterable[Event]], timestamp: Long, out: Collector[TimeoutEvent]) =>
        out.collect(TimeoutEvent())
} {
    (pattern: mutable.Map[String, Iterable[Event]], out: Collector[ComplexEvent]) =>
        out.collect(ComplexEvent())
}

val timeoutResult: DataStream[TimeoutEvent] = result.getSideOutput(outputTag)

```

`
val patternStream: PatternStream[Event] = CEP.pattern(input, pattern)

val outputTag = OutputTag[String]("side-output")

val result: SingleOutputStreamOperator[ComplexEvent] = patternStream.flatSelect(outputTag){
    (pattern: Map[String, Iterable[Event]], timestamp: Long, out: Collector[TimeoutEvent]) =>
        out.collect(TimeoutEvent())
} {
    (pattern: mutable.Map[String, Iterable[Event]], out: Collector[ComplexEvent]) =>
        out.collect(ComplexEvent())
}

val timeoutResult: DataStream[TimeoutEvent] = result.getSideOutput(outputTag)
`

## Time in CEP library#


### Handling Lateness in Event Time#


In CEP the order in which elements are processed matters. To guarantee that elements are processed in the correct order when working in event time, an incoming element is initially put in a buffer where elements are sorted in ascending order based on their timestamp, and when a watermark arrives, all the elements in this buffer with timestamps smaller than that of the watermark are processed. This implies that elements between watermarks are processed in event-time order.

`CEP`

> 
  The library assumes correctness of the watermark when working in event time.



To guarantee that elements across watermarks are processed in event-time order, Flink’s CEP library assumes
correctness of the watermark, and considers as late elements whose timestamp is smaller than that of the last
seen watermark. Late elements are not further processed. Also, you can specify a sideOutput tag to collect the late elements come after the last seen watermark, you can use it like this.


```
PatternStream<Event> patternStream = CEP.pattern(input, pattern);

OutputTag<String> lateDataOutputTag = new OutputTag<String>("late-data"){};

SingleOutputStreamOperator<ComplexEvent> result = patternStream
    .sideOutputLateData(lateDataOutputTag)
    .select(
        new PatternSelectFunction<Event, ComplexEvent>() {...}
    );

DataStream<String> lateData = result.getSideOutput(lateDataOutputTag);

```

`PatternStream<Event> patternStream = CEP.pattern(input, pattern);

OutputTag<String> lateDataOutputTag = new OutputTag<String>("late-data"){};

SingleOutputStreamOperator<ComplexEvent> result = patternStream
    .sideOutputLateData(lateDataOutputTag)
    .select(
        new PatternSelectFunction<Event, ComplexEvent>() {...}
    );

DataStream<String> lateData = result.getSideOutput(lateDataOutputTag);
`

```

val patternStream: PatternStream[Event] = CEP.pattern(input, pattern)

val lateDataOutputTag = OutputTag[String]("late-data")

val result: SingleOutputStreamOperator[ComplexEvent] = patternStream
      .sideOutputLateData(lateDataOutputTag)
      .select{
          pattern: Map[String, Iterable[ComplexEvent]] => ComplexEvent()
      }

val lateData: DataStream[String] = result.getSideOutput(lateDataOutputTag)

```

`
val patternStream: PatternStream[Event] = CEP.pattern(input, pattern)

val lateDataOutputTag = OutputTag[String]("late-data")

val result: SingleOutputStreamOperator[ComplexEvent] = patternStream
      .sideOutputLateData(lateDataOutputTag)
      .select{
          pattern: Map[String, Iterable[ComplexEvent]] => ComplexEvent()
      }

val lateData: DataStream[String] = result.getSideOutput(lateDataOutputTag)
`

### Time context#


In PatternProcessFunction as well as in IterativeCondition user has access to a context
that implements TimeContext as follows:

`TimeContext`

```
/**
 * Enables access to time related characteristics such as current processing time or timestamp of
 * currently processed element. Used in {@link PatternProcessFunction} and
 * {@link org.apache.flink.cep.pattern.conditions.IterativeCondition}
 */
@PublicEvolving
public interface TimeContext {

	/**
	 * Timestamp of the element currently being processed.
	 *
	 * <p>In case of {@link org.apache.flink.streaming.api.TimeCharacteristic#ProcessingTime} this
	 * will be set to the time when event entered the cep operator.
	 */
	long timestamp();

	/** Returns the current processing time. */
	long currentProcessingTime();
}

```

`/**
 * Enables access to time related characteristics such as current processing time or timestamp of
 * currently processed element. Used in {@link PatternProcessFunction} and
 * {@link org.apache.flink.cep.pattern.conditions.IterativeCondition}
 */
@PublicEvolving
public interface TimeContext {

	/**
	 * Timestamp of the element currently being processed.
	 *
	 * <p>In case of {@link org.apache.flink.streaming.api.TimeCharacteristic#ProcessingTime} this
	 * will be set to the time when event entered the cep operator.
	 */
	long timestamp();

	/** Returns the current processing time. */
	long currentProcessingTime();
}
`

This context gives user access to time characteristics of processed events (incoming records in case of IterativeCondition and matches in case of PatternProcessFunction).
Call to TimeContext#currentProcessingTime always gives you the value of current processing time and this call should be preferred to e.g. calling System.currentTimeMillis().

`IterativeCondition`
`PatternProcessFunction`
`TimeContext#currentProcessingTime`
`System.currentTimeMillis()`

In case of TimeContext#timestamp() the returned value is equal to assigned timestamp in case of EventTime. In ProcessingTime this will equal to the point of time when said event entered
cep operator (or when the match was generated in case of PatternProcessFunction). This means that the value will be consistent across multiple calls to that method.

`TimeContext#timestamp()`
`EventTime`
`ProcessingTime`
`PatternProcessFunction`

## Optional Configuration#


Options to configure the cache capacity of Flink CEP SharedBuffer.
It could accelerate the CEP operate process speed and limit the number of elements of cache in pure memory.

`SharedBuffer`

Note It’s only effective to limit usage of memory when state.backend.type was set as rocksdb, which would transport the elements exceeded the number of the cache into the rocksdb state storage instead of memory state storage.
The configuration items are helpful for memory limitation when the state.backend.type is set as rocksdb. By contrastï¼when the state.backend.type is set as not rocksdb, the cache would cause performance decreased. Compared with old cache implemented with Map, the state part will contain more elements swapped out from new guava-cache, which would make it heavier to copy on write for state.

`state.backend.type`
`rocksdb`
`state.backend.type`
`state.backend.type`
`rocksdb`
`Map`
`copy on write`

##### pipeline.cep.sharedbuffer.cache.entry-slots


##### pipeline.cep.sharedbuffer.cache.event-slots


##### pipeline.cep.sharedbuffer.cache.statistics-interval


## Examples#


The following example detects the pattern start, middle(name = "error") -> end(name = "critical") on a keyed data
stream of Events. The events are keyed by their ids and a valid pattern has to occur within 10 seconds.
The whole processing is done with event time.

`start, middle(name = "error") -> end(name = "critical")`
`Events`
`id`

```
StreamExecutionEnvironment env = ...;

DataStream<Event> input = ...;

DataStream<Event> partitionedInput = input.keyBy(new KeySelector<Event, Integer>() {
	@Override
	public Integer getKey(Event value) throws Exception {
		return value.getId();
	}
});

Pattern<Event, ?> pattern = Pattern.<Event>begin("start")
    .next("middle")
    .where(SimpleCondition.of(value -> value.getName().equals("error")))
    .followedBy("end")
    .where(SimpleCondition.of(value -> value.getName().equals("critical")))
    .within(Duration.ofSeconds(10));

PatternStream<Event> patternStream = CEP.pattern(partitionedInput, pattern);

DataStream<Alert> alerts = patternStream.select(new PatternSelectFunction<Event, Alert>() {
	@Override
	public Alert select(Map<String, List<Event>> pattern) throws Exception {
		return createAlert(pattern);
	}
});

```

`StreamExecutionEnvironment env = ...;

DataStream<Event> input = ...;

DataStream<Event> partitionedInput = input.keyBy(new KeySelector<Event, Integer>() {
	@Override
	public Integer getKey(Event value) throws Exception {
		return value.getId();
	}
});

Pattern<Event, ?> pattern = Pattern.<Event>begin("start")
    .next("middle")
    .where(SimpleCondition.of(value -> value.getName().equals("error")))
    .followedBy("end")
    .where(SimpleCondition.of(value -> value.getName().equals("critical")))
    .within(Duration.ofSeconds(10));

PatternStream<Event> patternStream = CEP.pattern(partitionedInput, pattern);

DataStream<Alert> alerts = patternStream.select(new PatternSelectFunction<Event, Alert>() {
	@Override
	public Alert select(Map<String, List<Event>> pattern) throws Exception {
		return createAlert(pattern);
	}
});
`

```
val env : StreamExecutionEnvironment = ...

val input : DataStream[Event] = ...

val partitionedInput = input.keyBy(event => event.getId)

val pattern = Pattern.begin[Event]("start")
  .next("middle").where(_.getName == "error")
  .followedBy("end").where(_.getName == "critical")
  .within(Duration.ofSeconds(10))

val patternStream = CEP.pattern(partitionedInput, pattern)

val alerts = patternStream.select(createAlert(_))

```

`val env : StreamExecutionEnvironment = ...

val input : DataStream[Event] = ...

val partitionedInput = input.keyBy(event => event.getId)

val pattern = Pattern.begin[Event]("start")
  .next("middle").where(_.getName == "error")
  .followedBy("end").where(_.getName == "critical")
  .within(Duration.ofSeconds(10))

val patternStream = CEP.pattern(partitionedInput, pattern)

val alerts = patternStream.select(createAlert(_))
`

## Migrating from an older Flink version(pre 1.5)#


### Migrating from Flink <= 1.5#


In Flink 1.13 we dropped direct savepoint backward compatibility with Flink <= 1.5. If you want to restore
from a savepoint taken from an older version, migrate it first to a newer version (1.6-1.12), take a savepoint
and then use that savepoint to restore with Flink >= 1.13.


 Back to top
