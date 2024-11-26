# Troubleshooting


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Troubleshooting#


## IllegalConfigurationException#


If you see an IllegalConfigurationException thrown from TaskExecutorProcessUtils or JobManagerProcessUtils, it
usually indicates that there is either an invalid configuration value (e.g. negative memory size, fraction that is
greater than 1, etc.) or configuration conflicts. Check the documentation chapters or
configuration options related to the memory components mentioned in the exception message.


## OutOfMemoryError: Java heap space#


The exception usually indicates that the JVM Heap is too small. You can try to increase the JVM Heap size
by increasing total memory. You can also directly increase
task heap memory for TaskManagers or
JVM Heap memory for JobManagers.


> 
  You can also increase the framework heap memory
for TaskManagers, but you should only change this option if you are sure the Flink framework itself needs more memory.



## OutOfMemoryError: Direct buffer memory#


The exception usually indicates that the JVM direct memory limit is too small or that there is a direct memory leak.
Check whether user code or other external dependencies use the JVM direct memory and that it is properly accounted for.
You can try to increase its limit by adjusting direct off-heap memory.
See also how to configure off-heap memory for TaskManagers,
JobManagers and the JVM arguments which Flink sets.


## OutOfMemoryError: Metaspace#


The exception usually indicates that JVM metaspace limit is configured too small.
You can try to increase the JVM metaspace option for TaskManagers
or JobManagers.


## IOException: Insufficient number of network buffers#


This is only relevant for TaskManagers.


The exception usually indicates that the size of the configured network memory
is not big enough. You can try to increase the network memory by adjusting the following options:

* taskmanager.memory.network.min
* taskmanager.memory.network.max
* taskmanager.memory.network.fraction
`taskmanager.memory.network.min`
`taskmanager.memory.network.max`
`taskmanager.memory.network.fraction`

## Container Memory Exceeded#


If a Flink container tries to allocate memory beyond its requested size (Yarn or Kubernetes),
this usually indicates that Flink has not reserved enough native memory. You can observe this either by using an external
monitoring system or from the error messages when a container gets killed by the deployment environment.


If you encounter this problem in the JobManager process, you can also enable the JVM Direct Memory limit by setting the
jobmanager.memory.enable-jvm-direct-memory-limit option
to exclude possible JVM Direct Memory leak.

`jobmanager.memory.enable-jvm-direct-memory-limit`

If RocksDBStateBackend is usedï¼

* and memory controlling is disabled: You can try to increase the TaskManager’s managed memory.
* and memory controlling is enabled and non-heap memory increases during savepoint or full checkpoints: This may happen due to the glibc memory allocator (see glibc bug).
You can try to add the environment variable MALLOC_ARENA_MAX=1 for TaskManagers.
`glibc`
`MALLOC_ARENA_MAX=1`

Alternatively, you can increase the JVM Overhead.


See also how to configure memory for containers.
