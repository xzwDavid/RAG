# Handling Application Parameters


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Handling Application Parameters#


## Handling Application Parameters#


Almost all Flink applications, both batch and streaming, rely on external configuration parameters.
They are used to specify input and output sources (like paths or addresses), system parameters (parallelism, runtime configuration), and application specific parameters (typically used within user functions).


Flink provides a simple utility called ParameterTool to provide some basic tooling for solving these problems.
Please note that you don’t have to use the ParameterTool described here. Other frameworks such as Commons CLI and
argparse4j also work well with Flink.

`ParameterTool`
`ParameterTool`

### Getting your configuration values into theParameterTool#

`ParameterTool`

The ParameterTool provides a set of predefined static methods for reading the configuration. The tool is internally expecting a Map<String, String>, so it’s very easy to integrate it with your own configuration style.

`ParameterTool`
`Map<String, String>`

#### From.propertiesfiles#

`.properties`

The following method will read a Properties file and provide the key/value pairs:


```
String propertiesFilePath = "/home/sam/flink/myjob.properties";
ParameterTool parameters = ParameterTool.fromPropertiesFile(propertiesFilePath);

File propertiesFile = new File(propertiesFilePath);
ParameterTool parameters = ParameterTool.fromPropertiesFile(propertiesFile);

InputStream propertiesFileInputStream = new FileInputStream(file);
ParameterTool parameters = ParameterTool.fromPropertiesFile(propertiesFileInputStream);

```

`String propertiesFilePath = "/home/sam/flink/myjob.properties";
ParameterTool parameters = ParameterTool.fromPropertiesFile(propertiesFilePath);

File propertiesFile = new File(propertiesFilePath);
ParameterTool parameters = ParameterTool.fromPropertiesFile(propertiesFile);

InputStream propertiesFileInputStream = new FileInputStream(file);
ParameterTool parameters = ParameterTool.fromPropertiesFile(propertiesFileInputStream);
`

#### From the command line arguments#


This allows getting arguments like --input hdfs:///mydata --elements 42 from the command line.

`--input hdfs:///mydata --elements 42`

```
public static void main(String[] args) {
    ParameterTool parameters = ParameterTool.fromArgs(args);
    // .. regular code ..

```

`public static void main(String[] args) {
    ParameterTool parameters = ParameterTool.fromArgs(args);
    // .. regular code ..
`

#### From system properties#


When starting a JVM, you can pass system properties to it: -Dinput=hdfs:///mydata. You can also initialize the ParameterTool from these system properties:

`-Dinput=hdfs:///mydata`
`ParameterTool`

```
ParameterTool parameters = ParameterTool.fromSystemProperties();

```

`ParameterTool parameters = ParameterTool.fromSystemProperties();
`

### Using the parameters in your Flink program#


Now that we’ve got the parameters from somewhere (see above) we can use them in various ways.


Directly from the ParameterTool

`ParameterTool`

The ParameterTool itself has methods for accessing the values.

`ParameterTool`

```
ParameterTool parameters = // ...
parameters.getRequired("input");
parameters.get("output", "myDefaultValue");
parameters.getLong("expectedCount", -1L);
parameters.getNumberOfParameters();
// .. there are more methods available.

```

`ParameterTool parameters = // ...
parameters.getRequired("input");
parameters.get("output", "myDefaultValue");
parameters.getLong("expectedCount", -1L);
parameters.getNumberOfParameters();
// .. there are more methods available.
`

You can use the return values of these methods directly in the main() method of the client submitting the application.
For example, you could set the parallelism of a operator like this:

`main()`

```
ParameterTool parameters = ParameterTool.fromArgs(args);
int parallelism = parameters.get("mapParallelism", 2);
DataStream<Tuple2<String, Integer>> counts = text.flatMap(new Tokenizer()).setParallelism(parallelism);

```

`ParameterTool parameters = ParameterTool.fromArgs(args);
int parallelism = parameters.get("mapParallelism", 2);
DataStream<Tuple2<String, Integer>> counts = text.flatMap(new Tokenizer()).setParallelism(parallelism);
`

Since the ParameterTool is serializable, you can pass it to the functions itself:

`ParameterTool`

```
ParameterTool parameters = ParameterTool.fromArgs(args);
DataStream<Tuple2<String, Integer>> counts = text.flatMap(new Tokenizer(parameters));

```

`ParameterTool parameters = ParameterTool.fromArgs(args);
DataStream<Tuple2<String, Integer>> counts = text.flatMap(new Tokenizer(parameters));
`

and then use it inside the function for getting values from the command line.


#### Register the parameters globally#


Parameters registered as global job parameters in the ExecutionConfig can be accessed as configuration values from the JobManager web interface and in all functions defined by the user.

`ExecutionConfig`

Register the parameters globally:


```
ParameterTool parameters = ParameterTool.fromArgs(args);

// set up the execution environment
final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
env.getConfig().setGlobalJobParameters(parameters);

```

`ParameterTool parameters = ParameterTool.fromArgs(args);

// set up the execution environment
final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
env.getConfig().setGlobalJobParameters(parameters);
`

Access them in any rich user function:


```
public static final class Tokenizer extends RichFlatMapFunction<String, Tuple2<String, Integer>> {

    @Override
    public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
	ParameterTool parameters = ParameterTool.fromMap(getRuntimeContext().getGlobalJobParameters());
	parameters.getRequired("input");
	// .. do more ..

```

`public static final class Tokenizer extends RichFlatMapFunction<String, Tuple2<String, Integer>> {

    @Override
    public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
	ParameterTool parameters = ParameterTool.fromMap(getRuntimeContext().getGlobalJobParameters());
	parameters.getRequired("input");
	// .. do more ..
`

 Back to top
