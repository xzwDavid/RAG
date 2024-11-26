# FileSystem


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# FileSystem SQL Connector#


This connector provides access to partitioned files in filesystems
supported by the Flink FileSystem abstraction.


The file system connector itself is included in Flink and does not require an additional dependency.
The corresponding jar can be found in the Flink distribution inside the /lib directory.
A corresponding format needs to be specified for reading and writing rows from and to a file system.

`/lib`

The file system connector allows for reading and writing from a local or distributed filesystem. A filesystem table can be defined as:


```
CREATE TABLE MyUserTable (
  column_name1 INT,
  column_name2 STRING,
  ...
  part_name1 INT,
  part_name2 STRING
) PARTITIONED BY (part_name1, part_name2) WITH (
  'connector' = 'filesystem',           -- required: specify the connector
  'path' = 'file:///path/to/whatever',  -- required: path to a directory
  'format' = '...',                     -- required: file system connector requires to specify a format,
                                        -- Please refer to Table Formats
                                        -- section for more details
  'partition.default-name' = '...',     -- optional: default partition name in case the dynamic partition
                                        -- column value is null/empty string
  'source.path.regex-pattern' = '...',  -- optional: regex pattern to filter files to read under the 
                                        -- directory of `path` option. This regex pattern should be
                                        -- matched with the absolute file path. If this option is set,
                                        -- the connector  will recursive all files under the directory
                                        -- of `path` option

  -- optional: the option to enable shuffle data by dynamic partition fields in sink phase, this can greatly
  -- reduce the number of file for filesystem sink but may lead data skew, the default value is false.
  'sink.shuffle-by-partition.enable' = '...',
  ...
)

```

`CREATE TABLE MyUserTable (
  column_name1 INT,
  column_name2 STRING,
  ...
  part_name1 INT,
  part_name2 STRING
) PARTITIONED BY (part_name1, part_name2) WITH (
  'connector' = 'filesystem',           -- required: specify the connector
  'path' = 'file:///path/to/whatever',  -- required: path to a directory
  'format' = '...',                     -- required: file system connector requires to specify a format,
                                        -- Please refer to Table Formats
                                        -- section for more details
  'partition.default-name' = '...',     -- optional: default partition name in case the dynamic partition
                                        -- column value is null/empty string
  'source.path.regex-pattern' = '...',  -- optional: regex pattern to filter files to read under the 
                                        -- directory of `path` option. This regex pattern should be
                                        -- matched with the absolute file path. If this option is set,
                                        -- the connector  will recursive all files under the directory
                                        -- of `path` option

  -- optional: the option to enable shuffle data by dynamic partition fields in sink phase, this can greatly
  -- reduce the number of file for filesystem sink but may lead data skew, the default value is false.
  'sink.shuffle-by-partition.enable' = '...',
  ...
)
`

> 
  Make sure to include Flink File System specific dependencies.



> 
  The behaviour of file system connector is much different from previous legacy filesystem connector:
the path parameter is specified for a directory not for a file and you can’t get a human-readable file in the path that you declare.


`previous legacy filesystem connector`

## Partition Files#


Flink’s file system partition support uses the standard hive format. However, it does not require partitions to be pre-registered with a table catalog. Partitions are discovered and inferred based on directory structure. For example, a table partitioned based on the directory below would be inferred to contain datetime and hour partitions.

`datetime`
`hour`

```
path
âââ datetime=2019-08-25
    âââ hour=11
        âââ part-0.parquet
        âââ part-1.parquet
    âââ hour=12
        âââ part-0.parquet
âââ datetime=2019-08-26
    âââ hour=6
        âââ part-0.parquet

```

`path
âââ datetime=2019-08-25
    âââ hour=11
        âââ part-0.parquet
        âââ part-1.parquet
    âââ hour=12
        âââ part-0.parquet
âââ datetime=2019-08-26
    âââ hour=6
        âââ part-0.parquet
`

The file system table supports both partition inserting and overwrite inserting. See INSERT Statement. When you insert overwrite to a partitioned table, only the corresponding partition will be overwritten, not the entire table.


## File Formats#


The file system connector supports multiple formats:

* CSV: RFC-4180.
* JSON: Note JSON format for file system connector is not a typical JSON file but newline delimited JSON.
* Avro: Apache Avro. Support compression by configuring avro.codec.
* Parquet: Apache Parquet. Compatible with Hive.
* Orc: Apache Orc. Compatible with Hive.
* Debezium-JSON: debezium-json.
* Canal-JSON: canal-json.
* Raw: raw.
`avro.codec`

## Source#


The file system connector can be used to read single files or entire directories into a single table.


When using a directory as the source path, there is no defined order of ingestion for the files inside the directory.


### Directory watching#


By default, the file system connector is bounded, that is it will scan the configured path once and then close itself.


You can enable continuous directory watching by configuring the option source.monitor-interval:

`source.monitor-interval`

##### source.monitor-interval


### Available Metadata#


The following connector metadata can be accessed as metadata columns in a table definition. All the metadata are read only.

`file.path`
`STRING NOT NULL`
`file.name`
`STRING NOT NULL`
`file.size`
`BIGINT NOT NULL`
`file.modification-time`
`TIMESTAMP_LTZ(3) NOT NULL`

The extended CREATE TABLE example demonstrates the syntax for exposing these metadata fields:

`CREATE TABLE`

```
CREATE TABLE MyUserTableWithFilepath (
  column_name1 INT,
  column_name2 STRING,
  `file.path` STRING NOT NULL METADATA
) WITH (
  'connector' = 'filesystem',
  'path' = 'file:///path/to/whatever',
  'format' = 'json'
)

```

`CREATE TABLE MyUserTableWithFilepath (
  column_name1 INT,
  column_name2 STRING,
  `file.path` STRING NOT NULL METADATA
) WITH (
  'connector' = 'filesystem',
  'path' = 'file:///path/to/whatever',
  'format' = 'json'
)
`

## Streaming Sink#


The file system connector supports streaming writes, based on Flink’s FileSystem,
to write records to file. Row-encoded Formats are CSV and JSON. Bulk-encoded Formats are Parquet, ORC and Avro.


You can write SQL directly, insert the stream data into the non-partitioned table.
If it is a partitioned table, you can configure partition related operations. See Partition Commit for details.


### Rolling Policy#


Data within the partition directories are split into part files. Each partition will contain at least one part file for
each subtask of the sink that has received data for that partition. The in-progress part file will be closed and additional
part file will be created according to the configurable rolling policy. The policy rolls part files based on size,
a timeout that specifies the maximum duration for which a file can be open.


##### sink.rolling-policy.file-size


##### sink.rolling-policy.rollover-interval


##### sink.rolling-policy.check-interval


NOTE: For bulk formats (parquet, orc, avro), the rolling policy in combination with the checkpoint interval(pending files
become finished on the next checkpoint) control the size and number of these parts.


NOTE: For row formats (csv, json), you can set the parameter sink.rolling-policy.file-size or sink.rolling-policy.rollover-interval in the connector properties and parameter execution.checkpointing.interval in Flink configuration file together
if you don’t want to wait a long period before observe the data exists in file system. For other formats (avro, orc), you can just set parameter execution.checkpointing.interval in Flink configuration file.

`sink.rolling-policy.file-size`
`sink.rolling-policy.rollover-interval`
`execution.checkpointing.interval`
`execution.checkpointing.interval`

### File Compaction#


The file sink supports file compactions, which allows applications to have smaller checkpoint intervals without generating a large number of files.


##### auto-compaction


##### compaction.file-size


If enabled, file compaction will merge multiple small files into larger files based on the target file size.
When running file compaction in production, please be aware that:

* Only files in a single checkpoint are compacted, that is, at least the same number of files as the number of checkpoints is generated.
* The file before merging is invisible, so the visibility of the file may be: checkpoint interval + compaction time.
* If the compaction takes too long, it will backpressure the job and extend the time period of checkpoint.

### Partition Commit#


After writing a partition, it is often necessary to notify downstream applications. For example, add the partition to a Hive metastore or writing a _SUCCESS file in the directory. The file system sink contains a partition commit feature that allows configuring custom policies. Commit actions are based on a combination of triggers and policies.

`_SUCCESS`
`triggers`
`policies`
* Trigger: The timing of the commit of the partition can be determined by the watermark with the time extracted from the partition, or by processing time.
* Policy: How to commit a partition, built-in policies support for the commit of success files and metastore, you can also implement your own policies, such as triggering hive’s analysis to generate statistics, or merging small files, etc.

NOTE: Partition Commit only works in dynamic partition inserting.


#### Partition commit trigger#


To define when to commit a partition, providing partition commit trigger:


##### sink.partition-commit.trigger


##### sink.partition-commit.delay


##### sink.partition-commit.watermark-time-zone


There are two types of trigger:

* The first is partition processing time. It neither requires partition time extraction nor watermark
generation. The trigger of partition commit according to partition creation time and current system time. This trigger
is more universal, but not so precise. For example, data delay or failover will lead to premature partition commit.
* The second is the trigger of partition commit according to the time that extracted from partition values and watermark.
This requires that your job has watermark generation, and the partition is divided according to time, such as
hourly partition or daily partition.

If you want to let downstream see the partition as soon as possible, no matter whether its data is complete or not:

* ‘sink.partition-commit.trigger’=‘process-time’ (Default value)
* ‘sink.partition-commit.delay’=‘0s’ (Default value)
Once there is data in the partition, it will immediately commit. Note: the partition may be committed multiple times.

If you want to let downstream see the partition only when its data is complete, and your job has watermark generation, and you can extract the time from partition values:

* ‘sink.partition-commit.trigger’=‘partition-time’
* ‘sink.partition-commit.delay’=‘1h’ (‘1h’ if your partition is hourly partition, depends on your partition type)
This is the most accurate way to commit partition, and it will try to ensure that the committed partitions are as data complete as possible.

If you want to let downstream see the partition only when its data is complete, but there is no watermark, or the time cannot be extracted from partition values:

* ‘sink.partition-commit.trigger’=‘process-time’ (Default value)
* ‘sink.partition-commit.delay’=‘1h’ (‘1h’ if your partition is hourly partition, depends on your partition type)
Try to commit partition accurately, but data delay or failover will lead to premature partition commit.

Late data processing: The record will be written into its partition when a record is supposed to be
written into a partition that has already been committed, and then the committing of this partition
will be triggered again.


#### Partition Time Extractor#


Time extractors define extracting time from partition values.


##### partition.time-extractor.kind


##### partition.time-extractor.class


##### partition.time-extractor.timestamp-pattern


##### partition.time-extractor.timestamp-formatter


The default extractor is based on a timestamp pattern composed of your partition fields. You can also specify an implementation for fully custom partition extraction based on the PartitionTimeExtractor interface.

`PartitionTimeExtractor`

```

public class HourPartTimeExtractor implements PartitionTimeExtractor {
    @Override
    public LocalDateTime extract(List<String> keys, List<String> values) {
        String dt = values.get(0);
        String hour = values.get(1);
		return Timestamp.valueOf(dt + " " + hour + ":00:00").toLocalDateTime();
	}
}

```

`
public class HourPartTimeExtractor implements PartitionTimeExtractor {
    @Override
    public LocalDateTime extract(List<String> keys, List<String> values) {
        String dt = values.get(0);
        String hour = values.get(1);
		return Timestamp.valueOf(dt + " " + hour + ":00:00").toLocalDateTime();
	}
}
`

#### Partition Commit Policy#


The partition commit policy defines what action is taken when partitions are committed.

* The first is metastore, only hive table supports metastore policy, file system manages partitions through directory structure.
* The second is the success file, which will write an empty file in the directory corresponding to the partition.

##### sink.partition-commit.policy.kind


##### sink.partition-commit.policy.class


##### sink.partition-commit.policy.class.parameters


##### sink.partition-commit.success-file.name


You can extend the implementation of commit policy, The custom commit policy implementation like:


```

public class AnalysisCommitPolicy implements PartitionCommitPolicy {
    private HiveShell hiveShell;
	
    @Override
	public void commit(Context context) throws Exception {
	    if (hiveShell == null) {
	        hiveShell = createHiveShell(context.catalogName());
	    }
	    
        hiveShell.execute(String.format(
            "ALTER TABLE %s ADD IF NOT EXISTS PARTITION (%s = '%s') location '%s'",
	        context.tableName(),
	        context.partitionKeys().get(0),
	        context.partitionValues().get(0),
	        context.partitionPath()));
	    hiveShell.execute(String.format(
	        "ANALYZE TABLE %s PARTITION (%s = '%s') COMPUTE STATISTICS FOR COLUMNS",
	        context.tableName(),
	        context.partitionKeys().get(0),
	        context.partitionValues().get(0)));
	}
}

```

`
public class AnalysisCommitPolicy implements PartitionCommitPolicy {
    private HiveShell hiveShell;
	
    @Override
	public void commit(Context context) throws Exception {
	    if (hiveShell == null) {
	        hiveShell = createHiveShell(context.catalogName());
	    }
	    
        hiveShell.execute(String.format(
            "ALTER TABLE %s ADD IF NOT EXISTS PARTITION (%s = '%s') location '%s'",
	        context.tableName(),
	        context.partitionKeys().get(0),
	        context.partitionValues().get(0),
	        context.partitionPath()));
	    hiveShell.execute(String.format(
	        "ANALYZE TABLE %s PARTITION (%s = '%s') COMPUTE STATISTICS FOR COLUMNS",
	        context.tableName(),
	        context.partitionKeys().get(0),
	        context.partitionValues().get(0)));
	}
}
`

## Sink Parallelism#


The parallelism of writing files into external file system (including Hive) can be configured by the corresponding table option, which is supported both in streaming mode and in batch mode. By default, the parallelism is configured to being the same as the parallelism of its last upstream chained operator. When the parallelism which is different from the parallelism of the upstream parallelism is configured, the operator of writing files and the operator compacting files (if used) will apply the parallelism.


##### sink.parallelism


NOTE: Currently, Configuring sink parallelism is supported if and only if the changelog mode of upstream is INSERT-ONLY. Otherwise, exception will be thrown.


## Full Example#


The below examples show how the file system connector can be used to write a streaming query to write data from Kafka into a file system and runs a batch query to read that data back out.


```

CREATE TABLE kafka_table (
  user_id STRING,
  order_amount DOUBLE,
  log_ts TIMESTAMP(3),
  WATERMARK FOR log_ts AS log_ts - INTERVAL '5' SECOND
) WITH (...);

CREATE TABLE fs_table (
  user_id STRING,
  order_amount DOUBLE,
  dt STRING,
  `hour` STRING
) PARTITIONED BY (dt, `hour`) WITH (
  'connector'='filesystem',
  'path'='...',
  'format'='parquet',
  'sink.partition-commit.delay'='1 h',
  'sink.partition-commit.policy.kind'='success-file'
);

-- streaming sql, insert into file system table
INSERT INTO fs_table 
SELECT 
    user_id, 
    order_amount, 
    DATE_FORMAT(log_ts, 'yyyy-MM-dd'),
    DATE_FORMAT(log_ts, 'HH') 
FROM kafka_table;

-- batch sql, select with partition pruning
SELECT * FROM fs_table WHERE dt='2020-05-20' and `hour`='12';

```

`
CREATE TABLE kafka_table (
  user_id STRING,
  order_amount DOUBLE,
  log_ts TIMESTAMP(3),
  WATERMARK FOR log_ts AS log_ts - INTERVAL '5' SECOND
) WITH (...);

CREATE TABLE fs_table (
  user_id STRING,
  order_amount DOUBLE,
  dt STRING,
  `hour` STRING
) PARTITIONED BY (dt, `hour`) WITH (
  'connector'='filesystem',
  'path'='...',
  'format'='parquet',
  'sink.partition-commit.delay'='1 h',
  'sink.partition-commit.policy.kind'='success-file'
);

-- streaming sql, insert into file system table
INSERT INTO fs_table 
SELECT 
    user_id, 
    order_amount, 
    DATE_FORMAT(log_ts, 'yyyy-MM-dd'),
    DATE_FORMAT(log_ts, 'HH') 
FROM kafka_table;

-- batch sql, select with partition pruning
SELECT * FROM fs_table WHERE dt='2020-05-20' and `hour`='12';
`

If the watermark is defined on TIMESTAMP_LTZ column and used partition-time to commit, the sink.partition-commit.watermark-time-zone is required to set to the session time zone, otherwise the partition committed may happen after a few hours.

`partition-time`
`sink.partition-commit.watermark-time-zone`

```

CREATE TABLE kafka_table (
  user_id STRING,
  order_amount DOUBLE,
  ts BIGINT, -- time in epoch milliseconds
  ts_ltz AS TO_TIMESTAMP_LTZ(ts, 3),
  WATERMARK FOR ts_ltz AS ts_ltz - INTERVAL '5' SECOND -- Define watermark on TIMESTAMP_LTZ column
) WITH (...);

CREATE TABLE fs_table (
  user_id STRING,
  order_amount DOUBLE,
  dt STRING,
  `hour` STRING
) PARTITIONED BY (dt, `hour`) WITH (
  'connector'='filesystem',
  'path'='...',
  'format'='parquet',
  'partition.time-extractor.timestamp-pattern'='$dt $hour:00:00',
  'sink.partition-commit.delay'='1 h',
  'sink.partition-commit.trigger'='partition-time',
  'sink.partition-commit.watermark-time-zone'='Asia/Shanghai', -- Assume user configured time zone is 'Asia/Shanghai'
  'sink.partition-commit.policy.kind'='success-file'
);

-- streaming sql, insert into file system table
INSERT INTO fs_table 
SELECT 
    user_id, 
    order_amount, 
    DATE_FORMAT(ts_ltz, 'yyyy-MM-dd'),
    DATE_FORMAT(ts_ltz, 'HH') 
FROM kafka_table;

-- batch sql, select with partition pruning
SELECT * FROM fs_table WHERE dt='2020-05-20' and `hour`='12';

```

`
CREATE TABLE kafka_table (
  user_id STRING,
  order_amount DOUBLE,
  ts BIGINT, -- time in epoch milliseconds
  ts_ltz AS TO_TIMESTAMP_LTZ(ts, 3),
  WATERMARK FOR ts_ltz AS ts_ltz - INTERVAL '5' SECOND -- Define watermark on TIMESTAMP_LTZ column
) WITH (...);

CREATE TABLE fs_table (
  user_id STRING,
  order_amount DOUBLE,
  dt STRING,
  `hour` STRING
) PARTITIONED BY (dt, `hour`) WITH (
  'connector'='filesystem',
  'path'='...',
  'format'='parquet',
  'partition.time-extractor.timestamp-pattern'='$dt $hour:00:00',
  'sink.partition-commit.delay'='1 h',
  'sink.partition-commit.trigger'='partition-time',
  'sink.partition-commit.watermark-time-zone'='Asia/Shanghai', -- Assume user configured time zone is 'Asia/Shanghai'
  'sink.partition-commit.policy.kind'='success-file'
);

-- streaming sql, insert into file system table
INSERT INTO fs_table 
SELECT 
    user_id, 
    order_amount, 
    DATE_FORMAT(ts_ltz, 'yyyy-MM-dd'),
    DATE_FORMAT(ts_ltz, 'HH') 
FROM kafka_table;

-- batch sql, select with partition pruning
SELECT * FROM fs_table WHERE dt='2020-05-20' and `hour`='12';
`

 Back to top
