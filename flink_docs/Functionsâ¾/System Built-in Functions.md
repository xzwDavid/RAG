# System (Built-in) Functions


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# System (Built-in) Functions#


Flink Table API & SQL provides users with a set of built-in functions for data transformations. This page gives a brief overview of them.
If a function that you need is not supported yet, you can implement a user-defined function.
If you think that the function is general enough, please open a Jira issue for it with a detailed description.


## Scalar Functions#


The scalar functions take zero, one or more values as the input and return a single value as the result.


### Comparison Functions#


### Logical Functions#


### Arithmetic Functions#

* numeric
* numeric

Converts hexadecimal string expr to BINARY.


If the length of expr is odd, the first character is discarded and the result is left padded with a null byte.


expr <CHAR | VARCHAR>


Returns a BINARY. NULL if expr is NULL or expr contains non-hex characters.

`NULL`
`NULL`

Returns the exact percentile value of expr at the specified percentage in a group.


percentage must be a literal numeric value between [0.0, 1.0] or an array of such values.
If a variable expression is passed to this function, the result will be calculated using any one of them.
frequency describes how many times expr should be counted, the default value is 1.

`[0.0, 1.0]`

If no expr lies exactly at the desired percentile, the result is calculated using linear interpolation of the two nearest exprs.
If expr or frequency is NULL, or frequency is not positive, the input row will be ignored.

`NULL`

NOTE: It is recommended to use this function in a window scenario, as it typically offers better performance.
In a regular group aggregation scenario, users should be aware of the performance overhead caused by a full sort triggered by each record.


value <NUMERIC>, percentage [<NUMERIC NOT NULL> | <ARRAY<NUMERIC NOT NULL> NOT NULL>], frequency <INTEGER_NUMERIC>
(INTEGER_NUMERIC: TINYINT, SMALLINT, INTEGER, BIGINT)
(NUMERIC: INTEGER_NUMERIC, FLOAT, DOUBLE, DECIMAL)

`value <NUMERIC>, percentage [<NUMERIC NOT NULL> | <ARRAY<NUMERIC NOT NULL> NOT NULL>], frequency <INTEGER_NUMERIC>`
`(INTEGER_NUMERIC: TINYINT, SMALLINT, INTEGER, BIGINT)`
`(NUMERIC: INTEGER_NUMERIC, FLOAT, DOUBLE, DECIMAL)`

Returns a DOUBLE if percentage is numeric, or an ARRAY<DOUBLE> if percentage is an array. NULL if percentage is an empty array.

`DOUBLE`
`ARRAY<DOUBLE>`
`NULL`

### String Functions#


Returns a formatted string from printf-style format string.


The function exploits the java.util.Formatter class with Locale.US.


null obj is formated as a string “null”.


format <CHAR | VARCHAR>, obj 


Returns a STRING representation of the formatted string. NULL if format is NULL or invalid.

`NULL`
`NULL`

Removes any leading characters within trimStr from str. trimStr is set to whitespace by default.


E.g., ’ This is a test String.’.ltrim() returns “This is a test String.”.


str <CHAR | VARCHAR>, trimStr <CHAR | VARCHAR>


Returns a STRING representation of the trimmed str. NULL if any of the arguments are NULL.

`NULL`
`NULL`

Removes any trailing characters within trimStr from str. trimStr is set to whitespace by default.


E.g., ‘This is a test String. ‘.rtrim() returns “This is a test String.”.


str <CHAR | VARCHAR>, trimStr <CHAR | VARCHAR>


Returns a STRING representation of the trimmed str. NULL if any of the arguments are NULL.

`NULL`
`NULL`

Removes any leading and trailing characters within trimStr from str. trimStr is set to whitespace by default.


str <CHAR | VARCHAR>, trimStr <CHAR | VARCHAR>


Returns a STRING representation of the trimmed str. NULL if any of the arguments are NULL.

`NULL`
`NULL`

Returns whether expr starts with startExpr. If startExpr is empty, the result is true.


expr and startExpr should have same type.


expr <CHAR | VARCHAR>, startExpr <CHAR | VARCHAR>

`expr <CHAR | VARCHAR>, startExpr <CHAR | VARCHAR>`

expr <BINARY | VARBINARY>, startExpr <BINARY | VARBINARY>

`expr <BINARY | VARBINARY>, startExpr <BINARY | VARBINARY>`

Returns a BOOLEAN. NULL if any of the arguments are NULL.

`BOOLEAN`
`NULL`
`NULL`

Returns whether expr ends with endExpr. If endExpr is empty, the result is true.


expr and endExpr should have same type.


expr <CHAR | VARCHAR>, endExpr <CHAR | VARCHAR>

`expr <CHAR | VARCHAR>, endExpr <CHAR | VARCHAR>`

expr <BINARY | VARBINARY>, endExpr <BINARY | VARBINARY>

`expr <BINARY | VARBINARY>, endExpr <BINARY | VARBINARY>`

Returns a BOOLEAN. NULL if any of the arguments are NULL.

`BOOLEAN`
`NULL`
`NULL`

Returns the number of times str matches the regex pattern. regex must be a Java regular expression.


str <CHAR | VARCHAR>, regex <CHAR | VARCHAR>

`str <CHAR | VARCHAR>, regex <CHAR | VARCHAR>`

Returns an INTEGER representation of the number of matches. NULL if any of the arguments are NULL or regex is invalid.

`INTEGER`
`NULL`
`NULL`

Returns a string from string1 which extracted with a specified
regular expression string2 and a regex match group index integer.


The regex match group index starts from 1 and 0 means matching
the whole regex. In addition, the regex match group index should
not exceed the number of the defined groups.


E.g. REGEXP_EXTRACT(‘foothebar’, ‘foo(.*?)(bar)’, 2)" returns “bar”.


Extracts all the substrings in str that match the regex expression and correspond to the regex group extractIndex.


regex may contain multiple groups. extractIndex indicates which regex group to extract and starts from 1, also the default value if not specified. 0 means matching the entire regular expression.


str <CHAR | VARCHAR>, regex <CHAR | VARCHAR>, extractIndex <TINYINT | SMALLINT | INTEGER | BIGINT>

`str <CHAR | VARCHAR>, regex <CHAR | VARCHAR>, extractIndex <TINYINT | SMALLINT | INTEGER | BIGINT>`

Returns an ARRAY<STRING> representation of all the matched substrings. NULL if any of the arguments are NULL or invalid.

`ARRAY<STRING>`
`NULL`
`NULL`

Returns the position of the first substring in str that matches regex.


Result indexes begin at 1, 0 if there is no match.


str <CHAR | VARCHAR>, regex <CHAR | VARCHAR>

`str <CHAR | VARCHAR>, regex <CHAR | VARCHAR>`

Returns an INTEGER representation of the first matched substring index. NULL if any of the arguments are NULL or regex is invalid.

`INTEGER`
`NULL`
`NULL`

Returns the first substring in str that matches regex.


str <CHAR | VARCHAR>, regex <CHAR | VARCHAR>

`str <CHAR | VARCHAR>, regex <CHAR | VARCHAR>`

Returns an STRING representation of the first matched substring. NULL if any of the arguments are NULL or regex if invalid or pattern is not found.

`STRING`
`NULL`
`NULL`

Translate an expr where all characters in fromStr have been replaced with those in toStr.


If toStr has a shorter length than fromStr, unmatched characters are removed.


expr <CHAR | VARCHAR>, fromStr <CHAR | VARCHAR>, toStr <CHAR | VARCHAR>

`expr <CHAR | VARCHAR>, fromStr <CHAR | VARCHAR>, toStr <CHAR | VARCHAR>`

Returns a STRING of translated expr.

`STRING`

Returns the specified part from the URL. Valid values for string2 include ‘HOST’, ‘PATH’, ‘QUERY’, ‘REF’, ‘PROTOCOL’, ‘AUTHORITY’, ‘FILE’, and ‘USERINFO’. Returns NULL if any of arguments is NULL.


E.g., parse_url(‘http://facebook.com/path1/p.php?k1=v1&k2=v2#Ref1', ‘HOST’), returns ‘facebook.com’.


Also a value of a particular key in QUERY can be extracted by providing the key as the third argument string3.


E.g., parse_url(‘http://facebook.com/path1/p.php?k1=v1&k2=v2#Ref1', ‘QUERY’, ‘k1’) returns ‘v1’.

`<([{\^-=$!|]})?*+.>`

Returns the index-th expression. index must be an integer between 1 and the number of expressions.


index <TINYINT | SMALLINT | INTEGER | BIGINT>, expr <CHAR | VARCHAR>, exprs <CHAR | VARCHAR>


index <TINYINT | SMALLINT | INTEGER | BIGINT>, expr <BINARY | VARBINARY>, exprs <BINARY | VARBINARY>


The result has the type of the least common type of all expressions. NULL if index is NULL or out of range.

`NULL`
`NULL`

### Temporal Functions#


Parses an interval string in the form “dd hh:mm:ss.fff” for SQL intervals of milliseconds or “yyyy-mm” for SQL intervals of months.
An interval range might be DAY, MINUTE, DAY TO HOUR, or DAY TO SECOND for intervals of milliseconds; YEAR or YEAR TO MONTH for intervals of months.


E.g., INTERVAL ‘10 00:00:00.004’ DAY TO SECOND, INTERVAL ‘10’ DAY, or INTERVAL ‘2-10’ YEAR TO MONTH return intervals.


Converts a date time string string1 with format string2 (by default: yyyy-MM-dd HH:mm:ss if not specified) to Unix timestamp (in seconds), using the specified timezone in table config.


If a time zone is specified in the date time string and parsed by UTC+X format such as “yyyy-MM-dd HH:mm:ss.SSS X”, this function will use the specified timezone in the date time string instead of the timezone in table config.
If the date time string can not be parsed, the default value Long.MIN_VALUE(-9223372036854775808) will be returned.


```
Flink SQL> SET 'table.local-time-zone' = 'Europe/Berlin';

-- Returns 25201
Flink SQL> SELECT UNIX_TIMESTAMP('1970-01-01 08:00:01.001', 'yyyy-MM-dd HH:mm:ss.SSS');
-- Returns 1
Flink SQL> SELECT UNIX_TIMESTAMP('1970-01-01 08:00:01.001 +0800', 'yyyy-MM-dd HH:mm:ss.SSS X');
-- Returns 25201
Flink SQL> SELECT UNIX_TIMESTAMP('1970-01-01 08:00:01.001 +0800', 'yyyy-MM-dd HH:mm:ss.SSS');
-- Returns -9223372036854775808
Flink SQL> SELECT UNIX_TIMESTAMP('1970-01-01 08:00:01.001', 'yyyy-MM-dd HH:mm:ss.SSS X');

```

`Flink SQL> SET 'table.local-time-zone' = 'Europe/Berlin';

-- Returns 25201
Flink SQL> SELECT UNIX_TIMESTAMP('1970-01-01 08:00:01.001', 'yyyy-MM-dd HH:mm:ss.SSS');
-- Returns 1
Flink SQL> SELECT UNIX_TIMESTAMP('1970-01-01 08:00:01.001 +0800', 'yyyy-MM-dd HH:mm:ss.SSS X');
-- Returns 25201
Flink SQL> SELECT UNIX_TIMESTAMP('1970-01-01 08:00:01.001 +0800', 'yyyy-MM-dd HH:mm:ss.SSS');
-- Returns -9223372036854775808
Flink SQL> SELECT UNIX_TIMESTAMP('1970-01-01 08:00:01.001', 'yyyy-MM-dd HH:mm:ss.SSS X');
`

Returns the current watermark for the given rowtime attribute, or NULL if no common watermark of all upstream operations is available at the current operation in the pipeline.
The return type of the function is inferred to match that of the provided rowtime attribute, but with an adjusted precision of 3. For example, if the rowtime attribute is TIMESTAMP_LTZ(9), the function will return TIMESTAMP_LTZ(3).

`NULL`
`TIMESTAMP_LTZ(9)`
`TIMESTAMP_LTZ(3)`

Note that this function can return NULL, and you may have to consider this case. For example, if you want to filter out late data you can use:

`NULL`

```
WHERE
  CURRENT_WATERMARK(ts) IS NULL
  OR ts > CURRENT_WATERMARK(ts)

```

`WHERE
  CURRENT_WATERMARK(ts) IS NULL
  OR ts > CURRENT_WATERMARK(ts)
`

### Conditional Functions#


Returns the first argument that is not NULL.


If all arguments are NULL, it returns NULL as well. The return type is the least restrictive, common type of all of its arguments.
The return type is nullable if all arguments are nullable as well.


```
-- Returns 'default'
COALESCE(NULL, 'default')

-- Returns the first non-null value among f0 and f1,
-- or 'default' if f0 and f1 are both NULL
COALESCE(f0, f1, 'default')

```

`-- Returns 'default'
COALESCE(NULL, 'default')

-- Returns the first non-null value among f0 and f1,
-- or 'default' if f0 and f1 are both NULL
COALESCE(f0, f1, 'default')
`

Returns null_replacement if input is NULL; otherwise input is returned.


Compared to COALESCE or CASE WHEN, this function returns a data type that is very specific in terms of nullability. The returned type is the common type of both arguments but only nullable if the null_replacement is nullable.


The function allows to pass nullable columns into a function or table that is declared with a NOT NULL constraint.


E.g., IFNULL(nullable_column, 5) returns never NULL.


### Type Conversion Functions#


### Collection Functions#


### JSON Functions#


JSON functions make use of JSON path expressions as described in ISO/IEC TR 19075-6 of the SQL
standard. Their syntax is inspired by and adopts many features of ECMAScript, but is neither a
subset nor superset thereof.


Path expressions come in two flavors, lax and strict. When omitted, it defaults to the strict mode.
Strict mode is intended to examine data from a schema perspective and will throw errors whenever
data does not adhere to the path expression. However, functions like JSON_VALUE allow defining
fallback behavior if an error is encountered. Lax mode, on the other hand, is more forgiving and
converts errors to empty sequences.

`JSON_VALUE`

The special character $ denotes the root node in a JSON path. Paths can access properties ($.a),
array elements ($.a[0].b), or branch over all elements in an array ($.a[*].b).

`$`
`$.a`
`$.a[0].b`
`$.a[*].b`

Known Limitations:

* Not all features of Lax mode are currently supported correctly. This is an upstream bug
(CALCITE-4717). Non-standard behavior is not guaranteed.

Determine whether a given string is valid JSON.


Specifying the optional type argument puts a constraint on which type of JSON object is
allowed. If the string is valid JSON, but not that type, false is returned. The default is
VALUE.

`false`
`VALUE`

```
-- TRUE
'1' IS JSON
'[]' IS JSON
'{}' IS JSON

-- TRUE
'"abc"' IS JSON
-- FALSE
'abc' IS JSON
NULL IS JSON

-- TRUE
'1' IS JSON SCALAR
-- FALSE
'1' IS JSON ARRAY
-- FALSE
'1' IS JSON OBJECT

-- FALSE
'{}' IS JSON SCALAR
-- FALSE
'{}' IS JSON ARRAY
-- TRUE
'{}' IS JSON OBJECT

```

`-- TRUE
'1' IS JSON
'[]' IS JSON
'{}' IS JSON

-- TRUE
'"abc"' IS JSON
-- FALSE
'abc' IS JSON
NULL IS JSON

-- TRUE
'1' IS JSON SCALAR
-- FALSE
'1' IS JSON ARRAY
-- FALSE
'1' IS JSON OBJECT

-- FALSE
'{}' IS JSON SCALAR
-- FALSE
'{}' IS JSON ARRAY
-- TRUE
'{}' IS JSON OBJECT
`

Determines whether a JSON string satisfies a given path search criterion.


If the error behavior is omitted, FALSE ON ERROR is assumed as the default.

`FALSE ON ERROR`

```
-- TRUE
SELECT JSON_EXISTS('{"a": true}', '$.a');
-- FALSE
SELECT JSON_EXISTS('{"a": true}', '$.b');
-- TRUE
SELECT JSON_EXISTS('{"a": [{ "b": 1 }]}',
  '$.a[0].b');

-- TRUE
SELECT JSON_EXISTS('{"a": true}',
  'strict $.b' TRUE ON ERROR);
-- FALSE
SELECT JSON_EXISTS('{"a": true}',
  'strict $.b' FALSE ON ERROR);

```

`-- TRUE
SELECT JSON_EXISTS('{"a": true}', '$.a');
-- FALSE
SELECT JSON_EXISTS('{"a": true}', '$.b');
-- TRUE
SELECT JSON_EXISTS('{"a": [{ "b": 1 }]}',
  '$.a[0].b');

-- TRUE
SELECT JSON_EXISTS('{"a": true}',
  'strict $.b' TRUE ON ERROR);
-- FALSE
SELECT JSON_EXISTS('{"a": true}',
  'strict $.b' FALSE ON ERROR);
`

Serializes a value into JSON.


This function returns a JSON string containing the serialized value. If the value is NULL,
the function returns NULL.

`NULL`
`NULL`

```
-- NULL
JSON_STRING(CAST(NULL AS INT))

-- '1'
JSON_STRING(1)
-- 'true'
JSON_STRING(TRUE)
-- '"Hello, World!"'
JSON_STRING('Hello, World!')
-- '[1,2]'
JSON_STRING(ARRAY[1, 2])

```

`-- NULL
JSON_STRING(CAST(NULL AS INT))

-- '1'
JSON_STRING(1)
-- 'true'
JSON_STRING(TRUE)
-- '"Hello, World!"'
JSON_STRING('Hello, World!')
-- '[1,2]'
JSON_STRING(ARRAY[1, 2])
`

Extracts a scalar from a JSON string.


This method searches a JSON string for a given path expression and returns the value if the
value at that path is scalar. Non-scalar values cannot be returned. By default, the value is
returned as STRING. Using dataType a different type can be chosen, with the following
types being supported:

`STRING`
`dataType`
* VARCHAR / STRING
* BOOLEAN
* INTEGER
* DOUBLE
`VARCHAR`
`STRING`
`BOOLEAN`
`INTEGER`
`DOUBLE`

For empty path expressions or errors a behavior can be defined to either return null, raise
an error or return a defined default value instead. When omitted, the default is
NULL ON EMPTY or NULL ON ERROR, respectively. The default value may be a literal or an
expression. If the default value itself raises an error, it falls through to the error
behavior for ON EMPTY, and raises an error for ON ERROR.

`null`
`NULL ON EMPTY`
`NULL ON ERROR`
`ON EMPTY`
`ON ERROR`

For path contains special characters such as spaces, you can use ['property'] or ["property"]
to select the specified property in a parent object. Be sure to put single or double quotes around the property name.
When using JSON_VALUE in SQL, the path is a character parameter which is already single quoted,
so you have to escape the single quotes around property name, such as JSON_VALUE('{"a b": "true"}', '$.[''a b'']').

`['property']`
`["property"]`
`JSON_VALUE('{"a b": "true"}', '$.[''a b'']')`

```
-- "true"
JSON_VALUE('{"a": true}', '$.a')

-- TRUE
JSON_VALUE('{"a": true}', '$.a' RETURNING BOOLEAN)

-- "false"
JSON_VALUE('{"a": true}', 'lax $.b'
    DEFAULT FALSE ON EMPTY)

-- "false"
JSON_VALUE('{"a": true}', 'strict $.b'
    DEFAULT FALSE ON ERROR)

-- 0.998D
JSON_VALUE('{"a.b": [0.998,0.996]}','$.["a.b"][0]' 
    RETURNING DOUBLE)

-- "right"
JSON_VALUE('{"contains blank": "right"}', 'strict $.[''contains blank'']' NULL ON EMPTY DEFAULT 'wrong' ON ERROR)

```

`-- "true"
JSON_VALUE('{"a": true}', '$.a')

-- TRUE
JSON_VALUE('{"a": true}', '$.a' RETURNING BOOLEAN)

-- "false"
JSON_VALUE('{"a": true}', 'lax $.b'
    DEFAULT FALSE ON EMPTY)

-- "false"
JSON_VALUE('{"a": true}', 'strict $.b'
    DEFAULT FALSE ON ERROR)

-- 0.998D
JSON_VALUE('{"a.b": [0.998,0.996]}','$.["a.b"][0]' 
    RETURNING DOUBLE)

-- "right"
JSON_VALUE('{"contains blank": "right"}', 'strict $.[''contains blank'']' NULL ON EMPTY DEFAULT 'wrong' ON ERROR)
`

Extracts JSON values from a JSON string.


The result is returned as a STRING or ARRAY<STRING>. This can be controlled with the RETURNING clause.

`STRING`
`ARRAY<STRING>`
`RETURNING`

The wrappingBehavior determines whether the extracted value should be wrapped into an array,
and whether to do so unconditionally or only if the value itself isn’t an array already.

`wrappingBehavior`

onEmpty and onError determine the behavior in case the path expression is empty, or in
case an error was raised, respectively. By default, in both cases null is returned. Other
choices are to use an empty array, an empty object, or to raise an error.

`onEmpty`
`onError`
`null`

```
-- '{ "b": 1 }'
JSON_QUERY('{ "a": { "b": 1 } }', '$.a')
-- '[1, 2]'
JSON_QUERY('[1, 2]', '$')
-- NULL
JSON_QUERY(CAST(NULL AS STRING), '$')
-- '["c1","c2"]'
JSON_QUERY('{"a":[{"c":"c1"},{"c":"c2"}]}',
    'lax $.a[*].c')
-- ['c1','c2']
JSON_QUERY('{"a":[{"c":"c1"},{"c":"c2"}]}', 'lax $.a[*].c' RETURNING ARRAY<STRING>)

-- Wrap result into an array
-- '[{}]'
JSON_QUERY('{}', '$' WITH CONDITIONAL ARRAY WRAPPER)
-- '[1, 2]'
JSON_QUERY('[1, 2]', '$' WITH CONDITIONAL ARRAY WRAPPER)
-- '[[1, 2]]'
JSON_QUERY('[1, 2]', '$' WITH UNCONDITIONAL ARRAY WRAPPER)

-- Scalars must be wrapped to be returned
-- NULL
JSON_QUERY(1, '$')
-- '[1]'
JSON_QUERY(1, '$' WITH CONDITIONAL ARRAY WRAPPER)

-- Behavior if path expression is empty / there is an error
-- '{}'
JSON_QUERY('{}', 'lax $.invalid' EMPTY OBJECT ON EMPTY)
-- '[]'
JSON_QUERY('{}', 'strict $.invalid' EMPTY ARRAY ON ERROR)

```

`-- '{ "b": 1 }'
JSON_QUERY('{ "a": { "b": 1 } }', '$.a')
-- '[1, 2]'
JSON_QUERY('[1, 2]', '$')
-- NULL
JSON_QUERY(CAST(NULL AS STRING), '$')
-- '["c1","c2"]'
JSON_QUERY('{"a":[{"c":"c1"},{"c":"c2"}]}',
    'lax $.a[*].c')
-- ['c1','c2']
JSON_QUERY('{"a":[{"c":"c1"},{"c":"c2"}]}', 'lax $.a[*].c' RETURNING ARRAY<STRING>)

-- Wrap result into an array
-- '[{}]'
JSON_QUERY('{}', '$' WITH CONDITIONAL ARRAY WRAPPER)
-- '[1, 2]'
JSON_QUERY('[1, 2]', '$' WITH CONDITIONAL ARRAY WRAPPER)
-- '[[1, 2]]'
JSON_QUERY('[1, 2]', '$' WITH UNCONDITIONAL ARRAY WRAPPER)

-- Scalars must be wrapped to be returned
-- NULL
JSON_QUERY(1, '$')
-- '[1]'
JSON_QUERY(1, '$' WITH CONDITIONAL ARRAY WRAPPER)

-- Behavior if path expression is empty / there is an error
-- '{}'
JSON_QUERY('{}', 'lax $.invalid' EMPTY OBJECT ON EMPTY)
-- '[]'
JSON_QUERY('{}', 'strict $.invalid' EMPTY ARRAY ON ERROR)
`

Builds a JSON object string from a list of key-value pairs.


Note that keys must be non-NULL string literals, while values may be arbitrary expressions.

`NULL`

This function returns a JSON string. The ON NULL behavior defines how to treat NULL
values. If omitted, NULL ON NULL is assumed by default.

`ON NULL`
`NULL`
`NULL ON NULL`

Values which are created from another JSON construction function call (JSON_OBJECT,
JSON_ARRAY) are inserted directly rather than as a string. This allows building nested JSON
structures.

`JSON_OBJECT`
`JSON_ARRAY`

```
-- '{}'
JSON_OBJECT()

-- '{"K1":"V1","K2":"V2"}'
JSON_OBJECT('K1' VALUE 'V1', 'K2' VALUE 'V2')

-- Expressions as values
JSON_OBJECT('orderNo' VALUE orders.orderId)

-- ON NULL
JSON_OBJECT(KEY 'K1' VALUE CAST(NULL AS STRING) NULL ON NULL)   -- '{"K1":null}'
JSON_OBJECT(KEY 'K1' VALUE CAST(NULL AS STRING) ABSENT ON NULL) -- '{}'

-- '{"K1":{"K2":"V"}}'
JSON_OBJECT(
  KEY 'K1'
  VALUE JSON_OBJECT(
    KEY 'K2'
    VALUE 'V'
  )
)

```

`-- '{}'
JSON_OBJECT()

-- '{"K1":"V1","K2":"V2"}'
JSON_OBJECT('K1' VALUE 'V1', 'K2' VALUE 'V2')

-- Expressions as values
JSON_OBJECT('orderNo' VALUE orders.orderId)

-- ON NULL
JSON_OBJECT(KEY 'K1' VALUE CAST(NULL AS STRING) NULL ON NULL)   -- '{"K1":null}'
JSON_OBJECT(KEY 'K1' VALUE CAST(NULL AS STRING) ABSENT ON NULL) -- '{}'

-- '{"K1":{"K2":"V"}}'
JSON_OBJECT(
  KEY 'K1'
  VALUE JSON_OBJECT(
    KEY 'K2'
    VALUE 'V'
  )
)
`

Builds a JSON array string from a list of values.


This function returns a JSON string. The values can be arbitrary expressions. The ON NULL
behavior defines how to treat NULL values. If omitted, ABSENT ON NULL is assumed by
default.

`ON NULL`
`NULL`
`ABSENT ON NULL`

Elements which are created from another JSON construction function call (JSON_OBJECT,
JSON_ARRAY) are inserted directly rather than as a string. This allows building nested JSON
structures.

`JSON_OBJECT`
`JSON_ARRAY`

```
-- '[]'
JSON_ARRAY()
-- '[1,"2"]'
JSON_ARRAY(1, '2')

-- Expressions as values
JSON_ARRAY(orders.orderId)

-- ON NULL
JSON_ARRAY(CAST(NULL AS STRING) NULL ON NULL) -- '[null]'
JSON_ARRAY(CAST(NULL AS STRING) ABSENT ON NULL) -- '[]'

-- '[[1]]'
JSON_ARRAY(JSON_ARRAY(1))

```

`-- '[]'
JSON_ARRAY()
-- '[1,"2"]'
JSON_ARRAY(1, '2')

-- Expressions as values
JSON_ARRAY(orders.orderId)

-- ON NULL
JSON_ARRAY(CAST(NULL AS STRING) NULL ON NULL) -- '[null]'
JSON_ARRAY(CAST(NULL AS STRING) ABSENT ON NULL) -- '[]'

-- '[[1]]'
JSON_ARRAY(JSON_ARRAY(1))
`

### Value Construction Functions#


implicit constructor with parenthesis


(value1 [, value2]*)


explicit ROW constructor with


ROW(value1 [, value2]*)


Returns a row created from a list of values (value1, value2,…).


The implicit row constructor requires at least two fields. The explicit row constructor can deal with an arbitrary number of fields. Both of them support arbitrary expressions as fields.


### Value Access Functions#


### Grouping Functions#


### Hash Functions#


### Auxiliary Functions#


## Aggregate Functions#


The aggregate functions take an expression across all the rows as the input and return a single aggregated value as the result.

`n`
`n`
`ALL`
`NULL`
`DISTINCT`
`NULL`
`IGNORE NULLS`
`NULL`
`ORDER BY`

Builds a JSON object string by aggregating key-value expressions into a single JSON object.


The key expression must return a non-nullable character string. Value expressions can be
arbitrary, including other JSON functions. If a value is NULL, the ON NULL behavior
defines what to do. If omitted, NULL ON NULL is assumed by default.

`NULL`
`ON NULL`
`NULL ON NULL`

Note that keys must be unique. If a key occurs multiple times, an error will be thrown.


This function is currently not supported in OVER windows.

`OVER`

```
-- '{"Apple":2,"Banana":17,"Orange":0}'
SELECT
  JSON_OBJECTAGG(KEY product VALUE cnt)
FROM orders

```

`-- '{"Apple":2,"Banana":17,"Orange":0}'
SELECT
  JSON_OBJECTAGG(KEY product VALUE cnt)
FROM orders
`

Builds a JSON object string by aggregating items into an array.


Item expressions can be arbitrary, including other JSON functions. If a value is NULL, the
ON NULL behavior defines what to do. If omitted, ABSENT ON NULL is assumed by default.

`NULL`
`ON NULL`
`ABSENT ON NULL`

This function is currently not supported in OVER windows, unbounded session windows, or hop
windows.

`OVER`

```
-- '["Apple","Banana","Orange"]'
SELECT
  JSON_ARRAYAGG(product)
FROM orders

```

`-- '["Apple","Banana","Orange"]'
SELECT
  JSON_ARRAYAGG(product)
FROM orders
`

## Time Interval and Point Unit Specifiers#


The following table lists specifiers for time interval and time point units.


For Table API, please use _ for spaces (e.g., DAY_TO_HOUR).
Plural works for SQL only.

`_`
`DAY_TO_HOUR`
`MILLENNIUM`
`CENTURY`
`DECADE`
`YEAR(S)`
`YEAR`
`YEAR(S) TO MONTH(S)`
`QUARTER(S)`
`QUARTER`
`MONTH(S)`
`MONTH`
`WEEK(S)`
`WEEK`
`DAY(S)`
`DAY`
`DAY(S) TO HOUR(S)`
`DAY(S) TO MINUTE(S)`
`DAY(S) TO SECOND(S)`
`HOUR(S)`
`HOUR`
`HOUR(S) TO MINUTE(S)`
`HOUR(S) TO SECOND(S)`
`MINUTE(S)`
`MINUTE`
`MINUTE(S) TO SECOND(S)`
`SECOND(S)`
`SECOND`
`MILLISECOND`
`MILLISECOND`
`MICROSECOND`
`MICROSECOND`
`NANOSECOND`
`EPOCH`
`DOY`
`DOW`
`EPOCH`
`ISODOW`
`ISOYEAR`
`SQL_TSI_YEAR`
`SQL_TSI_QUARTER`
`SQL_TSI_MONTH`
`SQL_TSI_WEEK`
`SQL_TSI_DAY`
`SQL_TSI_HOUR`
`SQL_TSI_MINUTE`
`SQL_TSI_SECOND `

 Back to top


## Column Functions#


The column functions are used to select or deselect table columns.


> 
  Column functions are only used in Table API.


`SELECT *`

The detailed syntax is as follows:


```
columnFunction:
    withColumns(columnExprs)
    withoutColumns(columnExprs)
    withAllColumns()

columnExprs:
    columnExpr [, columnExpr]*

columnExpr:
    columnRef | columnIndex to columnIndex | columnName to columnName

columnRef:
    columnName(The field name that exists in the table) | columnIndex(a positive integer starting from 1)

```

`columnFunction:
    withColumns(columnExprs)
    withoutColumns(columnExprs)
    withAllColumns()

columnExprs:
    columnExpr [, columnExpr]*

columnExpr:
    columnRef | columnIndex to columnIndex | columnName to columnName

columnRef:
    columnName(The field name that exists in the table) | columnIndex(a positive integer starting from 1)
`

The usage of the column function is illustrated in the following table. (Suppose we have a table with 5 columns: (a: Int, b: Long, c: String, d:String, e: String)):

`(a: Int, b: Long, c: String, d:String, e: String)`

The column functions can be used in all places where column fields are expected, such as select, groupBy, orderBy, UDFs etc. e.g.:

`select, groupBy, orderBy, UDFs etc.`

```
table
    .groupBy(withColumns(range(1, 3)))
    .select(withColumns(range("a", "b")), myUDAgg(myUDF(withColumns(range(5, 20)))));

```

`table
    .groupBy(withColumns(range(1, 3)))
    .select(withColumns(range("a", "b")), myUDAgg(myUDF(withColumns(range(5, 20)))));
`

```
table
    .groupBy(withColumns(range(1, 3)))
    .select(withColumns('a to 'b), myUDAgg(myUDF(withColumns(5 to 20))))

```

`table
    .groupBy(withColumns(range(1, 3)))
    .select(withColumns('a to 'b), myUDAgg(myUDF(withColumns(5 to 20))))
`

```
table \
    .group_by(with_columns(range_(1, 3))) \
    .select(with_columns(range_('a', 'b')), myUDAgg(myUDF(with_columns(range_(5, 20)))))

```

`table \
    .group_by(with_columns(range_(1, 3))) \
    .select(with_columns(range_('a', 'b')), myUDAgg(myUDF(with_columns(range_(5, 20)))))
`

 Back to top
