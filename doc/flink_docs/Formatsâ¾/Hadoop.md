# Hadoop


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Hadoop formats#


## Project Configuration#


Support for Hadoop is contained in the flink-hadoop-compatibility
Maven module.

`flink-hadoop-compatibility`

Add the following dependency to your pom.xml to use hadoop

`pom.xml`

```
<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-hadoop-compatibility</artifactId>
	<version>2.0-SNAPSHOT</version>
</dependency>

```

`<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-hadoop-compatibility</artifactId>
	<version>2.0-SNAPSHOT</version>
</dependency>
`

If you want to run your Flink application locally (e.g. from your IDE), you also need to add
a hadoop-client dependency such as:

`hadoop-client`

```
<dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-client</artifactId>
    <version>2.10.2</version>
    <scope>provided</scope>
</dependency>

```

`<dependency>
    <groupId>org.apache.hadoop</groupId>
    <artifactId>hadoop-client</artifactId>
    <version>2.10.2</version>
    <scope>provided</scope>
</dependency>
`

## Using Hadoop InputFormats#


To use Hadoop InputFormats with Flink the format must first be wrapped
using either readHadoopFile or createHadoopInput of the
HadoopInputs utility class.
The former is used for input formats derived
from FileInputFormat while the latter has to be used for general purpose
input formats.
The resulting InputFormat can be used to create a data source by using
ExecutionEnvironment#createInput.

`InputFormats`
`readHadoopFile`
`createHadoopInput`
`HadoopInputs`
`FileInputFormat`
`InputFormat`
`ExecutionEnvironment#createInput`

The resulting DataStream contains 2-tuples where the first field
is the key and the second field is the value retrieved from the Hadoop
InputFormat.

`DataStream`

The following example shows how to use Hadoop’s TextInputFormat.

`TextInputFormat`

```
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
KeyValueTextInputFormat textInputFormat = new KeyValueTextInputFormat();

DataStream<Tuple2<Text, Text>> input = env.createInput(HadoopInputs.readHadoopFile(
  textInputFormat, Text.class, Text.class, textPath));

// Do something with the data.
[...]

```

`StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
KeyValueTextInputFormat textInputFormat = new KeyValueTextInputFormat();

DataStream<Tuple2<Text, Text>> input = env.createInput(HadoopInputs.readHadoopFile(
  textInputFormat, Text.class, Text.class, textPath));

// Do something with the data.
[...]
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment
val textInputFormat = new KeyValueTextInputFormat
val input: DataStream[(Text, Text)] =
  env.createInput(HadoopInputs.readHadoopFile(
    textInputFormat, classOf[Text], classOf[Text], textPath))

// Do something with the data.
[...]

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment
val textInputFormat = new KeyValueTextInputFormat
val input: DataStream[(Text, Text)] =
  env.createInput(HadoopInputs.readHadoopFile(
    textInputFormat, classOf[Text], classOf[Text], textPath))

// Do something with the data.
[...]
`

 Back to top
