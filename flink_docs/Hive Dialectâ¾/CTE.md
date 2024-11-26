# CTE


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Common Table Expression (CTE)#


## Description#


A Common Table Expression (CTE) is a temporary result set derived from a query specified in a WITH clause, which immediately precedes a SELECT
or INSERT keyword. The CTE is defined only with the execution scope of a single statement, and can be referred in the scope.

`WITH`
`SELECT`
`INSERT`

## Syntax#


```
withClause: WITH cteClause [ , ... ]
cteClause: cte_name AS (select statement)

```

`withClause: WITH cteClause [ , ... ]
cteClause: cte_name AS (select statement)
`

> 
Note:

The WITH clause is not supported within Sub-Query block
CTEs are supported in Views, CTAS and INSERT statement
Recursive Queries are not supported




Note:

* The WITH clause is not supported within Sub-Query block
* CTEs are supported in Views, CTAS and INSERT statement
* Recursive Queries are not supported
`WITH`
`CTAS`
`INSERT`

## Examples#


```
WITH q1 AS ( SELECT key FROM src WHERE key = '5')
SELECT *
FROM q1;

-- chaining CTEs
WITH q1 AS ( SELECT key FROM q2 WHERE key = '5'),
q2 AS ( SELECT key FROM src WHERE key = '5')
SELECT * FROM (SELECT key FROM q1) a;

-- insert example
WITH q1 AS ( SELECT key, value FROM src WHERE key = '5')
FROM q1
INSERT OVERWRITE TABLE t1
SELECT *;

-- ctas example
CREATE TABLE t2 AS
WITH q1 AS ( SELECT key FROM src WHERE key = '4')
SELECT * FROM q1;

```

`WITH q1 AS ( SELECT key FROM src WHERE key = '5')
SELECT *
FROM q1;

-- chaining CTEs
WITH q1 AS ( SELECT key FROM q2 WHERE key = '5'),
q2 AS ( SELECT key FROM src WHERE key = '5')
SELECT * FROM (SELECT key FROM q1) a;

-- insert example
WITH q1 AS ( SELECT key, value FROM src WHERE key = '5')
FROM q1
INSERT OVERWRITE TABLE t1
SELECT *;

-- ctas example
CREATE TABLE t2 AS
WITH q1 AS ( SELECT key FROM src WHERE key = '4')
SELECT * FROM q1;
`