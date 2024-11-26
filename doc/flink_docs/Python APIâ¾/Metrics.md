# Metrics


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Metrics#


PyFlink exposes a metric system that allows gathering and exposing metrics to external systems.


## Registering metrics#


You can access the metric system from a Python user-defined function
by calling function_context.get_metric_group() in the open method.
The get_metric_group() method returns a MetricGroup object on which you can create
and register new metrics.

`function_context.get_metric_group()`
`open`
`get_metric_group()`
`MetricGroup`

### Metric types#


PyFlink supports Counters, Gauges, Distribution and Meters.

`Counters`
`Gauges`
`Distribution`
`Meters`

#### Counter#


A Counter is used to count something. The current value can be in- or decremented using inc()/inc(n: int) or dec()/dec(n: int).
You can create and register a Counter by calling counter(name: str) on a MetricGroup.

`Counter`
`inc()/inc(n: int)`
`dec()/dec(n: int)`
`Counter`
`counter(name: str)`
`MetricGroup`

```
from pyflink.table.udf import ScalarFunction

class MyUDF(ScalarFunction):

    def __init__(self):
        self.counter = None

    def open(self, function_context):
        self.counter = function_context.get_metric_group().counter("my_counter")

    def eval(self, i):
        self.counter.inc(i)
        return i

```

`from pyflink.table.udf import ScalarFunction

class MyUDF(ScalarFunction):

    def __init__(self):
        self.counter = None

    def open(self, function_context):
        self.counter = function_context.get_metric_group().counter("my_counter")

    def eval(self, i):
        self.counter.inc(i)
        return i
`

#### Gauge#


A Gauge provides a value on demand. You can register a gauge by calling
gauge(name: str, obj: Callable[[], int]) on a MetricGroup. The Callable object will be used to
report the values. Gauge metrics are restricted to integer-only values.

`Gauge`
`gauge(name: str, obj: Callable[[], int])`

```
from pyflink.table.udf import ScalarFunction

class MyUDF(ScalarFunction):

    def __init__(self):
        self.length = 0

    def open(self, function_context):
        function_context.get_metric_group().gauge("my_gauge", lambda : self.length)

    def eval(self, i):
        self.length = i
        return i - 1

```

`from pyflink.table.udf import ScalarFunction

class MyUDF(ScalarFunction):

    def __init__(self):
        self.length = 0

    def open(self, function_context):
        function_context.get_metric_group().gauge("my_gauge", lambda : self.length)

    def eval(self, i):
        self.length = i
        return i - 1
`

#### Distribution#


A metric that reports information(sum, count, min, max and mean) about the distribution of
reported values. The value can be updated using update(n: int). You can register a distribution
by calling distribution(name: str) on a MetricGroup. Distribution metrics are restricted to
integer-only distributions.

`update(n: int)`
`distribution(name: str)`

```
from pyflink.table.udf import ScalarFunction

class MyUDF(ScalarFunction):

    def __init__(self):
        self.distribution = None

    def open(self, function_context):
        self.distribution = function_context.get_metric_group().distribution("my_distribution")

    def eval(self, i):
        self.distribution.update(i)
        return i - 1

```

`from pyflink.table.udf import ScalarFunction

class MyUDF(ScalarFunction):

    def __init__(self):
        self.distribution = None

    def open(self, function_context):
        self.distribution = function_context.get_metric_group().distribution("my_distribution")

    def eval(self, i):
        self.distribution.update(i)
        return i - 1
`

#### Meter#


A Meter measures an average throughput. An occurrence of an event can be registered with the
mark_event() method. The occurrence of multiple events at the same time can be registered with
mark_event(n: int) method. You can register a meter by calling
meter(self, name: str, time_span_in_seconds: int = 60) on a MetricGroup.
The default value of time_span_in_seconds is 60.

`mark_event()`
`meter(self, name: str, time_span_in_seconds: int = 60)`

```
from pyflink.table.udf import ScalarFunction

class MyUDF(ScalarFunction):

    def __init__(self):
        self.meter = None

    def open(self, function_context):
        # an average rate of events per second over 120s, default is 60s.
        self.meter = function_context.get_metric_group().meter("my_meter", time_span_in_seconds=120)

    def eval(self, i):
        self.meter.mark_event(i)
        return i - 1

```

`from pyflink.table.udf import ScalarFunction

class MyUDF(ScalarFunction):

    def __init__(self):
        self.meter = None

    def open(self, function_context):
        # an average rate of events per second over 120s, default is 60s.
        self.meter = function_context.get_metric_group().meter("my_meter", time_span_in_seconds=120)

    def eval(self, i):
        self.meter.mark_event(i)
        return i - 1
`

## Scope#


You can refer to the Java metric document for more details on Scope definition.


### User Scope#


You can define a user scope by calling MetricGroup.add_group(key: str, value: str = None).
If value is not None, creates a new key-value MetricGroup pair.
The key group is added to this group’s sub-groups, while the value group is added to the key
group’s sub-groups. In this case, the value group will be returned, and a user variable will be defined.

`MetricGroup.add_group(key: str, value: str = None)`
`value`
`None`

```
function_context \
    .get_metric_group() \
    .add_group("my_metrics") \
    .counter("my_counter")

function_context \
    .get_metric_group() \
    .add_group("my_metrics_key", "my_metrics_value") \
    .counter("my_counter")

```

`function_context \
    .get_metric_group() \
    .add_group("my_metrics") \
    .counter("my_counter")

function_context \
    .get_metric_group() \
    .add_group("my_metrics_key", "my_metrics_value") \
    .counter("my_counter")
`

### System Scope#


You can refer to the Java metric document for more details on System Scope.


### List of all Variables#


You can refer to the Java metric document for more details on List of all Variables.


### User Variables#


You can define a user variable by calling MetricGroup.addGroup(key: str, value: str = None) and
specifying the value parameter.

`MetricGroup.addGroup(key: str, value: str = None)`

Important: User variables cannot be used in scope formats.


```
function_context \
    .get_metric_group() \
    .add_group("my_metrics_key", "my_metrics_value") \
    .counter("my_counter")

```

`function_context \
    .get_metric_group() \
    .add_group("my_metrics_key", "my_metrics_value") \
    .counter("my_counter")
`

## Common part between PyFlink and Flink#


You can refer to the Java metric document for more details on the following sections:

* Reporter.
* System metrics.
* Latency tracking.
* REST API integration.
* Dashboard integration.

 Back to top
