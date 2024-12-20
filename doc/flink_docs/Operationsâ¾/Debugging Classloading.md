# Debugging Classloading


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Debugging Classloading#


## Overview of Classloading in Flink#


When running Flink applications, the JVM will load various classes over time.
These classes can be divided into three groups based on their origin:

* 
The Java Classpath: This is Java’s common classpath, and it includes the JDK libraries, and all code
in Flink’s /lib folder (the classes of Apache Flink and some dependencies). They are loaded by AppClassLoader.

* 
The Flink Plugin Components: The plugins code in folders under Flink’s /plugins folder. Flink’s plugin mechanism will dynamically load them once during startup.

* 
The Dynamic User Code: These are all classes that are included in the JAR files of dynamically submitted jobs,
(via REST, CLI, web UI). They are loaded (and unloaded) dynamically by FlinkUserCodeClassLoader per job.


The Java Classpath: This is Java’s common classpath, and it includes the JDK libraries, and all code
in Flink’s /lib folder (the classes of Apache Flink and some dependencies). They are loaded by AppClassLoader.

`/lib`

The Flink Plugin Components: The plugins code in folders under Flink’s /plugins folder. Flink’s plugin mechanism will dynamically load them once during startup.

`/plugins`

The Dynamic User Code: These are all classes that are included in the JAR files of dynamically submitted jobs,
(via REST, CLI, web UI). They are loaded (and unloaded) dynamically by FlinkUserCodeClassLoader per job.


As a general rule, whenever you start the Flink processes first and submit jobs later, the job’s classes are loaded dynamically.
If the Flink processes are started together with the job/application, or if the application spawns the Flink components (JobManager, TaskManager, etc.), then all job’s classes are in the Java classpath.


Code in plugin components is loaded dynamically once by a dedicated class loader per plugin.


In the following are some more details about the different deployment modes:


Session Mode (Standalone/Yarn/Kubernetes)


When starting a Flink session(Standalone/Yarn/Kubernetes) cluster, the JobManagers and TaskManagers are started with the Flink framework classes in the
Java classpath. The classes from all jobs/applications that are submitted against the session (via REST / CLI) are loaded dynamically by FlinkUserCodeClassLoader.


Per-Job Mode (deprecated) (Yarn)


Currently, only Yarn supports Per-Job mode. By default, running a Flink cluster in Per-Job mode will include the user jars
(the JAR file specified in startup command and all JAR files in Flink’s usrlib folder) into the system classpath (the AppClassLoader).
This behavior can be controlled with the yarn.classpath.include-user-jar config option.
When setting it to DISABLED, Flink will include the user jars in the user classpath and load them dynamically by FlinkUserCodeClassLoader.
See Flink on Yarn for more details.

`usrlib`
`DISABLED`

Application Mode (Standalone/Yarn/Kubernetes)


When run a Standalone/Kubernetes Flink cluster in Application Mode, the user jars (the JAR file specified in startup command and all JAR files in Flink’s usrlib folder)
will be loaded dynamically by FlinkUserCodeClassLoader.

`usrlib`

When run a Yarn Flink cluster in Application Mode, the user jars (the JAR file specified in startup command and all JAR files in Flink’s usrlib folder)
will be included into the system classpath (the AppClassLoader) by default. Same as Per-Job mode, when setting the yarn.classpath.include-user-jar
to DISABLED, Flink will include the user jars in the user classpath and load them dynamically by FlinkUserCodeClassLoader.

`usrlib`
`DISABLED`

## Inverted Class Loading and ClassLoader Resolution Order#


In setups where dynamic classloading is involved (plugin components, Flink jobs in session setups), there is a hierarchy of typically two ClassLoaders:
(1) Java’s application classloader, which has all classes in the classpath, and (2) the dynamic plugin/user code classloader.
for loading classes from the plugin or the user-code jar(s). The dynamic ClassLoader has the application classloader as its parent.


By default, Flink inverts classloading order, meaning it looks into the dynamic classloader first, and only looks into
the parent (application classloader) if the class is not part of the dynamically loaded code.


The benefit of inverted classloading is that plugins and jobs can use different library versions than Flink’s core itself, which is very
useful when the different versions of the libraries are not compatible. The mechanism helps to avoid the common dependency conflict
errors like IllegalAccessError or NoSuchMethodError. Different parts of the code simply have separate copies of the
classes (Flink’s core or one of its dependencies can use a different copy than the user code or plugin code).
In most cases, this works well and no additional configuration from the user is needed.

`IllegalAccessError`
`NoSuchMethodError`

However, there are cases when the inverted classloading causes problems (see below, “X cannot be cast to X”).
For user code classloading, you can revert back to Java’s default mode by configuring the ClassLoader resolution order via
classloader.resolve-order in the Flink config to parent-first
(from Flink’s default child-first).

`classloader.resolve-order`
`parent-first`
`child-first`

Please note that certain classes are always resolved in a parent-first way (through the parent ClassLoader first), because they
are shared between Flink’s core and the plugin/user code or the plugin/user-code facing APIs. The packages for these classes are configured via
classloader.parent-first-patterns.default and
classloader.parent-first-patterns.additional.
To add new packages to be parent-first loaded, please set the classloader.parent-first-patterns.additional config option.

`classloader.parent-first-patterns.default`
`classloader.parent-first-patterns.additional`
`classloader.parent-first-patterns.additional`

## Avoiding Dynamic Classloading for User Code#


All components (JobManager, TaskManager, Client, ApplicationMaster, …) log their classpath setting on startup.
They can be found as part of the environment information at the beginning of the log.


When running a setup where the JobManager and TaskManagers are exclusive to one particular job, one can put user code JAR files
directly into the /lib folder to make sure they are part of the classpath and not loaded dynamically.

`/lib`

It usually works to put the job’s JAR file into the /lib directory. The JAR will be part of both the classpath
(the AppClassLoader) and the dynamic class loader (FlinkUserCodeClassLoader).
Because the AppClassLoader is the parent of the FlinkUserCodeClassLoader (and Java loads parent-first, by default), this should
result in classes being loaded only once.

`/lib`

For setups where the job’s JAR file cannot be put to the /lib folder (for example because the setup is a session that is
used by multiple jobs), it may still be possible to put common libraries to the /lib folder, and avoid dynamic class loading
for those.

`/lib`
`/lib`

## Manual Classloading in User Code#


In some cases, a transformation function, source, or sink needs to manually load classes (dynamically via reflection).
To do that, it needs the classloader that has access to the job’s classes.


In that case, the functions (or sources or sinks) can be made a RichFunction (for example RichMapFunction or RichWindowFunction)
and access the user code class loader via getRuntimeContext().getUserCodeClassLoader().

`RichFunction`
`RichMapFunction`
`RichWindowFunction`
`getRuntimeContext().getUserCodeClassLoader()`

## X cannot be cast to X exceptions#


In setups with dynamic classloading, you may see an exception in the style com.foo.X cannot be cast to com.foo.X.
This means that multiple versions of the class com.foo.X have been loaded by different class loaders, and types of that class are attempted to be assigned to each other.

`com.foo.X cannot be cast to com.foo.X`
`com.foo.X`

One common reason is that a library is not compatible with Flink’s inverted classloading approach. You can turn off inverted classloading
to verify this (set classloader.resolve-order: parent-first in the Flink config) or exclude
the library from inverted classloading (set classloader.parent-first-patterns.additional
in the Flink config).

`classloader.resolve-order: parent-first`
`classloader.parent-first-patterns.additional`

Another cause can be cached object instances, as produced by some libraries like Apache Avro, or by interning objects (for example via Guava’s Interners).
The solution here is to either have a setup without any dynamic classloading, or to make sure that the respective library is fully part of the dynamically loaded code.
The latter means that the library must not be added to Flink’s /lib folder, but must be part of the application’s fat-jar/uber-jar

`/lib`

## Unloading of Dynamically Loaded Classes in User Code#


All scenarios that involve dynamic user code classloading (sessions) rely on classes being unloaded again.
Class unloading means that the Garbage Collector finds that no objects from a class exist and more, and thus removes the class
(the code, static variable, metadata, etc).


Whenever a TaskManager starts (or restarts) a task, it will load that specific task’s code. Unless classes can be unloaded, this will
become a memory leak, as new versions of classes are loaded and the total number of loaded classes accumulates over time. This
typically manifests itself though a OutOfMemoryError: Metaspace.


Common causes for class leaks and suggested fixes:

* 
Lingering Threads: Make sure the application functions/sources/sinks shuts down all threads. Lingering threads cost resources themselves and
additionally typically hold references to (user code) objects, preventing garbage collection and unloading of the classes.

* 
Interners: Avoid caching objects in special structures that live beyond the lifetime of the functions/sources/sinks. Examples are Guava’s
interners, or Avro’s class/object caches in the serializers.

* 
JDBC: JDBC drivers leak references outside the user code classloader. To ensure that these classes are only loaded once
you should add the driver jars to Flink’s lib/ folder instead of bundling them in the user-jar.
If you can’t guarantee that none of your user-jars bundle the driver, you have to additionally add the driver classes to the list of parent-first
loaded classes via classloader.parent-first-patterns.additional.


Lingering Threads: Make sure the application functions/sources/sinks shuts down all threads. Lingering threads cost resources themselves and
additionally typically hold references to (user code) objects, preventing garbage collection and unloading of the classes.


Interners: Avoid caching objects in special structures that live beyond the lifetime of the functions/sources/sinks. Examples are Guava’s
interners, or Avro’s class/object caches in the serializers.


JDBC: JDBC drivers leak references outside the user code classloader. To ensure that these classes are only loaded once
you should add the driver jars to Flink’s lib/ folder instead of bundling them in the user-jar.
If you can’t guarantee that none of your user-jars bundle the driver, you have to additionally add the driver classes to the list of parent-first
loaded classes via classloader.parent-first-patterns.additional.

`lib/`
`classloader.parent-first-patterns.additional`

A helpful tool for unloading dynamically loaded classes are the user code class loader release hooks. These are hooks which are executed prior to the unloading of a classloader. It is generally recommended to shutdown and unload resources as part of the regular function lifecycle (typically the close() methods). But in some cases (for example for static fields), it is better to unload once a classloader is certainly not needed anymore.

`close()`

Class loader release hooks can be registered via the RuntimeContext.registerUserCodeClassLoaderReleaseHookIfAbsent() method.

`RuntimeContext.registerUserCodeClassLoaderReleaseHookIfAbsent()`

## Resolving Dependency Conflicts with Flink using the maven-shade-plugin.#


A way to address dependency conflicts from the application developer’s side is to avoid exposing dependencies by shading them away.


Apache Maven offers the maven-shade-plugin, which allows one to change the package of a
class after compiling it (so the code you are writing is not affected by the shading). For example if you have the com.amazonaws packages from
the aws sdk in your user code jar, the shade plugin would relocate them into the org.myorg.shaded.com.amazonaws package, so that your code is calling your aws sdk version.

`com.amazonaws`
`org.myorg.shaded.com.amazonaws`

This documentation page explains relocating classes using the shade plugin.


Note that most of Flink’s dependencies, such as guava, netty, jackson, etc. are shaded away by the maintainers of Flink, so users usually don’t have to worry about it.

`guava`
`netty`
`jackson`

 Back to top
