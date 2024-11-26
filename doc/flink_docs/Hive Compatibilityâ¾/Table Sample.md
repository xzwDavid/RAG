# Table Sample


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Table Sample#


## Description#


The TABLESAMPLE statement is used to sample rows from the table.

`TABLESAMPLE`

### Syntax#


```
TABLESAMPLE ( num_rows ROWS )

```

`TABLESAMPLE ( num_rows ROWS )
`

> 
Note:
Currently, only sample specific number of rows is supported.



### Parameters#

* 
num_rows ROWS
num_rows is a constant positive to specify how many rows to sample.


num_rows ROWS

`ROWS`

num_rows is a constant positive to specify how many rows to sample.


### Examples#


```
SELECT * FROM src TABLESAMPLE (5 ROWS)

```

`SELECT * FROM src TABLESAMPLE (5 ROWS)
`