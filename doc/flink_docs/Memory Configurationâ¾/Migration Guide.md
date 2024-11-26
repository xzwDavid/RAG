# Migration Guide


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Migration Guide#


The memory setup has changed a lot with the 1.10 release for TaskManagers and with the 1.11
release for JobManagers. Many configuration options were removed or their semantics changed.
This guide will help you to migrate the TaskManager memory configuration from Flink
<= 1.9 to >= 1.10 and
the JobManager memory configuration from Flink <= 1.10 to >= 1.11.


> 
  It is important to review this guide because the legacy and new memory configuration can
result in different sizes of memory components. If you try to reuse your Flink configuration from older versions
before 1.10 for TaskManagers or before 1.11 for JobManagers, it can result in changes to the behavior, performance or even configuration failures of your application.



Note Before version 1.10 for TaskManagers and before 1.11 for JobManagers,
Flink did not require that memory related options are set at all as they all had default values.
The new memory configuration requires that at least one subset of
the following options is configured explicitly, otherwise the configuration will fail:

`taskmanager.memory.flink.size`
`jobmanager.memory.flink.size`
`taskmanager.memory.process.size`
`jobmanager.memory.process.size`
`taskmanager.memory.task.heap.size`
`taskmanager.memory.managed.size`
`jobmanager.memory.heap.size`

The default Flink configuration file shipped with Flink sets
taskmanager.memory.process.size (since 1.10) and
jobmanager.memory.process.size (since 1.11)
to make the default memory configuration consistent.

`taskmanager.memory.process.size`
`jobmanager.memory.process.size`

This spreadsheet can also help
to evaluate and compare the results of the legacy and new memory computations.


## Migrate Task Manager Memory Configuration#


### Changes in Configuration Options#


This chapter shortly lists all changes to Flink’s memory configuration options introduced with the 1.10 release.
It also references other chapters for more details about migrating to the new configuration options.


The following options are completely removed. If they are still used, they will be ignored.


##### taskmanager.memory.fraction


##### taskmanager.memory.off-heap


##### taskmanager.memory.preallocate


The following options are deprecated but if they are still used they will be interpreted as new options for backwards compatibility:


##### taskmanager.heap.size

* taskmanager.memory.flink.size for standalone deployment
* taskmanager.memory.process.size for containerized deployments

##### taskmanager.memory.size


##### taskmanager.network.memory.min


##### taskmanager.network.memory.max


##### taskmanager.network.memory.fraction


Although, the network memory configuration has not changed too much it is recommended to verify its configuration.
It can change if other memory components have new sizes, e.g. the total memory which the network can be a fraction of.
See also new detailed memory model.


The container cut-off configuration options, containerized.heap-cutoff-ratio and containerized.heap-cutoff-min,
have no effect anymore for TaskManagers. See also how to migrate container cut-off.

`containerized.heap-cutoff-ratio`
`containerized.heap-cutoff-min`

### Total Memory (Previously Heap Memory)#


The previous options which were responsible for the total memory used by Flink are taskmanager.heap.size or taskmanager.heap.mb.
Despite their naming, they included not only JVM Heap but also other off-heap memory components. The options have been deprecated.

`taskmanager.heap.size`
`taskmanager.heap.mb`

If you use the mentioned legacy options without specifying the corresponding new options,
they will be directly translated into the following new options:

* Total Flink memory (taskmanager.memory.flink.size) for standalone deployments
* Total process memory (taskmanager.memory.process.size) for containerized deployments (Yarn)
`taskmanager.memory.flink.size`
`taskmanager.memory.process.size`

It is also recommended using these new options instead of the legacy ones as they might be completely removed in the following releases.


See also how to configure total memory now.


### JVM Heap Memory#


JVM Heap memory previously consisted of the managed memory (if configured to be on-heap) and the rest
which included any other usages of heap memory. This rest was the remaining part of the total memory,
see also how to migrate managed memory.


Now, if only total Flink memory or total process memory is configured, then the JVM Heap is the rest of
what is left after subtracting all other components from the total memory, see also how to configure total memory.


Additionally, you can now have more direct control over the JVM Heap assigned to the operator tasks
(taskmanager.memory.task.heap.size),
see also Task (Operator) Heap Memory.
The JVM Heap memory is also used by the heap state backends (MemoryStateBackend
or FsStateBackend) if it is chosen for streaming jobs.

`taskmanager.memory.task.heap.size`

A part of the JVM Heap is now always reserved for the Flink framework
(taskmanager.memory.framework.heap.size).
See also Framework memory.

`taskmanager.memory.framework.heap.size`

### Managed Memory#


See also how to configure managed memory now.


#### Explicit Size#


The previous option to configure managed memory size (taskmanager.memory.size) was renamed to
taskmanager.memory.managed.size and deprecated.
It is recommended to use the new option because the legacy one can be removed in future releases.

`taskmanager.memory.size`
`taskmanager.memory.managed.size`

#### Fraction#


If not set explicitly, the managed memory could be previously specified as a fraction (taskmanager.memory.fraction)
of the total memory minus network memory and container cut-off (only for Yarn deployments). This option has been completely removed and will have no effect if still used.
Please, use the new option taskmanager.memory.managed.fraction instead.
This new option will set the managed memory to the specified fraction of the
total Flink memory if its size is not set explicitly by
taskmanager.memory.managed.size.

`taskmanager.memory.fraction`
`taskmanager.memory.managed.fraction`
`taskmanager.memory.managed.size`

#### RocksDB state#


If the RocksDBStateBackend is chosen for a streaming job,
its native memory consumption should now be accounted for in managed memory.
The RocksDB memory allocation is limited by the managed memory size.
This should prevent the killing of containers on Yarn.
You can disable the RocksDB memory control by setting state.backend.rocksdb.memory.managed
to false. See also how to migrate container cut-off.

`false`

#### Other changes#


Additionally, the following changes have been made:

* The managed memory is always off-heap now. The configuration option taskmanager.memory.off-heap is removed and will have no effect anymore.
* The managed memory now uses native memory which is not direct memory. It means that the managed memory is no longer accounted for in the JVM direct memory limit.
* The managed memory is always lazily allocated now. The configuration option taskmanager.memory.preallocate is removed and will have no effect anymore.
`taskmanager.memory.off-heap`
`taskmanager.memory.preallocate`

## Migrate Job Manager Memory Configuration#


Previously, there were options responsible for setting the JVM Heap size of the JobManager:

* jobmanager.heap.size
* jobmanager.heap.mb
`jobmanager.heap.size`
`jobmanager.heap.mb`

Despite their naming, they represented the JVM Heap only for standalone deployments.
For the containerized deployments (Kubernetes and Yarn),
they also included other off-heap memory consumption. The size of JVM Heap was additionally reduced by the container
cut-off which has been completely removed after 1.11.


The mentioned legacy options have been deprecated. If they are used without specifying the corresponding new options,
they will be directly translated into the following new options:

* JVM Heap (jobmanager.memory.heap.size) for standalone deployments
* Total process memory (jobmanager.memory.process.size) for containerized deployments (Kubernetes and Yarn)
`jobmanager.memory.heap.size`
`jobmanager.memory.process.size`

It is also recommended using these new options instead of the legacy ones as they might be completely removed in the following releases.


Now, if only the total Flink memory or total process memory is configured, then the JVM Heap
is also derived as the rest of what is left after subtracting all other components from the total memory, see also
how to configure total memory. Additionally, you can now have more direct
control over the JVM Heap by adjusting the
jobmanager.memory.heap.size option.

`jobmanager.memory.heap.size`

## Flink JVM process memory limits#


Since 1.10 release, Flink sets the JVM Metaspace and JVM Direct Memory limits for the TaskManager process
by adding the corresponding JVM arguments. Since 1.11 release, Flink also sets the JVM Metaspace limit for the JobManager process.
You can enable the JVM Direct Memory limit for JobManager process if you set the
jobmanager.memory.enable-jvm-direct-memory-limit option.
See also JVM parameters.

`jobmanager.memory.enable-jvm-direct-memory-limit`

Flink sets the mentioned JVM memory limits to simplify debugging of the corresponding memory leaks and avoid
the container out-of-memory errors.
See also the troubleshooting guide for details about the JVM Metaspace
and JVM Direct Memory OutOfMemoryErrors.


## Container Cut-Off Memory#


For containerized deployments, you could previously specify a cut-off memory. This memory could accommodate for unaccounted memory allocations.
Dependencies which were not directly controlled by Flink were the main source of those allocations, e.g. RocksDB, JVM internals, etc.
This is no longer available, and the related configuration options (containerized.heap-cutoff-ratio and containerized.heap-cutoff-min)
will have no effect anymore. The new memory model introduced more specific memory components to address these concerns.

`containerized.heap-cutoff-ratio`
`containerized.heap-cutoff-min`

### for TaskManagers#


In streaming jobs which use RocksDBStateBackend, the RocksDB
native memory consumption should be accounted for as a part of the managed memory now.
The RocksDB memory allocation is also limited by the configured size of the managed memory.
See also migrating managed memory and how to configure managed memory now.


The other direct or native off-heap memory consumers can now be addressed by the following new configuration options:

* Task off-heap memory (taskmanager.memory.task.off-heap.size)
* Framework off-heap memory (taskmanager.memory.framework.off-heap.size)
* JVM metaspace (taskmanager.memory.jvm-metaspace.size)
* JVM overhead
`taskmanager.memory.task.off-heap.size`
`taskmanager.memory.framework.off-heap.size`
`taskmanager.memory.jvm-metaspace.size`

### for JobManagers#


The direct or native off-heap memory consumers can now be addressed by the following new configuration options:

* Off-heap memory (jobmanager.memory.off-heap.size)
* JVM metaspace (jobmanager.memory.jvm-metaspace.size)
* JVM overhead
`jobmanager.memory.off-heap.size`
`jobmanager.memory.jvm-metaspace.size`

## Default Configuration in Flink configuration file#


This section describes the changes of the default Flink configuration file shipped with Flink.


The total memory for TaskManagers (taskmanager.heap.size) is replaced by taskmanager.memory.process.size
in the default Flink configuration file. The value increased from 1024MB to 1728MB.

`taskmanager.heap.size`
`taskmanager.memory.process.size`

The total memory for JobManagers (jobmanager.heap.size) is replaced by jobmanager.memory.process.size
in the default Flink configuration file. The value increased from 1024MB to 1600MB.

`jobmanager.heap.size`
`jobmanager.memory.process.size`

See also how to configure total memory now.


> 
Warning: If you use the new default Flink configuration file it can result in different sizes of memory components and can lead to performance changes.

