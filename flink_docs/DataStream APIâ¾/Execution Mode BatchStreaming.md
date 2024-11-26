# Execution Mode (Batch/Streaming)


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Execution Mode (Batch/Streaming)#


The DataStream API supports different runtime execution modes from which you
can choose depending on the requirements of your use case and the
characteristics of your job.


There is the “classic” execution behavior of the DataStream API, which we call
STREAMING execution mode. This should be used for unbounded jobs that require
continuous incremental processing and are expected to stay online indefinitely.

`STREAMING`

Additionally, there is a batch-style execution mode that we call BATCH
execution mode. This executes jobs in a way that is more reminiscent of batch
processing frameworks such as MapReduce. This should be used for bounded jobs
for which you have a known fixed input and which do not run continuously.

`BATCH`

Apache Flink’s unified approach to stream and batch processing means that a
DataStream application executed over bounded input will produce the same
final results regardless of the configured execution mode. It is important to
note what final means here: a job executing in STREAMING mode might produce
incremental updates (think upserts in a database) while a BATCH job would
only produce one final result at the end. The final result will be the same if
interpreted correctly but the way to get there can be different.

`STREAMING`
`BATCH`

By enabling BATCH execution, we allow Flink to apply additional optimizations
that we can only do when we know that our input is bounded. For example,
different join/aggregation strategies can be used, in addition to a different
shuffle implementation that allows more efficient task scheduling and failure
recovery behavior. We will go into some of the details of the execution
behavior below.

`BATCH`

## When can/should I use BATCH execution mode?#


The BATCH execution mode can only be used for Jobs/Flink Programs that are
bounded. Boundedness is a property of a data source that tells us whether all
the input coming from that source is known before execution or whether new data
will show up, potentially indefinitely. A job, in turn, is bounded if all its
sources are bounded, and unbounded otherwise.

`BATCH`

STREAMING execution mode, on the other hand, can be used for both bounded and
unbounded jobs.

`STREAMING`

As a rule of thumb, you should be using BATCH execution mode when your program
is bounded because this will be more efficient. You have to use STREAMING
execution mode when your program is unbounded because only this mode is general
enough to be able to deal with continuous data streams.

`BATCH`
`STREAMING`

One obvious outlier is when you want to use a bounded job to bootstrap some job
state that you then want to use in an unbounded job. For example, by running a
bounded job using STREAMING mode, taking a savepoint, and then restoring that
savepoint on an unbounded job. This is a very specific use case and one that
might soon become obsolete when we allow producing a savepoint as additional
output of a BATCH execution job.

`STREAMING`
`BATCH`

Another case where you might run a bounded job using STREAMING mode is when
writing tests for code that will eventually run with unbounded sources. For
testing it can be more natural to use a bounded source in those cases.

`STREAMING`

## Configuring BATCH execution mode#


The execution mode can be configured via the execution.runtime-mode setting.
There are three possible values:

`execution.runtime-mode`
* STREAMING: The classic DataStream execution mode (default)
* BATCH: Batch-style execution on the DataStream API
* AUTOMATIC: Let the system decide based on the boundedness of the sources
`STREAMING`
`BATCH`
`AUTOMATIC`

This can be configured via command line parameters of bin/flink run ..., or
programmatically when creating/configuring the StreamExecutionEnvironment.

`bin/flink run ...`
`StreamExecutionEnvironment`

Here’s how you can configure the execution mode via the command line:


```
$ bin/flink run -Dexecution.runtime-mode=BATCH <jarFile>

```

`$ bin/flink run -Dexecution.runtime-mode=BATCH <jarFile>
`

This example shows how you can configure the execution mode in code:


```
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setRuntimeMode(RuntimeExecutionMode.BATCH);

```

`StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.setRuntimeMode(RuntimeExecutionMode.BATCH);
`

> 
  We recommend users to NOT set the runtime mode in their program but to instead
set it using the command-line when submitting the application. Keeping the
application code configuration-free allows for more flexibility as the same
application can be executed in any execution mode.



## Execution Behavior#


This section provides an overview of the execution behavior of BATCH
execution mode and contrasts it with STREAMING execution mode. For more
details, please refer to the FLIPs that introduced this feature:
FLIP-134 and
FLIP-140.

`BATCH`
`STREAMING`

### Task Scheduling And Network Shuffle#


Flink jobs consist of different operations that are connected together in a
dataflow graph. The system decides how to schedule the execution of these
operations on different processes/machines (TaskManagers) and how data is
shuffled (sent) between them.


Multiple operations/operators can be chained together using a feature called
chaining.
A group of one or multiple (chained)
operators that Flink considers as a unit of scheduling is called a task.
Often the term subtask is used to refer to the individual instances of tasks
that are running in parallel on multiple TaskManagers but we will only use the
term task here.


Task scheduling and network shuffles work differently for BATCH and
STREAMING execution mode. Mostly due to the fact that we know our input data
is bounded in BATCH execution mode, which allows Flink to use more efficient
data structures and algorithms.

`BATCH`
`STREAMING`
`BATCH`

We will use this example to explain the differences in task scheduling and
network transfer:


```
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStreamSource<String> source = env.fromElements(...);

source.name("source")
	.map(...).name("map1")
	.map(...).name("map2")
	.rebalance()
	.map(...).name("map3")
	.map(...).name("map4")
	.keyBy((value) -> value)
	.map(...).name("map5")
	.map(...).name("map6")
	.sinkTo(...).name("sink");

```

`StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

DataStreamSource<String> source = env.fromElements(...);

source.name("source")
	.map(...).name("map1")
	.map(...).name("map2")
	.rebalance()
	.map(...).name("map3")
	.map(...).name("map4")
	.keyBy((value) -> value)
	.map(...).name("map5")
	.map(...).name("map6")
	.sinkTo(...).name("sink");
`

Operations that imply a 1-to-1 connection pattern between operations, such as
map(), flatMap(), or filter() can just forward data straight to the next
operation, which allows these operations to be chained together. This means
that Flink would not normally insert a network shuffle between them.

`map()`
`flatMap()`
`filter()`

Operation such as keyBy() or rebalance() on the other hand require data to
be shuffled between different parallel instances of tasks. This induces a
network shuffle.

`keyBy()`
`rebalance()`

For the above example Flink would group operations together as tasks like this:

* Task1: source, map1, and map2
* Task2: map3, map4
* Task3: map5, map6, and sink
`source`
`map1`
`map2`
`map3`
`map4`
`map5`
`map6`
`sink`

And we have a network shuffle between Tasks 1 and 2, and also Tasks 2 and 3.
This is a visual representation of that job:


#### STREAMING Execution Mode#


In STREAMING execution mode, all tasks need to be online/running all the
time.  This allows Flink to immediately process new records through the whole
pipeline, which we need for continuous and low-latency stream processing. This
also means that the TaskManagers that are allotted to a job need to have enough
resources to run all the tasks at the same time.

`STREAMING`

Network shuffles are pipelined, meaning that records are immediately sent to
downstream tasks, with some buffering on the network layer. Again, this is
required because when processing a continuous stream of data there are no
natural points (in time) where data could be materialized between tasks (or
pipelines of tasks). This contrasts with BATCH execution mode where
intermediate results can be materialized, as explained below.

`BATCH`

#### BATCH Execution Mode#


In BATCH execution mode, the tasks of a job can be separated into stages that
can be executed one after another. We can do this because the input is bounded
and Flink can therefore fully process one stage of the pipeline before moving
on to the next. In the above example the job would have three stages that
correspond to the three tasks that are separated by the shuffle barriers.

`BATCH`

Instead of sending records immediately to downstream tasks, as explained above
for STREAMING mode, processing in stages requires Flink to materialize
intermediate results of tasks to some non-ephemeral storage which allows
downstream tasks to read them after upstream tasks have already gone off line.
This will increase the latency of processing but comes with other interesting
properties. For one, this allows Flink to backtrack to the latest available
results when a failure happens instead of restarting the whole job. Another
side effect is that BATCH jobs can execute on fewer resources (in terms of
available slots at TaskManagers) because the system can execute tasks
sequentially one after the other.

`STREAMING`
`BATCH`

TaskManagers will keep intermediate results at least as long as downstream
tasks have not consumed them. (Technically, they will be kept until the
consuming pipelined regions have produced their output.) After
that, they will be kept for as long as space allows in order to allow the
aforementioned backtracking to earlier results in case of a failure.


### State Backends / State#


In STREAMING mode, Flink uses a StateBackend to control how state is stored and how
checkpointing works.

`STREAMING`

In BATCH mode, the configured state backend is ignored. Instead, the input of
a keyed operation is grouped by key (using sorting) and then we process all
records of a key in turn. This allows keeping only the state of only one key at
the same time. State for a given key will be discarded when moving on to the
next key.

`BATCH`

See FLIP-140 for background
information on this.


### Order of Processing#


The order in which records are processed in operators or user-defined functions (UDFs) can differ between BATCH and STREAMING execution.

`BATCH`
`STREAMING`

In STREAMING mode, user-defined functions should not make any assumptions about incoming records’ order.
Data is processed as soon as it arrives.

`STREAMING`

In BATCH execution mode, there are some operations where Flink guarantees order.
The ordering can be a side effect of the particular task scheduling,
network shuffle, and state backend (see above), or a conscious choice by the system.

`BATCH`

There are three general types of input that we can differentiate:

* broadcast input: input from a broadcast stream (see also Broadcast
State)
* regular input: input that is neither broadcast nor keyed
* keyed input: input from a KeyedStream
`KeyedStream`

Functions, or Operators, that consume multiple input types will process them in the following order:

* broadcast inputs are processed first
* regular inputs are processed second
* keyed inputs are processed last

For functions that consume from multiple regular or broadcast inputs â such as a CoProcessFunction â Flink has the right to process data from any input of that type in any order.

`CoProcessFunction`

For functions that consume from multiple keyed inputs â such as a KeyedCoProcessFunction â Flink processes all records for a single key from all keyed inputs before moving on to the next.

`KeyedCoProcessFunction`

### Event Time / Watermarks#


When it comes to supporting event time, Flinkâs
streaming runtime builds on the pessimistic assumption that events may come
out-of-order, i.e. an event with timestamp t may come after an event with
timestamp t+1. Because of this, the system can never be sure that no more
elements with timestamp t < T for a given timestamp T can come in the
future. To amortise the impact of this out-of-orderness on the final result
while making the system practical, in STREAMING mode, Flink uses a heuristic
called Watermarks.
A watermark with timestamp T signals that no element with timestamp t < T will follow.

`t`
`t+1`
`t < T`
`T`
`STREAMING`
`T`
`t < T`

In BATCH mode, where the input dataset is known in advance, there is no need
for such a heuristic as, at the very least, elements can be sorted by timestamp
so that they are processed in temporal order. For readers familiar with
streaming, in BATCH we can assume âperfect watermarksâ.

`BATCH`
`BATCH`

Given the above, in BATCH mode, we only need a MAX_WATERMARK at the end of
the input associated with each key, or at the end of input if the input stream
is not keyed. Based on this scheme, all registered timers will fire at the end
of time and user-defined WatermarkAssigners or WatermarkGenerators are
ignored. Specifying a WatermarkStrategy is still important, though, because
its TimestampAssigner will still be used to assign timestamps to records.

`BATCH`
`MAX_WATERMARK`
`WatermarkAssigners`
`WatermarkGenerators`
`WatermarkStrategy`
`TimestampAssigner`

### Processing Time#


Processing Time is the wall-clock time on the machine that a record is
processed, at the specific instance that the record is being processed. Based
on this definition, we see that the results of a computation that is based on
processing time are not reproducible. This is because the same record processed
twice will have two different timestamps.


Despite the above, using processing time in STREAMING mode can be useful. The
reason has to do with the fact that streaming pipelines often ingest their
unbounded input in real time so there is a correlation between event time and
processing time. In addition, because of the above, in STREAMING mode 1h in
event time can often be almost 1h in processing time, or wall-clock time. So
using processing time can be used for early (incomplete) firings that give
hints about the expected results.

`STREAMING`
`STREAMING`
`1h`
`1h`

This correlation does not exist in the batch world where the input dataset is
static and known in advance.  Given this, in BATCH mode we allow users to
request the current processing time and register processing time timers, but,
as in the case of Event Time, all the timers are going to fire at the end of
the input.

`BATCH`

Conceptually, we can imagine that processing time does not advance during the
execution of a job and we fast-forward to the end of time when the whole
input is processed.


### Failure Recovery#


In STREAMING execution mode, Flink uses checkpoints for failure recovery.
Take a look at the checkpointing documentation for hands-on documentation about this and
how to configure it. There is also a more introductory section about fault
tolerance via state snapshots that
explains the concepts at a higher level.

`STREAMING`

One of the characteristics of checkpointing for failure recovery is that Flink
will restart all the running tasks from a checkpoint in case of a failure. This
can be more costly than what we have to do in BATCH mode (as explained
below), which is one of the reasons that you should use BATCH execution mode
if your job allows it.

`BATCH`
`BATCH`

In BATCH execution mode, Flink will try and backtrack to previous processing
stages for which intermediate results are still available. Potentially, only
the tasks that failed (or their predecessors in the graph) will have to be
restarted, which can improve processing efficiency and overall processing time
of the job compared to restarting all tasks from a checkpoint.

`BATCH`

## Important Considerations#


Compared to classic STREAMING execution mode, in BATCH mode some things
might not work as expected. Some features will work slightly differently while
others are not supported.

`STREAMING`
`BATCH`

Behavior Change in BATCH mode:

* “Rolling” operations such as reduce()
or sum() emit an incremental update for every new record that arrives in STREAMING
mode. In BATCH mode, these operations are not “rolling”. They emit only the
final result.
`STREAMING`
`BATCH`

Unsupported in BATCH mode:

* Checkpointing
and any operations that depend on checkpointing do not work.

Custom operators should be implemented with care, otherwise they might behave
improperly. See also additional explanations below for more details.


### Checkpointing#


As explained above, failure recovery for batch programs
does not use checkpointing.


It is important to remember that because there are no checkpoints, certain
features such as 

    CheckpointListener


and, as a result,  Kafka’s EXACTLY_ONCE mode or File Sink’s
OnCheckpointRollingPolicy
won’t work. If you need a transactional sink that works in
BATCH mode make sure it uses the Unified Sink API as proposed in
FLIP-143.

`File Sink`
`BATCH`

You can still use all the state primitives,
it’s just that the mechanism used for failure recovery will be different.


### Writing Custom Operators#


> 
Note: Custom operators are an advanced usage pattern of Apache Flink. For most
use-cases, consider using a (keyed-)process function instead.



It is important to remember the assumptions made for BATCH execution mode
when writing a custom operator. Otherwise, an operator that works just fine for
STREAMING mode might produce wrong results in BATCH mode. Operators are
never scoped to a particular key which means they see some properties of
BATCH processing Flink tries to leverage.

`BATCH`
`STREAMING`
`BATCH`
`BATCH`

First of all you should not cache the last seen watermark within an operator.
In BATCH mode we process records key by key. As a result, the Watermark will
switch from MAX_VALUE to MIN_VALUE between each key. You should not assume
that the Watermark will always be ascending in an operator. For the same
reasons timers will fire first in key order and then in timestamp order within
each key. Moreover, operations that change a key manually are not supported.

`BATCH`
`MAX_VALUE`
`MIN_VALUE`