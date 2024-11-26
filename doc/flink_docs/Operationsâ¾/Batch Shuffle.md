# Batch Shuffle


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Batch Shuffle#


## Overview#


Flink supports a batch execution mode in both DataStream API and Table / SQL for jobs executing across bounded input. In batch execution mode, Flink offers two modes for network exchanges: Blocking Shuffle and Hybrid Shuffle.

`Blocking Shuffle`
`Hybrid Shuffle`
* Blocking Shuffle is the default data exchange mode for batch executions. It persists all intermediate data, and can be consumed only after fully produced.
* Hybrid Shuffle is the next generation data exchange mode for batch executions. It persists data more smartly, and allows consuming while being produced. This feature is still experimental and has some known limitations.
`Blocking Shuffle`
`Hybrid Shuffle`

## Blocking Shuffle#


Unlike the pipeline shuffle used for streaming applications, blocking exchanges persists data to some storage. Downstream tasks then fetch these values via the network. Such an exchange reduces the resources required to execute the job as it does not need the upstream and downstream tasks to run simultaneously.


As a whole, Flink provides two different types of blocking shuffles: Hash shuffle and Sort shuffle.

`Hash shuffle`
`Sort shuffle`

### Hash Shuffle#


The default blocking shuffle implementation for 1.14 and lower, Hash Shuffle, has each upstream task persist its results in a separate file for each downstream task on the local disk of the TaskManager. When the downstream tasks run, they will request partitions from the upstream TaskManager’s, which read the files and transmit data via the network.

`Hash Shuffle`

Hash Shuffle provides different mechanisms for writing and reading files:

`Hash Shuffle`
* file: Writes files with the normal File IO, reads and transmits files with Netty FileRegion. FileRegion relies on sendfile system call to reduce the number of data copies and memory consumption.
* mmap: Writes and reads files with mmap system call.
* auto: Writes files with the normal File IO, for file reading, it falls back to normal file option on 32 bit machine and use mmap on 64 bit machine. This is to avoid file size limitation of java mmap implementation on 32 bit machine.
`file`
`FileRegion`
`FileRegion`
`sendfile`
`mmap`
`mmap`
`auto`
`file`
`mmap`
`mmap`

The different mechanism could be chosen via TaskManager configurations.


> 
  This option is experimental and might be changed future.



> 
  If SSL is enabled, the file mechanism can not use FileRegion and instead uses an un-pooled buffer to cache data before transmitting. This might cause direct memory OOM. Additionally, since the synchronous file reading might block Netty threads for some time, the SSL handshake timeout needs to be increased to avoid connection reset errors.


`file`
`FileRegion`

> 
  The memory usage of mmap is not accounted for by configured memory limits, but some resource frameworks like Yarn will track this memory usage and kill the container if memory exceeds some threshold.


`mmap`

Hash Shuffle works well for small scale jobs with SSD, but it also has some disadvantages:

`Hash Shuffle`
1. If the job scale is large, it might create too many files, and it requires a large write buffer to write these files at the same time.
2. On HDD, when multiple downstream tasks fetch their data simultaneously, it might incur the issue of random IO.

### Sort Shuffle#


Sort Shuffle is another blocking shuffle implementation introduced in version 1.13 and it becomes the default blocking shuffle implementation in 1.15. Different from Hash Shuffle, Sort Shuffle writes only one file for each result partition. When the result partition is read by multiple downstream tasks concurrently, the data file is opened only once and shared by all readers. As a result, the cluster uses fewer resources like inode and file descriptors, which improves stability. Furthermore, by writing fewer files and making a best effort to read data sequentially, Sort Shuffle can achieve better performance than Hash Shuffle, especially on HDD. Additionally, Sort Shuffle uses extra managed memory as data reading buffer and does not rely on sendfile or mmap mechanism, thus it also works well with SSL. Please refer to FLINK-19582 and FLINK-19614 for more details about Sort Shuffle.

`Sort Shuffle`
`Hash Shuffle`
`Sort Shuffle`
`Sort Shuffle`
`Hash Shuffle`
`Sort Shuffle`
`sendfile`
`mmap`
`Sort Shuffle`

Here are some config options that might need adjustment when using sort blocking shuffle:

* taskmanager.network.sort-shuffle.min-buffers: Config option to control data writing buffer size. For large scale jobs, you may need to increase this value, usually, several hundreds of megabytes memory is enough. Because this memory is allocated from network memory, to increase this value, you may also need to increase the total network memory by adjusting taskmanager.memory.network.fraction, taskmanager.memory.network.min and taskmanager.memory.network.max to avoid the potential “Insufficient number of network buffers” error.
* taskmanager.memory.framework.off-heap.batch-shuffle.size: Config option to control data reading buffer size. For large scale jobs, you may need to increase this value, usually, several hundreds of megabytes memory is enough. Because this memory is cut from the framework off-heap memory, to increase this value, you need also to increase the total framework off-heap memory by adjusting taskmanager.memory.framework.off-heap.size to avoid the potential direct memory OOM error.

> 
  Currently Sort Shuffle only sort records by partition index instead of the records themselves, that is to say, the sort is only used as a data clustering algorithm.


`Sort Shuffle`
`sort`

### Choices of Blocking Shuffle#


As a summary,

* For small scale jobs running on SSD, both implementation should work.
* For large scale jobs or for jobs running on HDD, Sort Shuffle should be more suitable.
`Sort Shuffle`

To switch between Sort Shuffle and Hash Shuffle, you need to adjust this config option: taskmanager.network.sort-shuffle.min-parallelism. It controls which shuffle implementation to use based on the parallelism of downstream tasks, if the parallelism is lower than the configured value, Hash Shuffle will be used, otherwise Sort Shuffle will be used. For versions lower than 1.15, its default value is Integer.MAX_VALUE, so Hash Shuffle will be used by default. Since 1.15, its default value is 1, so Sort Shuffle will be used by default.

`Sort Shuffle`
`Hash Shuffle`
`Hash Shuffle`
`Sort Shuffle`
`Integer.MAX_VALUE`
`Hash Shuffle`
`Sort Shuffle`

## Hybrid Shuffle#


> 
  This feature is still experimental and has some known limitations.



Hybrid shuffle is the next generation of batch data exchanges. It combines the advantages of blocking shuffle and pipelined shuffle (in streaming mode).

* Like blocking shuffle, it does not require upstream and downstream tasks to run simultaneously, which allows executing a job with little resources.
* Like pipelined shuffle, it does not require downstream tasks to be executed after upstream tasks finish, which reduces the overall execution time of the job when given sufficient resources.
* It adapts to custom preferences between persisting less data and restarting less tasks on failures, by providing different spilling strategies.

To use hybrid shuffle mode, you need to configure the execution.batch-shuffle-mode to ALL_EXCHANGES_HYBRID_FULL (full spilling strategy) or ALL_EXCHANGES_HYBRID_SELECTIVE (selective spilling strategy).

`ALL_EXCHANGES_HYBRID_FULL`
`ALL_EXCHANGES_HYBRID_SELECTIVE`

### Spilling Strategy#


Hybrid shuffle provides two spilling strategies:

* Selective Spilling Strategy persists data only if they are not consumed by downstream tasks timely. This reduces the amount of data to persist, at the price that in case of failures upstream tasks need to be restarted to reproduce the complete intermediate results.
* Full Spilling Strategy persists all data, no matter they are consumed by downstream tasks or not. In case of failures, the persisted complete intermediate result can be re-consumed, without having to restart upstream tasks.

To use hybrid shuffle mode, you need to configure the execution.batch-shuffle-mode to ALL_EXCHANGES_HYBRID_FULL (full spilling strategy) or ALL_EXCHANGES_HYBRID_SELECTIVE (selective spilling strategy).

`ALL_EXCHANGES_HYBRID_FULL`
`ALL_EXCHANGES_HYBRID_SELECTIVE`

### Data Consumption Constraints#


Hybrid shuffle divides the partition data consumption constraints between producer and consumer into the following three cases:

* ALL_PRODUCERS_FINISHED : hybrid partition data can be consumed only when all producers are finished.
* ONLY_FINISHED_PRODUCERS : hybrid partition can only consume data from finished producers.
* UNFINISHED_PRODUCERS : hybrid partition can consume data from unfinished producers.

These could be configured via jobmanager.partition.hybrid.partition-data-consume-constraint.

* For AdaptiveBatchScheduler : The default constraint is UNFINISHED_PRODUCERS to perform pipelined-like shuffle. If the value is set to ALL_PRODUCERS_FINISHED or ONLY_FINISHED_PRODUCERS, performance may be degraded.
* If SpeculativeExecution is enabled : The default constraint is ONLY_FINISHED_PRODUCERS to bring some performance optimization compared with blocking shuffle. Since producers and consumers have the opportunity to run at the same time, more speculative execution tasks may be created, and the cost of failover will also increase. If you want to fall back to the same behavior as blocking shuffle, you can configure this value to ALL_PRODUCERS_FINISHED. It is also important to note that UNFINISHED_PRODUCERS is not supported in this mode.
`AdaptiveBatchScheduler`
`UNFINISHED_PRODUCERS`
`ALL_PRODUCERS_FINISHED`
`ONLY_FINISHED_PRODUCERS`
`SpeculativeExecution`
`ONLY_FINISHED_PRODUCERS`
`ALL_PRODUCERS_FINISHED`
`UNFINISHED_PRODUCERS`

### Remote Storage Support#


Hybrid shuffle supports to store the shuffle data to the remote storage. The remote storage path can be configured by taskmanager.network.hybrid-shuffle.remote.path. This feature supports various remote storage systems, including OSS, HDFS, S3, etc. See Flink Filesystem for more information about the Flink supported filesystems.


### Limitations#


Hybrid shuffle mode is still experimental and has some known limitations, which the Flink community is still working on eliminating.

* No support for Slot Sharing. In hybrid shuffle mode, Flink currently forces each task to be executed in a dedicated slot exclusively. If slot sharing is explicitly specified, an error will occur.
* No pipelined execution for dynamic graph. If auto-parallelism (dynamic graph) is enabled, Adaptive Batch Scheduler will wait until upstream tasks finish to decide parallelism of downstream tasks, which means hybrid shuffle effectively fallback to blocking shuffle (ALL_PRODUCERS_FINISHED constraint).
`ALL_PRODUCERS_FINISHED`

## Performance Tuning#


The following guidelines may help you to achieve better performance especially for large scale batch jobs:

1. Always use Sort Shuffle on HDD because Sort Shuffle can largely improve stability and IO performance. Since 1.15, Sort Shuffle is already the default blocking shuffle implementation, for 1.14 and lower version, you need to enable it manually by setting taskmanager.network.sort-shuffle.min-parallelism to 1.
2. For both blocking shuffle implementations, you may consider enabling data compression to improve the performance unless the data is hard to compress. Since 1.15, data compression is already enabled by default, for 1.14 and lower version, you need to enable it manually.
3. When Sort Shuffle is used, decreasing the number of exclusive buffers per channel and increasing the number of floating buffers per gate can help. For 1.14 and higher version, it is suggested to set taskmanager.network.memory.buffers-per-channel to 0 and set taskmanager.network.memory.floating-buffers-per-gate to a larger value (for example, 4096). This setting has two main advantages: 1) It decouples the network memory consumption from parallelism so for large scale jobs, the possibility of “Insufficient number of network buffers” error can be decreased; 2) Networker buffers are distributed among different channels according to needs, which can improve the network buffer utilization and further improve performance.
4. Increase the total size of network memory. Currently, the default network memory size is pretty modest. For large scale jobs, it’s suggested to increase the total network memory fraction to at least 0.2 to achieve better performance. At the same time, you may also need to adjust the lower bound and upper bound of the network memory size, please refer to the memory configuration document for more information.
5. Increase the memory size for shuffle data write. As mentioned in the above section, for large scale jobs, it’s suggested to increase the number of write buffers per result partition to at least (2 * parallelism) if you have enough memory. Note that you may also need to increase the total size of network memory to avoid the “Insufficient number of network buffers” error after you increase this config value.
6. Increase the memory size for shuffle data read. As mentioned in the above section, for large scale jobs, it’s suggested to increase the size of the shared read memory to a larger value (for example, 256M or 512M). Because this memory is cut from the framework off-heap memory, you must increase taskmanager.memory.framework.off-heap.size by the same size to avoid the direct memory OOM error.
`Sort Shuffle`
`Sort Shuffle`
`Sort Shuffle`
`Sort Shuffle`
1. Increase the total size of network memory. Currently, the default network memory size is pretty modest. For large scale jobs, it’s suggested to increase the total network memory fraction to at least 0.2 to achieve better performance. At the same time, you may also need to adjust the lower bound and upper bound of the network memory size, please refer to the memory configuration document for more information.
2. Increase the memory size for shuffle data write. For large scale jobs, it’s suggested to increase the total size of network memory, the larger the memory that can be used in the shuffle write phase, the more opportunities downstream to read data directly from memory.  Note that if you use the legacy Hybrid shuffle mode, you need to ensure that each Result Partition can be allocated to at least numSubpartition + 1 buffers, otherwise the “Insufficient number of network buffers” will be encountered.
3. Increase the memory size for shuffle data read. For large scale jobs, it’s suggested to increase the size of the shared read memory to a larger value (for example, 256M or 512M). Because this memory is cut from the framework off-heap memory, you must increase taskmanager.memory.framework.off-heap.size by the same size to avoid the direct memory OOM error.
4. When the legacy Hybrid shuffle mode is used, decreasing the number of exclusive buffers per channel will seriously affect the performance. Therefore, this value should not be set to 0, and for large-scale job, this can be appropriately increased. It should be also noted that, for hybrid shuffle, taskmanager.network.memory.read-buffer.required-per-gate.max has been set to Integer.MAX_VALUE by default. It is better not to adjust this value, otherwise there is a risk of performance degradation.
`Result Partition`
`numSubpartition + 1`
`0`
`Integer.MAX_VALUE`

## Trouble Shooting#


Here are some exceptions you may encounter (rarely) and the corresponding solutions that may help:

`Sort Shuffle`
`Hash Shuffle`
`Sort Shuffle`
`Sort Shuffle`
`Hash Shuffle`
`Sort Shuffle`
`Sort Shuffle`
`Sort Shuffle`
`Hash Shuffle`
`Sort Shuffle`
`Sort Shuffle`
`Hash Shuffle`
`Hash Shuffle`
`Sort Shuffle`
`Sort Shuffle`