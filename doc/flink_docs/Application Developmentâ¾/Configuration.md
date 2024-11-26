# Configuration


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Configuration#


Depending on the requirements of a Python API program, it might be necessary to adjust certain parameters for optimization.


For Python DataStream API program, the config options could be set as following:


```
from pyflink.common import Configuration
from pyflink.datastream import StreamExecutionEnvironment

config = Configuration()
config.set_integer("python.fn-execution.bundle.size", 1000)
env = StreamExecutionEnvironment.get_execution_environment(config)

```

`from pyflink.common import Configuration
from pyflink.datastream import StreamExecutionEnvironment

config = Configuration()
config.set_integer("python.fn-execution.bundle.size", 1000)
env = StreamExecutionEnvironment.get_execution_environment(config)
`

For Python Table API program, all the config options available for Java/Scala Table API
program could also be used in the Python Table API program.
You could refer to the Table API Configuration for more details
on all the available config options for Table API programs.
The config options could be set as following in a Table API program:


```
from pyflink.table import TableEnvironment, EnvironmentSettings

env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)
t_env.get_config().set("python.fn-execution.bundle.size", "1000")

```

`from pyflink.table import TableEnvironment, EnvironmentSettings

env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)
t_env.get_config().set("python.fn-execution.bundle.size", "1000")
`

The config options could also be set when creating EnvironmentSettings:


```
from pyflink.common import Configuration
from pyflink.table import TableEnvironment, EnvironmentSettings

# create a streaming TableEnvironment
config = Configuration()
config.set_string("python.fn-execution.bundle.size", "1000")
env_settings = EnvironmentSettings \
    .new_instance() \
    .in_streaming_mode() \
    .with_configuration(config) \
    .build()
table_env = TableEnvironment.create(env_settings)

# or directly pass config into create method
table_env = TableEnvironment.create(config)

```

`from pyflink.common import Configuration
from pyflink.table import TableEnvironment, EnvironmentSettings

# create a streaming TableEnvironment
config = Configuration()
config.set_string("python.fn-execution.bundle.size", "1000")
env_settings = EnvironmentSettings \
    .new_instance() \
    .in_streaming_mode() \
    .with_configuration(config) \
    .build()
table_env = TableEnvironment.create(env_settings)

# or directly pass config into create method
table_env = TableEnvironment.create(config)
`

## Python Options#


##### python.archives


##### python.client.executable


##### python.executable


##### python.execution-mode


##### python.files


##### python.fn-execution.arrow.batch.size


##### python.fn-execution.bundle.size


##### python.fn-execution.bundle.time


##### python.fn-execution.memory.managed


##### python.map-state.iterate-response-batch-size


##### python.map-state.read-cache-size


##### python.map-state.write-cache-size


##### python.metric.enabled


##### python.operator-chaining.enabled


##### python.profile.enabled


##### python.pythonpath


##### python.requirements


##### python.state.cache-size


##### python.systemenv.enabled
