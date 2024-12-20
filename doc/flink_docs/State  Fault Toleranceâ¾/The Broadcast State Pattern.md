# The Broadcast State Pattern


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# The Broadcast State Pattern#


In this section you will learn about how to use broadcast state in practise. Please refer to Stateful Stream
Processing
to learn about the concepts behind stateful stream processing.


## Provided APIs#


To show the provided APIs, we will start with an example before presenting their full functionality. As our running
example, we will use the case where we have a stream of objects of different colors and shapes and we want to find pairs
of objects of the same color that follow a certain pattern, e.g. a rectangle followed by a triangle. We assume that
the set of interesting patterns evolves over time.


In this example, the first stream will contain elements of type Item with a Color and a Shape property. The other
stream will contain the Rules.

`Item`
`Color`
`Shape`
`Rules`

Starting from the stream of Items, we just need to key it by Color, as we want pairs of the same color. This will
make sure that elements of the same color end up on the same physical machine.

`Items`
`Color`

```
// key the items by color
KeyedStream<Item, Color> colorPartitionedStream = itemStream
                        .keyBy(new KeySelector<Item, Color>(){...});

```

`// key the items by color
KeyedStream<Item, Color> colorPartitionedStream = itemStream
                        .keyBy(new KeySelector<Item, Color>(){...});
`

```
# key the items by color
color_partitioned_stream = item_stream.key_by(lambda item: ...)

```

`# key the items by color
color_partitioned_stream = item_stream.key_by(lambda item: ...)
`

Moving on to the Rules, the stream containing them should be broadcasted to all downstream tasks, and these tasks
should store them locally so that they can evaluate them against all incoming Items. The snippet below will i) broadcast
the stream of rules and ii) using the provided MapStateDescriptor, it will create the broadcast state where the rules
will be stored.

`Rules`
`Items`
`MapStateDescriptor`

```

// a map descriptor to store the name of the rule (string) and the rule itself.
MapStateDescriptor<String, Rule> ruleStateDescriptor = new MapStateDescriptor<>(
			"RulesBroadcastState",
			BasicTypeInfo.STRING_TYPE_INFO,
			TypeInformation.of(new TypeHint<Rule>() {}));
		
// broadcast the rules and create the broadcast state
BroadcastStream<Rule> ruleBroadcastStream = ruleStream
                        .broadcast(ruleStateDescriptor);

```

`
// a map descriptor to store the name of the rule (string) and the rule itself.
MapStateDescriptor<String, Rule> ruleStateDescriptor = new MapStateDescriptor<>(
			"RulesBroadcastState",
			BasicTypeInfo.STRING_TYPE_INFO,
			TypeInformation.of(new TypeHint<Rule>() {}));
		
// broadcast the rules and create the broadcast state
BroadcastStream<Rule> ruleBroadcastStream = ruleStream
                        .broadcast(ruleStateDescriptor);
`

```
# a map descriptor to store the name of the rule (string) and the rule (Python object) itself.
rule_state_descriptor = MapStateDescriptor("RuleBroadcastState", Types.STRING(), Types.PICKLED_BYTE_ARRAY())

# broadcast the rules and create the broadcast state
rule_broadcast_stream = rule_stream.broadcast(rule_state_descriptor)

```

`# a map descriptor to store the name of the rule (string) and the rule (Python object) itself.
rule_state_descriptor = MapStateDescriptor("RuleBroadcastState", Types.STRING(), Types.PICKLED_BYTE_ARRAY())

# broadcast the rules and create the broadcast state
rule_broadcast_stream = rule_stream.broadcast(rule_state_descriptor)
`

Finally, in order to evaluate the Rules against the incoming elements from the Item stream, we need to:

`Rules`
`Item`
1. connect the two streams, and
2. specify our match detecting logic.

Connecting a stream (keyed or non-keyed) with a BroadcastStream can be done by calling connect() on the
non-broadcasted stream, with the BroadcastStream as an argument. This will return a BroadcastConnectedStream, on
which we can call process() with a special type of CoProcessFunction. The function will contain our matching logic.
The exact type of the function depends on the type of the non-broadcasted stream:

`BroadcastStream`
`connect()`
`BroadcastStream`
`BroadcastConnectedStream`
`process()`
`CoProcessFunction`
* if that is keyed, then the function is a KeyedBroadcastProcessFunction.
* if it is non-keyed, the function is a BroadcastProcessFunction.
`KeyedBroadcastProcessFunction`
`BroadcastProcessFunction`

Given that our non-broadcasted stream is keyed, the following snippet includes the above calls:


> 
  The connect should be called on the non-broadcasted stream, with the BroadcastStream as an argument.



```
DataStream<String> output = colorPartitionedStream
                 .connect(ruleBroadcastStream)
                 .process(
                     
                     // type arguments in our KeyedBroadcastProcessFunction represent: 
                     //   1. the key of the keyed stream
                     //   2. the type of elements in the non-broadcast side
                     //   3. the type of elements in the broadcast side
                     //   4. the type of the result, here a string
                     
                     new KeyedBroadcastProcessFunction<Color, Item, Rule, String>() {
                         // my matching logic
                     }
                 );

```

`DataStream<String> output = colorPartitionedStream
                 .connect(ruleBroadcastStream)
                 .process(
                     
                     // type arguments in our KeyedBroadcastProcessFunction represent: 
                     //   1. the key of the keyed stream
                     //   2. the type of elements in the non-broadcast side
                     //   3. the type of elements in the broadcast side
                     //   4. the type of the result, here a string
                     
                     new KeyedBroadcastProcessFunction<Color, Item, Rule, String>() {
                         // my matching logic
                     }
                 );
`

```
class MyKeyedBroadcastProcessFunction(KeyedBroadcastProcessFunction):
    # my matching logic
    ...

output = color_partitioned_stream \
    .connect(rule_broadcast_stream) \
    .process(MyKeyedBroadcastProcessFunction())

```

`class MyKeyedBroadcastProcessFunction(KeyedBroadcastProcessFunction):
    # my matching logic
    ...

output = color_partitioned_stream \
    .connect(rule_broadcast_stream) \
    .process(MyKeyedBroadcastProcessFunction())
`

### BroadcastProcessFunction and KeyedBroadcastProcessFunction#


As in the case of a CoProcessFunction, these functions have two process methods to implement; the processBroadcastElement()
which is responsible for processing incoming elements in the broadcasted stream and the processElement() which is used
for the non-broadcasted one. The full signatures of the methods are presented below:

`CoProcessFunction`
`processBroadcastElement()`
`processElement()`

```
public abstract class BroadcastProcessFunction<IN1, IN2, OUT> extends BaseBroadcastProcessFunction {

    public abstract void processElement(IN1 value, ReadOnlyContext ctx, Collector<OUT> out) throws Exception;

    public abstract void processBroadcastElement(IN2 value, Context ctx, Collector<OUT> out) throws Exception;
}

```

`public abstract class BroadcastProcessFunction<IN1, IN2, OUT> extends BaseBroadcastProcessFunction {

    public abstract void processElement(IN1 value, ReadOnlyContext ctx, Collector<OUT> out) throws Exception;

    public abstract void processBroadcastElement(IN2 value, Context ctx, Collector<OUT> out) throws Exception;
}
`

```
public abstract class KeyedBroadcastProcessFunction<KS, IN1, IN2, OUT> {

    public abstract void processElement(IN1 value, ReadOnlyContext ctx, Collector<OUT> out) throws Exception;

    public abstract void processBroadcastElement(IN2 value, Context ctx, Collector<OUT> out) throws Exception;

    public void onTimer(long timestamp, OnTimerContext ctx, Collector<OUT> out) throws Exception;
}

```

`public abstract class KeyedBroadcastProcessFunction<KS, IN1, IN2, OUT> {

    public abstract void processElement(IN1 value, ReadOnlyContext ctx, Collector<OUT> out) throws Exception;

    public abstract void processBroadcastElement(IN2 value, Context ctx, Collector<OUT> out) throws Exception;

    public void onTimer(long timestamp, OnTimerContext ctx, Collector<OUT> out) throws Exception;
}
`

```
class BroadcastProcessFunction(BaseBroadcastProcessFunction, Generic[IN1, IN2, OUT]):

    @abstractmethod
    def process_element(value: IN1, ctx: ReadOnlyContext):
        pass
    
    @abstractmethod
    def process_broadcast_element(value: IN2, ctx: Context):
        pass

```

`class BroadcastProcessFunction(BaseBroadcastProcessFunction, Generic[IN1, IN2, OUT]):

    @abstractmethod
    def process_element(value: IN1, ctx: ReadOnlyContext):
        pass
    
    @abstractmethod
    def process_broadcast_element(value: IN2, ctx: Context):
        pass
`

```
class KeyedBroadcastProcessFunction(BaseBrodcastProcessFunction, Generic[KEY, IN1, IN2, OUT]):

    @abstractmethod
    def process_element(value: IN1, ctx: ReadOnlyContext):
        pass
    
    @abstractmethod
    def process_broadcast_element(value: IN2, ctx: Context):
        pass
    
    def on_timer(timestamp: int, ctx: OnTimerContext):
        pass

```

`class KeyedBroadcastProcessFunction(BaseBrodcastProcessFunction, Generic[KEY, IN1, IN2, OUT]):

    @abstractmethod
    def process_element(value: IN1, ctx: ReadOnlyContext):
        pass
    
    @abstractmethod
    def process_broadcast_element(value: IN2, ctx: Context):
        pass
    
    def on_timer(timestamp: int, ctx: OnTimerContext):
        pass
`

The first thing to notice is that both functions require the implementation of the processBroadcastElement() method
for processing elements in the broadcast side and the processElement() for elements in the non-broadcasted side.

`processBroadcastElement()`
`processElement()`

The two methods differ in the context they are provided. The non-broadcast side has a ReadOnlyContext, while the
broadcasted side has a Context.

`ReadOnlyContext`
`Context`

Both of these contexts (ctx in the following enumeration):

`ctx`
1. give access to the broadcast state: ctx.getBroadcastState(MapStateDescriptor<K, V> stateDescriptor)
2. allow to query the timestamp of the element: ctx.timestamp(),
3. get the current watermark: ctx.currentWatermark()
4. get the current processing time: ctx.currentProcessingTime(), and
5. emit elements to side-outputs: ctx.output(OutputTag<X> outputTag, X value).
`ctx.getBroadcastState(MapStateDescriptor<K, V> stateDescriptor)`
`ctx.timestamp()`
`ctx.currentWatermark()`
`ctx.currentProcessingTime()`
`ctx.output(OutputTag<X> outputTag, X value)`
1. give access to the broadcast state: ctx.get_broadcast_state(state_descriptor: MapStateDescriptor)
2. allow to query the timestamp of the element: ctx.timestamp(),
3. get the current watermark: ctx.current_watermark()
4. get the current processing time: ctx.current_processing_time(), and
5. emit elements to side-outputs: yield output_tag, value.
`ctx.get_broadcast_state(state_descriptor: MapStateDescriptor)`
`ctx.timestamp()`
`ctx.current_watermark()`
`ctx.current_processing_time()`
`yield output_tag, value`

The stateDescriptor in the getBroadcastState() should be identical to the one in the .broadcast(ruleStateDescriptor)
above.

`stateDescriptor`
`getBroadcastState()`
`.broadcast(ruleStateDescriptor)`

The difference lies in the type of access each one gives to the broadcast state. The broadcasted side has
read-write access to it, while the non-broadcast side has read-only access (thus the names). The reason for this
is that in Flink there is no cross-task communication. So, to guarantee that the contents in the Broadcast State are the
same across all parallel instances of our operator, we give read-write access only to the broadcast side, which sees the
same elements across all tasks, and we require the computation on each incoming element on that side to be identical
across all tasks. Ignoring this rule would break the consistency guarantees of the state, leading to inconsistent and
often difficult to debug results.


> 
  The logic implemented in processBroadcastElement() must have the same deterministic behavior
across all parallel instances!


`processBroadcastElement()`

Finally, due to the fact that the KeyedBroadcastProcessFunction is operating on a keyed stream, it
exposes some functionality which is not available to the BroadcastProcessFunction. That is:

`KeyedBroadcastProcessFunction`
`BroadcastProcessFunction`
1. the ReadOnlyContext in the processElement() method gives access to Flink’s underlying timer service, which allows
to register event and/or processing time timers. When a timer fires, the onTimer() (shown above) is invoked with an
OnTimerContext which exposes the same functionality as the ReadOnlyContext plus
`ReadOnlyContext`
`processElement()`
`onTimer()`
`OnTimerContext`
`ReadOnlyContext`
* the ability to ask if the timer that fired was an event or processing time one and
* to query the key associated with the timer.
1. the Context in the processBroadcastElement() method contains the method
applyToKeyedState(StateDescriptor<S, VS> stateDescriptor, KeyedStateFunction<KS, S> function). This allows to
register a KeyedStateFunction to be applied to all states of all keys associated with the provided stateDescriptor.
Note that apply_to_keyed_state is not supported in PyFlink yet.
`Context`
`processBroadcastElement()`
`applyToKeyedState(StateDescriptor<S, VS> stateDescriptor, KeyedStateFunction<KS, S> function)`
`KeyedStateFunction`
`stateDescriptor`
`apply_to_keyed_state`


  Registering timers is only possible at processElement() of the KeyedBroadcastProcessFunction
and only there. It is not possible in the processBroadcastElement() method, as there is no key associated to the
broadcasted elements.


Coming back to our original example, our KeyedBroadcastProcessFunction could look like the following:


> 
  Registering timers is only possible at processElement() of the KeyedBroadcastProcessFunction
and only there. It is not possible in the processBroadcastElement() method, as there is no key associated to the
broadcasted elements.


`processElement()`
`KeyedBroadcastProcessFunction`
`processBroadcastElement()`
`KeyedBroadcastProcessFunction`

```
new KeyedBroadcastProcessFunction<Color, Item, Rule, String>() {

    // store partial matches, i.e. first elements of the pair waiting for their second element
    // we keep a list as we may have many first elements waiting
    private final MapStateDescriptor<String, List<Item>> mapStateDesc =
        new MapStateDescriptor<>(
            "items",
            BasicTypeInfo.STRING_TYPE_INFO,
            new ListTypeInfo<>(Item.class));

    // identical to our ruleStateDescriptor above
    private final MapStateDescriptor<String, Rule> ruleStateDescriptor = 
        new MapStateDescriptor<>(
            "RulesBroadcastState",
            BasicTypeInfo.STRING_TYPE_INFO,
            TypeInformation.of(new TypeHint<Rule>() {}));

    @Override
    public void processBroadcastElement(Rule value,
                                        Context ctx,
                                        Collector<String> out) throws Exception {
        ctx.getBroadcastState(ruleStateDescriptor).put(value.name, value);
    }

    @Override
    public void processElement(Item value,
                               ReadOnlyContext ctx,
                               Collector<String> out) throws Exception {

        final MapState<String, List<Item>> state = getRuntimeContext().getMapState(mapStateDesc);
        final Shape shape = value.getShape();
    
        for (Map.Entry<String, Rule> entry :
                ctx.getBroadcastState(ruleStateDescriptor).immutableEntries()) {
            final String ruleName = entry.getKey();
            final Rule rule = entry.getValue();
    
            List<Item> stored = state.get(ruleName);
            if (stored == null) {
                stored = new ArrayList<>();
            }
    
            if (shape == rule.second && !stored.isEmpty()) {
                for (Item i : stored) {
                    out.collect("MATCH: " + i + " - " + value);
                }
                stored.clear();
            }
    
            // there is no else{} to cover if rule.first == rule.second
            if (shape.equals(rule.first)) {
                stored.add(value);
            }
    
            if (stored.isEmpty()) {
                state.remove(ruleName);
            } else {
                state.put(ruleName, stored);
            }
        }
    }
}

```

`new KeyedBroadcastProcessFunction<Color, Item, Rule, String>() {

    // store partial matches, i.e. first elements of the pair waiting for their second element
    // we keep a list as we may have many first elements waiting
    private final MapStateDescriptor<String, List<Item>> mapStateDesc =
        new MapStateDescriptor<>(
            "items",
            BasicTypeInfo.STRING_TYPE_INFO,
            new ListTypeInfo<>(Item.class));

    // identical to our ruleStateDescriptor above
    private final MapStateDescriptor<String, Rule> ruleStateDescriptor = 
        new MapStateDescriptor<>(
            "RulesBroadcastState",
            BasicTypeInfo.STRING_TYPE_INFO,
            TypeInformation.of(new TypeHint<Rule>() {}));

    @Override
    public void processBroadcastElement(Rule value,
                                        Context ctx,
                                        Collector<String> out) throws Exception {
        ctx.getBroadcastState(ruleStateDescriptor).put(value.name, value);
    }

    @Override
    public void processElement(Item value,
                               ReadOnlyContext ctx,
                               Collector<String> out) throws Exception {

        final MapState<String, List<Item>> state = getRuntimeContext().getMapState(mapStateDesc);
        final Shape shape = value.getShape();
    
        for (Map.Entry<String, Rule> entry :
                ctx.getBroadcastState(ruleStateDescriptor).immutableEntries()) {
            final String ruleName = entry.getKey();
            final Rule rule = entry.getValue();
    
            List<Item> stored = state.get(ruleName);
            if (stored == null) {
                stored = new ArrayList<>();
            }
    
            if (shape == rule.second && !stored.isEmpty()) {
                for (Item i : stored) {
                    out.collect("MATCH: " + i + " - " + value);
                }
                stored.clear();
            }
    
            // there is no else{} to cover if rule.first == rule.second
            if (shape.equals(rule.first)) {
                stored.add(value);
            }
    
            if (stored.isEmpty()) {
                state.remove(ruleName);
            } else {
                state.put(ruleName, stored);
            }
        }
    }
}
`

```
class MyKeyedBroadcastProcessFunction(KeyedBroadcastProcessFunction):

    def __init__(self):
        self._map_state_desc = MapStateDescriptor("item", Types.STRING(), Types.LIST(Types.PICKLED_BYTE_ARRAY()))
        self._rule_state_desc = MapStateDescriptor("RulesBroadcastState", Types.STRING(), Types.PICKLED_BYTE_ARRAY())
        self._map_state = None
    
    def open(self, ctx: RuntimeContext):
        self._map_state = ctx.get_map_state(self._map_state_desc)
    
    def process_broadcast_element(value: Rule, ctx: KeyedBroadcastProcessFunction.Context):
        ctx.get_broadcast_state(self._rule_state_desc).put(value.name, value)
    
    def process_element(value: Item, ctx: KeyedBroadcastProcessFunction.ReadOnlyContext):
        shape = value.get_shape()

        for rule_name, rule in ctx.get_broadcast_state(self._rule_state_desc).items():

            stored = self._map_state.get(rule_name)
            if stored is None:
                stored = []
            
            if shape == rule.second and len(stored) > 0:
                for i in stored:
                    yield "MATCH: {} - {}".format(i, value)
                stored = []
            
            if shape == rule.first:
                stored.append(value)
            
            if len(stored) == 0:
                self._map_state.remove(rule_name)
            else:
                self._map_state.put(rule_name, stored)

```

`class MyKeyedBroadcastProcessFunction(KeyedBroadcastProcessFunction):

    def __init__(self):
        self._map_state_desc = MapStateDescriptor("item", Types.STRING(), Types.LIST(Types.PICKLED_BYTE_ARRAY()))
        self._rule_state_desc = MapStateDescriptor("RulesBroadcastState", Types.STRING(), Types.PICKLED_BYTE_ARRAY())
        self._map_state = None
    
    def open(self, ctx: RuntimeContext):
        self._map_state = ctx.get_map_state(self._map_state_desc)
    
    def process_broadcast_element(value: Rule, ctx: KeyedBroadcastProcessFunction.Context):
        ctx.get_broadcast_state(self._rule_state_desc).put(value.name, value)
    
    def process_element(value: Item, ctx: KeyedBroadcastProcessFunction.ReadOnlyContext):
        shape = value.get_shape()

        for rule_name, rule in ctx.get_broadcast_state(self._rule_state_desc).items():

            stored = self._map_state.get(rule_name)
            if stored is None:
                stored = []
            
            if shape == rule.second and len(stored) > 0:
                for i in stored:
                    yield "MATCH: {} - {}".format(i, value)
                stored = []
            
            if shape == rule.first:
                stored.append(value)
            
            if len(stored) == 0:
                self._map_state.remove(rule_name)
            else:
                self._map_state.put(rule_name, stored)
`

## Important Considerations#


After describing the offered APIs, this section focuses on the important things to keep in mind when using broadcast
state. These are:

* 
There is no cross-task communication: As stated earlier, this is the reason why only the broadcast side of a
(Keyed)-BroadcastProcessFunction can modify the contents of the broadcast state. In addition, the user has to make
sure that all tasks modify the contents of the broadcast state in the same way for each incoming element. Otherwise,
different tasks might have different contents, leading to inconsistent results.

* 
Order of events in Broadcast State may differ across tasks: Although broadcasting the elements of a stream
guarantees that all elements will (eventually) go to all downstream tasks, elements may arrive in a different order
to each task. So the state updates for each incoming element MUST NOT depend on the ordering of the incoming
events.

* 
All tasks checkpoint their broadcast state: Although all tasks have the same elements in their broadcast state
when a checkpoint takes place (checkpoint barriers do not overpass elements), all tasks checkpoint their broadcast state,
and not just one of them. This is a design decision to avoid having all tasks read from the same file during a restore
(thus avoiding hotspots), although it comes at the expense of increasing the size of the checkpointed state by a factor
of p (= parallelism). Flink guarantees that upon restoring/rescaling there will be no duplicates and no missing data.
In case of recovery with the same or smaller parallelism, each task reads its checkpointed state. Upon scaling up, each
task reads its own state, and the remaining tasks (p_new-p_old) read checkpoints of previous tasks in a round-robin
manner.

* 
No RocksDB state backend: Broadcast state is kept in-memory at runtime and memory provisioning should be done
accordingly. This holds for all operator states.


There is no cross-task communication: As stated earlier, this is the reason why only the broadcast side of a
(Keyed)-BroadcastProcessFunction can modify the contents of the broadcast state. In addition, the user has to make
sure that all tasks modify the contents of the broadcast state in the same way for each incoming element. Otherwise,
different tasks might have different contents, leading to inconsistent results.

`(Keyed)-BroadcastProcessFunction`

Order of events in Broadcast State may differ across tasks: Although broadcasting the elements of a stream
guarantees that all elements will (eventually) go to all downstream tasks, elements may arrive in a different order
to each task. So the state updates for each incoming element MUST NOT depend on the ordering of the incoming
events.


All tasks checkpoint their broadcast state: Although all tasks have the same elements in their broadcast state
when a checkpoint takes place (checkpoint barriers do not overpass elements), all tasks checkpoint their broadcast state,
and not just one of them. This is a design decision to avoid having all tasks read from the same file during a restore
(thus avoiding hotspots), although it comes at the expense of increasing the size of the checkpointed state by a factor
of p (= parallelism). Flink guarantees that upon restoring/rescaling there will be no duplicates and no missing data.
In case of recovery with the same or smaller parallelism, each task reads its checkpointed state. Upon scaling up, each
task reads its own state, and the remaining tasks (p_new-p_old) read checkpoints of previous tasks in a round-robin
manner.

`p_new`
`p_old`

No RocksDB state backend: Broadcast state is kept in-memory at runtime and memory provisioning should be done
accordingly. This holds for all operator states.


 Back to top
