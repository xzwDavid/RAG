# Cassandra


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Apache Cassandra Connector#


This connector provides sinks that writes data into a Apache Cassandra database.


To use this connector, add the following dependency to your project:


Only available for stable versions.


Note that the streaming connectors are currently NOT part of the binary distribution. See how to link with them for cluster execution here.


## Installing Apache Cassandra#


There are multiple ways to bring up a Cassandra instance on local machine:

1. Follow the instructions from Cassandra Getting Started page.
2. Launch a container running Cassandra from Official Docker Repository

## Cassandra Sinks#


### Configurations#


Flink’s Cassandra sink are created by using the static CassandraSink.addSink(DataStream input) method.
This method returns a CassandraSinkBuilder, which offers methods to further configure the sink, and finally build() the sink instance.

`build()`

The following configuration methods can be used:

1. setQuery(String query)

Sets the upsert query that is executed for every record the sink receives.
The query is internally treated as CQL statement.
DO set the upsert query for processing Tuple data type.
DO NOT set the query for processing POJO data types.


2. setClusterBuilder(ClusterBuilder clusterBuilder)

Sets the cluster builder that is used to configure the connection to cassandra with more sophisticated settings such as consistency level, retry policy and etc.


3. setHost(String host[, int port])

Simple version of setClusterBuilder() with host/port information to connect to Cassandra instances


4. setMapperOptions(MapperOptions options)

Sets the mapper options that are used to configure the DataStax ObjectMapper.
Only applies when processing POJO data types.


5. setMaxConcurrentRequests(int maxConcurrentRequests, Duration timeout)

Sets the maximum allowed number of concurrent requests with a timeout for acquiring permits to execute.
Only applies when enableWriteAheadLog() is not configured.


6. enableWriteAheadLog([CheckpointCommitter committer])

An optional setting
Allows exactly-once processing for non-deterministic algorithms.


7. setFailureHandler([CassandraFailureHandler failureHandler])

An optional setting
Sets the custom failure handler.


8. setDefaultKeyspace(String keyspace)

Sets the default keyspace to be used.


9. enableIgnoreNullFields()

Enables ignoring null values, treats null values as unset and avoids writing null fields and creating tombstones.


10. build()

Finalizes the configuration and constructs the CassandraSink instance.


* Sets the upsert query that is executed for every record the sink receives.
* The query is internally treated as CQL statement.
* DO set the upsert query for processing Tuple data type.
* DO NOT set the query for processing POJO data types.
* Sets the cluster builder that is used to configure the connection to cassandra with more sophisticated settings such as consistency level, retry policy and etc.
* Simple version of setClusterBuilder() with host/port information to connect to Cassandra instances
* Sets the mapper options that are used to configure the DataStax ObjectMapper.
* Only applies when processing POJO data types.
* Sets the maximum allowed number of concurrent requests with a timeout for acquiring permits to execute.
* Only applies when enableWriteAheadLog() is not configured.
* An optional setting
* Allows exactly-once processing for non-deterministic algorithms.
* An optional setting
* Sets the custom failure handler.
* Sets the default keyspace to be used.
* Enables ignoring null values, treats null values as unset and avoids writing null fields and creating tombstones.
* Finalizes the configuration and constructs the CassandraSink instance.

### Write-ahead Log#


A checkpoint committer stores additional information about completed checkpoints
in some resource. This information is used to prevent a full replay of the last
completed checkpoint in case of a failure.
You can use a CassandraCommitter to store these in a separate table in cassandra.
Note that this table will NOT be cleaned up by Flink.

`CassandraCommitter`

Flink can provide exactly-once guarantees if the query is idempotent (meaning it can be applied multiple
times without changing the result) and checkpointing is enabled. In case of a failure the failed
checkpoint will be replayed completely.


Furthermore, for non-deterministic programs the write-ahead log has to be enabled. For such a program
the replayed checkpoint may be completely different than the previous attempt, which may leave the
database in an inconsistent state since part of the first attempt may already be written.
The write-ahead log guarantees that the replayed checkpoint is identical to the first attempt.
Note that that enabling this feature will have an adverse impact on latency.


Note: The write-ahead log functionality is currently experimental. In many cases it is sufficient to use the connector without enabling it. Please report problems to the development mailing list.


### Checkpointing and Fault Tolerance#


With checkpointing enabled, Cassandra Sink guarantees at-least-once delivery of action requests to C* instance.


More details on checkpoints docs and fault tolerance guarantee docs


## Examples#


The Cassandra sink currently supports both Tuple and POJO data types, and Flink automatically detects which type of input is used. For general use of those streaming data types, please refer to Supported Data Types. We show two implementations based on 

    SocketWindowWordCount

, for POJO and Tuple data types respectively.


In all these examples, we assumed the associated Keyspace example and Table wordcount have been created.

`example`
`wordcount`

```
CREATE KEYSPACE IF NOT EXISTS example
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

CREATE TABLE IF NOT EXISTS example.wordcount (
    word text,
    count bigint,
    PRIMARY KEY(word)
);

```

`CREATE KEYSPACE IF NOT EXISTS example
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

CREATE TABLE IF NOT EXISTS example.wordcount (
    word text,
    count bigint,
    PRIMARY KEY(word)
);
`

### Cassandra Sink Example for Streaming Tuple Data Type#


While storing the result with Java/Scala Tuple data type to a Cassandra sink, it is required to set a CQL upsert statement (via setQuery(‘stmt’)) to persist each record back to the database. With the upsert query cached as PreparedStatement, each Tuple element is converted to parameters of the statement.

`PreparedStatement`

For details about PreparedStatement and BoundStatement, please visit DataStax Java Driver manual

`PreparedStatement`
`BoundStatement`

```
// get the execution environment
final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// get input data by connecting to the socket
DataStream<String> text = env.socketTextStream(hostname, port, "\n");

// parse the data, group it, window it, and aggregate the counts
DataStream<Tuple2<String, Long>> result = text
        .flatMap(new FlatMapFunction<String, Tuple2<String, Long>>() {
            @Override
            public void flatMap(String value, Collector<Tuple2<String, Long>> out) {
                // normalize and split the line
                String[] words = value.toLowerCase().split("\\s");

                // emit the pairs
                for (String word : words) {
                    //Do not accept empty word, since word is defined as primary key in C* table
                    if (!word.isEmpty()) {
                        out.collect(new Tuple2<String, Long>(word, 1L));
                    }
                }
            }
        })
        .keyBy(value -> value.f0)
        .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
        .sum(1);

CassandraSink.addSink(result)
        .setQuery("INSERT INTO example.wordcount(word, count) values (?, ?);")
        .setHost("127.0.0.1")
        .build();

```

`// get the execution environment
final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// get input data by connecting to the socket
DataStream<String> text = env.socketTextStream(hostname, port, "\n");

// parse the data, group it, window it, and aggregate the counts
DataStream<Tuple2<String, Long>> result = text
        .flatMap(new FlatMapFunction<String, Tuple2<String, Long>>() {
            @Override
            public void flatMap(String value, Collector<Tuple2<String, Long>> out) {
                // normalize and split the line
                String[] words = value.toLowerCase().split("\\s");

                // emit the pairs
                for (String word : words) {
                    //Do not accept empty word, since word is defined as primary key in C* table
                    if (!word.isEmpty()) {
                        out.collect(new Tuple2<String, Long>(word, 1L));
                    }
                }
            }
        })
        .keyBy(value -> value.f0)
        .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
        .sum(1);

CassandraSink.addSink(result)
        .setQuery("INSERT INTO example.wordcount(word, count) values (?, ?);")
        .setHost("127.0.0.1")
        .build();
`

```
val env: StreamExecutionEnvironment = StreamExecutionEnvironment.getExecutionEnvironment

// get input data by connecting to the socket
val text: DataStream[String] = env.socketTextStream(hostname, port, '\n')

// parse the data, group it, window it, and aggregate the counts
val result: DataStream[(String, Long)] = text
  // split up the lines in pairs (2-tuples) containing: (word,1)
  .flatMap(_.toLowerCase.split("\\s"))
  .filter(_.nonEmpty)
  .map((_, 1L))
  // group by the tuple field "0" and sum up tuple field "1"
  .keyBy(_._1)
  .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
  .sum(1)

CassandraSink.addSink(result)
  .setQuery("INSERT INTO example.wordcount(word, count) values (?, ?);")
  .setHost("127.0.0.1")
  .build()

result.print().setParallelism(1)

```

`val env: StreamExecutionEnvironment = StreamExecutionEnvironment.getExecutionEnvironment

// get input data by connecting to the socket
val text: DataStream[String] = env.socketTextStream(hostname, port, '\n')

// parse the data, group it, window it, and aggregate the counts
val result: DataStream[(String, Long)] = text
  // split up the lines in pairs (2-tuples) containing: (word,1)
  .flatMap(_.toLowerCase.split("\\s"))
  .filter(_.nonEmpty)
  .map((_, 1L))
  // group by the tuple field "0" and sum up tuple field "1"
  .keyBy(_._1)
  .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))
  .sum(1)

CassandraSink.addSink(result)
  .setQuery("INSERT INTO example.wordcount(word, count) values (?, ?);")
  .setHost("127.0.0.1")
  .build()

result.print().setParallelism(1)
`

### Cassandra Sink Example for Streaming POJO Data Type#


An example of streaming a POJO data type and store the same POJO entity back to Cassandra. In addition, this POJO implementation needs to follow DataStax Java Driver Manual to annotate the class as each field of this entity is mapped to an associated column of the designated table using the DataStax Java Driver com.datastax.driver.mapping.Mapper class.

`com.datastax.driver.mapping.Mapper`

The mapping of each table column can be defined through annotations placed on a field declaration in the Pojo class.  For details of the mapping, please refer to CQL documentation on Definition of Mapped Classes and CQL Data types


```
// get the execution environment
final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// get input data by connecting to the socket
DataStream<String> text = env.socketTextStream(hostname, port, "\n");

// parse the data, group it, window it, and aggregate the counts
DataStream<WordCount> result = text
        .flatMap(new FlatMapFunction<String, WordCount>() {
            public void flatMap(String value, Collector<WordCount> out) {
                // normalize and split the line
                String[] words = value.toLowerCase().split("\\s");

                // emit the pairs
                for (String word : words) {
                    if (!word.isEmpty()) {
                        //Do not accept empty word, since word is defined as primary key in C* table
                        out.collect(new WordCount(word, 1L));
                    }
                }
            }
        })
        .keyBy(WordCount::getWord)
        .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))

        .reduce(new ReduceFunction<WordCount>() {
            @Override
            public WordCount reduce(WordCount a, WordCount b) {
                return new WordCount(a.getWord(), a.getCount() + b.getCount());
            }
        });

CassandraSink.addSink(result)
        .setHost("127.0.0.1")
        .setMapperOptions(() -> new Mapper.Option[]{Mapper.Option.saveNullFields(true)})
        .build();


@Table(keyspace = "example", name = "wordcount")
public class WordCount {

    @Column(name = "word")
    private String word = "";

    @Column(name = "count")
    private long count = 0;

    public WordCount() {}

    public WordCount(String word, long count) {
        this.setWord(word);
        this.setCount(count);
    }

    public String getWord() {
        return word;
    }

    public void setWord(String word) {
        this.word = word;
    }

    public long getCount() {
        return count;
    }

    public void setCount(long count) {
        this.count = count;
    }

    @Override
    public String toString() {
        return getWord() + " : " + getCount();
    }
}

```

`// get the execution environment
final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// get input data by connecting to the socket
DataStream<String> text = env.socketTextStream(hostname, port, "\n");

// parse the data, group it, window it, and aggregate the counts
DataStream<WordCount> result = text
        .flatMap(new FlatMapFunction<String, WordCount>() {
            public void flatMap(String value, Collector<WordCount> out) {
                // normalize and split the line
                String[] words = value.toLowerCase().split("\\s");

                // emit the pairs
                for (String word : words) {
                    if (!word.isEmpty()) {
                        //Do not accept empty word, since word is defined as primary key in C* table
                        out.collect(new WordCount(word, 1L));
                    }
                }
            }
        })
        .keyBy(WordCount::getWord)
        .window(TumblingProcessingTimeWindows.of(Time.seconds(5)))

        .reduce(new ReduceFunction<WordCount>() {
            @Override
            public WordCount reduce(WordCount a, WordCount b) {
                return new WordCount(a.getWord(), a.getCount() + b.getCount());
            }
        });

CassandraSink.addSink(result)
        .setHost("127.0.0.1")
        .setMapperOptions(() -> new Mapper.Option[]{Mapper.Option.saveNullFields(true)})
        .build();


@Table(keyspace = "example", name = "wordcount")
public class WordCount {

    @Column(name = "word")
    private String word = "";

    @Column(name = "count")
    private long count = 0;

    public WordCount() {}

    public WordCount(String word, long count) {
        this.setWord(word);
        this.setCount(count);
    }

    public String getWord() {
        return word;
    }

    public void setWord(String word) {
        this.word = word;
    }

    public long getCount() {
        return count;
    }

    public void setCount(long count) {
        this.count = count;
    }

    @Override
    public String toString() {
        return getWord() + " : " + getCount();
    }
}
`

 Back to top
