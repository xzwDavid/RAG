# Connectors


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Connectors#


This page describes how to use connectors in PyFlink and highlights the details to be aware of when
using Flink connectors in Python programs.


Note For general connector information and common
configuration, please refer to the corresponding Java/Scala documentation.


## Download connector and format jars#


Since Flink is a Java/Scala-based project, for both connectors and formats, implementations
are available as jars that need to be specified as job dependencies.


```
table_env.get_config().set("pipeline.jars", "file:///my/jar/path/connector.jar;file:///my/jar/path/json.jar")

```

`table_env.get_config().set("pipeline.jars", "file:///my/jar/path/connector.jar;file:///my/jar/path/json.jar")
`

## How to use connectors#


In PyFlink’s Table API, DDL is the recommended way to define sources and sinks, executed via the
execute_sql() method on the TableEnvironment.
This makes the table available for use by the application.

`execute_sql()`
`TableEnvironment`

```
source_ddl = """
        CREATE TABLE source_table(
            a VARCHAR,
            b INT
        ) WITH (
          'connector' = 'kafka',
          'topic' = 'source_topic',
          'properties.bootstrap.servers' = 'kafka:9092',
          'properties.group.id' = 'test_3',
          'scan.startup.mode' = 'latest-offset',
          'format' = 'json'
        )
        """

sink_ddl = """
        CREATE TABLE sink_table(
            a VARCHAR
        ) WITH (
          'connector' = 'kafka',
          'topic' = 'sink_topic',
          'properties.bootstrap.servers' = 'kafka:9092',
          'format' = 'json'
        )
        """

t_env.execute_sql(source_ddl)
t_env.execute_sql(sink_ddl)

t_env.sql_query("SELECT a FROM source_table") \
    .execute_insert("sink_table").wait()

```

`source_ddl = """
        CREATE TABLE source_table(
            a VARCHAR,
            b INT
        ) WITH (
          'connector' = 'kafka',
          'topic' = 'source_topic',
          'properties.bootstrap.servers' = 'kafka:9092',
          'properties.group.id' = 'test_3',
          'scan.startup.mode' = 'latest-offset',
          'format' = 'json'
        )
        """

sink_ddl = """
        CREATE TABLE sink_table(
            a VARCHAR
        ) WITH (
          'connector' = 'kafka',
          'topic' = 'sink_topic',
          'properties.bootstrap.servers' = 'kafka:9092',
          'format' = 'json'
        )
        """

t_env.execute_sql(source_ddl)
t_env.execute_sql(sink_ddl)

t_env.sql_query("SELECT a FROM source_table") \
    .execute_insert("sink_table").wait()
`

Below is a complete example of how to use a Kafka source/sink and the JSON format in PyFlink.


```
from pyflink.table import TableEnvironment, EnvironmentSettings

def log_processing():
    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(env_settings)
    # specify connector and format jars
    t_env.get_config().set("pipeline.jars", "file:///my/jar/path/connector.jar;file:///my/jar/path/json.jar")
    
    source_ddl = """
            CREATE TABLE source_table(
                a VARCHAR,
                b INT
            ) WITH (
              'connector' = 'kafka',
              'topic' = 'source_topic',
              'properties.bootstrap.servers' = 'kafka:9092',
              'properties.group.id' = 'test_3',
              'scan.startup.mode' = 'latest-offset',
              'format' = 'json'
            )
            """

    sink_ddl = """
            CREATE TABLE sink_table(
                a VARCHAR
            ) WITH (
              'connector' = 'kafka',
              'topic' = 'sink_topic',
              'properties.bootstrap.servers' = 'kafka:9092',
              'format' = 'json'
            )
            """

    t_env.execute_sql(source_ddl)
    t_env.execute_sql(sink_ddl)

    t_env.sql_query("SELECT a FROM source_table") \
        .execute_insert("sink_table").wait()


if __name__ == '__main__':
    log_processing()

```

`from pyflink.table import TableEnvironment, EnvironmentSettings

def log_processing():
    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(env_settings)
    # specify connector and format jars
    t_env.get_config().set("pipeline.jars", "file:///my/jar/path/connector.jar;file:///my/jar/path/json.jar")
    
    source_ddl = """
            CREATE TABLE source_table(
                a VARCHAR,
                b INT
            ) WITH (
              'connector' = 'kafka',
              'topic' = 'source_topic',
              'properties.bootstrap.servers' = 'kafka:9092',
              'properties.group.id' = 'test_3',
              'scan.startup.mode' = 'latest-offset',
              'format' = 'json'
            )
            """

    sink_ddl = """
            CREATE TABLE sink_table(
                a VARCHAR
            ) WITH (
              'connector' = 'kafka',
              'topic' = 'sink_topic',
              'properties.bootstrap.servers' = 'kafka:9092',
              'format' = 'json'
            )
            """

    t_env.execute_sql(source_ddl)
    t_env.execute_sql(sink_ddl)

    t_env.sql_query("SELECT a FROM source_table") \
        .execute_insert("sink_table").wait()


if __name__ == '__main__':
    log_processing()
`

## Predefined Sources and Sinks#


Some data sources and sinks are built into Flink and are available out-of-the-box.
These predefined data sources include reading from Pandas DataFrame, or ingesting data from collections.
The predefined data sinks support writing to Pandas DataFrame.


### from/to Pandas#


PyFlink Tables support conversion to and from Pandas DataFrame.


```
from pyflink.table.expressions import col

import pandas as pd
import numpy as np

# Create a PyFlink Table
pdf = pd.DataFrame(np.random.rand(1000, 2))
table = t_env.from_pandas(pdf, ["a", "b"]).filter(col('a') > 0.5)

# Convert the PyFlink Table to a Pandas DataFrame
pdf = table.to_pandas()

```

`from pyflink.table.expressions import col

import pandas as pd
import numpy as np

# Create a PyFlink Table
pdf = pd.DataFrame(np.random.rand(1000, 2))
table = t_env.from_pandas(pdf, ["a", "b"]).filter(col('a') > 0.5)

# Convert the PyFlink Table to a Pandas DataFrame
pdf = table.to_pandas()
`

### from_elements()#


from_elements() is used to create a table from a collection of elements. The element types must
be acceptable atomic types or acceptable composite types.

`from_elements()`

```
from pyflink.table import DataTypes

table_env.from_elements([(1, 'Hi'), (2, 'Hello')])

# use the second parameter to specify custom field names
table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['a', 'b'])

# use the second parameter to specify a custom table schema
table_env.from_elements([(1, 'Hi'), (2, 'Hello')],
                        DataTypes.ROW([DataTypes.FIELD("a", DataTypes.INT()),
                                       DataTypes.FIELD("b", DataTypes.STRING())]))

```

`from pyflink.table import DataTypes

table_env.from_elements([(1, 'Hi'), (2, 'Hello')])

# use the second parameter to specify custom field names
table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['a', 'b'])

# use the second parameter to specify a custom table schema
table_env.from_elements([(1, 'Hi'), (2, 'Hello')],
                        DataTypes.ROW([DataTypes.FIELD("a", DataTypes.INT()),
                                       DataTypes.FIELD("b", DataTypes.STRING())]))
`

The above query returns a Table like:


```
+----+-------+
| a  |   b   |
+====+=======+
| 1  |  Hi   |
+----+-------+
| 2  | Hello |
+----+-------+

```

`+----+-------+
| a  |   b   |
+====+=======+
| 1  |  Hi   |
+----+-------+
| 2  | Hello |
+----+-------+
`

## User-defined sources & sinks#


In some cases, you may want to define custom sources and sinks. Currently, sources and sinks must
be implemented in Java/Scala, but you can define a TableFactory to support their use via DDL.
More details can be found in the Java/Scala documentation.

`TableFactory`