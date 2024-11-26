# Transform Clause


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Transform Clause#


## Description#


The TRANSFORM clause allows user to transform inputs using user-specified command or script.

`TRANSFORM`

## Syntax#


```
query:
   SELECT TRANSFORM ( expression [ , ... ] )
   [ inRowFormat ]
   [ inRecordWriter ]
   USING command_or_script
   [ AS colName [ colType ] [ , ... ] ]
   [ outRowFormat ]
   [ outRecordReader ]

rowFormat
  : ROW FORMAT
    (DELIMITED [FIELDS TERMINATED BY char]
               [COLLECTION ITEMS TERMINATED BY char]
               [MAP KEYS TERMINATED BY char]
               [ESCAPED BY char]
               [LINES SEPARATED BY char]
     |
     SERDE serde_name [WITH SERDEPROPERTIES
                            property_name=property_value,
                            property_name=property_value, ...])
 
outRowFormat : rowFormat
inRowFormat : rowFormat
outRecordReader : RECORDREADER className
inRecordWriter: RECORDWRITER record_write_class

```

`query:
   SELECT TRANSFORM ( expression [ , ... ] )
   [ inRowFormat ]
   [ inRecordWriter ]
   USING command_or_script
   [ AS colName [ colType ] [ , ... ] ]
   [ outRowFormat ]
   [ outRecordReader ]

rowFormat
  : ROW FORMAT
    (DELIMITED [FIELDS TERMINATED BY char]
               [COLLECTION ITEMS TERMINATED BY char]
               [MAP KEYS TERMINATED BY char]
               [ESCAPED BY char]
               [LINES SEPARATED BY char]
     |
     SERDE serde_name [WITH SERDEPROPERTIES
                            property_name=property_value,
                            property_name=property_value, ...])
 
outRowFormat : rowFormat
inRowFormat : rowFormat
outRecordReader : RECORDREADER className
inRecordWriter: RECORDWRITER record_write_class
`

> 
Note:

MAP .. and REDUCE .. are syntactic transformations of SELECT TRANSFORM ( ... ) in Hive dialect for such query.
So you can use MAP / REDUCE to replace SELECT TRANSFORM.




Note:

* MAP .. and REDUCE .. are syntactic transformations of SELECT TRANSFORM ( ... ) in Hive dialect for such query.
So you can use MAP / REDUCE to replace SELECT TRANSFORM.
`MAP ..`
`REDUCE ..`
`SELECT TRANSFORM ( ... )`
`MAP`
`REDUCE`
`SELECT TRANSFORM`

## Parameters#

* 
inRowFormat
Specific use what row format to feed to input data into the running script.
By default, columns will be transformed to STRING and delimited by TAB before feeding to the user script;
Similarly, all NULL values will be converted to the literal string \N in order to differentiate NULL values from empty strings.

* 
outRowFormat
Specific use what row format to read the output from the running script.
By default, the standard output of the user script will be treated as TAB-separated STRING columns,
any cell containing only \N will be re-interpreted as a NULL,
and then the resulting STRING column will be cast to the data type specified in the table declaration in the usual way.

* 
inRecordWriter
Specific use what writer(fully-qualified class name) to write the input data. The default is org.apache.hadoop.hive.ql.exec.TextRecordWriter

* 
outRecordReader
Specific use what reader(fully-qualified class name) to read the output data. The default is org.apache.hadoop.hive.ql.exec.TextRecordReader

* 
command_or_script
Specifies a command or a path to script to process data.

Note:

Add a script file and then transform input using the script is not supported yet.
The script used must be a local script and should be accessible on all hosts in the cluster.



* 
colType
Specific the output of the command/script should be cast what data type. By default, it will be STRING data type.


inRowFormat


Specific use what row format to feed to input data into the running script.
By default, columns will be transformed to STRING and delimited by TAB before feeding to the user script;
Similarly, all NULL values will be converted to the literal string \N in order to differentiate NULL values from empty strings.

`STRING`
`TAB`
`NULL`
`\N`
`NULL`

outRowFormat


Specific use what row format to read the output from the running script.
By default, the standard output of the user script will be treated as TAB-separated STRING columns,
any cell containing only \N will be re-interpreted as a NULL,
and then the resulting STRING column will be cast to the data type specified in the table declaration in the usual way.

`STRING`
`\N`
`NULL`
`STRING`

inRecordWriter


Specific use what writer(fully-qualified class name) to write the input data. The default is org.apache.hadoop.hive.ql.exec.TextRecordWriter

`org.apache.hadoop.hive.ql.exec.TextRecordWriter`

outRecordReader


Specific use what reader(fully-qualified class name) to read the output data. The default is org.apache.hadoop.hive.ql.exec.TextRecordReader

`org.apache.hadoop.hive.ql.exec.TextRecordReader`

command_or_script


Specifies a command or a path to script to process data.


> 
Note:

Add a script file and then transform input using the script is not supported yet.
The script used must be a local script and should be accessible on all hosts in the cluster.




Note:

* Add a script file and then transform input using the script is not supported yet.
* The script used must be a local script and should be accessible on all hosts in the cluster.

colType


Specific the output of the command/script should be cast what data type. By default, it will be STRING data type.

`STRING`

For the clause ( AS colName ( colType )? [, ... ] )?, please be aware the following behavior:

`( AS colName ( colType )? [, ... ] )?`
* If the actual number of output columns is less than user specified output columns, additional user specified out columns will be filled with NULL.
* If the actual number of output columns is more than user specified output columns, the actual output will be truncated, keeping the corresponding columns.
* If user don’t specific the clause ( AS colName ( colType )? [, ... ] )?, the default output schema is (key: STRING, value: STRING).
The key column contains all the characters before the first tab and the value column contains the remaining characters after the first tab.
If there is no tab, it will return the NULL value for the second column value.
Note that this is different from specifying AS key, value because in that case, value will only contain the portion between the first tab and the second tab if there are multiple tabs.
`( AS colName ( colType )? [, ... ] )?`
`(key: STRING, value: STRING)`
`value`
`key, value`
`value`

## Examples#


```
CREATE TABLE src(key string, value string);
-- transform using
SELECT TRANSFORM(key, value) USING 'cat' from t1;

-- transform using with specific record writer and record reader
SELECT TRANSFORM(key, value) ROW FORMAT SERDE 'MySerDe'
 WITH SERDEPROPERTIES ('p1'='v1','p2'='v2')
 RECORDWRITER 'MyRecordWriter'
 USING 'cat'
 ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
 RECORDREADER 'MyRecordReader' FROM src;
 
-- use keyword MAP instead of TRANSFORM
FROM src INSERT OVERWRITE TABLE dest1 MAP src.key, CAST(src.key / 10 AS INT) USING 'cat' AS (c1, c2);

-- specific the output of transform
SELECT TRANSFORM(key, value) USING 'cat' AS c1, c2;
SELECT TRANSFORM(key, value) USING 'cat' AS (c1 INT, c2 INT);

```

`CREATE TABLE src(key string, value string);
-- transform using
SELECT TRANSFORM(key, value) USING 'cat' from t1;

-- transform using with specific record writer and record reader
SELECT TRANSFORM(key, value) ROW FORMAT SERDE 'MySerDe'
 WITH SERDEPROPERTIES ('p1'='v1','p2'='v2')
 RECORDWRITER 'MyRecordWriter'
 USING 'cat'
 ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
 RECORDREADER 'MyRecordReader' FROM src;
 
-- use keyword MAP instead of TRANSFORM
FROM src INSERT OVERWRITE TABLE dest1 MAP src.key, CAST(src.key / 10 AS INT) USING 'cat' AS (c1, c2);

-- specific the output of transform
SELECT TRANSFORM(key, value) USING 'cat' AS c1, c2;
SELECT TRANSFORM(key, value) USING 'cat' AS (c1 INT, c2 INT);
`