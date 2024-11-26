# Memory Tuning Guide


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Memory tuning guide#


In addition to the main memory setup guide, this section explains how to set up memory
depending on the use case and which options are important for each case.


## Configure memory for standalone deployment#


It is recommended to configure total Flink memory
(taskmanager.memory.flink.size or jobmanager.memory.flink.size)
or its components for standalone deployment where you want to declare how much memory
is given to Flink itself. Additionally, you can adjust JVM metaspace if it causes problems.

`taskmanager.memory.flink.size`
`jobmanager.memory.flink.size`

The total Process memory is not relevant because JVM overhead is not controlled by Flink or the deployment environment,
only physical resources of the executing machine matter in this case.


## Configure memory for containers#


It is recommended to configure total process memory
(taskmanager.memory.process.size or jobmanager.memory.process.size)
for the containerized deployments (Kubernetes or Yarn).
It declares how much memory in total should be assigned to the Flink JVM process and corresponds to the size of the requested container.

`taskmanager.memory.process.size`
`jobmanager.memory.process.size`

Note If you configure the total Flink memory Flink will implicitly add JVM memory components
to derive the total process memory and request a container with the memory of that derived size.


> 
Warning: If Flink or user code allocates unmanaged off-heap (native) memory beyond the container size
the job can fail because the deployment environment can kill the offending containers.



See also description of container memory exceeded failure.


## Configure memory for state backends#


This is only relevant for TaskManagers.


When deploying a Flink streaming application, the type of state backend used
will dictate the optimal memory configurations of your cluster.


### HashMap state backend#


When running a stateless job or using the HashMapStateBackend), set managed memory to zero.
This will ensure that the maximum amount of heap memory is allocated for user code on the JVM.


### RocksDB state backend#


The EmbeddedRocksDBStateBackend uses native memory. By default,
RocksDB is set up to limit native memory allocation to the size of the managed memory.
Therefore, it is important to reserve enough managed memory for your state. If you disable the default RocksDB memory control,
TaskManagers can be killed in containerized deployments if RocksDB allocates memory above the limit of the requested container size
(the total process memory).
See also how to tune RocksDB memory
and state.backend.rocksdb.memory.managed.


## Configure memory for batch jobs#


This is only relevant for TaskManagers.


Flink’s batch operators leverage managed memory to run more efficiently.
In doing so, some operations can be performed directly on raw data without having to be deserialized into Java objects.
This means that managed memory configurations have practical effects
on the performance of your applications. Flink will attempt to allocate and use as much managed memory
as configured for batch jobs but not go beyond its limits. This prevents OutOfMemoryError’s because Flink knows precisely
how much memory it has to leverage. If the managed memory is not sufficient,
Flink will gracefully spill to disk.

`OutOfMemoryError`