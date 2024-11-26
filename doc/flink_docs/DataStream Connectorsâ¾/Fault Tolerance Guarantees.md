# Fault Tolerance Guarantees


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Fault Tolerance Guarantees of Data Sources and Sinks#


Flink’s fault tolerance mechanism recovers programs in the presence of failures and
continues to execute them. Such failures include machine hardware failures, network failures,
transient program failures, etc.


Flink can guarantee exactly-once state updates to user-defined state only when the source participates in the
snapshotting mechanism. The following table lists the state update guarantees of Flink coupled with the bundled connectors.


Please read the documentation of each connector to understand the details of the fault tolerance guarantees.


To guarantee end-to-end exactly-once record delivery (in addition to exactly-once state semantics), the data sink needs
to take part in the checkpointing mechanism. The following table lists the delivery guarantees (assuming exactly-once
state updates) of Flink coupled with bundled sinks:


 Back to top
