# Sort/Cluster/Distributed By


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Sort/Cluster/Distributed by Clause#


## Sort By#


### Description#


Unlike ORDER BY which guarantees a total order of output,
SORT BY only guarantees the result rows with each partition is in the user specified order.
So when there’s more than one partition, SORT BY may return result that’s partially ordered.

`SORT BY`
`SORT BY`

### Syntax#


```
query: SELECT expression [ , ... ] FROM src sortBy
sortBy: SORT BY expression colOrder [ , ... ] 
colOrder: ( ASC | DESC )

```

`query: SELECT expression [ , ... ] FROM src sortBy
sortBy: SORT BY expression colOrder [ , ... ] 
colOrder: ( ASC | DESC )
`

### Parameters#

* 
colOrder
it’s used specified the order of returned rows. The default order is ASC.


colOrder


it’s used specified the order of returned rows. The default order is ASC.

`ASC`

### Examples#


```
SELECT x, y FROM t SORT BY x;
SELECT x, y FROM t SORT BY abs(y) DESC;

```

`SELECT x, y FROM t SORT BY x;
SELECT x, y FROM t SORT BY abs(y) DESC;
`

## Distribute By#


### Description#


The DISTRIBUTE BY clause is used to repartition the data.
The data with same value evaluated by the specified expression will be in same partition.

`DISTRIBUTE BY`

### Syntax#


```
distributeBy: DISTRIBUTE BY expression [ , ... ]
query: SELECT expression [ , ... ] FROM src distributeBy

```

`distributeBy: DISTRIBUTE BY expression [ , ... ]
query: SELECT expression [ , ... ] FROM src distributeBy
`

### Examples#


```
-- only use DISTRIBUTE BY clause
SELECT x, y FROM t DISTRIBUTE BY x;
SELECT x, y FROM t DISTRIBUTE BY abs(y);

-- use both DISTRIBUTE BY and SORT BY clause
SELECT x, y FROM t DISTRIBUTE BY x SORT BY y DESC;

```

`-- only use DISTRIBUTE BY clause
SELECT x, y FROM t DISTRIBUTE BY x;
SELECT x, y FROM t DISTRIBUTE BY abs(y);

-- use both DISTRIBUTE BY and SORT BY clause
SELECT x, y FROM t DISTRIBUTE BY x SORT BY y DESC;
`

## Cluster By#


### Description#


CLUSTER BY is a short-cut for both DISTRIBUTE BY and SORT BY.
The CLUSTER BY is used to first repartition the data based on the input expressions and sort the data with each partition.
Also, this clause only guarantees the data is sorted within each partition.

`CLUSTER BY`
`DISTRIBUTE BY`
`SORT BY`
`CLUSTER BY`

### Syntax#


```
clusterBy: CLUSTER BY expression [ , ... ]
query: SELECT expression [ , ... ] FROM src clusterBy

```

`clusterBy: CLUSTER BY expression [ , ... ]
query: SELECT expression [ , ... ] FROM src clusterBy
`

### Examples#


```
SELECT x, y FROM t CLUSTER BY x;
SELECT x, y FROM t CLUSTER BY abs(y);

```

`SELECT x, y FROM t CLUSTER BY x;
SELECT x, y FROM t CLUSTER BY abs(y);
`