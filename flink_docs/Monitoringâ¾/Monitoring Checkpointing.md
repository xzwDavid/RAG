# Monitoring Checkpointing


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Monitoring Checkpointing#


## Overview#


Flink’s web interface provides a tab to monitor the checkpoints of jobs. These stats are also available after the job has terminated. There are four different tabs to display information about your checkpoints: Overview, History, Summary, and Configuration. The following sections will cover all of these in turn.


## Monitoring#


### Overview Tab#


The overview tabs lists the following statistics. Note that these statistics don’t survive a JobManager loss and are reset if your JobManager fails over.

* Checkpoint Counts

Triggered: The total number of checkpoints that have been triggered since the job started.
In Progress: The current number of checkpoints that are in progress.
Completed: The total number of successfully completed checkpoints since the job started.
Failed: The total number of failed checkpoints since the job started.
Restored: The number of restore operations since the job started. This also tells you how many times the job has restarted since submission. Note that the initial submission with a savepoint also counts as a restore and the count is reset if the JobManager was lost during operation.


* Latest Completed Checkpoint: The latest successfully completed checkpoints. Clicking on More details gives you detailed statistics down to the subtask level.
* Latest Failed Checkpoint: The latest failed checkpoint. Clicking on More details gives you detailed statistics down to the subtask level.
* Latest Savepoint: The latest triggered savepoint with its external path. Clicking on More details gives you detailed statistics down to the subtask level.
* Latest Restore: There are two types of restore operations.

Restore from Checkpoint: We restored from a regular periodic checkpoint.
Restore from Savepoint: We restored from a savepoint.


* Triggered: The total number of checkpoints that have been triggered since the job started.
* In Progress: The current number of checkpoints that are in progress.
* Completed: The total number of successfully completed checkpoints since the job started.
* Failed: The total number of failed checkpoints since the job started.
* Restored: The number of restore operations since the job started. This also tells you how many times the job has restarted since submission. Note that the initial submission with a savepoint also counts as a restore and the count is reset if the JobManager was lost during operation.
`More details`
`More details`
`More details`
* Restore from Checkpoint: We restored from a regular periodic checkpoint.
* Restore from Savepoint: We restored from a savepoint.

### History Tab#


The checkpoint history keeps statistics about recently triggered checkpoints, including those that are currently in progress.


Note that for failed checkpoints, metrics are updated on a best efforts basis and may be not accurate.

* ID: The ID of the triggered checkpoint. The IDs are incremented for each checkpoint, starting at 1.
* Status: The current status of the checkpoint, which is either In Progress, Completed, or Failed. If the triggered checkpoint is a savepoint, you will see a floppy-disk symbol.
* Acknowledged: The number of acknowledged subtask with total subtask.
* Trigger Time: The time when the checkpoint was triggered at the JobManager.
* Latest Acknowledgement: The time when the latest acknowledgement for any subtask was received at the JobManager (or n/a if no acknowledgement received yet).
* End to End Duration: The duration from the trigger timestamp until the latest acknowledgement (or n/a if no acknowledgement received yet). This end to end duration for a complete checkpoint is determined by the last subtask that acknowledges the checkpoint. This time is usually larger than single subtasks need to actually checkpoint the state.
* Checkpointed Data Size: The persisted data size during the sync and async phases of that checkpoint, the value could be different from full checkpoint data size if incremental checkpoint or changelog is enabled.
* Full Checkpoint Data Size: The accumulated checkpoint data size over all acknowledged subtasks.
* Processed (persisted) in-flight data: The approximate number of bytes processed/persisted during the alignment (time between receiving the first and the last checkpoint barrier) over all acknowledged subtasks. Persisted data could be larger than zero only if the unaligned checkpoints are enabled.

For subtasks there are a couple of more detailed stats available.

* Sync Duration: The duration of the synchronous part of the checkpoint. This includes snapshotting state of the operators and blocks all other activity on the subtask (processing records, firing timers, etc).
* Async Duration: The duration of the asynchronous part of the checkpoint. This includes time it took to write the checkpoint on to the selected filesystem. For unaligned checkpoints this also includes also the time the subtask had to wait for last of the checkpoint barriers to arrive (alignment duration) and the time it took to persist the in-flight data.
* Alignment Duration: The time between processing the first and the last checkpoint barrier. For aligned checkpoints, during the alignment, the channels that have already received checkpoint barrier are blocked from processing more data.
* Start Delay: The time it took for the first checkpoint barrier to reach this subtask since the checkpoint barrier has been created.
* Unaligned Checkpoint: Whether the checkpoint for the subtask is completed as an unaligned checkpoint. An aligned checkpoint can switch to an unaligned checkpoint if the alignment timeouts.

#### History Size Configuration#


You can configure the number of recent checkpoints that are remembered for the history via the following configuration key. The default is 10.

`10`

```
# Number of recent checkpoints that are remembered
web.checkpoints.history: 15

```

`# Number of recent checkpoints that are remembered
web.checkpoints.history: 15
`

### Summary Tab#


The summary computes a simple min/average/maximum statistics over all completed checkpoints for the End to End Duration, Incremental Checkpoint Data Size, Full Checkpoint Data Size, and Bytes Buffered During Alignment (see History for details about what these mean).


Note that these statistics don’t survive a JobManager loss and are reset if your JobManager fails over.


### Configuration Tab#


The configuration list your streaming configuration:

* Checkpointing Mode: Either Exactly Once or At least Once.
* Interval: The configured checkpointing interval. Trigger checkpoints in this interval.
* Timeout: Timeout after which a checkpoint is cancelled by the JobManager and a new checkpoint is triggered.
* Minimum Pause Between Checkpoints: Minimum required pause between checkpoints. After a checkpoint has completed successfully, we wait at least for this amount of time before triggering the next one, potentially delaying the regular interval.
* Maximum Concurrent Checkpoints: The maximum number of checkpoints that can be in progress concurrently.
* Persist Checkpoints Externally: Enabled or Disabled. If enabled, furthermore lists the cleanup config for externalized checkpoints (delete or retain on cancellation).

### Checkpoint Details#


When you click on a More details link for a checkpoint, you get a Minimum/Average/Maximum summary over all its operators and also the detailed numbers per single subtask.


#### Summary per Operator#


#### All Subtask Statistics#


 Back to top
