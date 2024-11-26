# Data Types


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Data Types#


Flink SQL has a rich set of native data types available to users.


## Data Type#


A data type describes the logical type of a value in the table ecosystem.
It can be used to declare input and/or output types of operations.


Flink’s data types are similar to the SQL standard’s data type terminology but also contain information
about the nullability of a value for efficient handling of scalar expressions.


Examples of data types are:

* INT
* INT NOT NULL
* INTERVAL DAY TO SECOND(3)
* ROW<myField ARRAY<BOOLEAN>, myOtherField TIMESTAMP(3)>
`INT`
`INT NOT NULL`
`INTERVAL DAY TO SECOND(3)`
`ROW<myField ARRAY<BOOLEAN>, myOtherField TIMESTAMP(3)>`

A list of all pre-defined data types can be found below.


### Data Types in the Table API#


Users of the JVM-based API work with instances of org.apache.flink.table.types.DataType within the Table API or when
defining connectors, catalogs, or user-defined functions.

`org.apache.flink.table.types.DataType`

A DataType instance has two responsibilities:

`DataType`
* Declaration of a logical type which does not imply a concrete physical representation for transmission
or storage but defines the boundaries between JVM-based/Python languages and the table ecosystem.
* Optional: Giving hints about the physical representation of data to the planner which is useful at the edges to other APIs.

For JVM-based languages, all pre-defined data types are available in org.apache.flink.table.api.DataTypes.

`org.apache.flink.table.api.DataTypes`

Users of the Python API work with instances of pyflink.table.types.DataType within the Python Table API or when
defining Python user-defined functions.

`pyflink.table.types.DataType`

A DataType instance has such a responsibility:

`DataType`
* Declaration of a logical type which does not imply a concrete physical representation for transmission
or storage but defines the boundaries between Python languages and the table ecosystem.

For Python language, those types are available in pyflink.table.types.DataTypes.

`pyflink.table.types.DataTypes`

It is recommended to add a star import to your table programs for having a fluent API:


```
import static org.apache.flink.table.api.DataTypes.*;

DataType t = INTERVAL(DAY(), SECOND(3));

```

`import static org.apache.flink.table.api.DataTypes.*;

DataType t = INTERVAL(DAY(), SECOND(3));
`

It is recommended to add a star import to your table programs for having a fluent API:


```
import org.apache.flink.table.api.DataTypes._

val t: DataType = INTERVAL(DAY(), SECOND(3))

```

`import org.apache.flink.table.api.DataTypes._

val t: DataType = INTERVAL(DAY(), SECOND(3))
`

```
from pyflink.table.types import DataTypes

t = DataTypes.INTERVAL(DataTypes.DAY(), DataTypes.SECOND(3))

```

`from pyflink.table.types import DataTypes

t = DataTypes.INTERVAL(DataTypes.DAY(), DataTypes.SECOND(3))
`

#### Physical Hints#


Physical hints are required at the edges of the table ecosystem where the SQL-based type system ends and
programming-specific data types are required. Hints indicate the data format that an implementation
expects.


For example, a data source could express that it produces values for logical TIMESTAMPs using a java.sql.Timestamp class
instead of using java.time.LocalDateTime which would be the default. With this information, the runtime is able to convert
the produced class into its internal data format. In return, a data sink can declare the data format it consumes from the runtime.

`TIMESTAMP`
`java.sql.Timestamp`
`java.time.LocalDateTime`

Here are some examples of how to declare a bridging conversion class:


```
// tell the runtime to not produce or consume java.time.LocalDateTime instances
// but java.sql.Timestamp
DataType t = DataTypes.TIMESTAMP(3).bridgedTo(java.sql.Timestamp.class);

// tell the runtime to not produce or consume boxed integer arrays
// but primitive int arrays
DataType t = DataTypes.ARRAY(DataTypes.INT().notNull()).bridgedTo(int[].class);

```

`// tell the runtime to not produce or consume java.time.LocalDateTime instances
// but java.sql.Timestamp
DataType t = DataTypes.TIMESTAMP(3).bridgedTo(java.sql.Timestamp.class);

// tell the runtime to not produce or consume boxed integer arrays
// but primitive int arrays
DataType t = DataTypes.ARRAY(DataTypes.INT().notNull()).bridgedTo(int[].class);
`

```
// tell the runtime to not produce or consume java.time.LocalDateTime instances
// but java.sql.Timestamp
val t: DataType = DataTypes.TIMESTAMP(3).bridgedTo(classOf[java.sql.Timestamp])

// tell the runtime to not produce or consume boxed integer arrays
// but primitive int arrays
val t: DataType = DataTypes.ARRAY(DataTypes.INT().notNull()).bridgedTo(classOf[Array[Int]])

```

`// tell the runtime to not produce or consume java.time.LocalDateTime instances
// but java.sql.Timestamp
val t: DataType = DataTypes.TIMESTAMP(3).bridgedTo(classOf[java.sql.Timestamp])

// tell the runtime to not produce or consume boxed integer arrays
// but primitive int arrays
val t: DataType = DataTypes.ARRAY(DataTypes.INT().notNull()).bridgedTo(classOf[Array[Int]])
`

Attention Please note that physical hints are usually only required if the
API is extended. Users of predefined sources/sinks/functions do not need to define such hints. Hints within
a table program (e.g. field.cast(TIMESTAMP(3).bridgedTo(Timestamp.class))) are ignored.

`field.cast(TIMESTAMP(3).bridgedTo(Timestamp.class))`

## List of Data Types#


This section lists all pre-defined data types.






Java/Scala
For the JVM-based Table API those types are also available in org.apache.flink.table.api.DataTypes.
Python
For the Python Table API, those types are available in pyflink.table.types.DataTypes.


`org.apache.flink.table.api.DataTypes`
`pyflink.table.types.DataTypes`

The default planner supports the following set of SQL types:

`CHAR`
`VARCHAR`
`STRING`
`BOOLEAN`
`BINARY`
`VARBINARY`
`BYTES`
`DECIMAL`
`TINYINT`
`SMALLINT`
`INTEGER`
`BIGINT`
`FLOAT`
`DOUBLE`
`DATE`
`TIME`
`0`
`TIMESTAMP`
`TIMESTAMP_LTZ`
`INTERVAL`
`MONTH`
`SECOND(3)`
`ARRAY`
`MULTISET`
`MAP`
`ROW`
`RAW`

### Character Strings#


#### CHAR#

`CHAR`

Data type of a fixed-length character string.


Declaration


```
CHAR
CHAR(n)

```

`CHAR
CHAR(n)
`

```
DataTypes.CHAR(n)

```

`DataTypes.CHAR(n)
`

Bridging to JVM Types

`java.lang.String`
`byte[]`
`org.apache.flink.table.data.StringData`

```
Not supported.

```

`Not supported.
`

The type can be declared using CHAR(n) where n is the number of code points. n must have a value between 1
and 2,147,483,647 (both inclusive). If no length is specified, n is equal to 1.

`CHAR(n)`
`n`
`n`
`1`
`2,147,483,647`
`n`
`1`

#### VARCHAR/STRING#

`VARCHAR`
`STRING`

Data type of a variable-length character string.


Declaration


```
VARCHAR
VARCHAR(n)

STRING

```

`VARCHAR
VARCHAR(n)

STRING
`

```
DataTypes.VARCHAR(n)

DataTypes.STRING()

```

`DataTypes.VARCHAR(n)

DataTypes.STRING()
`

Bridging to JVM Types

`java.lang.String`
`byte[]`
`org.apache.flink.table.data.StringData`

```
DataTypes.VARCHAR(n)

DataTypes.STRING()

```

`DataTypes.VARCHAR(n)

DataTypes.STRING()
`

Attention The specified maximum number of code points n in DataTypes.VARCHAR(n) must be 2,147,483,647 currently.

`n`
`DataTypes.VARCHAR(n)`
`2,147,483,647`

The type can be declared using VARCHAR(n) where n is the maximum number of code points. n must have a value
between 1 and 2,147,483,647 (both inclusive). If no length is specified, n is equal to 1.

`VARCHAR(n)`
`n`
`n`
`1`
`2,147,483,647`
`n`
`1`

STRING is a synonym for VARCHAR(2147483647).

`STRING`
`VARCHAR(2147483647)`

### Binary Strings#


#### BINARY#

`BINARY`

Data type of a fixed-length binary string (=a sequence of bytes).


Declaration


```
BINARY
BINARY(n)

```

`BINARY
BINARY(n)
`

```
DataTypes.BINARY(n)

```

`DataTypes.BINARY(n)
`

Bridging to JVM Types

`byte[]`

```
Not supported.

```

`Not supported.
`

The type can be declared using BINARY(n) where n is the number of bytes. n must have a value
between 1 and 2,147,483,647 (both inclusive). If no length is specified, n is equal to 1.

`BINARY(n)`
`n`
`n`
`1`
`2,147,483,647`
`n`
`1`

#### VARBINARY/BYTES#

`VARBINARY`
`BYTES`

Data type of a variable-length binary string (=a sequence of bytes).


Declaration


```
VARBINARY
VARBINARY(n)

BYTES

```

`VARBINARY
VARBINARY(n)

BYTES
`

```
DataTypes.VARBINARY(n)

DataTypes.BYTES()

```

`DataTypes.VARBINARY(n)

DataTypes.BYTES()
`

Bridging to JVM Types

`byte[]`

```
DataTypes.VARBINARY(n)

DataTypes.BYTES()

```

`DataTypes.VARBINARY(n)

DataTypes.BYTES()
`

Attention The specified maximum number of bytes n in DataTypes.VARBINARY(n) must be 2,147,483,647 currently.

`n`
`DataTypes.VARBINARY(n)`
`2,147,483,647`

The type can be declared using VARBINARY(n) where n is the maximum number of bytes. n must
have a value between 1 and 2,147,483,647 (both inclusive). If no length is specified, n is
equal to 1.

`VARBINARY(n)`
`n`
`n`
`1`
`2,147,483,647`
`n`
`1`

BYTES is a synonym for VARBINARY(2147483647).

`BYTES`
`VARBINARY(2147483647)`

### Exact Numerics#


#### DECIMAL#

`DECIMAL`

Data type of a decimal number with fixed precision and scale.


Declaration


```
DECIMAL
DECIMAL(p)
DECIMAL(p, s)

DEC
DEC(p)
DEC(p, s)

NUMERIC
NUMERIC(p)
NUMERIC(p, s)

```

`DECIMAL
DECIMAL(p)
DECIMAL(p, s)

DEC
DEC(p)
DEC(p, s)

NUMERIC
NUMERIC(p)
NUMERIC(p, s)
`

```
DataTypes.DECIMAL(p, s)

```

`DataTypes.DECIMAL(p, s)
`

Bridging to JVM Types

`java.math.BigDecimal`
`org.apache.flink.table.data.DecimalData`

```
DataTypes.DECIMAL(p, s)

```

`DataTypes.DECIMAL(p, s)
`

Attention The precision and scale specified in DataTypes.DECIMAL(p, s) must be 38 and 18 separately currently.

`precision`
`scale`
`DataTypes.DECIMAL(p, s)`
`38`
`18`

The type can be declared using DECIMAL(p, s) where p is the number of digits in a
number (precision) and s is the number of digits to the right of the decimal point
in a number (scale). p must have a value between 1 and 38 (both inclusive). s
must have a value between 0 and p (both inclusive). The default value for p is 10.
The default value for s is 0.

`DECIMAL(p, s)`
`p`
`s`
`p`
`1`
`38`
`s`
`0`
`p`
`p`
`s`
`0`

NUMERIC(p, s) and DEC(p, s) are synonyms for this type.

`NUMERIC(p, s)`
`DEC(p, s)`

#### TINYINT#

`TINYINT`

Data type of a 1-byte signed integer with values from -128 to 127.

`-128`
`127`

Declaration


```
TINYINT

```

`TINYINT
`

```
DataTypes.TINYINT()

```

`DataTypes.TINYINT()
`

Bridging to JVM Types

`java.lang.Byte`
`byte`

```
DataTypes.TINYINT()

```

`DataTypes.TINYINT()
`

#### SMALLINT#

`SMALLINT`

Data type of a 2-byte signed integer with values from -32,768 to 32,767.

`-32,768`
`32,767`

Declaration


```
SMALLINT

```

`SMALLINT
`

```
DataTypes.SMALLINT()

```

`DataTypes.SMALLINT()
`

Bridging to JVM Types

`java.lang.Short`
`short`

```
DataTypes.SMALLINT()

```

`DataTypes.SMALLINT()
`

#### INT#

`INT`

Data type of a 4-byte signed integer with values from -2,147,483,648 to 2,147,483,647.

`-2,147,483,648`
`2,147,483,647`

Declaration


```
INT

INTEGER

```

`INT

INTEGER
`

```
DataTypes.INT()

```

`DataTypes.INT()
`

Bridging to JVM Types

`java.lang.Integer`
`int`

```
DataTypes.INT()

```

`DataTypes.INT()
`

INTEGER is a synonym for this type.

`INTEGER`

#### BIGINT#

`BIGINT`

Data type of an 8-byte signed integer with values from -9,223,372,036,854,775,808 to
9,223,372,036,854,775,807.

`-9,223,372,036,854,775,808`
`9,223,372,036,854,775,807`

Declaration


```
BIGINT

```

`BIGINT
`

```
DataTypes.BIGINT()

```

`DataTypes.BIGINT()
`

Bridging to JVM Types

`java.lang.Long`
`long`

```
DataTypes.BIGINT()

```

`DataTypes.BIGINT()
`

### Approximate Numerics#


#### FLOAT#

`FLOAT`

Data type of a 4-byte single precision floating point number.


Compared to the SQL standard, the type does not take parameters.


Declaration


```
FLOAT

```

`FLOAT
`

```
DataTypes.FLOAT()

```

`DataTypes.FLOAT()
`

Bridging to JVM Types

`java.lang.Float`
`float`

```
DataTypes.FLOAT()

```

`DataTypes.FLOAT()
`

#### DOUBLE#

`DOUBLE`

Data type of an 8-byte double precision floating point number.


Declaration


```
DOUBLE

DOUBLE PRECISION

```

`DOUBLE

DOUBLE PRECISION
`

```
DataTypes.DOUBLE()

```

`DataTypes.DOUBLE()
`

Bridging to JVM Types

`java.lang.Double`
`double`

```
DataTypes.DOUBLE()

```

`DataTypes.DOUBLE()
`

DOUBLE PRECISION is a synonym for this type.

`DOUBLE PRECISION`

### Date and Time#


#### DATE#

`DATE`

Data type of a date consisting of year-month-day with values ranging from 0000-01-01
to 9999-12-31.

`year-month-day`
`0000-01-01`
`9999-12-31`

Compared to the SQL standard, the range starts at year 0000.

`0000`

Declaration


```
DATE

```

`DATE
`

```
DataTypes.DATE()

```

`DataTypes.DATE()
`

Bridging to JVM Types

`java.time.LocalDate`
`java.sql.Date`
`java.lang.Integer`
`int`

```
DataTypes.DATE()

```

`DataTypes.DATE()
`

#### TIME#

`TIME`

Data type of a time without time zone consisting of hour:minute:second[.fractional] with
up to nanosecond precision and values ranging from 00:00:00.000000000 to
23:59:59.999999999.

`hour:minute:second[.fractional]`
`00:00:00.000000000`
`23:59:59.999999999`
`23:59:60`
`23:59:61`
`java.time.LocalTime`
`23:59:60`
`23:59:61`

Declaration


```
TIME
TIME(p)

```

`TIME
TIME(p)
`

```
DataTypes.TIME(p)

```

`DataTypes.TIME(p)
`

Bridging to JVM Types

`java.time.LocalTime`
`java.sql.Time`
`java.lang.Integer`
`int`
`java.lang.Long`
`long`

```
DataTypes.TIME(p)

```

`DataTypes.TIME(p)
`

Attention The precision specified in DataTypes.TIME(p) must be 0 currently.

`precision`
`DataTypes.TIME(p)`
`0`

The type can be declared using TIME(p) where p is the number of digits of fractional
seconds (precision). p must have a value between 0 and 9 (both inclusive). If no
precision is specified, p is equal to 0.

`TIME(p)`
`p`
`p`
`0`
`9`
`p`
`0`

#### TIMESTAMP#

`TIMESTAMP`

Data type of a timestamp without time zone consisting of year-month-day hour:minute:second[.fractional]
with up to nanosecond precision and values ranging from 0000-01-01 00:00:00.000000000 to
9999-12-31 23:59:59.999999999.

`year-month-day hour:minute:second[.fractional]`
`0000-01-01 00:00:00.000000000`
`9999-12-31 23:59:59.999999999`

Compared to the SQL standard, leap seconds (23:59:60 and 23:59:61) are not supported as
the semantics are closer to java.time.LocalDateTime.

`23:59:60`
`23:59:61`
`java.time.LocalDateTime`

A conversion from and to BIGINT (a JVM long type) is not supported as this would imply a time
zone. However, this type is time zone free. For more java.time.Instant-like semantics use
TIMESTAMP_LTZ.

`BIGINT`
`long`
`java.time.Instant`
`TIMESTAMP_LTZ`

Compared to the SQL standard, leap seconds (23:59:60 and 23:59:61) are not supported.

`23:59:60`
`23:59:61`

A conversion from and to BIGINT is not supported as this would imply a time zone.
However, this type is time zone free. If you have such a requirement please use TIMESTAMP_LTZ.

`BIGINT`
`TIMESTAMP_LTZ`

Declaration


```
TIMESTAMP
TIMESTAMP(p)

TIMESTAMP WITHOUT TIME ZONE
TIMESTAMP(p) WITHOUT TIME ZONE

```

`TIMESTAMP
TIMESTAMP(p)

TIMESTAMP WITHOUT TIME ZONE
TIMESTAMP(p) WITHOUT TIME ZONE
`

```
DataTypes.TIMESTAMP(p)

```

`DataTypes.TIMESTAMP(p)
`

Bridging to JVM Types

`java.time.LocalDateTime`
`java.sql.Timestamp`
`org.apache.flink.table.data.TimestampData`

```
DataTypes.TIMESTAMP(p)

```

`DataTypes.TIMESTAMP(p)
`

Attention The precision specified in DataTypes.TIMESTAMP(p) must be 3 currently.

`precision`
`DataTypes.TIMESTAMP(p)`
`3`

The type can be declared using TIMESTAMP(p) where p is the number of digits of fractional
seconds (precision). p must have a value between 0 and 9 (both inclusive). If no precision
is specified, p is equal to 6.

`TIMESTAMP(p)`
`p`
`p`
`0`
`9`
`p`
`6`

TIMESTAMP(p) WITHOUT TIME ZONE is a synonym for this type.

`TIMESTAMP(p) WITHOUT TIME ZONE`

#### TIMESTAMP WITH TIME ZONE#

`TIMESTAMP WITH TIME ZONE`

Data type of a timestamp with time zone consisting of year-month-day hour:minute:second[.fractional] zone
with up to nanosecond precision and values ranging from 0000-01-01 00:00:00.000000000 +14:59 to
9999-12-31 23:59:59.999999999 -14:59.

`year-month-day hour:minute:second[.fractional] zone`
`0000-01-01 00:00:00.000000000 +14:59`
`9999-12-31 23:59:59.999999999 -14:59`
`23:59:60`
`23:59:61`
`java.time.OffsetDateTime`
`23:59:60`
`23:59:61`

Compared to TIMESTAMP_LTZ, the time zone offset information is physically
stored in every datum. It is used individually for every computation, visualization, or communication
to external systems.

`TIMESTAMP_LTZ`

Declaration


```
TIMESTAMP WITH TIME ZONE
TIMESTAMP(p) WITH TIME ZONE

```

`TIMESTAMP WITH TIME ZONE
TIMESTAMP(p) WITH TIME ZONE
`

```
DataTypes.TIMESTAMP_WITH_TIME_ZONE(p)

```

`DataTypes.TIMESTAMP_WITH_TIME_ZONE(p)
`

Bridging to JVM Types

`java.time.OffsetDateTime`
`java.time.ZonedDateTime`

```
Not supported.

```

`Not supported.
`
`TIMESTAMP(p) WITH TIME ZONE`
`p`
`p`
`0`
`9`
`p`
`6`

#### TIMESTAMP_LTZ#

`TIMESTAMP_LTZ`

Data type of a timestamp with local time zone consisting of year-month-day hour:minute:second[.fractional] zone
with up to nanosecond precision and values ranging from 0000-01-01 00:00:00.000000000 +14:59 to
9999-12-31 23:59:59.999999999 -14:59.

`year-month-day hour:minute:second[.fractional] zone`
`0000-01-01 00:00:00.000000000 +14:59`
`9999-12-31 23:59:59.999999999 -14:59`

Leap seconds (23:59:60 and 23:59:61) are not supported as the semantics are closer to java.time.OffsetDateTime.

`23:59:60`
`23:59:61`
`java.time.OffsetDateTime`

Compared to TIMESTAMP WITH TIME ZONE, the time zone offset information is not stored physically
in every datum. Instead, the type assumes java.time.Instant semantics in UTC time zone at
the edges of the table ecosystem. Every datum is interpreted in the local time zone configured in
the current session for computation and visualization.

`TIMESTAMP WITH TIME ZONE`
`java.time.Instant`

Leap seconds (23:59:60 and 23:59:61) are not supported.

`23:59:60`
`23:59:61`

Compared to TIMESTAMP WITH TIME ZONE, the time zone offset information is not stored physically
in every datum.
Every datum is interpreted in the local time zone configured in the current session for computation and visualization.

`TIMESTAMP WITH TIME ZONE`

This type fills the gap between time zone free and time zone mandatory timestamp types by allowing
the interpretation of UTC timestamps according to the configured session time zone.


Declaration


```
TIMESTAMP_LTZ
TIMESTAMP_LTZ(p)

TIMESTAMP WITH LOCAL TIME ZONE
TIMESTAMP(p) WITH LOCAL TIME ZONE

```

`TIMESTAMP_LTZ
TIMESTAMP_LTZ(p)

TIMESTAMP WITH LOCAL TIME ZONE
TIMESTAMP(p) WITH LOCAL TIME ZONE
`

```
DataTypes.TIMESTAMP_LTZ(p)
DataTypes.TIMESTAMP_WITH_LOCAL_TIME_ZONE(p)

```

`DataTypes.TIMESTAMP_LTZ(p)
DataTypes.TIMESTAMP_WITH_LOCAL_TIME_ZONE(p)
`

Bridging to JVM Types

`java.time.Instant`
`java.lang.Integer`
`int`
`java.lang.Long`
`long`
`java.sql.Timestamp`
`org.apache.flink.table.data.TimestampData`

```
DataTypes.TIMESTAMP_LTZ(p)
DataTypes.TIMESTAMP_WITH_LOCAL_TIME_ZONE(p)

```

`DataTypes.TIMESTAMP_LTZ(p)
DataTypes.TIMESTAMP_WITH_LOCAL_TIME_ZONE(p)
`

Attention The precision specified in DataTypes.TIMESTAMP_LTZ(p) must be 3 currently.

`precision`
`DataTypes.TIMESTAMP_LTZ(p)`
`3`

The type can be declared using TIMESTAMP_LTZ(p) where p is the number
of digits of fractional seconds (precision). p must have a value between 0 and 9
(both inclusive). If no precision is specified, p is equal to 6.

`TIMESTAMP_LTZ(p)`
`p`
`p`
`0`
`9`
`p`
`6`

TIMESTAMP(p) WITH LOCAL TIME ZONE is a synonym for this type.

`TIMESTAMP(p) WITH LOCAL TIME ZONE`

#### INTERVAL YEAR TO MONTH#

`INTERVAL YEAR TO MONTH`

Data type for a group of year-month interval types.


The type must be parameterized to one of the following resolutions:

* interval of years,
* interval of years to months,
* or interval of months.

An interval of year-month consists of +years-months with values ranging from -9999-11 to
+9999-11.

`+years-months`
`-9999-11`
`+9999-11`

The value representation is the same for all types of resolutions. For example, an interval
of months of 50 is always represented in an interval-of-years-to-months format (with default
year precision): +04-02.

`+04-02`

Declaration


```
INTERVAL YEAR
INTERVAL YEAR(p)
INTERVAL YEAR(p) TO MONTH
INTERVAL MONTH

```

`INTERVAL YEAR
INTERVAL YEAR(p)
INTERVAL YEAR(p) TO MONTH
INTERVAL MONTH
`

```
DataTypes.INTERVAL(DataTypes.YEAR())
DataTypes.INTERVAL(DataTypes.YEAR(p))
DataTypes.INTERVAL(DataTypes.YEAR(p), DataTypes.MONTH())
DataTypes.INTERVAL(DataTypes.MONTH())

```

`DataTypes.INTERVAL(DataTypes.YEAR())
DataTypes.INTERVAL(DataTypes.YEAR(p))
DataTypes.INTERVAL(DataTypes.YEAR(p), DataTypes.MONTH())
DataTypes.INTERVAL(DataTypes.MONTH())
`

Bridging to JVM Types

`java.time.Period`
`days`
`java.lang.Integer`
`int`

```
DataTypes.INTERVAL(DataTypes.YEAR())
DataTypes.INTERVAL(DataTypes.YEAR(p))
DataTypes.INTERVAL(DataTypes.YEAR(p), DataTypes.MONTH())
DataTypes.INTERVAL(DataTypes.MONTH())

```

`DataTypes.INTERVAL(DataTypes.YEAR())
DataTypes.INTERVAL(DataTypes.YEAR(p))
DataTypes.INTERVAL(DataTypes.YEAR(p), DataTypes.MONTH())
DataTypes.INTERVAL(DataTypes.MONTH())
`

The type can be declared using the above combinations where p is the number of digits of years
(year precision). p must have a value between 1 and 4 (both inclusive). If no year precision
is specified, p is equal to 2.

`p`
`p`
`1`
`4`
`p`
`2`

#### INTERVAL DAY TO SECOND#

`INTERVAL DAY TO SECOND`

Data type for a group of day-time interval types.


The type must be parameterized to one of the following resolutions with up to nanosecond precision:

* interval of days,
* interval of days to hours,
* interval of days to minutes,
* interval of days to seconds,
* interval of hours,
* interval of hours to minutes,
* interval of hours to seconds,
* interval of minutes,
* interval of minutes to seconds,
* or interval of seconds.

An interval of day-time consists of +days hours:months:seconds.fractional with values ranging from
-999999 23:59:59.999999999 to +999999 23:59:59.999999999. The value representation is the same
for all types of resolutions. For example, an interval of seconds of 70 is always represented in
an interval-of-days-to-seconds format (with default precisions): +00 00:01:10.000000.

`+days hours:months:seconds.fractional`
`-999999 23:59:59.999999999`
`+999999 23:59:59.999999999`
`+00 00:01:10.000000`

Declaration


```
INTERVAL DAY
INTERVAL DAY(p1)
INTERVAL DAY(p1) TO HOUR
INTERVAL DAY(p1) TO MINUTE
INTERVAL DAY(p1) TO SECOND(p2)
INTERVAL HOUR
INTERVAL HOUR TO MINUTE
INTERVAL HOUR TO SECOND(p2)
INTERVAL MINUTE
INTERVAL MINUTE TO SECOND(p2)
INTERVAL SECOND
INTERVAL SECOND(p2)

```

`INTERVAL DAY
INTERVAL DAY(p1)
INTERVAL DAY(p1) TO HOUR
INTERVAL DAY(p1) TO MINUTE
INTERVAL DAY(p1) TO SECOND(p2)
INTERVAL HOUR
INTERVAL HOUR TO MINUTE
INTERVAL HOUR TO SECOND(p2)
INTERVAL MINUTE
INTERVAL MINUTE TO SECOND(p2)
INTERVAL SECOND
INTERVAL SECOND(p2)
`

```
DataTypes.INTERVAL(DataTypes.DAY())
DataTypes.INTERVAL(DataTypes.DAY(p1))
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.HOUR())
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.HOUR())
DataTypes.INTERVAL(DataTypes.HOUR(), DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.HOUR(), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.MINUTE(), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.SECOND())
DataTypes.INTERVAL(DataTypes.SECOND(p2))

```

`DataTypes.INTERVAL(DataTypes.DAY())
DataTypes.INTERVAL(DataTypes.DAY(p1))
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.HOUR())
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.HOUR())
DataTypes.INTERVAL(DataTypes.HOUR(), DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.HOUR(), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.MINUTE(), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.SECOND())
DataTypes.INTERVAL(DataTypes.SECOND(p2))
`

Bridging to JVM Types

`java.time.Duration`
`java.lang.Long`
`long`

```
DataTypes.INTERVAL(DataTypes.DAY())
DataTypes.INTERVAL(DataTypes.DAY(p1))
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.HOUR())
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.HOUR())
DataTypes.INTERVAL(DataTypes.HOUR(), DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.HOUR(), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.MINUTE(), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.SECOND())
DataTypes.INTERVAL(DataTypes.SECOND(p2))

```

`DataTypes.INTERVAL(DataTypes.DAY())
DataTypes.INTERVAL(DataTypes.DAY(p1))
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.HOUR())
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.DAY(p1), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.HOUR())
DataTypes.INTERVAL(DataTypes.HOUR(), DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.HOUR(), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.MINUTE())
DataTypes.INTERVAL(DataTypes.MINUTE(), DataTypes.SECOND(p2))
DataTypes.INTERVAL(DataTypes.SECOND())
DataTypes.INTERVAL(DataTypes.SECOND(p2))
`

The type can be declared using the above combinations where p1 is the number of digits of days
(day precision) and p2 is the number of digits of fractional seconds (fractional precision).
p1 must have a value between 1 and 6 (both inclusive). p2 must have a value between 0
and 9 (both inclusive). If no p1 is specified, it is equal to 2 by default. If no p2 is
specified, it is equal to 6 by default.

`p1`
`p2`
`p1`
`1`
`6`
`p2`
`0`
`9`
`p1`
`2`
`p2`
`6`

### Constructured Data Types#


#### ARRAY#

`ARRAY`

Data type of an array of elements with same subtype.


Compared to the SQL standard, the maximum cardinality of an array cannot be specified but is
fixed at 2,147,483,647. Also, any valid type is supported as a subtype.

`2,147,483,647`

Declaration


```
ARRAY<t>
t ARRAY

```

`ARRAY<t>
t ARRAY
`

```
DataTypes.ARRAY(t)

```

`DataTypes.ARRAY(t)
`

Bridging to JVM Types

`[]`
`java.util.List<t>`
`java.util.List<t>`
`org.apache.flink.table.data.ArrayData`

```
DataTypes.ARRAY(t)

```

`DataTypes.ARRAY(t)
`

The type can be declared using ARRAY<t> where t is the data type of the contained
elements.

`ARRAY<t>`
`t`

t ARRAY is a synonym for being closer to the SQL standard. For example, INT ARRAY is
equivalent to ARRAY<INT>.

`t ARRAY`
`INT ARRAY`
`ARRAY<INT>`

#### MAP#

`MAP`

Data type of an associative array that maps keys (including NULL) to values (including NULL). A map
cannot contain duplicate keys; each key can map to at most one value.

`NULL`
`NULL`

There is no restriction of element types; it is the responsibility of the user to ensure uniqueness.


The map type is an extension to the SQL standard.


Declaration


```
MAP<kt, vt>

```

`MAP<kt, vt>
`

```
DataTypes.MAP(kt, vt)

```

`DataTypes.MAP(kt, vt)
`

Bridging to JVM Types

`java.util.Map<kt, vt>`
`java.util.Map<kt, vt>`
`org.apache.flink.table.data.MapData`

```
DataTypes.MAP(kt, vt)

```

`DataTypes.MAP(kt, vt)
`

The type can be declared using MAP<kt, vt> where kt is the data type of the key elements
and vt is the data type of the value elements.

`MAP<kt, vt>`
`kt`
`vt`

#### MULTISET#

`MULTISET`

Data type of a multiset (=bag). Unlike a set, it allows for multiple instances for each of its
elements with a common subtype. Each unique value (including NULL) is mapped to some multiplicity.

`NULL`

There is no restriction of element types; it is the responsibility of the user to ensure uniqueness.


Declaration


```
MULTISET<t>
t MULTISET

```

`MULTISET<t>
t MULTISET
`

```
DataTypes.MULTISET(t)

```

`DataTypes.MULTISET(t)
`

Bridging to JVM Types

`java.util.Map<t, java.lang.Integer>`
`java.util.Map<t, java.lang.Integer>>`
`org.apache.flink.table.data.MapData`

```
DataTypes.MULTISET(t)

```

`DataTypes.MULTISET(t)
`

The type can be declared using MULTISET<t> where t is the data type
of the contained elements.

`MULTISET<t>`
`t`

t MULTISET is a synonym for being closer to the SQL standard. For example, INT MULTISET is
equivalent to MULTISET<INT>.

`t MULTISET`
`INT MULTISET`
`MULTISET<INT>`

#### ROW#

`ROW`

Data type of a sequence of fields.


A field consists of a field name, field type, and an optional description. The most specific type
of a row of a table is a row type. In this case, each column of the row corresponds to the field
of the row type that has the same ordinal position as the column.


Compared to the SQL standard, an optional field description simplifies the handling with complex
structures.


A row type is similar to the STRUCT type known from other non-standard-compliant frameworks.

`STRUCT`

Declaration


```
ROW<n0 t0, n1 t1, ...>
ROW<n0 t0 'd0', n1 t1 'd1', ...>

ROW(n0 t0, n1 t1, ...)
ROW(n0 t0 'd0', n1 t1 'd1', ...)

```

`ROW<n0 t0, n1 t1, ...>
ROW<n0 t0 'd0', n1 t1 'd1', ...>

ROW(n0 t0, n1 t1, ...)
ROW(n0 t0 'd0', n1 t1 'd1', ...)
`

```
DataTypes.ROW(DataTypes.FIELD(n0, t0), DataTypes.FIELD(n1, t1), ...)
DataTypes.ROW(DataTypes.FIELD(n0, t0, d0), DataTypes.FIELD(n1, t1, d1), ...)

```

`DataTypes.ROW(DataTypes.FIELD(n0, t0), DataTypes.FIELD(n1, t1), ...)
DataTypes.ROW(DataTypes.FIELD(n0, t0, d0), DataTypes.FIELD(n1, t1, d1), ...)
`

Bridging to JVM Types

`org.apache.flink.types.Row`
`org.apache.flink.table.data.RowData`

```
DataTypes.ROW([DataTypes.FIELD(n0, t0), DataTypes.FIELD(n1, t1), ...])
DataTypes.ROW([DataTypes.FIELD(n0, t0, d0), DataTypes.FIELD(n1, t1, d1), ...])

```

`DataTypes.ROW([DataTypes.FIELD(n0, t0), DataTypes.FIELD(n1, t1), ...])
DataTypes.ROW([DataTypes.FIELD(n0, t0, d0), DataTypes.FIELD(n1, t1, d1), ...])
`

The type can be declared using ROW<n0 t0 'd0', n1 t1 'd1', ...> where n is the unique name of
a field, t is the logical type of a field, d is the description of a field.

`ROW<n0 t0 'd0', n1 t1 'd1', ...>`
`n`
`t`
`d`

ROW(...) is a synonym for being closer to the SQL standard. For example, ROW(myField INT, myOtherField BOOLEAN) is
equivalent to ROW<myField INT, myOtherField BOOLEAN>.

`ROW(...)`
`ROW(myField INT, myOtherField BOOLEAN)`
`ROW<myField INT, myOtherField BOOLEAN>`

### User-Defined Data Types#


Attention User-defined data types are not fully supported yet. They are
currently (as of Flink 1.11) only exposed as unregistered structured types in parameters and return types of functions.


A structured type is similar to an object in an object-oriented programming language. It contains
zero, one or more attributes. Each attribute consists of a name and a type.


There are two kinds of structured types:

* 
Types that are stored in a catalog and are identified by a catalog identifier (like cat.db.MyType). Those
are equal to the SQL standard definition of structured types.

* 
Anonymously defined, unregistered types (usually reflectively extracted) that are identified by
an implementation class (like com.myorg.model.MyType). Those are useful when programmatically
defining a table program. They enable reusing existing JVM classes without manually defining the
schema of a data type again.


Types that are stored in a catalog and are identified by a catalog identifier (like cat.db.MyType). Those
are equal to the SQL standard definition of structured types.

`cat.db.MyType`

Anonymously defined, unregistered types (usually reflectively extracted) that are identified by
an implementation class (like com.myorg.model.MyType). Those are useful when programmatically
defining a table program. They enable reusing existing JVM classes without manually defining the
schema of a data type again.

`com.myorg.model.MyType`

#### Registered Structured Types#


Currently, registered structured types are not supported. Thus, they cannot be stored in a catalog
or referenced in a CREATE TABLE DDL.

`CREATE TABLE`

#### Unregistered Structured Types#


Unregistered structured types can be created from regular POJOs (Plain Old Java Objects) using automatic reflective extraction.


The implementation class of a structured type must meet the following requirements:

* The class must be globally accessible which means it must be declared public, static, and not abstract.
* The class must offer a default constructor with zero arguments or a full constructor that assigns all
fields.
* All fields of the class must be readable by either public declaration or a getter that follows common
coding style such as getField(), isField(), field().
* All fields of the class must be writable by either public declaration, fully assigning constructor,
or a setter that follows common coding style such as setField(...), field(...).
* All fields must be mapped to a data type either implicitly via reflective extraction or explicitly
using the @DataTypeHint annotations.
* Fields that are declared static or transient are ignored.
`public`
`static`
`abstract`
`public`
`getField()`
`isField()`
`field()`
`public`
`setField(...)`
`field(...)`
`@DataTypeHint`
`static`
`transient`

The reflective extraction supports arbitrary nesting of fields as long as a field type does not
(transitively) refer to itself.


The declared field class (e.g. public int age;) must be contained in the list of supported JVM
bridging classes defined for every data type in this document (e.g. java.lang.Integer or int for INT).

`public int age;`
`java.lang.Integer`
`int`
`INT`

For some classes an annotation is required in order to map the class to a data type (e.g. @DataTypeHint("DECIMAL(10, 2)")
to assign a fixed precision and scale for java.math.BigDecimal).

`@DataTypeHint("DECIMAL(10, 2)")`
`java.math.BigDecimal`

Declaration


```
class User {

    // extract fields automatically
    public int age;
    public String name;

    // enrich the extraction with precision information
    public @DataTypeHint("DECIMAL(10, 2)") BigDecimal totalBalance;

    // enrich the extraction with forcing using RAW types
    public @DataTypeHint("RAW") Class<?> modelClass;
}

DataTypes.of(User.class);

```

`class User {

    // extract fields automatically
    public int age;
    public String name;

    // enrich the extraction with precision information
    public @DataTypeHint("DECIMAL(10, 2)") BigDecimal totalBalance;

    // enrich the extraction with forcing using RAW types
    public @DataTypeHint("RAW") Class<?> modelClass;
}

DataTypes.of(User.class);
`

Bridging to JVM Types

`org.apache.flink.types.Row`
`org.apache.flink.table.data.RowData`

```
case class User(

    // extract fields automatically
    age: Int,
    name: String,

    // enrich the extraction with precision information
    @DataTypeHint("DECIMAL(10, 2)") totalBalance: java.math.BigDecimal,

    // enrich the extraction with forcing using a RAW type
    @DataTypeHint("RAW") modelClass: Class[_]
)

DataTypes.of(classOf[User])

```

`case class User(

    // extract fields automatically
    age: Int,
    name: String,

    // enrich the extraction with precision information
    @DataTypeHint("DECIMAL(10, 2)") totalBalance: java.math.BigDecimal,

    // enrich the extraction with forcing using a RAW type
    @DataTypeHint("RAW") modelClass: Class[_]
)

DataTypes.of(classOf[User])
`

Bridging to JVM Types

`org.apache.flink.types.Row`
`org.apache.flink.table.data.RowData`

```
Not supported.

```

`Not supported.
`

### Other Data Types#


#### BOOLEAN#

`BOOLEAN`

Data type of a boolean with a (possibly) three-valued logic of TRUE, FALSE, and UNKNOWN.

`TRUE`
`FALSE`
`UNKNOWN`

Declaration


```
BOOLEAN

```

`BOOLEAN
`

```
DataTypes.BOOLEAN()

```

`DataTypes.BOOLEAN()
`

Bridging to JVM Types

`java.lang.Boolean`
`boolean`

```
DataTypes.BOOLEAN()

```

`DataTypes.BOOLEAN()
`

#### RAW#

`RAW`

Data type of an arbitrary serialized type. This type is a black box within the table ecosystem
and is only deserialized at the edges.


The raw type is an extension to the SQL standard.


Declaration


```
RAW('class', 'snapshot')

```

`RAW('class', 'snapshot')
`

```
DataTypes.RAW(class, serializer)

DataTypes.RAW(class)

```

`DataTypes.RAW(class, serializer)

DataTypes.RAW(class)
`

Bridging to JVM Types

`byte[]`
`org.apache.flink.table.data.RawValueData`

```
Not supported.

```

`Not supported.
`

The type can be declared using RAW('class', 'snapshot') where class is the originating class and
snapshot is the serialized TypeSerializerSnapshot in Base64 encoding. Usually, the type string is not
declared directly but is generated while persisting the type.

`RAW('class', 'snapshot')`
`class`
`snapshot`
`TypeSerializerSnapshot`

In the API, the RAW type can be declared either by directly supplying a Class + TypeSerializer or
by passing Class and letting the framework extract Class + TypeSerializer from there.

`RAW`
`Class`
`TypeSerializer`
`Class`
`Class`
`TypeSerializer`

#### NULL#

`NULL`

Data type for representing untyped NULL values.

`NULL`

The null type is an extension to the SQL standard. A null type has no other value
except NULL, thus, it can be cast to any nullable type similar to JVM semantics.

`NULL`

This type helps in representing unknown types in API calls that use a NULL literal
as well as bridging to formats such as JSON or Avro that define such a type as well.

`NULL`

This type is not very useful in practice and is just mentioned here for completeness.


Declaration


```
NULL

```

`NULL
`

```
DataTypes.NULL()

```

`DataTypes.NULL()
`

Bridging to JVM Types

`java.lang.Object`

```
Not supported.

```

`Not supported.
`

## Casting#


Flink Table API and SQL can perform casting between a defined input type and target type. While some
casting operations can always succeed regardless of the input value, others can fail at runtime
(i.e. where there is no way to create a value for the target type). For example, it is always
possible to convert INT to STRING, but you cannot always convert a STRING to INT.

`input`
`target`
`INT`
`STRING`
`STRING`
`INT`

During the planning stage, the query validator rejects queries for invalid type pairs with
a ValidationException, e.g. when trying to cast a TIMESTAMP to an INTERVAL.
Valid type pairs that can fail at runtime will be accepted by the query validator,
but requires the user to correctly handle failures.

`ValidationException`
`TIMESTAMP`
`INTERVAL`

In Flink Table API and SQL, casting can be performed by using one of the two following built-in functions:

* CAST: The regular cast function defined by the SQL standard. It can fail the job if the cast operation is fallible and the provided input is not valid. The type inference will preserve the nullability of the input type.
* TRY_CAST: An extension to the regular cast function which returns NULL in case the cast operation fails. Its return type is always nullable.
`CAST`
`TRY_CAST`
`NULL`

For example:


```
CAST('42' AS INT) --- returns 42 of type INT NOT NULL
CAST(NULL AS VARCHAR) --- returns NULL of type VARCHAR
CAST('non-number' AS INT) --- throws an exception and fails the job

TRY_CAST('42' AS INT) --- returns 42 of type INT
TRY_CAST(NULL AS VARCHAR) --- returns NULL of type VARCHAR
TRY_CAST('non-number' AS INT) --- returns NULL of type INT
COALESCE(TRY_CAST('non-number' AS INT), 0) --- returns 0 of type INT NOT NULL

```

`CAST('42' AS INT) --- returns 42 of type INT NOT NULL
CAST(NULL AS VARCHAR) --- returns NULL of type VARCHAR
CAST('non-number' AS INT) --- throws an exception and fails the job

TRY_CAST('42' AS INT) --- returns 42 of type INT
TRY_CAST(NULL AS VARCHAR) --- returns NULL of type VARCHAR
TRY_CAST('non-number' AS INT) --- returns NULL of type INT
COALESCE(TRY_CAST('non-number' AS INT), 0) --- returns 0 of type INT NOT NULL
`

The matrix below describes the supported cast pairs, where “Y” means supported, “!” means fallible, “N” means unsupported:

`CHAR`
`VARCHAR`
`STRING`
`BINARY`
`VARBINARY`
`BYTES`
`BOOLEAN`
`DECIMAL`
`TINYINT`
`SMALLINT`
`INTEGER`
`BIGINT`
`FLOAT`
`DOUBLE`
`DATE`
`TIME`
`TIMESTAMP`
`TIMESTAMP_LTZ`
`INTERVAL`
`ARRAY`
`MULTISET`
`MAP`
`ROW`
`STRUCTURED`
`RAW`
`CHAR`
`VARCHAR`
`STRING`
`BINARY`
`VARBINARY`
`BYTES`
`BOOLEAN`
`DECIMAL`
`TINYINT`
`SMALLINT`
`INTEGER`
`BIGINT`
`FLOAT`
`DOUBLE`
`DATE`
`TIME`
`TIMESTAMP`
`TIMESTAMP_LTZ`
`INTERVAL`
`ARRAY`
`MULTISET`
`MAP`
`ROW`
`STRUCTURED`
`RAW`

Notes:

1. All the casting to constant length or variable length will also trim and pad accordingly to the type definition.
2. TO_TIMESTAMP and TO_TIMESTAMP_LTZ must be used instead of CAST/TRY_CAST.
3. Supported iff the children type pairs are supported. Fallible iff the children type pairs are fallible.
4. Supported iff the RAW class and serializer are equals.
5. Supported iff INTERVAL is a MONTH TO YEAR range.
6. Supported iff INTERVAL is a DAY TO TIME range.
`TO_TIMESTAMP`
`TO_TIMESTAMP_LTZ`
`CAST`
`TRY_CAST`
`RAW`
`INTERVAL`
`MONTH TO YEAR`
`INTERVAL`
`DAY TO TIME`

Also note that a cast of a NULL value will always return NULL,
regardless of whether the function used is CAST or TRY_CAST.

`NULL`
`NULL`
`CAST`
`TRY_CAST`

### Legacy casting#


Pre Flink 1.15 casting behaviour can be enabled by setting table.exec.legacy-cast-behaviour to enabled.
In Flink 1.15 this flag is disabled by default.

`table.exec.legacy-cast-behaviour`
`enabled`

In particular, this will:

* Disable trimming/padding for casting to CHAR/VARCHAR/BINARY/VARBINARY
* CAST never fails but returns NULL, behaving as TRY_CAST but without inferring the correct type
* Formatting of some casting to CHAR/VARCHAR/STRING produces slightly different results.
`CHAR`
`VARCHAR`
`BINARY`
`VARBINARY`
`CAST`
`NULL`
`TRY_CAST`
`CHAR`
`VARCHAR`
`STRING`

> 
  We discourage the use of this flag and we strongly suggest for new projects to keep this flag disabled and use the new casting behaviour.
This flag will be removed in the next Flink versions.



## Data Type Extraction#


At many locations in the API, Flink tries to automatically extract data type from class information using
reflection to avoid repetitive manual schema work. However, extracting a data type reflectively is not always
successful because logical information might be missing. Therefore, it might be necessary to add additional
information close to a class or field declaration for supporting the extraction logic.


The following table lists classes that can be implicitly mapped to a data type without requiring further information.


If you intend to implement classes in Scala, it is recommended to use boxed types (e.g. java.lang.Integer)
instead of Scala’s primitives. Scala’s primitives (e.g. Int or Double) are compiled to JVM primitives (e.g.
int/double) and result in NOT NULL semantics as shown in the table below. Furthermore, Scala primitives that
are used in generics (e.g. java.util.Map[Int, Double]) are erased during compilation and lead to class
information similar to java.util.Map[java.lang.Object, java.lang.Object].

`java.lang.Integer`
`Int`
`Double`
`int`
`double`
`NOT NULL`
`java.util.Map[Int, Double]`
`java.util.Map[java.lang.Object, java.lang.Object]`
`java.lang.String`
`STRING`
`java.lang.Boolean`
`BOOLEAN`
`boolean`
`BOOLEAN NOT NULL`
`java.lang.Byte`
`TINYINT`
`byte`
`TINYINT NOT NULL`
`java.lang.Short`
`SMALLINT`
`short`
`SMALLINT NOT NULL`
`java.lang.Integer`
`INT`
`int`
`INT NOT NULL`
`java.lang.Long`
`BIGINT`
`long`
`BIGINT NOT NULL`
`java.lang.Float`
`FLOAT`
`float`
`FLOAT NOT NULL`
`java.lang.Double`
`DOUBLE`
`double`
`DOUBLE NOT NULL`
`java.sql.Date`
`DATE`
`java.time.LocalDate`
`DATE`
`java.sql.Time`
`TIME(0)`
`java.time.LocalTime`
`TIME(9)`
`java.sql.Timestamp`
`TIMESTAMP(9)`
`java.time.LocalDateTime`
`TIMESTAMP(9)`
`java.time.OffsetDateTime`
`TIMESTAMP(9) WITH TIME ZONE`
`java.time.Instant`
`TIMESTAMP_LTZ(9)`
`java.time.Duration`
`INTERVAL SECOND(9)`
`java.time.Period`
`INTERVAL YEAR(4) TO MONTH`
`byte[]`
`BYTES`
`T[]`
`ARRAY<T>`
`java.util.Map<K, V>`
`MAP<K, V>`
`T`
`T`

Other JVM bridging classes mentioned in this document require a @DataTypeHint annotation.

`@DataTypeHint`

Data type hints can parameterize or replace the default extraction logic of individual function parameters
and return types, structured classes, or fields of structured classes. An implementer can choose to what
extent the default extraction logic should be modified by declaring a @DataTypeHint annotation.

`@DataTypeHint`

The @DataTypeHint annotation provides a set of optional hint parameters. Some of those parameters are shown in the
following example. More information can be found in the documentation of the annotation class.

`@DataTypeHint`

```
import org.apache.flink.table.annotation.DataTypeHint;

class User {

    // defines an INT data type with a default conversion class `java.lang.Integer`
    public @DataTypeHint("INT") Object o;

    // defines a TIMESTAMP data type of millisecond precision with an explicit conversion class
    public @DataTypeHint(value = "TIMESTAMP(3)", bridgedTo = java.sql.Timestamp.class) Object o;

    // enrich the extraction with forcing using a RAW type
    public @DataTypeHint("RAW") Class<?> modelClass;

    // defines that all occurrences of java.math.BigDecimal (also in nested fields) will be
    // extracted as DECIMAL(12, 2)
    public @DataTypeHint(defaultDecimalPrecision = 12, defaultDecimalScale = 2) AccountStatement stmt;

    // defines that whenever a type cannot be mapped to a data type, instead of throwing
    // an exception, always treat it as a RAW type
    public @DataTypeHint(allowRawGlobally = HintFlag.TRUE) ComplexModel model;
}

```

`import org.apache.flink.table.annotation.DataTypeHint;

class User {

    // defines an INT data type with a default conversion class `java.lang.Integer`
    public @DataTypeHint("INT") Object o;

    // defines a TIMESTAMP data type of millisecond precision with an explicit conversion class
    public @DataTypeHint(value = "TIMESTAMP(3)", bridgedTo = java.sql.Timestamp.class) Object o;

    // enrich the extraction with forcing using a RAW type
    public @DataTypeHint("RAW") Class<?> modelClass;

    // defines that all occurrences of java.math.BigDecimal (also in nested fields) will be
    // extracted as DECIMAL(12, 2)
    public @DataTypeHint(defaultDecimalPrecision = 12, defaultDecimalScale = 2) AccountStatement stmt;

    // defines that whenever a type cannot be mapped to a data type, instead of throwing
    // an exception, always treat it as a RAW type
    public @DataTypeHint(allowRawGlobally = HintFlag.TRUE) ComplexModel model;
}
`

```
import org.apache.flink.table.annotation.DataTypeHint

class User {

    // defines an INT data type with a default conversion class `java.lang.Integer`
    @DataTypeHint("INT")
    var o: AnyRef

    // defines a TIMESTAMP data type of millisecond precision with an explicit conversion class
    @DataTypeHint(value = "TIMESTAMP(3)", bridgedTo = java.sql.Timestamp.class)
    var o: AnyRef

    // enrich the extraction with forcing using a RAW type
    @DataTypeHint("RAW")
    var modelClass: Class[_]

    // defines that all occurrences of java.math.BigDecimal (also in nested fields) will be
    // extracted as DECIMAL(12, 2)
    @DataTypeHint(defaultDecimalPrecision = 12, defaultDecimalScale = 2)
    var stmt: AccountStatement

    // defines that whenever a type cannot be mapped to a data type, instead of throwing
    // an exception, always treat it as a RAW type
    @DataTypeHint(allowRawGlobally = HintFlag.TRUE)
    var model: ComplexModel
}

```

`import org.apache.flink.table.annotation.DataTypeHint

class User {

    // defines an INT data type with a default conversion class `java.lang.Integer`
    @DataTypeHint("INT")
    var o: AnyRef

    // defines a TIMESTAMP data type of millisecond precision with an explicit conversion class
    @DataTypeHint(value = "TIMESTAMP(3)", bridgedTo = java.sql.Timestamp.class)
    var o: AnyRef

    // enrich the extraction with forcing using a RAW type
    @DataTypeHint("RAW")
    var modelClass: Class[_]

    // defines that all occurrences of java.math.BigDecimal (also in nested fields) will be
    // extracted as DECIMAL(12, 2)
    @DataTypeHint(defaultDecimalPrecision = 12, defaultDecimalScale = 2)
    var stmt: AccountStatement

    // defines that whenever a type cannot be mapped to a data type, instead of throwing
    // an exception, always treat it as a RAW type
    @DataTypeHint(allowRawGlobally = HintFlag.TRUE)
    var model: ComplexModel
}
`

```
Not supported.

```

`Not supported.
`

 Back to top
