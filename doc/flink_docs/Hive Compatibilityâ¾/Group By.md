# Group By


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Group By Clause#


## Description#


The Group by clause is used to compute a single result from multiple input rows with given aggregation function.
Hive dialect also supports enhanced aggregation features to do multiple aggregations based on the same record by using
ROLLUP/CUBE/GROUPING SETS.

`Group by`
`ROLLUP`
`CUBE`
`GROUPING SETS`

## Syntax#


```
group_by_clause: 
  group_by_clause_1 | group_by_clause_2

group_by_clause_1: 
  GROUP BY group_expression [ , ... ] [ WITH ROLLUP | WITH CUBE ] 
 
group_by_clause_2: 
  GROUP BY { group_expression | { ROLLUP | CUBE | GROUPING SETS } ( grouping_set [ , ... ] ) } [ , ... ]

grouping_set: 
  { expression | ( [ expression [ , ... ] ] ) }
 
groupByQuery: SELECT expression [ , ... ] FROM src groupByClause?

```

`group_by_clause: 
  group_by_clause_1 | group_by_clause_2

group_by_clause_1: 
  GROUP BY group_expression [ , ... ] [ WITH ROLLUP | WITH CUBE ] 
 
group_by_clause_2: 
  GROUP BY { group_expression | { ROLLUP | CUBE | GROUPING SETS } ( grouping_set [ , ... ] ) } [ , ... ]

grouping_set: 
  { expression | ( [ expression [ , ... ] ] ) }
 
groupByQuery: SELECT expression [ , ... ] FROM src groupByClause?
`

In group_expression, columns can be also specified by position number. But please remember:

`group_expression`
* For Hive 0.11.0 through 2.1.x, set hive.groupby.orderby.position.alias to true (the default is false)
* For Hive 2.2.0 and later, set hive.groupby.position.alias to true (the default is false)
`hive.groupby.orderby.position.alias`
`hive.groupby.position.alias`

## Parameters#


### GROUPING SETS#


GROUPING SETS allow for more complex grouping operations than those describable by a standard GROUP BY.
Rows are grouped separately by each specified grouping set and aggregates are computed for each group just as for simple GROUP BY clauses.

`GROUPING SETS`
`GROUP BY`
`GROUP BY`

All GROUPING SET clauses can be logically expressed in terms of several GROUP BY queries connected by UNION.

`GROUPING SET`
`GROUP BY`
`UNION`

For example:


```
SELECT a, b, SUM( c ) FROM tab1 GROUP BY a, b GROUPING SETS ( (a, b), a, b, ( ) )

```

`SELECT a, b, SUM( c ) FROM tab1 GROUP BY a, b GROUPING SETS ( (a, b), a, b, ( ) )
`

is equivalent to


```
SELECT a, b, SUM( c ) FROM tab1 GROUP BY a, b
UNION
SELECT a, null, SUM( c ) FROM tab1 GROUP BY a, null
UNION
SELECT null, b, SUM( c ) FROM tab1 GROUP BY null, b
UNION
SELECT null, null, SUM( c ) FROM tab1

```

`SELECT a, b, SUM( c ) FROM tab1 GROUP BY a, b
UNION
SELECT a, null, SUM( c ) FROM tab1 GROUP BY a, null
UNION
SELECT null, b, SUM( c ) FROM tab1 GROUP BY null, b
UNION
SELECT null, null, SUM( c ) FROM tab1
`

When aggregates are displayed for a column its value is null. This may conflict in case the column itself has some null values.
There needs to be some way to identify NULL in column, which means aggregate and NULL in column, which means GROUPING__ID function is the solution to that.

`GROUPING__ID`

This function returns a bitvector corresponding to whether each column is present or not.
For each column, a value of “1” is produced for a row in the result set if that column has been aggregated in that row, otherwise the value is “0”.
This can be used to differentiate when there are nulls in the data.
For more details, please refer to Hive’s docs Grouping__ID function.


Also, there’s Grouping function indicates whether an expression in a GROUP BY clause is aggregated or not for a given row.
The value 0 represents a column that is part of the grouping set, while the value 1 represents a column that is not part of the grouping set.

`GROUP BY`

### ROLLUP#


ROLLUP is a shorthand notation for specifying a common type of grouping set.
It represents the given list of expressions and all prefixes of the list, including the empty list.
For example:

`ROLLUP`

```
GROUP BY a, b, c WITH ROLLUP

```

`GROUP BY a, b, c WITH ROLLUP
`

is equivalent to


```
GROUP BY a, b, c GROUPING SETS ( (a, b, c), (a, b), (a), ( )).

```

`GROUP BY a, b, c GROUPING SETS ( (a, b, c), (a, b), (a), ( )).
`

### CUBE#


CUBE is a shorthand notation for specifying a common type of grouping set.
It represents the given list and all of its possible subsets - the power set.

`CUBE`

For example:


```
GROUP BY a, b, c WITH CUBE

```

`GROUP BY a, b, c WITH CUBE
`

is equivalent to


```
GROUP BY a, b, c GROUPING SETS ( (a, b, c), (a, b), (b, c), (a, c), (a), (b), (c), ( ))

```

`GROUP BY a, b, c GROUPING SETS ( (a, b, c), (a, b), (b, c), (a, c), (a), (b), (c), ( ))
`

## Examples#


```
-- use group by expression
SELECT abs(x), sum(y) FROM t GROUP BY abs(x);

-- use group by column
SELECT x, sum(y) FROM t GROUP BY x;

-- use group by position
SELECT x, sum(y) FROM t GROUP BY 1; -- group by first column in the table;

-- use grouping sets
SELECT x, SUM(y) FROM t GROUP BY x GROUPING SETS ( x, ( ) );

-- use rollup
SELECT x, SUM(y) FROM t GROUP BY x WITH ROLLUP;
SELECT x, SUM(y) FROM t GROUP BY ROLLUP (x);

-- use cube
SELECT x, SUM(y) FROM t GROUP BY x WITH CUBE;
SELECT x, SUM(y) FROM t GROUP BY CUBE (x);

```

`-- use group by expression
SELECT abs(x), sum(y) FROM t GROUP BY abs(x);

-- use group by column
SELECT x, sum(y) FROM t GROUP BY x;

-- use group by position
SELECT x, sum(y) FROM t GROUP BY 1; -- group by first column in the table;

-- use grouping sets
SELECT x, SUM(y) FROM t GROUP BY x GROUPING SETS ( x, ( ) );

-- use rollup
SELECT x, SUM(y) FROM t GROUP BY x WITH ROLLUP;
SELECT x, SUM(y) FROM t GROUP BY ROLLUP (x);

-- use cube
SELECT x, SUM(y) FROM t GROUP BY x WITH CUBE;
SELECT x, SUM(y) FROM t GROUP BY CUBE (x);
`