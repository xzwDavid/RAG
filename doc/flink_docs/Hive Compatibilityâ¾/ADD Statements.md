# ADD Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# ADD Statements#


With Hive dialect, the following ADD statements are supported for now:

`ADD`
* ADD JAR

## ADD JAR#


### Description#


ADD JAR statement is used to add user jars into the classpath.
Add multiple jars file in single ADD JAR statement is not supported.

`ADD JAR`
`ADD JAR`

### Syntax#


```
ADD JAR <jar_path>;

```

`ADD JAR <jar_path>;
`

### Parameters#

* 
jar_path
The path of the JAR file to be added. It could be either on a local file or distributed file system.


jar_path


The path of the JAR file to be added. It could be either on a local file or distributed file system.


### Examples#


```
-- add a local jar
ADD JAR t.jar;

-- add a remote jar
ADD JAR hdfs://namenode-host:port/path/t.jar

```

`-- add a local jar
ADD JAR t.jar;

-- add a remote jar
ADD JAR hdfs://namenode-host:port/path/t.jar
`