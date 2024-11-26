# Trace Reporters


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Trace Reporters#


Flink allows reporting traces to external systems.
For more information about Flink’s tracing system go to the tracing system documentation.


Traces can be exposed to an external system by configuring one or several reporters in Flink configuration file. These
reporters will be instantiated on each job and task manager when they are started.


Below is a list of parameters that are generally applicable to all reporters.
All properties are configured by setting traces.reporter.<reporter_name>.<property> in the configuration.
Reporters may additionally offer implementation-specific parameters, which are documented in the respective reporter’s section.

`traces.reporter.<reporter_name>.<property>`

##### traces.reporter.<name>.factory.class


##### traces.reporter.<name>.scope.variables.additional


##### traces.reporter.<name>.<parameter>


All reporter configurations must contain the factory.class property.

`factory.class`

Example reporter configuration that specifies multiple reporters:


```
traces.reporters: otel,my_other_otel

traces.reporter.otel.factory.class: org.apache.flink.traces.otel.OpenTelemetryTraceReporterFactory
traces.reporter.otel.exporter.endpoint: http://127.0.0.1:1337
traces.reporter.otel.scope.variables.additional: region:eu-west-1,environment:local,flink_runtime:1.17.1

traces.reporter.my_other_otel.factory.class: org.apache.flink.common.metrics.OpenTelemetryTraceReporterFactory
traces.reporter.my_other_otel.exporter.endpoint: http://196.168.0.1:31337

```

`traces.reporters: otel,my_other_otel

traces.reporter.otel.factory.class: org.apache.flink.traces.otel.OpenTelemetryTraceReporterFactory
traces.reporter.otel.exporter.endpoint: http://127.0.0.1:1337
traces.reporter.otel.scope.variables.additional: region:eu-west-1,environment:local,flink_runtime:1.17.1

traces.reporter.my_other_otel.factory.class: org.apache.flink.common.metrics.OpenTelemetryTraceReporterFactory
traces.reporter.my_other_otel.exporter.endpoint: http://196.168.0.1:31337
`

Important: The jar containing the reporter must be accessible when Flink is started.
Reporters are loaded as plugins.
All reporters documented on this page are available by default.


You can write your own Reporter by implementing the org.apache.flink.traces.reporter.TraceReporter and org.apache.flink.traces.reporter.TraceReporterFactory interfaces.
Be careful that all the method must not block for a significant amount of time, and any reporter needing more time should instead run the operation asynchronously.

`Reporter`
`org.apache.flink.traces.reporter.TraceReporter`
`org.apache.flink.traces.reporter.TraceReporterFactory`

## Reporters#


The following sections list the supported reporters.


### OpenTelemetry#


#### (org.apache.flink.traces.otel.OpenTelemetryTraceReporterFactory)#


OpenTelemetryTraceReporterFactory currently supports only gRPC.

`OpenTelemetryTraceReporterFactory`

Parameters:


##### exporter.endpoint


##### exporter.timeout


##### service.name


##### service.version


Example configuration:


```
traces.reporter.otel.factory.class: org.apache.flink.metrics.otel.OpenTelemetryTraceReporterFactory
traces.reporter.otel.exporter.endpoint: http://127.0.0.1:1337

```

`traces.reporter.otel.factory.class: org.apache.flink.metrics.otel.OpenTelemetryTraceReporterFactory
traces.reporter.otel.exporter.endpoint: http://127.0.0.1:1337
`

### Slf4j#


#### (org.apache.flink.traces.slf4j.Slf4jTraceReporter)#


Example configuration:


```
traces.reporter.slf4j.factory.class: org.apache.flink.traces.slf4j.Slf4jTraceReporterFactory

```

`traces.reporter.slf4j.factory.class: org.apache.flink.traces.slf4j.Slf4jTraceReporterFactory
`

 Back to top
