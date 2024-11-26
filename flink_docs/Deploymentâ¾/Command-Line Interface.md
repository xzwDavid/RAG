# Command-Line Interface


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Command-Line Interface#


Flink provides a Command-Line Interface (CLI) bin/flink to run programs that
are packaged as JAR files and to control their execution. The CLI is part of any
Flink setup, available in local single node setups and in distributed setups.
It connects to the running JobManager specified in Flink configuration file.

`bin/flink`

## Job Lifecycle Management#


A prerequisite for the commands listed in this section to work is to have a running Flink deployment
like Kubernetes,
YARN or any other option available. Feel free to
start a Flink cluster locally
to try the commands on your own machine.


### Submitting a Job#


Submitting a job means uploading the job’s JAR and related dependencies to the Flink cluster and
initiating the job execution. For the sake of this example, we select a long-running job like
examples/streaming/StateMachineExample.jar. Feel free to select any other JAR archive from the
examples/ folder or deploy your own job.

`examples/streaming/StateMachineExample.jar`
`examples/`

```
$ ./bin/flink run \
      --detached \
      ./examples/streaming/StateMachineExample.jar

```

`$ ./bin/flink run \
      --detached \
      ./examples/streaming/StateMachineExample.jar
`

Submitting the job using --detached will make the command return after the submission is done.
The output contains (besides other things) the ID of the newly submitted job.

`--detached`

```
Usage with built-in data generator: StateMachineExample [--error-rate <probability-of-invalid-transition>] [--sleep <sleep-per-record-in-ms>]
Usage with Kafka: StateMachineExample --kafka-topic <topic> [--brokers <brokers>]
Options for both the above setups:
        [--backend <file|rocks>]
        [--checkpoint-dir <filepath>]
        [--async-checkpoints <true|false>]
        [--incremental-checkpoints <true|false>]
        [--output <filepath> OR null for stdout]

Using standalone source with error rate 0.000000 and sleep delay 1 millis

Job has been submitted with JobID cca7bc1061d61cf15238e92312c2fc20

```

`Usage with built-in data generator: StateMachineExample [--error-rate <probability-of-invalid-transition>] [--sleep <sleep-per-record-in-ms>]
Usage with Kafka: StateMachineExample --kafka-topic <topic> [--brokers <brokers>]
Options for both the above setups:
        [--backend <file|rocks>]
        [--checkpoint-dir <filepath>]
        [--async-checkpoints <true|false>]
        [--incremental-checkpoints <true|false>]
        [--output <filepath> OR null for stdout]

Using standalone source with error rate 0.000000 and sleep delay 1 millis

Job has been submitted with JobID cca7bc1061d61cf15238e92312c2fc20
`

The usage information printed lists job-related parameters that can be added to the end of the job
submission command if necessary. For the purpose of readability, we assume that the returned JobID is
stored in a variable JOB_ID for the commands below:

`JOB_ID`

```
$ export JOB_ID="cca7bc1061d61cf15238e92312c2fc20"

```

`$ export JOB_ID="cca7bc1061d61cf15238e92312c2fc20"
`

The run command support passing additional configuration parameters via the
-D argument. For example setting the maximum parallelism
for a job can be done by setting -Dpipeline.max-parallelism=120. This argument is very useful for
configuring application mode clusters, because you can pass any configuration parameter
to the cluster without changing the configuration file.

`run`
`-D`
`-Dpipeline.max-parallelism=120`

When submitting a job to an existing session cluster, only execution configuration parameters are supported.


### Job Monitoring#


You can monitor any running jobs using the list action:

`list`

```
$ ./bin/flink list

```

`$ ./bin/flink list
`

```
Waiting for response...
------------------ Running/Restarting Jobs -------------------
30.11.2020 16:02:29 : cca7bc1061d61cf15238e92312c2fc20 : State machine job (RUNNING)
--------------------------------------------------------------
No scheduled jobs.

```

`Waiting for response...
------------------ Running/Restarting Jobs -------------------
30.11.2020 16:02:29 : cca7bc1061d61cf15238e92312c2fc20 : State machine job (RUNNING)
--------------------------------------------------------------
No scheduled jobs.
`

Jobs that were submitted but not started, yet, would be listed under “Scheduled Jobs”.


### Creating a Savepoint#


Savepoints can be created to save the current state a job is
in. All that’s needed is the JobID:


```
$ ./bin/flink savepoint \
      $JOB_ID \ 
      /tmp/flink-savepoints

```

`$ ./bin/flink savepoint \
      $JOB_ID \ 
      /tmp/flink-savepoints
`

```
Triggering savepoint for job cca7bc1061d61cf15238e92312c2fc20.
Waiting for response...
Savepoint completed. Path: file:/tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab
You can resume your program from this savepoint with the run command.

```

`Triggering savepoint for job cca7bc1061d61cf15238e92312c2fc20.
Waiting for response...
Savepoint completed. Path: file:/tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab
You can resume your program from this savepoint with the run command.
`

The savepoint folder is optional and needs to be specified if
execution.checkpointing.savepoint-dir isn’t set.


Lastly, you can optionally provide what should be the binary format of the savepoint.


The path to the savepoint can be used later on to restart the Flink job.


If the state of the job is quite big, the client will get a timeout exception since it should wait for the savepoint finished.


```
Triggering savepoint for job bec5244e09634ad71a80785937a9732d.
Waiting for response...

--------------------------------------------------------------
The program finished with the following exception:

org.apache.flink.util.FlinkException: Triggering a savepoint for the job bec5244e09634ad71a80785937a9732d failed.
        at org.apache.flink.client.cli.CliFrontend.triggerSavepoint(CliFrontend. java:828)
        at org.apache.flink.client.cli.CliFrontend.lambda$savepopint$8(CliFrontend.java:794)
        at org.apache.flink.client.cli.CliFrontend.runClusterAction(CliFrontend.java:1078)
        at org.apache.flink.client.cli.CliFrontend.savepoint(CliFrontend.java:779)
        at org.apache.flink.client.cli.CliFrontend.parseAndRun(CliFrontend.java:1150)
        at org.apache.flink.client.cli.CliFrontend.lambda$mainInternal$9(CliFrontend.java:1226)
        at org.apache.flink.runtime.security.contexts.NoOpSecurityContext.runSecured(NoOpSecurityContext.java:28)
        at org.apache.flink.client.cli.CliFrontend.mainInternal(CliFrontend.java:1226)
        at org.apache.flink.client.cli.CliFrontend.main(CliFronhtend.java:1194)
Caused by: java.util.concurrent.TimeoutException
        at java.util.concurrent.CompletableFuture.timedGet(CompletableFuture.java:1784)
        at java.util.concurrent.CompletableFuture.get(CompletableFuture.java:1928)
        at org.apache.flink.client.cli.CliFrontend.triggerSavepoint(CliFrontend.java:822)
        ... 8 more

```

`Triggering savepoint for job bec5244e09634ad71a80785937a9732d.
Waiting for response...

--------------------------------------------------------------
The program finished with the following exception:

org.apache.flink.util.FlinkException: Triggering a savepoint for the job bec5244e09634ad71a80785937a9732d failed.
        at org.apache.flink.client.cli.CliFrontend.triggerSavepoint(CliFrontend. java:828)
        at org.apache.flink.client.cli.CliFrontend.lambda$savepopint$8(CliFrontend.java:794)
        at org.apache.flink.client.cli.CliFrontend.runClusterAction(CliFrontend.java:1078)
        at org.apache.flink.client.cli.CliFrontend.savepoint(CliFrontend.java:779)
        at org.apache.flink.client.cli.CliFrontend.parseAndRun(CliFrontend.java:1150)
        at org.apache.flink.client.cli.CliFrontend.lambda$mainInternal$9(CliFrontend.java:1226)
        at org.apache.flink.runtime.security.contexts.NoOpSecurityContext.runSecured(NoOpSecurityContext.java:28)
        at org.apache.flink.client.cli.CliFrontend.mainInternal(CliFrontend.java:1226)
        at org.apache.flink.client.cli.CliFrontend.main(CliFronhtend.java:1194)
Caused by: java.util.concurrent.TimeoutException
        at java.util.concurrent.CompletableFuture.timedGet(CompletableFuture.java:1784)
        at java.util.concurrent.CompletableFuture.get(CompletableFuture.java:1928)
        at org.apache.flink.client.cli.CliFrontend.triggerSavepoint(CliFrontend.java:822)
        ... 8 more
`

In this case, we could use “-detached” option to trigger a detached savepoint, the client will return immediately as soon as the trigger id returns.


```
$ ./bin/flink savepoint \
      $JOB_ID \ 
      /tmp/flink-savepoints
      -detached

```

`$ ./bin/flink savepoint \
      $JOB_ID \ 
      /tmp/flink-savepoints
      -detached
`

```
Triggering savepoint in detached mode for job bec5244e09634ad71a80785937a9732d.
Successfully trigger manual savepoint, triggerId: 2505bbd12c5b58fd997d0f193db44b97

```

`Triggering savepoint in detached mode for job bec5244e09634ad71a80785937a9732d.
Successfully trigger manual savepoint, triggerId: 2505bbd12c5b58fd997d0f193db44b97
`

We could get the status of the detached savepoint by rest api.


#### Disposing a Savepoint#


The savepoint action can be also used to remove savepoints. --dispose with the corresponding
savepoint path needs to be added:

`savepoint`
`--dispose`

```
$ ./bin/flink savepoint \ 
      --dispose \
      /tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab \ 
      $JOB_ID

```

`$ ./bin/flink savepoint \ 
      --dispose \
      /tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab \ 
      $JOB_ID
`

```
Disposing savepoint '/tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab'.
Waiting for response...
Savepoint '/tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab' disposed.

```

`Disposing savepoint '/tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab'.
Waiting for response...
Savepoint '/tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab' disposed.
`

If you use custom state instances (for example custom reducing state or RocksDB state), you have to
specify the path to the program JAR with which the savepoint was triggered. Otherwise, you will run
into a ClassNotFoundException:

`ClassNotFoundException`

```
$ ./bin/flink savepoint \
      --dispose <savepointPath> \ 
      --jarfile <jarFile>

```

`$ ./bin/flink savepoint \
      --dispose <savepointPath> \ 
      --jarfile <jarFile>
`

Triggering the savepoint disposal through the savepoint action does not only remove the data from
the storage but makes Flink clean up the savepoint-related metadata as well.

`savepoint`

### Creating a Checkpoint#


Checkpoints can also be manually created to save the
current state. To get the difference between checkpoint and savepoint, please refer to
Checkpoints vs. Savepoints. All that’s
needed to trigger a checkpoint manually is the JobID:


```
$ ./bin/flink checkpoint \
      $JOB_ID

```

`$ ./bin/flink checkpoint \
      $JOB_ID
`

```
Triggering checkpoint for job 99c59fead08c613763944f533bf90c0f.
Waiting for response...
Checkpoint(CONFIGURED) 26 for job 99c59fead08c613763944f533bf90c0f completed.
You can resume your program from this checkpoint with the run command.

```

`Triggering checkpoint for job 99c59fead08c613763944f533bf90c0f.
Waiting for response...
Checkpoint(CONFIGURED) 26 for job 99c59fead08c613763944f533bf90c0f completed.
You can resume your program from this checkpoint with the run command.
`

If you want to trigger a full checkpoint while the job periodically triggering incremental checkpoints,
please use the --full option.

`--full`

```
$ ./bin/flink checkpoint \
      $JOB_ID \
      --full

```

`$ ./bin/flink checkpoint \
      $JOB_ID \
      --full
`

```
Triggering checkpoint for job 99c59fead08c613763944f533bf90c0f.
Waiting for response...
Checkpoint(FULL) 78 for job 99c59fead08c613763944f533bf90c0f completed.
You can resume your program from this checkpoint with the run command.

```

`Triggering checkpoint for job 99c59fead08c613763944f533bf90c0f.
Waiting for response...
Checkpoint(FULL) 78 for job 99c59fead08c613763944f533bf90c0f completed.
You can resume your program from this checkpoint with the run command.
`

### Terminating a Job#


#### Stopping a Job Gracefully Creating a Final Savepoint#


Another action for stopping a job is stop. It is a more graceful way of stopping a running streaming
job as the stop  flows from source to sink. When the user requests to stop a job, all sources will
be requested to send the last checkpoint barrier that will trigger a savepoint, and after the successful
completion of that savepoint, they will finish by calling their cancel() method.

`stop`
`stop`
`cancel()`

```
$ ./bin/flink stop \
      --savepointPath /tmp/flink-savepoints \
      $JOB_ID

```

`$ ./bin/flink stop \
      --savepointPath /tmp/flink-savepoints \
      $JOB_ID
`

```
Suspending job "cca7bc1061d61cf15238e92312c2fc20" with a savepoint.
Savepoint completed. Path: file:/tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab

```

`Suspending job "cca7bc1061d61cf15238e92312c2fc20" with a savepoint.
Savepoint completed. Path: file:/tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab
`

We have to use --savepointPath to specify the savepoint folder if
execution.checkpointing.savepoint-dir isn’t set.

`--savepointPath`

If the --drain flag is specified, then a MAX_WATERMARK will be emitted before the last checkpoint
barrier. This will make all registered event-time timers fire, thus flushing out any state that
is waiting for a specific watermark, e.g. windows. The job will keep running until all sources properly
shut down. This allows the job to finish processing all in-flight data, which can produce some
records to process after the savepoint taken while stopping.

`--drain`
`MAX_WATERMARK`

> 
  Use the --drain flag if you want to terminate the job permanently.
If you want to resume the job at a later point in time, then do not drain the pipeline because it could lead to incorrect results when the job is resumed.


`--drain`

If you want to trigger the savepoint in detached mode, add option -detached to the command.

`-detached`

Lastly, you can optionally provide what should be the binary format of the savepoint.


#### Cancelling a Job Ungracefully#


Cancelling a job can be achieved through the cancel action:

`cancel`

```
$ ./bin/flink cancel $JOB_ID

```

`$ ./bin/flink cancel $JOB_ID
`

```
Cancelling job cca7bc1061d61cf15238e92312c2fc20.
Cancelled job cca7bc1061d61cf15238e92312c2fc20.

```

`Cancelling job cca7bc1061d61cf15238e92312c2fc20.
Cancelled job cca7bc1061d61cf15238e92312c2fc20.
`

The corresponding job’s state will be transitioned from Running to Cancelled. Any computations
will be stopped.

`Running`
`Cancelled`

> 
  The --withSavepoint flag allows creating a savepoint as part of the job cancellation.
This feature is deprecated.
Use the stop action instead.


`--withSavepoint`

### Starting a Job from a Savepoint#


Starting a job from a savepoint can be achieved using the run action.

`run`

```
$ ./bin/flink run \
      --detached \ 
      --fromSavepoint /tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab \
      ./examples/streaming/StateMachineExample.jar

```

`$ ./bin/flink run \
      --detached \ 
      --fromSavepoint /tmp/flink-savepoints/savepoint-cca7bc-bb1e257f0dab \
      ./examples/streaming/StateMachineExample.jar
`

```
Usage with built-in data generator: StateMachineExample [--error-rate <probability-of-invalid-transition>] [--sleep <sleep-per-record-in-ms>]
Usage with Kafka: StateMachineExample --kafka-topic <topic> [--brokers <brokers>]
Options for both the above setups:
        [--backend <file|rocks>]
        [--checkpoint-dir <filepath>]
        [--async-checkpoints <true|false>]
        [--incremental-checkpoints <true|false>]
        [--output <filepath> OR null for stdout]

Using standalone source with error rate 0.000000 and sleep delay 1 millis

Job has been submitted with JobID 97b20a0a8ffd5c1d656328b0cd6436a6

```

`Usage with built-in data generator: StateMachineExample [--error-rate <probability-of-invalid-transition>] [--sleep <sleep-per-record-in-ms>]
Usage with Kafka: StateMachineExample --kafka-topic <topic> [--brokers <brokers>]
Options for both the above setups:
        [--backend <file|rocks>]
        [--checkpoint-dir <filepath>]
        [--async-checkpoints <true|false>]
        [--incremental-checkpoints <true|false>]
        [--output <filepath> OR null for stdout]

Using standalone source with error rate 0.000000 and sleep delay 1 millis

Job has been submitted with JobID 97b20a0a8ffd5c1d656328b0cd6436a6
`

See how the command is equal to the initial run command except for the
--fromSavepoint parameter which is used to refer to the state of the
previously stopped job. A new JobID is
generated that can be used to maintain the job.

`--fromSavepoint`

By default, we try to match the whole savepoint state to the job being submitted. If you want to
allow to skip savepoint state that cannot be restored with the new job you can set the
--allowNonRestoredState flag. You need to allow this if you removed an operator from your program
that was part of the program when the savepoint was triggered and you still want to use the savepoint.

`--allowNonRestoredState`

```
$ ./bin/flink run \
      --fromSavepoint <savepointPath> \
      --allowNonRestoredState ...

```

`$ ./bin/flink run \
      --fromSavepoint <savepointPath> \
      --allowNonRestoredState ...
`

This is useful if your program dropped an operator that was part of the savepoint.


You can also select the claim mode
which should be used for the savepoint. The mode controls who takes ownership of the files of
the specified savepoint.


 Back to top


## CLI Actions#


Here’s an overview of actions supported by Flink’s CLI tool:

`run`
`info`
`list`
`savepoint`
`Flink configuration file`
`checkpoint`
`cancel`
`stop`
`cancel`
`savepoint`

A more fine-grained description of all actions and their parameters can be accessed through bin/flink --help
or the usage information of each individual action bin/flink <action> --help.

`bin/flink --help`
`bin/flink <action> --help`

 Back to top


## Advanced CLI#


### REST API#


The Flink cluster can be also managed using the REST API. The commands
described in previous sections are a subset of what is offered by Flink’s REST endpoints. Therefore,
tools like curl can be used to get even more out of Flink.

`curl`

### Selecting Deployment Targets#


Flink is compatible with multiple cluster management frameworks like
Kubernetes or
YARN which are described in more detail in the
Resource Provider section. Jobs can be submitted in different Deployment Modes.
The parameterization of a job submission differs based on the underlying framework and Deployment Mode.


bin/flink offers a parameter --target to handle the different options. In addition to that, jobs
have to be submitted using either run (for Session
and Per-Job Mode (deprecated)) or run-application (for
Application Mode). See the following summary of
parameter combinations:

`bin/flink`
`--target`
`run`
`run-application`
* YARN

./bin/flink run --target yarn-session: Submission to an already running Flink on YARN cluster
./bin/flink run --target yarn-application: Submission spinning up Flink on YARN cluster in Application Mode


* Kubernetes

./bin/flink run --target kubernetes-session: Submission to an already running Flink on Kubernetes cluster
./bin/flink run --target kubernetes-application: Submission spinning up a Flink on Kubernetes cluster in Application Mode


* Standalone:

./bin/flink run --target local: Local submission using a MiniCluster in Session Mode
./bin/flink run --target remote: Submission to an already running Flink cluster


* ./bin/flink run --target yarn-session: Submission to an already running Flink on YARN cluster
* ./bin/flink run --target yarn-application: Submission spinning up Flink on YARN cluster in Application Mode
`./bin/flink run --target yarn-session`
`./bin/flink run --target yarn-application`
* ./bin/flink run --target kubernetes-session: Submission to an already running Flink on Kubernetes cluster
* ./bin/flink run --target kubernetes-application: Submission spinning up a Flink on Kubernetes cluster in Application Mode
`./bin/flink run --target kubernetes-session`
`./bin/flink run --target kubernetes-application`
* ./bin/flink run --target local: Local submission using a MiniCluster in Session Mode
* ./bin/flink run --target remote: Submission to an already running Flink cluster
`./bin/flink run --target local`
`./bin/flink run --target remote`

The --target will overwrite the execution.target
specified in the Flink configuration file.

`--target`

For more details on the commands and the available options, please refer to the Resource Provider-specific
pages of the documentation.


### Submitting PyFlink Jobs#


Currently, users are able to submit a PyFlink job via the CLI. It does not require to specify the
JAR file path or the entry main class, which is different from the Java job submission.


> 
  When submitting Python job via flink run, Flink will run the command “python”. Please run the following command to confirm that the python executable in current environment points to a supported Python version of 3.8+.


`flink run`

```
$ python --version
# the version printed here must be 3.8+

```

`$ python --version
# the version printed here must be 3.8+
`

The following commands show different PyFlink job submission use-cases:

* Run a PyFlink job:

```
$ ./bin/flink run --python examples/python/table/word_count.py

```

`$ ./bin/flink run --python examples/python/table/word_count.py
`
* Run a PyFlink job with additional source and resource files. Files specified in --pyFiles will be
added to the PYTHONPATH and, therefore, available in the Python code.
`--pyFiles`
`PYTHONPATH`

```
$ ./bin/flink run \
      --python examples/python/table/word_count.py \
      --pyFiles file:///user.txt,hdfs:///$namenode_address/username.txt

```

`$ ./bin/flink run \
      --python examples/python/table/word_count.py \
      --pyFiles file:///user.txt,hdfs:///$namenode_address/username.txt
`
* Run a PyFlink job which will reference Java UDF or external connectors. JAR file specified in --jarfile will be uploaded
to the cluster.
`--jarfile`

```
$ ./bin/flink run \
      --python examples/python/table/word_count.py \
      --jarfile <jarFile>

```

`$ ./bin/flink run \
      --python examples/python/table/word_count.py \
      --jarfile <jarFile>
`
* Run a PyFlink job with pyFiles and the main entry module specified in --pyModule:
`--pyModule`

```
$ ./bin/flink run \
      --pyModule word_count \
      --pyFiles examples/python/table

```

`$ ./bin/flink run \
      --pyModule word_count \
      --pyFiles examples/python/table
`
* Submit a PyFlink job on a specific JobManager running on host <jobmanagerHost> (adapt the command accordingly):
`<jobmanagerHost>`

```
$ ./bin/flink run \
      --jobmanager <jobmanagerHost>:8081 \
      --python examples/python/table/word_count.py

```

`$ ./bin/flink run \
      --jobmanager <jobmanagerHost>:8081 \
      --python examples/python/table/word_count.py
`
* Run a PyFlink job using a YARN cluster in Per-Job Mode:

```
$ ./bin/flink run \
      --target yarn-per-job
      --python examples/python/table/word_count.py

```

`$ ./bin/flink run \
      --target yarn-per-job
      --python examples/python/table/word_count.py
`
* Run a PyFlink job using a YARN cluster in Application Mode:

```
$ ./bin/flink run -t yarn-application \
      -Djobmanager.memory.process.size=1024m \
      -Dtaskmanager.memory.process.size=1024m \
      -Dyarn.application.name=<ApplicationName> \
      -Dyarn.ship-files=/path/to/shipfiles \
      -pyarch shipfiles/venv.zip \
      -pyclientexec venv.zip/venv/bin/python3 \
      -pyexec venv.zip/venv/bin/python3 \
      -pyfs shipfiles \
      -pym word_count

```

`$ ./bin/flink run -t yarn-application \
      -Djobmanager.memory.process.size=1024m \
      -Dtaskmanager.memory.process.size=1024m \
      -Dyarn.application.name=<ApplicationName> \
      -Dyarn.ship-files=/path/to/shipfiles \
      -pyarch shipfiles/venv.zip \
      -pyclientexec venv.zip/venv/bin/python3 \
      -pyexec venv.zip/venv/bin/python3 \
      -pyfs shipfiles \
      -pym word_count
`

Note It assumes that the Python dependencies needed to execute the job are already placed in the directory /path/to/shipfiles. For example, it should contain venv.zip and word_count.py for the above example.

`/path/to/shipfiles`

Note As it executes the job on the JobManager in YARN application mode, the paths specified in -pyarch and -pyfs are paths relative to shipfiles which is the directory name of the shipped files.
It’s suggested to use -pym to specify the program entrypoint instead of -py as it’s impossible to know either the absolute path, or the relative path of the entrypoint program.

`-pyarch`
`-pyfs`
`shipfiles`
`-pym`
`-py`

Note The archive files specified via -pyarch will be distributed to the TaskManagers through blob server where the file size limit is 2 GB.
If the size of an archive file is more than 2 GB, you could upload it to a distributed file system and then use the path in the command line option -pyarch.

`-pyarch`
`-pyarch`
* Run a PyFlink application on a native Kubernetes cluster having the cluster ID <ClusterId>, it requires a docker image with PyFlink installed, please refer to Enabling PyFlink in docker:
`<ClusterId>`

```
$ ./bin/flink run \
      --target kubernetes-application \
      --parallelism 8 \
      -Dkubernetes.cluster-id=<ClusterId> \
      -Dtaskmanager.memory.process.size=4096m \
      -Dkubernetes.taskmanager.cpu=2 \
      -Dtaskmanager.numberOfTaskSlots=4 \
      -Dkubernetes.container.image.ref=<PyFlinkImageName> \
      --pyModule word_count \
      --pyFiles /opt/flink/examples/python/table/word_count.py

```

`$ ./bin/flink run \
      --target kubernetes-application \
      --parallelism 8 \
      -Dkubernetes.cluster-id=<ClusterId> \
      -Dtaskmanager.memory.process.size=4096m \
      -Dkubernetes.taskmanager.cpu=2 \
      -Dtaskmanager.numberOfTaskSlots=4 \
      -Dkubernetes.container.image.ref=<PyFlinkImageName> \
      --pyModule word_count \
      --pyFiles /opt/flink/examples/python/table/word_count.py
`

To learn more available options, please refer to Kubernetes
or YARN which are described in more detail in the
Resource Provider section.


Besides --pyFiles, --pyModule and --python mentioned above, there are also some other Python
related options. Here’s an overview of all the Python related options for the actions
run supported by Flink’s CLI tool:

`--pyFiles`
`--pyModule`
`--python`
`run`
`-py,--python`
`--pyFiles`
`-pym,--pyModule`
`--pyFiles`
`-pyfs,--pyFiles`
`-pyarch,--pyArchives`
`-pyclientexec,--pyClientExecutable`
`-pyexec,--pyExecutable`
`-pyreq,--pyRequirements`

In addition to the command line options during submitting the job, it also supports to specify the
dependencies via configuration or Python API inside the code. Please refer to the
dependency management for more details.


 Back to top
