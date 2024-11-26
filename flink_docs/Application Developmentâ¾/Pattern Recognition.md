# Pattern Recognition


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Pattern Recognition#


It is a common use case to search for a set of event patterns, especially in case of data streams.
Flink comes with a complex event processing (CEP) library
which allows for pattern detection in event streams. Furthermore, Flink’s SQL API provides a
relational way of expressing queries with a large set of built-in functions and rule-based
optimizations that can be used out of the box.


In December 2016, the International Organization for Standardization (ISO) released a new version
of the SQL standard which includes Row Pattern Recognition in SQL
(ISO/IEC TR 19075-5:2016).
It allows Flink to consolidate CEP and SQL API using the MATCH_RECOGNIZE clause for complex event
processing in SQL.

`MATCH_RECOGNIZE`

A MATCH_RECOGNIZE clause enables the following tasks:

`MATCH_RECOGNIZE`
* Logically partition and order the data that is used with the PARTITION BY and ORDER BY
clauses.
* Define patterns of rows to seek using the PATTERN clause. These patterns use a syntax similar to
that of regular expressions.
* The logical components of the row pattern variables are specified in the DEFINE clause.
* Define measures, which are expressions usable in other parts of the SQL query, in the MEASURES
clause.
`PARTITION BY`
`ORDER BY`
`PATTERN`
`DEFINE`
`MEASURES`

The following example illustrates the syntax for basic pattern recognition:


```
SELECT T.aid, T.bid, T.cid
FROM MyTable
    MATCH_RECOGNIZE (
      PARTITION BY userid
      ORDER BY proctime
      MEASURES
        A.id AS aid,
        B.id AS bid,
        C.id AS cid
      PATTERN (A B C)
      DEFINE
        A AS name = 'a',
        B AS name = 'b',
        C AS name = 'c'
    ) AS T

```

`SELECT T.aid, T.bid, T.cid
FROM MyTable
    MATCH_RECOGNIZE (
      PARTITION BY userid
      ORDER BY proctime
      MEASURES
        A.id AS aid,
        B.id AS bid,
        C.id AS cid
      PATTERN (A B C)
      DEFINE
        A AS name = 'a',
        B AS name = 'b',
        C AS name = 'c'
    ) AS T
`

This page will explain each keyword in more detail and will illustrate more complex examples.


> 
  Flink’s implementation of the MATCH_RECOGNIZE
clause is a subset of the full standard. Only those features documented in the following sections
are supported. Additional features may be supported based on community feedback, please also take a look at the
known limitations.


`MATCH_RECOGNIZE`

## Introduction and Examples#


### Installation Guide#


The pattern recognition feature uses the Apache Flink’s CEP library internally. In order to be able
to use the MATCH_RECOGNIZE clause, the library needs to be added as a dependency to your Maven
project.

`MATCH_RECOGNIZE`

```
<dependency>
  <groupId>org.apache.flink</groupId>
  <artifactId>flink-cep</artifactId>
  <version>2.0-SNAPSHOT</version>
</dependency>

```

`<dependency>
  <groupId>org.apache.flink</groupId>
  <artifactId>flink-cep</artifactId>
  <version>2.0-SNAPSHOT</version>
</dependency>
`

Alternatively, you can also add the dependency to the cluster classpath (see the
dependency section for more information).


If you want to use the MATCH_RECOGNIZE clause in the
SQL Client, you don’t have to do anything as all the
dependencies are included by default.

`MATCH_RECOGNIZE`

### SQL Semantics#


Every MATCH_RECOGNIZE query consists of the following clauses:

`MATCH_RECOGNIZE`
* PARTITION BY - defines the logical partitioning of the table; similar to a
GROUP BY operation.
* ORDER BY - specifies how the incoming rows should be ordered; this is
essential as patterns depend on an order.
* MEASURES - defines output of the clause; similar to a SELECT clause.
* ONE ROW PER MATCH - output mode which defines how many rows per match should be
produced.
* AFTER MATCH SKIP - specifies where the next match should start; this is
also a way to control how many distinct matches a single event can belong to.
* PATTERN - allows constructing patterns that will be searched for using a
regular expression-like syntax.
* DEFINE - this section defines the conditions that the pattern variables must
satisfy.
`GROUP BY`
`SELECT`

Attention Currently, the MATCH_RECOGNIZE clause can only
be applied to an append table. Furthermore, it
always produces an append table as well.

`MATCH_RECOGNIZE`

### Examples#


For our examples, we assume that a table Ticker has been registered. The table contains prices of
stocks at a particular point in time.

`Ticker`

The table has a following schema:


```
Ticker
     |-- symbol: String                           # symbol of the stock
     |-- price: Long                              # price of the stock
     |-- tax: Long                                # tax liability of the stock
     |-- rowtime: TimeIndicatorTypeInfo(rowtime)  # point in time when the change to those values happened

```

`Ticker
     |-- symbol: String                           # symbol of the stock
     |-- price: Long                              # price of the stock
     |-- tax: Long                                # tax liability of the stock
     |-- rowtime: TimeIndicatorTypeInfo(rowtime)  # point in time when the change to those values happened
`

For simplification, we only consider the incoming data for a single stock ACME. A ticker could
look similar to the following table where rows are continuously appended.

`ACME`

```
symbol         rowtime         price    tax
======  ====================  ======= =======
'ACME'  '01-Apr-11 10:00:00'   12      1
'ACME'  '01-Apr-11 10:00:01'   17      2
'ACME'  '01-Apr-11 10:00:02'   19      1
'ACME'  '01-Apr-11 10:00:03'   21      3
'ACME'  '01-Apr-11 10:00:04'   25      2
'ACME'  '01-Apr-11 10:00:05'   18      1
'ACME'  '01-Apr-11 10:00:06'   15      1
'ACME'  '01-Apr-11 10:00:07'   14      2
'ACME'  '01-Apr-11 10:00:08'   24      2
'ACME'  '01-Apr-11 10:00:09'   25      2
'ACME'  '01-Apr-11 10:00:10'   19      1

```

`symbol         rowtime         price    tax
======  ====================  ======= =======
'ACME'  '01-Apr-11 10:00:00'   12      1
'ACME'  '01-Apr-11 10:00:01'   17      2
'ACME'  '01-Apr-11 10:00:02'   19      1
'ACME'  '01-Apr-11 10:00:03'   21      3
'ACME'  '01-Apr-11 10:00:04'   25      2
'ACME'  '01-Apr-11 10:00:05'   18      1
'ACME'  '01-Apr-11 10:00:06'   15      1
'ACME'  '01-Apr-11 10:00:07'   14      2
'ACME'  '01-Apr-11 10:00:08'   24      2
'ACME'  '01-Apr-11 10:00:09'   25      2
'ACME'  '01-Apr-11 10:00:10'   19      1
`

The task is now to find periods of a constantly decreasing price of a single ticker. For this, one
could write a query like:


```
SELECT *
FROM Ticker
    MATCH_RECOGNIZE (
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            START_ROW.rowtime AS start_tstamp,
            LAST(PRICE_DOWN.rowtime) AS bottom_tstamp,
            LAST(PRICE_UP.rowtime) AS end_tstamp
        ONE ROW PER MATCH
        AFTER MATCH SKIP TO LAST PRICE_UP
        PATTERN (START_ROW PRICE_DOWN+ PRICE_UP)
        DEFINE
            PRICE_DOWN AS
                (LAST(PRICE_DOWN.price, 1) IS NULL AND PRICE_DOWN.price < START_ROW.price) OR
                    PRICE_DOWN.price < LAST(PRICE_DOWN.price, 1),
            PRICE_UP AS
                PRICE_UP.price > LAST(PRICE_DOWN.price, 1)
    ) MR;

```

`SELECT *
FROM Ticker
    MATCH_RECOGNIZE (
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            START_ROW.rowtime AS start_tstamp,
            LAST(PRICE_DOWN.rowtime) AS bottom_tstamp,
            LAST(PRICE_UP.rowtime) AS end_tstamp
        ONE ROW PER MATCH
        AFTER MATCH SKIP TO LAST PRICE_UP
        PATTERN (START_ROW PRICE_DOWN+ PRICE_UP)
        DEFINE
            PRICE_DOWN AS
                (LAST(PRICE_DOWN.price, 1) IS NULL AND PRICE_DOWN.price < START_ROW.price) OR
                    PRICE_DOWN.price < LAST(PRICE_DOWN.price, 1),
            PRICE_UP AS
                PRICE_UP.price > LAST(PRICE_DOWN.price, 1)
    ) MR;
`

The query partitions the Ticker table by the symbol column and orders it by the rowtime
time attribute.

`Ticker`
`symbol`
`rowtime`

The PATTERN clause specifies that we are interested in a pattern with a starting event START_ROW
that is followed by one or more PRICE_DOWN events and concluded with a PRICE_UP event. If such
a pattern can be found, the next pattern match will be seeked at the last PRICE_UP event as
indicated by the AFTER MATCH SKIP TO LAST clause.

`PATTERN`
`START_ROW`
`PRICE_DOWN`
`PRICE_UP`
`PRICE_UP`
`AFTER MATCH SKIP TO LAST`

The DEFINE clause specifies the conditions that need to be met for a PRICE_DOWN and PRICE_UP
event. Although the START_ROW pattern variable is not present it has an implicit condition that
is evaluated always as TRUE.

`DEFINE`
`PRICE_DOWN`
`PRICE_UP`
`START_ROW`
`TRUE`

A pattern variable PRICE_DOWN is defined as a row with a price that is smaller than the price of
the last row that met the PRICE_DOWN condition. For the initial case or when there is no last row
that met the PRICE_DOWN condition, the price of the row should be smaller than the price of the
preceding row in the pattern (referenced by START_ROW).

`PRICE_DOWN`
`PRICE_DOWN`
`PRICE_DOWN`
`START_ROW`

A pattern variable PRICE_UP is defined as a row with a price that is larger than the price of the
last row that met the PRICE_DOWN condition.

`PRICE_UP`
`PRICE_DOWN`

This query produces a summary row for each period in which the price of a stock was continuously
decreasing.


The exact representation of the output rows is defined in the MEASURES part of the query. The
number of output rows is defined by the ONE ROW PER MATCH output mode.

`MEASURES`
`ONE ROW PER MATCH`

```
 symbol       start_tstamp       bottom_tstamp         end_tstamp
=========  ==================  ==================  ==================
ACME       01-APR-11 10:00:04  01-APR-11 10:00:07  01-APR-11 10:00:08

```

` symbol       start_tstamp       bottom_tstamp         end_tstamp
=========  ==================  ==================  ==================
ACME       01-APR-11 10:00:04  01-APR-11 10:00:07  01-APR-11 10:00:08
`

The resulting row describes a period of falling prices that started at 01-APR-11 10:00:04 and
achieved the lowest price at 01-APR-11 10:00:07 that increased again at 01-APR-11 10:00:08.

`01-APR-11 10:00:04`
`01-APR-11 10:00:07`
`01-APR-11 10:00:08`

## Partitioning#


It is possible to look for patterns in partitioned data, e.g., trends for a single ticker or a
particular user. This can be expressed using the PARTITION BY clause. The clause is similar to
using GROUP BY for aggregations.

`PARTITION BY`
`GROUP BY`

It is highly advised to partition the incoming data because otherwise the MATCH_RECOGNIZE clause will be translated into a non-parallel operator
to ensure global ordering.

`MATCH_RECOGNIZE`

## Order of Events#


Apache Flink allows for searching for patterns based on time; either
processing time or event time.


In case of event time, the events are sorted before they are passed to the internal pattern state
machine. As a consequence, the produced output will be correct regardless of the order in which
rows are appended to the table. Instead, the pattern is evaluated in the order specified by the
time contained in each row.


The MATCH_RECOGNIZE clause assumes a time attribute with ascending
ordering as the first argument to ORDER BY clause.

`MATCH_RECOGNIZE`
`ORDER BY`

For the example Ticker table, a definition like ORDER BY rowtime ASC, price DESC is valid but
ORDER BY price, rowtime or ORDER BY rowtime DESC, price ASC is not.

`Ticker`
`ORDER BY rowtime ASC, price DESC`
`ORDER BY price, rowtime`
`ORDER BY rowtime DESC, price ASC`

## Define & Measures#


The DEFINE and MEASURES keywords have similar meanings to the WHERE and SELECT clauses in a
simple SQL query.

`DEFINE`
`MEASURES`
`WHERE`
`SELECT`

The MEASURES clause defines what will be included in the output of a matching pattern. It can
project columns and define expressions for evaluation. The number of produced rows depends on the
output mode setting.

`MEASURES`

The DEFINE clause specifies conditions that rows have to fulfill in order to be classified to a
corresponding pattern variable. If a condition is not defined for a pattern
variable, a default condition will be used which evaluates to true for every row.

`DEFINE`
`true`

For a more detailed explanation about expressions that can be used in those clauses, please have a
look at the event stream navigation section.


### Aggregations#


Aggregations can be used in DEFINE and MEASURES clauses. Both
built-in and custom
user defined functions are supported.

`DEFINE`
`MEASURES`

Aggregate functions are applied to each subset of rows mapped to a match. In order to understand
how those subsets are evaluated have a look at the event stream navigation
section.


The task of the following example is to find the longest period of time for which the average price
of a ticker did not go below certain threshold. It shows how expressible MATCH_RECOGNIZE can
become with aggregations. This task can be performed with the following query:

`MATCH_RECOGNIZE`

```
SELECT *
FROM Ticker
    MATCH_RECOGNIZE (
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            FIRST(A.rowtime) AS start_tstamp,
            LAST(A.rowtime) AS end_tstamp,
            AVG(A.price) AS avgPrice
        ONE ROW PER MATCH
        AFTER MATCH SKIP PAST LAST ROW
        PATTERN (A+ B)
        DEFINE
            A AS AVG(A.price) < 15
    ) MR;

```

`SELECT *
FROM Ticker
    MATCH_RECOGNIZE (
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            FIRST(A.rowtime) AS start_tstamp,
            LAST(A.rowtime) AS end_tstamp,
            AVG(A.price) AS avgPrice
        ONE ROW PER MATCH
        AFTER MATCH SKIP PAST LAST ROW
        PATTERN (A+ B)
        DEFINE
            A AS AVG(A.price) < 15
    ) MR;
`

Given this query and following input values:


```
symbol         rowtime         price    tax
======  ====================  ======= =======
'ACME'  '01-Apr-11 10:00:00'   12      1
'ACME'  '01-Apr-11 10:00:01'   17      2
'ACME'  '01-Apr-11 10:00:02'   13      1
'ACME'  '01-Apr-11 10:00:03'   16      3
'ACME'  '01-Apr-11 10:00:04'   25      2
'ACME'  '01-Apr-11 10:00:05'   2       1
'ACME'  '01-Apr-11 10:00:06'   4       1
'ACME'  '01-Apr-11 10:00:07'   10      2
'ACME'  '01-Apr-11 10:00:08'   15      2
'ACME'  '01-Apr-11 10:00:09'   25      2
'ACME'  '01-Apr-11 10:00:10'   25      1
'ACME'  '01-Apr-11 10:00:11'   30      1

```

`symbol         rowtime         price    tax
======  ====================  ======= =======
'ACME'  '01-Apr-11 10:00:00'   12      1
'ACME'  '01-Apr-11 10:00:01'   17      2
'ACME'  '01-Apr-11 10:00:02'   13      1
'ACME'  '01-Apr-11 10:00:03'   16      3
'ACME'  '01-Apr-11 10:00:04'   25      2
'ACME'  '01-Apr-11 10:00:05'   2       1
'ACME'  '01-Apr-11 10:00:06'   4       1
'ACME'  '01-Apr-11 10:00:07'   10      2
'ACME'  '01-Apr-11 10:00:08'   15      2
'ACME'  '01-Apr-11 10:00:09'   25      2
'ACME'  '01-Apr-11 10:00:10'   25      1
'ACME'  '01-Apr-11 10:00:11'   30      1
`

The query will accumulate events as part of the pattern variable A as long as the average price
of them does not exceed 15. For example, such a limit exceeding happens at 01-Apr-11 10:00:04.
The following period exceeds the average price of 15 again at 01-Apr-11 10:00:11. Thus the
results for said query will be:

`A`
`15`
`01-Apr-11 10:00:04`
`15`
`01-Apr-11 10:00:11`

```
 symbol       start_tstamp       end_tstamp          avgPrice
=========  ==================  ==================  ============
ACME       01-APR-11 10:00:00  01-APR-11 10:00:03     14.5
ACME       01-APR-11 10:00:05  01-APR-11 10:00:10     13.5

```

` symbol       start_tstamp       end_tstamp          avgPrice
=========  ==================  ==================  ============
ACME       01-APR-11 10:00:00  01-APR-11 10:00:03     14.5
ACME       01-APR-11 10:00:05  01-APR-11 10:00:10     13.5
`

Aggregations can be applied to expressions, but only if
they reference a single pattern variable. Thus SUM(A.price * A.tax) is a valid one, but
AVG(A.price * B.tax) is not.

`SUM(A.price * A.tax)`
`AVG(A.price * B.tax)`

> 
DISTINCT aggregations are not supported.


`DISTINCT`

## Defining a Pattern#


The MATCH_RECOGNIZE clause allows users to search for patterns in event streams using a powerful
and expressive syntax that is somewhat similar to the widespread regular expression syntax.

`MATCH_RECOGNIZE`

Every pattern is constructed from basic building blocks, called pattern variables, to which
operators (quantifiers and other modifiers) can be applied. The whole pattern must be enclosed in
brackets.


An example pattern could look like:


```
PATTERN (A B+ C* D)

```

`PATTERN (A B+ C* D)
`

One may use the following operators:

* Concatenation - a pattern like (A B) means that the contiguity is strict between A and B.
Therefore, there can be no rows that were not mapped to A or B in between.
* Quantifiers - modify the number of rows that can be mapped to the pattern variable.

* â 0 or more rows
+ â 1 or more rows
? â 0 or 1 rows
{ n } â exactly n rows (n > 0)
{ n, } â n or more rows (n â¥ 0)
{ n, m } â between n and m (inclusive) rows (0 â¤ n â¤ m, 0 < m)
{ , m } â between 0 and m (inclusive) rows (m > 0)


`(A B)`
`A`
`B`
`A`
`B`
* * â 0 or more rows
* + â 1 or more rows
* ? â 0 or 1 rows
* { n } â exactly n rows (n > 0)
* { n, } â n or more rows (n â¥ 0)
* { n, m } â between n and m (inclusive) rows (0 â¤ n â¤ m, 0 < m)
* { , m } â between 0 and m (inclusive) rows (m > 0)
`*`
`+`
`?`
`{ n }`
`{ n, }`
`{ n, m }`
`{ , m }`

> 
  Patterns that can potentially produce an empty
match are not supported. Examples of such patterns are PATTERN (A*), PATTERN  (A? B*),
PATTERN (A{0,} B{0,} C*), etc.


`PATTERN (A*)`
`PATTERN  (A? B*)`
`PATTERN (A{0,} B{0,} C*)`

### Greedy & Reluctant Quantifiers#


Each quantifier can be either greedy (default behavior) or reluctant. Greedy quantifiers try to
match as many rows as possible while reluctant quantifiers try to match as few as possible.


In order to illustrate the difference, one can view the following example with a query where a
greedy quantifier is applied to the B variable:

`B`

```
SELECT *
FROM Ticker
    MATCH_RECOGNIZE(
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            C.price AS lastPrice
        ONE ROW PER MATCH
        AFTER MATCH SKIP PAST LAST ROW
        PATTERN (A B* C)
        DEFINE
            A AS A.price > 10,
            B AS B.price < 15,
            C AS C.price > 12
    )

```

`SELECT *
FROM Ticker
    MATCH_RECOGNIZE(
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            C.price AS lastPrice
        ONE ROW PER MATCH
        AFTER MATCH SKIP PAST LAST ROW
        PATTERN (A B* C)
        DEFINE
            A AS A.price > 10,
            B AS B.price < 15,
            C AS C.price > 12
    )
`

Given we have the following input:


```
 symbol  tax   price          rowtime
======= ===== ======== =====================
 XYZ     1     10       2018-09-17 10:00:02
 XYZ     2     11       2018-09-17 10:00:03
 XYZ     1     12       2018-09-17 10:00:04
 XYZ     2     13       2018-09-17 10:00:05
 XYZ     1     14       2018-09-17 10:00:06
 XYZ     2     16       2018-09-17 10:00:07

```

` symbol  tax   price          rowtime
======= ===== ======== =====================
 XYZ     1     10       2018-09-17 10:00:02
 XYZ     2     11       2018-09-17 10:00:03
 XYZ     1     12       2018-09-17 10:00:04
 XYZ     2     13       2018-09-17 10:00:05
 XYZ     1     14       2018-09-17 10:00:06
 XYZ     2     16       2018-09-17 10:00:07
`

The pattern above will produce the following output:


```
 symbol   lastPrice
======== ===========
 XYZ      16

```

` symbol   lastPrice
======== ===========
 XYZ      16
`

The same query where B* is modified to B*?, which means that B* should be reluctant, will
produce:

`B*`
`B*?`
`B*`

```
 symbol   lastPrice
======== ===========
 XYZ      13
 XYZ      16

```

` symbol   lastPrice
======== ===========
 XYZ      13
 XYZ      16
`

The pattern variable B matches only to the row with price 12 instead of swallowing the rows
with prices 12, 13, and 14.

`B`
`12`
`12`
`13`
`14`

It is not possible to use a greedy quantifier for
the last variable of a pattern. Thus, a pattern like (A B*) is not allowed. This can be easily
worked around by introducing an artificial state (e.g. C) that has a negated condition of B. So
you could use a query like:

`(A B*)`
`C`
`B`

```
PATTERN (A B* C)
DEFINE
    A AS condA(),
    B AS condB(),
    C AS NOT condB()

```

`PATTERN (A B* C)
DEFINE
    A AS condA(),
    B AS condB(),
    C AS NOT condB()
`

Attention The optional reluctant quantifier (A?? or
A{0,1}?) is not supported right now.

`A??`
`A{0,1}?`

### Time constraint#


Especially for streaming use cases, it is often required that a pattern finishes within a given
period of time. This allows for limiting the overall state size that Flink has to maintain
internally, even in case of greedy quantifiers.


Therefore, Flink SQL supports the additional (non-standard SQL) WITHIN clause for defining a time
constraint for a pattern. The clause can be defined after the PATTERN clause and takes an
interval of millisecond resolution.

`WITHIN`
`PATTERN`

If the time between the first and last event of a potential match is longer than the given value,
such a match will not be appended to the result table.


Note It is generally encouraged to use the WITHIN clause as
it helps Flink with efficient memory management. Underlying state can be pruned once the threshold
is reached.

`WITHIN`

Attention However, the WITHIN clause is not part of the
SQL standard. The recommended way of dealing with time constraints might change in the future.

`WITHIN`

The use of the WITHIN clause is illustrated in the following example query:

`WITHIN`

```
SELECT *
FROM Ticker
    MATCH_RECOGNIZE(
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            C.rowtime AS dropTime,
            A.price - C.price AS dropDiff
        ONE ROW PER MATCH
        AFTER MATCH SKIP PAST LAST ROW
        PATTERN (A B* C) WITHIN INTERVAL '1' HOUR
        DEFINE
            B AS B.price > A.price - 10,
            C AS C.price < A.price - 10
    )

```

`SELECT *
FROM Ticker
    MATCH_RECOGNIZE(
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            C.rowtime AS dropTime,
            A.price - C.price AS dropDiff
        ONE ROW PER MATCH
        AFTER MATCH SKIP PAST LAST ROW
        PATTERN (A B* C) WITHIN INTERVAL '1' HOUR
        DEFINE
            B AS B.price > A.price - 10,
            C AS C.price < A.price - 10
    )
`

The query detects a price drop of 10 that happens within an interval of 1 hour.

`10`

Let’s assume the query is used to analyze the following ticker data:


```
symbol         rowtime         price    tax
======  ====================  ======= =======
'ACME'  '01-Apr-11 10:00:00'   20      1
'ACME'  '01-Apr-11 10:20:00'   17      2
'ACME'  '01-Apr-11 10:40:00'   18      1
'ACME'  '01-Apr-11 11:00:00'   11      3
'ACME'  '01-Apr-11 11:20:00'   14      2
'ACME'  '01-Apr-11 11:40:00'   9       1
'ACME'  '01-Apr-11 12:00:00'   15      1
'ACME'  '01-Apr-11 12:20:00'   14      2
'ACME'  '01-Apr-11 12:40:00'   24      2
'ACME'  '01-Apr-11 13:00:00'   1       2
'ACME'  '01-Apr-11 13:20:00'   19      1

```

`symbol         rowtime         price    tax
======  ====================  ======= =======
'ACME'  '01-Apr-11 10:00:00'   20      1
'ACME'  '01-Apr-11 10:20:00'   17      2
'ACME'  '01-Apr-11 10:40:00'   18      1
'ACME'  '01-Apr-11 11:00:00'   11      3
'ACME'  '01-Apr-11 11:20:00'   14      2
'ACME'  '01-Apr-11 11:40:00'   9       1
'ACME'  '01-Apr-11 12:00:00'   15      1
'ACME'  '01-Apr-11 12:20:00'   14      2
'ACME'  '01-Apr-11 12:40:00'   24      2
'ACME'  '01-Apr-11 13:00:00'   1       2
'ACME'  '01-Apr-11 13:20:00'   19      1
`

The query will produce the following results:


```
symbol         dropTime         dropDiff
======  ====================  =============
'ACME'  '01-Apr-11 13:00:00'      14

```

`symbol         dropTime         dropDiff
======  ====================  =============
'ACME'  '01-Apr-11 13:00:00'      14
`

The resulting row represents a price drop from 15 (at 01-Apr-11 12:00:00) to 1 (at
01-Apr-11 13:00:00). The dropDiff column contains the price difference.

`15`
`01-Apr-11 12:00:00`
`1`
`01-Apr-11 13:00:00`
`dropDiff`

Notice that even though prices also drop by higher values, for example, by 11 (between
01-Apr-11 10:00:00 and 01-Apr-11 11:40:00), the time difference between those two events is
larger than 1 hour. Thus, they don’t produce a match.

`11`
`01-Apr-11 10:00:00`
`01-Apr-11 11:40:00`

## Output Mode#


The output mode describes how many rows should be emitted for every found match. The SQL standard
describes two modes:

* ALL ROWS PER MATCH
* ONE ROW PER MATCH.
`ALL ROWS PER MATCH`
`ONE ROW PER MATCH`

Currently, the only supported output mode is ONE ROW PER MATCH that will always produce one
output summary row for each found match.

`ONE ROW PER MATCH`

The schema of the output row will be a concatenation of
[partitioning columns] + [measures columns] in that particular order.

`[partitioning columns] + [measures columns]`

The following example shows the output of a query defined as:


```
SELECT *
FROM Ticker
    MATCH_RECOGNIZE(
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            FIRST(A.price) AS startPrice,
            LAST(A.price) AS topPrice,
            B.price AS lastPrice
        ONE ROW PER MATCH
        PATTERN (A+ B)
        DEFINE
            A AS LAST(A.price, 1) IS NULL OR A.price > LAST(A.price, 1),
            B AS B.price < LAST(A.price)
    )

```

`SELECT *
FROM Ticker
    MATCH_RECOGNIZE(
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            FIRST(A.price) AS startPrice,
            LAST(A.price) AS topPrice,
            B.price AS lastPrice
        ONE ROW PER MATCH
        PATTERN (A+ B)
        DEFINE
            A AS LAST(A.price, 1) IS NULL OR A.price > LAST(A.price, 1),
            B AS B.price < LAST(A.price)
    )
`

For the following input rows:


```
 symbol   tax   price          rowtime
======== ===== ======== =====================
 XYZ      1     10       2018-09-17 10:00:02
 XYZ      2     12       2018-09-17 10:00:03
 XYZ      1     13       2018-09-17 10:00:04
 XYZ      2     11       2018-09-17 10:00:05

```

` symbol   tax   price          rowtime
======== ===== ======== =====================
 XYZ      1     10       2018-09-17 10:00:02
 XYZ      2     12       2018-09-17 10:00:03
 XYZ      1     13       2018-09-17 10:00:04
 XYZ      2     11       2018-09-17 10:00:05
`

The query will produce the following output:


```
 symbol   startPrice   topPrice   lastPrice
======== ============ ========== ===========
 XYZ      10           13         11

```

` symbol   startPrice   topPrice   lastPrice
======== ============ ========== ===========
 XYZ      10           13         11
`

The pattern recognition is partitioned by the symbol column. Even though not explicitly mentioned
in the MEASURES clause, the partitioned column is added at the beginning of the result.

`symbol`
`MEASURES`

## Pattern Navigation#


The DEFINE and MEASURES clauses allow for navigating within the list of rows that (potentially)
match a pattern.

`DEFINE`
`MEASURES`

This section discusses this navigation for declaring conditions or producing output results.


### Pattern Variable Referencing#


A pattern variable reference allows a set of rows mapped to a particular pattern variable in the
DEFINE or MEASURES clauses to be referenced.

`DEFINE`
`MEASURES`

For example, the expression A.price describes a set of rows mapped so far to A plus the current
row if we try to match the current row to A. If an expression in the DEFINE/MEASURES clause
requires a single row (e.g. A.price or A.price > 10), it selects the last value belonging to
the corresponding set.

`A.price`
`A`
`A`
`DEFINE`
`MEASURES`
`A.price`
`A.price > 10`

If no pattern variable is specified (e.g. SUM(price)), an expression references the default
pattern variable * which references all variables in the pattern. In other words, it creates a
list of all the rows mapped so far to any variable plus the current row.

`SUM(price)`
`*`

#### Example#


For a more thorough example, one can take a look at the following pattern and corresponding
conditions:


```
PATTERN (A B+)
DEFINE
  A AS A.price >= 10,
  B AS B.price > A.price AND SUM(price) < 100 AND SUM(B.price) < 80

```

`PATTERN (A B+)
DEFINE
  A AS A.price >= 10,
  B AS B.price > A.price AND SUM(price) < 100 AND SUM(B.price) < 80
`

The following table describes how those conditions are evaluated for each incoming event.


The table consists of the following columns:

* # - the row identifier that uniquely identifies an incoming row in the lists
[A.price]/[B.price]/[price].
* price - the price of the incoming row.
* [A.price]/[B.price]/[price] - describe lists of rows which are used in the DEFINE
clause to evaluate conditions.
* Classifier - the classifier of the current row which indicates the pattern variable the row
is mapped to.
* A.price/B.price/SUM(price)/SUM(B.price) - describes the result after those expressions
have been evaluated.
`#`
`[A.price]`
`[B.price]`
`[price]`
`price`
`[A.price]`
`[B.price]`
`[price]`
`DEFINE`
`Classifier`
`A.price`
`B.price`
`SUM(price)`
`SUM(B.price)`

As can be seen in the table, the first row is mapped to pattern variable A and subsequent rows
are mapped to pattern variable B. However, the last row does not fulfill the B condition
because the sum over all mapped rows SUM(price) and the sum over all rows in B exceed the
specified thresholds.

`A`
`B`
`B`
`SUM(price)`
`B`

### Logical Offsets#


Logical offsets enable navigation within the events that were mapped to a particular pattern
variable. This can be expressed with two corresponding functions:

`LAST(variable.field, n)`

Returns the value of the field from the event that was mapped to the n-th
      last element of the variable. The counting starts at the last element mapped.

`FIRST(variable.field, n)`

Returns the value of the field from the event that was mapped to the n-th element
      of the variable. The counting starts at the first element mapped.


#### Examples#


For a more thorough example, one can take a look at the following pattern and corresponding
conditions:


```
PATTERN (A B+)
DEFINE
  A AS A.price >= 10,
  B AS (LAST(B.price, 1) IS NULL OR B.price > LAST(B.price, 1)) AND
       (LAST(B.price, 2) IS NULL OR B.price > 2 * LAST(B.price, 2))

```

`PATTERN (A B+)
DEFINE
  A AS A.price >= 10,
  B AS (LAST(B.price, 1) IS NULL OR B.price > LAST(B.price, 1)) AND
       (LAST(B.price, 2) IS NULL OR B.price > 2 * LAST(B.price, 2))
`

The following table describes how those conditions are evaluated for each incoming event.


The table consists of the following columns:

* price - the price of the incoming row.
* Classifier - the classifier of the current row which indicates the pattern variable the row
is mapped to.
* LAST(B.price, 1)/LAST(B.price, 2) - describes the result after those expressions have been
evaluated.
`price`
`Classifier`
`LAST(B.price, 1)`
`LAST(B.price, 2)`
`LAST(B.price, 1)`
`B`
`35 < 2 * 20`

It might also make sense to use the default pattern variable with logical offsets.


In this case, an offset considers all the rows mapped so far:


```
PATTERN (A B? C)
DEFINE
  B AS B.price < 20,
  C AS LAST(price, 1) < C.price

```

`PATTERN (A B? C)
DEFINE
  B AS B.price < 20,
  C AS LAST(price, 1) < C.price
`
`LAST(price, 1)`
`B`

If the second row did not map to the B variable, we would have the following results:

`B`
`LAST(price, 1)`
`A`

It is also possible to use multiple pattern variable references in the first argument of the
FIRST/LAST functions. This way, one can write an expression that accesses multiple columns.
However, all of them must use the same pattern variable. In other words, the value of the
LAST/FIRST function must be computed in a single row.

`FIRST/LAST`
`LAST`
`FIRST`

Thus, it is possible to use LAST(A.price * A.tax), but an expression like LAST(A.price * B.tax)
is not allowed.

`LAST(A.price * A.tax)`
`LAST(A.price * B.tax)`

## After Match Strategy#


The AFTER MATCH SKIP clause specifies where to start a new matching procedure after a complete
match was found.

`AFTER MATCH SKIP`

There are four different strategies:

* SKIP PAST LAST ROW - resumes the pattern matching at the next row after the last row of the
current match.
* SKIP TO NEXT ROW - continues searching for a new match starting at the next row after the
starting row of the match.
* SKIP TO LAST variable - resumes the pattern matching at the last row that is mapped to the
specified pattern variable.
* SKIP TO FIRST variable - resumes the pattern matching at the first row that is mapped to the
specified pattern variable.
`SKIP PAST LAST ROW`
`SKIP TO NEXT ROW`
`SKIP TO LAST variable`
`SKIP TO FIRST variable`

This is also a way to specify how many matches a single event can belong to. For example, with the
SKIP PAST LAST ROW strategy every event can belong to at most one match.

`SKIP PAST LAST ROW`

#### Examples#


In order to better understand the differences between those strategies one can take a look at the
following example.


For the following input rows:


```
 symbol   tax   price         rowtime
======== ===== ======= =====================
 XYZ      1     7       2018-09-17 10:00:01
 XYZ      2     9       2018-09-17 10:00:02
 XYZ      1     10      2018-09-17 10:00:03
 XYZ      2     5       2018-09-17 10:00:04
 XYZ      2     10      2018-09-17 10:00:05
 XYZ      2     7       2018-09-17 10:00:06
 XYZ      2     14      2018-09-17 10:00:07

```

` symbol   tax   price         rowtime
======== ===== ======= =====================
 XYZ      1     7       2018-09-17 10:00:01
 XYZ      2     9       2018-09-17 10:00:02
 XYZ      1     10      2018-09-17 10:00:03
 XYZ      2     5       2018-09-17 10:00:04
 XYZ      2     10      2018-09-17 10:00:05
 XYZ      2     7       2018-09-17 10:00:06
 XYZ      2     14      2018-09-17 10:00:07
`

We evaluate the following query with different strategies:


```
SELECT *
FROM Ticker
    MATCH_RECOGNIZE(
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            SUM(A.price) AS sumPrice,
            FIRST(rowtime) AS startTime,
            LAST(rowtime) AS endTime
        ONE ROW PER MATCH
        [AFTER MATCH STRATEGY]
        PATTERN (A+ C)
        DEFINE
            A AS SUM(A.price) < 30
    )

```

`SELECT *
FROM Ticker
    MATCH_RECOGNIZE(
        PARTITION BY symbol
        ORDER BY rowtime
        MEASURES
            SUM(A.price) AS sumPrice,
            FIRST(rowtime) AS startTime,
            LAST(rowtime) AS endTime
        ONE ROW PER MATCH
        [AFTER MATCH STRATEGY]
        PATTERN (A+ C)
        DEFINE
            A AS SUM(A.price) < 30
    )
`

The query returns the sum of the prices of all rows mapped to A and the first and last timestamp
of the overall match.

`A`

The query will produce different results based on which AFTER MATCH strategy was used:

`AFTER MATCH`

##### AFTER MATCH SKIP PAST LAST ROW#

`AFTER MATCH SKIP PAST LAST ROW`

```
 symbol   sumPrice        startTime              endTime
======== ========== ===================== =====================
 XYZ      26         2018-09-17 10:00:01   2018-09-17 10:00:04
 XYZ      17         2018-09-17 10:00:05   2018-09-17 10:00:07

```

` symbol   sumPrice        startTime              endTime
======== ========== ===================== =====================
 XYZ      26         2018-09-17 10:00:01   2018-09-17 10:00:04
 XYZ      17         2018-09-17 10:00:05   2018-09-17 10:00:07
`

The first result matched against the rows #1, #2, #3, #4.


The second result matched against the rows #5, #6, #7.


##### AFTER MATCH SKIP TO NEXT ROW#

`AFTER MATCH SKIP TO NEXT ROW`

```
 symbol   sumPrice        startTime              endTime
======== ========== ===================== =====================
 XYZ      26         2018-09-17 10:00:01   2018-09-17 10:00:04
 XYZ      24         2018-09-17 10:00:02   2018-09-17 10:00:05
 XYZ      25         2018-09-17 10:00:03   2018-09-17 10:00:06
 XYZ      22         2018-09-17 10:00:04   2018-09-17 10:00:07
 XYZ      17         2018-09-17 10:00:05   2018-09-17 10:00:07

```

` symbol   sumPrice        startTime              endTime
======== ========== ===================== =====================
 XYZ      26         2018-09-17 10:00:01   2018-09-17 10:00:04
 XYZ      24         2018-09-17 10:00:02   2018-09-17 10:00:05
 XYZ      25         2018-09-17 10:00:03   2018-09-17 10:00:06
 XYZ      22         2018-09-17 10:00:04   2018-09-17 10:00:07
 XYZ      17         2018-09-17 10:00:05   2018-09-17 10:00:07
`

Again, the first result matched against the rows #1, #2, #3, #4.


Compared to the previous strategy, the next match includes row #2 again for the next matching.
Therefore, the second result matched against the rows #2, #3, #4, #5.


The third result matched against the rows #3, #4, #5, #6.


The forth result matched against the rows #4, #5, #6, #7.


The last result matched against the rows #5, #6, #7.


##### AFTER MATCH SKIP TO LAST A#

`AFTER MATCH SKIP TO LAST A`

```
 symbol   sumPrice        startTime              endTime
======== ========== ===================== =====================
 XYZ      26         2018-09-17 10:00:01   2018-09-17 10:00:04
 XYZ      25         2018-09-17 10:00:03   2018-09-17 10:00:06
 XYZ      17         2018-09-17 10:00:05   2018-09-17 10:00:07

```

` symbol   sumPrice        startTime              endTime
======== ========== ===================== =====================
 XYZ      26         2018-09-17 10:00:01   2018-09-17 10:00:04
 XYZ      25         2018-09-17 10:00:03   2018-09-17 10:00:06
 XYZ      17         2018-09-17 10:00:05   2018-09-17 10:00:07
`

Again, the first result matched against the rows #1, #2, #3, #4.


Compared to the previous strategy, the next match includes only row #3 (mapped to A) again for
the next matching. Therefore, the second result matched against the rows #3, #4, #5, #6.

`A`

The last result matched against the rows #5, #6, #7.


##### AFTER MATCH SKIP TO FIRST A#

`AFTER MATCH SKIP TO FIRST A`

This combination will produce a runtime exception because one would always try to start a new match
where the last one started. This would produce an infinite loop and, thus, is prohibited.


One has to keep in mind that in case of the SKIP TO FIRST/LAST variable strategy it might be
possible that there are no rows mapped to that variable (e.g. for pattern A*). In such cases, a
runtime exception will be thrown as the standard requires a valid row to continue the matching.

`SKIP TO FIRST/LAST variable`
`A*`

## Time attributes#


In order to apply some subsequent queries on top of the MATCH_RECOGNIZE it might be required to
use time attributes. To select those there are available two functions:

`MATCH_RECOGNIZE`
`MATCH_ROWTIME([rowtime_field])`

Returns the timestamp of the last row that was mapped to the given pattern.


The function accepts zero or one operand which is a field reference with rowtime attribute. If there is no operand, the function will return rowtime attribute with TIMESTAMP type. Otherwise, the return type will be same with the operand type.


The resulting attribute is a rowtime attribute
         that can be used in subsequent time-based operations such as
         interval joins and group window or over
         window aggregations.

`MATCH_PROCTIME()`

Returns a proctime attribute
          that can be used in subsequent time-based operations such as
          interval joins and group window or over
          window aggregations.


## Controlling Memory Consumption#


Memory consumption is an important consideration when writing MATCH_RECOGNIZE queries, as the
space of potential matches is built in a breadth-first-like manner. Having that in mind, one must
make sure that the pattern can finish. Preferably with a reasonable number of rows mapped to the
match as they have to fit into memory.

`MATCH_RECOGNIZE`

For example, the pattern must not have a quantifier without an upper limit that accepts every
single row. Such a pattern could look like this:


```
PATTERN (A B+ C)
DEFINE
  A as A.price > 10,
  C as C.price > 20

```

`PATTERN (A B+ C)
DEFINE
  A as A.price > 10,
  C as C.price > 20
`

The query will map every incoming row to the B variable and thus will never finish. This query
could be fixed, e.g., by negating the condition for C:

`B`
`C`

```
PATTERN (A B+ C)
DEFINE
  A as A.price > 10,
  B as B.price <= 20,
  C as C.price > 20

```

`PATTERN (A B+ C)
DEFINE
  A as A.price > 10,
  B as B.price <= 20,
  C as C.price > 20
`

Or by using the reluctant quantifier:


```
PATTERN (A B+? C)
DEFINE
  A as A.price > 10,
  C as C.price > 20

```

`PATTERN (A B+? C)
DEFINE
  A as A.price > 10,
  C as C.price > 20
`

Attention Please note that the MATCH_RECOGNIZE clause
does not use a configured state retention time.
One may want to use the WITHIN clause for this purpose.

`MATCH_RECOGNIZE`
`WITHIN`

## Known Limitations#


Flink’s implementation of the MATCH_RECOGNIZE clause is an ongoing effort, and some features of
the SQL standard are not yet supported.

`MATCH_RECOGNIZE`

Unsupported features include:

* Pattern expressions:

Pattern groups - this means that e.g. quantifiers can not be applied to a subsequence of the
pattern. Thus, (A (B C)+) is not a valid pattern.
Alterations - patterns like PATTERN((A B | C D) E), which means that either a subsequence
A B or C D has to be found before looking for the E row.
PERMUTE operator - which is equivalent to all permutations of variables that it was applied
to e.g. PATTERN (PERMUTE (A, B, C)) = PATTERN (A B C | A C B | B A C | B C A | C A B | C B A).
Anchors - ^, $, which denote beginning/end of a partition, those do not make sense in the
streaming context and will not be supported.
Exclusion - PATTERN ({- A -} B) meaning that A will be looked for but will not participate
in the output. This works only for the ALL ROWS PER MATCH mode.
Reluctant optional quantifier - PATTERN A?? only the greedy optional quantifier is supported.


* ALL ROWS PER MATCH output mode - which produces an output row for every row that participated
in the creation of a found match. This also means:

that the only supported semantic for the MEASURES clause is FINAL
CLASSIFIER function, which returns the pattern variable that a row was mapped to, is not yet
supported.


* SUBSET - which allows creating logical groups of pattern variables and using those groups in
the DEFINE and MEASURES clauses.
* Physical offsets - PREV/NEXT, which indexes all events seen rather than only those that were
mapped to a pattern variable (as in logical offsets case).
* Extracting time attributes - there is currently no possibility to get a time attribute for
subsequent time-based operations.
* MATCH_RECOGNIZE is supported only for SQL. There is no equivalent in the Table API.
* Aggregations:

distinct aggregations are not supported.


* Pattern groups - this means that e.g. quantifiers can not be applied to a subsequence of the
pattern. Thus, (A (B C)+) is not a valid pattern.
* Alterations - patterns like PATTERN((A B | C D) E), which means that either a subsequence
A B or C D has to be found before looking for the E row.
* PERMUTE operator - which is equivalent to all permutations of variables that it was applied
to e.g. PATTERN (PERMUTE (A, B, C)) = PATTERN (A B C | A C B | B A C | B C A | C A B | C B A).
* Anchors - ^, $, which denote beginning/end of a partition, those do not make sense in the
streaming context and will not be supported.
* Exclusion - PATTERN ({- A -} B) meaning that A will be looked for but will not participate
in the output. This works only for the ALL ROWS PER MATCH mode.
* Reluctant optional quantifier - PATTERN A?? only the greedy optional quantifier is supported.
`(A (B C)+)`
`PATTERN((A B | C D) E)`
`A B`
`C D`
`E`
`PERMUTE`
`PATTERN (PERMUTE (A, B, C))`
`PATTERN (A B C | A C B | B A C | B C A | C A B | C B A)`
`^, $`
`PATTERN ({- A -} B)`
`A`
`ALL ROWS PER MATCH`
`PATTERN A??`
`ALL ROWS PER MATCH`
* that the only supported semantic for the MEASURES clause is FINAL
* CLASSIFIER function, which returns the pattern variable that a row was mapped to, is not yet
supported.
`MEASURES`
`FINAL`
`CLASSIFIER`
`SUBSET`
`DEFINE`
`MEASURES`
`PREV/NEXT`
`MATCH_RECOGNIZE`
* distinct aggregations are not supported.

 Back to top
