# Using Maven


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# How to use Maven to configure your project#


This guide will show you how to configure a Flink job project with Maven,
an open-source build automation tool developed by the Apache Software Foundation that enables you to build,
publish, and deploy projects. You can use it to manage the entire lifecycle of your software project.


## Requirements#

* Maven 3.8.6
* Java 8 (deprecated) or Java 11

## Importing the project into your IDE#


Once the project folder and files
have been created, we recommend that you import this project into your IDE for developing and testing.


IntelliJ IDEA supports Maven projects out-of-the-box. Eclipse offers the m2e plugin
to import Maven projects.


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


If you want to build/package your project, navigate to your project directory and run the
‘mvn clean package’ command. You will find a JAR file that contains your application (plus connectors
and libraries that you may have added as dependencies to the application) here:target/<artifact-id>-<version>.jar.

`mvn clean package`
`target/<artifact-id>-<version>.jar`

Note: If you used a different class than DataStreamJob as the application’s main class / entry point,
we recommend you change the mainClass setting in the pom.xml file accordingly so that Flink
can run the application from the JAR file without additionally specifying the main class.

`DataStreamJob`
`mainClass`
`pom.xml`

## Adding dependencies to the project#


Open the pom.xml file in your project directory and add the dependency in between
the dependencies tab.

`pom.xml`
`dependencies`

For example, you can add the Kafka connector as a dependency like this:


```
<dependencies>
    
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-connector-kafka</artifactId>
        <version>2.0-SNAPSHOT</version>
    </dependency>
    
</dependencies>

```

`<dependencies>
    
    <dependency>
        <groupId>org.apache.flink</groupId>
        <artifactId>flink-connector-kafka</artifactId>
        <version>2.0-SNAPSHOT</version>
    </dependency>
    
</dependencies>
`

Then execute mvn install on the command line.

`mvn install`

Projects created from the Java Project Template, the Scala Project Template, or Gradle are configured
to automatically include the application dependencies into the application JAR when you run mvn clean package.
For projects that are not set up from those templates, we recommend adding the Maven Shade Plugin to
build the application jar with all required dependencies.

`Java Project Template`
`Scala Project Template`
`mvn clean package`

Important: Note that all these core API dependencies should have their scope set to provided. This means that
they are needed to compile against, but that they should not be packaged into the project’s resulting
application JAR file. If not set to provided, the best case scenario is that the resulting JAR
becomes excessively large, because it also contains all Flink core dependencies. The worst case scenario
is that the Flink core dependencies that are added to the application’s JAR file clash with some of
your own dependency versions (which is normally avoided through inverted classloading).


To correctly package the dependencies into the application JAR, the Flink API dependencies must
be set to the compile scope.


## Packaging the application#


Depending on your use case, you may need to package your Flink application in different ways before it
gets deployed to a Flink environment.


If you want to create a JAR for a Flink Job and use only Flink dependencies without any third-party
dependencies (i.e. using the filesystem connector with JSON format), you do not need to create an
uber/fat JAR or shade any dependencies.


If you want to create a JAR for a Flink Job and use external dependencies not built into the Flink
distribution, you can either add them to the classpath of the distribution or shade them into your
uber/fat application JAR.


With the generated uber/fat JAR, you can submit it to a local or remote cluster with:


```
bin/flink run -c org.example.MyJob myFatJar.jar

```

`bin/flink run -c org.example.MyJob myFatJar.jar
`

To learn more about how to deploy Flink jobs, check out the deployment guide.


## Template for creating an uber/fat JAR with dependencies#


To build an application JAR that contains all dependencies required for declared connectors and libraries,
you can use the following shade plugin definition:


```
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-shade-plugin</artifactId>
            <version>3.1.1</version>
            <executions>
                <execution>
                    <phase>package</phase>
                    <goals>
                        <goal>shade</goal>
                    </goals>
                    <configuration>
                        <artifactSet>
                            <excludes>
                                <exclude>com.google.code.findbugs:jsr305</exclude>
                            </excludes>
                        </artifactSet>
                        <filters>
                            <filter>
                                <!-- Do not copy the signatures in the META-INF folder.
                                Otherwise, this might cause SecurityExceptions when using the JAR. -->
                                <artifact>*:*</artifact>
                                <excludes>
                                    <exclude>META-INF/*.SF</exclude>
                                    <exclude>META-INF/*.DSA</exclude>
                                    <exclude>META-INF/*.RSA</exclude>
                                </excludes>
                            </filter>
                        </filters>
                        <transformers>
                            <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                <!-- Replace this with the main class of your job -->
                                <mainClass>my.programs.main.clazz</mainClass>
                            </transformer>
                            <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
                        </transformers>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>

```

`<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-shade-plugin</artifactId>
            <version>3.1.1</version>
            <executions>
                <execution>
                    <phase>package</phase>
                    <goals>
                        <goal>shade</goal>
                    </goals>
                    <configuration>
                        <artifactSet>
                            <excludes>
                                <exclude>com.google.code.findbugs:jsr305</exclude>
                            </excludes>
                        </artifactSet>
                        <filters>
                            <filter>
                                <!-- Do not copy the signatures in the META-INF folder.
                                Otherwise, this might cause SecurityExceptions when using the JAR. -->
                                <artifact>*:*</artifact>
                                <excludes>
                                    <exclude>META-INF/*.SF</exclude>
                                    <exclude>META-INF/*.DSA</exclude>
                                    <exclude>META-INF/*.RSA</exclude>
                                </excludes>
                            </filter>
                        </filters>
                        <transformers>
                            <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                <!-- Replace this with the main class of your job -->
                                <mainClass>my.programs.main.clazz</mainClass>
                            </transformer>
                            <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
                        </transformers>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
`

The Maven shade plugin will include,
by default, all the dependencies in the “runtime” and “compile” scope.
