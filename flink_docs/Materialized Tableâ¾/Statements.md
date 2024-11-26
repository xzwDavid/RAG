# Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Materialized Table Statements#


Flink SQL supports the following Materialized Table statements for now:

* CREATE MATERIALIZED TABLE
* ALTER MATERIALIZED TABLE
* DROP MATERIALIZED TABLE

# CREATE MATERIALIZED TABLE#


```
CREATE MATERIALIZED TABLE [catalog_name.][db_name.]table_name

[ ([ <table_constraint> ]) ]

[COMMENT table_comment]

[PARTITIONED BY (partition_column_name1, partition_column_name2, ...)]

[WITH (key1=val1, key2=val2, ...)]

FRESHNESS = INTERVAL '<num>' { SECOND | MINUTE | HOUR | DAY }

[REFRESH_MODE = { CONTINUOUS | FULL }]

AS <select_statement>

<table_constraint>:
  [CONSTRAINT constraint_name] PRIMARY KEY (column_name, ...) NOT ENFORCED

```

`CREATE MATERIALIZED TABLE [catalog_name.][db_name.]table_name

[ ([ <table_constraint> ]) ]

[COMMENT table_comment]

[PARTITIONED BY (partition_column_name1, partition_column_name2, ...)]

[WITH (key1=val1, key2=val2, ...)]

FRESHNESS = INTERVAL '<num>' { SECOND | MINUTE | HOUR | DAY }

[REFRESH_MODE = { CONTINUOUS | FULL }]

AS <select_statement>

<table_constraint>:
  [CONSTRAINT constraint_name] PRIMARY KEY (column_name, ...) NOT ENFORCED
`

## PRIMARY KEY#


PRIMARY KEY defines an optional list of columns that uniquely identifies each row within the table. The column as the primary key must be non-null.

`PRIMARY KEY`

## PARTITIONED BY#


PARTITIONED BY defines an optional list of columns to partition the materialized table. A directory is created for each partition if this materialized table is used as a filesystem sink.

`PARTITIONED BY`

Example:


```
-- Create a materialized table and specify the partition field as `ds`.
CREATE MATERIALIZED TABLE my_materialized_table
    PARTITIONED BY (ds)
    FRESHNESS = INTERVAL '1' HOUR
    AS SELECT 
        ds
    FROM
        ...

```

`-- Create a materialized table and specify the partition field as `ds`.
CREATE MATERIALIZED TABLE my_materialized_table
    PARTITIONED BY (ds)
    FRESHNESS = INTERVAL '1' HOUR
    AS SELECT 
        ds
    FROM
        ...
`

Note

* The partition column must be included in the query statement of the materialized table.

## WITH Options#


WITH Options are used to specify the materialized table properties, including connector options and time format option for partition fields.

`WITH Options`

```
-- Create a materialized table, specify the partition field as 'ds', and the corresponding time format as 'yyyy-MM-dd'
CREATE MATERIALIZED TABLE my_materialized_table
    PARTITIONED BY (ds)
    WITH (
        'format' = 'json',
        'partition.fields.ds.date-formatter' = 'yyyy-MM-dd'
    )
    ...

```

`-- Create a materialized table, specify the partition field as 'ds', and the corresponding time format as 'yyyy-MM-dd'
CREATE MATERIALIZED TABLE my_materialized_table
    PARTITIONED BY (ds)
    WITH (
        'format' = 'json',
        'partition.fields.ds.date-formatter' = 'yyyy-MM-dd'
    )
    ...
`

As shown in the above example, we specified the date-formatter option for the ds partition column. During each scheduling, the scheduling time will be converted to the ds partition value. For example, for a scheduling time of 2024-01-01 00:00:00, only the partition ds = '2024-01-01' will be refreshed.

`ds`
`2024-01-01 00:00:00`
`ds = '2024-01-01'`

Note

* The partition.fields.#.date-formatter option only works in full mode.
* The field in the partition.fields.#.date-formatter must be a valid string type partition field.

## FRESHNESS#


FRESHNESS defines the data freshness of a materialized table.

`FRESHNESS`

FRESHNESS and Refresh Mode Relationship


FRESHNESS defines the maximum amount of time that the materialized tableâs content should lag behind updates to the base tables. It does two things, firstly it determines the refresh mode of the materialized table through configuration, followed by determines the data refresh frequency to meet the actual data freshness requirements.


Explanation of FRESHNESS Parameter


The FRESHNESS parameter range is INTERVAL '<num>' { SECOND | MINUTE | HOUR | DAY }. '<num>' must be a positive integer, and in FULL mode, '<num>' should be a common divisor of the respective time interval unit.

`'<num>'`
`'<num>'`
`'<num>'`

Examples:
(Assuming materialized-table.refresh-mode.freshness-threshold is 30 minutes)

`materialized-table.refresh-mode.freshness-threshold`

```
-- The corresponding refresh pipeline is a streaming job with a checkpoint interval of 1 second
FRESHNESS = INTERVAL '1' SECOND

-- The corresponding refresh pipeline is a real-time job with a checkpoint interval of 1 minute
FRESHNESS = INTERVAL '1' MINUTE

-- The corresponding refresh pipeline is a scheduled workflow with a schedule cycle of 1 hour
FRESHNESS = INTERVAL '1' HOUR

-- The corresponding refresh pipeline is a scheduled workflow with a schedule cycle of 1 day
FRESHNESS = INTERVAL '1' DAY

```

`-- The corresponding refresh pipeline is a streaming job with a checkpoint interval of 1 second
FRESHNESS = INTERVAL '1' SECOND

-- The corresponding refresh pipeline is a real-time job with a checkpoint interval of 1 minute
FRESHNESS = INTERVAL '1' MINUTE

-- The corresponding refresh pipeline is a scheduled workflow with a schedule cycle of 1 hour
FRESHNESS = INTERVAL '1' HOUR

-- The corresponding refresh pipeline is a scheduled workflow with a schedule cycle of 1 day
FRESHNESS = INTERVAL '1' DAY
`

Invalid FRESHNESS Examples:

`FRESHNESS`

```
-- Interval is a negative number
FRESHNESS = INTERVAL '-1' SECOND

-- Interval is 0
FRESHNESS = INTERVAL '0' SECOND

-- Interval is in months or years
FRESHNESS = INTERVAL '1' MONTH
FRESHNESS = INTERVAL '1' YEAR

-- In FULL mode, the interval is not a common divisor of the respective time range
FRESHNESS = INTERVAL '60' SECOND
FRESHNESS = INTERVAL '5' HOUR

```

`-- Interval is a negative number
FRESHNESS = INTERVAL '-1' SECOND

-- Interval is 0
FRESHNESS = INTERVAL '0' SECOND

-- Interval is in months or years
FRESHNESS = INTERVAL '1' MONTH
FRESHNESS = INTERVAL '1' YEAR

-- In FULL mode, the interval is not a common divisor of the respective time range
FRESHNESS = INTERVAL '60' SECOND
FRESHNESS = INTERVAL '5' HOUR
`

Note

* The materialized table data will be refreshed as closely as possible within the defined freshness but cannot guarantee complete satisfaction.
* In CONTINUOUS mode, setting a data freshness interval that is too short can impact job performance as it aligns with the checkpoint interval. To optimize checkpoint performance, consider enabling-changelog.
* In FULL mode, data freshness must be translated into a cron expression, consequently, only freshness intervals within predefined time spans are presently accommodated, this design ensures alignment with cron’s capabilities. Specifically, support for the following freshness:

Second: 30, 15, 10, 5, 2, and 1 second intervals.
Minute: 30, 15, 10, 5, 2, and 1 minute intervals.
Hour: 8, 4, 2, and 1 hour intervals.
Day: 1 day.


* Second: 30, 15, 10, 5, 2, and 1 second intervals.
* Minute: 30, 15, 10, 5, 2, and 1 minute intervals.
* Hour: 8, 4, 2, and 1 hour intervals.
* Day: 1 day.

## REFRESH_MODE#


REFRESH_MODE is used to explicitly specify the refresh mode of the materialized table. The specified mode takes precedence over the framework’s automatic inference to meet specific scenarios’ needs.

`REFRESH_MODE`

Examples:
(Assuming materialized-table.refresh-mode.freshness-threshold is 30 minutes)

`materialized-table.refresh-mode.freshness-threshold`

```
-- The refresh mode of the created materialized table is CONTINUOUS, and the job's checkpoint interval is 1 hour.
CREATE MATERIALIZED TABLE my_materialized_table
    REFRESH_MODE = CONTINUOUS
    FRESHNESS = INTERVAL '1' HOUR
    AS SELECT
       ...    

-- The refresh mode of the created materialized table is FULL, and the job's schedule cycle is 10 minutes.
CREATE MATERIALIZED TABLE my_materialized_table
    REFRESH_MODE = FULL
    FRESHNESS = INTERVAL '10' MINUTE
    AS SELECT
       ...    

```

`-- The refresh mode of the created materialized table is CONTINUOUS, and the job's checkpoint interval is 1 hour.
CREATE MATERIALIZED TABLE my_materialized_table
    REFRESH_MODE = CONTINUOUS
    FRESHNESS = INTERVAL '1' HOUR
    AS SELECT
       ...    

-- The refresh mode of the created materialized table is FULL, and the job's schedule cycle is 10 minutes.
CREATE MATERIALIZED TABLE my_materialized_table
    REFRESH_MODE = FULL
    FRESHNESS = INTERVAL '10' MINUTE
    AS SELECT
       ...    
`

## AS <select_statement>#


This clause is used to define the query for populating materialized view data. The upstream table can be a materialized table, table, or view. The select statement supports all Flink SQL Queries.


Example:


```
CREATE MATERIALIZED TABLE my_materialized_table
    FRESHNESS = INTERVAL '10' SECOND
    AS SELECT * FROM kafka_catalog.db1.kafka_table;

```

`CREATE MATERIALIZED TABLE my_materialized_table
    FRESHNESS = INTERVAL '10' SECOND
    AS SELECT * FROM kafka_catalog.db1.kafka_table;
`

## Examples#


(Assuming materialized-table.refresh-mode.freshness-threshold is 30 minutes)

`materialized-table.refresh-mode.freshness-threshold`

Create a materialized table with a data freshness of 10 seconds and the derived refresh mode is CONTINUOUS:


```
CREATE MATERIALIZED TABLE my_materialized_table_continuous
    PARTITIONED BY (ds)
    WITH (
        'format' = 'debezium-json',
        'partition.fields.ds.date-formatter' = 'yyyy-MM-dd'
    )
    FRESHNESS = INTERVAL '10' SECOND
    AS 
    SELECT 
        k.ds,
        k.user_id,
        COUNT(*) AS event_count,
        SUM(k.amount) AS total_amount,
        MAX(u.age) AS max_age
    FROM 
        kafka_catalog.db1.kafka_table k
    JOIN 
        user_catalog.db1.user_table u
    ON 
        k.user_id = u.user_id
    WHERE 
        k.event_type = 'purchase'
    GROUP BY 
        k.ds, k.user_id

```

`CREATE MATERIALIZED TABLE my_materialized_table_continuous
    PARTITIONED BY (ds)
    WITH (
        'format' = 'debezium-json',
        'partition.fields.ds.date-formatter' = 'yyyy-MM-dd'
    )
    FRESHNESS = INTERVAL '10' SECOND
    AS 
    SELECT 
        k.ds,
        k.user_id,
        COUNT(*) AS event_count,
        SUM(k.amount) AS total_amount,
        MAX(u.age) AS max_age
    FROM 
        kafka_catalog.db1.kafka_table k
    JOIN 
        user_catalog.db1.user_table u
    ON 
        k.user_id = u.user_id
    WHERE 
        k.event_type = 'purchase'
    GROUP BY 
        k.ds, k.user_id
`

Create a materialized table with a data freshness of 1 hour and the derived refresh mode is FULL:


```
CREATE MATERIALIZED TABLE my_materialized_table_full
    PARTITIONED BY (ds)
    WITH (
        'format' = 'json',
        'partition.fields.ds.date-formatter' = 'yyyy-MM-dd'
    )
    FRESHNESS = INTERVAL '1' HOUR
    AS 
    SELECT 
        p.ds,
        p.product_id,
        p.product_name,
        AVG(s.sale_price) AS avg_sale_price,
        SUM(s.quantity) AS total_quantity
    FROM 
        paimon_catalog.db1.product_table p
    LEFT JOIN 
        paimon_catalog.db1.sales_table s
    ON 
        p.product_id = s.product_id
    WHERE 
        p.category = 'electronics'
    GROUP BY 
        p.ds, p.product_id, p.product_name

```

`CREATE MATERIALIZED TABLE my_materialized_table_full
    PARTITIONED BY (ds)
    WITH (
        'format' = 'json',
        'partition.fields.ds.date-formatter' = 'yyyy-MM-dd'
    )
    FRESHNESS = INTERVAL '1' HOUR
    AS 
    SELECT 
        p.ds,
        p.product_id,
        p.product_name,
        AVG(s.sale_price) AS avg_sale_price,
        SUM(s.quantity) AS total_quantity
    FROM 
        paimon_catalog.db1.product_table p
    LEFT JOIN 
        paimon_catalog.db1.sales_table s
    ON 
        p.product_id = s.product_id
    WHERE 
        p.category = 'electronics'
    GROUP BY 
        p.ds, p.product_id, p.product_name
`

## Limitations#

* Does not support explicitly specifying columns
* Does not support modified query statements
* Does not support using temporary tables, temporary views, or temporary functions in the select query

# ALTER MATERIALIZED TABLE#


```
ALTER MATERIALIZED TABLE [catalog_name.][db_name.]table_name SUSPEND | RESUME [WITH (key1=val1, key2=val2, ...)] | REFRESH [PARTITION partition_spec]

```

`ALTER MATERIALIZED TABLE [catalog_name.][db_name.]table_name SUSPEND | RESUME [WITH (key1=val1, key2=val2, ...)] | REFRESH [PARTITION partition_spec]
`

ALTER MATERIALIZED TABLE is used to manage materialized tables. This command allows users to suspend and resume refresh pipeline of materialized tables and manually trigger data refreshes.

`ALTER MATERIALIZED TABLE`

## SUSPEND#


```
ALTER MATERIALIZED TABLE [catalog_name.][db_name.]table_name SUSPEND

```

`ALTER MATERIALIZED TABLE [catalog_name.][db_name.]table_name SUSPEND
`

SUSPEND is used to pause the background refresh pipeline of the materialized table.

`SUSPEND`

Example:


```
-- Specify SAVEPOINT path before pausing
SET 'execution.checkpointing.savepoint-dir' = 'hdfs://savepoint_path';

-- Suspend the specified materialized table
ALTER MATERIALIZED TABLE my_materialized_table SUSPEND;

```

`-- Specify SAVEPOINT path before pausing
SET 'execution.checkpointing.savepoint-dir' = 'hdfs://savepoint_path';

-- Suspend the specified materialized table
ALTER MATERIALIZED TABLE my_materialized_table SUSPEND;
`

Note

* When suspending a table in CONTINUOUS mode, the job will be paused using STOP WITH SAVEPOINT by default. You need to set the SAVEPOINT save path using parameters.

## RESUME#


```
ALTER MATERIALIZED TABLE [catalog_name.][db_name.]table_name RESUME [WITH (key1=val1, key2=val2, ...)]

```

`ALTER MATERIALIZED TABLE [catalog_name.][db_name.]table_name RESUME [WITH (key1=val1, key2=val2, ...)]
`

RESUME is used to resume the refresh pipeline of a materialized table. Materialized table dynamic options can be specified through WITH options clause, which only take effect on the current refreshed pipeline and are not persistent.

`RESUME`
`WITH options`

Example:


```
-- Resume the specified materialized table
ALTER MATERIALIZED TABLE my_materialized_table RESUME;

-- Resume the specified materialized table and specify sink parallelism
ALTER MATERIALIZED TABLE my_materialized_table RESUME WITH ('sink.parallelism'='10');

```

`-- Resume the specified materialized table
ALTER MATERIALIZED TABLE my_materialized_table RESUME;

-- Resume the specified materialized table and specify sink parallelism
ALTER MATERIALIZED TABLE my_materialized_table RESUME WITH ('sink.parallelism'='10');
`

## REFRESH#


```
ALTER MATERIALIZED TABLE [catalog_name.][db_name.]table_name REFRESH [PARTITION partition_spec]

```

`ALTER MATERIALIZED TABLE [catalog_name.][db_name.]table_name REFRESH [PARTITION partition_spec]
`

REFRESH is used to proactively trigger the refresh of the materialized table.

`REFRESH`

Example:


```
-- Refresh the entire table data
ALTER MATERIALIZED TABLE my_materialized_table REFRESH;

-- Refresh specified partition data
ALTER MATERIALIZED TABLE my_materialized_table REFRESH PARTITION (ds='2024-06-28');

```

`-- Refresh the entire table data
ALTER MATERIALIZED TABLE my_materialized_table REFRESH;

-- Refresh specified partition data
ALTER MATERIALIZED TABLE my_materialized_table REFRESH PARTITION (ds='2024-06-28');
`

Note

* The REFRESH operation will start a Flink batch job to refresh the materialized table data.

# DROP MATERIALIZED TABLE#


```
DROP MATERIALIZED TABLE [IF EXISTS] [catalog_name.][database_name.]table_name

```

`DROP MATERIALIZED TABLE [IF EXISTS] [catalog_name.][database_name.]table_name
`

When dropping a materialized table, the background refresh pipeline will be deleted first, and then the metadata corresponding to the materialized table will be removed from the Catalog.


Example:


```
-- Delete the specified materialized table
DROP MATERIALIZED TABLE IF EXISTS my_materialized_table;

```

`-- Delete the specified materialized table
DROP MATERIALIZED TABLE IF EXISTS my_materialized_table;
`