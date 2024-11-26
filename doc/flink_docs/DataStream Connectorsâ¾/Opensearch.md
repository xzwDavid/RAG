# Opensearch


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Opensearch Connector#


This connector provides sinks that can request document actions to an
Opensearch Index. To use this connector, add
the following dependency to your project:


Only available for stable versions.


Only available for stable versions.


```
      By default, Apache Flink Opensearch Connector uses 1.3.x client libraries. You could switch to use 2.x (or upcoming 3.x) clients noting that those require **JDK-11 or above**, for example.

      ```xml
      <dependencyManagement>
          <dependencies>
              <dependency>
                  <groupId>org.opensearch</groupId>
                  <artifactId>opensearch</artifactId>
                  <version>2.5.0</version>
              </dependency>          
              <dependency>
                  <groupId>org.opensearch.client</groupId>
                  <artifactId>opensearch-rest-high-level-client</artifactId>
                  <version>2.5.0</version>
              </dependency>
          </dependencies>
      </dependencyManagement>
      ```
    </td>
</tr>

```

`      By default, Apache Flink Opensearch Connector uses 1.3.x client libraries. You could switch to use 2.x (or upcoming 3.x) clients noting that those require **JDK-11 or above**, for example.

      ```xml
      <dependencyManagement>
          <dependencies>
              <dependency>
                  <groupId>org.opensearch</groupId>
                  <artifactId>opensearch</artifactId>
                  <version>2.5.0</version>
              </dependency>          
              <dependency>
                  <groupId>org.opensearch.client</groupId>
                  <artifactId>opensearch-rest-high-level-client</artifactId>
                  <version>2.5.0</version>
              </dependency>
          </dependencies>
      </dependencyManagement>
      ```
    </td>
</tr>
`

Note that the streaming connectors are currently not part of the binary
distribution. See here for information
about how to package the program with the libraries for cluster execution.


## Installing Opensearch#


Instructions for setting up an Opensearch cluster can be found
here.


## Opensearch Sink#


The example below shows how to configure and create a sink:


```
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.connector.opensearch.sink.Opensearch2SinkBuilder;
import org.apache.flink.streaming.api.datastream.DataStream;

import org.apache.http.HttpHost;
import org.opensearch.action.index.IndexRequest;
import org.opensearch.client.Requests;

import java.util.HashMap;
import java.util.Map;

DataStream<String> input = ...;

input.sinkTo(
    new OpensearchSinkBuilder<String>()
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
import org.apache.flink.connector.opensearch.sink.Opensearch2SinkBuilder;
import org.apache.flink.streaming.api.datastream.DataStream;

import org.apache.http.HttpHost;
import org.opensearch.action.index.IndexRequest;
import org.opensearch.client.Requests;

import java.util.HashMap;
import java.util.Map;

DataStream<String> input = ...;

input.sinkTo(
    new OpensearchSinkBuilder<String>()
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

```
import org.apache.flink.api.connector.sink.SinkWriter
import org.apache.flink.connector.opensearch.sink.{OpensearchSinkBuilder, RequestIndexer}
import org.apache.flink.streaming.api.datastream.DataStream
import org.apache.http.HttpHost
import org.opensearch.action.index.IndexRequest
import org.opensearch.client.Requests

val input: DataStream[String] = ...

input.sinkTo(
  new OpensearchSinkBuilder[String]
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
import org.apache.flink.connector.opensearch.sink.{OpensearchSinkBuilder, RequestIndexer}
import org.apache.flink.streaming.api.datastream.DataStream
import org.apache.http.HttpHost
import org.opensearch.action.index.IndexRequest
import org.opensearch.client.Requests

val input: DataStream[String] = ...

input.sinkTo(
  new OpensearchSinkBuilder[String]
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

Note that the example only demonstrates performing a single index
request for each incoming element. Generally, the OpensearchEmitter
can be used to perform requests of different types (ex.,
DeleteRequest, UpdateRequest, etc.).

`OpensearchEmitter`
`DeleteRequest`
`UpdateRequest`

Internally, each parallel instance of the Flink Opensearch Sink uses
a BulkProcessor to send action requests to the cluster.
This will buffer elements before sending them in bulk to the cluster. The BulkProcessor
executes bulk requests one at a time, i.e. there will be no two concurrent
flushes of the buffered actions in progress.

`BulkProcessor`
`BulkProcessor`

### Opensearch Sinks and Fault Tolerance#


With Flinkâs checkpointing enabled, the Flink Opensearch Sink guarantees
at-least-once delivery of action requests to Opensearch clusters. It does
so by waiting for all pending action requests in the BulkProcessor at the
time of checkpoints. This effectively assures that all requests before the
checkpoint was triggered have been successfully acknowledged by Opensearch, before
proceeding to process more records sent to the sink.

`BulkProcessor`

More details on checkpoints and fault tolerance are in the fault tolerance docs.


To use fault tolerant Opensearch Sinks, checkpointing of the topology needs to be enabled at the execution environment:


```
final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.enableCheckpointing(5000); // checkpoint every 5000 msecs

```

`final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env.enableCheckpointing(5000); // checkpoint every 5000 msecs
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.enableCheckpointing(5000) // checkpoint every 5000 msecs

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.enableCheckpointing(5000) // checkpoint every 5000 msecs
`


IMPORTANT: Checkpointing is not enabled by default but the default delivery guarantee is `AT_LEAST_ONCE`.
This causes the sink to buffer requests until it either finishes or the `BulkProcessor` flushes automatically. 
By default, the `BulkProcessor` will flush after `1000` added actions. To configure the processor to flush more frequently, please refer to the BulkProcessor configuration section.




Using `UpdateRequests` with deterministic IDs and the upsert method it is possible to achieve exactly-once semantics in Opensearch when `AT_LEAST_ONCE` delivery is configured for the connector.



### Handling Failing Opensearch Requests#


Opensearch action requests may fail due to a variety of reasons, including
temporarily saturated node queue capacity or malformed documents to be indexed.
The Flink Opensearch Sink allows the user to retry requests by specifying a backoff-policy.


Below is an example:


```
DataStream<String> input = ...;

input.sinkTo(
    new OpensearchSinkBuilder<String>()
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
    new OpensearchSinkBuilder<String>()
        .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
        .setEmitter(
        (element, context, indexer) ->
        indexer.add(createIndexRequest(element)))
        // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
        .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
        .build());
`

```
val input: DataStream[String] = ...

input.sinkTo(
  new OpensearchSinkBuilder[String]
    .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
    .setEmitter((element: String, context: SinkWriter.Context, indexer: RequestIndexer) => 
    indexer.add(createIndexRequest(element)))
    // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
    .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
    .build())

```

`val input: DataStream[String] = ...

input.sinkTo(
  new OpensearchSinkBuilder[String]
    .setHosts(new HttpHost("127.0.0.1", 9200, "http"))
    .setEmitter((element: String, context: SinkWriter.Context, indexer: RequestIndexer) => 
    indexer.add(createIndexRequest(element)))
    // This enables an exponential backoff retry mechanism, with a maximum of 5 retries and an initial delay of 1000 milliseconds
    .setBulkFlushBackoffStrategy(FlushBackoffType.EXPONENTIAL, 5, 1000)
    .build())
`

The above example will let the sink re-add requests that failed due to resource constrains (e.g.
queue capacity saturation). For all other failures, such as malformed documents, the sink will fail.
If no BulkFlushBackoffStrategy (or FlushBackoffType.NONE) is configured, the sink will fail for any kind of error.

`BulkFlushBackoffStrategy`
`FlushBackoffType.NONE`


IMPORTANT: Re-adding requests back to the internal BulkProcessor
on failures will lead to longer checkpoints, as the sink will also
need to wait for the re-added requests to be flushed when checkpointing.
For example, when using FlushBackoffType.EXPONENTIAL, checkpoints
will need to wait until Opensearch node queues have enough capacity for
all the pending requests, or until the maximum number of retries has been reached.



### Configuring the Internal Bulk Processor#


The internal BulkProcessor can be further configured for its behaviour
on how buffered action requests are flushed, by using the following methods of the OpensearchSinkBuilder:

`BulkProcessor`
* setBulkFlushMaxActions(int numMaxActions): Maximum amount of actions to buffer before flushing.
* setBulkFlushMaxSizeMb(int maxSizeMb): Maximum size of data (in megabytes) to buffer before flushing.
* setBulkFlushInterval(long intervalMillis): Interval at which to flush regardless of the amount or size of buffered actions.

Configuring how temporary request errors are retried is also supported:

* setBulkFlushBackoffStrategy(FlushBackoffType flushBackoffType, int maxRetries, long delayMillis): The type of backoff delay, either CONSTANT or EXPONENTIAL, the amount of backoff retries to attempt, the amount of delay for backoff. For constant backoff, this
is simply the delay between each retry. For exponential backoff, this is the initial base delay.
`CONSTANT`
`EXPONENTIAL`

More information about Opensearch can be found here.


## Packaging the Opensearch Connector into an Uber-Jar#


For the execution of your Flink program, it is recommended to build a
so-called uber-jar (executable jar) containing all your dependencies
(see here for further information).


Alternatively, you can put the connector’s jar file into Flink’s lib/ folder to make it available
system-wide, i.e. for all job being run.

`lib/`

 Back to top
