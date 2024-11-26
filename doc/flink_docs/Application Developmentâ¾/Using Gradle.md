# Using Gradle


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# How to use Gradle to configure your project#


You will likely need a build tool to configure your Flink project. This guide will show you how to
do so with Gradle, an open-source general-purpose build tool that can be used
to automate tasks in the development process.


## Requirements#

* Gradle 7.x
* Java 8 (deprecated) or Java 11

## Importing the project into your IDE#


Once the project folder and files
have been created, we recommend that you import this project into your IDE for developing and testing.


IntelliJ IDEA supports Gradle projects via the Gradle plugin.

`Gradle`

Eclipse does so via the Eclipse Buildship
plugin (make sure to specify a Gradle version >= 3.0 in the last step of the import wizard; the shadow
plugin requires it). You may also use Gradle’s IDE integration
to create project files with Gradle.

`shadow`

Note: The default JVM heap size for Java may be too small for Flink and you have to manually increase it.
In Eclipse, choose Run Configurations -> Arguments and write into the VM Arguments box: -Xmx800m.
In IntelliJ IDEA recommended way to change JVM options is from the Help | Edit Custom VM Options menu.
See this article for details.

`Run Configurations -> Arguments`
`VM Arguments`
`-Xmx800m`
`Help | Edit Custom VM Options`

Note on IntelliJ: To make the applications run within IntelliJ IDEA, it is necessary to tick the
Include dependencies with "Provided" scope box in the run configuration. If this option is not available
(possibly due to using an older IntelliJ IDEA version), then a workaround is to create a test that
calls the application’s main() method.

`Include dependencies with "Provided" scope`
`main()`

## Building the project#


If you want to build/package your project, go to your project directory and
run the ‘gradle clean shadowJar’ command.
You will find a JAR file that contains your application, plus connectors and libraries
that you may have added as dependencies to the application: build/libs/<project-name>-<version>-all.jar.

`gradle clean shadowJar`
`build/libs/<project-name>-<version>-all.jar`

Note: If you use a different class than StreamingJob as the application’s main class / entry point,
we recommend you change the mainClassName setting in the build.gradle file accordingly. That way, Flink
can run the application from the JAR file without additionally specifying the main class.

`mainClassName`
`build.gradle`

## Adding dependencies to the project#


Specify a dependency configuration in the dependencies block of your build.gradle file.

`build.gradle`

For example, if you created your project using our Gradle build script or quickstart script, you can
add the Kafka connector as a dependency like this:


build.gradle


```
...
dependencies {
    ...  
    flinkShadowJar "org.apache.flink:flink-connector-kafka:${flinkVersion}"
    ...
}
...

```

`...
dependencies {
    ...  
    flinkShadowJar "org.apache.flink:flink-connector-kafka:${flinkVersion}"
    ...
}
...
`

Important: Note that all these (core) dependencies should have their scope set to provided. This means that
they are needed to compile against, but that they should not be packaged into the project’s resulting
application JAR file. If not set to provided, the best case scenario is that the resulting JAR
becomes excessively large, because it also contains all Flink core dependencies. The worst case scenario
is that the Flink core dependencies that are added to the application’s JAR file clash with some of
your own dependency versions (which is normally avoided through inverted classloading).


To correctly package the dependencies into the application JAR, these application dependencies must
be set to the compile scope.


## Packaging the application#


Depending on your use case, you may need to package your Flink application in different ways before
it gets deployed to a Flink environment.


If you want to create a JAR for a Flink Job and use only Flink dependencies without any third-party
dependencies (i.e. using the filesystem connector with JSON format), you do not need to create an
uber/fat JAR or shade any dependencies.


You can use the command gradle clean installDist. If you are using a Gradle
Wrapper, this would be ./gradlew clean installDist.

`gradle clean installDist`
`./gradlew clean installDist`

If you want to create a JAR for a Flink Job and use external dependencies not built into the Flink
distribution, you can either add them to the classpath of the distribution or shade them into your
uber/fat application JAR.


You can use the command gradle clean installShadowDist, which will produce a single fat JAR in /build/install/yourProject/lib.
If you are using a Gradle Wrapper,
this would be ./gradlew clean installShadowDist.

`gradle clean installShadowDist`
`/build/install/yourProject/lib`
`./gradlew clean installShadowDist`

With the generated uber/fat JAR, you can submit it to a local or remote cluster with:


```
bin/flink run -c org.example.MyJob myFatJar.jar

```

`bin/flink run -c org.example.MyJob myFatJar.jar
`

To learn more about how to deploy Flink jobs, check out the deployment guide.
