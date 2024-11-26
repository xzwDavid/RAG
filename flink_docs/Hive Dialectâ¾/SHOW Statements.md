# SHOW Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# SHOW Statements#


With Hive dialect, the following SHOW statements are supported for now:

* SHOW DATABASES
* SHOW TABLES
* SHOW VIEWS
* SHOW PARTITIONS
* SHOW FUNCTIONS

## SHOW DATABASES#


### Description#


SHOW DATABASES statement is used to list all the databases defined in the metastore.

`SHOW DATABASES`

### Syntax#


```
SHOW (DATABASES|SCHEMAS);

```

`SHOW (DATABASES|SCHEMAS);
`

The use of SCHEMA and DATABASE are interchangeable - they mean the same thing.

`SCHEMA`
`DATABASE`

## SHOW TABLES#


### Description#


SHOW TABLES statement lists all the base tables and views in the current database.

`SHOW TABLES`

### Syntax#


```
SHOW TABLES;

```

`SHOW TABLES;
`

## SHOW VIEWS#


### Description#


SHOW VIEWS statement lists all the views in the current database.

`SHOW VIEWS`

### Syntax#


```
SHOW VIEWS;

```

`SHOW VIEWS;
`

## SHOW PARTITIONS#


### Description#


SHOW PARTITIONS lists all the existing partitions or the partitions matching the specified partition spec for a given base table.

`SHOW PARTITIONS`

### Syntax#


```
SHOW PARTITIONS table_name [ partition_spec ];
partition_spec:
  : (partition_column = partition_col_value, partition_column = partition_col_value, ...)

```

`SHOW PARTITIONS table_name [ partition_spec ];
partition_spec:
  : (partition_column = partition_col_value, partition_column = partition_col_value, ...)
`

### Parameter#

* 
partition_spec
The optional partition_spec is used to what kind of partition should be returned.
When specified, the partitions that match the partition_spec specification are returned.
The partition_spec can be partial which means you can specific only part of partition columns for listing the partitions.


partition_spec


The optional partition_spec is used to what kind of partition should be returned.
When specified, the partitions that match the partition_spec specification are returned.
The partition_spec can be partial which means you can specific only part of partition columns for listing the partitions.

`partition_spec`
`partition_spec`
`partition_spec`

### Examples#


```
-- list all partitions
SHOW PARTITIONS t1;

-- specific a full partition partition spec to list specific partition
SHOW PARTITIONS t1 PARTITION (year = 2022, month = 12);

-- specific a partial partition spec to list all the specifc partitions
SHOW PARTITIONS t1 PARTITION (year = 2022);

```

`-- list all partitions
SHOW PARTITIONS t1;

-- specific a full partition partition spec to list specific partition
SHOW PARTITIONS t1 PARTITION (year = 2022, month = 12);

-- specific a partial partition spec to list all the specifc partitions
SHOW PARTITIONS t1 PARTITION (year = 2022);
`

## SHOW FUNCTIONS#


### Description#


SHOW FUNCTIONS statement is used to list all the user defined and builtin functions.

`SHOW FUNCTIONS`

### Syntax#


```
SHOW FUNCTIONS;

```

`SHOW FUNCTIONS;
`