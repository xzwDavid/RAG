# Over Aggregation


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Over Aggregation#



Batch
Streaming


OVER aggregates compute an aggregated value for every input row over a range of ordered rows. In contrast to GROUP BY aggregates, OVER aggregates do not reduce the number of result rows to a single row for every group. Instead OVER aggregates produce an aggregated value for every input row.

`OVER`
`GROUP BY`
`OVER`
`OVER`

The following query computes for every order the sum of amounts of all orders for the same product that were received within one hour before the current order.


```
SELECT order_id, order_time, amount,
  SUM(amount) OVER (
    PARTITION BY product
    ORDER BY order_time
    RANGE BETWEEN INTERVAL '1' HOUR PRECEDING AND CURRENT ROW
  ) AS one_hour_prod_amount_sum
FROM Orders

```

`SELECT order_id, order_time, amount,
  SUM(amount) OVER (
    PARTITION BY product
    ORDER BY order_time
    RANGE BETWEEN INTERVAL '1' HOUR PRECEDING AND CURRENT ROW
  ) AS one_hour_prod_amount_sum
FROM Orders
`

The syntax for an OVER window is summarized below.

`OVER`

```
SELECT
  agg_func(agg_col) OVER (
    [PARTITION BY col1[, col2, ...]]
    ORDER BY time_col
    range_definition),
  ...
FROM ...

```

`SELECT
  agg_func(agg_col) OVER (
    [PARTITION BY col1[, col2, ...]]
    ORDER BY time_col
    range_definition),
  ...
FROM ...
`

You can define multiple OVER window aggregates in a SELECT clause. However, for streaming queries, the OVER windows for all aggregates must be identical due to current limitation.

`OVER`
`SELECT`
`OVER`

### ORDER BY#


OVER windows are defined on an ordered sequence of rows. Since tables do not have an inherent order, the ORDER BY clause is mandatory. For streaming queries, Flink currently only supports OVER windows that are defined with an ascending time attributes order. Additional orderings are not supported.

`OVER`
`ORDER BY`
`OVER`

### PARTITION BY#


OVER windows can be defined on a partitioned table. In presence of a PARTITION BY clause, the aggregate is computed for each input row only over the rows of its partition.

`OVER`
`PARTITION BY`

### Range Definitions#


The range definition specifies how many rows are included in the aggregate. The range is defined with a BETWEEN clause that defines a lower and an upper boundary. All rows between these boundaries are included in the aggregate. Flink only supports CURRENT ROW as the upper boundary.

`BETWEEN`
`CURRENT ROW`

There are two options to define the range, ROWS intervals and RANGE intervals.

`ROWS`
`RANGE`

#### RANGE intervals#


A RANGE interval is defined on the values of the ORDER BY column, which is in case of Flink always a time attribute. The following RANGE interval defines that all rows with a time attribute of at most 30 minutes less than the current row are included in the aggregate.

`RANGE`

```
RANGE BETWEEN INTERVAL '30' MINUTE PRECEDING AND CURRENT ROW

```

`RANGE BETWEEN INTERVAL '30' MINUTE PRECEDING AND CURRENT ROW
`

#### ROW intervals#


A ROWS interval is a count-based interval. It defines exactly how many rows are included in the aggregate. The following ROWS interval defines that the 10 rows preceding the current row and the current row (so 11 rows in total) are included in the aggregate.

`ROWS`
`ROWS`

```
ROWS BETWEEN 10 PRECEDING AND CURRENT ROW
WINDOW

```

`ROWS BETWEEN 10 PRECEDING AND CURRENT ROW
WINDOW
`

The WINDOW clause can be used to define an OVER window outside of the SELECT clause. It can make queries more readable and also allows us to reuse the window definition for multiple aggregates.

`WINDOW`
`OVER`
`SELECT`

```
SELECT order_id, order_time, amount,
  SUM(amount) OVER w AS sum_amount,
  AVG(amount) OVER w AS avg_amount
FROM Orders
WINDOW w AS (
  PARTITION BY product
  ORDER BY order_time
  RANGE BETWEEN INTERVAL '1' HOUR PRECEDING AND CURRENT ROW)

```

`SELECT order_id, order_time, amount,
  SUM(amount) OVER w AS sum_amount,
  AVG(amount) OVER w AS avg_amount
FROM Orders
WINDOW w AS (
  PARTITION BY product
  ORDER BY order_time
  RANGE BETWEEN INTERVAL '1' HOUR PRECEDING AND CURRENT ROW)
`

 Back to top
