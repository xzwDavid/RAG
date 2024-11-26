# Test Dependencies


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Dependencies for Testing#


Flink provides utilities for testing your job that you can add as dependencies.


## DataStream API Testing#


You need to add the following dependencies if you want to develop tests for a job built with the
DataStream API:

`pom.xml`

```
&ltdependency>
    &ltgroupId>org.apache.flink</groupId>
    &ltartifactId>flink-test-utils</artifactId>
    &ltversion>2.0-SNAPSHOT</version>
    &ltscope>test</scope>
</dependency>
```

`&ltdependency>
    &ltgroupId>org.apache.flink</groupId>
    &ltartifactId>flink-test-utils</artifactId>
    &ltversion>2.0-SNAPSHOT</version>
    &ltscope>test</scope>
</dependency>`
`build.gradle`

```
testCompile "org.apache.flink:flink-test-utils:2.0-SNAPSHOT"
```

`testCompile "org.apache.flink:flink-test-utils:2.0-SNAPSHOT"`

Among the various test utilities, this module provides MiniCluster, a lightweight configurable Flink cluster runnable in a JUnit test that can directly execute jobs.

`MiniCluster`

For more information on how to use these utilities, check out the section on DataStream API testing


## Table API Testing#


If you want to test the Table API & SQL programs locally within your IDE, you can add the following
dependency, in addition to the aforementioned flink-test-utils:

`flink-test-utils`
`pom.xml`

```
&ltdependency>
    &ltgroupId>org.apache.flink</groupId>
    &ltartifactId>flink-table-test-utils</artifactId>
    &ltversion>2.0-SNAPSHOT</version>
    &ltscope>test</scope>
</dependency>
```

`&ltdependency>
    &ltgroupId>org.apache.flink</groupId>
    &ltartifactId>flink-table-test-utils</artifactId>
    &ltversion>2.0-SNAPSHOT</version>
    &ltscope>test</scope>
</dependency>`
`build.gradle`

```
testCompile "org.apache.flink:flink-table-test-utils:2.0-SNAPSHOT"
```

`testCompile "org.apache.flink:flink-table-test-utils:2.0-SNAPSHOT"`

This will automatically bring in the query planner and the runtime, required respectively to plan
and execute the queries.


> 
  The module flink-table-test-utils has been introduced in Flink 1.15 and is considered experimental.


`flink-table-test-utils`