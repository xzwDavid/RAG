# Program Packaging


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Program Packaging and Distributed Execution#


As described earlier, Flink programs can be executed on
clusters by using a remote environment. Alternatively, programs can be packaged into JAR Files
(Java Archives) for execution. Packaging the program is a prerequisite to executing them through the
command line interface.

`remote environment`

### Packaging Programs#


To support execution from a packaged JAR file via the command line or web interface, a program must
use the environment obtained by StreamExecutionEnvironment.getExecutionEnvironment(). This environment
will act as the cluster’s environment when the JAR is submitted to the command line or web
interface. If the Flink program is invoked differently than through these interfaces, the
environment will act like a local environment.

`StreamExecutionEnvironment.getExecutionEnvironment()`

To package the program, simply export all involved classes as a JAR file. The JAR file’s manifest
must point to the class that contains the program’s entry point (the class with the public
main method). The simplest way to do this is by putting the main-class entry into the
manifest (such as main-class: org.apache.flinkexample.MyProgram). The main-class attribute is
the same one that is used by the Java Virtual Machine to find the main method when executing a JAR
files through the command java -jar pathToTheJarFile. Most IDEs offer to include that attribute
automatically when exporting JAR files.

`main`
`main-class: org.apache.flinkexample.MyProgram`
`java -jar pathToTheJarFile`

### Summary#


The overall procedure to invoke a packaged program consists of two steps:

1. 
The JAR’s manifest is searched for a main-class or program-class attribute. If both
attributes are found, the program-class attribute takes precedence over the main-class
attribute. Both the command line and the web interface support a parameter to pass the entry point
class name manually for cases where the JAR manifest contains neither attribute.

2. 
The system invokes the main method of the class.


The JAR’s manifest is searched for a main-class or program-class attribute. If both
attributes are found, the program-class attribute takes precedence over the main-class
attribute. Both the command line and the web interface support a parameter to pass the entry point
class name manually for cases where the JAR manifest contains neither attribute.


The system invokes the main method of the class.


 Back to top
