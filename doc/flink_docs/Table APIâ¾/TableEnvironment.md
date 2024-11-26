# TableEnvironment


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# TableEnvironment#


This document is an introduction of PyFlink TableEnvironment.
It includes detailed descriptions of every public interface of the TableEnvironment class.

`TableEnvironment`
`TableEnvironment`

## Create a TableEnvironment#


The recommended way to create a TableEnvironment is to create from an EnvironmentSettings object:

`TableEnvironment`
`EnvironmentSettings`

```
from pyflink.common import Configuration
from pyflink.table import EnvironmentSettings, TableEnvironment

# create a streaming TableEnvironment
config = Configuration()
config.set_string('execution.buffer-timeout', '1 min')
env_settings = EnvironmentSettings \
    .new_instance() \
    .in_streaming_mode() \
    .with_configuration(config) \
    .build()

table_env = TableEnvironment.create(env_settings)

```

`from pyflink.common import Configuration
from pyflink.table import EnvironmentSettings, TableEnvironment

# create a streaming TableEnvironment
config = Configuration()
config.set_string('execution.buffer-timeout', '1 min')
env_settings = EnvironmentSettings \
    .new_instance() \
    .in_streaming_mode() \
    .with_configuration(config) \
    .build()

table_env = TableEnvironment.create(env_settings)
`

Alternatively, users can create a StreamTableEnvironment from an existing StreamExecutionEnvironment to interoperate with the DataStream API.

`StreamTableEnvironment`
`StreamExecutionEnvironment`

```
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

# create a streaming TableEnvironment from a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()
table_env = StreamTableEnvironment.create(env)

```

`from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

# create a streaming TableEnvironment from a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()
table_env = StreamTableEnvironment.create(env)
`

## TableEnvironment API#


### Table/SQL Operations#


These APIs are used to create/remove Table API/SQL Tables and write queries:


Deprecated APIs


### Execute/Explain Jobs#


These APIs are used to explain/execute jobs. Note that the API execute_sql can also be used to execute jobs.

`execute_sql`

Deprecated APIs


### Create/Drop User Defined Functions#


These APIs are used to register UDFs or remove the registered UDFs.
Note that the API execute_sql can also be used to register/remove UDFs.
For more details about the different kinds of UDFs, please refer to User Defined Functions.

`execute_sql`

### Dependency Management#


These APIs are used to manage the Python dependencies which are required by the Python UDFs.
Please refer to the Dependency Management documentation for more details.


### Configuration#


### Catalog APIs#


These APIs are used to access catalogs and modules. You can find more detailed introduction in Modules and Catalogs documentation.


## Statebackend, Checkpoint and Restart Strategy#


Before Flink 1.10 you can configure the statebackend, checkpointing and restart strategy via the StreamExecutionEnvironment.
And now you can configure them by setting key-value options in TableConfig, see Fault Tolerance, State Backends and Checkpointing for more details.

`StreamExecutionEnvironment`
`TableConfig`

The following code is an example showing how to configure the statebackend, checkpoint and restart strategy through the Table API:


```
# set the restart strategy to "fixed-delay"
table_env.get_config().set("restart-strategy.type", "fixed-delay")
table_env.get_config().set("restart-strategy.fixed-delay.attempts", "3")
table_env.get_config().set("restart-strategy.fixed-delay.delay", "30s")

# set the checkpoint mode to EXACTLY_ONCE
table_env.get_config().set("execution.checkpointing.mode", "EXACTLY_ONCE")
table_env.get_config().set("execution.checkpointing.interval", "3min")

# set the statebackend type to "rocksdb", other available options are "hashmap"
# you can also set the full qualified Java class name of the StateBackendFactory to this option
# e.g. org.apache.flink.state.rocksdb.EmbeddedRocksDBStateBackendFactory
table_env.get_config().set("state.backend.type", "rocksdb")

# set the checkpoint directory, which is required by the RocksDB statebackend
table_env.get_config().set("execution.checkpointing.dir", "file:///tmp/checkpoints/")

```

`# set the restart strategy to "fixed-delay"
table_env.get_config().set("restart-strategy.type", "fixed-delay")
table_env.get_config().set("restart-strategy.fixed-delay.attempts", "3")
table_env.get_config().set("restart-strategy.fixed-delay.delay", "30s")

# set the checkpoint mode to EXACTLY_ONCE
table_env.get_config().set("execution.checkpointing.mode", "EXACTLY_ONCE")
table_env.get_config().set("execution.checkpointing.interval", "3min")

# set the statebackend type to "rocksdb", other available options are "hashmap"
# you can also set the full qualified Java class name of the StateBackendFactory to this option
# e.g. org.apache.flink.state.rocksdb.EmbeddedRocksDBStateBackendFactory
table_env.get_config().set("state.backend.type", "rocksdb")

# set the checkpoint directory, which is required by the RocksDB statebackend
table_env.get_config().set("execution.checkpointing.dir", "file:///tmp/checkpoints/")
`