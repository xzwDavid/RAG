# Set up Flink's Process Memory


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Set up Flink’s Process Memory#


Apache Flink provides efficient workloads on top of the JVM by tightly controlling the memory usage of its various components.
While the community strives to offer sensible defaults to all configurations, the full breadth of applications
that users deploy on Flink means this isn’t always possible. To provide the most production value to our users,
Flink allows both high-level and fine-grained tuning of memory allocation within clusters. To optimize memory requirements, check the network memory tuning guide.


The further described memory configuration is applicable starting with the release version 1.10 for TaskManager and
1.11 for JobManager processes. If you upgrade Flink from earlier versions, check the migration guide
because many changes were introduced with the 1.10 and 1.11 releases.


## Configure Total Memory#


The total process memory of Flink JVM processes consists of memory consumed by the Flink application (total Flink memory)
and by the JVM to run the process. The total Flink memory consumption includes usage of JVM Heap and Off-heap
(Direct or Native) memory.


The simplest way to setup memory in Flink is to configure either of the two following options:

`taskmanager.memory.flink.size`
`jobmanager.memory.flink.size`
`taskmanager.memory.process.size`
`jobmanager.memory.process.size`

> 
  For local execution, see detailed information for TaskManager and JobManager processes.



The rest of the memory components will be adjusted automatically, based on default values or additionally configured options.
See also how to set up other components for TaskManager and JobManager memory.


Configuring total Flink memory is better suited for standalone deployments
where you want to declare how much memory is given to Flink itself. The total Flink memory splits up into JVM Heap
and Off-heap memory.
See also how to configure memory for standalone deployments.


If you configure total process memory you declare how much memory in total should be assigned to the Flink JVM process.
For the containerized deployments it corresponds to the size of the requested container, see also
how to configure memory for containers
(Kubernetes or Yarn).


Another way to set up the memory is to configure the required internal components of the total Flink memory which are
specific to the concrete Flink process. Check how to configure them for TaskManager
and for JobManager.


One of the three mentioned ways has to be used to configure Flinkâs memory
(except for local execution), or the Flink startup will fail. This means that one of the following option subsets,
which do not have default values, have to be configured explicitly:

`taskmanager.memory.flink.size`
`jobmanager.memory.flink.size`
`taskmanager.memory.process.size`
`jobmanager.memory.process.size`
`taskmanager.memory.task.heap.size`
`taskmanager.memory.managed.size`
`jobmanager.memory.heap.size`

> 
  Explicitly configuring both total process memory and total Flink memory
is not recommended. It may lead to deployment failures due to potential memory configuration conflicts.
Configuring other memory components also requires caution as it can produce further configuration conflicts.



## JVM Parameters#


Flink explicitly adds the following memory related JVM arguments while starting its processes, based on the configured
or derived memory component sizes:


(*) Keep in mind that you might not be able to use the full amount of heap memory depending on the GC algorithm used. Some GC algorithms allocate a certain amount of heap memory for themselves.
This will lead to a different maximum being returned by the Heap metrics.

(**) Notice, that the native non-direct usage of memory in user code can be also accounted for as a part of the off-heap memory.

(***) The JVM Direct memory limit is added for JobManager process only if the corresponding option
jobmanager.memory.enable-jvm-direct-memory-limit is set.


`jobmanager.memory.enable-jvm-direct-memory-limit`

Check also the detailed memory model for TaskManager and
JobManager to understand how to configure the relevant components.


## Capped Fractionated Components#


This section describes the configuration details of options which can be a fraction of some other memory size while being constrained by a min-max range:

* JVM Overhead can be a fraction of the total process memory
* Network memory can be a fraction of the total Flink memory (only for TaskManager)

Check also the detailed memory model for TaskManager and
JobManager to understand how to configure the relevant components.


The size of those components always has to be between its maximum and minimum value, otherwise Flink startup will fail.
The maximum and minimum values have defaults or can be explicitly set by corresponding configuration options.
For example, if you only set the following memory options:

* total Process memory = 1000MB,
* JVM Overhead min = 64MB,
* JVM Overhead max = 128MB,
* JVM Overhead fraction = 0.1

then the JVM Overhead will be 1000MB x 0.1 = 100MB which is within the range 64-128MB.


Notice if you configure the same maximum and minimum value it effectively fixes the size to that value.


If you do not explicitly configure the component memory, then Flink will use the fraction to calculate the memory size
based on the total memory. The calculated value is capped by its corresponding min/max options.
For example, if only the following memory options are set:

* total Process memory = 1000MB,
* JVM Overhead min = 128MB,
* JVM Overhead max = 256MB,
* JVM Overhead fraction = 0.1

then the JVM Overhead will be 128MB because the size derived from fraction is 100MB, and it is less than the minimum.


It can also happen that the fraction is ignored if the sizes of the total memory and its other components are defined.
In this case, the JVM Overhead is the rest of the total memory. The derived value still has to be within its min/max
range otherwise the configuration fails. For example, suppose only the following memory options are set:

* total Process memory = 1000MB,
* task heap = 100MB, (similar example can be for JVM Heap in the JobManager)
* JVM Overhead min = 64MB,
* JVM Overhead max = 256MB,
* JVM Overhead fraction = 0.1

All other components of the total Process memory have default values, including the default Managed Memory fraction
(or Off-heap memory in the JobManager). Then the JVM Overhead is not the fraction (1000MB x 0.1 = 100MB), but the rest
of the total Process memory which will either be within the range 64-256MB or fail.
