# JAR Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# JAR Statements#


JAR statements are used to add user jars into the classpath or remove user jars from the classpath
or show added jars in the classpath in the runtime.


Flink SQL supports the following JAR statements for now:

* ADD JAR
* SHOW JARS
* REMOVE JAR

## Run a JAR statement#

`JAR`

```
Flink SQL> ADD JAR '/path/hello.jar';
[INFO] Execute statement succeeded.

Flink SQL> ADD JAR 'hdfs:///udf/common-udf.jar';
[INFO] Execute statement succeeded.

Flink SQL> SHOW JARS;
+----------------------------+
|                       jars |
+----------------------------+
|            /path/hello.jar |
| hdfs:///udf/common-udf.jar |
+----------------------------+

Flink SQL> REMOVE JAR '/path/hello.jar';
[INFO] The specified jar is removed from session classloader.

```

`Flink SQL> ADD JAR '/path/hello.jar';
[INFO] Execute statement succeeded.

Flink SQL> ADD JAR 'hdfs:///udf/common-udf.jar';
[INFO] Execute statement succeeded.

Flink SQL> SHOW JARS;
+----------------------------+
|                       jars |
+----------------------------+
|            /path/hello.jar |
| hdfs:///udf/common-udf.jar |
+----------------------------+

Flink SQL> REMOVE JAR '/path/hello.jar';
[INFO] The specified jar is removed from session classloader.
`

## ADD JAR#


```
ADD JAR '<path_to_filename>.jar'

```

`ADD JAR '<path_to_filename>.jar'
`

Add a JAR file to the list of resources, it supports adding the jar locates in a local or remote file system. The added JAR file can be listed using SHOW JARS statements.

`SHOW JARS`

### Limitation#


Please don’t use ADD JAR statements to load Hive source/sink/function/catalog. This is a known limitation of Hive connector and will be fixed in the future version. Currently, it’s recommended to follow this instruction to setup Hive integration.

`ADD JAR`

## SHOW JARS#


```
SHOW JARS

```

`SHOW JARS
`

Show all added jars which are added by ADD JAR statements.

`ADD JAR`

## REMOVE JAR#


```
REMOVE JAR '<path_to_filename>.jar'

```

`REMOVE JAR '<path_to_filename>.jar'
`

Remove the specified jar that is added by the ADD JAR statements.

`ADD JAR`

Attention REMOVE JAR statements only work in SQL CLI.


 Back to top
