# Intro to the Python Table API


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Intro to the Python Table API#


This document is a short introduction to the PyFlink Table API, which is used to help novice users quickly understand the basic usage of PyFlink Table API.
For advanced usage, please refer to other documents in this user guide.


## Common Structure of Python Table API Program#


All Table API and SQL programs, both batch and streaming, follow the same pattern. The following code example shows the common structure of Table API and SQL programs.


```
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col

# 1. create a TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

# 2. create source Table
table_env.execute_sql("""
    CREATE TABLE datagen (
        id INT,
        data STRING
    ) WITH (
        'connector' = 'datagen',
        'fields.id.kind' = 'sequence',
        'fields.id.start' = '1',
        'fields.id.end' = '10'
    )
""")

# 3. create sink Table
table_env.execute_sql("""
    CREATE TABLE print (
        id INT,
        data STRING
    ) WITH (
        'connector' = 'print'
    )
""")

# 4. query from source table and perform calculations
# create a Table from a Table API query:
source_table = table_env.from_path("datagen")
# or create a Table from a SQL query:
# source_table = table_env.sql_query("SELECT * FROM datagen")

result_table = source_table.select(col("id") + 1, col("data"))

# 5. emit query result to sink table
# emit a Table API result Table to a sink table:
result_table.execute_insert("print").wait()
# or emit results via SQL query:
# table_env.execute_sql("INSERT INTO print SELECT * FROM datagen").wait()

```

`from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col

# 1. create a TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

# 2. create source Table
table_env.execute_sql("""
    CREATE TABLE datagen (
        id INT,
        data STRING
    ) WITH (
        'connector' = 'datagen',
        'fields.id.kind' = 'sequence',
        'fields.id.start' = '1',
        'fields.id.end' = '10'
    )
""")

# 3. create sink Table
table_env.execute_sql("""
    CREATE TABLE print (
        id INT,
        data STRING
    ) WITH (
        'connector' = 'print'
    )
""")

# 4. query from source table and perform calculations
# create a Table from a Table API query:
source_table = table_env.from_path("datagen")
# or create a Table from a SQL query:
# source_table = table_env.sql_query("SELECT * FROM datagen")

result_table = source_table.select(col("id") + 1, col("data"))

# 5. emit query result to sink table
# emit a Table API result Table to a sink table:
result_table.execute_insert("print").wait()
# or emit results via SQL query:
# table_env.execute_sql("INSERT INTO print SELECT * FROM datagen").wait()
`

 Back to top


## Create a TableEnvironment#


TableEnvironment is a central concept of the Table API and SQL integration. The following code example shows how to create a TableEnvironment:

`TableEnvironment`

```
from pyflink.table import EnvironmentSettings, TableEnvironment

# create a streaming TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

# or create a batch TableEnvironment
env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

```

`from pyflink.table import EnvironmentSettings, TableEnvironment

# create a streaming TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

# or create a batch TableEnvironment
env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)
`

For more details about the different ways to create a TableEnvironment, please refer to the TableEnvironment Documentation.

`TableEnvironment`

TableEnvironment is responsible for:

`TableEnvironment`
* Table management: Creating Tables, listing Tables, Conversion between Table and DataStream, etc.
* User-defined function management: User-defined function registration, dropping, listing, etc. See General User-defined Functions and Vectorized User-defined Functions for more details about Python user-defined functions.
* Executing SQL queries: See Write SQL Queries for more details.
* Job configuration: See Python Configuration for more details.
* Python dependency management: See Dependency Management for more details.
* Job submission: See Emit Results for more details.
`Table`

 Back to top


## Create Tables#


Table is a core component of the Python Table API. A Table object describes a pipeline of data transformations. It does not
contain the data itself in any way. Instead, it describes how to read data from a table source,
and how to eventually write data to a table sink. The declared pipeline can be
printed, optimized, and eventually executed in a cluster. The pipeline can work with bounded or
unbounded streams which enables both streaming and batch scenarios.

`Table`
`Table`

A Table is always bound to a specific TableEnvironment. It is not possible to combine tables from different TableEnvironments in same query, e.g., to join or union them.

`Table`
`TableEnvironment`

### Create using a List Object#


You can create a Table from a list object, this is usually used when writing examples or unit tests.


```
from pyflink.table import EnvironmentSettings, TableEnvironment

# create a batch TableEnvironment
env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')])
table.execute().print()

```

`from pyflink.table import EnvironmentSettings, TableEnvironment

# create a batch TableEnvironment
env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')])
table.execute().print()
`

The results are as following:


```
+----------------------+--------------------------------+
|                   _1 |                             _2 |
+----------------------+--------------------------------+
|                    1 |                             Hi |
|                    2 |                          Hello |
+----------------------+--------------------------------+

```

`+----------------------+--------------------------------+
|                   _1 |                             _2 |
+----------------------+--------------------------------+
|                    1 |                             Hi |
|                    2 |                          Hello |
+----------------------+--------------------------------+
`

You can also create a Table with specified column names:


```
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table.execute().print()

```

`table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table.execute().print()
`

The results are as following:


```
+----------------------+--------------------------------+
|                   id |                           data |
+----------------------+--------------------------------+
|                    1 |                             Hi |
|                    2 |                          Hello |
+----------------------+--------------------------------+

```

`+----------------------+--------------------------------+
|                   id |                           data |
+----------------------+--------------------------------+
|                    1 |                             Hi |
|                    2 |                          Hello |
+----------------------+--------------------------------+
`

By default, the table schema is extracted from the data automatically. If the automatically generated table schema isn’t as expected, you can also specify it manually:


```
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
# by default, the type of the "id" column is BIGINT
print('By default the type of the "id" column is %s.' % table.get_schema().get_field_data_type("id"))

from pyflink.table import DataTypes
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')],
                                DataTypes.ROW([DataTypes.FIELD("id", DataTypes.TINYINT()),
                                               DataTypes.FIELD("data", DataTypes.STRING())]))
# now the type of the "id" column is set as TINYINT
print('Now the type of the "id" column is %s.' % table.get_schema().get_field_data_type("id"))

```

`table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
# by default, the type of the "id" column is BIGINT
print('By default the type of the "id" column is %s.' % table.get_schema().get_field_data_type("id"))

from pyflink.table import DataTypes
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')],
                                DataTypes.ROW([DataTypes.FIELD("id", DataTypes.TINYINT()),
                                               DataTypes.FIELD("data", DataTypes.STRING())]))
# now the type of the "id" column is set as TINYINT
print('Now the type of the "id" column is %s.' % table.get_schema().get_field_data_type("id"))
`

The results are as following:


```
By default the type of the "id" column is BIGINT.
Now the type of the "id" column is TINYINT.

```

`By default the type of the "id" column is BIGINT.
Now the type of the "id" column is TINYINT.
`

### Create using DDL statements#


You can also create a Table using SQL DDL statements. It represents a Table which reads data from the specified external storage.


```
from pyflink.table import EnvironmentSettings, TableEnvironment

# create a stream TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table_env.execute_sql("""
    CREATE TABLE random_source (
        id BIGINT, 
        data TINYINT 
    ) WITH (
        'connector' = 'datagen',
        'fields.id.kind'='sequence',
        'fields.id.start'='1',
        'fields.id.end'='3',
        'fields.data.kind'='sequence',
        'fields.data.start'='4',
        'fields.data.end'='6'
    )
""")
table = table_env.from_path("random_source")
table.execute().print()

```

`from pyflink.table import EnvironmentSettings, TableEnvironment

# create a stream TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table_env.execute_sql("""
    CREATE TABLE random_source (
        id BIGINT, 
        data TINYINT 
    ) WITH (
        'connector' = 'datagen',
        'fields.id.kind'='sequence',
        'fields.id.start'='1',
        'fields.id.end'='3',
        'fields.data.kind'='sequence',
        'fields.data.start'='4',
        'fields.data.end'='6'
    )
""")
table = table_env.from_path("random_source")
table.execute().print()
`

The results are as following:


```
+----+----------------------+--------+
| op |                   id |   data |
+----+----------------------+--------+
| +I |                    1 |      4 |
| +I |                    2 |      5 |
| +I |                    3 |      6 |
+----+----------------------+--------+

```

`+----+----------------------+--------+
| op |                   id |   data |
+----+----------------------+--------+
| +I |                    1 |      4 |
| +I |                    2 |      5 |
| +I |                    3 |      6 |
+----+----------------------+--------+
`

### Create using TableDescriptor#


TableDescriptor is another way to define a Table. It’s equivalent to SQL DDL statements.


```
from pyflink.table import EnvironmentSettings, TableEnvironment, TableDescriptor, Schema, DataTypes

# create a stream TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table_env.create_temporary_table(
    'random_source',
    TableDescriptor.for_connector('datagen')
        .schema(Schema.new_builder()
                .column('id', DataTypes.BIGINT())
                .column('data', DataTypes.TINYINT())
                .build())
        .option('fields.id.kind', 'sequence')
        .option('fields.id.start', '1')
        .option('fields.id.end', '3')
        .option('fields.data.kind', 'sequence')
        .option('fields.data.start', '4')
        .option('fields.data.end', '6')
        .build())

table = table_env.from_path("random_source")
table.execute().print()

```

`from pyflink.table import EnvironmentSettings, TableEnvironment, TableDescriptor, Schema, DataTypes

# create a stream TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table_env.create_temporary_table(
    'random_source',
    TableDescriptor.for_connector('datagen')
        .schema(Schema.new_builder()
                .column('id', DataTypes.BIGINT())
                .column('data', DataTypes.TINYINT())
                .build())
        .option('fields.id.kind', 'sequence')
        .option('fields.id.start', '1')
        .option('fields.id.end', '3')
        .option('fields.data.kind', 'sequence')
        .option('fields.data.start', '4')
        .option('fields.data.end', '6')
        .build())

table = table_env.from_path("random_source")
table.execute().print()
`

The results are as following:


```
+----+----------------------+--------+
| op |                   id |   data |
+----+----------------------+--------+
| +I |                    1 |      4 |
| +I |                    2 |      5 |
| +I |                    3 |      6 |
+----+----------------------+--------+

```

`+----+----------------------+--------+
| op |                   id |   data |
+----+----------------------+--------+
| +I |                    1 |      4 |
| +I |                    2 |      5 |
| +I |                    3 |      6 |
+----+----------------------+--------+
`

### Create using a Catalog#


TableEnvironment maintains a map of catalogs of tables which are created with an identifier.

`TableEnvironment`

The tables in a catalog may either be temporary, and tied to the lifecycle of a single Flink session, or permanent, and visible across multiple Flink sessions.


The tables and views created via SQL DDL, e.g. “create table …” and “create view …” are also stored in a catalog.


You can directly access the tables in a catalog via SQL.


If you want to use tables from a catalog with the Table API, you can use the “from_path” method to create the Table API objects:


```
# prepare the catalog
# register Table API tables in the catalog
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table_env.create_temporary_view('source_table', table)

# create Table API table from catalog
new_table = table_env.from_path('source_table')
new_table.execute().print()

```

`# prepare the catalog
# register Table API tables in the catalog
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table_env.create_temporary_view('source_table', table)

# create Table API table from catalog
new_table = table_env.from_path('source_table')
new_table.execute().print()
`

The results are as following:


```
+----+----------------------+--------------------------------+
| op |                   id |                           data |
+----+----------------------+--------------------------------+
| +I |                    1 |                             Hi |
| +I |                    2 |                          Hello |
+----+----------------------+--------------------------------+

```

`+----+----------------------+--------------------------------+
| op |                   id |                           data |
+----+----------------------+--------------------------------+
| +I |                    1 |                             Hi |
| +I |                    2 |                          Hello |
+----+----------------------+--------------------------------+
`

 Back to top


## Write Queries#


### Write Table API Queries#


The Table object offers many methods for applying relational operations.
These methods return new Table objects representing the result of applying the relational operations on the input Table.
These relational operations may be composed of multiple method calls, such as table.group_by(...).select(...).

`Table`
`Table`
`Table`
`table.group_by(...).select(...)`

The Table API documentation describes all Table API operations that are supported on streaming and batch tables.


The following example shows a simple Table API aggregation query:


```
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import call, col

# using batch table environment to execute the queries
env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

orders = table_env.from_elements([('Jack', 'FRANCE', 10), ('Rose', 'ENGLAND', 30), ('Jack', 'FRANCE', 20)],
                                 ['name', 'country', 'revenue'])

# compute revenue for all customers from France
revenue = orders \
    .select(col("name"), col("country"), col("revenue")) \
    .where(col("country") == 'FRANCE') \
    .group_by(col("name")) \
    .select(col("name"), call("sum", col("revenue")).alias('rev_sum'))

revenue.execute().print()

```

`from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import call, col

# using batch table environment to execute the queries
env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

orders = table_env.from_elements([('Jack', 'FRANCE', 10), ('Rose', 'ENGLAND', 30), ('Jack', 'FRANCE', 20)],
                                 ['name', 'country', 'revenue'])

# compute revenue for all customers from France
revenue = orders \
    .select(col("name"), col("country"), col("revenue")) \
    .where(col("country") == 'FRANCE') \
    .group_by(col("name")) \
    .select(col("name"), call("sum", col("revenue")).alias('rev_sum'))

revenue.execute().print()
`

The results are as following:


```
+--------------------------------+----------------------+
|                           name |              rev_sum |
+--------------------------------+----------------------+
|                           Jack |                   30 |
+--------------------------------+----------------------+

```

`+--------------------------------+----------------------+
|                           name |              rev_sum |
+--------------------------------+----------------------+
|                           Jack |                   30 |
+--------------------------------+----------------------+
`

The Row-based Operations are also supported in Python Table API, which include Map Operation,
FlatMap Operation, Aggregate Operation and FlatAggregate Operation.


The following example shows a simple row-based operation query:


```
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table import DataTypes
from pyflink.table.udf import udf
import pandas as pd

# using batch table environment to execute the queries
env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

orders = table_env.from_elements([('Jack', 'FRANCE', 10), ('Rose', 'ENGLAND', 30), ('Jack', 'FRANCE', 20)],
                                 ['name', 'country', 'revenue'])

map_function = udf(lambda x: pd.concat([x.name, x.revenue * 10], axis=1),
                   result_type=DataTypes.ROW(
                               [DataTypes.FIELD("name", DataTypes.STRING()),
                                DataTypes.FIELD("revenue", DataTypes.BIGINT())]),
                   func_type="pandas")

orders.map(map_function).execute().print()

```

`from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table import DataTypes
from pyflink.table.udf import udf
import pandas as pd

# using batch table environment to execute the queries
env_settings = EnvironmentSettings.in_batch_mode()
table_env = TableEnvironment.create(env_settings)

orders = table_env.from_elements([('Jack', 'FRANCE', 10), ('Rose', 'ENGLAND', 30), ('Jack', 'FRANCE', 20)],
                                 ['name', 'country', 'revenue'])

map_function = udf(lambda x: pd.concat([x.name, x.revenue * 10], axis=1),
                   result_type=DataTypes.ROW(
                               [DataTypes.FIELD("name", DataTypes.STRING()),
                                DataTypes.FIELD("revenue", DataTypes.BIGINT())]),
                   func_type="pandas")

orders.map(map_function).execute().print()
`

The results are as following:


```
+--------------------------------+----------------------+
|                           name |              revenue |
+--------------------------------+----------------------+
|                           Jack |                  100 |
|                           Rose |                  300 |
|                           Jack |                  200 |
+--------------------------------+----------------------+

```

`+--------------------------------+----------------------+
|                           name |              revenue |
+--------------------------------+----------------------+
|                           Jack |                  100 |
|                           Rose |                  300 |
|                           Jack |                  200 |
+--------------------------------+----------------------+
`

### Write SQL Queries#


Flink’s SQL integration is based on Apache Calcite, which implements the SQL standard. SQL queries are specified as Strings.


The SQL documentation describes Flink’s SQL support for streaming and batch tables.


The following example shows a simple SQL aggregation query:


```
from pyflink.table import EnvironmentSettings, TableEnvironment

# use a stream TableEnvironment to execute the queries
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)


table_env.execute_sql("""
    CREATE TABLE random_source (
        id BIGINT, 
        data TINYINT
    ) WITH (
        'connector' = 'datagen',
        'fields.id.kind'='sequence',
        'fields.id.start'='1',
        'fields.id.end'='8',
        'fields.data.kind'='sequence',
        'fields.data.start'='4',
        'fields.data.end'='11'
    )
""")

table_env.execute_sql("""
    CREATE TABLE print_sink (
        id BIGINT, 
        data_sum TINYINT 
    ) WITH (
        'connector' = 'print'
    )
""")

table_env.execute_sql("""
    INSERT INTO print_sink
        SELECT id, sum(data) as data_sum FROM 
            (SELECT id / 2 as id, data FROM random_source)
        WHERE id > 1
        GROUP BY id
""").wait()

```

`from pyflink.table import EnvironmentSettings, TableEnvironment

# use a stream TableEnvironment to execute the queries
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)


table_env.execute_sql("""
    CREATE TABLE random_source (
        id BIGINT, 
        data TINYINT
    ) WITH (
        'connector' = 'datagen',
        'fields.id.kind'='sequence',
        'fields.id.start'='1',
        'fields.id.end'='8',
        'fields.data.kind'='sequence',
        'fields.data.start'='4',
        'fields.data.end'='11'
    )
""")

table_env.execute_sql("""
    CREATE TABLE print_sink (
        id BIGINT, 
        data_sum TINYINT 
    ) WITH (
        'connector' = 'print'
    )
""")

table_env.execute_sql("""
    INSERT INTO print_sink
        SELECT id, sum(data) as data_sum FROM 
            (SELECT id / 2 as id, data FROM random_source)
        WHERE id > 1
        GROUP BY id
""").wait()
`

The results are as following:


```
2> +I(4,11)
6> +I(2,8)
8> +I(3,10)
6> -U(2,8)
8> -U(3,10)
6> +U(2,15)
8> +U(3,19)

```

`2> +I(4,11)
6> +I(2,8)
8> +I(3,10)
6> -U(2,8)
8> -U(3,10)
6> +U(2,15)
8> +U(3,19)
`

In fact, this shows the change logs received by the print sink.
The output format of a change log is:


```
{subtask id}> {message type}{string format of the value}

```

`{subtask id}> {message type}{string format of the value}
`

For example, “2> +I(4,11)” means this message comes from the 2nd subtask, and “+I” means it is an insert message. “(4, 11)” is the content of the message.
In addition, “-U” means a retract record (i.e. update-before), which means this message should be deleted or retracted from the sink.
“+U” means this is an update record (i.e. update-after), which means this message should be updated or inserted by the sink.


So, we get this result from the change logs above:


```
(4, 11)
(2, 15) 
(3, 19)

```

`(4, 11)
(2, 15) 
(3, 19)
`

### Mix the Table API and SQL#


The Table objects used in Table API and the tables used in SQL can be freely converted to each other.

`Table`

The following example shows how to use a Table object in SQL:

`Table`

```
# create a sink table to emit results
table_env.execute_sql("""
    CREATE TABLE table_sink (
        id BIGINT, 
        data VARCHAR 
    ) WITH (
        'connector' = 'print'
    )
""")

# convert the Table API table to a SQL view
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table_env.create_temporary_view('table_api_table', table)

# emit the Table API table
table_env.execute_sql("INSERT INTO table_sink SELECT * FROM table_api_table").wait()

```

`# create a sink table to emit results
table_env.execute_sql("""
    CREATE TABLE table_sink (
        id BIGINT, 
        data VARCHAR 
    ) WITH (
        'connector' = 'print'
    )
""")

# convert the Table API table to a SQL view
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table_env.create_temporary_view('table_api_table', table)

# emit the Table API table
table_env.execute_sql("INSERT INTO table_sink SELECT * FROM table_api_table").wait()
`

The results are as following:


```
6> +I(1,Hi)
6> +I(2,Hello)

```

`6> +I(1,Hi)
6> +I(2,Hello)
`

And the following example shows how to use SQL tables in the Table API:


```
# create a sql source table
table_env.execute_sql("""
    CREATE TABLE sql_source (
        id BIGINT, 
        data TINYINT 
    ) WITH (
        'connector' = 'datagen',
        'fields.id.kind'='sequence',
        'fields.id.start'='1',
        'fields.id.end'='4',
        'fields.data.kind'='sequence',
        'fields.data.start'='4',
        'fields.data.end'='7'
    )
""")

# convert the sql table to Table API table
table = table_env.from_path("sql_source")

# or create the table from a sql query
# table = table_env.sql_query("SELECT * FROM sql_source")

# emit the table
table.execute().print()

```

`# create a sql source table
table_env.execute_sql("""
    CREATE TABLE sql_source (
        id BIGINT, 
        data TINYINT 
    ) WITH (
        'connector' = 'datagen',
        'fields.id.kind'='sequence',
        'fields.id.start'='1',
        'fields.id.end'='4',
        'fields.data.kind'='sequence',
        'fields.data.start'='4',
        'fields.data.end'='7'
    )
""")

# convert the sql table to Table API table
table = table_env.from_path("sql_source")

# or create the table from a sql query
# table = table_env.sql_query("SELECT * FROM sql_source")

# emit the table
table.execute().print()
`

The results are as following:


```
+----+----------------------+--------+
| op |                   id |   data |
+----+----------------------+--------+
| +I |                    1 |      4 |
| +I |                    2 |      5 |
| +I |                    3 |      6 |
| +I |                    4 |      7 |
+----+----------------------+--------+

```

`+----+----------------------+--------+
| op |                   id |   data |
+----+----------------------+--------+
| +I |                    1 |      4 |
| +I |                    2 |      5 |
| +I |                    3 |      6 |
| +I |                    4 |      7 |
+----+----------------------+--------+
`

 Back to top


## Emit Results#


### Print the Table#


You can call the TableResult.print method to print the content of the Table to console.
This is usually used when you want to preview the table.

`TableResult.print`

```
# prepare source tables 
source = table_env.from_elements([(1, "Hi", "Hello"), (2, "Hello", "Hello")], ["a", "b", "c"])

# Get TableResult
table_result = table_env.execute_sql("select a + 1, b, c from %s" % source)

# Print the table
table_result.print()

```

`# prepare source tables 
source = table_env.from_elements([(1, "Hi", "Hello"), (2, "Hello", "Hello")], ["a", "b", "c"])

# Get TableResult
table_result = table_env.execute_sql("select a + 1, b, c from %s" % source)

# Print the table
table_result.print()
`

The results are as following:


```
+----+----------------------+--------------------------------+--------------------------------+
| op |               EXPR$0 |                              b |                              c |
+----+----------------------+--------------------------------+--------------------------------+
| +I |                    2 |                             Hi |                          Hello |
| +I |                    3 |                          Hello |                          Hello |
+----+----------------------+--------------------------------+--------------------------------+

```

`+----+----------------------+--------------------------------+--------------------------------+
| op |               EXPR$0 |                              b |                              c |
+----+----------------------+--------------------------------+--------------------------------+
| +I |                    2 |                             Hi |                          Hello |
| +I |                    3 |                          Hello |                          Hello |
+----+----------------------+--------------------------------+--------------------------------+
`

Note It will trigger the materialization of the table and collect table content to the memory of the client, it’s a good practice to limit the number of rows collected via 



    Table.limit

.


### Collect Results to Client#


You can call the TableResult.collect method to collect results of a table to client.
The type of the results is an auto closeable iterator.

`TableResult.collect`

The following code shows how to use the TableResult.collect() methodï¼

`TableResult.collect()`

```
# prepare source tables 
source = table_env.from_elements([(1, "Hi", "Hello"), (2, "Hello", "Hello")], ["a", "b", "c"])

# Get TableResult
table_result = table_env.execute_sql("select a + 1, b, c from %s" % source)

# Traversal result
with table_result.collect() as results:
   for result in results:
       print(result)

```

`# prepare source tables 
source = table_env.from_elements([(1, "Hi", "Hello"), (2, "Hello", "Hello")], ["a", "b", "c"])

# Get TableResult
table_result = table_env.execute_sql("select a + 1, b, c from %s" % source)

# Traversal result
with table_result.collect() as results:
   for result in results:
       print(result)
`

The results are as followingï¼


```
<Row(2, 'Hi', 'Hello')>
<Row(3, 'Hello', 'Hello')>

```

`<Row(2, 'Hi', 'Hello')>
<Row(3, 'Hello', 'Hello')>
`

Note It will trigger the materialization of the table and collect table content to the memory of the client, it’s a good practice to limit the number of rows collected via 



    Table.limit

.


### Collect Results to Client by converting it to pandas DataFrame#


You can call the “to_pandas” method to convert a Table object to a pandas DataFrame:

`Table`

```
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
print(table.to_pandas())

```

`table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
print(table.to_pandas())
`

The results are as following:


```
   id   data
0   1     Hi
1   2  Hello

```

`   id   data
0   1     Hi
1   2  Hello
`

Note It will trigger the materialization of the table and collect table content to the memory of the client, it’s a good practice to limit the number of rows collected via 



    Table.limit

.


Note Not all the data types are supported.


### Emit Results to One Sink Table#


You can call the “execute_insert” method to emit the data in a Table object to a sink table:

`Table`

```
table_env.execute_sql("""
    CREATE TABLE sink_table (
        id BIGINT, 
        data VARCHAR 
    ) WITH (
        'connector' = 'print'
    )
""")

table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table.execute_insert("sink_table").wait()

```

`table_env.execute_sql("""
    CREATE TABLE sink_table (
        id BIGINT, 
        data VARCHAR 
    ) WITH (
        'connector' = 'print'
    )
""")

table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table.execute_insert("sink_table").wait()
`

The results are as following:


```
6> +I(1,Hi)
6> +I(2,Hello)

```

`6> +I(1,Hi)
6> +I(2,Hello)
`

This could also be done using SQL:


```
table_env.create_temporary_view("table_source", table)
table_env.execute_sql("INSERT INTO sink_table SELECT * FROM table_source").wait()

```

`table_env.create_temporary_view("table_source", table)
table_env.execute_sql("INSERT INTO sink_table SELECT * FROM table_source").wait()
`

### Emit Results to Multiple Sink Tables#


You can use a StatementSet to emit the Tables to multiple sink tables in one job:

`StatementSet`
`Table`

```
# prepare source tables and sink tables
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table_env.create_temporary_view("simple_source", table)
table_env.execute_sql("""
    CREATE TABLE first_sink_table (
        id BIGINT, 
        data VARCHAR 
    ) WITH (
        'connector' = 'print'
    )
""")
table_env.execute_sql("""
    CREATE TABLE second_sink_table (
        id BIGINT, 
        data VARCHAR
    ) WITH (
        'connector' = 'print'
    )
""")

# create a statement set
statement_set = table_env.create_statement_set()

# emit the "table" object to the "first_sink_table"
statement_set.add_insert("first_sink_table", table)

# emit the "simple_source" to the "second_sink_table" via a insert sql query
statement_set.add_insert_sql("INSERT INTO second_sink_table SELECT * FROM simple_source")

# execute the statement set
statement_set.execute().wait()

```

`# prepare source tables and sink tables
table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table_env.create_temporary_view("simple_source", table)
table_env.execute_sql("""
    CREATE TABLE first_sink_table (
        id BIGINT, 
        data VARCHAR 
    ) WITH (
        'connector' = 'print'
    )
""")
table_env.execute_sql("""
    CREATE TABLE second_sink_table (
        id BIGINT, 
        data VARCHAR
    ) WITH (
        'connector' = 'print'
    )
""")

# create a statement set
statement_set = table_env.create_statement_set()

# emit the "table" object to the "first_sink_table"
statement_set.add_insert("first_sink_table", table)

# emit the "simple_source" to the "second_sink_table" via a insert sql query
statement_set.add_insert_sql("INSERT INTO second_sink_table SELECT * FROM simple_source")

# execute the statement set
statement_set.execute().wait()
`

The results are as following:


```
7> +I(1,Hi)
7> +I(1,Hi)
7> +I(2,Hello)
7> +I(2,Hello)

```

`7> +I(1,Hi)
7> +I(1,Hi)
7> +I(2,Hello)
7> +I(2,Hello)
`

## Explain Tables#


The Table API provides a mechanism to explain the logical and optimized query plans used to compute a Table.
This is done through the Table.explain() or StatementSet.explain() methods. Table.explain() returns the plan of a Table.
StatementSet.explain() is used to get the plan for a job which contains multiple sinks. These methods return a string describing three things:

`Table`
`Table.explain()`
`StatementSet.explain()`
`Table.explain()`
`Table`
`StatementSet.explain()`
1. the Abstract Syntax Tree of the relational query, i.e., the unoptimized logical query plan,
2. the optimized logical query plan, and
3. the physical execution plan.

TableEnvironment.explain_sql() and TableEnvironment.execute_sql() support executing an EXPLAIN statement to get the plans. Please refer to the EXPLAIN page for more details.

`TableEnvironment.explain_sql()`
`TableEnvironment.execute_sql()`
`EXPLAIN`

The following code shows how to use the Table.explain() method:

`Table.explain()`

```
# using a stream TableEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col

env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table1 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table2 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table = table1 \
    .where(col("data").like('H%')) \
    .union_all(table2)
print(table.explain())

```

`# using a stream TableEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col

env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table1 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table2 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table = table1 \
    .where(col("data").like('H%')) \
    .union_all(table2)
print(table.explain())
`

The results are as following:


```
== Abstract Syntax Tree ==
LogicalUnion(all=[true])
:- LogicalFilter(condition=[LIKE($1, _UTF-16LE'H%')])
:  +- LogicalTableScan(table=[[default_catalog, default_database, Unregistered_TableSource_201907291, source: [PythonInputFormatTableSource(id, data)]]])
+- LogicalTableScan(table=[[default_catalog, default_database, Unregistered_TableSource_1709623525, source: [PythonInputFormatTableSource(id, data)]]])

== Optimized Logical Plan ==
Union(all=[true], union=[id, data])
:- Calc(select=[id, data], where=[LIKE(data, _UTF-16LE'H%')])
:  +- LegacyTableSourceScan(table=[[default_catalog, default_database, Unregistered_TableSource_201907291, source: [PythonInputFormatTableSource(id, data)]]], fields=[id, data])
+- LegacyTableSourceScan(table=[[default_catalog, default_database, Unregistered_TableSource_1709623525, source: [PythonInputFormatTableSource(id, data)]]], fields=[id, data])

== Physical Execution Plan ==
Stage 133 : Data Source
        content : Source: PythonInputFormatTableSource(id, data)

        Stage 134 : Operator
                content : SourceConversion(table=[default_catalog.default_database.Unregistered_TableSource_201907291, source: [PythonInputFormatTableSource(id, data)]], fields=[id, data])
                ship_strategy : FORWARD

                Stage 135 : Operator
                        content : Calc(select=[id, data], where=[(data LIKE _UTF-16LE'H%')])
                        ship_strategy : FORWARD

Stage 136 : Data Source
        content : Source: PythonInputFormatTableSource(id, data)

        Stage 137 : Operator
                content : SourceConversion(table=[default_catalog.default_database.Unregistered_TableSource_1709623525, source: [PythonInputFormatTableSource(id, data)]], fields=[id, data])
                ship_strategy : FORWARD

```

`== Abstract Syntax Tree ==
LogicalUnion(all=[true])
:- LogicalFilter(condition=[LIKE($1, _UTF-16LE'H%')])
:  +- LogicalTableScan(table=[[default_catalog, default_database, Unregistered_TableSource_201907291, source: [PythonInputFormatTableSource(id, data)]]])
+- LogicalTableScan(table=[[default_catalog, default_database, Unregistered_TableSource_1709623525, source: [PythonInputFormatTableSource(id, data)]]])

== Optimized Logical Plan ==
Union(all=[true], union=[id, data])
:- Calc(select=[id, data], where=[LIKE(data, _UTF-16LE'H%')])
:  +- LegacyTableSourceScan(table=[[default_catalog, default_database, Unregistered_TableSource_201907291, source: [PythonInputFormatTableSource(id, data)]]], fields=[id, data])
+- LegacyTableSourceScan(table=[[default_catalog, default_database, Unregistered_TableSource_1709623525, source: [PythonInputFormatTableSource(id, data)]]], fields=[id, data])

== Physical Execution Plan ==
Stage 133 : Data Source
        content : Source: PythonInputFormatTableSource(id, data)

        Stage 134 : Operator
                content : SourceConversion(table=[default_catalog.default_database.Unregistered_TableSource_201907291, source: [PythonInputFormatTableSource(id, data)]], fields=[id, data])
                ship_strategy : FORWARD

                Stage 135 : Operator
                        content : Calc(select=[id, data], where=[(data LIKE _UTF-16LE'H%')])
                        ship_strategy : FORWARD

Stage 136 : Data Source
        content : Source: PythonInputFormatTableSource(id, data)

        Stage 137 : Operator
                content : SourceConversion(table=[default_catalog.default_database.Unregistered_TableSource_1709623525, source: [PythonInputFormatTableSource(id, data)]], fields=[id, data])
                ship_strategy : FORWARD
`

The following code shows how to use the StatementSet.explain() method:

`StatementSet.explain()`

```
# using a stream TableEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col

env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table1 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table2 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table_env.execute_sql("""
    CREATE TABLE print_sink_table (
        id BIGINT, 
        data VARCHAR 
    ) WITH (
        'connector' = 'print'
    )
""")
table_env.execute_sql("""
    CREATE TABLE black_hole_sink_table (
        id BIGINT, 
        data VARCHAR 
    ) WITH (
        'connector' = 'blackhole'
    )
""")

statement_set = table_env.create_statement_set()

statement_set.add_insert("print_sink_table", table1.where(col("data").like('H%')))
statement_set.add_insert("black_hole_sink_table", table2)

print(statement_set.explain())

```

`# using a stream TableEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col

env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table1 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table2 = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table_env.execute_sql("""
    CREATE TABLE print_sink_table (
        id BIGINT, 
        data VARCHAR 
    ) WITH (
        'connector' = 'print'
    )
""")
table_env.execute_sql("""
    CREATE TABLE black_hole_sink_table (
        id BIGINT, 
        data VARCHAR 
    ) WITH (
        'connector' = 'blackhole'
    )
""")

statement_set = table_env.create_statement_set()

statement_set.add_insert("print_sink_table", table1.where(col("data").like('H%')))
statement_set.add_insert("black_hole_sink_table", table2)

print(statement_set.explain())
`

The results are as following:


```
== Abstract Syntax Tree ==
LogicalSink(table=[default_catalog.default_database.print_sink_table], fields=[id, data])
+- LogicalFilter(condition=[LIKE($1, _UTF-16LE'H%')])
   +- LogicalTableScan(table=[[default_catalog, default_database, Unregistered_TableSource_541737614, source: [PythonInputFormatTableSource(id, data)]]])

LogicalSink(table=[default_catalog.default_database.black_hole_sink_table], fields=[id, data])
+- LogicalTableScan(table=[[default_catalog, default_database, Unregistered_TableSource_1437429083, source: [PythonInputFormatTableSource(id, data)]]])

== Optimized Logical Plan ==
Sink(table=[default_catalog.default_database.print_sink_table], fields=[id, data])
+- Calc(select=[id, data], where=[LIKE(data, _UTF-16LE'H%')])
   +- LegacyTableSourceScan(table=[[default_catalog, default_database, Unregistered_TableSource_541737614, source: [PythonInputFormatTableSource(id, data)]]], fields=[id, data])

Sink(table=[default_catalog.default_database.black_hole_sink_table], fields=[id, data])
+- LegacyTableSourceScan(table=[[default_catalog, default_database, Unregistered_TableSource_1437429083, source: [PythonInputFormatTableSource(id, data)]]], fields=[id, data])

== Physical Execution Plan ==
Stage 139 : Data Source
        content : Source: PythonInputFormatTableSource(id, data)

        Stage 140 : Operator
                content : SourceConversion(table=[default_catalog.default_database.Unregistered_TableSource_541737614, source: [PythonInputFormatTableSource(id, data)]], fields=[id, data])
                ship_strategy : FORWARD

                Stage 141 : Operator
                        content : Calc(select=[id, data], where=[(data LIKE _UTF-16LE'H%')])
                        ship_strategy : FORWARD

Stage 143 : Data Source
        content : Source: PythonInputFormatTableSource(id, data)

        Stage 144 : Operator
                content : SourceConversion(table=[default_catalog.default_database.Unregistered_TableSource_1437429083, source: [PythonInputFormatTableSource(id, data)]], fields=[id, data])
                ship_strategy : FORWARD

                Stage 142 : Data Sink
                        content : Sink: Sink(table=[default_catalog.default_database.print_sink_table], fields=[id, data])
                        ship_strategy : FORWARD

                        Stage 145 : Data Sink
                                content : Sink: Sink(table=[default_catalog.default_database.black_hole_sink_table], fields=[id, data])
                                ship_strategy : FORWARD

```

`== Abstract Syntax Tree ==
LogicalSink(table=[default_catalog.default_database.print_sink_table], fields=[id, data])
+- LogicalFilter(condition=[LIKE($1, _UTF-16LE'H%')])
   +- LogicalTableScan(table=[[default_catalog, default_database, Unregistered_TableSource_541737614, source: [PythonInputFormatTableSource(id, data)]]])

LogicalSink(table=[default_catalog.default_database.black_hole_sink_table], fields=[id, data])
+- LogicalTableScan(table=[[default_catalog, default_database, Unregistered_TableSource_1437429083, source: [PythonInputFormatTableSource(id, data)]]])

== Optimized Logical Plan ==
Sink(table=[default_catalog.default_database.print_sink_table], fields=[id, data])
+- Calc(select=[id, data], where=[LIKE(data, _UTF-16LE'H%')])
   +- LegacyTableSourceScan(table=[[default_catalog, default_database, Unregistered_TableSource_541737614, source: [PythonInputFormatTableSource(id, data)]]], fields=[id, data])

Sink(table=[default_catalog.default_database.black_hole_sink_table], fields=[id, data])
+- LegacyTableSourceScan(table=[[default_catalog, default_database, Unregistered_TableSource_1437429083, source: [PythonInputFormatTableSource(id, data)]]], fields=[id, data])

== Physical Execution Plan ==
Stage 139 : Data Source
        content : Source: PythonInputFormatTableSource(id, data)

        Stage 140 : Operator
                content : SourceConversion(table=[default_catalog.default_database.Unregistered_TableSource_541737614, source: [PythonInputFormatTableSource(id, data)]], fields=[id, data])
                ship_strategy : FORWARD

                Stage 141 : Operator
                        content : Calc(select=[id, data], where=[(data LIKE _UTF-16LE'H%')])
                        ship_strategy : FORWARD

Stage 143 : Data Source
        content : Source: PythonInputFormatTableSource(id, data)

        Stage 144 : Operator
                content : SourceConversion(table=[default_catalog.default_database.Unregistered_TableSource_1437429083, source: [PythonInputFormatTableSource(id, data)]], fields=[id, data])
                ship_strategy : FORWARD

                Stage 142 : Data Sink
                        content : Sink: Sink(table=[default_catalog.default_database.print_sink_table], fields=[id, data])
                        ship_strategy : FORWARD

                        Stage 145 : Data Sink
                                content : Sink: Sink(table=[default_catalog.default_database.black_hole_sink_table], fields=[id, data])
                                ship_strategy : FORWARD
`