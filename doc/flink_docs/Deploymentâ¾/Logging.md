# Logging


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# How to use logging#


All Flink processes create a log text file that contains messages for various events happening in that process.
These logs provide deep insights into the inner workings of Flink, and can be used to detect problems (in the form of WARN/ERROR messages) and can help in debugging them.


The log files can be accessed via the Job-/TaskManager pages of the WebUI. The used Resource Provider (e.g., YARN) may provide additional means of accessing them.


The logging in Flink uses the SLF4J logging interface.
This allows you to use any logging framework that supports SLF4J, without having to modify the Flink source code.


By default, Log4j 2 is used as the underlying logging framework.


### Structured logging#


Flink adds the following fields to MDC of most of the relevant log messages (experimental feature):

* Job ID

key: flink-job-id
format: string
length 32


* key: flink-job-id
* format: string
* length 32
`flink-job-id`

This is most useful in environments with structured logging and allows you to quickly filter the relevant logs.


The MDC is propagated by slf4j to the logging backend which usually adds it to the log records automatically (e.g. in log4j json layout).
Alternatively, it can be configured explicitly - log4j pattern layout might look like this:


[%-32X{flink-job-id}] %c{0} %m%n.

`[%-32X{flink-job-id}] %c{0} %m%n`

## Configuring Log4j 2#


Log4j 2 is controlled using a mixture of property files and configuration.


### Log4j 2 property files#


The Flink distribution ships with the following log4j properties files in the conf directory, which are used automatically if Log4j 2 is enabled:

`conf`
* log4j-cli.properties: used by the command line interface (e.g., flink run, sql-client)
* log4j-session.properties: used by the command line interface when starting a Kubernetes/Yarn session cluster (i.e., kubernetes-session.sh/yarn-session.sh)
* log4j-console.properties: used for Job-/TaskManagers if they are run in the foreground (e.g., Kubernetes)
* log4j.properties: used for Job-/TaskManagers by default
`log4j-cli.properties`
`flink run`
`sql-client`
`log4j-session.properties`
`kubernetes-session.sh`
`yarn-session.sh`
`log4j-console.properties`
`log4j.properties`

Log4j periodically scans this file for changes and adjusts the logging behavior if necessary.
By default, this check happens every 30 seconds and is controlled by the monitorInterval setting in the Log4j properties files.

`monitorInterval`

### Log4j 2 configuration#


The following logging-related configuration options are available:

`env.log.dir`
`log`
`env.log.level`
`INFO`
`env.log.max`

### Compatibility with Log4j 1#


Flink ships with the Log4j API bridge, allowing existing applications that work against Log4j1 classes to continue working.


If you have custom Log4j 1 properties files or code that relies on Log4j 1, please check out the official Log4j compatibility and migration guides.


## Configuring Log4j1#


To use Flink with Log4j 1 you must ensure that:

* org.apache.logging.log4j:log4j-core, org.apache.logging.log4j:log4j-slf4j-impl and org.apache.logging.log4j:log4j-1.2-api are not on the classpath,
* log4j:log4j, org.slf4j:slf4j-log4j12, org.apache.logging.log4j:log4j-to-slf4j and org.apache.logging.log4j:log4j-api are on the classpath.
`org.apache.logging.log4j:log4j-core`
`org.apache.logging.log4j:log4j-slf4j-impl`
`org.apache.logging.log4j:log4j-1.2-api`
`log4j:log4j`
`org.slf4j:slf4j-log4j12`
`org.apache.logging.log4j:log4j-to-slf4j`
`org.apache.logging.log4j:log4j-api`

In the IDE this means you have to replace such dependencies defined in your pom, and possibly add exclusions on dependencies that transitively depend on them.


For Flink distributions this means you have to

* remove the log4j-core, log4j-slf4j-impl and log4j-1.2-api jars from the lib directory,
* add the log4j, slf4j-log4j12 and log4j-to-slf4j jars to the lib directory,
* replace all log4j properties files in the conf directory with Log4j1-compliant versions.
`log4j-core`
`log4j-slf4j-impl`
`log4j-1.2-api`
`lib`
`log4j`
`slf4j-log4j12`
`log4j-to-slf4j`
`lib`
`conf`

## Configuring logback#


To use Flink with logback you must ensure that:

* org.apache.logging.log4j:log4j-slf4j-impl is not on the classpath,
* ch.qos.logback:logback-core and ch.qos.logback:logback-classic are on the classpath.
`org.apache.logging.log4j:log4j-slf4j-impl`
`ch.qos.logback:logback-core`
`ch.qos.logback:logback-classic`

In the IDE this means you have to replace such dependencies defined in your pom, and possibly add exclusions on dependencies that transitively depend on them.


For Flink distributions this means you have to

* remove the log4j-slf4j-impl jar from the lib directory,
* add the logback-core, and logback-classic jars to the lib directory.
`log4j-slf4j-impl`
`lib`
`logback-core`
`logback-classic`
`lib`

The Flink distribution ships with the following logback configuration files in the conf directory, which are used automatically if logback is enabled:

`conf`
* logback-session.properties: used by the command line interface when starting a Kubernetes/Yarn session cluster (i.e., kubernetes-session.sh/yarn-session.sh)
* logback-console.properties: used for Job-/TaskManagers if they are run in the foreground (e.g., Kubernetes)
* logback.xml: used for command line interface and Job-/TaskManagers by default
`logback-session.properties`
`kubernetes-session.sh`
`yarn-session.sh`
`logback-console.properties`
`logback.xml`

> 
  Logback 1.3+ requires SLF4J 2, which is currently not supported.



## Best practices for developers#


You can create an SLF4J logger by calling org.slf4j.LoggerFactory#LoggerFactory.getLogger with the Class of your class as an argument.

`org.slf4j.LoggerFactory#LoggerFactory.getLogger`
`Class`

We highly recommend storing this logger in a private static final field.

`private static final`

```
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Foobar {
	private static final Logger LOG = LoggerFactory.getLogger(Foobar.class);

	public static void main(String[] args) {
		LOG.info("Hello world!");
	}
}

```

`import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Foobar {
	private static final Logger LOG = LoggerFactory.getLogger(Foobar.class);

	public static void main(String[] args) {
		LOG.info("Hello world!");
	}
}
`

In order to benefit most from SLF4J, it is recommended to use its placeholder mechanism.
Using placeholders allows avoiding unnecessary string constructions in case that the logging level is set so high that the message would not be logged.


The syntax of placeholders is the following:


```
LOG.info("This message contains {} placeholders. {}", 2, "Yippie");

```

`LOG.info("This message contains {} placeholders. {}", 2, "Yippie");
`

Placeholders can also be used in conjunction with exceptions which shall be logged.


```
catch(Exception exception){
	LOG.error("An {} occurred.", "error", exception);
}

```

`catch(Exception exception){
	LOG.error("An {} occurred.", "error", exception);
}
`

 Back to top
