# Metrics


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Metrics#


Flink exposes a metric system that allows gathering and exposing metrics to external systems.


## Registering metrics#


You can access the metric system from any user function that extends RichFunction by calling getRuntimeContext().getMetricGroup().
This method returns a MetricGroup object on which you can create and register new metrics.

`getRuntimeContext().getMetricGroup()`
`MetricGroup`

### Metric types#


Flink supports Counters, Gauges, Histograms and Meters.

`Counters`
`Gauges`
`Histograms`
`Meters`

#### Counter#


A Counter is used to count something. The current value can be in- or decremented using inc()/inc(long n) or dec()/dec(long n).
You can create and register a Counter by calling counter(String name) on a MetricGroup.

`Counter`
`inc()/inc(long n)`
`dec()/dec(long n)`
`Counter`
`counter(String name)`
`MetricGroup`

```

public class MyMapper extends RichMapFunction<String, String> {
  private transient Counter counter;

  @Override
  public void open(OpenContext ctx) {
    this.counter = getRuntimeContext()
      .getMetricGroup()
      .counter("myCounter");
  }

  @Override
  public String map(String value) throws Exception {
    this.counter.inc();
    return value;
  }
}

```

`
public class MyMapper extends RichMapFunction<String, String> {
  private transient Counter counter;

  @Override
  public void open(OpenContext ctx) {
    this.counter = getRuntimeContext()
      .getMetricGroup()
      .counter("myCounter");
  }

  @Override
  public String map(String value) throws Exception {
    this.counter.inc();
    return value;
  }
}
`

```

class MyMapper extends RichMapFunction[String,String] {
  @transient private var counter: Counter = _

  override def open(parameters: Configuration): Unit = {
    counter = getRuntimeContext()
      .getMetricGroup()
      .counter("myCounter")
  }

  override def map(value: String): String = {
    counter.inc()
    value
  }
}

```

`
class MyMapper extends RichMapFunction[String,String] {
  @transient private var counter: Counter = _

  override def open(parameters: Configuration): Unit = {
    counter = getRuntimeContext()
      .getMetricGroup()
      .counter("myCounter")
  }

  override def map(value: String): String = {
    counter.inc()
    value
  }
}
`

```

class MyMapper(MapFunction):
    def __init__(self):
        self.counter = None

    def open(self, runtime_context: RuntimeContext):
        self.counter = runtime_context \
            .get_metrics_group() \
            .counter("my_counter")

    def map(self, value: str):
        self.counter.inc()
        return value

```

`
class MyMapper(MapFunction):
    def __init__(self):
        self.counter = None

    def open(self, runtime_context: RuntimeContext):
        self.counter = runtime_context \
            .get_metrics_group() \
            .counter("my_counter")

    def map(self, value: str):
        self.counter.inc()
        return value
`

Alternatively you can also use your own Counter implementation:

`Counter`

```

public class MyMapper extends RichMapFunction<String, String> {
  private transient Counter counter;

  @Override
  public void open(OpenContext ctx) {
    this.counter = getRuntimeContext()
      .getMetricGroup()
      .counter("myCustomCounter", new CustomCounter());
  }

  @Override
  public String map(String value) throws Exception {
    this.counter.inc();
    return value;
  }
}

```

`
public class MyMapper extends RichMapFunction<String, String> {
  private transient Counter counter;

  @Override
  public void open(OpenContext ctx) {
    this.counter = getRuntimeContext()
      .getMetricGroup()
      .counter("myCustomCounter", new CustomCounter());
  }

  @Override
  public String map(String value) throws Exception {
    this.counter.inc();
    return value;
  }
}
`

```

class MyMapper extends RichMapFunction[String,String] {
  @transient private var counter: Counter = _

  override def open(parameters: Configuration): Unit = {
    counter = getRuntimeContext()
      .getMetricGroup()
      .counter("myCustomCounter", new CustomCounter())
  }

  override def map(value: String): String = {
    counter.inc()
    value
  }
}

```

`
class MyMapper extends RichMapFunction[String,String] {
  @transient private var counter: Counter = _

  override def open(parameters: Configuration): Unit = {
    counter = getRuntimeContext()
      .getMetricGroup()
      .counter("myCustomCounter", new CustomCounter())
  }

  override def map(value: String): String = {
    counter.inc()
    value
  }
}
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

#### Gauge#


A Gauge provides a value of any type on demand. In order to use a Gauge you must first create a class that implements the org.apache.flink.metrics.Gauge interface.
There is no restriction for the type of the returned value.
You can register a gauge by calling gauge(String name, Gauge gauge) on a MetricGroup.

`Gauge`
`Gauge`
`org.apache.flink.metrics.Gauge`
`gauge(String name, Gauge gauge)`
`MetricGroup`

```

public class MyMapper extends RichMapFunction<String, String> {
  private transient int valueToExpose = 0;

  @Override
  public void open(OpenContext ctx) {
    getRuntimeContext()
      .getMetricGroup()
      .gauge("MyGauge", new Gauge<Integer>() {
        @Override
        public Integer getValue() {
          return valueToExpose;
        }
      });
  }

  @Override
  public String map(String value) throws Exception {
    valueToExpose++;
    return value;
  }
}

```

`
public class MyMapper extends RichMapFunction<String, String> {
  private transient int valueToExpose = 0;

  @Override
  public void open(OpenContext ctx) {
    getRuntimeContext()
      .getMetricGroup()
      .gauge("MyGauge", new Gauge<Integer>() {
        @Override
        public Integer getValue() {
          return valueToExpose;
        }
      });
  }

  @Override
  public String map(String value) throws Exception {
    valueToExpose++;
    return value;
  }
}
`

```

new class MyMapper extends RichMapFunction[String,String] {
  @transient private var valueToExpose = 0

  override def open(parameters: Configuration): Unit = {
    getRuntimeContext()
      .getMetricGroup()
      .gauge[Int, ScalaGauge[Int]]("MyGauge", ScalaGauge[Int]( () => valueToExpose ) )
  }

  override def map(value: String): String = {
    valueToExpose += 1
    value
  }
}

```

`
new class MyMapper extends RichMapFunction[String,String] {
  @transient private var valueToExpose = 0

  override def open(parameters: Configuration): Unit = {
    getRuntimeContext()
      .getMetricGroup()
      .gauge[Int, ScalaGauge[Int]]("MyGauge", ScalaGauge[Int]( () => valueToExpose ) )
  }

  override def map(value: String): String = {
    valueToExpose += 1
    value
  }
}
`

```

class MyMapper(MapFunction):
    def __init__(self):
        self.value_to_expose = 0

    def open(self, runtime_context: RuntimeContext):
        runtime_context \
            .get_metrics_group() \
            .gauge("my_gauge", lambda: self.value_to_expose)

    def map(self, value: str):
        self.value_to_expose += 1
        return value

```

`
class MyMapper(MapFunction):
    def __init__(self):
        self.value_to_expose = 0

    def open(self, runtime_context: RuntimeContext):
        runtime_context \
            .get_metrics_group() \
            .gauge("my_gauge", lambda: self.value_to_expose)

    def map(self, value: str):
        self.value_to_expose += 1
        return value
`

Note that reporters will turn the exposed object into a String, which means that a meaningful toString() implementation is required.

`String`
`toString()`

#### Histogram#


A Histogram measures the distribution of long values.
You can register one by calling histogram(String name, Histogram histogram) on a MetricGroup.

`Histogram`
`histogram(String name, Histogram histogram)`
`MetricGroup`

```
public class MyMapper extends RichMapFunction<Long, Long> {
  private transient Histogram histogram;

  @Override
  public void open(OpenContext ctx) {
    this.histogram = getRuntimeContext()
      .getMetricGroup()
      .histogram("myHistogram", new MyHistogram());
  }

  @Override
  public Long map(Long value) throws Exception {
    this.histogram.update(value);
    return value;
  }
}

```

`public class MyMapper extends RichMapFunction<Long, Long> {
  private transient Histogram histogram;

  @Override
  public void open(OpenContext ctx) {
    this.histogram = getRuntimeContext()
      .getMetricGroup()
      .histogram("myHistogram", new MyHistogram());
  }

  @Override
  public Long map(Long value) throws Exception {
    this.histogram.update(value);
    return value;
  }
}
`

```

class MyMapper extends RichMapFunction[Long,Long] {
  @transient private var histogram: Histogram = _

  override def open(parameters: Configuration): Unit = {
    histogram = getRuntimeContext()
      .getMetricGroup()
      .histogram("myHistogram", new MyHistogram())
  }

  override def map(value: Long): Long = {
    histogram.update(value)
    value
  }
}

```

`
class MyMapper extends RichMapFunction[Long,Long] {
  @transient private var histogram: Histogram = _

  override def open(parameters: Configuration): Unit = {
    histogram = getRuntimeContext()
      .getMetricGroup()
      .histogram("myHistogram", new MyHistogram())
  }

  override def map(value: Long): Long = {
    histogram.update(value)
    value
  }
}
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

Flink does not provide a default implementation for Histogram, but offers a 

    Wrapper

 that allows usage of Codahale/DropWizard histograms.
To use this wrapper add the following dependency in your pom.xml:

`Histogram`
`pom.xml`

```
<dependency>
      <groupId>org.apache.flink</groupId>
      <artifactId>flink-metrics-dropwizard</artifactId>
      <version>2.0-SNAPSHOT</version>
</dependency>

```

`<dependency>
      <groupId>org.apache.flink</groupId>
      <artifactId>flink-metrics-dropwizard</artifactId>
      <version>2.0-SNAPSHOT</version>
</dependency>
`

You can then register a Codahale/DropWizard histogram like this:


```
public class MyMapper extends RichMapFunction<Long, Long> {
  private transient Histogram histogram;

  @Override
  public void open(OpenContext ctx) {
    com.codahale.metrics.Histogram dropwizardHistogram =
      new com.codahale.metrics.Histogram(new SlidingWindowReservoir(500));

    this.histogram = getRuntimeContext()
      .getMetricGroup()
      .histogram("myHistogram", new DropwizardHistogramWrapper(dropwizardHistogram));
  }

  @Override
  public Long map(Long value) throws Exception {
    this.histogram.update(value);
    return value;
  }
}

```

`public class MyMapper extends RichMapFunction<Long, Long> {
  private transient Histogram histogram;

  @Override
  public void open(OpenContext ctx) {
    com.codahale.metrics.Histogram dropwizardHistogram =
      new com.codahale.metrics.Histogram(new SlidingWindowReservoir(500));

    this.histogram = getRuntimeContext()
      .getMetricGroup()
      .histogram("myHistogram", new DropwizardHistogramWrapper(dropwizardHistogram));
  }

  @Override
  public Long map(Long value) throws Exception {
    this.histogram.update(value);
    return value;
  }
}
`

```

class MyMapper extends RichMapFunction[Long, Long] {
  @transient private var histogram: Histogram = _

  override def open(config: Configuration): Unit = {
    val dropwizardHistogram =
      new com.codahale.metrics.Histogram(new SlidingWindowReservoir(500))

    histogram = getRuntimeContext()
      .getMetricGroup()
      .histogram("myHistogram", new DropwizardHistogramWrapper(dropwizardHistogram))
  }

  override def map(value: Long): Long = {
    histogram.update(value)
    value
  }
}

```

`
class MyMapper extends RichMapFunction[Long, Long] {
  @transient private var histogram: Histogram = _

  override def open(config: Configuration): Unit = {
    val dropwizardHistogram =
      new com.codahale.metrics.Histogram(new SlidingWindowReservoir(500))

    histogram = getRuntimeContext()
      .getMetricGroup()
      .histogram("myHistogram", new DropwizardHistogramWrapper(dropwizardHistogram))
  }

  override def map(value: Long): Long = {
    histogram.update(value)
    value
  }
}
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

#### Meter#


A Meter measures an average throughput. An occurrence of an event can be registered with the markEvent() method. Occurrence of multiple events at the same time can be registered with markEvent(long n) method.
You can register a meter by calling meter(String name, Meter meter) on a MetricGroup.

`Meter`
`markEvent()`
`markEvent(long n)`
`meter(String name, Meter meter)`
`MetricGroup`

```
public class MyMapper extends RichMapFunction<Long, Long> {
  private transient Meter meter;

  @Override
  public void open(OpenContext ctx) {
    this.meter = getRuntimeContext()
      .getMetricGroup()
      .meter("myMeter", new MyMeter());
  }

  @Override
  public Long map(Long value) throws Exception {
    this.meter.markEvent();
    return value;
  }
}

```

`public class MyMapper extends RichMapFunction<Long, Long> {
  private transient Meter meter;

  @Override
  public void open(OpenContext ctx) {
    this.meter = getRuntimeContext()
      .getMetricGroup()
      .meter("myMeter", new MyMeter());
  }

  @Override
  public Long map(Long value) throws Exception {
    this.meter.markEvent();
    return value;
  }
}
`

```

class MyMapper extends RichMapFunction[Long,Long] {
  @transient private var meter: Meter = _

  override def open(config: Configuration): Unit = {
    meter = getRuntimeContext()
      .getMetricGroup()
      .meter("myMeter", new MyMeter())
  }

  override def map(value: Long): Long = {
    meter.markEvent()
    value
  }
}

```

`
class MyMapper extends RichMapFunction[Long,Long] {
  @transient private var meter: Meter = _

  override def open(config: Configuration): Unit = {
    meter = getRuntimeContext()
      .getMetricGroup()
      .meter("myMeter", new MyMeter())
  }

  override def map(value: Long): Long = {
    meter.markEvent()
    value
  }
}
`

```

class MyMapperMeter(MapFunction):
    def __init__(self):
        self.meter = None

    def open(self, runtime_context: RuntimeContext):
        # an average rate of events per second over 120s, default is 60s.
        self.meter = runtime_context
            .get_metrics_group()
            .meter("my_meter", time_span_in_seconds=120)

    def map(self, value: str):
        self.meter.mark_event()
        return value

```

`
class MyMapperMeter(MapFunction):
    def __init__(self):
        self.meter = None

    def open(self, runtime_context: RuntimeContext):
        # an average rate of events per second over 120s, default is 60s.
        self.meter = runtime_context
            .get_metrics_group()
            .meter("my_meter", time_span_in_seconds=120)

    def map(self, value: str):
        self.meter.mark_event()
        return value
`

Flink offers a 

    Wrapper

 that allows usage of Codahale/DropWizard meters.
To use this wrapper add the following dependency in your pom.xml:

`pom.xml`

```
<dependency>
      <groupId>org.apache.flink</groupId>
      <artifactId>flink-metrics-dropwizard</artifactId>
      <version>2.0-SNAPSHOT</version>
</dependency>

```

`<dependency>
      <groupId>org.apache.flink</groupId>
      <artifactId>flink-metrics-dropwizard</artifactId>
      <version>2.0-SNAPSHOT</version>
</dependency>
`

You can then register a Codahale/DropWizard meter like this:


```
public class MyMapper extends RichMapFunction<Long, Long> {
  private transient Meter meter;

  @Override
  public void open(OpenContext ctx) {
    com.codahale.metrics.Meter dropwizardMeter = new com.codahale.metrics.Meter();

    this.meter = getRuntimeContext()
      .getMetricGroup()
      .meter("myMeter", new DropwizardMeterWrapper(dropwizardMeter));
  }

  @Override
  public Long map(Long value) throws Exception {
    this.meter.markEvent();
    return value;
  }
}

```

`public class MyMapper extends RichMapFunction<Long, Long> {
  private transient Meter meter;

  @Override
  public void open(OpenContext ctx) {
    com.codahale.metrics.Meter dropwizardMeter = new com.codahale.metrics.Meter();

    this.meter = getRuntimeContext()
      .getMetricGroup()
      .meter("myMeter", new DropwizardMeterWrapper(dropwizardMeter));
  }

  @Override
  public Long map(Long value) throws Exception {
    this.meter.markEvent();
    return value;
  }
}
`

```

class MyMapper extends RichMapFunction[Long,Long] {
  @transient private var meter: Meter = _

  override def open(config: Configuration): Unit = {
    val dropwizardMeter: com.codahale.metrics.Meter = new com.codahale.metrics.Meter()

    meter = getRuntimeContext()
      .getMetricGroup()
      .meter("myMeter", new DropwizardMeterWrapper(dropwizardMeter))
  }

  override def map(value: Long): Long = {
    meter.markEvent()
    value
  }
}

```

`
class MyMapper extends RichMapFunction[Long,Long] {
  @transient private var meter: Meter = _

  override def open(config: Configuration): Unit = {
    val dropwizardMeter: com.codahale.metrics.Meter = new com.codahale.metrics.Meter()

    meter = getRuntimeContext()
      .getMetricGroup()
      .meter("myMeter", new DropwizardMeterWrapper(dropwizardMeter))
  }

  override def map(value: Long): Long = {
    meter.markEvent()
    value
  }
}
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

## Scope#


Every metric is assigned an identifier and a set of key-value pairs under which the metric will be reported.


The identifier is based on 3 components: a user-defined name when registering the metric, an optional user-defined scope and a system-provided scope.
For example, if A.B is the system scope, C.D the user scope and E the name, then the identifier for the metric will be A.B.C.D.E.

`A.B`
`C.D`
`E`
`A.B.C.D.E`

You can configure which delimiter to use for the identifier (default: .) by setting the metrics.scope.delimiter key in Flink configuration file.

`.`
`metrics.scope.delimiter`

### User Scope#


You can define a user scope by calling MetricGroup#addGroup(String name), MetricGroup#addGroup(int name) or MetricGroup#addGroup(String key, String value).
These methods affect what MetricGroup#getMetricIdentifier and MetricGroup#getScopeComponents return.

`MetricGroup#addGroup(String name)`
`MetricGroup#addGroup(int name)`
`MetricGroup#addGroup(String key, String value)`
`MetricGroup#getMetricIdentifier`
`MetricGroup#getScopeComponents`

```

counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetrics")
  .counter("myCounter");

counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetricsKey", "MyMetricsValue")
  .counter("myCounter");

```

`
counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetrics")
  .counter("myCounter");

counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetricsKey", "MyMetricsValue")
  .counter("myCounter");
`

```

counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetrics")
  .counter("myCounter")

counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetricsKey", "MyMetricsValue")
  .counter("myCounter")

```

`
counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetrics")
  .counter("myCounter")

counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetricsKey", "MyMetricsValue")
  .counter("myCounter")
`

```

counter = runtime_context \
    .get_metric_group() \
    .add_group("my_metrics") \
    .counter("my_counter")

counter = runtime_context \
    .get_metric_group() \
    .add_group("my_metrics_key", "my_metrics_value") \
    .counter("my_counter")

```

`
counter = runtime_context \
    .get_metric_group() \
    .add_group("my_metrics") \
    .counter("my_counter")

counter = runtime_context \
    .get_metric_group() \
    .add_group("my_metrics_key", "my_metrics_value") \
    .counter("my_counter")
`

### System Scope#


The system scope contains context information about the metric, for example in which task it was registered or what job that task belongs to.


Which context information should be included can be configured by setting the following keys in Flink configuration file.
Each of these keys expect a format string that may contain constants (e.g. “taskmanager”) and variables (e.g. “<task_id>”) which will be replaced at runtime.

* metrics.scope.jm

Default: <host>.jobmanager
Applied to all metrics that were scoped to a job manager.


* metrics.scope.jm-job

Default: <host>.jobmanager.<job_name>
Applied to all metrics that were scoped to a job manager and job.


* metrics.scope.tm

Default: <host>.taskmanager.<tm_id>
Applied to all metrics that were scoped to a task manager.


* metrics.scope.tm-job

Default: <host>.taskmanager.<tm_id>.<job_name>
Applied to all metrics that were scoped to a task manager and job.


* metrics.scope.task

Default: <host>.taskmanager.<tm_id>.<job_name>.<task_name>.<subtask_index>
Applied to all metrics that were scoped to a task.


* metrics.scope.operator

Default: <host>.taskmanager.<tm_id>.<job_name>.<operator_name>.<subtask_index>
Applied to all metrics that were scoped to an operator.


`metrics.scope.jm`
* Default: <host>.jobmanager
* Applied to all metrics that were scoped to a job manager.
`metrics.scope.jm-job`
* Default: <host>.jobmanager.<job_name>
* Applied to all metrics that were scoped to a job manager and job.
`metrics.scope.tm`
* Default: <host>.taskmanager.<tm_id>
* Applied to all metrics that were scoped to a task manager.
`metrics.scope.tm-job`
* Default: <host>.taskmanager.<tm_id>.<job_name>
* Applied to all metrics that were scoped to a task manager and job.
`metrics.scope.task`
* Default: <host>.taskmanager.<tm_id>.<job_name>.<task_name>.<subtask_index>
* Applied to all metrics that were scoped to a task.
`metrics.scope.operator`
* Default: <host>.taskmanager.<tm_id>.<job_name>.<operator_name>.<subtask_index>
* Applied to all metrics that were scoped to an operator.

There are no restrictions on the number or order of variables. Variables are case sensitive.


The default scope for operator metrics will result in an identifier akin to localhost.taskmanager.1234.MyJob.MyOperator.0.MyMetric

`localhost.taskmanager.1234.MyJob.MyOperator.0.MyMetric`

If you also want to include the task name but omit the task manager information you can specify the following format:


metrics.scope.operator: <host>.<job_name>.<task_name>.<operator_name>.<subtask_index>

`metrics.scope.operator: <host>.<job_name>.<task_name>.<operator_name>.<subtask_index>`

This could create the identifier localhost.MyJob.MySource_->_MyOperator.MyOperator.0.MyMetric.

`localhost.MyJob.MySource_->_MyOperator.MyOperator.0.MyMetric`

Note that for this format string an identifier clash can occur should the same job be run multiple times concurrently, which can lead to inconsistent metric data.
As such it is advised to either use format strings that provide a certain degree of uniqueness by including IDs (e.g <job_id>)
or by assigning unique names to jobs and operators.


### List of all Variables#

* JobManager: <host>
* TaskManager: <host>, <tm_id>
* Job: <job_id>, <job_name>
* Task: <task_id>, <task_name>, <task_attempt_id>, <task_attempt_num>, <subtask_index>
* Operator: <operator_id>,<operator_name>, <subtask_index>

Important: For the Batch API, <operator_id> is always equal to <task_id>.


### User Variables#


You can define a user variable by calling MetricGroup#addGroup(String key, String value).
This method affects what MetricGroup#getMetricIdentifier, MetricGroup#getScopeComponents and MetricGroup#getAllVariables() returns.

`MetricGroup#addGroup(String key, String value)`
`MetricGroup#getMetricIdentifier`
`MetricGroup#getScopeComponents`
`MetricGroup#getAllVariables()`

Important: User variables cannot be used in scope formats.


```

counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetricsKey", "MyMetricsValue")
  .counter("myCounter");

```

`
counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetricsKey", "MyMetricsValue")
  .counter("myCounter");
`

```

counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetricsKey", "MyMetricsValue")
  .counter("myCounter")

```

`
counter = getRuntimeContext()
  .getMetricGroup()
  .addGroup("MyMetricsKey", "MyMetricsValue")
  .counter("myCounter")
`

## Reporter#


For information on how to set up Flink’s metric reporters please take a look at the metric reporters documentation.


## System metrics#


By default Flink gathers several metrics that provide deep insights on the current state.
This section is a reference of all these metrics.


The tables below generally feature 5 columns:

* 
The “Scope” column describes which scope format is used to generate the system scope.
For example, if the cell contains “Operator” then the scope format for “metrics.scope.operator” is used.
If the cell contains multiple values, separated by a slash, then the metrics are reported multiple
times for different entities, like for both job- and taskmanagers.

* 
The (optional)“Infix” column describes which infix is appended to the system scope.

* 
The “Metrics” column lists the names of all metrics that are registered for the given scope and infix.

* 
The “Description” column provides information as to what a given metric is measuring.

* 
The “Type” column describes which metric type is used for the measurement.


The “Scope” column describes which scope format is used to generate the system scope.
For example, if the cell contains “Operator” then the scope format for “metrics.scope.operator” is used.
If the cell contains multiple values, separated by a slash, then the metrics are reported multiple
times for different entities, like for both job- and taskmanagers.


The (optional)“Infix” column describes which infix is appended to the system scope.


The “Metrics” column lists the names of all metrics that are registered for the given scope and infix.


The “Description” column provides information as to what a given metric is measuring.


The “Type” column describes which metric type is used for the measurement.


Note that all dots in the infix/metric name columns are still subject to the “metrics.delimiter” setting.


Thus, in order to infer the metric identifier:

1. Take the scope-format based on the “Scope” column
2. Append the value in the “Infix” column if present, and account for the “metrics.delimiter” setting
3. Append metric name.

### CPU#


### Memory#


The memory-related metrics require Oracle’s memory management (also included in OpenJDK’s Hotspot implementation) to be in place.
Some metrics might not be exposed when using other JVM implementations (e.g. IBM’s J9).


### Threads#


### GarbageCollection#


### ClassLoader#


### Network#


> 
  Deprecated: use Default shuffle service metrics



### Default shuffle service#


Metrics related to data exchange between task executors using netty network communication.


### Cluster#


### Availability#


The metrics in this table are available for each of the following job states: INITIALIZING, CREATED, RUNNING, RESTARTING, CANCELLING, FAILING.
Whether these metrics are reported depends on the metrics.job.status.enable setting.


Evolving The semantics of these metrics may change in later releases.


> 
Experimental
While the job is in the RUNNING state the metrics in this table provide additional details on what the job is currently doing.
Whether these metrics are reported depends on the metrics.job.status.enable setting.



Scope
Metrics
Description
Type




Job (only available on JobManager)
deployingState
Return 1 if the job is currently deploying* tasks, otherwise return 0.
Gauge


deployingTime
Return the time (in milliseconds) since the job has started deploying* tasks, otherwise return 0.
Gauge


deployingTimeTotal
Return how much time (in milliseconds) the job has spent deploying* tasks in total.
Gauge



*A job is considered to be deploying tasks when:

for streaming jobs, any task is in the DEPLOYING state
for batch jobs, if at least 1 task is in the DEPLOYING state, and there are no INITIALIZING/RUNNING tasks




Experimental


While the job is in the RUNNING state the metrics in this table provide additional details on what the job is currently doing.
Whether these metrics are reported depends on the metrics.job.status.enable setting.


*A job is considered to be deploying tasks when:

* for streaming jobs, any task is in the DEPLOYING state
* for batch jobs, if at least 1 task is in the DEPLOYING state, and there are no INITIALIZING/RUNNING tasks

### Checkpointing#


Note that for failed checkpoints, metrics are updated on a best efforts basis and may be not accurate.


### State Access Latency#


### RocksDB#


Certain RocksDB native metrics are available but disabled by default, you can find full documentation here


### State Changelog#


Note that the metrics are only available via reporters.


### IO#


Note: For operators/tasks with 2 inputs this is the minimum of the last received watermarks.


Note: Only for operators with 2 or more inputs.


Note: Available only when watermark alignment is enabled and the first common watermark is
        announced. You can configure the update interval in the WatermarkStrategy.


### Connectors#


#### Kafka Connectors#


Please refer to Kafka monitoring.


#### Kinesis Source#


#### Kinesis Sink#


#### HBase Connectors#


### System resources#


System resources reporting is disabled by default. When metrics.system-resource
is enabled additional metrics listed below will be available on Job- and TaskManager.
System resources metrics are updated periodically and they present average values for a
configured interval (metrics.system-resource-probing-interval).

`metrics.system-resource`
`metrics.system-resource-probing-interval`

System resources reporting requires an optional dependency to be present on the
classpath (for example placed in Flink’s lib directory):

`lib`
* com.github.oshi:oshi-core:6.1.5 (licensed under MIT license)
`com.github.oshi:oshi-core:6.1.5`

Including it’s transitive dependencies:

* net.java.dev.jna:jna-platform:jar:5.10.0
* net.java.dev.jna:jna:jar:5.10.0
`net.java.dev.jna:jna-platform:jar:5.10.0`
`net.java.dev.jna:jna:jar:5.10.0`

Failures in this regard will be reported as warning messages like NoClassDefFoundError
logged by SystemResourcesMetricsInitializer during the startup.

`NoClassDefFoundError`
`SystemResourcesMetricsInitializer`

#### System CPU#


#### System memory#


#### System network#


### Speculative Execution#


Metrics below can be used to measure the effectiveness of speculative execution.


## End-to-End latency tracking#


Flink allows to track the latency of records travelling through the system. This feature is disabled by default.
To enable the latency tracking you must set the latencyTrackingInterval to a positive number in either the
Flink configuration or ExecutionConfig.

`latencyTrackingInterval`
`ExecutionConfig`

At the latencyTrackingInterval, the sources will periodically emit a special record, called a LatencyMarker.
The marker contains a timestamp from the time when the record has been emitted at the sources.
Latency markers can not overtake regular user records, thus if records are queuing up in front of an operator,
it will add to the latency tracked by the marker.

`latencyTrackingInterval`
`LatencyMarker`

Note that the latency markers are not accounting for the time user records spend in operators as they are
bypassing them. In particular the markers are not accounting for the time records spend for example in window buffers.
Only if operators are not able to accept new records, thus they are queuing up, the latency measured using
the markers will reflect that.


The LatencyMarkers are used to derive a distribution of the latency between the sources of the topology and each
downstream operator. These distributions are reported as histogram metrics. The granularity of these distributions can
be controlled in the Flink configuration. For the highest
granularity subtask Flink will derive the latency distribution between every source subtask and every downstream
subtask, which results in quadratic (in the terms of the parallelism) number of histograms.

`LatencyMarker`
`subtask`

Currently, Flink assumes that the clocks of all machines in the cluster are in sync. We recommend setting
up an automated clock synchronisation service (like NTP) to avoid false latency results.


Warning Enabling latency metrics can significantly impact the performance
of the cluster (in particular for subtask granularity). It is highly recommended to only use them for debugging
purposes.

`subtask`

## State access latency tracking#


Flink also allows to track the keyed state access latency for standard Flink state-backends or customized state backends which extending from AbstractStateBackend. This feature is disabled by default.
To enable this feature you must set the state.latency-track.keyed-state-enabled to true in the Flink configuration.

`AbstractStateBackend`
`state.latency-track.keyed-state-enabled`

Once tracking keyed state access latency is enabled, Flink will sample the state access latency every N access, in which N is defined by state.latency-track.sample-interval.
This configuration has a default value of 100. A smaller value will get more accurate results but have a higher performance impact since it is sampled more frequently.

`N`
`N`
`state.latency-track.sample-interval`

As the type of this latency metrics is histogram, state.latency-track.history-size will control the maximum number of recorded values in history, which has the default value of 128.
A larger value of this configuration will require more memory, but will provide a more accurate result.

`state.latency-track.history-size`

Warning Enabling state-access-latency metrics may impact the performance.
It is recommended to only use them for debugging purposes.


## REST API integration#


Metrics can be queried through the Monitoring REST API.


Below is a list of available endpoints, with a sample JSON response. All endpoints are of the sample form http://hostname:8081/jobmanager/metrics, below we list only the path part of the URLs.

`http://hostname:8081/jobmanager/metrics`

Values in angle brackets are variables, for example http://hostname:8081/jobs/<jobid>/metrics will have to be requested for example as http://hostname:8081/jobs/7684be6004e4e955c2a558a9bc463f65/metrics.

`http://hostname:8081/jobs/<jobid>/metrics`
`http://hostname:8081/jobs/7684be6004e4e955c2a558a9bc463f65/metrics`

Request metrics for a specific entity:

* /jobmanager/metrics
* /taskmanagers/<taskmanagerid>/metrics
* /jobs/<jobid>/metrics
* /jobs/<jobid>/vertices/<vertexid>/subtasks/<subtaskindex>
`/jobmanager/metrics`
`/taskmanagers/<taskmanagerid>/metrics`
`/jobs/<jobid>/metrics`
`/jobs/<jobid>/vertices/<vertexid>/subtasks/<subtaskindex>`

Request metrics aggregated across all entities of the respective type:

* /taskmanagers/metrics
* /jobs/metrics
* /jobs/<jobid>/vertices/<vertexid>/subtasks/metrics
* /jobs/<jobid>/vertices/<vertexid>/jm-operator-metrics
`/taskmanagers/metrics`
`/jobs/metrics`
`/jobs/<jobid>/vertices/<vertexid>/subtasks/metrics`
`/jobs/<jobid>/vertices/<vertexid>/jm-operator-metrics`

Request metrics aggregated over a subset of all entities of the respective type:

* /taskmanagers/metrics?taskmanagers=A,B,C
* /jobs/metrics?jobs=D,E,F
* /jobs/<jobid>/vertices/<vertexid>/subtasks/metrics?subtask=1,2,3
`/taskmanagers/metrics?taskmanagers=A,B,C`
`/jobs/metrics?jobs=D,E,F`
`/jobs/<jobid>/vertices/<vertexid>/subtasks/metrics?subtask=1,2,3`

Warning Metric names can contain special characters that you need to escape when querying metrics.
For example, “a_+_b” would be escaped to “a_%2B_b”.

`a_+_b`
`a_%2B_b`

List of characters that should be escaped:


Request a list of available metrics:


GET /jobmanager/metrics

`GET /jobmanager/metrics`

```
[
  {
    "id": "metric1"
  },
  {
    "id": "metric2"
  }
]

```

`[
  {
    "id": "metric1"
  },
  {
    "id": "metric2"
  }
]
`

Request the values for specific (unaggregated) metrics:


GET taskmanagers/ABCDE/metrics?get=metric1,metric2

`GET taskmanagers/ABCDE/metrics?get=metric1,metric2`

```
[
  {
    "id": "metric1",
    "value": "34"
  },
  {
    "id": "metric2",
    "value": "2"
  }
]

```

`[
  {
    "id": "metric1",
    "value": "34"
  },
  {
    "id": "metric2",
    "value": "2"
  }
]
`

Request aggregated values for specific metrics:


GET /taskmanagers/metrics?get=metric1,metric2

`GET /taskmanagers/metrics?get=metric1,metric2`

```
[
  {
    "id": "metric1",
    "min": 1,
    "max": 34,
    "avg": 15,
    "sum": 45
  },
  {
    "id": "metric2",
    "min": 2,
    "max": 14,
    "avg": 7,
    "sum": 16
  }
]

```

`[
  {
    "id": "metric1",
    "min": 1,
    "max": 34,
    "avg": 15,
    "sum": 45
  },
  {
    "id": "metric2",
    "min": 2,
    "max": 14,
    "avg": 7,
    "sum": 16
  }
]
`

Request specific aggregated values for specific metrics:


GET /taskmanagers/metrics?get=metric1,metric2&agg=min,max

`GET /taskmanagers/metrics?get=metric1,metric2&agg=min,max`

```
[
  {
    "id": "metric1",
    "min": 1,
    "max": 34
  },
  {
    "id": "metric2",
    "min": 2,
    "max": 14
  }
]

```

`[
  {
    "id": "metric1",
    "min": 1,
    "max": 34
  },
  {
    "id": "metric2",
    "min": 2,
    "max": 14
  }
]
`

## Dashboard integration#


Metrics that were gathered for each task or operator can also be visualized in the Dashboard. On the main page for a
job, select the Metrics tab. After selecting one of the tasks in the top graph you can select metrics to display using
the Add Metric drop-down menu.

`Metrics`
`Add Metric`
* Task metrics are listed as <subtask_index>.<metric_name>.
* Operator metrics are listed as <subtask_index>.<operator_name>.<metric_name>.
`<subtask_index>.<metric_name>`
`<subtask_index>.<operator_name>.<metric_name>`

Each metric will be visualized as a separate graph, with the x-axis representing time and the y-axis the measured value.
All graphs are automatically updated every 10 seconds, and continue to do so when navigating to another page.


There is no limit as to the number of visualized metrics; however only numeric metrics can be visualized.


 Back to top
