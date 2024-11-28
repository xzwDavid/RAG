# Profiler


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Profiler#


Since Flink 1.19, we support profiling the JobManager/TaskManager process interactively with async-profiler via Flink Web UI, which allows users to create a profiling instance with arbitrary intervals and event modes, e.g ITIMER, CPU, Lock, Wall-Clock and Allocation.

* CPU: In this mode the profiler collects stack trace samples that include Java methods, native calls, JVM code and kernel functions.
* ALLOCATION: In allocation profiling mode, the top frame of every call trace is the class of the allocated object, and the counter is the heap pressure (the total size of allocated TLABs or objects outside TLAB).
* Wall-clock: Wall-Clock option tells async-profiler to sample all threads equally every given period of time regardless of thread status: Running, Sleeping or Blocked. For instance, this can be helpful when profiling application start-up time.
* Lock: In lock profiling mode the top frame is the class of lock/monitor, and the counter is number of nanoseconds it took to enter this lock/monitor.
* ITIMER: You can fall back to itimer profiling mode. It is similar to cpu mode, but does not require perf_events support. As a drawback, there will be no kernel stack traces.

> 
  Any measurement process in and of itself inevitably affects the subject of measurement. In order to prevent unintended impacts on production environments, Profiler are currently available as an opt-in feature. To enable it, you’ll need to set rest.profiling.enabled: true in Flink configuration file. We recommend enabling it in development and pre-production environments, but you should treat it as an experimental feature in production.


`rest.profiling.enabled: true`

## Requirements#


Since the Profiler is powered by the Async-profiler, it is required to work on platforms that are supported by the Async-profiler.


Profiling on platforms beyond those listed above will fail with an error message in the Message column.

`Message`

## Usage#


Flink users can complete the profiling submission and result export via Flink Web UI conveniently.


For example,

* First, you should find out the candidate TaskManager/JobManager with performance bottleneck for profiling, and switch to the corresponding TaskManager/JobManager page (profiler tab).
* You can submit a profiling instance with a specified duration and mode by simply clicking on the button Create Profiling Instance. (The description of the profiling mode will be shown when hovering over the corresponding mode.)
* Once the profiling instance is complete, you can easily download the interactive HTML file by clicking on the link.

## Troubleshooting#

1. 
Failed to profiling in CPU mode: No access to perf events. Try –fdtransfer or –all-user option or ‘sysctl kernel.perf_event_paranoid=1’ 
That means perf_event_open() syscall has failed. By default, Docker container restricts the access to perf_event_open syscall. The recommended solution is to fall back to ITIMER profiling mode. It is similar to CPU mode, but does not require perf_events support. As a drawback, there will be no kernel stack traces.

2. 
Failed to profiling in Allocation mode: No AllocTracer symbols found. Are JDK debug symbols installed? 
The OpenJDK debug symbols are required for allocation profiling. See Installing Debug Symbols for more details.


Failed to profiling in CPU mode: No access to perf events. Try –fdtransfer or –all-user option or ‘sysctl kernel.perf_event_paranoid=1’ 
That means perf_event_open() syscall has failed. By default, Docker container restricts the access to perf_event_open syscall. The recommended solution is to fall back to ITIMER profiling mode. It is similar to CPU mode, but does not require perf_events support. As a drawback, there will be no kernel stack traces.

`perf_event_open()`
`perf_event_open`
`perf_events`

Failed to profiling in Allocation mode: No AllocTracer symbols found. Are JDK debug symbols installed? 
The OpenJDK debug symbols are required for allocation profiling. See Installing Debug Symbols for more details.


> 
  You can refer to the Troubleshooting page of async-profiler for more cases.

