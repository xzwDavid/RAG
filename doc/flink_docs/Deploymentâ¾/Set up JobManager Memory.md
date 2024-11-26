# Set up JobManager Memory


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Set up JobManager Memory#


The JobManager is the controlling element of the Flink Cluster.
It consists of three distinct components: Resource Manager, Dispatcher and one JobMaster per running Flink Job.
This guide walks you through high level and fine-grained memory configurations for the JobManager.


The further described memory configuration is applicable starting with the release version 1.11. If you upgrade Flink
from earlier versions, check the migration guide because many changes were introduced with the 1.11 release.


> 
  This memory setup guide is relevant only for the JobManager!
The JobManager memory components have a similar but simpler structure compared to the TaskManagers’ memory configuration.



## Configure Total Memory#


The simplest way to set up the memory configuration is to configure the total memory for the process.
If you run the JobManager process using local execution mode you do not need to configure memory options, they will have no effect.


## Detailed configuration#


The following table lists all memory components, depicted above, and references Flink configuration options which
affect the size of the respective components:

`jobmanager.memory.heap.size`
`jobmanager.memory.off-heap.size`
`jobmanager.memory.jvm-metaspace.size`
`jobmanager.memory.jvm-overhead.min`
`jobmanager.memory.jvm-overhead.max`
`jobmanager.memory.jvm-overhead.fraction`

### Configure JVM Heap#


As mentioned before in the total memory description, another way to set up the memory
for the JobManager is to specify explicitly the JVM Heap size (jobmanager.memory.heap.size).
It gives more control over the available JVM Heap which is used by:

`jobmanager.memory.heap.size`
* Flink framework
* User code executed during job submission (e.g. for certain batch sources) or in checkpoint completion callbacks

The required size of JVM Heap is mostly driven by the number of running jobs, their structure, and requirements for
the mentioned user code.


Note If you have configured the JVM Heap explicitly, it is recommended to set
neither total process memory nor total Flink memory. Otherwise, it may easily lead to memory configuration conflicts.


The Flink scripts and CLI set the JVM Heap size via the JVM parameters -Xms and -Xmx when they start the JobManager process, see also JVM parameters.


### Configure Off-heap Memory#


The Off-heap memory component accounts for any type of JVM direct memory and native memory usage. Therefore,
you can also enable the JVM Direct Memory limit by setting the jobmanager.memory.enable-jvm-direct-memory-limit option.
If this option is configured, Flink will set the limit to the Off-heap memory size via the corresponding JVM argument: -XX:MaxDirectMemorySize.
See also JVM parameters.

`jobmanager.memory.enable-jvm-direct-memory-limit`

The size of this component can be configured by jobmanager.memory.off-heap.size
option. This option can be tuned e.g. if the JobManager process throws âOutOfMemoryError: Direct buffer memoryâ, see
the troubleshooting guide for more information.

`jobmanager.memory.off-heap.size`

There can be the following possible sources of Off-heap memory consumption:

* Flink framework dependencies (e.g. Pekko network communication)
* User code executed during job submission (e.g. for certain batch sources) or in checkpoint completion callbacks

Note If you have configured the Total Flink Memory
and the JVM Heap explicitly but you have not configured the Off-heap memory, the size of the Off-heap memory
will be derived as the Total Flink Memory minus the JVM Heap.
The default value of the Off-heap memory option will be ignored.


## Local Execution#


If you run Flink locally (e.g. from your IDE) without creating a cluster, then the JobManager memory configuration options are ignored.
