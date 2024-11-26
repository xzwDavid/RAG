# Deduplication


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Deduplication#



Batch
Streaming


Deduplication removes rows that duplicate over a set of columns, keeping only the first one or the last one. In some cases, the upstream ETL jobs are not end-to-end exactly-once; this may result in duplicate records in the sink in case of failover. However, the duplicate records will affect the correctness of downstream analytical jobs - e.g. SUM, COUNT - so deduplication is needed before further analysis.

`SUM`
`COUNT`

Flink uses ROW_NUMBER() to remove duplicates, just like the way of Top-N query. In theory, deduplication is a special case of Top-N in which the N is one and order by the processing time or event time.

`ROW_NUMBER()`

The following shows the syntax of the Deduplication statement:


```
SELECT [column_list]
FROM table_name
QUALIFY ROW_NUMBER() OVER ([PARTITION BY col1[, col2...]] ORDER BY time_attr [asc|desc]) = 1

```

`SELECT [column_list]
FROM table_name
QUALIFY ROW_NUMBER() OVER ([PARTITION BY col1[, col2...]] ORDER BY time_attr [asc|desc]) = 1
`

Parameter Specification:

* ROW_NUMBER(): Assigns an unique, sequential number to each row, starting with one.
* PARTITION BY col1[, col2...]: Specifies the partition columns, i.e. the deduplicate key.
* ORDER BY time_attr [asc|desc]: Specifies the ordering column, it must be a time attribute. Currently Flink supports processing time attribute and event time attribute. Ordering by ASC means keeping the first row, ordering by DESC means keeping the last row.
* WHERE rownum = 1: The rownum = 1 is required for Flink to recognize this query is deduplication.
`ROW_NUMBER()`
`PARTITION BY col1[, col2...]`
`ORDER BY time_attr [asc|desc]`
`WHERE rownum = 1`
`rownum = 1`

> 
  Note: the above pattern must be followed exactly, otherwise the optimizer wonât be able to translate the query.



The following examples show how to specify SQL queries with Deduplication on streaming tables.


```
CREATE TABLE Orders (
  order_id  STRING,
  user        STRING,
  product     STRING,
  num         BIGINT,
  proctime AS PROCTIME()
) WITH (...);

-- remove duplicate rows on order_id and keep the first occurrence row,
-- because there shouldn't be two orders with the same order_id.
SELECT order_id, user, product, num
FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY proctime ASC) AS row_num
  FROM Orders)
WHERE row_num = 1

```

`CREATE TABLE Orders (
  order_id  STRING,
  user        STRING,
  product     STRING,
  num         BIGINT,
  proctime AS PROCTIME()
) WITH (...);

-- remove duplicate rows on order_id and keep the first occurrence row,
-- because there shouldn't be two orders with the same order_id.
SELECT order_id, user, product, num
FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY proctime ASC) AS row_num
  FROM Orders)
WHERE row_num = 1
`

 Back to top
