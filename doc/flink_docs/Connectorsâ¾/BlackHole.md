# BlackHole


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# BlackHole SQL Connector#



Sink: Bounded
Sink: UnBounded


The BlackHole connector allows for swallowing all input records. It is designed for:

* high performance testing.
* UDF to output, not substantive sink.

Just like /dev/null device on Unix-like operating systems.


The BlackHole connector is built-in.


## How to create a BlackHole table#


```
CREATE TABLE blackhole_table (
  f0 INT,
  f1 INT,
  f2 STRING,
  f3 DOUBLE
) WITH (
  'connector' = 'blackhole'
);

```

`CREATE TABLE blackhole_table (
  f0 INT,
  f1 INT,
  f2 STRING,
  f3 DOUBLE
) WITH (
  'connector' = 'blackhole'
);
`

Alternatively, it may be based on an existing schema using the LIKE Clause.


```
CREATE TABLE blackhole_table WITH ('connector' = 'blackhole')
LIKE source_table (EXCLUDING ALL)

```

`CREATE TABLE blackhole_table WITH ('connector' = 'blackhole')
LIKE source_table (EXCLUDING ALL)
`

## Connector Options#


##### connector
