# RESET Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# RESET Statements#


RESET statements are used to reset the configuration to the default.

`RESET`

## Run a RESET statement#


RESET statements can be executed in SQL CLI.

`RESET`

The following examples show how to run a RESET statement in SQL CLI.

`RESET`

```
Flink SQL> RESET 'table.planner';
[INFO] Session property has been reset.

Flink SQL> RESET;
[INFO] All session properties have been set to their default values.

```

`Flink SQL> RESET 'table.planner';
[INFO] Session property has been reset.

Flink SQL> RESET;
[INFO] All session properties have been set to their default values.
`

## Syntax#


```
RESET ('key')?

```

`RESET ('key')?
`

If no key is specified, it reset all the properties to the default. Otherwise, reset the specified key to the default.


 Back to top
