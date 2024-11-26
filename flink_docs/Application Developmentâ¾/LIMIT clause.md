# LIMIT clause


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# LIMIT clause#


LIMIT clause constrains the number of rows returned by the SELECT statement. In general, this clause is used in conjunction with ORDER BY to ensure that the results are deterministic.

`LIMIT`
`SELECT`

The following example selects the first 3 rows in Orders table.

`Orders`

```
SELECT *
FROM Orders
ORDER BY orderTime
LIMIT 3

```

`SELECT *
FROM Orders
ORDER BY orderTime
LIMIT 3
`

 Back to top
