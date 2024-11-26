# Window Aggregation


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Window Aggregation#


## Window TVF Aggregation#



Batch
Streaming


Window aggregations are defined in the GROUP BY clause contains “window_start” and “window_end” columns of the relation applied Windowing TVF. Just like queries with regular GROUP BY clauses, queries with a group by window aggregation will compute a single result row per group.

`GROUP BY`
`GROUP BY`

```
SELECT ...
FROM <windowed_table> -- relation applied windowing TVF
GROUP BY window_start, window_end, ...

```

`SELECT ...
FROM <windowed_table> -- relation applied windowing TVF
GROUP BY window_start, window_end, ...
`

Unlike other aggregations on continuous tables, window aggregation do not emit intermediate results but only a final result, the total aggregation at the end of the window. Moreover, window aggregations purge all intermediate state when no longer needed.


### Windowing TVFs#


Flink supports TUMBLE, HOP, CUMULATE and SESSION types of window aggregations.
In streaming mode, the time attribute field of a window table-valued function must be on either event or processing time attributes. See Windowing TVF for more windowing functions information.
In batch mode, the time attribute field of a window table-valued function must be an attribute of type TIMESTAMP or TIMESTAMP_LTZ.

`TUMBLE`
`HOP`
`CUMULATE`
`SESSION`
`TIMESTAMP`
`TIMESTAMP_LTZ`

> 
  Note: SESSION Window Aggregation is not supported in batch mode now.


`SESSION`

Here are some examples for TUMBLE, HOP, CUMULATE and SESSION window aggregations.

`TUMBLE`
`HOP`
`CUMULATE`
`SESSION`

```
-- tables must have time attribute, e.g. `bidtime` in this table
Flink SQL> desc Bid;
+-------------+------------------------+------+-----+--------+---------------------------------+
|        name |                   type | null | key | extras |                       watermark |
+-------------+------------------------+------+-----+--------+---------------------------------+
|     bidtime | TIMESTAMP(3) *ROWTIME* | true |     |        | `bidtime` - INTERVAL '1' SECOND |
|       price |         DECIMAL(10, 2) | true |     |        |                                 |
|        item |                 STRING | true |     |        |                                 |
| supplier_id |                 STRING | true |     |        |                                 |
+-------------+------------------------+------+-----+--------+---------------------------------+

Flink SQL> SELECT * FROM Bid;
+------------------+-------+------+-------------+
|          bidtime | price | item | supplier_id |
+------------------+-------+------+-------------+
| 2020-04-15 08:05 | 4.00  | C    | supplier1   |
| 2020-04-15 08:07 | 2.00  | A    | supplier1   |
| 2020-04-15 08:09 | 5.00  | D    | supplier2   |
| 2020-04-15 08:11 | 3.00  | B    | supplier2   |
| 2020-04-15 08:13 | 1.00  | E    | supplier1   |
| 2020-04-15 08:17 | 6.00  | F    | supplier2   |
+------------------+-------+------+-------------+

-- tumbling window aggregation
Flink SQL> SELECT window_start, window_end, SUM(price) AS total_price
  FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end;
+------------------+------------------+-------------+
|     window_start |       window_end | total_price |
+------------------+------------------+-------------+
| 2020-04-15 08:00 | 2020-04-15 08:10 |       11.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |       10.00 |
+------------------+------------------+-------------+

-- hopping window aggregation
Flink SQL> SELECT window_start, window_end, SUM(price) AS total_price
  FROM TABLE(
    HOP(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '5' MINUTES, INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end;
+------------------+------------------+-------------+
|     window_start |       window_end | total_price |
+------------------+------------------+-------------+
| 2020-04-15 08:00 | 2020-04-15 08:10 |       11.00 |
| 2020-04-15 08:05 | 2020-04-15 08:15 |       15.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |       10.00 |
| 2020-04-15 08:15 | 2020-04-15 08:25 |        6.00 |
+------------------+------------------+-------------+

-- cumulative window aggregation
Flink SQL> SELECT window_start, window_end, SUM(price) AS total_price
  FROM TABLE(
    CUMULATE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '2' MINUTES, INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end;
+------------------+------------------+-------------+
|     window_start |       window_end | total_price |
+------------------+------------------+-------------+
| 2020-04-15 08:00 | 2020-04-15 08:06 |        4.00 |
| 2020-04-15 08:00 | 2020-04-15 08:08 |        6.00 |
| 2020-04-15 08:00 | 2020-04-15 08:10 |       11.00 |
| 2020-04-15 08:10 | 2020-04-15 08:12 |        3.00 |
| 2020-04-15 08:10 | 2020-04-15 08:14 |        4.00 |
| 2020-04-15 08:10 | 2020-04-15 08:16 |        4.00 |
| 2020-04-15 08:10 | 2020-04-15 08:18 |       10.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |       10.00 |
+------------------+------------------+-------------+

-- session window aggregation with partition keys
Flink SQL> SELECT window_start, window_end, supplier_id, SUM(price) AS total_price
           FROM TABLE(
               SESSION(TABLE Bid PARTITION BY supplier_id, DESCRIPTOR(bidtime), INTERVAL '2' MINUTES))
           GROUP BY window_start, window_end, supplier_id;
+------------------+------------------+-------------+-------------+
|     window_start |       window_end | supplier_id | total_price |
+------------------+------------------+-------------+-------------+
| 2020-04-15 08:05 | 2020-04-15 08:09 | supplier1   |        6.00 |
| 2020-04-15 08:09 | 2020-04-15 08:13 | supplier2   |        8.00 |
| 2020-04-15 08:13 | 2020-04-15 08:15 | supplier1   |        1.00 |
| 2020-04-15 08:17 | 2020-04-15 08:19 | supplier2   |        6.00 |
+------------------+------------------+-------------+-------------+

-- session window aggregation without partition keys
Flink SQL> SELECT window_start, window_end, SUM(price) AS total_price
           FROM TABLE(
               SESSION(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '2' MINUTES))
           GROUP BY window_start, window_end;
+------------------+------------------+-------------+
|     window_start |       window_end | total_price |
+------------------+------------------+-------------+
| 2020-04-15 08:05 | 2020-04-15 08:15 |       15.00 |
| 2020-04-15 08:17 | 2020-04-15 08:19 |        6.00 |
+------------------+------------------+-------------+

```

`-- tables must have time attribute, e.g. `bidtime` in this table
Flink SQL> desc Bid;
+-------------+------------------------+------+-----+--------+---------------------------------+
|        name |                   type | null | key | extras |                       watermark |
+-------------+------------------------+------+-----+--------+---------------------------------+
|     bidtime | TIMESTAMP(3) *ROWTIME* | true |     |        | `bidtime` - INTERVAL '1' SECOND |
|       price |         DECIMAL(10, 2) | true |     |        |                                 |
|        item |                 STRING | true |     |        |                                 |
| supplier_id |                 STRING | true |     |        |                                 |
+-------------+------------------------+------+-----+--------+---------------------------------+

Flink SQL> SELECT * FROM Bid;
+------------------+-------+------+-------------+
|          bidtime | price | item | supplier_id |
+------------------+-------+------+-------------+
| 2020-04-15 08:05 | 4.00  | C    | supplier1   |
| 2020-04-15 08:07 | 2.00  | A    | supplier1   |
| 2020-04-15 08:09 | 5.00  | D    | supplier2   |
| 2020-04-15 08:11 | 3.00  | B    | supplier2   |
| 2020-04-15 08:13 | 1.00  | E    | supplier1   |
| 2020-04-15 08:17 | 6.00  | F    | supplier2   |
+------------------+-------+------+-------------+

-- tumbling window aggregation
Flink SQL> SELECT window_start, window_end, SUM(price) AS total_price
  FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end;
+------------------+------------------+-------------+
|     window_start |       window_end | total_price |
+------------------+------------------+-------------+
| 2020-04-15 08:00 | 2020-04-15 08:10 |       11.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |       10.00 |
+------------------+------------------+-------------+

-- hopping window aggregation
Flink SQL> SELECT window_start, window_end, SUM(price) AS total_price
  FROM TABLE(
    HOP(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '5' MINUTES, INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end;
+------------------+------------------+-------------+
|     window_start |       window_end | total_price |
+------------------+------------------+-------------+
| 2020-04-15 08:00 | 2020-04-15 08:10 |       11.00 |
| 2020-04-15 08:05 | 2020-04-15 08:15 |       15.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |       10.00 |
| 2020-04-15 08:15 | 2020-04-15 08:25 |        6.00 |
+------------------+------------------+-------------+

-- cumulative window aggregation
Flink SQL> SELECT window_start, window_end, SUM(price) AS total_price
  FROM TABLE(
    CUMULATE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '2' MINUTES, INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end;
+------------------+------------------+-------------+
|     window_start |       window_end | total_price |
+------------------+------------------+-------------+
| 2020-04-15 08:00 | 2020-04-15 08:06 |        4.00 |
| 2020-04-15 08:00 | 2020-04-15 08:08 |        6.00 |
| 2020-04-15 08:00 | 2020-04-15 08:10 |       11.00 |
| 2020-04-15 08:10 | 2020-04-15 08:12 |        3.00 |
| 2020-04-15 08:10 | 2020-04-15 08:14 |        4.00 |
| 2020-04-15 08:10 | 2020-04-15 08:16 |        4.00 |
| 2020-04-15 08:10 | 2020-04-15 08:18 |       10.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |       10.00 |
+------------------+------------------+-------------+

-- session window aggregation with partition keys
Flink SQL> SELECT window_start, window_end, supplier_id, SUM(price) AS total_price
           FROM TABLE(
               SESSION(TABLE Bid PARTITION BY supplier_id, DESCRIPTOR(bidtime), INTERVAL '2' MINUTES))
           GROUP BY window_start, window_end, supplier_id;
+------------------+------------------+-------------+-------------+
|     window_start |       window_end | supplier_id | total_price |
+------------------+------------------+-------------+-------------+
| 2020-04-15 08:05 | 2020-04-15 08:09 | supplier1   |        6.00 |
| 2020-04-15 08:09 | 2020-04-15 08:13 | supplier2   |        8.00 |
| 2020-04-15 08:13 | 2020-04-15 08:15 | supplier1   |        1.00 |
| 2020-04-15 08:17 | 2020-04-15 08:19 | supplier2   |        6.00 |
+------------------+------------------+-------------+-------------+

-- session window aggregation without partition keys
Flink SQL> SELECT window_start, window_end, SUM(price) AS total_price
           FROM TABLE(
               SESSION(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '2' MINUTES))
           GROUP BY window_start, window_end;
+------------------+------------------+-------------+
|     window_start |       window_end | total_price |
+------------------+------------------+-------------+
| 2020-04-15 08:05 | 2020-04-15 08:15 |       15.00 |
| 2020-04-15 08:17 | 2020-04-15 08:19 |        6.00 |
+------------------+------------------+-------------+
`

Note: in order to better understand the behavior of windowing, we simplify the displaying of timestamp values to not show the trailing zeros, e.g. 2020-04-15 08:05 should be displayed as 2020-04-15 08:05:00.000 in Flink SQL Client if the type is TIMESTAMP(3).

`2020-04-15 08:05`
`2020-04-15 08:05:00.000`
`TIMESTAMP(3)`

### GROUPING SETS#


Window aggregations also support GROUPING SETS syntax. Grouping sets allow for more complex grouping operations than those describable by a standard GROUP BY. Rows are grouped separately by each specified grouping set and aggregates are computed for each group just as for simple GROUP BY clauses.

`GROUPING SETS`
`GROUP BY`
`GROUP BY`

Window aggregations with GROUPING SETS require both the window_start and window_end columns have to be in the GROUP BY clause, but not in the GROUPING SETS clause.

`GROUPING SETS`
`window_start`
`window_end`
`GROUP BY`
`GROUPING SETS`

```
Flink SQL> SELECT window_start, window_end, supplier_id, SUM(price) AS total_price
  FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end, GROUPING SETS ((supplier_id), ());
+------------------+------------------+-------------+-------------+
|     window_start |       window_end | supplier_id | total_price |
+------------------+------------------+-------------+-------------+
| 2020-04-15 08:00 | 2020-04-15 08:10 |      (NULL) |       11.00 |
| 2020-04-15 08:00 | 2020-04-15 08:10 |   supplier2 |        5.00 |
| 2020-04-15 08:00 | 2020-04-15 08:10 |   supplier1 |        6.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |      (NULL) |       10.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |   supplier2 |        9.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |   supplier1 |        1.00 |
+------------------+------------------+-------------+-------------+

```

`Flink SQL> SELECT window_start, window_end, supplier_id, SUM(price) AS total_price
  FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end, GROUPING SETS ((supplier_id), ());
+------------------+------------------+-------------+-------------+
|     window_start |       window_end | supplier_id | total_price |
+------------------+------------------+-------------+-------------+
| 2020-04-15 08:00 | 2020-04-15 08:10 |      (NULL) |       11.00 |
| 2020-04-15 08:00 | 2020-04-15 08:10 |   supplier2 |        5.00 |
| 2020-04-15 08:00 | 2020-04-15 08:10 |   supplier1 |        6.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |      (NULL) |       10.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |   supplier2 |        9.00 |
| 2020-04-15 08:10 | 2020-04-15 08:20 |   supplier1 |        1.00 |
+------------------+------------------+-------------+-------------+
`

Each sublist of GROUPING SETS may specify zero or more columns or expressions and is interpreted the same way as though used directly in the GROUP BY clause. An empty grouping set means that all rows are aggregated down to a single group, which is output even if no input rows were present.

`GROUPING SETS`
`GROUP BY`

References to the grouping columns or expressions are replaced by null values in result rows for grouping sets in which those columns do not appear.


#### ROLLUP#


ROLLUP is a shorthand notation for specifying a common type of grouping set. It represents the given list of expressions and all prefixes of the list, including the empty list.

`ROLLUP`

Window aggregations with ROLLUP requires both the window_start and window_end columns have to be in the GROUP BY clause, but not in the ROLLUP clause.

`ROLLUP`
`window_start`
`window_end`
`GROUP BY`
`ROLLUP`

For example, the following query is equivalent to the one above.


```
SELECT window_start, window_end, supplier_id, SUM(price) AS total_price
FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES))
GROUP BY window_start, window_end, ROLLUP (supplier_id);

```

`SELECT window_start, window_end, supplier_id, SUM(price) AS total_price
FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES))
GROUP BY window_start, window_end, ROLLUP (supplier_id);
`

#### CUBE#


CUBE is a shorthand notation for specifying a common type of grouping set. It represents the given list and all of its possible subsets - the power set.

`CUBE`

Window aggregations with CUBE requires both the window_start and window_end columns have to be in the GROUP BY clause, but not in the CUBE clause.

`CUBE`
`window_start`
`window_end`
`GROUP BY`
`CUBE`

For example, the following two queries are equivalent.


```
SELECT window_start, window_end, item, supplier_id, SUM(price) AS total_price
  FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end, CUBE (supplier_id, item);

SELECT window_start, window_end, item, supplier_id, SUM(price) AS total_price
  FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end, GROUPING SETS (
      (supplier_id, item),
      (supplier_id      ),
      (             item),
      (                 )
)

```

`SELECT window_start, window_end, item, supplier_id, SUM(price) AS total_price
  FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end, CUBE (supplier_id, item);

SELECT window_start, window_end, item, supplier_id, SUM(price) AS total_price
  FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end, GROUPING SETS (
      (supplier_id, item),
      (supplier_id      ),
      (             item),
      (                 )
)
`

### Selecting Group Window Start and End Timestamps#


The start and end timestamps of group windows can be selected with the grouped window_start and window_end columns.

`window_start`
`window_end`

### Cascading Window Aggregation#


The window_start and window_end columns are regular timestamp columns, not time attributes. Thus they can’t be used as time attributes in subsequent time-based operations.
In order to propagate time attributes, you need to additionally add window_time column into GROUP BY clause. The window_time is the third column produced by Windowing TVFs which is a time attribute of the assigned window.
Adding window_time into GROUP BY clause makes window_time also to be group key that can be selected. Then following queries can use this column for subsequent time-based operations, such as cascading window aggregations and Window TopN.

`window_start`
`window_end`
`window_time`
`GROUP BY`
`window_time`
`window_time`
`GROUP BY`
`window_time`

The following shows a cascading window aggregation where the first window aggregation propagates the time attribute for the second window aggregation.


```
-- tumbling 5 minutes for each supplier_id
CREATE VIEW window1 AS
-- Note: The window start and window end fields of inner Window TVF are optional in the select clause. However, if they appear in the clause, they need to be aliased to prevent name conflicting with the window start and window end of the outer Window TVF.
SELECT window_start AS window_5mintumble_start, window_end AS window_5mintumble_end, window_time AS rowtime, SUM(price) AS partial_price
  FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '5' MINUTES))
  GROUP BY supplier_id, window_start, window_end, window_time;

-- tumbling 10 minutes on the first window
SELECT window_start, window_end, SUM(partial_price) AS total_price
  FROM TABLE(
      TUMBLE(TABLE window1, DESCRIPTOR(rowtime), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end;

```

`-- tumbling 5 minutes for each supplier_id
CREATE VIEW window1 AS
-- Note: The window start and window end fields of inner Window TVF are optional in the select clause. However, if they appear in the clause, they need to be aliased to prevent name conflicting with the window start and window end of the outer Window TVF.
SELECT window_start AS window_5mintumble_start, window_end AS window_5mintumble_end, window_time AS rowtime, SUM(price) AS partial_price
  FROM TABLE(
    TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '5' MINUTES))
  GROUP BY supplier_id, window_start, window_end, window_time;

-- tumbling 10 minutes on the first window
SELECT window_start, window_end, SUM(partial_price) AS total_price
  FROM TABLE(
      TUMBLE(TABLE window1, DESCRIPTOR(rowtime), INTERVAL '10' MINUTES))
  GROUP BY window_start, window_end;
`

## Group Window Aggregation#



Batch
Streaming


> 
Warning: Group Window Aggregation is deprecated. It’s encouraged to use Window TVF Aggregation which is more powerful and effective.
Compared to Group Window Aggregation, Window TVF Aggregation have many advantages, including:

Have all performance optimizations mentioned in Performance Tuning.
Support standard GROUPING SETS syntax.
Can apply Window TopN after window aggregation result.
and so on.




Warning: Group Window Aggregation is deprecated. It’s encouraged to use Window TVF Aggregation which is more powerful and effective.


Compared to Group Window Aggregation, Window TVF Aggregation have many advantages, including:

* Have all performance optimizations mentioned in Performance Tuning.
* Support standard GROUPING SETS syntax.
* Can apply Window TopN after window aggregation result.
* and so on.
`GROUPING SETS`

Group Window Aggregations are defined in the GROUP BY clause of a SQL query. Just like queries with regular GROUP BY clauses, queries with a GROUP BY clause that includes a group window function compute a single result row per group. The following group windows functions are supported for SQL on batch and streaming tables.

`GROUP BY`
`GROUP BY`
`GROUP BY`

### Group Window Functions#

`TUMBLE(time_attr, interval)`
`interval`
`HOP(time_attr, interval, interval)`
`interval`
`interval`
`SESSION(time_attr, interval)`
`interval`

### Time Attributes#


In streaming mode, the time_attr argument of the group window function must refer to a valid time attribute that specifies the processing time or event time of rows. See the documentation of time attributes to learn how to define time attributes.

`time_attr`

In batch mode, the time_attr argument of the group window function must be an attribute of type TIMESTAMP.

`time_attr`
`TIMESTAMP`

### Selecting Group Window Start and End Timestamps#


The start and end timestamps of group windows as well as time attributes can be selected with the following auxiliary functions:

`TUMBLE_START(time_attr, interval)`
`HOP_START(time_attr, interval, interval)`
`SESSION_START(time_attr, interval)`

Returns the timestamp of the inclusive lower bound of the corresponding tumbling, hopping, or session window.

`TUMBLE_END(time_attr, interval)`
`HOP_END(time_attr, interval, interval)`
`SESSION_END(time_attr, interval)`

Returns the timestamp of the exclusive upper bound of the corresponding tumbling, hopping, or session window.


Note: The exclusive upper bound timestamp cannot be used as a rowtime attribute in subsequent time-based operations, such as interval joins and group window or over window aggregations.

`TUMBLE_ROWTIME(time_attr, interval)`
`HOP_ROWTIME(time_attr, interval, interval)`
`SESSION_ROWTIME(time_attr, interval)`

Returns the timestamp of the inclusive upper bound of the corresponding tumbling, hopping, or session window.


The resulting attribute is a rowtime attribute that can be used in subsequent time-based operations such as interval joins and group window or over window aggregations.

`TUMBLE_PROCTIME(time_attr, interval)`
`HOP_PROCTIME(time_attr, interval, interval)`
`SESSION_PROCTIME(time_attr, interval)`

Returns a proctime attribute that can be used in subsequent time-based operations such as interval joins and group window or over window aggregations.


Note: Auxiliary functions must be called with exactly same arguments as the group window function in the GROUP BY clause.

`GROUP BY`

The following examples show how to specify SQL queries with group windows on streaming tables.


```
CREATE TABLE Orders (
  user       BIGINT,
  product    STRING,
  amount     INT,
  order_time TIMESTAMP(3),
  WATERMARK FOR order_time AS order_time - INTERVAL '1' MINUTE
) WITH (...);

SELECT
  user,
  TUMBLE_START(order_time, INTERVAL '1' DAY) AS wStart,
  SUM(amount) FROM Orders
GROUP BY
  TUMBLE(order_time, INTERVAL '1' DAY),
  user

```

`CREATE TABLE Orders (
  user       BIGINT,
  product    STRING,
  amount     INT,
  order_time TIMESTAMP(3),
  WATERMARK FOR order_time AS order_time - INTERVAL '1' MINUTE
) WITH (...);

SELECT
  user,
  TUMBLE_START(order_time, INTERVAL '1' DAY) AS wStart,
  SUM(amount) FROM Orders
GROUP BY
  TUMBLE(order_time, INTERVAL '1' DAY),
  user
`

 Back to top
