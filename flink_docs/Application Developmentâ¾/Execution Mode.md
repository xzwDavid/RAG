# Execution Mode


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Execution Mode#


The Python API supports different runtime execution modes from which you can choose depending on the
requirements of your use case and the characteristics of your job. The Python runtime execution mode
defines how the Python user-defined functions will be executed.


Prior to release-1.15, there is the only execution mode called PROCESS execution mode. The PROCESS
mode means that the Python user-defined functions will be executed in separate Python processes.

`PROCESS`
`PROCESS`

In release-1.15, it has introduced a new execution mode called THREAD execution mode. The THREAD
mode means that the Python user-defined functions will be executed in JVM.

`THREAD`
`THREAD`

NOTE: Multiple Python user-defined functions running in the same JVM are still affected by GIL.


## When can/should I use THREAD execution mode?#


The purpose of the introduction of THREAD mode is to overcome the overhead of serialization/deserialization
and network communication introduced of inter-process communication in the PROCESS mode.
So if performance is not your concern, or the computing logic of your Python user-defined functions is the performance bottleneck of the job,
PROCESS mode will be the best choice as PROCESS mode provides the best isolation compared to THREAD mode.

`THREAD`
`PROCESS`
`PROCESS`
`PROCESS`
`THREAD`

## Configuring Python execution mode#


The execution mode can be configured via the python.execution-mode setting.
There are two possible values:

`python.execution-mode`
* PROCESS: The Python user-defined functions will be executed in separate Python process. (default)
* THREAD: The Python user-defined functions will be executed in JVM.
`PROCESS`
`THREAD`

You could specify the execution mode in Python Table API or Python DataStream API jobs as following:


```
## Python Table API
# Specify `PROCESS` mode
table_env.get_config().set("python.execution-mode", "process")

# Specify `THREAD` mode
table_env.get_config().set("python.execution-mode", "thread")


## Python DataStream API

config = Configuration()

# Specify `PROCESS` mode
config.set_string("python.execution-mode", "process")

# Specify `THREAD` mode
config.set_string("python.execution-mode", "thread")

# Create the corresponding StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment(config)

```

`## Python Table API
# Specify `PROCESS` mode
table_env.get_config().set("python.execution-mode", "process")

# Specify `THREAD` mode
table_env.get_config().set("python.execution-mode", "thread")


## Python DataStream API

config = Configuration()

# Specify `PROCESS` mode
config.set_string("python.execution-mode", "process")

# Specify `THREAD` mode
config.set_string("python.execution-mode", "thread")

# Create the corresponding StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment(config)
`

## Supported Cases#


### Python Table API#


The following table shows where the THREAD execution mode is supported in Python Table API.

`THREAD`
`PROCESS`
`THREAD`

### Python DataStream API#


The following table shows where the PROCESS execution mode and the THREAD execution mode are supported in Python DataStream API.

`PROCESS`
`THREAD`
`PROCESS`
`THREAD`


  Currently, it still doesn’t support to execute Python UDFs in THREAD execution mode in all places.
It will fall back to PROCESS execution mode in these cases. So it may happen that you configure a job
to execute in THREAD execution mode, however, it’s actually executed in PROCESS execution mode.


THREAD execution mode is only supported in Python 3.8+.




> 
  Currently, it still doesn’t support to execute Python UDFs in THREAD execution mode in all places.
It will fall back to PROCESS execution mode in these cases. So it may happen that you configure a job
to execute in THREAD execution mode, however, it’s actually executed in PROCESS execution mode.


`THREAD`
`PROCESS`
`THREAD`
`PROCESS`

> 
THREAD execution mode is only supported in Python 3.8+.


`THREAD`

## Execution Behavior#


This section provides an overview of the execution behavior of THREAD execution mode and contrasts
they with PROCESS execution mode. For more details, please refer to the FLIP that introduced this feature:
FLIP-206.

`THREAD`
`PROCESS`

#### PROCESS Execution Mode#


In PROCESS execution mode, the Python user-defined functions will be executed in separate Python Worker process.
The Java operator process communicates with the Python worker process using various Grpc services.

`PROCESS`

#### THREAD Execution Mode#


In THREAD execution mode, the Python user-defined functions will be executed in the same process
as Java operators. PyFlink takes use of third part library PEMJA
to embed Python in Java Application.

`THREAD`