# SELECT & WHERE


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# SELECT & WHERE clause#



Batch
Streaming


The general syntax of the SELECT statement is:

`SELECT`

```
SELECT select_list FROM table_expression [ WHERE boolean_expression ]

```

`SELECT select_list FROM table_expression [ WHERE boolean_expression ]
`

The table_expression refers to any source of data. It could be an existing table, view, VALUES, or VALUE clause, the joined results of multiple existing tables, or a subquery. Assuming that the table is available in the catalog, the following would read all rows from Orders.

`table_expression`
`VALUES`
`VALUE`
`Orders`

```
SELECT * FROM Orders

```

`SELECT * FROM Orders
`

The select_list specification * means the query will resolve all columns. However, usage of * is discouraged in production because it makes queries less robust to catalog changes. Instead, a select_list can specify a subset of available columns or make calculations using said columns. For example, if Orders has columns named order_id, price, and tax you could write the following query:

`select_list`
`*`
`*`
`select_list`
`Orders`
`order_id`
`price`
`tax`

```
SELECT order_id, price + tax FROM Orders

```

`SELECT order_id, price + tax FROM Orders
`

Queries can also consume from inline data using the VALUES clause. Each tuple corresponds to one row and an alias may be provided to assign names to each column.

`VALUES`

```
SELECT order_id, price FROM (VALUES (1, 2.0), (2, 3.1))  AS t (order_id, price)

```

`SELECT order_id, price FROM (VALUES (1, 2.0), (2, 3.1))  AS t (order_id, price)
`

Rows can be filtered based on a WHERE clause.

`WHERE`

```
SELECT price + tax FROM Orders WHERE id = 10

```

`SELECT price + tax FROM Orders WHERE id = 10
`

Additionally, built-in and user-defined scalar functions can be invoked on the columns of a single row. User-defined functions must be registered in a catalog before use.


```
SELECT PRETTY_PRINT(order_id) FROM Orders

```

`SELECT PRETTY_PRINT(order_id) FROM Orders
`

 Back to top
