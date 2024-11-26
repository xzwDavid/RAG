# SET Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# SET Statements#


## Description#


The SET statement sets a property which provide a ways to set variables for a session and
configuration property including system variable and Hive configuration.
But environment variable can’t be set via SET statement. The behavior of SET with Hive dialect is compatible to Hive’s.

`SET`
`SET`
`SET`

## EXAMPLES#


```
-- set Flink's configuration
SET table.sql-dialect=default;

-- set Hive's configuration
SET hiveconf:k1=v1;

-- set system property
SET system:k2=v2;

-- set vairable for current session
SET hivevar:k3=v3;

-- get value for configuration
SET table.sql-dialect;
SET hiveconf:k1;
SET system:k2;
SET hivevar:k3;

-- only print Flink's configuration
SET;

-- print all configurations
SET -v;

```

`-- set Flink's configuration
SET table.sql-dialect=default;

-- set Hive's configuration
SET hiveconf:k1=v1;

-- set system property
SET system:k2=v2;

-- set vairable for current session
SET hivevar:k3=v3;

-- get value for configuration
SET table.sql-dialect;
SET hiveconf:k1;
SET system:k2;
SET hivevar:k3;

-- only print Flink's configuration
SET;

-- print all configurations
SET -v;
`

> 
Note:

In Hive, the SET command SET xx=yy whose key has no prefix is equivalent to SET hiveconf:xx=yy, which means it’ll set it to Hive Conf.
But in Flink, with Hive dialect, such SET command set xx=yy will set xx with value yy to Flink’s configuration.
So, if you want to set configuration to Hive’s Conf, please add the prefix hiveconf:, using the  SET command like SET hiveconf:xx=yy.
In Hive dialect, the key/value to be set shouldn’t be quoted.




Note:

* In Hive, the SET command SET xx=yy whose key has no prefix is equivalent to SET hiveconf:xx=yy, which means it’ll set it to Hive Conf.
But in Flink, with Hive dialect, such SET command set xx=yy will set xx with value yy to Flink’s configuration.
So, if you want to set configuration to Hive’s Conf, please add the prefix hiveconf:, using the  SET command like SET hiveconf:xx=yy.
* In Hive dialect, the key/value to be set shouldn’t be quoted.
`SET`
`SET xx=yy`
`SET hiveconf:xx=yy`
`SET`
`set xx=yy`
`xx`
`yy`
`hiveconf:`
`SET`
`SET hiveconf:xx=yy`
`key`
`value`