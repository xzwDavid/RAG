# Traces


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Traces#


Flink exposes a tracing system that allows gathering and exposing traces to external systems.


## Reporting traces#


You can access the tracing system from any user function that extends RichFunction by calling getRuntimeContext().getMetricGroup().
This method returns a MetricGroup object via which you can report a new single span trace.

`getRuntimeContext().getMetricGroup()`
`MetricGroup`

### Reporting single Span#


A Span represents something that happened in Flink at certain point of time, that will be reported to a TraceReporter.
To report a Span you can use the MetricGroup#addSpan(SpanBuilder) method.

`Span`
`TraceReporter`
`Span`
`MetricGroup#addSpan(SpanBuilder)`

Currently we don’t support traces with multiple spans. Each Span is self-contained and represents things like a checkpoint or recovery.






Java
public class MyClass {
    void doSomething() {
        // (...)
        metricGroup.addSpan(
                Span.builder(MyClass.class, "SomeAction")
                        .setStartTsMillis(startTs) // Optional
                        .setEndTsMillis(endTs) // Optional
                        .setAttribute("foo", "bar");
    }
}

Python
Currently reporting Spans from Python is not supported.



`Span`

```
public class MyClass {
    void doSomething() {
        // (...)
        metricGroup.addSpan(
                Span.builder(MyClass.class, "SomeAction")
                        .setStartTsMillis(startTs) // Optional
                        .setEndTsMillis(endTs) // Optional
                        .setAttribute("foo", "bar");
    }
}

```

`public class MyClass {
    void doSomething() {
        // (...)
        metricGroup.addSpan(
                Span.builder(MyClass.class, "SomeAction")
                        .setStartTsMillis(startTs) // Optional
                        .setEndTsMillis(endTs) // Optional
                        .setAttribute("foo", "bar");
    }
}
`

```
Currently reporting Spans from Python is not supported.

```

`Currently reporting Spans from Python is not supported.
`

## Reporter#


For information on how to set up Flink’s trace reporters please take a look at the trace reporters documentation.


## System traces#


Flink reports traces listed below.


The tables below generally feature 5 columns:

* 
The “Scope” column describes what is that trace reported scope.

* 
The “Name” column describes the name of the reported trace.

* 
The “Attributes” column lists the names of all attributes that are reported with the given trace.

* 
The “Description” column provides information as to what a given attribute is reporting.


The “Scope” column describes what is that trace reported scope.


The “Name” column describes the name of the reported trace.


The “Attributes” column lists the names of all attributes that are reported with the given trace.


The “Description” column provides information as to what a given attribute is reporting.


### Checkpointing and initialization#


Flink reports a single span trace for the whole checkpoint and job initialization events once that event reaches a terminal state: COMPLETED or FAILED.


 Back to top
