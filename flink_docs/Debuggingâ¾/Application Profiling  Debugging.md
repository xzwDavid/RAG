# Application Profiling & Debugging


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Application Profiling & Debugging#


## Overview of Custom Logging with Apache Flink#


Each standalone JobManager, TaskManager, HistoryServer, and ZooKeeper daemon redirects stdout and stderr to a file
with a .out filename suffix and writes internal logging to a file with a .log suffix. Java options configured by the
user in env.java.opts.all, env.java.opts.jobmanager, env.java.opts.taskmanager, env.java.opts.historyserver and
env.java.opts.client can likewise define log files with
use of the script variable FLINK_LOG_PREFIX and by enclosing the options in double quotes for late evaluation. Log files
using FLINK_LOG_PREFIX are rotated along with the default .out and .log files.

`stdout`
`stderr`
`.out`
`.log`
`env.java.opts.all`
`env.java.opts.jobmanager`
`env.java.opts.taskmanager`
`env.java.opts.historyserver`
`env.java.opts.client`
`FLINK_LOG_PREFIX`
`FLINK_LOG_PREFIX`
`.out`
`.log`

## Profiling with Java Flight Recorder#


Java Flight Recorder is a profiling and event collection framework built into the Oracle JDK.
Java Mission Control
is an advanced set of tools that enables efficient and detailed analysis of the extensive of data collected by Java
Flight Recorder. Example configuration:


```
env.java.opts.all: "-XX:+UnlockCommercialFeatures -XX:+UnlockDiagnosticVMOptions -XX:+FlightRecorder -XX:+DebugNonSafepoints -XX:FlightRecorderOptions=defaultrecording=true,dumponexit=true,dumponexitpath=${FLINK_LOG_PREFIX}.jfr"

```

`env.java.opts.all: "-XX:+UnlockCommercialFeatures -XX:+UnlockDiagnosticVMOptions -XX:+FlightRecorder -XX:+DebugNonSafepoints -XX:FlightRecorderOptions=defaultrecording=true,dumponexit=true,dumponexitpath=${FLINK_LOG_PREFIX}.jfr"
`

## Profiling with JITWatch#


JITWatch is a log analyser and visualizer for the Java HotSpot JIT
compiler used to inspect inlining decisions, hot methods, bytecode, and assembly. Example configuration:


```
env.java.opts.all: "-XX:+UnlockDiagnosticVMOptions -XX:+TraceClassLoading -XX:+LogCompilation -XX:LogFile=${FLINK_LOG_PREFIX}.jit -XX:+PrintAssembly"

```

`env.java.opts.all: "-XX:+UnlockDiagnosticVMOptions -XX:+TraceClassLoading -XX:+LogCompilation -XX:LogFile=${FLINK_LOG_PREFIX}.jit -XX:+PrintAssembly"
`

## Analyzing Out of Memory Problems#


If you encounter OutOfMemoryExceptions with your Flink application, then it is a good idea to enable heap dumps on out of memory errors.

`OutOfMemoryExceptions`

```
env.java.opts.all: "-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=${FLINK_LOG_PREFIX}.hprof"

```

`env.java.opts.all: "-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=${FLINK_LOG_PREFIX}.hprof"
`

The heap dump will allow you to analyze potential memory leaks in your user code.
If the memory leak should be caused by Flink, then please reach out to the dev mailing list.


## Analyzing Memory & Garbage Collection Behaviour#


Memory usage and garbage collection can have a profound impact on your application.
The effects can range from slight performance degradation to a complete cluster failure if the GC pauses are too long.
If you want to better understand the memory and GC behaviour of your application, then you can enable memory logging on the TaskManagers.

`TaskManagers`

```
taskmanager.debug.memory.log: true
taskmanager.debug.memory.log-interval: 10000 // 10s interval

```

`taskmanager.debug.memory.log: true
taskmanager.debug.memory.log-interval: 10000 // 10s interval
`

If you are interested in more detailed GC statistics, then you can activate the JVM’s GC logging via:


```
env.java.opts.all: "-Xloggc:${FLINK_LOG_PREFIX}.gc.log -XX:+PrintGCApplicationStoppedTime -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=10M -XX:+PrintPromotionFailure -XX:+PrintGCCause"

```

`env.java.opts.all: "-Xloggc:${FLINK_LOG_PREFIX}.gc.log -XX:+PrintGCApplicationStoppedTime -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=10M -XX:+PrintPromotionFailure -XX:+PrintGCCause"
`

 Back to top
