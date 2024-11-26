# Set Operations


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Set Operations#



Batch
Streaming


## UNION#


UNION and UNION ALL return the rows that are found in either table.
UNION takes only distinct rows while UNION ALL does not remove duplicates from the result rows.

`UNION`
`UNION ALL`
`UNION`
`UNION ALL`

```
Flink SQL> create view t1(s) as values ('c'), ('a'), ('b'), ('b'), ('c');
Flink SQL> create view t2(s) as values ('d'), ('e'), ('a'), ('b'), ('b');

Flink SQL> (SELECT s FROM t1) UNION (SELECT s FROM t2);
+---+
|  s|
+---+
|  c|
|  a|
|  b|
|  d|
|  e|
+---+

Flink SQL> (SELECT s FROM t1) UNION ALL (SELECT s FROM t2);
+---+
|  c|
+---+
|  c|
|  a|
|  b|
|  b|
|  c|
|  d|
|  e|
|  a|
|  b|
|  b|
+---+

```

`Flink SQL> create view t1(s) as values ('c'), ('a'), ('b'), ('b'), ('c');
Flink SQL> create view t2(s) as values ('d'), ('e'), ('a'), ('b'), ('b');

Flink SQL> (SELECT s FROM t1) UNION (SELECT s FROM t2);
+---+
|  s|
+---+
|  c|
|  a|
|  b|
|  d|
|  e|
+---+

Flink SQL> (SELECT s FROM t1) UNION ALL (SELECT s FROM t2);
+---+
|  c|
+---+
|  c|
|  a|
|  b|
|  b|
|  c|
|  d|
|  e|
|  a|
|  b|
|  b|
+---+
`

## INTERSECT#


INTERSECT and INTERSECT ALL return the rows that are found in both tables.
INTERSECT takes only distinct rows while INTERSECT ALL does not remove duplicates from the result rows.

`INTERSECT`
`INTERSECT ALL`
`INTERSECT`
`INTERSECT ALL`

```
Flink SQL> (SELECT s FROM t1) INTERSECT (SELECT s FROM t2);
+---+
|  s|
+---+
|  a|
|  b|
+---+

Flink SQL> (SELECT s FROM t1) INTERSECT ALL (SELECT s FROM t2);
+---+
|  s|
+---+
|  a|
|  b|
|  b|
+---+

```

`Flink SQL> (SELECT s FROM t1) INTERSECT (SELECT s FROM t2);
+---+
|  s|
+---+
|  a|
|  b|
+---+

Flink SQL> (SELECT s FROM t1) INTERSECT ALL (SELECT s FROM t2);
+---+
|  s|
+---+
|  a|
|  b|
|  b|
+---+
`

## EXCEPT#


EXCEPT and EXCEPT ALL return the rows that are found in one table but not the other.
EXCEPT takes only distinct rows while EXCEPT ALL does not remove duplicates from the result rows.

`EXCEPT`
`EXCEPT ALL`
`EXCEPT`
`EXCEPT ALL`

```
Flink SQL> (SELECT s FROM t1) EXCEPT (SELECT s FROM t2);
+---+
| s |
+---+
| c |
+---+

Flink SQL> (SELECT s FROM t1) EXCEPT ALL (SELECT s FROM t2);
+---+
| s |
+---+
| c |
| c |
+---+

```

`Flink SQL> (SELECT s FROM t1) EXCEPT (SELECT s FROM t2);
+---+
| s |
+---+
| c |
+---+

Flink SQL> (SELECT s FROM t1) EXCEPT ALL (SELECT s FROM t2);
+---+
| s |
+---+
| c |
| c |
+---+
`

## IN#


Returns true if an expression exists in a given table sub-query. The sub-query table must
consist of one column. This column must have the same data type as the expression.


```
SELECT user, amount
FROM Orders
WHERE product IN (
    SELECT product FROM NewProducts
)

```

`SELECT user, amount
FROM Orders
WHERE product IN (
    SELECT product FROM NewProducts
)
`

The optimizer rewrites the IN condition into a join and group operation. For streaming queries, the required state for computing the query result might grow infinitely depending on the number of distinct input rows. You can provide a query configuration with an appropriate state time-to-live (TTL) to prevent excessive state size. Note that this might affect the correctness of the query result. See query configuration for details.


## EXISTS#


```
SELECT user, amount
FROM Orders
WHERE product EXISTS (
    SELECT product FROM NewProducts
)

```

`SELECT user, amount
FROM Orders
WHERE product EXISTS (
    SELECT product FROM NewProducts
)
`

Returns true if the sub-query returns at least one row. Only supported if the operation can be rewritten in a join and group operation.


The optimizer rewrites the EXISTS operation into a join and group operation. For streaming queries, the required state for computing the query result might grow infinitely depending on the number of distinct input rows. You can provide a query configuration with an appropriate state time-to-live (TTL) to prevent excessive state size. Note that this might affect the correctness of the query result. See query configuration for details.

`EXISTS`

 Back to top
