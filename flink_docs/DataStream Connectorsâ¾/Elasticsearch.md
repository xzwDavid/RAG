# Elasticsearch


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Elasticsearch Connector#


This connector provides sinks that can request document actions to an
Elasticsearch Index. To use this connector, add one
of the following dependencies to your project, depending on the version
of the Elasticsearch installation:


Only available for stable versions.


Only available for stable versions.




In order to use the  in PyFlink jobs, the following
dependencies are required:



Version
PyFlink JAR



flink-connector-elasticsearch6
Only available for stable releases.


flink-connector-elasticsearch7
Only available for stable releases.




See Python dependency management
for more details on how to use JARs in PyFlink.




Note that the streaming connectors are currently not part of the binary
distribution. See here for information
about how to package the program with the libraries for cluster execution.


## Installing Elasticsearch#


Instructions for setting up an Elasticsearch cluster can be found
here.


## Elasticsearch Sink#


The example below shows how to configure and create a sink:


Elasticsearch 6:


```
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch6SinkBuilder;
import org.apache.flink.streaming.api.datastream.DataStream;

import org.apache.http.HttpHost;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.client.Requests;

import java.util.HashMap;
import java.util.Map;

DataStream<String> input = ...;

input.sinkTo(
    new Elasticsearch6SinkBuilder<String>()
        .setBulkFlushMaxActions(1) // Instructs the sink to emit after every element, otherwise they would be buffered
        .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
        .setEmitter(
        (element, context, indexer) ->
        indexer.add(createIndexRequest(element)))
        .build());

private static IndexRequest createIndexRequest(String element) {
    Map<String, Object> json = new HashMap<>();
    json.put("data", element);

    return Requests.indexRequest()
        .index("my-index")
        .type("my-type")
        .id(element)
        .source(json);
}

```

`import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch6SinkBuilder;
import org.apache.flink.streaming.api.datastream.DataStream;

import org.apache.http.HttpHost;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.client.Requests;

import java.util.HashMap;
import java.util.Map;

DataStream<String> input = ...;

input.sinkTo(
    new Elasticsearch6SinkBuilder<String>()
        .setBulkFlushMaxActions(1) // Instructs the sink to emit after every element, otherwise they would be buffered
        .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
        .setEmitter(
        (element, context, indexer) ->
        indexer.add(createIndexRequest(element)))
        .build());

private static IndexRequest createIndexRequest(String element) {
    Map<String, Object> json = new HashMap<>();
    json.put("data", element);

    return Requests.indexRequest()
        .index("my-index")
        .type("my-type")
        .id(element)
        .source(json);
}
`

Elasticsearch 7:


```
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch7SinkBuilder;
import org.apache.flink.streaming.api.datastream.DataStream;

import org.apache.http.HttpHost;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.client.Requests;

import java.util.HashMap;
import java.util.Map;

DataStream<String> input = ...;

input.sinkTo(
    new Elasticsearch7SinkBuilder<String>()
        .setBulkFlushMaxActions(1) // Instructs the sink to emit after every element, otherwise they would be buffered
        .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
        .setEmitter(
        (element, context, indexer) ->
        indexer.add(createIndexRequest(element)))
        .build());

private static IndexRequest createIndexRequest(String element) {
    Map<String, Object> json = new HashMap<>();
    json.put("data", element);

    return Requests.indexRequest()
        .index("my-index")
        .id(element)
        .source(json);
}

```

`import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.connector.elasticsearch.sink.Elasticsearch7SinkBuilder;
import org.apache.flink.streaming.api.datastream.DataStream;

import org.apache.http.HttpHost;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.client.Requests;

import java.util.HashMap;
import java.util.Map;

DataStream<String> input = ...;

input.sinkTo(
    new Elasticsearch7SinkBuilder<String>()
        .setBulkFlushMaxActions(1) // Instructs the sink to emit after every element, otherwise they would be buffered
        .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
        .setEmitter(
        (element, context, indexer) ->
        indexer.add(createIndexRequest(element)))
        .build());

private static IndexRequest createIndexRequest(String element) {
    Map<String, Object> json = new HashMap<>();
    json.put("data", element);

    return Requests.indexRequest()
        .index("my-index")
        .id(element)
        .source(json);
}
`

Elasticsearch 6:


```
import org.apache.flink.api.connector.sink.SinkWriter
import org.apache.flink.connector.elasticsearch.sink.{Elasticsearch6SinkBuilder, RequestIndexer}
import org.apache.flink.streaming.api.datastream.DataStream
import org.apache.http.HttpHost
import org.elasticsearch.action.index.IndexRequest
import org.elasticsearch.client.Requests

val input: DataStream[String] = ...

input.sinkTo(
  new Elasticsearch6SinkBuilder[String]
    .setBulkFlushMaxActions(1) // Instructs the sink to emit after every element, otherwise they would be buffered
    .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
    .setEmitter((element: String, context: SinkWriter.Context, indexer: RequestIndexer) => 
    indexer.add(createIndexRequest(element)))
    .build())

def createIndexRequest(element: (String)): IndexRequest = {

  val json = Map(
    "data" -> element.asInstanceOf[AnyRef]
  )

  Requests.indexRequest.index("my-index").`type`("my-type").source(mapAsJavaMap(json))
}

```

`import org.apache.flink.api.connector.sink.SinkWriter
import org.apache.flink.connector.elasticsearch.sink.{Elasticsearch6SinkBuilder, RequestIndexer}
import org.apache.flink.streaming.api.datastream.DataStream
import org.apache.http.HttpHost
import org.elasticsearch.action.index.IndexRequest
import org.elasticsearch.client.Requests

val input: DataStream[String] = ...

input.sinkTo(
  new Elasticsearch6SinkBuilder[String]
    .setBulkFlushMaxActions(1) // Instructs the sink to emit after every element, otherwise they would be buffered
    .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
    .setEmitter((element: String, context: SinkWriter.Context, indexer: RequestIndexer) => 
    indexer.add(createIndexRequest(element)))
    .build())

def createIndexRequest(element: (String)): IndexRequest = {

  val json = Map(
    "data" -> element.asInstanceOf[AnyRef]
  )

  Requests.indexRequest.index("my-index").`type`("my-type").source(mapAsJavaMap(json))
}
`

Elasticsearch 7:


```
import org.apache.flink.api.connector.sink.SinkWriter
import org.apache.flink.connector.elasticsearch.sink.{Elasticsearch7SinkBuilder, RequestIndexer}
import org.apache.flink.streaming.api.datastream.DataStream
import org.apache.http.HttpHost
import org.elasticsearch.action.index.IndexRequest
import org.elasticsearch.client.Requests

val input: DataStream[String] = ...

input.sinkTo(
  new Elasticsearch7SinkBuilder[String]
    .setBulkFlushMaxActions(1) // Instructs the sink to emit after every element, otherwise they would be buffered
    .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
    .setEmitter((element: String, context: SinkWriter.Context, indexer: RequestIndexer) => 
    indexer.add(createIndexRequest(element)))
    .build())

def createIndexRequest(element: (String)): IndexRequest = {

  val json = Map(
    "data" -> element.asInstanceOf[AnyRef]
  )

  Requests.indexRequest.index("my-index").source(mapAsJavaMap(json))
}

```

`import org.apache.flink.api.connector.sink.SinkWriter
import org.apache.flink.connector.elasticsearch.sink.{Elasticsearch7SinkBuilder, RequestIndexer}
import org.apache.flink.streaming.api.datastream.DataStream
import org.apache.http.HttpHost
import org.elasticsearch.action.index.IndexRequest
import org.elasticsearch.client.Requests

val input: DataStream[String] = ...

input.sinkTo(
  new Elasticsearch7SinkBuilder[String]
    .setBulkFlushMaxActions(1) // Instructs the sink to emit after every element, otherwise they would be buffered
    .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
    .setEmitter((element: String, context: SinkWriter.Context, indexer: RequestIndexer) => 
    indexer.add(createIndexRequest(element)))
    .build())

def createIndexRequest(element: (String)): IndexRequest = {

  val json = Map(
    "data" -> element.asInstanceOf[AnyRef]
  )

  Requests.indexRequest.index("my-index").source(mapAsJavaMap(json))
}
`

Elasticsearch 6 static index:


```
from pyflink.datastream.connectors.elasticsearch import Elasticsearch6SinkBuilder, ElasticsearchEmitter

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars(ELASTICSEARCH_SQL_CONNECTOR_PATH)

input = ...

# The set_bulk_flush_max_actions instructs the sink to emit after every element, otherwise they would be buffered
es6_sink = Elasticsearch6SinkBuilder() \
    .set_bulk_flush_max_actions(1) \
    .set_emitter(ElasticsearchEmitter.static_index('foo', 'id', 'bar')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es6_sink).name('es6 sink')

```

`from pyflink.datastream.connectors.elasticsearch import Elasticsearch6SinkBuilder, ElasticsearchEmitter

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars(ELASTICSEARCH_SQL_CONNECTOR_PATH)

input = ...

# The set_bulk_flush_max_actions instructs the sink to emit after every element, otherwise they would be buffered
es6_sink = Elasticsearch6SinkBuilder() \
    .set_bulk_flush_max_actions(1) \
    .set_emitter(ElasticsearchEmitter.static_index('foo', 'id', 'bar')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es6_sink).name('es6 sink')
`

Elasticsearch 6 dynamic index:


```
from pyflink.datastream.connectors.elasticsearch import Elasticsearch6SinkBuilder, ElasticsearchEmitter

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars(ELASTICSEARCH_SQL_CONNECTOR_PATH)

input = ...

es_sink = Elasticsearch6SinkBuilder() \
    .set_emitter(ElasticsearchEmitter.dynamic_index('name', 'id', 'bar')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es6_sink).name('es6 dynamic index sink')

```

`from pyflink.datastream.connectors.elasticsearch import Elasticsearch6SinkBuilder, ElasticsearchEmitter

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars(ELASTICSEARCH_SQL_CONNECTOR_PATH)

input = ...

es_sink = Elasticsearch6SinkBuilder() \
    .set_emitter(ElasticsearchEmitter.dynamic_index('name', 'id', 'bar')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es6_sink).name('es6 dynamic index sink')
`

Elasticsearch 7 static index:


```
from pyflink.datastream.connectors.elasticsearch import Elasticsearch7SinkBuilder, ElasticsearchEmitter

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars(ELASTICSEARCH_SQL_CONNECTOR_PATH)

input = ...

# The set_bulk_flush_max_actions instructs the sink to emit after every element, otherwise they would be buffered
es7_sink = Elasticsearch7SinkBuilder() \
    .set_bulk_flush_max_actions(1) \
    .set_emitter(ElasticsearchEmitter.static('foo', 'id')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es7_sink).name('es7 sink')

```

`from pyflink.datastream.connectors.elasticsearch import Elasticsearch7SinkBuilder, ElasticsearchEmitter

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars(ELASTICSEARCH_SQL_CONNECTOR_PATH)

input = ...

# The set_bulk_flush_max_actions instructs the sink to emit after every element, otherwise they would be buffered
es7_sink = Elasticsearch7SinkBuilder() \
    .set_bulk_flush_max_actions(1) \
    .set_emitter(ElasticsearchEmitter.static('foo', 'id')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es7_sink).name('es7 sink')
`

Elasticsearch 7 dynamic index:


```
from pyflink.datastream.connectors.elasticsearch import Elasticsearch7SinkBuilder, ElasticsearchEmitter

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars(ELASTICSEARCH_SQL_CONNECTOR_PATH)

input = ...

es7_sink = Elasticsearch7SinkBuilder() \
    .set_emitter(ElasticsearchEmitter.dynamic_index('name', 'id')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es7_sink).name('es7 dynamic index sink')

```

`from pyflink.datastream.connectors.elasticsearch import Elasticsearch7SinkBuilder, ElasticsearchEmitter

env = StreamExecutionEnvironment.get_execution_environment()
env.add_jars(ELASTICSEARCH_SQL_CONNECTOR_PATH)

input = ...

es7_sink = Elasticsearch7SinkBuilder() \
    .set_emitter(ElasticsearchEmitter.dynamic_index('name', 'id')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es7_sink).name('es7 dynamic index sink')
`

Note that the example only demonstrates performing a single index
request for each incoming element. Generally, the ElasticsearchEmitter
can be used to perform requests of different types (ex.,
DeleteRequest, UpdateRequest, etc.).

`ElasticsearchEmitter`
`DeleteRequest`
`UpdateRequest`

Internally, each parallel instance of the Flink Elasticsearch Sink uses
a BulkProcessor to send action requests to the cluster.
This will buffer elements before sending them in bulk to the cluster. The BulkProcessor
executes bulk requests one at a time, i.e. there will be no two concurrent
flushes of the buffered actions in progress.

`BulkProcessor`
`BulkProcessor`

### Elasticsearch Sinks and Fault Tolerance#


With Flinkâs checkpointing enabled, the Flink Elasticsearch Sink guarantees
at-least-once delivery of action requests to Elasticsearch clusters. It does
so by waiting for all pending action requests in the BulkProcessor at the
time of checkpoints. This effectively assures that all requests before the
checkpoint was triggered have been successfully acknowledged by Elasticsearch, before
proceeding to process more records sent to the sink.

`BulkProcessor`

More details on checkpoints and fault tolerance are in the fault tolerance docs.


To use fault tolerant Elasticsearch Sinks, checkpointing of the topology needs to be enabled at the execution environment:


```
final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.enableCheckpointing(5000); // checkpoint every 5000 msecs

```

`final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.enableCheckpointing(5000); // checkpoint every 5000 msecs
`

Elasticsearch 6:


```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.enableCheckpointing(5000) // checkpoint every 5000 msecs

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.enableCheckpointing(5000) // checkpoint every 5000 msecs
`

```
env = StreamExecutionEnvironment.get_execution_environment()
# checkpoint every 5000 msecs
env.enable_checkpointing(5000)

```

`env = StreamExecutionEnvironment.get_execution_environment()
# checkpoint every 5000 msecs
env.enable_checkpointing(5000)
`


IMPORTANT: Checkpointing is not enabled by default but the default delivery guarantee is AT_LEAST_ONCE.
This causes the sink to buffer requests until it either finishes or the BulkProcessor flushes automatically. 
By default, the BulkProcessor will flush after 1000 added Actions. To configure the processor to flush more frequently, please refer to the BulkProcessor configuration section.




Using UpdateRequests with deterministic ids and the upsert method it is possible to achieve exactly-once semantics in Elasticsearch when AT_LEAST_ONCE delivery is configured for the connector.



### Handling Failing Elasticsearch Requests#


Elasticsearch action requests may fail due to a variety of reasons, including
temporarily saturated node queue capacity or malformed documents to be indexed.
The Flink Elasticsearch Sink allows the user to retry requests by specifying a backoff-policy.


Below is an example:


Elasticsearch 6:


```
DataStream<String> input = ...;

input.sinkTo(
    new Elasticsearch6SinkBuilder<String>()
        .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
        .setEmitter(
        (element, context, indexer) ->
        indexer.add(createIndexRequest(element)))
        // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
        .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
        .build());

```

`DataStream<String> input = ...;

input.sinkTo(
    new Elasticsearch6SinkBuilder<String>()
        .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
        .setEmitter(
        (element, context, indexer) ->
        indexer.add(createIndexRequest(element)))
        // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
        .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
        .build());
`

Elasticsearch 7:


```
DataStream<String> input = ...;

input.sinkTo(
    new Elasticsearch7SinkBuilder<String>()
        .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
        .setEmitter(
        (element, context, indexer) ->
        indexer.add(createIndexRequest(element)))
        // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
        .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
        .build());

```

`DataStream<String> input = ...;

input.sinkTo(
    new Elasticsearch7SinkBuilder<String>()
        .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
        .setEmitter(
        (element, context, indexer) ->
        indexer.add(createIndexRequest(element)))
        // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
        .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
        .build());
`

Elasticsearch 6:


```
val input: DataStream[String] = ...

input.sinkTo(
  new Elasticsearch6SinkBuilder[String]
    .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
    .setEmitter((element: String, context: SinkWriter.Context, indexer: RequestIndexer) => 
    indexer.add(createIndexRequest(element)))
    // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
    .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
    .build())

```

`val input: DataStream[String] = ...

input.sinkTo(
  new Elasticsearch6SinkBuilder[String]
    .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
    .setEmitter((element: String, context: SinkWriter.Context, indexer: RequestIndexer) => 
    indexer.add(createIndexRequest(element)))
    // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
    .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
    .build())
`

Elasticsearch 7:


```
val input: DataStream[String] = ...

input.sinkTo(
  new Elasticsearch7SinkBuilder[String]
    .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
    .setEmitter((element: String, context: SinkWriter.Context, indexer: RequestIndexer) => 
    indexer.add(createIndexRequest(element)))
    // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
    .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
    .build())

```

`val input: DataStream[String] = ...

input.sinkTo(
  new Elasticsearch7SinkBuilder[String]
    .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
    .setEmitter((element: String, context: SinkWriter.Context, indexer: RequestIndexer) => 
    indexer.add(createIndexRequest(element)))
    // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
    .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
    .build())
`

Elasticsearch 6:


```
input = ...

# This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
es_sink = Elasticsearch6SinkBuilder() \
    .set_bulk_flush_backoff_strategy(FlushBackoffType.CONSTANT, 5, 1000) \
    .set_emitter(ElasticsearchEmitter.static_index('foo', 'id', 'bar')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es_sink).name('es6 sink')

```

`input = ...

# This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
es_sink = Elasticsearch6SinkBuilder() \
    .set_bulk_flush_backoff_strategy(FlushBackoffType.CONSTANT, 5, 1000) \
    .set_emitter(ElasticsearchEmitter.static_index('foo', 'id', 'bar')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es_sink).name('es6 sink')
`

Elasticsearch 7:


```
input = ...

# This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
es7_sink = Elasticsearch7SinkBuilder() \
    .set_bulk_flush_backoff_strategy(FlushBackoffType.EXPONENTIAL, 5, 1000) \
    .set_emitter(ElasticsearchEmitter.static_index('foo', 'id')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es7_sink).name('es7 sink')

```

`input = ...

# This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
es7_sink = Elasticsearch7SinkBuilder() \
    .set_bulk_flush_backoff_strategy(FlushBackoffType.EXPONENTIAL, 5, 1000) \
    .set_emitter(ElasticsearchEmitter.static_index('foo', 'id')) \
    .set_hosts(['localhost:9200']) \
    .build()

input.sink_to(es7_sink).name('es7 sink')
`

The above example will let the sink re-add requests that failed due to resource constrains (e.g.
queue capacity saturation). For all other failures, such as malformed documents, the sink will fail.
If no BulkFlushBackoffStrategy (or FlushBackoffType.NONE) is configured, the sink will fail for any kind of error.

`FlushBackoffType.NONE`


IMPORTANT: Re-adding requests back to the internal BulkProcessor
on failures will lead to longer checkpoints, as the sink will also
need to wait for the re-added requests to be flushed when checkpointing.
For example, when using FlushBackoffType.EXPONENTIAL, checkpoints
will need to wait until Elasticsearch node queues have enough capacity for
all the pending requests, or until the maximum number of retries has been reached.



### Configuring the Internal Bulk Processor#


The internal BulkProcessor can be further configured for its behaviour
on how buffered action requests are flushed, by using the following methods of the Elasticsearch6SinkBuilder:

`BulkProcessor`
* setBulkFlushMaxActions(int numMaxActions): Maximum amount of actions to buffer before flushing.
* setBulkFlushMaxSizeMb(int maxSizeMb): Maximum size of data (in megabytes) to buffer before flushing.
* setBulkFlushInterval(long intervalMillis): Interval at which to flush regardless of the amount or size of buffered actions.

Configuring how temporary request errors are retried is also supported:

* setBulkFlushBackoffStrategy(FlushBackoffType flushBackoffType, int maxRetries, long delayMillis): The type of backoff delay, either CONSTANT or EXPONENTIAL, the amount of backoff retries to attempt, the amount of delay for backoff. For constant backoff, this
is simply the delay between each retry. For exponential backoff, this is the initial base delay.
`CONSTANT`
`EXPONENTIAL`

More information about Elasticsearch can be found here.


## Packaging the Elasticsearch Connector into an Uber-Jar#


For the execution of your Flink program, it is recommended to build a
so-called uber-jar (executable jar) containing all your dependencies
(see here for further information).


Alternatively, you can put the connector’s jar file into Flink’s lib/ folder to make it available
system-wide, i.e. for all job being run.

`lib/`

 Back to top
