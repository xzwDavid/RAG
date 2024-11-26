# Task Failure Recovery


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Task Failure Recovery#


When a task failure happens, Flink needs to restart the failed task and other affected tasks to recover the job to a normal state.


Restart strategies and failover strategies are used to control the task restarting.
Restart strategies decide whether and when the failed/affected tasks can be restarted.
Failover strategies decide which tasks should be restarted to recover the job.


## Restart Strategies#


The cluster can be started with a default restart strategy which is always used when no job specific restart strategy has been defined.
In case that the job is submitted with a restart strategy, this strategy overrides the cluster’s default setting.


The default restart strategy is set via Flink configuration file.
The configuration parameter restart-strategy.type defines which strategy is taken.
If checkpointing is not enabled, the no restart strategy is used.
If checkpointing is activated and the restart strategy has not been configured,
the exponential-delay restart strategy and the default values of exponential-delay
related config options will be used.
See the following list of available restart strategies to learn what values are supported.

`no restart`
`exponential-delay`
`exponential-delay`

Each restart strategy comes with its own set of parameters which control its behaviour.
These values are also set in the configuration file.
The description of each restart strategy contains more information about the respective configuration values.


##### restart-strategy.type

* disable, off, none: No restart strategy.
* fixed-delay, fixeddelay: Fixed delay restart strategy. More details can be found here.
* failure-rate, failurerate: Failure rate restart strategy. More details can be found here.
* exponential-delay, exponentialdelay: Exponential delay restart strategy. More details can be found here.
`disable`
`off`
`none`
`fixed-delay`
`fixeddelay`
`failure-rate`
`failurerate`
`exponential-delay`
`exponentialdelay`
`disable`
`exponential-delay`
`exponential-delay`

Apart from defining a default restart strategy, it is possible to define for each Flink job a specific restart strategy.


The following example shows how we can set a fixed delay restart strategy for our job.
In case of a failure the system tries to restart the job 3 times and waits 10 seconds in-between successive restart attempts.


```
Configuration config = new Configuration();
config.set(RestartStrategyOptions.RESTART_STRATEGY, "fixed-delay");
config.set(RestartStrategyOptions.RESTART_STRATEGY_FIXED_DELAY_ATTEMPTS, 3); // number of restart attempts
config.set(RestartStrategyOptions.RESTART_STRATEGY_FIXED_DELAY_DELAY, Duration.ofSeconds(10)); // delay
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);

```

`Configuration config = new Configuration();
config.set(RestartStrategyOptions.RESTART_STRATEGY, "fixed-delay");
config.set(RestartStrategyOptions.RESTART_STRATEGY_FIXED_DELAY_ATTEMPTS, 3); // number of restart attempts
config.set(RestartStrategyOptions.RESTART_STRATEGY_FIXED_DELAY_DELAY, Duration.ofSeconds(10)); // delay
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setRestartStrategy(RestartStrategies.fixedDelayRestart(
  3, // number of restart attempts
  Duration.ofSeconds(10) // delay
))

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setRestartStrategy(RestartStrategies.fixedDelayRestart(
  3, // number of restart attempts
  Duration.ofSeconds(10) // delay
))
`

```
config = Configuration()
config.set_string('restart-strategy.type', 'fixed-delay')
config.set_string('restart-strategy.fixed-delay.attempts', '3') # number of restart attempts
config.set_string('restart-strategy.fixed-delay.delay', '10000 ms') # delay
env = StreamExecutionEnvironment.get_execution_environment(config)

```

`config = Configuration()
config.set_string('restart-strategy.type', 'fixed-delay')
config.set_string('restart-strategy.fixed-delay.attempts', '3') # number of restart attempts
config.set_string('restart-strategy.fixed-delay.delay', '10000 ms') # delay
env = StreamExecutionEnvironment.get_execution_environment(config)
`

The following sections describe restart strategy specific configuration options.


### Fixed Delay Restart Strategy#


The fixed delay restart strategy attempts a given number of times to restart the job.
If the maximum number of attempts is exceeded, the job eventually fails.
In-between two consecutive restart attempts, the restart strategy waits a fixed amount of time.


This strategy is enabled as default by setting the following configuration parameter in Flink configuration file.


```
restart-strategy.type: fixed-delay

```

`restart-strategy.type: fixed-delay
`

##### restart-strategy.fixed-delay.attempts

`restart-strategy.type`
`fixed-delay`

##### restart-strategy.fixed-delay.delay

`restart-strategy.type`
`fixed-delay`

For example:


```
restart-strategy.fixed-delay.attempts: 3
restart-strategy.fixed-delay.delay: 10 s

```

`restart-strategy.fixed-delay.attempts: 3
restart-strategy.fixed-delay.delay: 10 s
`

The fixed delay restart strategy can also be set programmatically:


```
Configuration config = new Configuration();
config.set(RestartStrategyOptions.RESTART_STRATEGY, "fixed-delay");
config.set(RestartStrategyOptions.RESTART_STRATEGY_FIXED_DELAY_ATTEMPTS, 3); // number of restart attempts
config.set(RestartStrategyOptions.RESTART_STRATEGY_FIXED_DELAY_DELAY, Duration.ofSeconds(10)); // delay
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);

```

`Configuration config = new Configuration();
config.set(RestartStrategyOptions.RESTART_STRATEGY, "fixed-delay");
config.set(RestartStrategyOptions.RESTART_STRATEGY_FIXED_DELAY_ATTEMPTS, 3); // number of restart attempts
config.set(RestartStrategyOptions.RESTART_STRATEGY_FIXED_DELAY_DELAY, Duration.ofSeconds(10)); // delay
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setRestartStrategy(RestartStrategies.fixedDelayRestart(
  3, // number of restart attempts
  Duration.ofSeconds(10) // delay
))

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setRestartStrategy(RestartStrategies.fixedDelayRestart(
  3, // number of restart attempts
  Duration.ofSeconds(10) // delay
))
`

```
config = Configuration()
config.set_string('restart-strategy.type', 'fixed-delay')
config.set_string('restart-strategy.fixed-delay.attempts', '3') # number of restart attempts
config.set_string('restart-strategy.fixed-delay.delay', '10000 ms') # delay
env = StreamExecutionEnvironment.get_execution_environment(config)

```

`config = Configuration()
config.set_string('restart-strategy.type', 'fixed-delay')
config.set_string('restart-strategy.fixed-delay.attempts', '3') # number of restart attempts
config.set_string('restart-strategy.fixed-delay.delay', '10000 ms') # delay
env = StreamExecutionEnvironment.get_execution_environment(config)
`

### Exponential Delay Restart Strategy#


In-between two consecutive restart attempts, the exponential delay restart strategy keeps exponentially increasing until the maximum number is reached.
Then, it keeps the delay at the maximum number.


When the job executes correctly, the exponential delay value resets after some time; this threshold is configurable.


```
restart-strategy.type: exponential-delay

```

`restart-strategy.type: exponential-delay
`

##### restart-strategy.exponential-delay.attempts-before-reset-backoff

`restart-strategy.type`
`exponential-delay`

##### restart-strategy.exponential-delay.backoff-multiplier

`restart-strategy.type`
`exponential-delay`

##### restart-strategy.exponential-delay.initial-backoff

`restart-strategy.type`
`exponential-delay`

##### restart-strategy.exponential-delay.jitter-factor

`restart-strategy.type`
`exponential-delay`

##### restart-strategy.exponential-delay.max-backoff

`restart-strategy.type`
`exponential-delay`

##### restart-strategy.exponential-delay.reset-backoff-threshold

`restart-strategy.type`
`exponential-delay`

For example:


```
restart-strategy.exponential-delay.initial-backoff: 10 s
restart-strategy.exponential-delay.max-backoff: 2 min
restart-strategy.exponential-delay.backoff-multiplier: 1.4
restart-strategy.exponential-delay.reset-backoff-threshold: 10 min
restart-strategy.exponential-delay.jitter-factor: 0.1
restart-strategy.exponential-delay.attempts-before-reset-backoff: 10

```

`restart-strategy.exponential-delay.initial-backoff: 10 s
restart-strategy.exponential-delay.max-backoff: 2 min
restart-strategy.exponential-delay.backoff-multiplier: 1.4
restart-strategy.exponential-delay.reset-backoff-threshold: 10 min
restart-strategy.exponential-delay.jitter-factor: 0.1
restart-strategy.exponential-delay.attempts-before-reset-backoff: 10
`

The exponential delay restart strategy can also be set programmatically:


```
Configuration config = new Configuration();
config.set(RestartStrategyOptions.RESTART_STRATEGY, "exponential-delay");
config.set(RestartStrategyOptions.RESTART_STRATEGY_EXPONENTIAL_DELAY_INITIAL_BACKOFF, Durartion.ofMillis(1));
config.set(RestartStrategyOptions.RESTART_STRATEGY_EXPONENTIAL_DELAY_MAX_BACKOFF, Durartion.ofMillis(1000));
config.set(RestartStrategyOptions.RESTART_STRATEGY_EXPONENTIAL_DELAY_BACKOFF_MULTIPLIER, 1.1); // exponential multiplier
config.set(RestartStrategyOptions.RESTART_STRATEGY_EXPONENTIAL_DELAY_RESET_BACKOFF_THRESHOLD, Durartion.ofMillis(2000)); // threshold duration to reset delay to its initial value
config.set(RestartStrategyOptions.RESTART_STRATEGY_EXPONENTIAL_DELAY_JITTER_FACTOR, 0.1); // jitter        
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);

```

`Configuration config = new Configuration();
config.set(RestartStrategyOptions.RESTART_STRATEGY, "exponential-delay");
config.set(RestartStrategyOptions.RESTART_STRATEGY_EXPONENTIAL_DELAY_INITIAL_BACKOFF, Durartion.ofMillis(1));
config.set(RestartStrategyOptions.RESTART_STRATEGY_EXPONENTIAL_DELAY_MAX_BACKOFF, Durartion.ofMillis(1000));
config.set(RestartStrategyOptions.RESTART_STRATEGY_EXPONENTIAL_DELAY_BACKOFF_MULTIPLIER, 1.1); // exponential multiplier
config.set(RestartStrategyOptions.RESTART_STRATEGY_EXPONENTIAL_DELAY_RESET_BACKOFF_THRESHOLD, Durartion.ofMillis(2000)); // threshold duration to reset delay to its initial value
config.set(RestartStrategyOptions.RESTART_STRATEGY_EXPONENTIAL_DELAY_JITTER_FACTOR, 0.1); // jitter        
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setRestartStrategy(RestartStrategies.exponentialDelayRestart(
  Duration.ofMillis(1), // initial delay between restarts
  Duration.ofMillis(1000), // maximum delay between restarts
  1.1, // exponential multiplier
  Duration.ofSeconds(2), // threshold duration to reset delay to its initial value
  0.1 // jitter
))

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setRestartStrategy(RestartStrategies.exponentialDelayRestart(
  Duration.ofMillis(1), // initial delay between restarts
  Duration.ofMillis(1000), // maximum delay between restarts
  1.1, // exponential multiplier
  Duration.ofSeconds(2), // threshold duration to reset delay to its initial value
  0.1 // jitter
))
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

#### Example#


Here is an example to explain how the exponential delay restart strategy works.


```
restart-strategy.exponential-delay.initial-backoff: 1 s
restart-strategy.exponential-delay.backoff-multiplier: 2
restart-strategy.exponential-delay.max-backoff: 10 s
# For convenience of description, jitter is turned off here
restart-strategy.exponential-delay.jitter-factor: 0

```

`restart-strategy.exponential-delay.initial-backoff: 1 s
restart-strategy.exponential-delay.backoff-multiplier: 2
restart-strategy.exponential-delay.max-backoff: 10 s
# For convenience of description, jitter is turned off here
restart-strategy.exponential-delay.jitter-factor: 0
`
* initial-backoff = 1s means that when an exception occurs for the first time, the job will be delayed for 1 second before retrying.
* backoff-multiplier = 2 means that when the job has continuous exceptions, the delay time is doubled each time.
* max-backoff = 10 s means the retry delay is at most 10 seconds.
`initial-backoff = 1s`
`backoff-multiplier = 2`
`max-backoff = 10 s`

Based on these parameters:

* When an exception occurs and the job needs to be retried for the 1st time, the job will be delayed for 1 second and then retry.
* When an exception occurs and the job needs to be retried for the 2nd time, the job will be delayed for 2 second and then retry.
* When an exception occurs and the job needs to be retried for the 3rd time, the job will be delayed for 4 second and then retry.
* When an exception occurs and the job needs to be retried for the 4th time, the job will be delayed for 8 second and then retry.
* When an exception occurs and the job needs to be retried for the 5th time, the job will be delayed for 10 second and then retry
(it will exceed the upper limit after doubling, so the upper limit of 10 seconds is used as the delay time)..
* On the 5th retry, the delay time has reached the upper limit (max-backoff), so after the 5th retry, the delay time will be always 10 seconds.
After each failure, it will be delayed for 10 seconds and then retry.

```
restart-strategy.exponential-delay.jitter-factor: 0.1
restart-strategy.exponential-delay.attempts-before-reset-backoff: 8
restart-strategy.exponential-delay.reset-backoff-threshold: 6 min

```

`restart-strategy.exponential-delay.jitter-factor: 0.1
restart-strategy.exponential-delay.attempts-before-reset-backoff: 8
restart-strategy.exponential-delay.reset-backoff-threshold: 6 min
`
* jitter-factor = 0.1 means that each delay time will be added or subtracted by a random value, and the ration range of the random value is within 0.1. For example:

In the 3rd retry, the job delay time is between 3.6 seconds and 4.4 seconds (3.6 = 4 * 0.9, 4.4 = 4 * 1.1).
In the 4th retry, the job delay time is between 7.2 seconds and 8.8 seconds (7.2 = 8 * 0.9, 8.8 = 8 * 1.1).
Random values can prevent multiple jobs restart at the same time, so it is not recommended to set jitter-factor to 0 in the production environment.


* attempts-before-reset-backoff = 8 means that if the job still encounters exceptions after 8 consecutive retries, it will fail (no more retries).
* reset-backoff-threshold = 6 min means that when the job runs for 6 minutes without an exception, the delay time and retry counter will be reset.
That is, when an exception occurs in a job, if the last exception occurred 6 minutes ago, the retry delay time is reset to 1 second and the current retry counter is reset to 1.
`jitter-factor = 0.1`
* In the 3rd retry, the job delay time is between 3.6 seconds and 4.4 seconds (3.6 = 4 * 0.9, 4.4 = 4 * 1.1).
* In the 4th retry, the job delay time is between 7.2 seconds and 8.8 seconds (7.2 = 8 * 0.9, 8.8 = 8 * 1.1).
* Random values can prevent multiple jobs restart at the same time, so it is not recommended to set jitter-factor to 0 in the production environment.
`attempts-before-reset-backoff = 8`
`reset-backoff-threshold = 6 min`

### Failure Rate Restart Strategy#


The failure rate restart strategy restarts job after failure, but when failure rate (failures per time interval) is exceeded, the job eventually fails.
In-between two consecutive restart attempts, the restart strategy waits a fixed amount of time.

`failure rate`

This strategy is enabled as default by setting the following configuration parameter in Flink configuration file.


```
restart-strategy.type: failure-rate

```

`restart-strategy.type: failure-rate
`

##### restart-strategy.failure-rate.delay

`restart-strategy.type`
`failure-rate`

##### restart-strategy.failure-rate.failure-rate-interval

`restart-strategy.type`
`failure-rate`

##### restart-strategy.failure-rate.max-failures-per-interval

`restart-strategy.type`
`failure-rate`

```
restart-strategy.failure-rate.max-failures-per-interval: 3
restart-strategy.failure-rate.failure-rate-interval: 5 min
restart-strategy.failure-rate.delay: 10 s

```

`restart-strategy.failure-rate.max-failures-per-interval: 3
restart-strategy.failure-rate.failure-rate-interval: 5 min
restart-strategy.failure-rate.delay: 10 s
`

The failure rate restart strategy can also be set programmatically:


```
Configuration config = new Configuration();
config.set(RestartStrategyOptions.RESTART_STRATEGY, "failure-rate");
config.set(RestartStrategyOptions.RESTART_STRATEGY_FAILURE_RATE_MAX_FAILURES_PER_INTERVAL, 3); // max failures per interval
config.set(RestartStrategyOptions.RESTART_STRATEGY_FAILURE_RATE_FAILURE_RATE_INTERVAL, Duration.ofMinutes(5)); // time interval for measuring failure rate
config.set(RestartStrategyOptions.RESTART_STRATEGY_FAILURE_RATE_DELAY, Duration.ofSeconds(10)); // delay
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);

```

`Configuration config = new Configuration();
config.set(RestartStrategyOptions.RESTART_STRATEGY, "failure-rate");
config.set(RestartStrategyOptions.RESTART_STRATEGY_FAILURE_RATE_MAX_FAILURES_PER_INTERVAL, 3); // max failures per interval
config.set(RestartStrategyOptions.RESTART_STRATEGY_FAILURE_RATE_FAILURE_RATE_INTERVAL, Duration.ofMinutes(5)); // time interval for measuring failure rate
config.set(RestartStrategyOptions.RESTART_STRATEGY_FAILURE_RATE_DELAY, Duration.ofSeconds(10)); // delay
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setRestartStrategy(RestartStrategies.failureRateRestart(
  3, // max failures per unit
  Duration.ofMinutes(5), //time interval for measuring failure rate
  Duration.ofSeconds(10) // delay
))

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setRestartStrategy(RestartStrategies.failureRateRestart(
  3, // max failures per unit
  Duration.ofMinutes(5), //time interval for measuring failure rate
  Duration.ofSeconds(10) // delay
))
`

```
config = Configuration()
config.set_string('restart-strategy.type', 'failure-rate')
config.set_string('restart-strategy.failure-rate.max-failures-per-interval', '3') # max failures per interval
config.set_string('restart-strategy.failure-rate.failure-rate-interval', '5 min') # time interval for measuring failure rate
config.set_string('restart-strategy.failure-rate.delay', '10 s') # delay
env = StreamExecutionEnvironment.get_execution_environment(config)

```

`config = Configuration()
config.set_string('restart-strategy.type', 'failure-rate')
config.set_string('restart-strategy.failure-rate.max-failures-per-interval', '3') # max failures per interval
config.set_string('restart-strategy.failure-rate.failure-rate-interval', '5 min') # time interval for measuring failure rate
config.set_string('restart-strategy.failure-rate.delay', '10 s') # delay
env = StreamExecutionEnvironment.get_execution_environment(config)
`

### No Restart Strategy#


The job fails directly and no restart is attempted.


```
restart-strategy.type: none

```

`restart-strategy.type: none
`

The no restart strategy can also be set programmatically:


```
Configuration config = new Configuration();
config.set(RestartStrategyOptions.RESTART_STRATEGY, "none");
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);

```

`Configuration config = new Configuration();
config.set(RestartStrategyOptions.RESTART_STRATEGY, "none");
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setRestartStrategy(RestartStrategies.noRestart())

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
env.setRestartStrategy(RestartStrategies.noRestart())
`

```
config = Configuration()
config.set_string('restart-strategy.type', 'none')
env = StreamExecutionEnvironment.get_execution_environment(config)

```

`config = Configuration()
config.set_string('restart-strategy.type', 'none')
env = StreamExecutionEnvironment.get_execution_environment(config)
`

### Fallback Restart Strategy#


The cluster defined restart strategy is used.
This is helpful for streaming programs which enable checkpointing.
By default, the exponential delay restart strategy is chosen if there is no other restart strategy defined.


### Default restart strategy#


When Checkpoint is enabled and the user does not specify a restart strategy, Exponential delay restart strategy
is the current default restart strategy. We strongly recommend Flink users to use the exponential delay restart strategy because by using this strategy,
jobs can be retried quickly when exceptions occur occasionally, and avalanches of external components can be avoided when exceptions occur frequently. The reasons are as follows:

`Exponential delay restart strategy`
* All restart strategies will delay some time when restarting the job to avoid frequent retries that put greater pressure on external components.
* The delay time for all restart strategies except the exponential delay restart strategy is fixed.

If the delay time is set too short, when exceptions occur frequently in a short period of time, the master node of external service will be accessed frequently, which may cause an avalanche of the external services.
For example: a large number of Flink jobs are consuming Kafka. When the Kafka cluster crashes, a large number of Flink jobs are frequently retried at the same time, which is likely to cause an avalanche.
If the delay time is set too long, when exceptions occur occasionally, jobs will have to wait a long time before retrying, resulting in reduced job availability.


* The delay time of each retry of the exponential delay restart strategy will increase exponentially until the maximum delay time is reached.

The initial value of the delay time is shorter, so when exceptions occur occasionally, jobs can be retried quickly to improve job availability.
When exceptions occur frequently in a short period of time, the exponential delay restart strategy will reduce the frequency of retries to avoid an avalanche of external services.


* In addition, the delay time of the exponential delay restart strategy supports the jitter-factor configuration option.

The jitter factor adds or subtracts a random value to each delay time.
Even if multiple jobs use an exponential delay restart strategy and the value of all configuration options are exactly the same, the jitter factor will let these jobs restart at different times.


* If the delay time is set too short, when exceptions occur frequently in a short period of time, the master node of external service will be accessed frequently, which may cause an avalanche of the external services.
For example: a large number of Flink jobs are consuming Kafka. When the Kafka cluster crashes, a large number of Flink jobs are frequently retried at the same time, which is likely to cause an avalanche.
* If the delay time is set too long, when exceptions occur occasionally, jobs will have to wait a long time before retrying, resulting in reduced job availability.
* The initial value of the delay time is shorter, so when exceptions occur occasionally, jobs can be retried quickly to improve job availability.
* When exceptions occur frequently in a short period of time, the exponential delay restart strategy will reduce the frequency of retries to avoid an avalanche of external services.
* The jitter factor adds or subtracts a random value to each delay time.
* Even if multiple jobs use an exponential delay restart strategy and the value of all configuration options are exactly the same, the jitter factor will let these jobs restart at different times.

## Failover Strategies#


Flink supports different failover strategies which can be configured via the configuration parameter
jobmanager.execution.failover-strategy in Flink configuration file.


### Restart All Failover Strategy#


This strategy restarts all tasks in the job to recover from a task failure.


### Restart Pipelined Region Failover Strategy#


This strategy groups tasks into disjoint regions. When a task failure is detected,
this strategy computes the smallest set of regions that must be restarted to recover from the failure.
For some jobs this can result in fewer tasks that will be restarted compared to the Restart All Failover Strategy.


A region is a set of tasks that communicate via pipelined data exchanges.
That is, batch data exchanges denote the boundaries of a region.


DataStream/Table/SQL job data exchanges are determined by the ExecutionMode,
which can be set through ExecutionConfig,
which are pipelined in Streaming Mode, are batched by default in Batch Mode.

`ExecutionMode`

The regions to restart are decided as below:

1. The region containing the failed task will be restarted.
2. If a result partition is not available while it is required by a region that will be restarted,
the region producing the result partition will be restarted as well.
3. If a region is to be restarted, all of its consumer regions will also be restarted. This is to guarantee
data consistency because nondeterministic processing or partitioning can result in different partitions.

 Back to top
