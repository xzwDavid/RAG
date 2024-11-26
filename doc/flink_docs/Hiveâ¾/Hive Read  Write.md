# Hive Read & Write


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Hive Read & Write#


Using the HiveCatalog, Apache Flink can be used for unified BATCH and STREAM processing of Apache
Hive Tables. This means Flink can be used as a more performant alternative to Hiveâs batch engine,
or to continuously read and write data into and out of Hive tables to power real-time data
warehousing applications.

`HiveCatalog`
`BATCH`
`STREAM`

## Reading#


Flink supports reading data from Hive in both BATCH and STREAMING modes. When run as a BATCH
application, Flink will execute its query over the state of the table at the point in time when the
query is executed. STREAMING reads will continuously monitor the table and incrementally fetch
new data as it is made available. Flink will read tables as bounded by default.

`BATCH`
`STREAMING`
`BATCH`
`STREAMING`

STREAMING reads support consuming both partitioned and non-partitioned tables.
For partitioned tables, Flink will monitor the generation of new partitions, and read
them incrementally when available. For non-partitioned tables, Flink will monitor the generation
of new files in the folder and read new files incrementally.

`STREAMING`

##### streaming-source.enable


##### streaming-source.partition.include


##### streaming-source.monitor-interval


##### streaming-source.partition-order


##### streaming-source.consume-start-offset


SQL Hints can be used to apply configurations to a Hive table
without changing its definition in the Hive metastore.


```

SELECT * 
FROM hive_table 
/*+ OPTIONS('streaming-source.enable'='true', 'streaming-source.consume-start-offset'='2020-05-20') */;

```

`
SELECT * 
FROM hive_table 
/*+ OPTIONS('streaming-source.enable'='true', 'streaming-source.consume-start-offset'='2020-05-20') */;
`

Notes

* Monitor strategy is to scan all directories/files currently in the location path. Many partitions may cause performance degradation.
* Streaming reads for non-partitioned tables requires that each file be written atomically into the target directory.
* Streaming reading for partitioned tables requires that each partition should be added atomically in the view of hive metastore. If not, new data added to an existing partition will be consumed.
* Streaming reads do not support watermark grammar in Flink DDL. These tables cannot be used for window operators.

### Reading Hive Views#


Flink is able to read from Hive defined views, but some limitations apply:

1. 
The Hive catalog must be set as the current catalog before you can query the view.
This can be done by either tableEnv.useCatalog(...) in Table API or USE CATALOG ... in SQL Client.

2. 
Hive and Flink SQL have different syntax, e.g. different reserved keywords and literals.
Make sure the viewâs query is compatible with Flink grammar.


The Hive catalog must be set as the current catalog before you can query the view.
This can be done by either tableEnv.useCatalog(...) in Table API or USE CATALOG ... in SQL Client.

`tableEnv.useCatalog(...)`
`USE CATALOG ...`

Hive and Flink SQL have different syntax, e.g. different reserved keywords and literals.
Make sure the viewâs query is compatible with Flink grammar.


### Vectorized Optimization upon Read#


Flink will automatically used vectorized reads of Hive tables when the following conditions are met:

* Format: ORC or Parquet.
* Columns without complex data type, like hive types: List, Map, Struct, Union.

This feature is enabled by default.
It may be disabled with the following configuration.


```
table.exec.hive.fallback-mapred-reader=true

```

`table.exec.hive.fallback-mapred-reader=true
`

### Source Parallelism Inference#


By default, Flink will infer the optimal parallelism for its Hive readers
based on the number of files, and number of blocks in each file.


Flink allows you to flexibly configure the policy of parallelism inference. You can configure the
following parameters in TableConfig (note that these parameters affect all sources of the job):

`TableConfig`

##### table.exec.hive.infer-source-parallelism.mode


##### table.exec.hive.infer-source-parallelism.max


### Tuning Split Size While Reading Hive Table#


While reading Hive table, the data files will be enumerated into splits, one of which is a portion of data consumed by the source.
Splits are granularity by which the source distributes the work and parallelize the data reading.
Users can do some performance tuning by tuning the split’s size with the follow configurations.


##### table.exec.hive.split-max-size


##### table.exec.hive.file-open-cost


> 
NOTE:

To tune the split’s size, Flink will first get all files’ size for all partitions.
If there are too many partitions, it maybe time-consuming,
then you can configure the job configuration table.exec.hive.calculate-partition-size.thread-num (3 by default) to a bigger value to enable more threads to speed up the process.
Currently, these configurations for tuning split size only works for the Hive table stored as ORC format.




NOTE:

* To tune the split’s size, Flink will first get all files’ size for all partitions.
If there are too many partitions, it maybe time-consuming,
then you can configure the job configuration table.exec.hive.calculate-partition-size.thread-num (3 by default) to a bigger value to enable more threads to speed up the process.
* Currently, these configurations for tuning split size only works for the Hive table stored as ORC format.
`table.exec.hive.calculate-partition-size.thread-num`

### Read Table Statistics#


When the table statistic is not available from the Hive metastore, Flink will try to scan the table to get the statistic to generate a better execution plan. It may cost some time to get the statistic. To get it faster, you can use table.exec.hive.read-statistics.thread-num to configure how many threads to use to scan the table.
The default value is the number of available processors in the current system and the configured value should be bigger than 0.

`table.exec.hive.read-statistics.thread-num`

### Load Partition Splits#


Multi-thread is used to split hive’s partitions. You can use table.exec.hive.load-partition-splits.thread-num to configure the thread number. The default value is 3 and the configured value should be bigger than 0.

`table.exec.hive.load-partition-splits.thread-num`

### Read Partition With Subdirectory#


In some case, you may create an external table referring another table, but the partition columns is a subset of the referred table.
For example, you have a partitioned table fact_tz with partition day and hour:

`fact_tz`
`day`
`hour`

```
CREATE TABLE fact_tz(x int) PARTITIONED BY (day STRING, hour STRING);

```

`CREATE TABLE fact_tz(x int) PARTITIONED BY (day STRING, hour STRING);
`

And you have an external table fact_daily referring to table fact_tz with a coarse-grained partition day:

`fact_daily`
`fact_tz`
`day`

```
CREATE EXTERNAL TABLE fact_daily(x int) PARTITIONED BY (ds STRING) LOCATION '/path/to/fact_tz';

```

`CREATE EXTERNAL TABLE fact_daily(x int) PARTITIONED BY (ds STRING) LOCATION '/path/to/fact_tz';
`

Then when reading the external table fact_daily, there will be sub-directories (hour=1 to hour=24) in the partition directory of the table.

`fact_daily`
`hour=1`
`hour=24`

By default, you can add partition with sub-directories to the external table. Flink SQL can recursively scan all sub-directories and fetch all the data from all sub-directories.


```
ALTER TABLE fact_daily ADD PARTITION (ds='2022-07-07') location '/path/to/fact_tz/ds=2022-07-07';

```

`ALTER TABLE fact_daily ADD PARTITION (ds='2022-07-07') location '/path/to/fact_tz/ds=2022-07-07';
`

You can set job configuration table.exec.hive.read-partition-with-subdirectory.enabled (true by default) to false to disallow Flink to read the sub-directories.
If the configuration is false and the directory does not contain files, rather consists of sub directories Flink blows up with the exception: java.io.IOException: Not a file: /path/to/data/*.

`table.exec.hive.read-partition-with-subdirectory.enabled`
`true`
`false`
`false`
`java.io.IOException: Not a file: /path/to/data/*`

## Temporal Table Join#


You can use a Hive table as a temporal table, and then a stream can correlate the Hive table by temporal join.
Please see temporal join for more information about the temporal join.


Flink supports processing-time temporal join Hive Table, the processing-time temporal join always joins the latest version of temporal table.
Flink supports temporal join both partitioned table and Hive non-partitioned table, for partitioned table, Flink supports tracking the latest partition of Hive table automatically.


NOTE: Flink does not support event-time temporal join Hive table yet.


### Temporal Join The Latest Partition#


For a partitioned table which is changing over time, we can read it out as an unbounded stream, the partition can be acted as a version of the temporal table if every partition contains complete data of a version,
the version of temporal table keeps the data of the partition.


Flink supports tracking the latest partition (version) of temporal table automatically in processing time temporal join, the latest partition (version) is defined by ‘streaming-source.partition-order’ option,
This is the most common user cases that use Hive table as dimension table in a Flink stream application job.


NOTE: This feature is only supported in Flink STREAMING Mode.

`STREAMING`

The following demo shows a classical business pipeline, the dimension table comes from Hive and it’s updated once every day by a batch pipeline job or a Flink job, the kafka stream comes from real time online business data or log and need to join with the dimension table to enrich stream.


```
-- Assume the data in hive table is updated per day, every day contains the latest and complete dimension data
SET table.sql-dialect=hive;
CREATE TABLE dimension_table (
  product_id STRING,
  product_name STRING,
  unit_price DECIMAL(10, 4),
  pv_count BIGINT,
  like_count BIGINT,
  comment_count BIGINT,
  update_time TIMESTAMP(3),
  update_user STRING,
  ...
) PARTITIONED BY (pt_year STRING, pt_month STRING, pt_day STRING) TBLPROPERTIES (
  -- using default partition-name order to load the latest partition every 12h (the most recommended and convenient way)
  'streaming-source.enable' = 'true',
  'streaming-source.partition.include' = 'latest',
  'streaming-source.monitor-interval' = '12 h',
  'streaming-source.partition-order' = 'partition-name',  -- option with default value, can be ignored.

  -- using partition file create-time order to load the latest partition every 12h
  'streaming-source.enable' = 'true',
  'streaming-source.partition.include' = 'latest',
  'streaming-source.partition-order' = 'create-time',
  'streaming-source.monitor-interval' = '12 h'

  -- using partition-time order to load the latest partition every 12h
  'streaming-source.enable' = 'true',
  'streaming-source.partition.include' = 'latest',
  'streaming-source.monitor-interval' = '12 h',
  'streaming-source.partition-order' = 'partition-time',
  'partition.time-extractor.kind' = 'default',
  'partition.time-extractor.timestamp-pattern' = '$pt_year-$pt_month-$pt_day 00:00:00' 
);

SET table.sql-dialect=default;
CREATE TABLE orders_table (
  order_id STRING,
  order_amount DOUBLE,
  product_id STRING,
  log_ts TIMESTAMP(3),
  proctime as PROCTIME()
) WITH (...);


-- streaming sql, kafka temporal join a hive dimension table. Flink will automatically reload data from the
-- configured latest partition in the interval of 'streaming-source.monitor-interval'.

SELECT * FROM orders_table AS o 
JOIN dimension_table FOR SYSTEM_TIME AS OF o.proctime AS dim
ON o.product_id = dim.product_id;

```

`-- Assume the data in hive table is updated per day, every day contains the latest and complete dimension data
SET table.sql-dialect=hive;
CREATE TABLE dimension_table (
  product_id STRING,
  product_name STRING,
  unit_price DECIMAL(10, 4),
  pv_count BIGINT,
  like_count BIGINT,
  comment_count BIGINT,
  update_time TIMESTAMP(3),
  update_user STRING,
  ...
) PARTITIONED BY (pt_year STRING, pt_month STRING, pt_day STRING) TBLPROPERTIES (
  -- using default partition-name order to load the latest partition every 12h (the most recommended and convenient way)
  'streaming-source.enable' = 'true',
  'streaming-source.partition.include' = 'latest',
  'streaming-source.monitor-interval' = '12 h',
  'streaming-source.partition-order' = 'partition-name',  -- option with default value, can be ignored.

  -- using partition file create-time order to load the latest partition every 12h
  'streaming-source.enable' = 'true',
  'streaming-source.partition.include' = 'latest',
  'streaming-source.partition-order' = 'create-time',
  'streaming-source.monitor-interval' = '12 h'

  -- using partition-time order to load the latest partition every 12h
  'streaming-source.enable' = 'true',
  'streaming-source.partition.include' = 'latest',
  'streaming-source.monitor-interval' = '12 h',
  'streaming-source.partition-order' = 'partition-time',
  'partition.time-extractor.kind' = 'default',
  'partition.time-extractor.timestamp-pattern' = '$pt_year-$pt_month-$pt_day 00:00:00' 
);

SET table.sql-dialect=default;
CREATE TABLE orders_table (
  order_id STRING,
  order_amount DOUBLE,
  product_id STRING,
  log_ts TIMESTAMP(3),
  proctime as PROCTIME()
) WITH (...);


-- streaming sql, kafka temporal join a hive dimension table. Flink will automatically reload data from the
-- configured latest partition in the interval of 'streaming-source.monitor-interval'.

SELECT * FROM orders_table AS o 
JOIN dimension_table FOR SYSTEM_TIME AS OF o.proctime AS dim
ON o.product_id = dim.product_id;
`

### Temporal Join The Latest Table#


For a Hive table, we can read it out as a bounded stream. In this case, the Hive table can only track its latest version at the time when we query.
The latest version of table keep all data of the Hive table.


When performing the temporal join the latest Hive table, the Hive table will be cached in Slot memory and each record from the stream is joined against the table by key to decide whether a match is found.
Using the latest Hive table as a temporal table does not require any additional configuration. Optionally, you can configure the TTL of the Hive table cache with the following property. After the cache expires, the Hive table will be scanned again to load the latest data.


##### lookup.join.cache.ttl


The following demo shows load all data of hive table as a temporal table.


```
-- Assume the data in hive table is overwrite by batch pipeline.
SET table.sql-dialect=hive;
CREATE TABLE dimension_table (
  product_id STRING,
  product_name STRING,
  unit_price DECIMAL(10, 4),
  pv_count BIGINT,
  like_count BIGINT,
  comment_count BIGINT,
  update_time TIMESTAMP(3),
  update_user STRING,
  ...
) TBLPROPERTIES (
  'streaming-source.enable' = 'false',           -- option with default value, can be ignored.
  'streaming-source.partition.include' = 'all',  -- option with default value, can be ignored.
  'lookup.join.cache.ttl' = '12 h'
);

SET table.sql-dialect=default;
CREATE TABLE orders_table (
  order_id STRING,
  order_amount DOUBLE,
  product_id STRING,
  log_ts TIMESTAMP(3),
  proctime as PROCTIME()
) WITH (...);


-- streaming sql, kafka join a hive dimension table. Flink will reload all data from dimension_table after cache ttl is expired.

SELECT * FROM orders_table AS o 
JOIN dimension_table FOR SYSTEM_TIME AS OF o.proctime AS dim
ON o.product_id = dim.product_id;

```

`-- Assume the data in hive table is overwrite by batch pipeline.
SET table.sql-dialect=hive;
CREATE TABLE dimension_table (
  product_id STRING,
  product_name STRING,
  unit_price DECIMAL(10, 4),
  pv_count BIGINT,
  like_count BIGINT,
  comment_count BIGINT,
  update_time TIMESTAMP(3),
  update_user STRING,
  ...
) TBLPROPERTIES (
  'streaming-source.enable' = 'false',           -- option with default value, can be ignored.
  'streaming-source.partition.include' = 'all',  -- option with default value, can be ignored.
  'lookup.join.cache.ttl' = '12 h'
);

SET table.sql-dialect=default;
CREATE TABLE orders_table (
  order_id STRING,
  order_amount DOUBLE,
  product_id STRING,
  log_ts TIMESTAMP(3),
  proctime as PROCTIME()
) WITH (...);


-- streaming sql, kafka join a hive dimension table. Flink will reload all data from dimension_table after cache ttl is expired.

SELECT * FROM orders_table AS o 
JOIN dimension_table FOR SYSTEM_TIME AS OF o.proctime AS dim
ON o.product_id = dim.product_id;
`

Note:

1. Each joining subtask needs to keep its own cache of the Hive table. Please make sure the Hive table can fit into the memory of a TM task slot.
2. It is encouraged to set a relatively large value both for streaming-source.monitor-interval(latest partition as temporal table) or lookup.join.cache.ttl(all partitions as temporal table). Otherwise, Jobs are prone to performance issues as the table needs to be updated and reloaded too frequently.
3. Currently we simply load the whole Hive table whenever the cache needs refreshing. There’s no way to differentiate
new data from the old.
`streaming-source.monitor-interval`
`lookup.join.cache.ttl`

## Writing#


Flink supports writing data from Hive in both BATCH and STREAMING modes. When run as a BATCH
application, Flink will write to a Hive table only making those records visible when the Job finishes.
BATCH writes support both appending to and overwriting existing tables.

`BATCH`
`STREAMING`
`BATCH`
`BATCH`

```
# ------ INSERT INTO will append to the table or partition, keeping the existing data intact ------ 
Flink SQL> INSERT INTO mytable SELECT 'Tom', 25;

# ------ INSERT OVERWRITE will overwrite any existing data in the table or partition ------ 
Flink SQL> INSERT OVERWRITE mytable SELECT 'Tom', 25;

```

`# ------ INSERT INTO will append to the table or partition, keeping the existing data intact ------ 
Flink SQL> INSERT INTO mytable SELECT 'Tom', 25;

# ------ INSERT OVERWRITE will overwrite any existing data in the table or partition ------ 
Flink SQL> INSERT OVERWRITE mytable SELECT 'Tom', 25;
`

Data can also be inserted into particular partitions.


```
# ------ Insert with static partition ------ 
Flink SQL> INSERT OVERWRITE myparttable PARTITION (my_type='type_1', my_date='2019-08-08') SELECT 'Tom', 25;

# ------ Insert with dynamic partition ------ 
Flink SQL> INSERT OVERWRITE myparttable SELECT 'Tom', 25, 'type_1', '2019-08-08';

# ------ Insert with static(my_type) and dynamic(my_date) partition ------ 
Flink SQL> INSERT OVERWRITE myparttable PARTITION (my_type='type_1') SELECT 'Tom', 25, '2019-08-08';

```

`# ------ Insert with static partition ------ 
Flink SQL> INSERT OVERWRITE myparttable PARTITION (my_type='type_1', my_date='2019-08-08') SELECT 'Tom', 25;

# ------ Insert with dynamic partition ------ 
Flink SQL> INSERT OVERWRITE myparttable SELECT 'Tom', 25, 'type_1', '2019-08-08';

# ------ Insert with static(my_type) and dynamic(my_date) partition ------ 
Flink SQL> INSERT OVERWRITE myparttable PARTITION (my_type='type_1') SELECT 'Tom', 25, '2019-08-08';
`

STREAMING writes continuously adding new data to Hive, committing records - making them
visible - incrementally. Users control when/how to trigger commits with several properties. Insert
overwrite is not supported for streaming write.

`STREAMING`

The below examples show how the streaming sink can be used to write a streaming query to write data from Kafka into a Hive table with partition-commit,
and runs a batch query to read that data back out.


Please see the streaming sink for a full list of available configurations.


```

SET table.sql-dialect=hive;
CREATE TABLE hive_table (
  user_id STRING,
  order_amount DOUBLE
) PARTITIONED BY (dt STRING, hr STRING) STORED AS parquet TBLPROPERTIES (
  'partition.time-extractor.timestamp-pattern'='$dt $hr:00:00',
  'sink.partition-commit.trigger'='partition-time',
  'sink.partition-commit.delay'='1 h',
  'sink.partition-commit.policy.kind'='metastore,success-file'
);

SET table.sql-dialect=default;
CREATE TABLE kafka_table (
  user_id STRING,
  order_amount DOUBLE,
  log_ts TIMESTAMP(3),
  WATERMARK FOR log_ts AS log_ts - INTERVAL '5' SECOND -- Define watermark on TIMESTAMP column
) WITH (...);

-- streaming sql, insert into hive table
INSERT INTO TABLE hive_table 
SELECT user_id, order_amount, DATE_FORMAT(log_ts, 'yyyy-MM-dd'), DATE_FORMAT(log_ts, 'HH')
FROM kafka_table;

-- batch sql, select with partition pruning
SELECT * FROM hive_table WHERE dt='2020-05-20' and hr='12';

```

`
SET table.sql-dialect=hive;
CREATE TABLE hive_table (
  user_id STRING,
  order_amount DOUBLE
) PARTITIONED BY (dt STRING, hr STRING) STORED AS parquet TBLPROPERTIES (
  'partition.time-extractor.timestamp-pattern'='$dt $hr:00:00',
  'sink.partition-commit.trigger'='partition-time',
  'sink.partition-commit.delay'='1 h',
  'sink.partition-commit.policy.kind'='metastore,success-file'
);

SET table.sql-dialect=default;
CREATE TABLE kafka_table (
  user_id STRING,
  order_amount DOUBLE,
  log_ts TIMESTAMP(3),
  WATERMARK FOR log_ts AS log_ts - INTERVAL '5' SECOND -- Define watermark on TIMESTAMP column
) WITH (...);

-- streaming sql, insert into hive table
INSERT INTO TABLE hive_table 
SELECT user_id, order_amount, DATE_FORMAT(log_ts, 'yyyy-MM-dd'), DATE_FORMAT(log_ts, 'HH')
FROM kafka_table;

-- batch sql, select with partition pruning
SELECT * FROM hive_table WHERE dt='2020-05-20' and hr='12';
`

If the watermark is defined on TIMESTAMP_LTZ column and used partition-time to commit, the sink.partition-commit.watermark-time-zone is required to set to the session time zone, otherwise the partition committed may happen after a few hours.

`partition-time`
`sink.partition-commit.watermark-time-zone`

```

SET table.sql-dialect=hive;
CREATE TABLE hive_table (
  user_id STRING,
  order_amount DOUBLE
) PARTITIONED BY (dt STRING, hr STRING) STORED AS parquet TBLPROPERTIES (
  'partition.time-extractor.timestamp-pattern'='$dt $hr:00:00',
  'sink.partition-commit.trigger'='partition-time',
  'sink.partition-commit.delay'='1 h',
  'sink.partition-commit.watermark-time-zone'='Asia/Shanghai', -- Assume user configured time zone is 'Asia/Shanghai'
  'sink.partition-commit.policy.kind'='metastore,success-file'
);

SET table.sql-dialect=default;
CREATE TABLE kafka_table (
  user_id STRING,
  order_amount DOUBLE,
  ts BIGINT, -- time in epoch milliseconds
  ts_ltz AS TO_TIMESTAMP_LTZ(ts, 3),
  WATERMARK FOR ts_ltz AS ts_ltz - INTERVAL '5' SECOND -- Define watermark on TIMESTAMP_LTZ column
) WITH (...);

-- streaming sql, insert into hive table
INSERT INTO TABLE hive_table 
SELECT user_id, order_amount, DATE_FORMAT(ts_ltz, 'yyyy-MM-dd'), DATE_FORMAT(ts_ltz, 'HH')
FROM kafka_table;

-- batch sql, select with partition pruning
SELECT * FROM hive_table WHERE dt='2020-05-20' and hr='12';

```

`
SET table.sql-dialect=hive;
CREATE TABLE hive_table (
  user_id STRING,
  order_amount DOUBLE
) PARTITIONED BY (dt STRING, hr STRING) STORED AS parquet TBLPROPERTIES (
  'partition.time-extractor.timestamp-pattern'='$dt $hr:00:00',
  'sink.partition-commit.trigger'='partition-time',
  'sink.partition-commit.delay'='1 h',
  'sink.partition-commit.watermark-time-zone'='Asia/Shanghai', -- Assume user configured time zone is 'Asia/Shanghai'
  'sink.partition-commit.policy.kind'='metastore,success-file'
);

SET table.sql-dialect=default;
CREATE TABLE kafka_table (
  user_id STRING,
  order_amount DOUBLE,
  ts BIGINT, -- time in epoch milliseconds
  ts_ltz AS TO_TIMESTAMP_LTZ(ts, 3),
  WATERMARK FOR ts_ltz AS ts_ltz - INTERVAL '5' SECOND -- Define watermark on TIMESTAMP_LTZ column
) WITH (...);

-- streaming sql, insert into hive table
INSERT INTO TABLE hive_table 
SELECT user_id, order_amount, DATE_FORMAT(ts_ltz, 'yyyy-MM-dd'), DATE_FORMAT(ts_ltz, 'HH')
FROM kafka_table;

-- batch sql, select with partition pruning
SELECT * FROM hive_table WHERE dt='2020-05-20' and hr='12';
`

By default, for streaming writes, Flink only supports renaming committers, meaning the S3 filesystem
cannot support exactly-once streaming writes.
Exactly-once writes to S3 can be achieved by configuring the following parameter to false.
This will instruct the sink to use Flink’s native writers but only works for
parquet and orc file types.
This configuration is set in the TableConfig and will affect all sinks of the job.

`TableConfig`

##### table.exec.hive.fallback-mapred-writer


### Dynamic Partition Writing#


Different from static partition writing which requires users to specify the partition column value, dynamic partition writing allow
users not to specify partition column value.
For example, for a partitioned table like:


```
CREATE TABLE fact_tz(x int) PARTITIONED BY (day STRING, hour STRING);

```

`CREATE TABLE fact_tz(x int) PARTITIONED BY (day STRING, hour STRING);
`

Users can use the follow SQL statement to write data to partitioned table fact_tz:

`fact_tz`

```
INSERT INTO TABLE fact_tz PARTITION (day, hour) select 1, '2022-8-8', '14';

```

`INSERT INTO TABLE fact_tz PARTITION (day, hour) select 1, '2022-8-8', '14';
`

It’s a typical case for dynamic partition writing since user does not specify any partition column value in the SQL statement.


By default, if it’s for dynamic partition writing, Flink will sort the data additionally by dynamic partition columns before writing into sink table.
That means the sink will receive all elements of one partition and then all elements of another partition.
Elements of different partitions will not be mixed. This is helpful for Hive sink to reduce the number of partition writers and improve writing performance by writing one partition at a time.
Otherwise, too many partition writers may cause the OutOfMemory exception.


To avoid the extra sorting, you can set job configuration table.exec.hive.sink.sort-by-dynamic-partition.enable (true by default) to false.
But with such a configuration, as said before, it may throw OutOfMemory exception if there are too many partitions fall into same sink node.

`table.exec.hive.sink.sort-by-dynamic-partition.enable`
`true`
`false`

To relieve the problem of too many partition writers, if data is not skewed, you can add DISTRIBUTED BY <partition_field> in your SQL statement to shuffle the data with same partition into same node.

`DISTRIBUTED BY <partition_field>`

Also, you can manually add SORTED BY <partition_field> in your SQL statement to achieve the same purpose as table.exec.hive.sink.sort-by-dynamic-partition.enable=true.

`SORTED BY <partition_field>`
`table.exec.hive.sink.sort-by-dynamic-partition.enable=true`

NOTE:

* The configuration table.exec.hive.sink.sort-by-dynamic-partition.enable only works in Flink BATCH mode.
* Currently, DISTRIBUTED BY and SORTED BY is only supported when using Hive dialect  in Flink BATCH mode.
`table.exec.hive.sink.sort-by-dynamic-partition.enable`
`BATCH`
`DISTRIBUTED BY`
`SORTED BY`
`BATCH`

### Auto Gather Statistic#


By default, Flink will gather the statistic automatically and then committed to Hive metastore during writing Hive table.


But in some case, you may want to disable it as it may be time-consuming to gather the statistic.
Then, you can set the job configuration table.exec.hive.sink.statistic-auto-gather.enable (true by default) to false
to disable it.

`table.exec.hive.sink.statistic-auto-gather.enable`
`true`
`false`

If the Hive table is stored as Parquet or ORC format, numFiles/totalSize/numRows/rawDataSize can be gathered.
Otherwise, only numFiles/totalSize can be gathered.

`numFiles`
`totalSize`
`numRows`
`rawDataSize`
`numFiles`
`totalSize`

To gather statistic numRows/rawDataSize for Parquet and ORC format, Flink will only read the file’s footer to do fast gathering.
But it may still time-consuming when there are too many files, then you can configure the job configuration table.exec.hive.sink.statistic-auto-gather.thread-num (3 by default) to
use more threads to speed the gathering.

`numRows`
`rawDataSize`
`table.exec.hive.sink.statistic-auto-gather.thread-num`
`3`

NOTE:

* Only BATCH mode supports to auto gather statistic, STREAMING mode doesn’t support it yet.
`BATCH`
`STREAMING`

### File Compaction#


The Hive sink also supports file compactions, which allows applications to reduce the number of files generated while writing into Hive.


#### Stream Mode#


In stream mode, the behavior is the same as FileSystem sink. Please refer to File Compaction for more details.

`FileSystem`

#### Batch Mode#


When it’s in batch mode and auto compaction is enabled, after finishing writing files, Flink will calculate the average size of written files for each partition. And if the average size is less than the
configured threshold, then Flink will try to compact these files to files with a target size. The following are the table’s options for file compaction.


##### auto-compaction


##### compaction.small-files.avg-size


##### compaction.file-size


##### compaction.parallelism


## Formats#


Flink’s Hive integration has been tested against the following file formats:

* Text
* CSV
* SequenceFile
* ORC
* Parquet