# Process Function


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Process Function#


## ProcessFunction#


The ProcessFunction is a low-level stream processing operation, giving access to the basic building blocks of
all (acyclic) streaming applications:

`ProcessFunction`
* events (stream elements)
* state (fault-tolerant, consistent, only on keyed stream)
* timers (event time and processing time, only on keyed stream)

The ProcessFunction can be thought of as a FlatMapFunction with access to keyed state and timers. It handles events
by being invoked for each event received in the input stream(s).

`ProcessFunction`
`FlatMapFunction`

Please refer to Process Function
for more details about the concept and usage of ProcessFunction.

`ProcessFunction`

## Execution behavior of timer#


Python user-defined functions are executed in a separate Python process from Flink’s operators which run in a JVM,
the timer registration requests made in ProcessFunction will be sent to the Java operator asynchronously.
Once received timer registration requests, the Java operator will register it into the underlying timer service.

`ProcessFunction`

If the registered timer has already passed the current time (the current system time for processing time timer,
or the current watermark for event time), it will be triggered immediately.


Note that, due to the asynchronous processing characteristics, it may happen that the timer was triggered a little later than the actual time.
For example, a registered processing time timer of 10:00:00 may be actually processed at 10:00:05.

`10:00:00`
`10:00:05`