# JDBC


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# JDBC Connector#


This connector provides a sink that writes data to a JDBC database.


To use it, add the following dependency to your project (along with your JDBC driver):


Only available for stable versions.


Note that the streaming connectors are currently NOT part of the binary distribution. See how to link with them for cluster execution here.
A driver dependency is also required to connect to a specified database. Please consult your database documentation on how to add the corresponding driver.


## JdbcSink.sink#

`JdbcSink.sink`

The JDBC sink provides at-least-once guarantee.
Effectively though, exactly-once can be achieved by crafting upsert SQL statements or idempotent SQL updates.
Configuration goes as follow (see also 

    JdbcSink javadoc

).


```
JdbcSink.sink(
      	sqlDmlStatement,                       // mandatory
      	jdbcStatementBuilder,                  // mandatory   	
      	jdbcExecutionOptions,                  // optional
      	jdbcConnectionOptions                  // mandatory
);

```

`JdbcSink.sink(
      	sqlDmlStatement,                       // mandatory
      	jdbcStatementBuilder,                  // mandatory   	
      	jdbcExecutionOptions,                  // optional
      	jdbcConnectionOptions                  // mandatory
);
`

```
JdbcSink.sink(
    sql_dml_statement,          # mandatory
    type_info,                  # mandatory
    jdbc_connection_options,    # mandatory
    jdbc_execution_options      # optional
)

```

`JdbcSink.sink(
    sql_dml_statement,          # mandatory
    type_info,                  # mandatory
    jdbc_connection_options,    # mandatory
    jdbc_execution_options      # optional
)
`

### SQL DML statement and JDBC statement builder#


The sink builds one JDBC prepared statement from a user-provider SQL string, e.g.:


```
INSERT INTO some_table field1, field2 values (?, ?)

```

`INSERT INTO some_table field1, field2 values (?, ?)
`

It then repeatedly calls a user-provided function to update that prepared statement with each value of the stream, e.g.:


```
(preparedStatement, someRecord) -> { ... update here the preparedStatement with values from someRecord ... }

```

`(preparedStatement, someRecord) -> { ... update here the preparedStatement with values from someRecord ... }
`

### JDBC execution options#


The SQL DML statements are executed in batches, which can optionally be configured with the following instance (see also 

    JdbcExecutionOptions javadoc

)


```
JdbcExecutionOptions.builder()
        .withBatchIntervalMs(200)             // optional: default = 0, meaning no time-based execution is done
        .withBatchSize(1000)                  // optional: default = 5000 values
        .withMaxRetries(5)                    // optional: default = 3 
.build();

```

`JdbcExecutionOptions.builder()
        .withBatchIntervalMs(200)             // optional: default = 0, meaning no time-based execution is done
        .withBatchSize(1000)                  // optional: default = 5000 values
        .withMaxRetries(5)                    // optional: default = 3 
.build();
`

```
JdbcExecutionOptions.builder() \
    .with_batch_interval_ms(2000) \
    .with_batch_size(100) \
    .with_max_retries(5) \
    .build()

```

`JdbcExecutionOptions.builder() \
    .with_batch_interval_ms(2000) \
    .with_batch_size(100) \
    .with_max_retries(5) \
    .build()
`

A JDBC batch is executed as soon as one of the following conditions is true:

* the configured batch interval time is elapsed
* the maximum batch size is reached
* a Flink checkpoint has started

### JDBC connection parameters#


The connection to the database is configured with a JdbcConnectionOptions instance.
Please see 

    JdbcConnectionOptions javadoc

 for details

`JdbcConnectionOptions`

### Full example#


```
public class JdbcSinkExample {

    static class Book {
        public Book(Long id, String title, String authors, Integer year) {
            this.id = id;
            this.title = title;
            this.authors = authors;
            this.year = year;
        }
        final Long id;
        final String title;
        final String authors;
        final Integer year;
    }

    public static void main(String[] args) throws Exception {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();

        env.fromElements(
                new Book(101L, "Stream Processing with Apache Flink", "Fabian Hueske, Vasiliki Kalavri", 2019),
                new Book(102L, "Streaming Systems", "Tyler Akidau, Slava Chernyak, Reuven Lax", 2018),
                new Book(103L, "Designing Data-Intensive Applications", "Martin Kleppmann", 2017),
                new Book(104L, "Kafka: The Definitive Guide", "Gwen Shapira, Neha Narkhede, Todd Palino", 2017)
        ).addSink(
                JdbcSink.sink(
                        "insert into books (id, title, authors, year) values (?, ?, ?, ?)",
                        (statement, book) -> {
                            statement.setLong(1, book.id);
                            statement.setString(2, book.title);
                            statement.setString(3, book.authors);
                            statement.setInt(4, book.year);
                        },
                        JdbcExecutionOptions.builder()
                                .withBatchSize(1000)
                                .withBatchIntervalMs(200)
                                .withMaxRetries(5)
                                .build(),
                        new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
                                .withUrl("jdbc:postgresql://dbhost:5432/postgresdb")
                                .withDriverName("org.postgresql.Driver")
                                .withUsername("someUser")
                                .withPassword("somePassword")
                                .build()
                ));
                
        env.execute();
    }
}

```

`public class JdbcSinkExample {

    static class Book {
        public Book(Long id, String title, String authors, Integer year) {
            this.id = id;
            this.title = title;
            this.authors = authors;
            this.year = year;
        }
        final Long id;
        final String title;
        final String authors;
        final Integer year;
    }

    public static void main(String[] args) throws Exception {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();

        env.fromElements(
                new Book(101L, "Stream Processing with Apache Flink", "Fabian Hueske, Vasiliki Kalavri", 2019),
                new Book(102L, "Streaming Systems", "Tyler Akidau, Slava Chernyak, Reuven Lax", 2018),
                new Book(103L, "Designing Data-Intensive Applications", "Martin Kleppmann", 2017),
                new Book(104L, "Kafka: The Definitive Guide", "Gwen Shapira, Neha Narkhede, Todd Palino", 2017)
        ).addSink(
                JdbcSink.sink(
                        "insert into books (id, title, authors, year) values (?, ?, ?, ?)",
                        (statement, book) -> {
                            statement.setLong(1, book.id);
                            statement.setString(2, book.title);
                            statement.setString(3, book.authors);
                            statement.setInt(4, book.year);
                        },
                        JdbcExecutionOptions.builder()
                                .withBatchSize(1000)
                                .withBatchIntervalMs(200)
                                .withMaxRetries(5)
                                .build(),
                        new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
                                .withUrl("jdbc:postgresql://dbhost:5432/postgresdb")
                                .withDriverName("org.postgresql.Driver")
                                .withUsername("someUser")
                                .withPassword("somePassword")
                                .build()
                ));
                
        env.execute();
    }
}
`

```
env = StreamExecutionEnvironment.get_execution_environment()
type_info = Types.ROW([Types.INT(), Types.STRING(), Types.STRING(), Types.INT()])
env.from_collection(
    [(101, "Stream Processing with Apache Flink", "Fabian Hueske, Vasiliki Kalavri", 2019),
     (102, "Streaming Systems", "Tyler Akidau, Slava Chernyak, Reuven Lax", 2018),
     (103, "Designing Data-Intensive Applications", "Martin Kleppmann", 2017),
     (104, "Kafka: The Definitive Guide", "Gwen Shapira, Neha Narkhede, Todd Palino", 2017)
     ], type_info=type_info) \
    .add_sink(
    JdbcSink.sink(
        "insert into books (id, title, authors, year) values (?, ?, ?, ?)",
        type_info,
        JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
            .with_url('jdbc:postgresql://dbhost:5432/postgresdb')
            .with_driver_name('org.postgresql.Driver')
            .with_user_name('someUser')
            .with_password('somePassword')
            .build(),
        JdbcExecutionOptions.builder()
            .with_batch_interval_ms(1000)
            .with_batch_size(200)
            .with_max_retries(5)
            .build()
    ))

env.execute()

```

`env = StreamExecutionEnvironment.get_execution_environment()
type_info = Types.ROW([Types.INT(), Types.STRING(), Types.STRING(), Types.INT()])
env.from_collection(
    [(101, "Stream Processing with Apache Flink", "Fabian Hueske, Vasiliki Kalavri", 2019),
     (102, "Streaming Systems", "Tyler Akidau, Slava Chernyak, Reuven Lax", 2018),
     (103, "Designing Data-Intensive Applications", "Martin Kleppmann", 2017),
     (104, "Kafka: The Definitive Guide", "Gwen Shapira, Neha Narkhede, Todd Palino", 2017)
     ], type_info=type_info) \
    .add_sink(
    JdbcSink.sink(
        "insert into books (id, title, authors, year) values (?, ?, ?, ?)",
        type_info,
        JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
            .with_url('jdbc:postgresql://dbhost:5432/postgresdb')
            .with_driver_name('org.postgresql.Driver')
            .with_user_name('someUser')
            .with_password('somePassword')
            .build(),
        JdbcExecutionOptions.builder()
            .with_batch_interval_ms(1000)
            .with_batch_size(200)
            .with_max_retries(5)
            .build()
    ))

env.execute()
`

## JdbcSink.exactlyOnceSink#

`JdbcSink.exactlyOnceSink`

Since 1.13, Flink JDBC sink supports exactly-once mode.
The implementation relies on the JDBC driver support of XA
standard.
Most drivers support XA if the database also supports XA (so the driver is usually the same).


To use it, create a sink using exactlyOnceSink() method as above and additionally provide:

`exactlyOnceSink()`
* 

    exactly-once options


* 

    execution options


* XA DataSource Supplier

For example:


```
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env
        .fromElements(...)
        .addSink(JdbcSink.exactlyOnceSink(
                "insert into books (id, title, author, price, qty) values (?,?,?,?,?)",
                (ps, t) -> {
                    ps.setInt(1, t.id);
                    ps.setString(2, t.title);
                    ps.setString(3, t.author);
                    ps.setDouble(4, t.price);
                    ps.setInt(5, t.qty);
                },
                JdbcExecutionOptions.builder()
                    .withMaxRetries(0)
                    .build(),
                JdbcExactlyOnceOptions.defaults(),
                () -> {
                    // create a driver-specific XA DataSource
                    // The following example is for derby 
                    EmbeddedXADataSource ds = new EmbeddedXADataSource();
                    ds.setDatabaseName("my_db");
                    return ds;
                });
env.execute();

```

`StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
env
        .fromElements(...)
        .addSink(JdbcSink.exactlyOnceSink(
                "insert into books (id, title, author, price, qty) values (?,?,?,?,?)",
                (ps, t) -> {
                    ps.setInt(1, t.id);
                    ps.setString(2, t.title);
                    ps.setString(3, t.author);
                    ps.setDouble(4, t.price);
                    ps.setInt(5, t.qty);
                },
                JdbcExecutionOptions.builder()
                    .withMaxRetries(0)
                    .build(),
                JdbcExactlyOnceOptions.defaults(),
                () -> {
                    // create a driver-specific XA DataSource
                    // The following example is for derby 
                    EmbeddedXADataSource ds = new EmbeddedXADataSource();
                    ds.setDatabaseName("my_db");
                    return ds;
                });
env.execute();
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

NOTE: Some databases only allow a single XA transaction per connection (e.g. PostgreSQL, MySQL).
In such cases, please use the following API to construct JdbcExactlyOnceOptions:

`JdbcExactlyOnceOptions`

```
JdbcExactlyOnceOptions.builder()
.withTransactionPerConnection(true)
.build();

```

`JdbcExactlyOnceOptions.builder()
.withTransactionPerConnection(true)
.build();
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

This will make Flink use a separate connection for every XA transaction. This may require adjusting connection limits.
For PostgreSQL and MySQL, this can be done by increasing max_connections.

`max_connections`

Furthermore, XA needs to be enabled and/or configured in some databases.
For PostgreSQL, you should set max_prepared_transactions to some value greater than zero.
For MySQL v8+, you should grant XA_RECOVER_ADMIN to Flink DB user.

`max_prepared_transactions`
`XA_RECOVER_ADMIN`

ATTENTION: Currently, JdbcSink.exactlyOnceSink can ensure exactly once semantics
with JdbcExecutionOptions.maxRetries == 0; otherwise, duplicated results maybe produced.

`JdbcSink.exactlyOnceSink`
`JdbcExecutionOptions.maxRetries == 0`

### XADataSourceexamples#

`XADataSource`

PostgreSQL XADataSource example:






Java
PGXADataSource xaDataSource = new org.postgresql.xa.PGXADataSource();
xaDataSource.setUrl("jdbc:postgresql://localhost:5432/postgres");
xaDataSource.setUser(username);
xaDataSource.setPassword(password);

Python
Still not supported in Python API.



`XADataSource`

```
PGXADataSource xaDataSource = new org.postgresql.xa.PGXADataSource();
xaDataSource.setUrl("jdbc:postgresql://localhost:5432/postgres");
xaDataSource.setUser(username);
xaDataSource.setPassword(password);

```

`PGXADataSource xaDataSource = new org.postgresql.xa.PGXADataSource();
xaDataSource.setUrl("jdbc:postgresql://localhost:5432/postgres");
xaDataSource.setUser(username);
xaDataSource.setPassword(password);
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

MySQL XADataSource example:






Java
MysqlXADataSource xaDataSource = new com.mysql.cj.jdbc.MysqlXADataSource();
xaDataSource.setUrl("jdbc:mysql://localhost:3306/");
xaDataSource.setUser(username);
xaDataSource.setPassword(password);

Python
Still not supported in Python API.



`XADataSource`

```
MysqlXADataSource xaDataSource = new com.mysql.cj.jdbc.MysqlXADataSource();
xaDataSource.setUrl("jdbc:mysql://localhost:3306/");
xaDataSource.setUser(username);
xaDataSource.setPassword(password);

```

`MysqlXADataSource xaDataSource = new com.mysql.cj.jdbc.MysqlXADataSource();
xaDataSource.setUrl("jdbc:mysql://localhost:3306/");
xaDataSource.setUser(username);
xaDataSource.setPassword(password);
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

Oracle XADataSource example:






Java
OracleXADataSource xaDataSource = new oracle.jdbc.xa.OracleXADataSource();
xaDataSource.setURL("jdbc:oracle:oci8:@");
xaDataSource.setUser("scott");
xaDataSource.setPassword("tiger");

Python
Still not supported in Python API.



`XADataSource`

```
OracleXADataSource xaDataSource = new oracle.jdbc.xa.OracleXADataSource();
xaDataSource.setURL("jdbc:oracle:oci8:@");
xaDataSource.setUser("scott");
xaDataSource.setPassword("tiger");

```

`OracleXADataSource xaDataSource = new oracle.jdbc.xa.OracleXADataSource();
xaDataSource.setURL("jdbc:oracle:oci8:@");
xaDataSource.setUser("scott");
xaDataSource.setPassword("tiger");
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

Please also take Oracle connection pooling into account.


Please refer to the JdbcXaSinkFunction documentation for more details.

`JdbcXaSinkFunction`