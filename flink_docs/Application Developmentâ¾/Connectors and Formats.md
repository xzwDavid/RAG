# Connectors and Formats


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Connectors and Formats#


Flink applications can read from and write to various external systems via connectors.
It supports multiple formats in order to encode and decode data to match Flink’s data structures.


An overview of available connectors and formats is available for both
DataStream and
Table API/SQL.


## Available artifacts#


In order to use connectors and formats, you need to make sure Flink has access to the artifacts implementing them.
For each connector supported by the Flink community, we publish two artifacts on Maven Central:

* flink-connector-<NAME> which is a thin JAR including only the connector code, but excluding eventual third-party dependencies
* flink-sql-connector-<NAME> which is an uber JAR ready to use with all the connector third-party dependencies
`flink-connector-<NAME>`
`flink-sql-connector-<NAME>`

The same applies for formats as well. Note that some connectors may not have a corresponding
flink-sql-connector-<NAME> artifact because they do not require third-party dependencies.

`flink-sql-connector-<NAME>`

> 
  The uber/fat JARs are supported mostly for being used in conjunction with the SQL client,
but you can also use them in any DataStream/Table application.



## Using artifacts#


In order to use a connector/format module, you can either:

* Shade the thin JAR and its transitive dependencies in your job JAR
* Shade the uber JAR in your job JAR
* Copy the uber JAR directly in the /lib folder of the Flink distribution
`/lib`

For shading dependencies, check out the specific Maven
and Gradle guides.
For a reference about the Flink distribution, check Anatomy of the Flink distribution.


> 
  Deciding whether to shade the uber JAR, the thin JAR or just include the dependency in the distribution is up to you and your use case.
If you shade a dependency, you will have more control over the dependency version in the job JAR.
In case of shading the thin JAR, you will have even more control over the transitive dependencies,
since you can change the versions without changing the connector version (binary compatibility permitting).
In case of embedding the connector uber JAR directly in the Flink distribution /lib folder,
you will be able to control in one place connector versions for all jobs.


`/lib`