# Sub-Queries


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Sub-Queries#


## Sub-Queries in the FROM Clause#


### Description#


Hive dialect supports sub-queries in the FROM clause. The sub-query has to be given a name because every table in a FROM clause must have a name.
Columns in the sub-query select list must have unique names.
The columns in the sub-query select list are available in the outer query just like columns of a table.
The sub-query can also be a query expression with UNION. Hive dialect supports arbitrary levels of sub-queries.

`FROM`
`FROM`
`UNION`

### Syntax#


```
select_statement FROM ( select_statement ) [ AS ] name

```

`select_statement FROM ( select_statement ) [ AS ] name
`

### Example#


```
SELECT col
FROM (
  SELECT a+b AS col
  FROM t1
) t2

```

`SELECT col
FROM (
  SELECT a+b AS col
  FROM t1
) t2
`

## Sub-Queries in the WHERE Clause#


### Description#


Hive dialect also supports some types of sub-queries in the WHERE clause.

`WHERE`

### Syntax#


```
select_statement FROM table WHERE { colName { IN | NOT IN } 
                                  | NOT EXISTS | EXISTS } ( subquery_select_statement )

```

`select_statement FROM table WHERE { colName { IN | NOT IN } 
                                  | NOT EXISTS | EXISTS } ( subquery_select_statement )
`

### Examples#


```
SELECT * FROM t1 WHERE t1.x IN (SELECT y FROM t2);
 
SELECT * FROM t1 WHERE EXISTS (SELECT y FROM t2 WHERE t1.x = t2.x);

```

`SELECT * FROM t1 WHERE t1.x IN (SELECT y FROM t2);
 
SELECT * FROM t1 WHERE EXISTS (SELECT y FROM t2 WHERE t1.x = t2.x);
`