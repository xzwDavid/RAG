# State Backends


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# State Backends#


Flink provides different state backends that specify how and where state is stored.


State can be located on Javaâs heap or off-heap. Depending on your state backend, Flink can also manage the state for the application, meaning Flink deals with the memory management (possibly spilling to disk if necessary) to allow applications to hold very large state. By default, the Flink configuration file determines the state backend for all Flink jobs.


However, the default state backend can be overridden on a per-job basis, as shown below.


For more information about the available state backends, their advantages, limitations, and configuration parameters see the corresponding section in Deployment & Operations.


```
Configuration config = new Configuration();
config.set(StateBackendOptions.STATE_BACKEND, "hashmap");
env.configure(config);

```

`Configuration config = new Configuration();
config.set(StateBackendOptions.STATE_BACKEND, "hashmap");
env.configure(config);
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setStateBackend(...)

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setStateBackend(...)
`

```
config = Configuration()
config.set_string('state.backend.type', 'hashmap')
env = StreamExecutionEnvironment.get_execution_environment(config)

```

`config = Configuration()
config.set_string('state.backend.type', 'hashmap')
env = StreamExecutionEnvironment.get_execution_environment(config)
`

 Back to top
