# Working Directory


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Working Directory#


Flink supports to configure a working directory (FLIP-198) for Flink processes (JobManager and TaskManager).
The working directory is used by the processes to store information that can be recovered upon a process restart.
The requirement for this to work is that the process is started with the same identity and has access to the volume on which the working directory is stored.


## Configuring the Working Directory#


The working directories for the Flink processes are:

* JobManager working directory: <WORKING_DIR_BASE>/jm_<JM_RESOURCE_ID>
* TaskManager working directory: <WORKING_DIR_BASE>/tm_<TM_RESOURCE_ID>
`<WORKING_DIR_BASE>/jm_<JM_RESOURCE_ID>`
`<WORKING_DIR_BASE>/tm_<TM_RESOURCE_ID>`

with <WORKING_DIR_BASE> being the working directory base, <JM_RESOURCE_ID> being the resource id of the JobManager process and <TM_RESOURCE_ID> being the resource id of the TaskManager process.

`<WORKING_DIR_BASE>`
`<JM_RESOURCE_ID>`
`<TM_RESOURCE_ID>`

The <WORKING_DIR_BASE> can be configured by process.working-dir.
It needs to point to a local directory.
If not explicitly configured, then it defaults to a randomly picked directory from io.tmp.dirs.

`<WORKING_DIR_BASE>`
`process.working-dir`
`io.tmp.dirs`

It is also possible to configure a JobManager and TaskManager specific <WORKING_DIR_BASE> via process.jobmanager.working-dir and process.taskmanager.working-dir respectively.

`<WORKING_DIR_BASE>`
`process.jobmanager.working-dir`
`process.taskmanager.working-dir`

The JobManager resource id can be configured via jobmanager.resource-id.
If not explicitly configured, then it will be a random UUID.

`jobmanager.resource-id`

Similarly, the TaskManager resource id can be configured via taskmanager.resource-id.
If not explicitly configured, then it will be a random value containing the host and port of the running process.

`taskmanager.resource-id`

## Artifacts Stored in the Working Directory#


Flink processes will use the working directory to store the following artifacts:

* Blobs stored by the BlobServer and BlobCache
* Local state if state.backend.local-recovery is enabled
* RocksDB’s working directory
`BlobServer`
`BlobCache`
`state.backend.local-recovery`

## Local Recovery Across Process Restarts#


The working directory can be used to enable local recovery across process restarts (FLIP-201).
This means that Flink does not have to recover state information from remote storage.


In order to use this feature, local recovery has to be enabled via state.backend.local-recovery.
Moreover, the TaskManager processes need to get a deterministic resource id assigned via taskmanager.resource-id.
Last but not least, a failed TaskManager process needs to be restarted with the same working directory.

`state.backend.local-recovery`
`taskmanager.resource-id`

```
process.working-dir: /path/to/working/dir/base
state.backend.local-recovery: true
taskmanager.resource-id: TaskManager_1 # important: Change for every TaskManager process

```

`process.working-dir: /path/to/working/dir/base
state.backend.local-recovery: true
taskmanager.resource-id: TaskManager_1 # important: Change for every TaskManager process
`

 Back to top
