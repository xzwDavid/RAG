# Java Compatibility


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Java compatibility#


This page lists which Java versions Flink supports and what limitations apply (if any).


## Java 11#


Support for Java 11 was added in 1.10.0 and is the recommended Java version to run Flink on.


This is the default version for docker images.


### Untested Flink features#


The following Flink features have not been tested with Java 11:

* Hive connector
* Hbase 1.x connector

### Untested language features#

* Modularized user jars have not been tested.

## Java 17#


Experimental support for Java 17 was added in 1.18. (FLINK-15736)
In Flink 1.19, we added support for Java Records. (FLINK-32380)


### Untested Flink features#


These Flink features have not been tested with Java 17:

* Hive connector
* Hbase 1.x connector

### JDK modularization#


Starting with Java 16 Java applications have to fully cooperate with the JDK modularization, also known as Project Jigsaw.
This means that access to JDK classes/internal must be explicitly allowed by the application when it is started, on a per-module basis, in the form of –add-opens/–add-exports JVM arguments.


Since Flink uses reflection for serializing user-defined functions and data (via Kryo), this means that if your UDFs or data types use JDK classes you may have to allow access to these JDK classes.


These should be configured via the env.java.opts.all option.


In the default configuration in the Flink distribution this option is configured such that Flink itself works on Java 17.
The list of configured arguments must not be shortened, but only extended.


### Known issues#

* Mandatory Kryo dependency upgrade, FLIP-371.
* SIGSEGV in C2 Compiler thread: Early Java 17 builds are affected by a bug where the JVM can fail abruptly. Update your Java 17 installation to resolve the issue. See JDK-8277529 for details.