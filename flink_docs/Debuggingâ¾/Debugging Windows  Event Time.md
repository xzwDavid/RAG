# Debugging Windows & Event Time


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Debugging Windows & Event Time#


## Monitoring Current Event Time#


Flink’s event time and watermark support are powerful features for handling
out-of-order events. However, it’s harder to understand what exactly is going on because the progress of time
is tracked within the system.


Low watermarks of each task can be accessed through Flink web interface or metrics system.


Each Task in Flink exposes a metric called currentInputWatermark that represents the lowest watermark received
by this task. This long value represents the “current event time”.
The value is calculated by taking the minimum of all watermarks received by upstream operators. This means that
the event time tracked with watermarks is always dominated by the furthest-behind source.

`currentInputWatermark`

The low watermark metric is accessible using the web interface, by choosing a task in the metric tab,
and selecting the <taskNr>.currentInputWatermark metric. In the new box you’ll now be able to see
the current low watermark of the task.

`<taskNr>.currentInputWatermark`

Another way of getting the metric is using one of the metric reporters, as described in the documentation
for the metrics system.
For local setups, we recommend using the JMX metric reporter and a tool like VisualVM.


## Handling Event Time Stragglers#

* Approach 1: Watermark stays late (indicated completeness), windows fire early
* Approach 2: Watermark heuristic with maximum lateness, windows accept late data

 Back to top
