# Print


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Print SQL Connector#


The Print connector allows for writing every row to the standard output or standard error stream.


It is designed for:

* Easy test for streaming job.
* Very useful in production debugging.

Four possible format options:


##### PRINT_IDENTIFIER:taskId> output


##### PRINT_IDENTIFIER> output


##### taskId> output


##### output


The output string format is “$row_kind(f0,f1,f2…)”, row_kind is the short string of RowKind, example is: “+I(1,1)”.

`RowKind`

The Print connector is built-in.


Attention Print sinks print records in runtime tasks, you need to observe the task log.


## How to create a Print table#


```
CREATE TABLE print_table (
  f0 INT,
  f1 INT,
  f2 STRING,
  f3 DOUBLE
) WITH (
  'connector' = 'print'
);

```

`CREATE TABLE print_table (
  f0 INT,
  f1 INT,
  f2 STRING,
  f3 DOUBLE
) WITH (
  'connector' = 'print'
);
`

Alternatively, it may be based on  an existing schema using the LIKE Clause.


```
CREATE TABLE print_table WITH ('connector' = 'print')
LIKE source_table (EXCLUDING ALL)

```

`CREATE TABLE print_table WITH ('connector' = 'print')
LIKE source_table (EXCLUDING ALL)
`

## Connector Options#


##### connector


##### print-identifier


##### standard-error


##### sink.parallelism
