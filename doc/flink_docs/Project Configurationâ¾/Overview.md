# Overview


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Project Configuration#


The guides in this section will show you how to configure your projects via popular build tools
(Maven, Gradle),
add the necessary dependencies (i.e. connectors and formats,
testing), and cover some
advanced configuration topics.


Every Flink application depends on a set of Flink libraries. At a minimum, the application depends
on the Flink APIs and, in addition, on certain connector libraries (i.e. Kafka, Cassandra) and
3rd party dependencies required to the user to develop custom functions to process the data.


## Getting started#


To get started working on your Flink application, use the following commands, scripts, and templates
to create a Flink project.


You can create a project based on an Archetype
with the Maven command below or use the provided quickstart bash script.


> 
All Flink Scala APIs are deprecated and will be removed in a future Flink version. You can still build your application in Scala, but you should move to the Java version of either the DataStream and/or Table API.
See FLIP-265 Deprecate and remove Scala API support



All Flink Scala APIs are deprecated and will be removed in a future Flink version. You can still build your application in Scala, but you should move to the Java version of either the DataStream and/or Table API.


See FLIP-265 Deprecate and remove Scala API support


### Maven command#


```
$ mvn archetype:generate                \
  -DarchetypeGroupId=org.apache.flink   \
  -DarchetypeArtifactId=flink-quickstart-java \
  -DarchetypeVersion=2.0-SNAPSHOT

```

`$ mvn archetype:generate                \
  -DarchetypeGroupId=org.apache.flink   \
  -DarchetypeArtifactId=flink-quickstart-java \
  -DarchetypeVersion=2.0-SNAPSHOT
`

This allows you to name your newly created project and will interactively ask you for the groupId,
artifactId, and package name.


### Quickstart script#


```
$ curl https://flink.apache.org/q/quickstart.sh | bash -s 2.0-SNAPSHOT

```

`$ curl https://flink.apache.org/q/quickstart.sh | bash -s 2.0-SNAPSHOT
`

You can create an empty project, where you are required to create the src/main/java and
src/main/resources directories manually and start writing some class(es) in that, with the use
of the following Gradle build script or instead use the provided quickstart bash script to get a
completely functional startup project.

`src/main/java`
`src/main/resources`

### Gradle build script#


To execute these build configuration scripts, run the gradle command in the directory with these scripts.

`gradle`

build.gradle


```
plugins {
    id 'java'
    id 'application'
    // shadow plugin to produce fat JARs
    id 'com.github.johnrengelman.shadow' version '7.1.2'
}
// artifact properties
group = 'org.quickstart'
version = '0.1-SNAPSHOT'
mainClassName = 'org.quickstart.DataStreamJob'
description = """Flink Quickstart Job"""
ext {
    javaVersion = '1.8'
    flinkVersion = '2.0-SNAPSHOT'
    scalaBinaryVersion = '_2.12'
    slf4jVersion = '1.7.36'
    log4jVersion = '2.24.1'
}
sourceCompatibility = javaVersion
targetCompatibility = javaVersion
tasks.withType(JavaCompile) {
    options.encoding = 'UTF-8'
}
applicationDefaultJvmArgs = ["-Dlog4j.configurationFile=log4j2.properties"]

// declare where to find the dependencies of your project
repositories {
    mavenCentral()
    maven {
        url "https://repository.apache.org/content/repositories/snapshots"
        mavenContent {
            snapshotsOnly()
        }
    }
}
// NOTE: We cannot use "compileOnly" or "shadow" configurations since then we could not run code
// in the IDE or with "gradle run". We also cannot exclude transitive dependencies from the
// shadowJar yet (see https://github.com/johnrengelman/shadow/issues/159).
// -> Explicitly define the // libraries we want to be included in the "flinkShadowJar" configuration!
configurations {
    flinkShadowJar // dependencies which go into the shadowJar
    // always exclude these (also from transitive dependencies) since they are provided by Flink
    flinkShadowJar.exclude group: 'org.apache.flink', module: 'force-shading'
    flinkShadowJar.exclude group: 'com.google.code.findbugs', module: 'jsr305'
    flinkShadowJar.exclude group: 'org.slf4j'
    flinkShadowJar.exclude group: 'org.apache.logging.log4j'
}
// declare the dependencies for your production and test code
dependencies {
    // --------------------------------------------------------------
    // Compile-time dependencies that should NOT be part of the
    // shadow (uber) jar and are provided in the lib folder of Flink
    // --------------------------------------------------------------
    implementation "org.apache.flink:flink-streaming-java:${flinkVersion}"
    implementation "org.apache.flink:flink-clients:${flinkVersion}"
    // --------------------------------------------------------------
    // Dependencies that should be part of the shadow jar, e.g.
    // connectors. These must be in the flinkShadowJar configuration!
    // --------------------------------------------------------------
    //flinkShadowJar "org.apache.flink:flink-connector-kafka:${flinkVersion}"
    runtimeOnly "org.apache.logging.log4j:log4j-slf4j-impl:${log4jVersion}"
    runtimeOnly "org.apache.logging.log4j:log4j-api:${log4jVersion}"
    runtimeOnly "org.apache.logging.log4j:log4j-core:${log4jVersion}"
    // Add test dependencies here.
    // testCompile "junit:junit:4.12"
}
// make compileOnly dependencies available for tests:
sourceSets {
    main.compileClasspath += configurations.flinkShadowJar
    main.runtimeClasspath += configurations.flinkShadowJar
    test.compileClasspath += configurations.flinkShadowJar
    test.runtimeClasspath += configurations.flinkShadowJar
    javadoc.classpath += configurations.flinkShadowJar
}
run.classpath = sourceSets.main.runtimeClasspath

jar {
    manifest {
        attributes 'Built-By': System.getProperty('user.name'),
                'Build-Jdk': System.getProperty('java.version')
    }
}

shadowJar {
    configurations = [project.configurations.flinkShadowJar]
}

```

`plugins {
    id 'java'
    id 'application'
    // shadow plugin to produce fat JARs
    id 'com.github.johnrengelman.shadow' version '7.1.2'
}
// artifact properties
group = 'org.quickstart'
version = '0.1-SNAPSHOT'
mainClassName = 'org.quickstart.DataStreamJob'
description = """Flink Quickstart Job"""
ext {
    javaVersion = '1.8'
    flinkVersion = '2.0-SNAPSHOT'
    scalaBinaryVersion = '_2.12'
    slf4jVersion = '1.7.36'
    log4jVersion = '2.24.1'
}
sourceCompatibility = javaVersion
targetCompatibility = javaVersion
tasks.withType(JavaCompile) {
    options.encoding = 'UTF-8'
}
applicationDefaultJvmArgs = ["-Dlog4j.configurationFile=log4j2.properties"]

// declare where to find the dependencies of your project
repositories {
    mavenCentral()
    maven {
        url "https://repository.apache.org/content/repositories/snapshots"
        mavenContent {
            snapshotsOnly()
        }
    }
}
// NOTE: We cannot use "compileOnly" or "shadow" configurations since then we could not run code
// in the IDE or with "gradle run". We also cannot exclude transitive dependencies from the
// shadowJar yet (see https://github.com/johnrengelman/shadow/issues/159).
// -> Explicitly define the // libraries we want to be included in the "flinkShadowJar" configuration!
configurations {
    flinkShadowJar // dependencies which go into the shadowJar
    // always exclude these (also from transitive dependencies) since they are provided by Flink
    flinkShadowJar.exclude group: 'org.apache.flink', module: 'force-shading'
    flinkShadowJar.exclude group: 'com.google.code.findbugs', module: 'jsr305'
    flinkShadowJar.exclude group: 'org.slf4j'
    flinkShadowJar.exclude group: 'org.apache.logging.log4j'
}
// declare the dependencies for your production and test code
dependencies {
    // --------------------------------------------------------------
    // Compile-time dependencies that should NOT be part of the
    // shadow (uber) jar and are provided in the lib folder of Flink
    // --------------------------------------------------------------
    implementation "org.apache.flink:flink-streaming-java:${flinkVersion}"
    implementation "org.apache.flink:flink-clients:${flinkVersion}"
    // --------------------------------------------------------------
    // Dependencies that should be part of the shadow jar, e.g.
    // connectors. These must be in the flinkShadowJar configuration!
    // --------------------------------------------------------------
    //flinkShadowJar "org.apache.flink:flink-connector-kafka:${flinkVersion}"
    runtimeOnly "org.apache.logging.log4j:log4j-slf4j-impl:${log4jVersion}"
    runtimeOnly "org.apache.logging.log4j:log4j-api:${log4jVersion}"
    runtimeOnly "org.apache.logging.log4j:log4j-core:${log4jVersion}"
    // Add test dependencies here.
    // testCompile "junit:junit:4.12"
}
// make compileOnly dependencies available for tests:
sourceSets {
    main.compileClasspath += configurations.flinkShadowJar
    main.runtimeClasspath += configurations.flinkShadowJar
    test.compileClasspath += configurations.flinkShadowJar
    test.runtimeClasspath += configurations.flinkShadowJar
    javadoc.classpath += configurations.flinkShadowJar
}
run.classpath = sourceSets.main.runtimeClasspath

jar {
    manifest {
        attributes 'Built-By': System.getProperty('user.name'),
                'Build-Jdk': System.getProperty('java.version')
    }
}

shadowJar {
    configurations = [project.configurations.flinkShadowJar]
}
`

settings.gradle


```
rootProject.name = 'quickstart'

```

`rootProject.name = 'quickstart'
`

### Quickstart script#


```
bash -c "$(curl https://flink.apache.org/q/gradle-quickstart.sh)" -- 2.0-SNAPSHOT _2.12

```

`bash -c "$(curl https://flink.apache.org/q/gradle-quickstart.sh)" -- 2.0-SNAPSHOT _2.12
`

## Which dependencies do you need?#


To start working on a Flink job, you usually need the following dependencies:

* Flink APIs, in order to develop your job
* Connectors and formats, in order to integrate your job with external systems
* Testing utilities, in order to test your job

And in addition to these, you might want to add 3rd party dependencies that you need to develop custom functions.


### Flink APIs#


Flink offers two major APIs: Datastream API and Table API & SQL.
They can be used separately, or they can be mixed, depending on your use cases:

`flink-streaming-java`
`flink-table-api-java`
`flink-table-api-scala_2.12`
`flink-table-api-java-bridge`
`flink-table-api-scala-bridge_2.12`

Just include them in your build tool script/descriptor, and you can start developing your job!


## Running and packaging#


If you want to run your job by simply executing the main class, you will need flink-clients in your classpath.
In case of Table API programs, you will also need flink-table-runtime and flink-table-planner-loader.

`flink-clients`
`flink-table-runtime`
`flink-table-planner-loader`

As a rule of thumb, we suggest packaging the application code and all its required dependencies into one fat/uber JAR.
This includes packaging connectors, formats, and third-party dependencies of your job.
This rule does not apply to Java APIs, DataStream Scala APIs, and the aforementioned runtime modules,
which are already provided by Flink itself and should not be included in a job uber JAR.
This job JAR can be submitted to an already running Flink cluster, or added to a Flink application
container image easily without modifying the distribution.


## What’s next?#

* To start developing your job, check out DataStream API and Table API & SQL.
* For more details on how to package your job depending on the build tools, check out the following specific guides:

Maven
Gradle


* For more advanced topics about project configuration, check out the section on advanced topics.
* Maven
* Gradle