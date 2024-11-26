# ANALYZE Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# ANALYZE Statements#


ANALYZE statements are used to collect statistics for existing tables and store the result to catalog. Only
ANALYZE TABLE statements are supported now, and need to be triggered manually instead of automatically.

`ANALYZE`
`ANALYZE TABLE`

Attention Currently, ANALYZE TABLE only supports in batch mode. Only existing
table is supported, and an exception will be thrown if the table is a view or table not exists.

`ANALYZE TABLE`

## Run an ANALYZE TABLE statement#


ANALYZE TABLE statements can be executed with the executeSql() method of the TableEnvironment.

`ANALYZE TABLE`
`executeSql()`
`TableEnvironment`

The following examples show how to run a ANALYZE TABLE statement in TableEnvironment.

`ANALYZE TABLE`
`TableEnvironment`

ANALYZE TABLE statements can be executed with the executeSql() method of the TableEnvironment.

`ANALYZE TABLE`
`executeSql()`
`TableEnvironment`

The following examples show how to run a ANALYZE TABLE statement in TableEnvironment.

`ANALYZE TABLE`
`TableEnvironment`

ANALYZE TABLE statements can be executed with the execute_sql() method of the TableEnvironment.

`ANALYZE TABLE`
`execute_sql()`
`TableEnvironment`

The following examples show how to run a ANALYZE TABLE statement in TableEnvironment.

`ANALYZE TABLE`
`TableEnvironment`

ANALYZE TABLE statements can be executed in SQL CLI.

`ANALYZE TABLE`

The following examples show how to run a ANALYZE TABLE statement in SQL CLI.

`ANALYZE TABLE`

```
TableEnvironment tableEnv = TableEnvironment.create(...);

// register a non-partition table named "Store"
tableEnv.executeSql(
        "CREATE TABLE Store (" +
        " `id` BIGINT NOT NULl," +
        " `location` VARCHAR(32)," +
        " `owner` VARCHAR(32)" +
        ") with (...)");

// register a partition table named "Orders"
tableEnv.executeSql(
        "CREATE TABLE Orders (" +
        " `id` BIGINT NOT NULl," +
        " `product` VARCHAR(32)," +
        " `amount` INT," +
        " `sold_year` BIGINT," +
        " `sold_month` BIGINT," +
        " `sold_day` BIGINT" +
        ") PARTITIONED BY (`sold_year`, `sold_month`, `sold_day`) "
        ") with (...)");

// Non-partition table, collect row count.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS");

// Non-partition table, collect row count and statistics for all columns.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS FOR ALL COLUMNS");

// Non-partition table, collect row count and statistics for column `location`.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS FOR COLUMNS location");


// Suppose table "Orders" has 4 partitions with specs:
// Partition1 : (sold_year='2022', sold_month='1', sold_day='10')
// Partition2 : (sold_year='2022', sold_month='1', sold_day='11')
// Partition3 : (sold_year='2022', sold_month='2', sold_day='10')
// Partition4 : (sold_year='2022', sold_month='2', sold_day='11')


// Partition table, collect row count for Partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS");

// Partition table, collect row count for Partition1 and Partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS");

// Partition table, collect row count for all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS");

// Partition table, collect row count and statistics for all columns on partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for all columns on partition1 and partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for all columns on all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for column `amount` on partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR COLUMNS amount");

// Partition table, collect row count and statistics for `amount` and `product` on partition1 and partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");

// Partition table, collect row count and statistics for column `amount` and `product` on all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");

```

`TableEnvironment tableEnv = TableEnvironment.create(...);

// register a non-partition table named "Store"
tableEnv.executeSql(
        "CREATE TABLE Store (" +
        " `id` BIGINT NOT NULl," +
        " `location` VARCHAR(32)," +
        " `owner` VARCHAR(32)" +
        ") with (...)");

// register a partition table named "Orders"
tableEnv.executeSql(
        "CREATE TABLE Orders (" +
        " `id` BIGINT NOT NULl," +
        " `product` VARCHAR(32)," +
        " `amount` INT," +
        " `sold_year` BIGINT," +
        " `sold_month` BIGINT," +
        " `sold_day` BIGINT" +
        ") PARTITIONED BY (`sold_year`, `sold_month`, `sold_day`) "
        ") with (...)");

// Non-partition table, collect row count.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS");

// Non-partition table, collect row count and statistics for all columns.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS FOR ALL COLUMNS");

// Non-partition table, collect row count and statistics for column `location`.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS FOR COLUMNS location");


// Suppose table "Orders" has 4 partitions with specs:
// Partition1 : (sold_year='2022', sold_month='1', sold_day='10')
// Partition2 : (sold_year='2022', sold_month='1', sold_day='11')
// Partition3 : (sold_year='2022', sold_month='2', sold_day='10')
// Partition4 : (sold_year='2022', sold_month='2', sold_day='11')


// Partition table, collect row count for Partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS");

// Partition table, collect row count for Partition1 and Partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS");

// Partition table, collect row count for all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS");

// Partition table, collect row count and statistics for all columns on partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for all columns on partition1 and partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for all columns on all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for column `amount` on partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR COLUMNS amount");

// Partition table, collect row count and statistics for `amount` and `product` on partition1 and partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");

// Partition table, collect row count and statistics for column `amount` and `product` on all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");
`

```
val tableEnv = TableEnvironment.create(...)

// register a non-partition table named "Store"
tableEnv.executeSql(
  "CREATE TABLE Store (" +
          " `id` BIGINT NOT NULl," +
          " `location` VARCHAR(32)," +
          " `owner` VARCHAR(32)" +
          ") with (...)");

// register a partition table named "Orders"
tableEnv.executeSql(
  "CREATE TABLE Orders (" +
          " `id` BIGINT NOT NULl," +
          " `product` VARCHAR(32)," +
          " `amount` INT," +
          " `sold_year` BIGINT," +
          " `sold_month` BIGINT," +
          " `sold_day` BIGINT" +
          ") PARTITIONED BY (`sold_year`, `sold_month`, `sold_day`) "
") with (...)");

// Non-partition table, collect row count.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS");

// Non-partition table, collect row count and statistics for all columns.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS FOR ALL COLUMNS");

// Non-partition table, collect row count and statistics for column `location`.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS FOR COLUMNS location");


// Suppose table "Orders" has 4 partitions with specs:
// Partition1 : (sold_year='2022', sold_month='1', sold_day='10')
// Partition2 : (sold_year='2022', sold_month='1', sold_day='11')
// Partition3 : (sold_year='2022', sold_month='2', sold_day='10')
// Partition4 : (sold_year='2022', sold_month='2', sold_day='11')


// Partition table, collect row count for Partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS");

// Partition table, collect row count for Partition1 and Partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS");

// Partition table, collect row count for all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS");

// Partition table, collect row count and statistics for all columns on partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for all columns on partition1 and partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for all columns on all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for column `amount` on partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR COLUMNS amount");

// Partition table, collect row count and statistics for `amount` and `product` on partition1 and partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");

// Partition table, collect row count and statistics for column `amount` and `product` on all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");

```

`val tableEnv = TableEnvironment.create(...)

// register a non-partition table named "Store"
tableEnv.executeSql(
  "CREATE TABLE Store (" +
          " `id` BIGINT NOT NULl," +
          " `location` VARCHAR(32)," +
          " `owner` VARCHAR(32)" +
          ") with (...)");

// register a partition table named "Orders"
tableEnv.executeSql(
  "CREATE TABLE Orders (" +
          " `id` BIGINT NOT NULl," +
          " `product` VARCHAR(32)," +
          " `amount` INT," +
          " `sold_year` BIGINT," +
          " `sold_month` BIGINT," +
          " `sold_day` BIGINT" +
          ") PARTITIONED BY (`sold_year`, `sold_month`, `sold_day`) "
") with (...)");

// Non-partition table, collect row count.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS");

// Non-partition table, collect row count and statistics for all columns.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS FOR ALL COLUMNS");

// Non-partition table, collect row count and statistics for column `location`.
tableEnv.executeSql("ANALYZE TABLE Store COMPUTE STATISTICS FOR COLUMNS location");


// Suppose table "Orders" has 4 partitions with specs:
// Partition1 : (sold_year='2022', sold_month='1', sold_day='10')
// Partition2 : (sold_year='2022', sold_month='1', sold_day='11')
// Partition3 : (sold_year='2022', sold_month='2', sold_day='10')
// Partition4 : (sold_year='2022', sold_month='2', sold_day='11')


// Partition table, collect row count for Partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS");

// Partition table, collect row count for Partition1 and Partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS");

// Partition table, collect row count for all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS");

// Partition table, collect row count and statistics for all columns on partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for all columns on partition1 and partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for all columns on all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

// Partition table, collect row count and statistics for column `amount` on partition1.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR COLUMNS amount");

// Partition table, collect row count and statistics for `amount` and `product` on partition1 and partition2.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");

// Partition table, collect row count and statistics for column `amount` and `product` on all partitions.
tableEnv.executeSql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");
`

```
table_env = TableEnvironment.create(...)

# register a non-partition table named "Store"
table_env.execute_sql(
  "CREATE TABLE Store (" +
          " `id` BIGINT NOT NULl," +
          " `location` VARCHAR(32)," +
          " `owner` VARCHAR(32)" +
          ") with (...)");

# register a partition table named "Orders"
table_env.execute_sql(
  "CREATE TABLE Orders (" +
          " `id` BIGINT NOT NULl," +
          " `product` VARCHAR(32)," +
          " `amount` INT," +
          " `sold_year` BIGINT," +
          " `sold_month` BIGINT," +
          " `sold_day` BIGINT" +
          ") PARTITIONED BY (`sold_year`, `sold_month`, `sold_day`) "
") with (...)");

# Non-partition table, collect row count.
table_env.execute_sql("ANALYZE TABLE Store COMPUTE STATISTICS");

# Non-partition table, collect row count and statistics for all columns.
table_env.execute_sql("ANALYZE TABLE Store COMPUTE STATISTICS FOR ALL COLUMNS");

# Non-partition table, collect row count and statistics for column `location`.
table_env.execute_sql("ANALYZE TABLE Store COMPUTE STATISTICS FOR COLUMNS location");


# Suppose table "Orders" has 4 partitions with specs:
# Partition1 : (sold_year='2022', sold_month='1', sold_day='10')
# Partition2 : (sold_year='2022', sold_month='1', sold_day='11')
# Partition3 : (sold_year='2022', sold_month='2', sold_day='10')
# Partition4 : (sold_year='2022', sold_month='2', sold_day='11')


# Partition table, collect row count for Partition1.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS");

# Partition table, collect row count for Partition1 and Partition2.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS");

# Partition table, collect row count for all partitions.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS");

# Partition table, collect row count and statistics for all columns on partition1.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR ALL COLUMNS");

# Partition table, collect row count and statistics for all columns on partition1 and partition2.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

# Partition table, collect row count and statistics for all columns on all partitions.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

# Partition table, collect row count and statistics for column `amount` on partition1.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR COLUMNS amount");

# Partition table, collect row count and statistics for `amount` and `product` on partition1 and partition2.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");

# Partition table, collect row count and statistics for column `amount` and `product` on all partitions.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");

```

`table_env = TableEnvironment.create(...)

# register a non-partition table named "Store"
table_env.execute_sql(
  "CREATE TABLE Store (" +
          " `id` BIGINT NOT NULl," +
          " `location` VARCHAR(32)," +
          " `owner` VARCHAR(32)" +
          ") with (...)");

# register a partition table named "Orders"
table_env.execute_sql(
  "CREATE TABLE Orders (" +
          " `id` BIGINT NOT NULl," +
          " `product` VARCHAR(32)," +
          " `amount` INT," +
          " `sold_year` BIGINT," +
          " `sold_month` BIGINT," +
          " `sold_day` BIGINT" +
          ") PARTITIONED BY (`sold_year`, `sold_month`, `sold_day`) "
") with (...)");

# Non-partition table, collect row count.
table_env.execute_sql("ANALYZE TABLE Store COMPUTE STATISTICS");

# Non-partition table, collect row count and statistics for all columns.
table_env.execute_sql("ANALYZE TABLE Store COMPUTE STATISTICS FOR ALL COLUMNS");

# Non-partition table, collect row count and statistics for column `location`.
table_env.execute_sql("ANALYZE TABLE Store COMPUTE STATISTICS FOR COLUMNS location");


# Suppose table "Orders" has 4 partitions with specs:
# Partition1 : (sold_year='2022', sold_month='1', sold_day='10')
# Partition2 : (sold_year='2022', sold_month='1', sold_day='11')
# Partition3 : (sold_year='2022', sold_month='2', sold_day='10')
# Partition4 : (sold_year='2022', sold_month='2', sold_day='11')


# Partition table, collect row count for Partition1.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS");

# Partition table, collect row count for Partition1 and Partition2.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS");

# Partition table, collect row count for all partitions.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS");

# Partition table, collect row count and statistics for all columns on partition1.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR ALL COLUMNS");

# Partition table, collect row count and statistics for all columns on partition1 and partition2.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

# Partition table, collect row count and statistics for all columns on all partitions.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR ALL COLUMNS");

# Partition table, collect row count and statistics for column `amount` on partition1.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR COLUMNS amount");

# Partition table, collect row count and statistics for `amount` and `product` on partition1 and partition2.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");

# Partition table, collect row count and statistics for column `amount` and `product` on all partitions.
table_env.execute_sql("ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product");
`

```
Flink SQL> CREATE TABLE Store (
> `id` BIGINT NOT NULl,
> `location` VARCHAR(32),
> `owner` VARCHAR(32)
> ) with (
> ...
> );
[INFO] Table has been created.

Flink SQL> CREATE TABLE Orders (
> `id` BIGINT NOT NULl,
> `product` VARCHAR(32),
> `amount` INT,
> `sold_year` BIGINT,
> `sold_month` BIGINT,
> `sold_day` BIGINT   
> ) PARTITIONED BY (`sold_year`, `sold_month`, `sold_day`)
> ) with (
> ...
> );
[INFO] Table has been created.

Flink SQL> ANALYZE TABLE Store COMPUTE STATISTICS;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Store COMPUTE STATISTICS FOR ALL COLUMNS;
[INFO] Execute statement succeeded.

Flink SQL> ANALYZE TABLE Store COMPUTE STATISTICS FOR COLUMNS location;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS;
[INFO] Execute statement succeeded.

Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS;
[INFO] Execute statement succeeded.

Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS;
[INFO] Execute statement succeeded.

Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR ALL COLUMNS;
[INFO] Execute statement succeeded.    

Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR ALL COLUMNS;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR ALL COLUMNS;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR COLUMNS amount;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Orders PARTITION (sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product;
[INFO] Execute statement succeeded.

```

`Flink SQL> CREATE TABLE Store (
> `id` BIGINT NOT NULl,
> `location` VARCHAR(32),
> `owner` VARCHAR(32)
> ) with (
> ...
> );
[INFO] Table has been created.

Flink SQL> CREATE TABLE Orders (
> `id` BIGINT NOT NULl,
> `product` VARCHAR(32),
> `amount` INT,
> `sold_year` BIGINT,
> `sold_month` BIGINT,
> `sold_day` BIGINT   
> ) PARTITIONED BY (`sold_year`, `sold_month`, `sold_day`)
> ) with (
> ...
> );
[INFO] Table has been created.

Flink SQL> ANALYZE TABLE Store COMPUTE STATISTICS;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Store COMPUTE STATISTICS FOR ALL COLUMNS;
[INFO] Execute statement succeeded.

Flink SQL> ANALYZE TABLE Store COMPUTE STATISTICS FOR COLUMNS location;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS;
[INFO] Execute statement succeeded.

Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS;
[INFO] Execute statement succeeded.

Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS;
[INFO] Execute statement succeeded.

Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR ALL COLUMNS;
[INFO] Execute statement succeeded.    

Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR ALL COLUMNS;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR ALL COLUMNS;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year='2022', sold_month='1', sold_day='10') COMPUTE STATISTICS FOR COLUMNS amount;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Orders PARTITION (sold_year='2022', sold_month='1', sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product;
[INFO] Execute statement succeeded.
    
Flink SQL> ANALYZE TABLE Orders PARTITION(sold_year, sold_month, sold_day) COMPUTE STATISTICS FOR COLUMNS amount, product;
[INFO] Execute statement succeeded.
`

## Syntax#


```
ANALYZE TABLE [catalog_name.][db_name.]table_name PARTITION(partcol1[=val1] [, partcol2[=val2], ...]) COMPUTE STATISTICS [FOR COLUMNS col1 [, col2, ...] | FOR ALL COLUMNS]

```

`ANALYZE TABLE [catalog_name.][db_name.]table_name PARTITION(partcol1[=val1] [, partcol2[=val2], ...]) COMPUTE STATISTICS [FOR COLUMNS col1 [, col2, ...] | FOR ALL COLUMNS]
`
* 
PARTITION(partcol1[=val1] [, partcol2[=val2], …]) is required for the partition table

If no partition is specified, the statistics will be gathered for all partitions
If a certain partition is specified, the statistics will be gathered only for specific partition
If the table is non-partition table , while a partition is specified, an exception will be thrown
If a certain partition is specified, but the partition does not exist, an exception will be thrown


* 
FOR COLUMNS col1 [, col2, …] or FOR ALL COLUMNS are optional

If no column is specified, only the table level statistics will be gathered
If a column does not exist, or column is not a physical column, an exception will be thrown.
If a column or any column is specified, the column level statistics will be gathered

the column level statistics include:

ndv: the number of distinct values
nullCount: the number of nulls
avgLen: the average length of column values
maxLen: the max length of column values
minValue: the min value of column values
maxValue: the max value of column values
valueCount: the value count only for boolean type


the supported types and its corresponding column level statistics are as following sheet lists(“Y” means support, “N” means unsupported):





PARTITION(partcol1[=val1] [, partcol2[=val2], …]) is required for the partition table

* If no partition is specified, the statistics will be gathered for all partitions
* If a certain partition is specified, the statistics will be gathered only for specific partition
* If the table is non-partition table , while a partition is specified, an exception will be thrown
* If a certain partition is specified, but the partition does not exist, an exception will be thrown

FOR COLUMNS col1 [, col2, …] or FOR ALL COLUMNS are optional

* If no column is specified, only the table level statistics will be gathered
* If a column does not exist, or column is not a physical column, an exception will be thrown.
* If a column or any column is specified, the column level statistics will be gathered

the column level statistics include:

ndv: the number of distinct values
nullCount: the number of nulls
avgLen: the average length of column values
maxLen: the max length of column values
minValue: the min value of column values
maxValue: the max value of column values
valueCount: the value count only for boolean type


the supported types and its corresponding column level statistics are as following sheet lists(“Y” means support, “N” means unsupported):


* the column level statistics include:

ndv: the number of distinct values
nullCount: the number of nulls
avgLen: the average length of column values
maxLen: the max length of column values
minValue: the min value of column values
maxValue: the max value of column values
valueCount: the value count only for boolean type


* the supported types and its corresponding column level statistics are as following sheet lists(“Y” means support, “N” means unsupported):
* ndv: the number of distinct values
* nullCount: the number of nulls
* avgLen: the average length of column values
* maxLen: the max length of column values
* minValue: the min value of column values
* maxValue: the max value of column values
* valueCount: the value count only for boolean type
`ndv`
`nullCount`
`avgLen`
`maxLen`
`maxValue`
`minValue`
`valueCount`
`BOOLEAN`
`TINYINT`
`SMALLINT`
`INTEGER`
`FLOAT`
`DATE`
`TIME_WITHOUT_TIME_ZONE`
`BIGINT`
`DOUBLE`
`DECIMAL`
`TIMESTAMP_WITH_LOCAL_TIME_ZONE`
`TIMESTAMP_WITHOUT_TIME_ZONE`
`CHAR`
`VARCHAR`
`other types`

NOTE: For the fix length types (like BOOLEAN, INTEGER, DOUBLE etc.), we need not collect the avgLen and maxLen from the original records.

`BOOLEAN`
`INTEGER`
`DOUBLE`
`avgLen`
`maxLen`

 Back to top
