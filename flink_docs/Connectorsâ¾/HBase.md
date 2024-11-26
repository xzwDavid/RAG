# HBase


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# HBase SQL Connector#



Scan Source: Bounded
Lookup Source: Sync Mode
Sink: Batch
Sink: Streaming Upsert Mode


The HBase connector allows for reading from and writing to an HBase cluster. This document describes how to setup the HBase Connector to run SQL queries against HBase.


HBase always works in upsert mode for exchange changelog messages with the external system using a primary key defined on the DDL. The primary key must be defined on the HBase rowkey field (rowkey field must be declared). If the PRIMARY KEY clause is not declared, the HBase connector will take rowkey as the primary key by default.


## Dependencies#


Only available for stable versions.


The HBase connector is not part of the binary distribution.
See how to link with it for cluster execution here.


## How to use HBase table#


All the column families in HBase table must be declared as ROW type, the field name maps to the column family name, and the nested field names map to the column qualifier names. There is no need to declare all the families and qualifiers in the schema, users can declare whatâs used in the query. Except the ROW type fields, the single atomic type field (e.g. STRING, BIGINT) will be recognized as HBase rowkey. The rowkey field can be arbitrary name, but should be quoted using backticks if it is a reserved keyword.


```
-- register the HBase table 'mytable' in Flink SQL
CREATE TABLE hTable (
 rowkey INT,
 family1 ROW<q1 INT>,
 family2 ROW<q2 STRING, q3 BIGINT>,
 family3 ROW<q4 DOUBLE, q5 BOOLEAN, q6 STRING>,
 PRIMARY KEY (rowkey) NOT ENFORCED
) WITH (
 'connector' = 'hbase-1.4',
 'table-name' = 'mytable',
 'zookeeper.quorum' = 'localhost:2181'
);

-- use ROW(...) construction function construct column families and write data into the HBase table.
-- assuming the schema of "T" is [rowkey, f1q1, f2q2, f2q3, f3q4, f3q5, f3q6]
INSERT INTO hTable
SELECT rowkey, ROW(f1q1), ROW(f2q2, f2q3), ROW(f3q4, f3q5, f3q6) FROM T;

-- scan data from the HBase table
SELECT rowkey, family1, family3.q4, family3.q6 FROM hTable;

-- temporal join the HBase table as a dimension table
SELECT * FROM myTopic
LEFT JOIN hTable FOR SYSTEM_TIME AS OF myTopic.proctime
ON myTopic.key = hTable.rowkey;

```

`-- register the HBase table 'mytable' in Flink SQL
CREATE TABLE hTable (
 rowkey INT,
 family1 ROW<q1 INT>,
 family2 ROW<q2 STRING, q3 BIGINT>,
 family3 ROW<q4 DOUBLE, q5 BOOLEAN, q6 STRING>,
 PRIMARY KEY (rowkey) NOT ENFORCED
) WITH (
 'connector' = 'hbase-1.4',
 'table-name' = 'mytable',
 'zookeeper.quorum' = 'localhost:2181'
);

-- use ROW(...) construction function construct column families and write data into the HBase table.
-- assuming the schema of "T" is [rowkey, f1q1, f2q2, f2q3, f3q4, f3q5, f3q6]
INSERT INTO hTable
SELECT rowkey, ROW(f1q1), ROW(f2q2, f2q3), ROW(f3q4, f3q5, f3q6) FROM T;

-- scan data from the HBase table
SELECT rowkey, family1, family3.q4, family3.q6 FROM hTable;

-- temporal join the HBase table as a dimension table
SELECT * FROM myTopic
LEFT JOIN hTable FOR SYSTEM_TIME AS OF myTopic.proctime
ON myTopic.key = hTable.rowkey;
`

## Available Metadata#


The following connector metadata can be accessed as metadata columns in a table definition.


The R/W column defines whether a metadata field is readable (R) and/or writable (W).
Read-only columns must be declared VIRTUAL to exclude them during an INSERT INTO operation.

`R/W`
`R`
`W`
`VIRTUAL`
`INSERT INTO`
`timestamp`
`TIMESTAMP_LTZ(3) NOT NULL`
`W`
`ttl`
`BIGINT NOT NULL`
`W`

## Connector Options#


##### connector

* hbase-1.4: connect to HBase 1.4.x cluster
* hbase-2.2: connect to HBase 2.2.x cluster
`hbase-1.4`
`hbase-2.2`

##### table-name


##### zookeeper.quorum


##### zookeeper.znode.parent


##### null-string-literal


##### sink.buffer-flush.max-size

`'0'`

##### sink.buffer-flush.max-rows

`'0'`

##### sink.buffer-flush.interval

`'0'`
`'sink.buffer-flush.max-size'`
`'sink.buffer-flush.max-rows'`
`'0'`

##### sink.ignore-null-value


##### sink.parallelism


##### lookup.async


##### lookup.cache


Enum


##### lookup.partial-cache.max-rows


##### lookup.partial-cache.expire-after-write


##### lookup.partial-cache.expire-after-access


##### lookup.partial-cache.caching-missing-key


##### lookup.max-retries


##### properties.*

`'properties.hbase.security.authentication' = 'kerberos'`

### Deprecated Options#


These deprecated options has been replaced by new options listed above and will be removed eventually. Please consider using new options first.


##### lookup.cache.max-rows


##### lookup.cache.ttl


## Data Type Mapping#


HBase stores all data as byte arrays. The data needs to be serialized and deserialized during read and write operation


When serializing and de-serializing, Flink HBase connector uses utility class org.apache.hadoop.hbase.util.Bytes provided by HBase (Hadoop) to convert Flink Data Types to and from byte arrays.

`org.apache.hadoop.hbase.util.Bytes`

Flink HBase connector encodes null values to empty bytes, and decode empty bytes to null values for all data types except string type. For string type, the null literal is determined by null-string-literal option.

`null`
`null`
`null-string-literal`

The data type mappings are as follows:

`CHAR / VARCHAR / STRING`

```
byte[] toBytes(String s)
String toString(byte[] b)
```

`byte[] toBytes(String s)
String toString(byte[] b)`
`BOOLEAN`

```
byte[] toBytes(boolean b)
boolean toBoolean(byte[] b)
```

`byte[] toBytes(boolean b)
boolean toBoolean(byte[] b)`
`BINARY / VARBINARY`
`byte[]`
`DECIMAL`

```
byte[] toBytes(BigDecimal v)
BigDecimal toBigDecimal(byte[] b)
```

`byte[] toBytes(BigDecimal v)
BigDecimal toBigDecimal(byte[] b)`
`TINYINT`

```
new byte[] { val }
bytes[0] // returns first and only byte from bytes

```

`new byte[] { val }
bytes[0] // returns first and only byte from bytes
`
`SMALLINT`

```
byte[] toBytes(short val)
short toShort(byte[] bytes)
```

`byte[] toBytes(short val)
short toShort(byte[] bytes)`
`INT`

```
byte[] toBytes(int val)
int toInt(byte[] bytes)
```

`byte[] toBytes(int val)
int toInt(byte[] bytes)`
`BIGINT`

```
byte[] toBytes(long val)
long toLong(byte[] bytes)
```

`byte[] toBytes(long val)
long toLong(byte[] bytes)`
`FLOAT`

```
byte[] toBytes(float val)
float toFloat(byte[] bytes)
```

`byte[] toBytes(float val)
float toFloat(byte[] bytes)`
`DOUBLE`

```
byte[] toBytes(double val)
double toDouble(byte[] bytes)
```

`byte[] toBytes(double val)
double toDouble(byte[] bytes)`
`DATE`
`TIME`
`TIMESTAMP`
`ARRAY`
`MAP / MULTISET`
`ROW`

 Back to top
