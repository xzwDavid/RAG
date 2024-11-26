# SELECT DISTINCT


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# SELECT DISTINCT#



Batch
Streaming


If SELECT DISTINCT is specified, all duplicate rows are removed from the result set (one row is kept from each group of duplicates).

`SELECT DISTINCT`

```
SELECT DISTINCT id FROM Orders

```

`SELECT DISTINCT id FROM Orders
`

For streaming queries, the required state for computing the query result might grow infinitely. State size depends on number of distinct rows. You can provide a query configuration with an appropriate state time-to-live (TTL) to prevent excessive state size. Note that this might affect the correctness of the query result. See query configuration for details


 Back to top
