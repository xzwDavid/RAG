# Temporal Table Function


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Temporal Table Function#


A Temporal table function provides access to the version of a temporal table at a specific point in time.
In order to access the data in a temporal table, one must pass a time attribute that determines the version of the table that will be returned.
Flink uses the SQL syntax of table functions to provide a way to express it.


Unlike a versioned table, temporal table functions can only be defined on top of append-only streams
â it does not support changelog inputs.
Additionally, a temporal table function cannot be defined in pure SQL DDL.


## Defining a Temporal Table Function#


Temporal table functions can be defined on top of append-only streams using the Table API.
The table is registered with one or more key columns, and a time attribute used for versioning.


Suppose we have an append-only table of currency rates that we would like to
register as a temporal table function.


```
SELECT * FROM currency_rates;

update_time   currency   rate
============= =========  ====
09:00:00      Yen        102
09:00:00      Euro       114
09:00:00      USD        1
11:15:00      Euro       119
11:49:00      Pounds     108

```

`SELECT * FROM currency_rates;

update_time   currency   rate
============= =========  ====
09:00:00      Yen        102
09:00:00      Euro       114
09:00:00      USD        1
11:15:00      Euro       119
11:49:00      Pounds     108
`

Using the Table API, we can register this stream using currency for the key and update_time as
the versioning time attribute.

`currency`
`update_time`

```
TemporalTableFunction rates = tEnv
    .from("currency_rates")
    .createTemporalTableFunction("update_time", "currency");
 
tEnv.createTemporarySystemFunction("rates", rates);                                                        

```

`TemporalTableFunction rates = tEnv
    .from("currency_rates")
    .createTemporalTableFunction("update_time", "currency");
 
tEnv.createTemporarySystemFunction("rates", rates);                                                        
`

```
rates = tEnv
    .from("currency_rates")
    .createTemporalTableFunction("update_time", "currency")
 
tEnv.createTemporarySystemFunction("rates", rates)

```

`rates = tEnv
    .from("currency_rates")
    .createTemporalTableFunction("update_time", "currency")
 
tEnv.createTemporarySystemFunction("rates", rates)
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

## Temporal Table Function Join#


Once defined, a temporal table function is used as a standard table function.
Append-only tables (left input/probe side) can join with a temporal table (right input/build side),
i.e., a table that changes over time and tracks its changes, to retrieve the value for a key as it was at a particular point in time.


Consider an append-only table orders that tracks customers’ orders in different currencies.

`orders`

```
SELECT * FROM orders;

order_time amount currency
========== ====== =========
10:15        2    Euro
10:30        1    USD
10:32       50    Yen
10:52        3    Euro
11:04        5    USD

```

`SELECT * FROM orders;

order_time amount currency
========== ====== =========
10:15        2    Euro
10:30        1    USD
10:32       50    Yen
10:52        3    Euro
11:04        5    USD
`

Given these tables, we would like to convert orders to a common currency â USD.


```
SELECT
  SUM(amount * rate) AS amount
FROM
  orders,
  LATERAL TABLE (rates(order_time))
WHERE
  rates.currency = orders.currency

```

`SELECT
  SUM(amount * rate) AS amount
FROM
  orders,
  LATERAL TABLE (rates(order_time))
WHERE
  rates.currency = orders.currency
`

```
Table result = orders
    .joinLateral(call("rates", $("o_proctime")), $("o_currency").isEqual($("r_currency")))
    .select($("(o_amount").times($("r_rate")).sum().as("amount"));

```

`Table result = orders
    .joinLateral(call("rates", $("o_proctime")), $("o_currency").isEqual($("r_currency")))
    .select($("(o_amount").times($("r_rate")).sum().as("amount"));
`

```
val result = orders
    .joinLateral($"rates(order_time)", $"orders.currency = rates.currency")
    .select($"(o_amount * r_rate).sum as amount"))

```

`val result = orders
    .joinLateral($"rates(order_time)", $"orders.currency = rates.currency")
    .select($"(o_amount * r_rate).sum as amount"))
`

```
Still not supported in Python API.

```

`Still not supported in Python API.
`

 Back to top
