# SET Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# SET Statements#


SET statements are used to modify the configuration or list the configuration.

`SET`

## Run a SET statement#


SET statements can be executed in SQL CLI.

`SET`

The following examples show how to run a SET statement in SQL CLI.

`SET`

```
Flink SQL> SET 'table.local-time-zone' = 'Europe/Berlin';
[INFO] Session property has been set.

Flink SQL> SET;
'table.local-time-zone' = 'Europe/Berlin'

```

`Flink SQL> SET 'table.local-time-zone' = 'Europe/Berlin';
[INFO] Session property has been set.

Flink SQL> SET;
'table.local-time-zone' = 'Europe/Berlin'
`

## Syntax#


```
SET ('key' = 'value')?

```

`SET ('key' = 'value')?
`

If no key and value are specified, it just prints all the properties. Otherwise, set the key with specified value.


 Back to top
