# Set Operations


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Set Operations#


Set Operations are used to combine multiple SELECT statements into a single result set.
Hive dialect supports the following operations:

`SELECT`
* UNION
* INTERSECT
* EXCEPT/MINUS

## UNION#


### Description#


UNION/UNION DISTINCT/UNION ALL returns the rows that are found in either side.

`UNION`
`UNION DISTINCT`
`UNION ALL`

UNION and UNION DISTINCT only returns the distinct rows, while UNION ALL does not duplicate.

`UNION`
`UNION DISTINCT`
`UNION ALL`

### Syntax#


```
<query> { UNION [ ALL | DISTINCT ] } <query> [ .. ]

```

`<query> { UNION [ ALL | DISTINCT ] } <query> [ .. ]
`

### Examples#


```
SELECT x, y FROM t1 UNION DISTINCT SELECT x, y FROM t2;
SELECT x, y FROM t1 UNION SELECT x, y FROM t2;
SELECT x, y FROM t1 UNION ALL SELECT x, y FROM t2;

```

`SELECT x, y FROM t1 UNION DISTINCT SELECT x, y FROM t2;
SELECT x, y FROM t1 UNION SELECT x, y FROM t2;
SELECT x, y FROM t1 UNION ALL SELECT x, y FROM t2;
`

## INTERSECT#


### Description#


INTERSECT/INTERSECT DISTINCT/INTERSECT ALL returns the rows that are found in both side.

`INTERSECT`
`INTERSECT DISTINCT`
`INTERSECT ALL`

INTERSECT/INTERSECT DISTINCT only returns the distinct rows, while INTERSECT ALL does not duplicate.

`INTERSECT`
`INTERSECT DISTINCT`
`INTERSECT ALL`

### Syntax#


```
<query> { INTERSECT [ ALL | DISTINCT ] } <query> [ .. ]

```

`<query> { INTERSECT [ ALL | DISTINCT ] } <query> [ .. ]
`

### Examples#


```
SELECT x, y FROM t1 INTERSECT DISTINCT SELECT x, y FROM t2;
SELECT x, y FROM t1 INTERSECT SELECT x, y FROM t2;
SELECT x, y FROM t1 INTERSECT ALL SELECT x, y FROM t2;

```

`SELECT x, y FROM t1 INTERSECT DISTINCT SELECT x, y FROM t2;
SELECT x, y FROM t1 INTERSECT SELECT x, y FROM t2;
SELECT x, y FROM t1 INTERSECT ALL SELECT x, y FROM t2;
`

## EXCEPT/MINUS#


### Description#


EXCEPT/EXCEPT DISTINCT/EXCEPT ALL returns the rows that are found in left side but not in right side.

`EXCEPT`
`EXCEPT DISTINCT`
`EXCEPT ALL`

EXCEPT/EXCEPT DISTINCT only returns the distinct rows, while EXCEPT ALL does not duplicate.

`EXCEPT`
`EXCEPT DISTINCT`
`EXCEPT ALL`

MINUS is synonym for EXCEPT.

`MINUS`
`EXCEPT`

### Syntax#


```
<query> { EXCEPT [ ALL | DISTINCT ] } <query> [ .. ]

```

`<query> { EXCEPT [ ALL | DISTINCT ] } <query> [ .. ]
`

### Examples#


```
SELECT x, y FROM t1 EXCEPT DISTINCT SELECT x, y FROM t2;
SELECT x, y FROM t1 EXCEPT SELECT x, y FROM t2;
SELECT x, y FROM t1 EXCEPT ALL SELECT x, y FROM t2;

```

`SELECT x, y FROM t1 EXCEPT DISTINCT SELECT x, y FROM t2;
SELECT x, y FROM t1 EXCEPT SELECT x, y FROM t2;
SELECT x, y FROM t1 EXCEPT ALL SELECT x, y FROM t2;
`