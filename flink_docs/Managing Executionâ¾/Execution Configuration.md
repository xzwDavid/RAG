# Execution Configuration


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Execution Configuration#


The StreamExecutionEnvironment contains the ExecutionConfig which allows to set job specific configuration values for the runtime.
To change the defaults that affect all jobs, see Configuration.

`StreamExecutionEnvironment`
`ExecutionConfig`

```
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
ExecutionConfig executionConfig = env.getConfig();

```

`StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
ExecutionConfig executionConfig = env.getConfig();
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment
var executionConfig = env.getConfig

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment
var executionConfig = env.getConfig
`

```
env = StreamExecutionEnvironment.get_execution_environment()
execution_config = env.get_config()

```

`env = StreamExecutionEnvironment.get_execution_environment()
execution_config = env.get_config()
`

The following configuration options are available: (the default is bold)

* 
setClosureCleanerLevel(). The closure cleaner level is set to ClosureCleanerLevel.RECURSIVE by default. The closure cleaner removes unneeded references to the surrounding class of anonymous functions inside Flink programs.
With the closure cleaner disabled, it might happen that an anonymous user function is referencing the surrounding class, which is usually not Serializable. This will lead to exceptions by the serializer. The settings are:
NONE: disable the closure cleaner completely, TOP_LEVEL: clean only the top-level class without recursing into fields, RECURSIVE: clean all the fields recursively.

* 
getParallelism() / setParallelism(int parallelism) Set the default parallelism for the job.

* 
getMaxParallelism() / setMaxParallelism(int parallelism) Set the default maximum parallelism for the job. This setting determines the maximum degree of parallelism and specifies the upper limit for dynamic scaling.

* 
getNumberOfExecutionRetries() / setNumberOfExecutionRetries(int numberOfExecutionRetries) Sets the number of times that failed tasks are re-executed. A value of zero effectively disables fault tolerance. A value of -1 indicates that the system default value (as defined in the configuration) should be used. This is deprecated, use restart strategies instead.

* 
getExecutionRetryDelay() / setExecutionRetryDelay(long executionRetryDelay) Sets the delay in milliseconds that the system waits after a job has failed, before re-executing it. The delay starts after all tasks have been successfully stopped on the TaskManagers, and once the delay is past, the tasks are re-started. This parameter is useful to delay re-execution in order to let certain time-out related failures surface fully (like broken connections that have not fully timed out), before attempting a re-execution and immediately failing again due to the same problem. This parameter only has an effect if the number of execution re-tries is one or more. This is deprecated, use restart strategies instead.

* 
getExecutionMode() / setExecutionMode(). The default execution mode is PIPELINED. Sets the execution mode to execute the program. The execution mode defines whether data exchanges are performed in a batch or on a pipelined manner.

* 
enableForceKryo() / disableForceKryo. Kryo is not forced by default. Forces the GenericTypeInformation to use the Kryo serializer for POJOs even though we could analyze them as a POJO. In some cases this might be preferable. For example, when Flink’s internal serializers fail to handle a POJO properly.

* 
enableForceAvro() / disableForceAvro(). Avro is not forced by default. Forces the Flink AvroTypeInfo to use the Avro serializer instead of Kryo for serializing Avro POJOs.

* 
enableObjectReuse() / disableObjectReuse() By default, objects are not reused in Flink. Enabling the object reuse mode will instruct the runtime to reuse user objects for better performance. Keep in mind that this can lead to bugs when the user-code function of an operation is not aware of this behavior.

* 
getGlobalJobParameters() / setGlobalJobParameters() This method allows users to set custom objects as a global configuration for the job. Since the ExecutionConfig is accessible in all user defined functions, this is an easy method for making configuration globally available in a job.

* 
addDefaultKryoSerializer(Class<?> type, Serializer<?> serializer) Register a Kryo serializer instance for the given type.

* 
addDefaultKryoSerializer(Class<?> type, Class<? extends Serializer<?>> serializerClass) Register a Kryo serializer class for the given type.

* 
registerTypeWithKryoSerializer(Class<?> type, Serializer<?> serializer) Register the given type with Kryo and specify a serializer for it. By registering a type with Kryo, the serialization of the type will be much more efficient.

* 
registerKryoType(Class<?> type) If the type ends up being serialized with Kryo, then it will be registered at Kryo to make sure that only tags (integer IDs) are written. If a type is not registered with Kryo, its entire class-name will be serialized with every instance, leading to much higher I/O costs.

* 
registerPojoType(Class<?> type) Registers the given type with the serialization stack. If the type is eventually serialized as a POJO, then the type is registered with the POJO serializer. If the type ends up being serialized with Kryo, then it will be registered at Kryo to make sure that only tags are written. If a type is not registered with Kryo, its entire class-name will be serialized with every instance, leading to much higher I/O costs.


setClosureCleanerLevel(). The closure cleaner level is set to ClosureCleanerLevel.RECURSIVE by default. The closure cleaner removes unneeded references to the surrounding class of anonymous functions inside Flink programs.
With the closure cleaner disabled, it might happen that an anonymous user function is referencing the surrounding class, which is usually not Serializable. This will lead to exceptions by the serializer. The settings are:
NONE: disable the closure cleaner completely, TOP_LEVEL: clean only the top-level class without recursing into fields, RECURSIVE: clean all the fields recursively.

`setClosureCleanerLevel()`
`ClosureCleanerLevel.RECURSIVE`
`NONE`
`TOP_LEVEL`
`RECURSIVE`

getParallelism() / setParallelism(int parallelism) Set the default parallelism for the job.

`getParallelism()`
`setParallelism(int parallelism)`

getMaxParallelism() / setMaxParallelism(int parallelism) Set the default maximum parallelism for the job. This setting determines the maximum degree of parallelism and specifies the upper limit for dynamic scaling.

`getMaxParallelism()`
`setMaxParallelism(int parallelism)`

getNumberOfExecutionRetries() / setNumberOfExecutionRetries(int numberOfExecutionRetries) Sets the number of times that failed tasks are re-executed. A value of zero effectively disables fault tolerance. A value of -1 indicates that the system default value (as defined in the configuration) should be used. This is deprecated, use restart strategies instead.

`getNumberOfExecutionRetries()`
`setNumberOfExecutionRetries(int numberOfExecutionRetries)`
`-1`

getExecutionRetryDelay() / setExecutionRetryDelay(long executionRetryDelay) Sets the delay in milliseconds that the system waits after a job has failed, before re-executing it. The delay starts after all tasks have been successfully stopped on the TaskManagers, and once the delay is past, the tasks are re-started. This parameter is useful to delay re-execution in order to let certain time-out related failures surface fully (like broken connections that have not fully timed out), before attempting a re-execution and immediately failing again due to the same problem. This parameter only has an effect if the number of execution re-tries is one or more. This is deprecated, use restart strategies instead.

`getExecutionRetryDelay()`
`setExecutionRetryDelay(long executionRetryDelay)`

getExecutionMode() / setExecutionMode(). The default execution mode is PIPELINED. Sets the execution mode to execute the program. The execution mode defines whether data exchanges are performed in a batch or on a pipelined manner.

`getExecutionMode()`
`setExecutionMode()`

enableForceKryo() / disableForceKryo. Kryo is not forced by default. Forces the GenericTypeInformation to use the Kryo serializer for POJOs even though we could analyze them as a POJO. In some cases this might be preferable. For example, when Flink’s internal serializers fail to handle a POJO properly.

`enableForceKryo()`
`disableForceKryo`

enableForceAvro() / disableForceAvro(). Avro is not forced by default. Forces the Flink AvroTypeInfo to use the Avro serializer instead of Kryo for serializing Avro POJOs.

`enableForceAvro()`
`disableForceAvro()`

enableObjectReuse() / disableObjectReuse() By default, objects are not reused in Flink. Enabling the object reuse mode will instruct the runtime to reuse user objects for better performance. Keep in mind that this can lead to bugs when the user-code function of an operation is not aware of this behavior.

`enableObjectReuse()`
`disableObjectReuse()`

getGlobalJobParameters() / setGlobalJobParameters() This method allows users to set custom objects as a global configuration for the job. Since the ExecutionConfig is accessible in all user defined functions, this is an easy method for making configuration globally available in a job.

`getGlobalJobParameters()`
`setGlobalJobParameters()`
`ExecutionConfig`

addDefaultKryoSerializer(Class<?> type, Serializer<?> serializer) Register a Kryo serializer instance for the given type.

`addDefaultKryoSerializer(Class<?> type, Serializer<?> serializer)`
`type`

addDefaultKryoSerializer(Class<?> type, Class<? extends Serializer<?>> serializerClass) Register a Kryo serializer class for the given type.

`addDefaultKryoSerializer(Class<?> type, Class<? extends Serializer<?>> serializerClass)`
`type`

registerTypeWithKryoSerializer(Class<?> type, Serializer<?> serializer) Register the given type with Kryo and specify a serializer for it. By registering a type with Kryo, the serialization of the type will be much more efficient.

`registerTypeWithKryoSerializer(Class<?> type, Serializer<?> serializer)`

registerKryoType(Class<?> type) If the type ends up being serialized with Kryo, then it will be registered at Kryo to make sure that only tags (integer IDs) are written. If a type is not registered with Kryo, its entire class-name will be serialized with every instance, leading to much higher I/O costs.

`registerKryoType(Class<?> type)`

registerPojoType(Class<?> type) Registers the given type with the serialization stack. If the type is eventually serialized as a POJO, then the type is registered with the POJO serializer. If the type ends up being serialized with Kryo, then it will be registered at Kryo to make sure that only tags are written. If a type is not registered with Kryo, its entire class-name will be serialized with every instance, leading to much higher I/O costs.

`registerPojoType(Class<?> type)`

Note that types registered with registerKryoType() are not available to Flink’s POJO serializer instance.

`registerKryoType()`
* 
disableAutoTypeRegistration() Automatic type registration is enabled by default. The automatic type registration is registering all types (including sub-types) used by usercode with Kryo and the POJO serializer.

* 
setTaskCancellationInterval(long interval) Sets the interval (in milliseconds) to wait between consecutive attempts to cancel a running task. When a task is canceled a new thread is created which periodically calls interrupt() on the task thread, if the task thread does not terminate within a certain time. This parameter refers to the time between consecutive calls to interrupt() and is set by default to 30000 milliseconds, or 30 seconds.


disableAutoTypeRegistration() Automatic type registration is enabled by default. The automatic type registration is registering all types (including sub-types) used by usercode with Kryo and the POJO serializer.

`disableAutoTypeRegistration()`

setTaskCancellationInterval(long interval) Sets the interval (in milliseconds) to wait between consecutive attempts to cancel a running task. When a task is canceled a new thread is created which periodically calls interrupt() on the task thread, if the task thread does not terminate within a certain time. This parameter refers to the time between consecutive calls to interrupt() and is set by default to 30000 milliseconds, or 30 seconds.

`setTaskCancellationInterval(long interval)`
`interrupt()`
`interrupt()`

The RuntimeContext which is accessible in Rich* functions through the getRuntimeContext() method also allows to access the ExecutionConfig in all user defined functions.

`RuntimeContext`
`Rich*`
`getRuntimeContext()`
`ExecutionConfig`

 Back to top
