# OLAP Quickstart


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# OLAP Quickstart#


OLAP (OnLine Analysis Processing) is a key technology in the field of data analysis, it is generally used to perform complex queries on large data sets with latencies in seconds. Now Flink can not only support streaming and batch computing, but also supports users to deploy it as an OLAP computing service. This page will show you how to quickly set up a local Flink OLAP service, and will also introduce some best practices helping you deploy Flink OLAP service in production.


## Architecture Introduction#


This chapter will introduce you to the overall architecture of Flink OLAP service and the advantages of using it.


### Architecture#


Flink OLAP service consists of three parts: Client, Flink SQL Gateway and Flink Session Cluster.

* Client: Could be any client that can interact with Flink SQL Gateway, such as SQL Client, Flink JDBC Driver and so on.
* Flink SQL Gateway: The SQL Gateway provides an easy way to parse the sql query, look up the metadata, analyze table stats, optimize the plan and submit JobGraphs to cluster.
* Flink Session Cluster: OLAP queries run on session cluster, mainly to avoid the overhead of cluster startup.

### Advantage#

* Massively Parallel Processing

Flink OLAP runs naturally as a massively parallel processing system, which enables planners to easily adjust the job parallelism to fulfill queries’ latency requirement under different data sizes.


* Elastic Resource Management

Flink’s resource management supports min/max scaling, which means the session cluster can allocate the resource according to workload dynamically.


* Reuse Connectors

Flink OLAP can reuse the rich Connectors in Flink ecosystem.


* Unified Engine

Unified computing engine for Streaming/Batch/OLAP.


* Flink OLAP runs naturally as a massively parallel processing system, which enables planners to easily adjust the job parallelism to fulfill queries’ latency requirement under different data sizes.
* Flink’s resource management supports min/max scaling, which means the session cluster can allocate the resource according to workload dynamically.
* Flink OLAP can reuse the rich Connectors in Flink ecosystem.
* Unified computing engine for Streaming/Batch/OLAP.

## Deploying in Local Mode#


In this chapter, you will learn how to build Flink OLAP services locally.


### Downloading Flink#


The same as Local Installation. Flink runs on all UNIX-like environments, i.e. Linux, Mac OS X, and Cygwin (for Windows). User need to have at Java 11 installed. To check the Java version installed, user can type in the terminal:


```
java -version

```

`java -version
`

Next, Download the latest binary release of Flink, then extract the archive:


```
tar -xzf flink-*.tgz

```

`tar -xzf flink-*.tgz
`

### Starting a local cluster#


To start a local cluster, run the bash script that comes with Flink:


```
./bin/start-cluster.sh

```

`./bin/start-cluster.sh
`

You should be able to navigate to the web UI at http://localhost:8081 to view the Flink dashboard and see that the cluster is up and running.


### Start a SQL Client CLI#


You can start the CLI with an embedded gateway by calling:


```
./bin/sql-client.sh

```

`./bin/sql-client.sh
`

### Running Queries#


You could simply execute queries in CLI and retrieve the results.


```
SET 'sql-client.execution.result-mode' = 'tableau';

CREATE TABLE Orders (
    order_number BIGINT,
    price        DECIMAL(32,2),
    buyer        ROW<first_name STRING, last_name STRING>,
    order_time   TIMESTAMP(3)
) WITH (
  'connector' = 'datagen',
  'number-of-rows' = '100000'
);

SELECT buyer, SUM(price) AS total_cost
FROM Orders
GROUP BY  buyer
ORDER BY  total_cost LIMIT 3;

```

`SET 'sql-client.execution.result-mode' = 'tableau';

CREATE TABLE Orders (
    order_number BIGINT,
    price        DECIMAL(32,2),
    buyer        ROW<first_name STRING, last_name STRING>,
    order_time   TIMESTAMP(3)
) WITH (
  'connector' = 'datagen',
  'number-of-rows' = '100000'
);

SELECT buyer, SUM(price) AS total_cost
FROM Orders
GROUP BY  buyer
ORDER BY  total_cost LIMIT 3;
`

And then you could find job detail information in web UI at http://localhost:8081.


## Deploying in Production#


This section guides you through setting up a production ready Flink OLAP service.


### Client#


#### Flink JDBC Driver#


You should use Flink JDBC Driver when submitting queries to SQL Gateway since it provides low-level connection management. When used in production, you should pay attention to reuse the JDBC connection to avoid frequently creating/closing sessions in the Gateway and then reduce the E2E query latency. For detailed information, please refer to the [Flink JDBC Driver]({{ <ref “docs/dev/table/jdbcDriver”> }}).


### Cluster Deployment#


In production, you should use Flink Session Cluster, Flink SQL Gateway to build an OLAP service.


#### Session Cluster#


For Flink Session Cluster, you can deploy it on Native Kubernetes using session mode. Kubernetes is a popular container-orchestration system for automating computer application deployment, scaling, and management. By deploying on Native Kubernetes, Flink Session Cluster is able to dynamically allocate and de-allocate TaskManagers. For more information, please refer to [Native Kubernetes]({{ < ref “docs/deployment/resource-providers/native_kubernetes”> }}). Furthermore, you can config the option slotmanager.number-of-slots.min in session cluster. This will help you significantly reduce the cold start time of your query. For detailed information, please refer to FLIP-362.


#### SQL Gateway#


For Flink SQL Gateway, you should deploy it as a stateless microservice and register the instance on service discovery component. Through this way, client can balance the query between instances easily. For more information, please refer to SQL Gateway Overview.


### Datasource Configurations#


#### Catalogs#


In OLAP scenario, you should configure FileCatalogStore provided by Catalogs as the catalog used by cluster. As a long-running service, Flink OLAP cluster’s catalog information will not change frequently and should be re-used cross sessions to reduce the cold-start cost. For more information, please refer to the Catalog Store.

`FileCatalogStore`

#### Connectors#


Both Session Cluster and SQL Gateway rely on connectors to analyze table stats and read data from the configured data source. To add connectors, please refer to the Connectors.


### Recommended Cluster Configurations#


In OLAP scenario, appropriate configurations that can greatly help users improve the overall usability and query performance. Here are some recommended production configurations:


#### SQL&Table Options#


#### Runtime Options#


Using JDK17 within ZGC can greatly help optimize the metaspace garbage collection issue, detailed information can be found in FLINK-32746. Meanwhile, ZGC can provide close to zero application pause time when collecting garbage objects in memory. Additionally, OLAP queries need to be executed in BATCH mode because both Pipelined and Blocking edges may appear in the execution plan of an OLAP query. Batch scheduler allows queries to be scheduled in stages, which could avoid scheduling deadlocks in this scenario.

`BATCH`
`Pipelined`
`Blocking`

#### Scheduling Options#


#### Network Options#


#### ResourceManager Options#


You can configure slotmanager.number-of-slots.min to a proper value as the reserved resource pool serving OLAP queries. TaskManager should configure with a large resource specification in OLAP scenario since this can put more computations in local and reduce network/deserialization/serialization overhead. Meanwhile, as a single point of calculation in OLAP, JobManager also prefer large resource specification.

`slotmanager.number-of-slots.min`

## Future Work#


Flink OLAP is now part of Apache Flink Roadmap, which means the community will keep putting efforts to improve Flink OLAP, both in usability and query performance. Relevant work are traced in underlying tickets:

* https://issues.apache.org/jira/browse/FLINK-25318
* https://issues.apache.org/jira/browse/FLINK-32898