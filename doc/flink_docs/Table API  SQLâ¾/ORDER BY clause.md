# ORDER BY clause


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# ORDER BY clause#



Batch
Streaming


The ORDER BY clause causes the result rows to be sorted according to the specified expression(s). If two rows are equal according to the leftmost expression, they are compared according to the next expression and so on. If they are equal according to all specified expressions, they are returned in an implementation-dependent order.

`ORDER BY`

When running in streaming mode, the primary sort order of a table must be ascending on a time attribute. All subsequent orders can be freely chosen. But there is no this limitation in batch mode.


```
SELECT *
FROM Orders
ORDER BY order_time, order_id

```

`SELECT *
FROM Orders
ORDER BY order_time, order_id
`

 Back to top
