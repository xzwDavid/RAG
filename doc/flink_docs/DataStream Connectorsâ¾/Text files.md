# Text files


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Text files format#


Flink supports reading from text lines from a file using TextLineInputFormat. This format uses Java’s built-in InputStreamReader to decode the byte stream using various supported charset encodings.
To use the format you need to add the Flink Connector Files dependency to your project:

`TextLineInputFormat`

```
<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-connector-files</artifactId>
	<version>2.0-SNAPSHOT</version>
</dependency>

```

`<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-connector-files</artifactId>
	<version>2.0-SNAPSHOT</version>
</dependency>
`

For PyFlink users, you could use it directly in your jobs.


This format is compatible with the new Source that can be used in both batch and streaming modes.
Thus, you can use this format in two ways:

* Bounded read for batch mode
* Continuous read for streaming mode: monitors a directory for new files that appear

Bounded read example:


In this example we create a DataStream containing the lines of a text file as Strings.
There is no need for a watermark strategy as records do not contain event timestamps.


```
final FileSource<String> source =
  FileSource.forRecordStreamFormat(new TextLineInputFormat(), /* Flink Path */)
  .build();
final DataStream<String> stream =
  env.fromSource(source, WatermarkStrategy.noWatermarks(), "file-source");

```

`final FileSource<String> source =
  FileSource.forRecordStreamFormat(new TextLineInputFormat(), /* Flink Path */)
  .build();
final DataStream<String> stream =
  env.fromSource(source, WatermarkStrategy.noWatermarks(), "file-source");
`

```
source = FileSource.for_record_stream_format(StreamFormat.text_line_format(), *path).build()
stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "file-source")

```

`source = FileSource.for_record_stream_format(StreamFormat.text_line_format(), *path).build()
stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "file-source")
`

Continuous read example:
In this example, we create a DataStream containing the lines of text files as Strings that will infinitely grow
as new files are added to the directory. We monitor for new files each second.
There is no need for a watermark strategy as records do not contain event timestamps.


```
final FileSource<String> source =
    FileSource.forRecordStreamFormat(new TextLineInputFormat(), /* Flink Path */)
  .monitorContinuously(Duration.ofSeconds(1L))
  .build();
final DataStream<String> stream =
  env.fromSource(source, WatermarkStrategy.noWatermarks(), "file-source");

```

`final FileSource<String> source =
    FileSource.forRecordStreamFormat(new TextLineInputFormat(), /* Flink Path */)
  .monitorContinuously(Duration.ofSeconds(1L))
  .build();
final DataStream<String> stream =
  env.fromSource(source, WatermarkStrategy.noWatermarks(), "file-source");
`

```
source = FileSource \
    .for_record_stream_format(StreamFormat.text_line_format(), *path) \
    .monitor_continously(Duration.of_seconds(1)) \
    .build()
stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "file-source")

```

`source = FileSource \
    .for_record_stream_format(StreamFormat.text_line_format(), *path) \
    .monitor_continously(Duration.of_seconds(1)) \
    .build()
stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "file-source")
`