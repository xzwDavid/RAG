# Set up TaskManager Memory


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Set up TaskManager Memory#


The TaskManager runs user code in Flink.
Configuring memory usage for your needs can greatly reduce Flink’s resource footprint and improve Job stability.


The further described memory configuration is applicable starting with the release version 1.10. If you upgrade Flink
from earlier versions, check the migration guide because many changes were introduced with the 1.10 release.


> 
  This memory setup guide is relevant only for TaskManagers!
The TaskManager memory components have a similar but more sophisticated structure compared to the memory model of the JobManager process.



## Configure Total Memory#


The total process memory of Flink JVM processes consists of memory consumed by Flink application (total Flink memory)
and by the JVM to run the process. The total Flink memory consumption includes usage of JVM Heap,
managed memory (managed by Flink) and other direct (or native) memory.


If you run Flink locally (e.g. from your IDE) without creating a cluster, then only a subset of the memory configuration
options are relevant, see also local execution for more details.


Otherwise, the simplest way to setup memory for TaskManagers is to configure the total memory.
A more fine-grained approach is described in more detail here.


The rest of the memory components will be adjusted automatically, based on default values or additionally configured options.
See next chapters for more details about the other memory components.


## Configure Heap and Managed Memory#


As mentioned before in total memory description, another way to setup memory in Flink is
to specify explicitly both task heap and managed memory.
It gives more control over the available JVM Heap to Flinkâs tasks and its managed memory.


The rest of the memory components will be adjusted automatically, based on default values or additionally configured options.
Here are more details about the other memory components.


> 
  If you have configured the task heap and managed memory explicitly, it is recommended to set neither
total process memory nor total Flink memory. Otherwise, it may easily lead to memory configuration conflicts.



### Task (Operator) Heap Memory#


If you want to guarantee that a certain amount of JVM Heap is available for your user code, you can set the task heap memory
explicitly (taskmanager.memory.task.heap.size).
It will be added to the JVM Heap size and will be dedicated to Flinkâs operators running the user code.

`taskmanager.memory.task.heap.size`

### Managed Memory#


Managed memory is managed by Flink and is allocated as native memory (off-heap). The following workloads use managed memory:

* Streaming jobs can use it for RocksDB state backend.
* Both streaming and batch jobs can use it for sorting, hash tables, caching of intermediate results.
* Both streaming and batch jobs can use it for executing User Defined Functions in Python processes.

The size of managed memory can be

* either configured explicitly via taskmanager.memory.managed.size
* or computed as a fraction of total Flink memory via taskmanager.memory.managed.fraction.
`taskmanager.memory.managed.size`
`taskmanager.memory.managed.fraction`

Size will override fraction, if both are set.
If neither size nor fraction is explicitly configured, the default fraction will be used.


See also how to configure memory for state backends and batch jobs.


#### Consumer Weights#


If your job contains multiple types of managed memory consumers, you can also control how managed memory should be shared across these types.
The configuration option taskmanager.memory.managed.consumer-weights allows you to set a weight for each type, to which Flink will reserve managed memory proportionally.
Valid consumer types are:

`taskmanager.memory.managed.consumer-weights`
* OPERATOR: for built-in algorithms.
* STATE_BACKEND: for RocksDB state backend in streaming
* PYTHON: for Python processes.
`OPERATOR`
`STATE_BACKEND`
`PYTHON`

E.g. if a streaming job uses both RocksDB state backend and Python UDFs, and the consumer weights are configured as STATE_BACKEND:70,PYTHON:30, Flink will reserve 70% of the total managed memory for RocksDB state backend and 30% for Python processes.

`STATE_BACKEND:70,PYTHON:30`
`70%`
`30%`

For each type, Flink reserves managed memory only if the job contains managed memory consumers of that type.
E.g, if a streaming job uses the heap state backend and Python UDFs, and the consumer weights are configured as STATE_BACKEND:70,PYTHON:30, Flink will use all of its managed memory for Python processes, because the heap state backend does not use managed memory.

`STATE_BACKEND:70,PYTHON:30`

> 
  Flink will not reserve managed memory for consumer types that are not included in the consumer weights.
If the missing type is actually needed by the job, it can lead to memory allocation failures.
By default, all consumer types are included.
This could only happen when the weights are explicitly configured/overwritten.



## Configure Off-heap Memory (direct or native)#


The off-heap memory which is allocated by user code should be accounted for in task off-heap memory
(taskmanager.memory.task.off-heap.size).

`taskmanager.memory.task.off-heap.size`

You can also adjust the framework off-heap memory.
You should only change this value if you are sure that the Flink framework needs more memory.


Flink includes the framework off-heap memory and task off-heap memory into the direct memory limit of the JVM,
see also JVM parameters.


Note Although, native non-direct memory usage can be accounted for as a part of the
framework off-heap memory or task off-heap memory, it will result in a higher JVM’s direct memory limit in this case.


Note The network memory is also part of JVM direct memory, but it is managed by Flink and guaranteed
to never exceed its configured size. Therefore, resizing the network memory will not help in this situation.


See also the detailed memory model.


## Detailed Memory Model#


The following table lists all memory components, depicted above, and references Flink configuration options
which affect the size of the respective components:

`taskmanager.memory.framework.heap.size`
`taskmanager.memory.task.heap.size`
`taskmanager.memory.managed.size`
`taskmanager.memory.managed.fraction`
`taskmanager.memory.framework.off-heap.size`
`taskmanager.memory.task.off-heap.size`
`taskmanager.memory.network.min`
`taskmanager.memory.network.max`
`taskmanager.memory.network.fraction`
`taskmanager.memory.jvm-metaspace.size`
`taskmanager.memory.jvm-overhead.min`
`taskmanager.memory.jvm-overhead.max`
`taskmanager.memory.jvm-overhead.fraction`

As you can see, the size of some memory components can be simply set by the respective option.
Other components can be tuned using multiple options.


## Framework Memory#


You should not change the framework heap memory and framework off-heap memory without a good reason.
Adjust them only if you are sure that Flink needs more memory for some internal data structures or operations.
It can be related to a particular deployment environment or job structure, like high parallelism.
In addition, Flink dependencies, such as Hadoop may consume more direct or native memory in certain setups.


Note Flink neither isolates heap nor off-heap versions of framework and task memory at the moment.
The separation of framework and task memory can be used in future releases for further optimizations.


## Local Execution#


If you start Flink locally on your machine as a single java program without creating a cluster (e.g. from your IDE)
then all components are ignored except for the following:

`taskmanager.memory.task.heap.size`
`taskmanager.memory.task.off-heap.size`
`taskmanager.memory.managed.size`
`taskmanager.memory.network.min`
`taskmanager.memory.network.max`

All of the components listed above can be but do not have to be explicitly configured for local execution.
If they are not configured they are set to their default values. Task heap memory and
task off-heap memory are considered to be infinite (Long.MAX_VALUE bytes) and managed memory
has a default value of 128MB only for the local execution mode.


Note The task heap size is not related in any way to the real heap size in this case.
It can become relevant for future optimizations coming with next releases. The actual JVM Heap size of the started
local process is not controlled by Flink and depends on how you start the process.
If you want to control the JVM Heap size you have to explicitly pass the corresponding JVM arguments, e.g. -Xmx, -Xms.
