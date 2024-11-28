# Monitoring Back Pressure


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Monitoring Back Pressure#


Flink’s web interface provides a tab to monitor the back pressure behaviour of running jobs.


## Back Pressure#


If you see a back pressure warning (e.g. High) for a task, this means that it is producing data faster than the downstream operators can consume. Records in your job flow downstream (e.g. from sources to sinks) and back pressure is propagated in the opposite direction, up the stream.

`High`

Take a simple Source -> Sink job as an example. If you see a warning for Source, this means that Sink is consuming data slower than Source is producing. Sink is back pressuring the upstream operator Source.

`Source -> Sink`
`Source`
`Sink`
`Source`
`Sink`
`Source`

## Task performance metrics#


Every parallel instance of a task (subtask) is exposing a group of three metrics:

* backPressuredTimeMsPerSecond, time that subtask spent being back pressured
* idleTimeMsPerSecond, time that subtask spent waiting for something to process
* busyTimeMsPerSecond, time that subtask was busy doing some actual work
At any point of time these three metrics are adding up approximately to 1000ms.
`backPressuredTimeMsPerSecond`
`idleTimeMsPerSecond`
`busyTimeMsPerSecond`
`1000ms`

These metrics are being updated every couple of seconds, and the reported value represents the
average time that subtask was back pressured (or idle or busy) during the last couple of seconds.
Keep this in mind if your job has a varying load. For example, a subtask with a constant load of 50%
and another subtask that is alternating every second between fully loaded and idling will both have
the same value of busyTimeMsPerSecond: around 500ms.

`busyTimeMsPerSecond`
`500ms`

Internally, back pressure is judged based on the availability of output buffers.
If a task has no available output buffers, then that task is considered back pressured.
Idleness, on the other hand, is determined by whether or not there is input available.


## Example#


The WebUI aggregates the maximum value of the back pressure and busy metrics from all of the
subtasks and presents those aggregated values inside the JobGraph. Besides displaying the raw
values, tasks are also color-coded to make the investigation easier.


Idling tasks are blue, fully back pressured tasks are black, and fully busy tasks are colored red.
All values in between are represented as shades between those three colors.


### Back Pressure Status#


In the Back Pressure tab next to the job overview you can find more detailed metrics.


For subtasks whose status is OK, there is no indication of back pressure. HIGH, on the
other hand, means that a subtask is back pressured. Status is defined in the following way:

* OK: 0% <= back pressured <= 10%
* LOW: 10% < back pressured <= 50%
* HIGH: 50% < back pressured <= 100%

Additionally, you can find the percentage of time each subtask is back pressured, idle, or busy.


 Back to top
