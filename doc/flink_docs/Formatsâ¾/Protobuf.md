# Protobuf


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Protobuf Format#



Format: Serialization Schema
Format: Deserialization Schema


The Protocol Buffers Protobuf format allows you to read and write Protobuf data, based on Protobuf generated classes.


## Dependencies#


In order to use the Protobuf format the following
dependencies are required for both projects using a build automation tool (such as Maven or SBT)
and SQL Client with SQL JAR bundles.


```
&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-protobuf</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>
```

`&ltdependency>
  &ltgroupId>org.apache.flink</groupId>
  &ltartifactId>flink-protobuf</artifactId>
  &ltversion>2.0-SNAPSHOT</version>
</dependency>`

## How to create a table with Protobuf format#


Here is an example to create a table using the Kafka connector and Protobuf format.


Below is the proto definition file.


```
syntax = "proto2";
package com.example;
option java_package = "com.example";
option java_multiple_files = true;

message SimpleTest {
    optional int64 uid = 1;
    optional string name = 2;
    optional int32 category_type = 3;
    optional bytes content = 4;
    optional double price = 5;
    map<int64, InnerMessageTest> value_map = 6;
    repeated  InnerMessageTest value_arr = 7;
    optional Corpus corpus_int = 8; 
    optional Corpus corpus_str = 9; 
    
    message InnerMessageTest{
          optional int64 v1 =1;
          optional int32 v2 =2;
    }
    
    enum Corpus {
        UNIVERSAL = 0;
        WEB = 1;
        IMAGES = 2;
        LOCAL = 3;
        NEWS = 4;
        PRODUCTS = 5;
        VIDEO = 7;
      }
}

```

`syntax = "proto2";
package com.example;
option java_package = "com.example";
option java_multiple_files = true;

message SimpleTest {
    optional int64 uid = 1;
    optional string name = 2;
    optional int32 category_type = 3;
    optional bytes content = 4;
    optional double price = 5;
    map<int64, InnerMessageTest> value_map = 6;
    repeated  InnerMessageTest value_arr = 7;
    optional Corpus corpus_int = 8; 
    optional Corpus corpus_str = 9; 
    
    message InnerMessageTest{
          optional int64 v1 =1;
          optional int32 v2 =2;
    }
    
    enum Corpus {
        UNIVERSAL = 0;
        WEB = 1;
        IMAGES = 2;
        LOCAL = 3;
        NEWS = 4;
        PRODUCTS = 5;
        VIDEO = 7;
      }
}
`
1. Use protoc command to compile the .proto file to java classes
2. Then compile and package the classes (there is no need to package proto-java into the jar)
3. Finally you should provide the jar in your classpath, e.g. pass it using -j in sql-client
`protoc`
`.proto`
`jar`
`-j`

```
CREATE TABLE simple_test (
  uid BIGINT,
  name STRING,
  category_type INT,
  content BINARY,
  price DOUBLE,
  value_map map<BIGINT, row<v1 BIGINT, v2 INT>>,
  value_arr array<row<v1 BIGINT, v2 INT>>,
  corpus_int INT,
  corpus_str STRING
) WITH (
 'connector' = 'kafka',
 'topic' = 'user_behavior',
 'properties.bootstrap.servers' = 'localhost:9092',
 'properties.group.id' = 'testGroup',
 'format' = 'protobuf',
 'protobuf.message-class-name' = 'com.example.SimpleTest',
 'protobuf.ignore-parse-errors' = 'true'
)

```

`CREATE TABLE simple_test (
  uid BIGINT,
  name STRING,
  category_type INT,
  content BINARY,
  price DOUBLE,
  value_map map<BIGINT, row<v1 BIGINT, v2 INT>>,
  value_arr array<row<v1 BIGINT, v2 INT>>,
  corpus_int INT,
  corpus_str STRING
) WITH (
 'connector' = 'kafka',
 'topic' = 'user_behavior',
 'properties.bootstrap.servers' = 'localhost:9092',
 'properties.group.id' = 'testGroup',
 'format' = 'protobuf',
 'protobuf.message-class-name' = 'com.example.SimpleTest',
 'protobuf.ignore-parse-errors' = 'true'
)
`

## Format Options#


##### format

`'protobuf'`

##### protobuf.message-class-name

`$`

##### protobuf.ignore-parse-errors


##### protobuf.read-default-values


##### protobuf.write-null-string-literal


## Data Type Mapping#


The following table lists the type mapping from Flink type to Protobuf type.

`CHAR / VARCHAR / STRING`
`string`
`BOOLEAN`
`bool`
`BINARY / VARBINARY`
`bytes`
`INT`
`int32`
`BIGINT`
`int64`
`FLOAT`
`float`
`DOUBLE`
`double`
`ARRAY`
`repeated`
`write-null-string-literal`
`MAP`
`map`
`write-null-string-literal`
`ROW`
`message`
`VARCHAR / CHAR / TINYINT / SMALLINT / INTEGER / BIGINT`
`enum`
`ROW<seconds BIGINT, nanos INT>`
`google.protobuf.timestamp`

## Null Values#


As protobuf does not permit null values in maps and array, we need to auto-generate default values when converting from Flink Rows to Protobuf.


## OneOf field#


In the serialization process, there’s no guarantee that the Flink fields of the same one-of group only contain at most one valid value.
When serializing, each field is set in the order of Flink schema, so the field in the higher position will override the field in lower position in the same one-of group.


You can refer to Language Guide (proto2) or Language Guide (proto3) for more information about Protobuf types.
