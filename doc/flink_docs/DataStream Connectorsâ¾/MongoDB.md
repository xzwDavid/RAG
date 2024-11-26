# MongoDB


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# MongoDB Connector#


Flink provides a MongoDB connector for reading and writing data from
and to MongoDB collections with at-least-once guarantees.


To use this connector, add one of the following dependencies to your project.


Only available for stable versions.


## MongoDB Source#


The example below shows how to configure and create a source:


```
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.typeinfo.BasicTypeInfo;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.source.reader.deserializer.MongoDeserializationSchema;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import org.bson.BsonDocument;

MongoSource<String> source = MongoSource.<String>builder()
        .setUri("mongodb://user:password@127.0.0.1:27017")
        .setDatabase("my_db")
        .setCollection("my_coll")
        .setProjectedFields("_id", "f0", "f1")
        .setFetchSize(2048)
        .setLimit(10000)
        .setNoCursorTimeout(true)
        .setPartitionStrategy(PartitionStrategy.SAMPLE)
        .setPartitionSize(MemorySize.ofMebiBytes(64))
        .setSamplesPerPartition(10)
        .setDeserializationSchema(new MongoDeserializationSchema<String>() {
            @Override
            public String deserialize(BsonDocument document) {
                return document.toJson();
            }

            @Override
            public TypeInformation<String> getProducedType() {
                return BasicTypeInfo.STRING_TYPE_INFO;
            }
        })
        .build();

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

env.fromSource(source, WatermarkStrategy.noWatermarks(), "MongoDB-Source")
        .setParallelism(2)
        .print()
        .setParallelism(1);

```

`import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.typeinfo.BasicTypeInfo;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.connector.mongodb.source.MongoSource;
import org.apache.flink.connector.mongodb.source.reader.deserializer.MongoDeserializationSchema;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import org.bson.BsonDocument;

MongoSource<String> source = MongoSource.<String>builder()
        .setUri("mongodb://user:password@127.0.0.1:27017")
        .setDatabase("my_db")
        .setCollection("my_coll")
        .setProjectedFields("_id", "f0", "f1")
        .setFetchSize(2048)
        .setLimit(10000)
        .setNoCursorTimeout(true)
        .setPartitionStrategy(PartitionStrategy.SAMPLE)
        .setPartitionSize(MemorySize.ofMebiBytes(64))
        .setSamplesPerPartition(10)
        .setDeserializationSchema(new MongoDeserializationSchema<String>() {
            @Override
            public String deserialize(BsonDocument document) {
                return document.toJson();
            }

            @Override
            public TypeInformation<String> getProducedType() {
                return BasicTypeInfo.STRING_TYPE_INFO;
            }
        })
        .build();

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

env.fromSource(source, WatermarkStrategy.noWatermarks(), "MongoDB-Source")
        .setParallelism(2)
        .print()
        .setParallelism(1);
`

### Configurations#


Flink’s MongoDB source is created by using the static builder MongoSource.<OutputType>builder().

`MongoSource.<OutputType>builder()`
1. setUri(String uri)

Required.
Sets the connection string of MongoDB.


2. setDatabase(String database)

Required.
Name of the database to read from.


3. setCollection(String collection)

Required.
Name of the collection to read from.


4. setFetchSize(int fetchSize)

Optional. Default: 2048.
Sets the number of documents should be fetched per round-trip when reading.


5. setNoCursorTimeout(boolean noCursorTimeout)

Optional. Default: true.
The MongoDB server normally times out idle cursors after an inactivity period (10 minutes) to
prevent excess memory use. Set this option to prevent that. If a session is idle for longer
than 30 minutes, the MongoDB server marks that session as expired and may close it at any
time. When the MongoDB server closes the session, it also kills any in-progress operations
and open cursors associated with the session. This includes cursors configured with
noCursorTimeout() or a maxTimeMS() greater than 30 minutes.


6. setPartitionStrategy(PartitionStrategy partitionStrategy)

Optional. Default: PartitionStrategy.DEFAULT.
Sets the partition strategy. Available partition strategies are SINGLE, SAMPLE, SPLIT_VECTOR,
SHARDED and DEFAULT. You can see Partition Strategies section for detail.


7. setPartitionSize(MemorySize partitionSize)

Optional. Default: 64mb.
Sets the partition memory size of MongoDB split. Split a MongoDB collection into multiple
partitions according to the partition memory size. Partitions can be read in parallel by
multiple readers to speed up the overall read time.


8. setSamplesPerPartition(int samplesPerPartition)

Optional. Default: 10.
Sets the number of samples to take per partition which is only used for the sample partition
strategy SAMPLE. The sample partitioner samples the collection, projects and sorts by the
partition fields. Then uses every samplesPerPartition as the value to use to calculate the
partition boundaries. The total number of samples taken is:
samples per partition * ( count of documents / number of documents per partition).


9. setLimit(int limit)

Optional. Default: -1.
Sets the limit of documents for each reader to read. If limit is not set or set to -1,
the documents of the entire collection will be read. If we set the parallelism of reading to
be greater than 1, the maximum documents to read is equal to the parallelism * limit.


10. setProjectedFields(String… projectedFields)

Optional.
Sets the projection fields of documents to read. If projected fields is not set, all fields of
the collection will be read.


11. setDeserializationSchema(MongoDeserializationSchema deserializationSchema)

Required.
A MongoDeserializationSchema is required for parsing MongoDB BSON documents.


* Required.
* Sets the connection string of MongoDB.
* Required.
* Name of the database to read from.
* Required.
* Name of the collection to read from.
* Optional. Default: 2048.
* Sets the number of documents should be fetched per round-trip when reading.
`2048`
* Optional. Default: true.
* The MongoDB server normally times out idle cursors after an inactivity period (10 minutes) to
prevent excess memory use. Set this option to prevent that. If a session is idle for longer
than 30 minutes, the MongoDB server marks that session as expired and may close it at any
time. When the MongoDB server closes the session, it also kills any in-progress operations
and open cursors associated with the session. This includes cursors configured with
noCursorTimeout() or a maxTimeMS() greater than 30 minutes.
`true`
`noCursorTimeout()`
`maxTimeMS()`
* Optional. Default: PartitionStrategy.DEFAULT.
* Sets the partition strategy. Available partition strategies are SINGLE, SAMPLE, SPLIT_VECTOR,
SHARDED and DEFAULT. You can see Partition Strategies section for detail.
`PartitionStrategy.DEFAULT`
`SINGLE`
`SAMPLE`
`SPLIT_VECTOR`
`SHARDED`
`DEFAULT`
* Optional. Default: 64mb.
* Sets the partition memory size of MongoDB split. Split a MongoDB collection into multiple
partitions according to the partition memory size. Partitions can be read in parallel by
multiple readers to speed up the overall read time.
`64mb`
* Optional. Default: 10.
* Sets the number of samples to take per partition which is only used for the sample partition
strategy SAMPLE. The sample partitioner samples the collection, projects and sorts by the
partition fields. Then uses every samplesPerPartition as the value to use to calculate the
partition boundaries. The total number of samples taken is:
samples per partition * ( count of documents / number of documents per partition).
`10`
`SAMPLE`
`samplesPerPartition`
`samples per partition * ( count of documents / number of documents per partition)`
* Optional. Default: -1.
* Sets the limit of documents for each reader to read. If limit is not set or set to -1,
the documents of the entire collection will be read. If we set the parallelism of reading to
be greater than 1, the maximum documents to read is equal to the parallelism * limit.
`-1`
`parallelism * limit`
* Optional.
* Sets the projection fields of documents to read. If projected fields is not set, all fields of
the collection will be read.
* Required.
* A MongoDeserializationSchema is required for parsing MongoDB BSON documents.
`MongoDeserializationSchema`

### Partition Strategies#


Partitions can be read in parallel by multiple readers to speed up the overall read time.
The following partition strategies are provided:

* SINGLE: treats the entire collection as a single partition.
* SAMPLE: samples the collection and generate partitions which is fast but possibly uneven.
* SPLIT_VECTOR: uses the splitVector command to generate partitions for non-sharded
collections which is fast and even. The splitVector permission is required.
* SHARDED: reads config.chunks (MongoDB splits a sharded collection into chunks, and the
range of the chunks are stored within the collection) as the partitions directly. The
sharded strategy only used for sharded collection which is fast and even. Read permission
of config database is required.
* DEFAULT: uses sharded strategy for sharded collections otherwise using split vector
strategy.
`SINGLE`
`SAMPLE`
`SPLIT_VECTOR`
`SHARDED`
`config.chunks`
`DEFAULT`

## MongoDB Sink#


The example below shows how to configure and create a sink:


```
import org.apache.flink.connector.base.DeliveryGuarantee;
import org.apache.flink.connector.mongodb.sink.MongoSink;
import org.apache.flink.streaming.api.datastream.DataStream;

import com.mongodb.client.model.InsertOneModel;
import org.bson.BsonDocument;

DataStream<String> stream = ...;

MongoSink<String> sink = MongoSink.<String>builder()
        .setUri("mongodb://user:password@127.0.0.1:27017")
        .setDatabase("my_db")
        .setCollection("my_coll")
        .setBatchSize(1000)
        .setBatchIntervalMs(1000)
        .setMaxRetries(3)
        .setDeliveryGuarantee(DeliveryGuarantee.AT_LEAST_ONCE)
        .setSerializationSchema(
                (input, context) -> new InsertOneModel<>(BsonDocument.parse(input)))
        .build();

stream.sinkTo(sink);

```

`import org.apache.flink.connector.base.DeliveryGuarantee;
import org.apache.flink.connector.mongodb.sink.MongoSink;
import org.apache.flink.streaming.api.datastream.DataStream;

import com.mongodb.client.model.InsertOneModel;
import org.bson.BsonDocument;

DataStream<String> stream = ...;

MongoSink<String> sink = MongoSink.<String>builder()
        .setUri("mongodb://user:password@127.0.0.1:27017")
        .setDatabase("my_db")
        .setCollection("my_coll")
        .setBatchSize(1000)
        .setBatchIntervalMs(1000)
        .setMaxRetries(3)
        .setDeliveryGuarantee(DeliveryGuarantee.AT_LEAST_ONCE)
        .setSerializationSchema(
                (input, context) -> new InsertOneModel<>(BsonDocument.parse(input)))
        .build();

stream.sinkTo(sink);
`

### Configurations#


Flink’s MongoDB sink is created by using the static builder MongoSink.<InputType>builder().

`MongoSink.<InputType>builder()`
1. setUri(String uri)

Required.
Sets the connection string of MongoDB.


2. setDatabase(String database)

Required.
Name of the database to sink to.


3. setCollection(String collection)

Required.
Name of the collection to sink to.


4. setBatchSize(int batchSize)

Optional. Default: 1000.
Sets the maximum number of actions to buffer for each batch request.
You can pass -1 to disable batching.


5. setBatchIntervalMs(long batchIntervalMs)

Optional. Default: 1000.
Sets the batch flush interval, in milliseconds. You can pass -1 to disable it.


6. setMaxRetries(int maxRetries)

Optional. Default: 3.
Sets the max retry times if writing records failed.


7. setDeliveryGuarantee(DeliveryGuarantee deliveryGuarantee)

Optional. Default: DeliveryGuarantee.AT_LEAST_ONCE.
Sets the wanted DeliveryGuarantee. The EXACTLY_ONCE guarantee is not supported yet.


8. setSerializationSchema(MongoSerializationSchema serializationSchema)

Required.
A MongoSerializationSchema is required for parsing input record to MongoDB
WriteModel.


* Required.
* Sets the connection string of MongoDB.
* Required.
* Name of the database to sink to.
* Required.
* Name of the collection to sink to.
* Optional. Default: 1000.
* Sets the maximum number of actions to buffer for each batch request.
You can pass -1 to disable batching.
`1000`
* Optional. Default: 1000.
* Sets the batch flush interval, in milliseconds. You can pass -1 to disable it.
`1000`
* Optional. Default: 3.
* Sets the max retry times if writing records failed.
`3`
* Optional. Default: DeliveryGuarantee.AT_LEAST_ONCE.
* Sets the wanted DeliveryGuarantee. The EXACTLY_ONCE guarantee is not supported yet.
`DeliveryGuarantee.AT_LEAST_ONCE`
`DeliveryGuarantee`
`EXACTLY_ONCE`
* Required.
* A MongoSerializationSchema is required for parsing input record to MongoDB
WriteModel.
`MongoSerializationSchema`

### Fault Tolerance#


With Flinkâs checkpointing enabled, the Flink MongoDB Sink guarantees
at-least-once delivery of write operations to MongoDB clusters. It does
so by waiting for all pending write operations in the MongoWriter at the
time of checkpoints. This effectively assures that all requests before the
checkpoint was triggered have been successfully acknowledged by MongoDB, before
proceeding to process more records sent to the sink.

`MongoWriter`

More details on checkpoints and fault tolerance are in the fault tolerance docs.


To use fault tolerant MongoDB Sinks, checkpointing of the topology needs to be enabled at the execution environment:


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
This causes the sink to buffer requests until it either finishes or the `MongoWriter` flushes automatically. 
By default, the `MongoWriter` will flush after 1000 added write operations. To configure the writer to flush more frequently,
please refer to the MongoWriter configuration section.




Using WriteModel with deterministic ids and the upsert method it is possible to achieve exactly-once 
semantics in MongoDB when AT_LEAST_ONCE delivery is configured for the connector.



### Configuring the Internal Mongo Writer#


The internal MongoWriter can be further configured for its behaviour on how write operations are
flushed, by using the following methods of the MongoSinkBuilder:

`MongoWriter`
`MongoSinkBuilder`
* setBatchSize(int batchSize): Maximum amount of write operations to buffer before flushing. You can pass -1 to disable it.
* setBatchIntervalMs(long batchIntervalMs): Interval at which to flush regardless of the size of buffered write operations. You can pass -1 to disable it.

When set as follows, there are the following writing behaviours:

* Flush when time interval or batch size exceed limit.

batchSize > 1 and batchInterval > 0


* Flush only on checkpoint.

batchSize == -1 and batchInterval == -1


* Flush for every single write operation.

batchSize == 1 or batchInterval == 0


* batchSize > 1 and batchInterval > 0
* batchSize == -1 and batchInterval == -1
* batchSize == 1 or batchInterval == 0