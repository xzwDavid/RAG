# DataGen


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# DataGen SQL Connector#



Scan Source: Bounded
Scan Source: UnBounded


The DataGen connector allows for creating tables based on in-memory data generation.
This is useful when developing queries locally without access to external systems such as Kafka.
Tables can include Computed Column syntax which allows for flexible record generation.


The DataGen connector is built-in, no additional dependencies are required.


## Usage#


By default, a DataGen table will create an unbounded number of rows with a random value for each column.
Additionally, a total number of rows can be specified, resulting in a bounded table.


The DataGen connector can generate data that conforms to its defined schema, It should be noted that it handles length-constrained fields as follows:

* For fixed-length data types (char/binary), the field length can only be defined by the schema,
and does not support customization.
* For variable-length data types (varchar/varbinary), the field length is initially defined by the schema,
and the customized length cannot be greater than the schema definition.
* For super-long fields (string/bytes), the default length is 100, but can be set to a length less than 2^31.

There also exists a sequence generator, where users specify a sequence of start and end values.
If any column in a table is a sequence type, the table will be bounded and end with the first sequence completes.


Time types are always the local machines current system time.


```
CREATE TABLE Orders (
    order_number BIGINT,
    price        DECIMAL(32,2),
    buyer        ROW<first_name STRING, last_name STRING>,
    order_time   TIMESTAMP(3)
) WITH (
  'connector' = 'datagen'
)

```

`CREATE TABLE Orders (
    order_number BIGINT,
    price        DECIMAL(32,2),
    buyer        ROW<first_name STRING, last_name STRING>,
    order_time   TIMESTAMP(3)
) WITH (
  'connector' = 'datagen'
)
`

Often, the data generator connector is used in conjunction with the LIKE clause to mock out physical tables.

`LIKE`

```
CREATE TABLE Orders (
    order_number BIGINT,
    price        DECIMAL(32,2),
    buyer        ROW<first_name STRING, last_name STRING>,
    order_time   TIMESTAMP(3)
) WITH (...)

-- create a bounded mock table
CREATE TEMPORARY TABLE GenOrders
WITH (
    'connector' = 'datagen',
    'number-of-rows' = '10'
)
LIKE Orders (EXCLUDING ALL)

```

`CREATE TABLE Orders (
    order_number BIGINT,
    price        DECIMAL(32,2),
    buyer        ROW<first_name STRING, last_name STRING>,
    order_time   TIMESTAMP(3)
) WITH (...)

-- create a bounded mock table
CREATE TEMPORARY TABLE GenOrders
WITH (
    'connector' = 'datagen',
    'number-of-rows' = '10'
)
LIKE Orders (EXCLUDING ALL)
`

Furthermore, for variable sized types, varchar/string/varbinary/bytes, you can specify whether to enable variable-length data generation.


```
CREATE TABLE Orders (
    order_number BIGINT,
    price        DECIMAL(32,2),
    buyer        ROW<first_name STRING, last_name STRING>,
    order_time   TIMESTAMP(3),
    seller       VARCHAR(150)
) WITH (
  'connector' = 'datagen',
  'fields.seller.var-len' = 'true'
)

```

`CREATE TABLE Orders (
    order_number BIGINT,
    price        DECIMAL(32,2),
    buyer        ROW<first_name STRING, last_name STRING>,
    order_time   TIMESTAMP(3),
    seller       VARCHAR(150)
) WITH (
  'connector' = 'datagen',
  'fields.seller.var-len' = 'true'
)
`

## Types#


## Connector Options#


##### connector


##### rows-per-second


##### number-of-rows


##### scan.parallelism


##### fields.#.kind


##### fields.#.min


##### fields.#.max


##### fields.#.max-past


##### fields.#.length


##### fields.#.var-len


##### fields.#.start


##### fields.#.end


##### fields.#.null-rate
