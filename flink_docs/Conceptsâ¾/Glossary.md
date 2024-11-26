# Glossary


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Glossary#


#### Checkpoint Storage#


The location where the State Backend will store its snapshot during a checkpoint (Java Heap of JobManager or Filesystem).


#### Flink Application Cluster#


A Flink Application Cluster is a dedicated Flink Cluster that
only executes Flink Jobs from one Flink
Application. The lifetime of the Flink
Cluster is bound to the lifetime of the Flink Application.


#### Flink Job Cluster#


A Flink Job Cluster is a dedicated Flink Cluster that only
executes a single Flink Job. The lifetime of the
Flink Cluster is bound to the lifetime of the Flink Job.
This deployment mode has been deprecated since Flink 1.15.


#### Flink Cluster#


A distributed system consisting of (typically) one JobManager and one or more
Flink TaskManager processes.


#### Event#


An event is a statement about a change of the state of the domain modelled by the
application. Events can be input and/or output of a stream or batch processing application.
Events are special types of records.


#### ExecutionGraph#


see Physical Graph


#### Function#


Functions are implemented by the user and encapsulate the
application logic of a Flink program. Most Functions are wrapped by a corresponding
Operator.


#### Instance#


The term instance is used to describe a specific instance of a specific type (usually
Operator or Function) during runtime. As Apache Flink is mostly written in
Java, this corresponds to the definition of Instance or Object in Java. In the context of Apache
Flink, the term parallel instance is also frequently used to emphasize that multiple instances of
the same Operator or Function type are running in parallel.


#### Flink Application#


A Flink application is a Java Application that submits one or multiple Flink
Jobs from the main() method (or by some other means). Submitting
jobs is usually done by calling execute() on an execution environment.

`main()`
`execute()`

The jobs of an application can either be submitted to a long running Flink
Session Cluster, to a dedicated Flink Application
Cluster, or to a Flink Job
Cluster.


#### Flink Job#


A Flink Job is the runtime representation of a logical graph
(also often called dataflow graph) that is created and submitted by calling
execute() in a Flink Application.

`execute()`

#### JobGraph#


see Logical Graph


#### Flink JobManager#


The JobManager is the orchestrator of a Flink Cluster. It contains three distinct
components: Flink Resource Manager, Flink Dispatcher and one Flink JobMaster
per running Flink Job.


#### Flink JobMaster#


JobMasters are one of the components running in the JobManager. A JobMaster is
responsible for supervising the execution of the Tasks of a single job.


#### JobResultStore#


The JobResultStore is a Flink component that persists the results of globally terminated
(i.e. finished, cancelled or failed) jobs to a filesystem, allowing the results to outlive
a finished job. These results are then used by Flink to determine whether jobs should
be subject to recovery in highly-available clusters.


#### Logical Graph#


A logical graph is a directed graph where the nodes are  Operators
and the edges define input/output-relationships of the operators and correspond
to data streams or data sets. A logical graph is created by submitting jobs
from a Flink Application.


Logical graphs are also often referred to as dataflow graphs.


#### Managed State#


Managed State describes application state which has been registered with the framework. For
Managed State, Apache Flink will take care about persistence and rescaling among other things.


#### Operator#


Node of a Logical Graph. An Operator performs a certain operation, which is
usually executed by a Function. Sources and Sinks are special Operators for data
ingestion and data egress.


#### Operator Chain#


An Operator Chain consists of two or more consecutive Operators without any
repartitioning in between. Operators within the same Operator Chain forward records to each other
directly without going through serialization or Flink’s network stack.


#### Partition#


A partition is an independent subset of the overall data stream or data set. A data stream or
data set is divided into partitions by assigning each record to one or more partitions.
Partitions of data streams or data sets are consumed by Tasks during runtime. A
transformation which changes the way a data stream or data set is partitioned is often called
repartitioning.


#### Physical Graph#


A physical graph is the result of translating a Logical Graph for execution in a
distributed runtime. The nodes are Tasks and the edges indicate input/output-relationships
or partitions of data streams or data sets.


#### Record#


Records are the constituent elements of a data set or data stream. Operators and
Functions receive records as input and emit records as output.


#### (Runtime) Execution Mode#


DataStream API programs can be executed in one of two execution modes: BATCH
or STREAMING. See Execution Mode for more details.

`BATCH`
`STREAMING`

#### Flink Session Cluster#


A long-running Flink Cluster which accepts multiple Flink Jobs for
execution. The lifetime of this Flink Cluster is not bound to the lifetime of any Flink Job.
Formerly, a Flink Session Cluster was also known as a Flink Cluster in session mode. Compare to
Flink Application Cluster.


#### State Backend#


For stream processing programs, the State Backend of a Flink Job determines how its
state is stored on each TaskManager (Java Heap of TaskManager or (embedded)
RocksDB).


#### Sub-Task#


A Sub-Task is a Task responsible for processing a partition of
the data stream. The term “Sub-Task” emphasizes that there are multiple parallel Tasks for the same
Operator or Operator Chain.


#### Table Program#


A generic term for pipelines declared with Flink’s relational APIs (Table API or SQL).


#### Task#


Node of a Physical Graph. A task is the basic unit of work, which is executed by
Flink’s runtime. Tasks encapsulate exactly one parallel instance of an
Operator or Operator Chain.


#### Flink TaskManager#


TaskManagers are the worker processes of a Flink Cluster. Tasks are
scheduled to TaskManagers for execution. They communicate with each other to exchange data between
subsequent Tasks.


#### Transformation#


A Transformation is applied on one or more data streams or data sets and results in one or more
output data streams or data sets. A transformation might change a data stream or data set on a
per-record basis, but might also only change its partitioning or perform an aggregation. While
Operators and Functions are the “physical” parts of Flink’s API,
Transformations are only an API concept. Specifically, most transformations are
implemented by certain Operators.


#### UID#


A unique identifier of an Operator, either provided by the user or determined from the
structure of the job. When the Application is submitted this is converted to
a UID hash.


#### UID hash#


A unique identifier of an Operator at runtime, otherwise known as “Operator ID” or
“Vertex ID” and generated from a UID.
It is commonly exposed in logs, the REST API or metrics, and most importantly is how
operators are identified within savepoints.
