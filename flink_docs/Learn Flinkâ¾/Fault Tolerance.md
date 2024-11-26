# Fault Tolerance


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Fault Tolerance via State Snapshots#


## State Backends#


The keyed state managed by Flink is a sort of sharded, key/value store, and the working copy of each
item of keyed state is kept somewhere local to the taskmanager responsible for that key. Operator
state is also local to the machine(s) that need(s) it.


This state that Flink manages is stored in a state backend.
Two implementations of state backends are available – one based on RocksDB, an embedded key/value store that keeps its working state on
disk, and another heap-based state backend that keeps its working state in memory, on the Java heap.

* Supports state larger than available memory
* Rule of thumb: 10x slower than heap-based backends
* Fast, requires large heap
* Subject to GC

When working with state kept in a heap-based state backend, accesses and updates involve reading and
writing objects on the heap. But for objects kept in the EmbeddedRocksDBStateBackend, accesses and updates
involve serialization and deserialization, and so are much more expensive. But the amount of state
you can have with RocksDB is limited only by the size of the local disk. Note also that only the
EmbeddedRocksDBStateBackend is able to do incremental snapshotting, which is a significant benefit for
applications with large amounts of slowly changing state.

`EmbeddedRocksDBStateBackend`
`EmbeddedRocksDBStateBackend`

Both of these state backends are able to do asynchronous snapshotting, meaning that they can take a
snapshot without impeding the ongoing stream processing.


## Checkpoint Storage#


Flink periodically takes persistent snapshots of all the state in every operator and copies these snapshots somewhere more durable, such as a distributed file system. In the event of the failure, Flink can restore the complete state of your application and resume
processing as though nothing had gone wrong.


The location where these snapshots are stored is defined via the jobs checkpoint storage.
Two implementations of checkpoint storage are available - one that persists its state snapshots
to a distributed file system, and another that uses the JobManager’s heap.

* Supports very large state size
* Highly durable
* Recommended for production deployments
* Good for testing and experimentation with small state (locally)

 Back to top


## State Snapshots#


### Definitions#

* Snapshot – a generic term referring to a global, consistent image of the state of a Flink job.
A snapshot includes a pointer into each of the data sources (e.g., an offset into a file or Kafka
partition), as well as a copy of the state from each of the job’s stateful operators that resulted
from having processed all of the events up to those positions in the sources.
* Checkpoint – a snapshot taken automatically by Flink for the purpose of being able to recover
from faults. Checkpoints can be incremental, and are optimized for being restored quickly.
* Externalized Checkpoint – normally checkpoints are not intended to be manipulated by users.
Flink retains only the n-most-recent checkpoints (n being configurable) while a job is
running, and deletes them when a job is cancelled. But you can configure them to be retained
instead, in which case you can manually resume from them.
* Savepoint – a snapshot triggered manually by a user (or an API call) for some operational
purpose, such as a stateful redeploy/upgrade/rescaling operation. Savepoints are always complete,
and are optimized for operational flexibility.

### How does State Snapshotting Work?#


Flink uses a variant of the Chandy-Lamport algorithm known as asynchronous barrier
snapshotting.


When a task manager is instructed by the checkpoint coordinator (part of the job manager) to begin a
checkpoint, it has all of the sources record their offsets and insert numbered checkpoint barriers
into their streams. These barriers flow through the job graph, indicating the part of the stream
before and after each checkpoint.


Checkpoint n will contain the state of each operator that resulted from having consumed every
event before checkpoint barrier n, and none of the events after it.


As each operator in the job graph receives one of these barriers, it records its state. Operators
with two input streams (such as a CoProcessFunction) perform barrier alignment so that the
snapshot will reflect the state resulting from consuming events from both input streams up to (but
not past) both barriers.

`CoProcessFunction`

Flink’s state backends use a copy-on-write mechanism to allow stream processing to continue
unimpeded while older versions of the state are being asynchronously snapshotted. Only when the
snapshots have been durably persisted will these older versions of the state be garbage collected.


### Exactly Once Guarantees#


When things go wrong in a stream processing application, it is possible to have either lost, or
duplicated results. With Flink, depending on the choices you make for your application and the
cluster you run it on, any of these outcomes is possible:

* Flink makes no effort to recover from failures (at most once)
* Nothing is lost, but you may experience duplicated results (at least once)
* Nothing is lost or duplicated (exactly once)

Given that Flink recovers from faults by rewinding and replaying the source data streams, when the
ideal situation is described as exactly once this does not mean that every event will be
processed exactly once. Instead, it means that every event will affect the state being managed by
Flink exactly once.


Barrier alignment is only needed for providing exactly once guarantees. If you don’t need this, you
can gain some performance by configuring Flink to use CheckpointingMode.AT_LEAST_ONCE, which has
the effect of disabling barrier alignment.

`CheckpointingMode.AT_LEAST_ONCE`

### Exactly Once End-to-end#


To achieve exactly once end-to-end, so that every event from the sources affects the sinks exactly
once, the following must be true:

1. your sources must be replayable, and
2. your sinks must be transactional (or idempotent)

 Back to top


## Hands-on#


The Flink Operations Playground includes a section on
Observing Failure & Recovery.


 Back to top


## Further Reading#

* Stateful Stream Processing
* State Backends
* Fault Tolerance Guarantees of Data Sources and Sinks
* Enabling and Configuring Checkpointing
* Checkpoints
* Savepoints
* Tuning Checkpoints and Large State
* Monitoring Checkpointing
* Task Failure Recovery

 Back to top
