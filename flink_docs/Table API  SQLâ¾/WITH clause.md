# WITH clause


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# WITH clause#



Batch
Streaming


WITH provides a way to write auxiliary statements for use in a larger query. These statements, which are often referred to as Common Table Expression (CTE), can be thought of as defining temporary views that exist just for one query.

`WITH`

The syntax of WITH statement is:

`WITH`

```
WITH <with_item_definition> [ , ... ]
SELECT ... FROM ...;

<with_item_defintion>:
    with_item_name (column_name[, ...n]) AS ( <select_query> )

```

`WITH <with_item_definition> [ , ... ]
SELECT ... FROM ...;

<with_item_defintion>:
    with_item_name (column_name[, ...n]) AS ( <select_query> )
`

The following example defines a common table expression orders_with_total and use it in a GROUP BY query.

`orders_with_total`
`GROUP BY`

```
WITH orders_with_total AS (
    SELECT order_id, price + tax AS total
    FROM Orders
)
SELECT order_id, SUM(total)
FROM orders_with_total
GROUP BY order_id;

```

`WITH orders_with_total AS (
    SELECT order_id, price + tax AS total
    FROM Orders
)
SELECT order_id, SUM(total)
FROM orders_with_total
GROUP BY order_id;
`

 Back to top
