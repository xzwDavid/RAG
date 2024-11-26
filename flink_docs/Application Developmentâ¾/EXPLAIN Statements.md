# EXPLAIN Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# EXPLAIN Statements#


EXPLAIN statements are used to explain the logical and optimized query plans of a query or an INSERT statement.


## Run an EXPLAIN statement#


EXPLAIN statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns explain result for a successful EXPLAIN operation, otherwise will throw an exception.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run an EXPLAIN statement in TableEnvironment.

`TableEnvironment`

EXPLAIN statements can be executed with the executeSql() method of the TableEnvironment. The executeSql() method returns explain result for a successful EXPLAIN operation, otherwise will throw an exception.

`executeSql()`
`TableEnvironment`
`executeSql()`

The following examples show how to run an EXPLAIN statement in TableEnvironment.

`TableEnvironment`

EXPLAIN statements can be executed with the execute_sql() method of the TableEnvironment. The execute_sql() method returns explain result for a successful EXPLAIN operation, otherwise will throw an exception.

`execute_sql()`
`TableEnvironment`
`execute_sql()`

The following examples show how to run an EXPLAIN statement in TableEnvironment.

`TableEnvironment`

EXPLAIN statements can be executed in SQL CLI.


The following examples show how to run an EXPLAIN statement in SQL CLI.


```
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

// register a table named "Orders"
tEnv.executeSql("CREATE TABLE MyTable1 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')");
tEnv.executeSql("CREATE TABLE MyTable2 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')");

// explain SELECT statement through TableEnvironment.explainSql()
String explanation =
                tEnv.explainSql(
                        "SELECT `count`, COUNT(word) FROM ("
                                + "MyTable1 WHERE word LIKE 'F%' "
                                + "UNION ALL "
                                + "SELECT `count`, word FROM MyTable2) tmp"
                                + "GROUP BY `count`");
System.out.println(explanation);

// explain SELECT statement through TableEnvironment.executeSql()
TableResult tableResult =
                tEnv.executeSql(
                        "EXPLAIN PLAN FOR "
                                + "SELECT `count`, COUNT(word) FROM ("
                                + "MyTable1 WHERE word LIKE 'F%' "
                                + "UNION ALL "
                                + "SELECT `count`, word FROM MyTable2) tmp GROUP BY `count`");
tableResult.print();

TableResult tableResult2 =
                tEnv.executeSql(
                        "EXPLAIN ESTIMATED_COST, CHANGELOG_MODE, PLAN_ADVICE, JSON_EXECUTION_PLAN "
                                + "SELECT `count`, COUNT(word) FROM ("
                                + "MyTable1 WHERE word LIKE 'F%' "
                                + "UNION ALL "
                                + "SELECT `count`, word FROM MyTable2) tmp GROUP BY `count`");
tableResult2.print();

```

`StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
StreamTableEnvironment tEnv = StreamTableEnvironment.create(env);

// register a table named "Orders"
tEnv.executeSql("CREATE TABLE MyTable1 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')");
tEnv.executeSql("CREATE TABLE MyTable2 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')");

// explain SELECT statement through TableEnvironment.explainSql()
String explanation =
                tEnv.explainSql(
                        "SELECT `count`, COUNT(word) FROM ("
                                + "MyTable1 WHERE word LIKE 'F%' "
                                + "UNION ALL "
                                + "SELECT `count`, word FROM MyTable2) tmp"
                                + "GROUP BY `count`");
System.out.println(explanation);

// explain SELECT statement through TableEnvironment.executeSql()
TableResult tableResult =
                tEnv.executeSql(
                        "EXPLAIN PLAN FOR "
                                + "SELECT `count`, COUNT(word) FROM ("
                                + "MyTable1 WHERE word LIKE 'F%' "
                                + "UNION ALL "
                                + "SELECT `count`, word FROM MyTable2) tmp GROUP BY `count`");
tableResult.print();

TableResult tableResult2 =
                tEnv.executeSql(
                        "EXPLAIN ESTIMATED_COST, CHANGELOG_MODE, PLAN_ADVICE, JSON_EXECUTION_PLAN "
                                + "SELECT `count`, COUNT(word) FROM ("
                                + "MyTable1 WHERE word LIKE 'F%' "
                                + "UNION ALL "
                                + "SELECT `count`, word FROM MyTable2) tmp GROUP BY `count`");
tableResult2.print();
`

```
val env = StreamExecutionEnvironment.getExecutionEnvironment()
val tEnv = StreamTableEnvironment.create(env)

// register a table named "Orders"
tEnv.executeSql("CREATE TABLE MyTable1 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')")
tEnv.executeSql("CREATE TABLE MyTable2 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')")

// explain SELECT statement through TableEnvironment.explainSql()
val explanation = tEnv.explainSql(
"""
  |SELECT `count`, COUNT(word)
  |FROM (
  |  SELECT `count`, word FROM MyTable1
  |  WHERE word LIKE 'F%'
  |  UNION ALL 
  |  SELECT `count`, word FROM MyTable2 ) tmp
  |GROUP BY `count`
  |""".stripMargin)
println(explanation)

// explain SELECT statement through TableEnvironment.executeSql()
val tableResult = tEnv.executeSql(
"""
  |EXPLAIN PLAN FOR
  |SELECT `count`, COUNT(word)
  |FROM (
  |  SELECT `count`, word FROM MyTable1
  |  WHERE word LIKE 'F%'
  |  UNION ALL
  |  SELECT `count`, word FROM MyTable2 ) tmp
  |GROUP BY `count`
  |""".stripMargin)
tableResult.print()

val tableResult2 = tEnv.executeSql(
"""
  |EXPLAIN ESTIMATED_COST, CHANGELOG_MODE, PLAN_ADVICE, JSON_EXECUTION_PLAN
  |SELECT `count`, COUNT(word)
  |FROM (
  |  SELECT `count`, word FROM MyTable1
  |  WHERE word LIKE 'F%'
  |  UNION ALL
  |  SELECT `count`, word FROM MyTable2 ) tmp
  |GROUP BY `count`
  |""".stripMargin)
tableResult2.print()

```

`val env = StreamExecutionEnvironment.getExecutionEnvironment()
val tEnv = StreamTableEnvironment.create(env)

// register a table named "Orders"
tEnv.executeSql("CREATE TABLE MyTable1 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')")
tEnv.executeSql("CREATE TABLE MyTable2 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')")

// explain SELECT statement through TableEnvironment.explainSql()
val explanation = tEnv.explainSql(
"""
  |SELECT `count`, COUNT(word)
  |FROM (
  |  SELECT `count`, word FROM MyTable1
  |  WHERE word LIKE 'F%'
  |  UNION ALL 
  |  SELECT `count`, word FROM MyTable2 ) tmp
  |GROUP BY `count`
  |""".stripMargin)
println(explanation)

// explain SELECT statement through TableEnvironment.executeSql()
val tableResult = tEnv.executeSql(
"""
  |EXPLAIN PLAN FOR
  |SELECT `count`, COUNT(word)
  |FROM (
  |  SELECT `count`, word FROM MyTable1
  |  WHERE word LIKE 'F%'
  |  UNION ALL
  |  SELECT `count`, word FROM MyTable2 ) tmp
  |GROUP BY `count`
  |""".stripMargin)
tableResult.print()

val tableResult2 = tEnv.executeSql(
"""
  |EXPLAIN ESTIMATED_COST, CHANGELOG_MODE, PLAN_ADVICE, JSON_EXECUTION_PLAN
  |SELECT `count`, COUNT(word)
  |FROM (
  |  SELECT `count`, word FROM MyTable1
  |  WHERE word LIKE 'F%'
  |  UNION ALL
  |  SELECT `count`, word FROM MyTable2 ) tmp
  |GROUP BY `count`
  |""".stripMargin)
tableResult2.print()
`

```
table_env = StreamTableEnvironment.create(...)

t_env.execute_sql("CREATE TABLE MyTable1 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')")
t_env.execute_sql("CREATE TABLE MyTable2 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')")

# explain SELECT statement through TableEnvironment.explain_sql()
explanation1 = t_env.explain_sql(
    "SELECT `count`, COUNT(word) FROM (" 
    "MyTable1 WHERE word LIKE 'F%' "
    "UNION ALL "
    "SELECT `count`, word FROM MyTable2) tmp GROUP BY `count`")
print(explanation1)

# explain SELECT statement through TableEnvironment.execute_sql()
table_result = t_env.execute_sql(
    "EXPLAIN PLAN FOR "
    "SELECT `count`, COUNT(word) FROM (" 
    "MyTable1 WHERE word LIKE 'F%' "
    "UNION ALL "
    "SELECT `count`, word FROM MyTable2) tmp GROUP BY `count`")
table_result.print()

table_result2 = t_env.execute_sql(
    "EXPLAIN ESTIMATED_COST, CHANGELOG_MODE, PLAN_ADVICE, JSON_EXECUTION_PLAN "
    "SELECT `count`, COUNT(word) FROM (" 
    "MyTable1 WHERE word LIKE 'F%' "
    "UNION ALL "
    "SELECT `count`, word FROM MyTable2) tmp GROUP BY `count`")
table_result2.print()

```

`table_env = StreamTableEnvironment.create(...)

t_env.execute_sql("CREATE TABLE MyTable1 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')")
t_env.execute_sql("CREATE TABLE MyTable2 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen')")

# explain SELECT statement through TableEnvironment.explain_sql()
explanation1 = t_env.explain_sql(
    "SELECT `count`, COUNT(word) FROM (" 
    "MyTable1 WHERE word LIKE 'F%' "
    "UNION ALL "
    "SELECT `count`, word FROM MyTable2) tmp GROUP BY `count`")
print(explanation1)

# explain SELECT statement through TableEnvironment.execute_sql()
table_result = t_env.execute_sql(
    "EXPLAIN PLAN FOR "
    "SELECT `count`, COUNT(word) FROM (" 
    "MyTable1 WHERE word LIKE 'F%' "
    "UNION ALL "
    "SELECT `count`, word FROM MyTable2) tmp GROUP BY `count`")
table_result.print()

table_result2 = t_env.execute_sql(
    "EXPLAIN ESTIMATED_COST, CHANGELOG_MODE, PLAN_ADVICE, JSON_EXECUTION_PLAN "
    "SELECT `count`, COUNT(word) FROM (" 
    "MyTable1 WHERE word LIKE 'F%' "
    "UNION ALL "
    "SELECT `count`, word FROM MyTable2) tmp GROUP BY `count`")
table_result2.print()
`

```
Flink SQL> CREATE TABLE MyTable1 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen');
[INFO] Table has been created.

Flink SQL> CREATE TABLE MyTable2 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen');
[INFO] Table has been created.

Flink SQL> EXPLAIN PLAN FOR SELECT `count`, COUNT(word) FROM
> ( SELECT `count`, word FROM MyTable1 WHERE word LIKE 'F%' 
>   UNION ALL 
>   SELECT `count`, word FROM MyTable2 ) tmp GROUP BY `count`;
                                  
Flink SQL> EXPLAIN ESTIMATED_COST, CHANGELOG_MODE, PLAN_ADVICE, JSON_EXECUTION_PLAN SELECT `count`, COUNT(word) FROM
> ( SELECT `count`, word FROM MyTable1 WHERE word LIKE 'F%' 
>   UNION ALL 
>   SELECT `count`, word FROM MyTable2 ) tmp GROUP BY `count`;

```

`Flink SQL> CREATE TABLE MyTable1 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen');
[INFO] Table has been created.

Flink SQL> CREATE TABLE MyTable2 (`count` bigint, word VARCHAR(256)) WITH ('connector' = 'datagen');
[INFO] Table has been created.

Flink SQL> EXPLAIN PLAN FOR SELECT `count`, COUNT(word) FROM
> ( SELECT `count`, word FROM MyTable1 WHERE word LIKE 'F%' 
>   UNION ALL 
>   SELECT `count`, word FROM MyTable2 ) tmp GROUP BY `count`;
                                  
Flink SQL> EXPLAIN ESTIMATED_COST, CHANGELOG_MODE, PLAN_ADVICE, JSON_EXECUTION_PLAN SELECT `count`, COUNT(word) FROM
> ( SELECT `count`, word FROM MyTable1 WHERE word LIKE 'F%' 
>   UNION ALL 
>   SELECT `count`, word FROM MyTable2 ) tmp GROUP BY `count`;
`

The EXPLAIN result is:

`EXPLAIN`

```
== Abstract Syntax Tree ==
LogicalAggregate(group=[{0}], EXPR$1=[COUNT($1)])
+- LogicalUnion(all=[true])
   :- LogicalProject(count=[$0], word=[$1])
   :  +- LogicalFilter(condition=[LIKE($1, _UTF-16LE'F%')])
   :     +- LogicalTableScan(table=[[default_catalog, default_database, MyTable1]])
   +- LogicalProject(count=[$0], word=[$1])
      +- LogicalTableScan(table=[[default_catalog, default_database, MyTable2]])

== Optimized Physical Plan ==
GroupAggregate(groupBy=[count], select=[count, COUNT(word) AS EXPR$1])
+- Exchange(distribution=[hash[count]])
   +- Union(all=[true], union=[count, word])
      :- Calc(select=[count, word], where=[LIKE(word, _UTF-16LE'F%')])
      :  +- TableSourceScan(table=[[default_catalog, default_database, MyTable1]], fields=[count, word])
      +- TableSourceScan(table=[[default_catalog, default_database, MyTable2]], fields=[count, word])

== Optimized Execution Plan ==
GroupAggregate(groupBy=[count], select=[count, COUNT(word) AS EXPR$1])
+- Exchange(distribution=[hash[count]])
   +- Union(all=[true], union=[count, word])
      :- Calc(select=[count, word], where=[LIKE(word, 'F%')])
      :  +- TableSourceScan(table=[[default_catalog, default_database, MyTable1]], fields=[count, word])
      +- TableSourceScan(table=[[default_catalog, default_database, MyTable2]], fields=[count, word])

```

`== Abstract Syntax Tree ==
LogicalAggregate(group=[{0}], EXPR$1=[COUNT($1)])
+- LogicalUnion(all=[true])
   :- LogicalProject(count=[$0], word=[$1])
   :  +- LogicalFilter(condition=[LIKE($1, _UTF-16LE'F%')])
   :     +- LogicalTableScan(table=[[default_catalog, default_database, MyTable1]])
   +- LogicalProject(count=[$0], word=[$1])
      +- LogicalTableScan(table=[[default_catalog, default_database, MyTable2]])

== Optimized Physical Plan ==
GroupAggregate(groupBy=[count], select=[count, COUNT(word) AS EXPR$1])
+- Exchange(distribution=[hash[count]])
   +- Union(all=[true], union=[count, word])
      :- Calc(select=[count, word], where=[LIKE(word, _UTF-16LE'F%')])
      :  +- TableSourceScan(table=[[default_catalog, default_database, MyTable1]], fields=[count, word])
      +- TableSourceScan(table=[[default_catalog, default_database, MyTable2]], fields=[count, word])

== Optimized Execution Plan ==
GroupAggregate(groupBy=[count], select=[count, COUNT(word) AS EXPR$1])
+- Exchange(distribution=[hash[count]])
   +- Union(all=[true], union=[count, word])
      :- Calc(select=[count, word], where=[LIKE(word, 'F%')])
      :  +- TableSourceScan(table=[[default_catalog, default_database, MyTable1]], fields=[count, word])
      +- TableSourceScan(table=[[default_catalog, default_database, MyTable2]], fields=[count, word])
`

```
== Abstract Syntax Tree ==
LogicalAggregate(group=[{0}], EXPR$1=[COUNT($1)])
+- LogicalUnion(all=[true])
   :- LogicalProject(count=[$0], word=[$1])
   :  +- LogicalFilter(condition=[LIKE($1, _UTF-16LE'F%')])
   :     +- LogicalTableScan(table=[[default_catalog, default_database, MyTable1]])
   +- LogicalProject(count=[$0], word=[$1])
      +- LogicalTableScan(table=[[default_catalog, default_database, MyTable2]])

== Optimized Physical Plan With Advice ==
GroupAggregate(advice=[1], groupBy=[count], select=[count, COUNT(word) AS EXPR$1], changelogMode=[I,UA]): rowcount = 1.05E8, cumulative cost = {5.2E8 rows, 1.805E10 cpu, 4.0E9 io, 2.1E9 network, 0.0 memory}
+- Exchange(distribution=[hash[count]], changelogMode=[I]): rowcount = 1.05E8, cumulative cost = {4.15E8 rows, 1.7945E10 cpu, 4.0E9 io, 2.1E9 network, 0.0 memory}
   +- Union(all=[true], union=[count, word], changelogMode=[I]): rowcount = 1.05E8, cumulative cost = {3.1E8 rows, 3.05E8 cpu, 4.0E9 io, 0.0 network, 0.0 memory}
      :- Calc(select=[count, word], where=[LIKE(word, _UTF-16LE'F%')], changelogMode=[I]): rowcount = 5000000.0, cumulative cost = {1.05E8 rows, 1.0E8 cpu, 2.0E9 io, 0.0 network, 0.0 memory}
      :  +- TableSourceScan(table=[[default_catalog, default_database, MyTable1]], fields=[count, word], changelogMode=[I]): rowcount = 1.0E8, cumulative cost = {1.0E8 rows, 1.0E8 cpu, 2.0E9 io, 0.0 network, 0.0 memory}
      +- TableSourceScan(table=[[default_catalog, default_database, MyTable2]], fields=[count, word], changelogMode=[I]): rowcount = 1.0E8, cumulative cost = {1.0E8 rows, 1.0E8 cpu, 2.0E9 io, 0.0 network, 0.0 memory}

advice[1]: [ADVICE] You might want to enable local-global two-phase optimization by configuring ('table.exec.mini-batch.enabled' to 'true', 'table.exec.mini-batch.allow-latency' to a positive long value, 'table.exec.mini-batch.size' to a positive long value).

== Optimized Execution Plan ==
GroupAggregate(groupBy=[count], select=[count, COUNT(word) AS EXPR$1])
+- Exchange(distribution=[hash[count]])
   +- Union(all=[true], union=[count, word])
      :- Calc(select=[count, word], where=[LIKE(word, 'F%')])
      :  +- TableSourceScan(table=[[default_catalog, default_database, MyTable1]], fields=[count, word])
      +- TableSourceScan(table=[[default_catalog, default_database, MyTable2]], fields=[count, word])

== Physical Execution Plan ==
{
  "nodes" : [ {
    "id" : 17,
    "type" : "Source: MyTable1[15]",
    "pact" : "Data Source",
    "contents" : "[15]:TableSourceScan(table=[[default_catalog, default_database, MyTable1]], fields=[count, word])",
    "parallelism" : 1
  }, {
    "id" : 18,
    "type" : "Calc[16]",
    "pact" : "Operator",
    "contents" : "[16]:Calc(select=[count, word], where=[LIKE(word, 'F%')])",
    "parallelism" : 1,
    "predecessors" : [ {
      "id" : 17,
      "ship_strategy" : "FORWARD",
      "side" : "second"
    } ]
  }, {
    "id" : 19,
    "type" : "Source: MyTable2[17]",
    "pact" : "Data Source",
    "contents" : "[17]:TableSourceScan(table=[[default_catalog, default_database, MyTable2]], fields=[count, word])",
    "parallelism" : 1
  }, {
    "id" : 22,
    "type" : "GroupAggregate[20]",
    "pact" : "Operator",
    "contents" : "[20]:GroupAggregate(groupBy=[count], select=[count, COUNT(word) AS EXPR$1])",
    "parallelism" : 1,
    "predecessors" : [ {
      "id" : 18,
      "ship_strategy" : "HASH",
      "side" : "second"
    }, {
      "id" : 19,
      "ship_strategy" : "HASH",
      "side" : "second"
    } ]
  } ]
}

```

`== Abstract Syntax Tree ==
LogicalAggregate(group=[{0}], EXPR$1=[COUNT($1)])
+- LogicalUnion(all=[true])
   :- LogicalProject(count=[$0], word=[$1])
   :  +- LogicalFilter(condition=[LIKE($1, _UTF-16LE'F%')])
   :     +- LogicalTableScan(table=[[default_catalog, default_database, MyTable1]])
   +- LogicalProject(count=[$0], word=[$1])
      +- LogicalTableScan(table=[[default_catalog, default_database, MyTable2]])

== Optimized Physical Plan With Advice ==
GroupAggregate(advice=[1], groupBy=[count], select=[count, COUNT(word) AS EXPR$1], changelogMode=[I,UA]): rowcount = 1.05E8, cumulative cost = {5.2E8 rows, 1.805E10 cpu, 4.0E9 io, 2.1E9 network, 0.0 memory}
+- Exchange(distribution=[hash[count]], changelogMode=[I]): rowcount = 1.05E8, cumulative cost = {4.15E8 rows, 1.7945E10 cpu, 4.0E9 io, 2.1E9 network, 0.0 memory}
   +- Union(all=[true], union=[count, word], changelogMode=[I]): rowcount = 1.05E8, cumulative cost = {3.1E8 rows, 3.05E8 cpu, 4.0E9 io, 0.0 network, 0.0 memory}
      :- Calc(select=[count, word], where=[LIKE(word, _UTF-16LE'F%')], changelogMode=[I]): rowcount = 5000000.0, cumulative cost = {1.05E8 rows, 1.0E8 cpu, 2.0E9 io, 0.0 network, 0.0 memory}
      :  +- TableSourceScan(table=[[default_catalog, default_database, MyTable1]], fields=[count, word], changelogMode=[I]): rowcount = 1.0E8, cumulative cost = {1.0E8 rows, 1.0E8 cpu, 2.0E9 io, 0.0 network, 0.0 memory}
      +- TableSourceScan(table=[[default_catalog, default_database, MyTable2]], fields=[count, word], changelogMode=[I]): rowcount = 1.0E8, cumulative cost = {1.0E8 rows, 1.0E8 cpu, 2.0E9 io, 0.0 network, 0.0 memory}

advice[1]: [ADVICE] You might want to enable local-global two-phase optimization by configuring ('table.exec.mini-batch.enabled' to 'true', 'table.exec.mini-batch.allow-latency' to a positive long value, 'table.exec.mini-batch.size' to a positive long value).

== Optimized Execution Plan ==
GroupAggregate(groupBy=[count], select=[count, COUNT(word) AS EXPR$1])
+- Exchange(distribution=[hash[count]])
   +- Union(all=[true], union=[count, word])
      :- Calc(select=[count, word], where=[LIKE(word, 'F%')])
      :  +- TableSourceScan(table=[[default_catalog, default_database, MyTable1]], fields=[count, word])
      +- TableSourceScan(table=[[default_catalog, default_database, MyTable2]], fields=[count, word])

== Physical Execution Plan ==
{
  "nodes" : [ {
    "id" : 17,
    "type" : "Source: MyTable1[15]",
    "pact" : "Data Source",
    "contents" : "[15]:TableSourceScan(table=[[default_catalog, default_database, MyTable1]], fields=[count, word])",
    "parallelism" : 1
  }, {
    "id" : 18,
    "type" : "Calc[16]",
    "pact" : "Operator",
    "contents" : "[16]:Calc(select=[count, word], where=[LIKE(word, 'F%')])",
    "parallelism" : 1,
    "predecessors" : [ {
      "id" : 17,
      "ship_strategy" : "FORWARD",
      "side" : "second"
    } ]
  }, {
    "id" : 19,
    "type" : "Source: MyTable2[17]",
    "pact" : "Data Source",
    "contents" : "[17]:TableSourceScan(table=[[default_catalog, default_database, MyTable2]], fields=[count, word])",
    "parallelism" : 1
  }, {
    "id" : 22,
    "type" : "GroupAggregate[20]",
    "pact" : "Operator",
    "contents" : "[20]:GroupAggregate(groupBy=[count], select=[count, COUNT(word) AS EXPR$1])",
    "parallelism" : 1,
    "predecessors" : [ {
      "id" : 18,
      "ship_strategy" : "HASH",
      "side" : "second"
    }, {
      "id" : 19,
      "ship_strategy" : "HASH",
      "side" : "second"
    } ]
  } ]
}
`

 Back to top


## ExplainDetails#


ExplainDetail defines the types of details for explain result.

`ExplainDetail`

ESTIMATED_COST


Specify ESTIMATED_COST will inform the optimizer to attach the estimated optimal cost of each physical rel node to the output.

`ESTIMATED_COST`

```
== Optimized Physical Plan ==
TableSourceScan(..., cumulative cost ={1.0E8 rows, 1.0E8 cpu, 2.4E9 io, 0.0 network, 0.0 memory})

```

`== Optimized Physical Plan ==
TableSourceScan(..., cumulative cost ={1.0E8 rows, 1.0E8 cpu, 2.4E9 io, 0.0 network, 0.0 memory})
`

CHANGELOG_MODE


Specify CHANGELOG_MODE will inform the optimizer to attach the changelog mode (see more details at Dynamic Tables) of each physical rel node to the ouptput.

`CHANGELOG_MODE`

```
== Optimized Physical Plan ==
GroupAggregate(..., changelogMode=[I,UA,D])

```

`== Optimized Physical Plan ==
GroupAggregate(..., changelogMode=[I,UA,D])
`

PLAN_ADVICE

PLAN_ADVICE is supported since Flink version 1.17.




> 
PLAN_ADVICE is supported since Flink version 1.17.


`PLAN_ADVICE`

Specify PLAN_ADVICE will inform the optimizer to analyze the optimized physical plan to provide the potential risk warnings and/or optimization advice.
Meanwhile, it will change the title of “Optimized Physical Plan” to “Optimized Physical Plan with Advice” as the highlight.

`PLAN_ADVICE`

Plan advice is categorized by Kind and Scope.


Flink SQL provides the plan advice targeting the following issues

* Data Skewness caused by Group Aggregation (see more details at Group Aggregation and Performance Tuning)
* Non-deterministic Updates (abbr. NDU, see more details at Determinism In Continuous Queries)

If GroupAggregate is detected and can be optimized to the local-global aggregation, the optimizer will tag advice id to the GroupAggregate rel node, and suggests users to update configurations.






SQL1
SET 'table.exec.mini-batch.enabled' = 'true';
SET 'table.exec.mini-batch.allow-latency' = '5s';
SET 'table.exec.mini-batch.size' = '200';
SET 'table.optimizer.agg-phase-strategy' = 'ONE_PHASE';

CREATE TABLE MyTable (
  a BIGINT,
  b INT NOT NULL,
  c VARCHAR,
  d BIGINT
) WITH (
  'connector' = 'values',
  'bounded' = 'false');

EXPLAIN PLAN_ADVICE
SELECT
  AVG(a) AS avg_a,
  COUNT(*) AS cnt,
  COUNT(b) AS cnt_b,
  MIN(b) AS min_b,
  MAX(c) FILTER (WHERE a > 1) AS max_c
FROM MyTable;

NODE_LEVEL ADVICE
== Optimized Physical Plan With Advice ==
Calc(select=[avg_a, cnt, cnt AS cnt_b, min_b, max_c])
+- GroupAggregate(advice=[1], select=[AVG(a) AS avg_a, COUNT(*) AS cnt, MIN(b) AS min_b, MAX(c) FILTER $f3 AS max_c])
   +- Exchange(distribution=[single])
      +- Calc(select=[a, b, c, IS TRUE(>(a, 1)) AS $f3])
         +- MiniBatchAssigner(interval=[10000ms], mode=[ProcTime])
            +- TableSourceScan(table=[[default_catalog, default_database, MyTable, project=[a, b, c], metadata=[]]], fields=[a, b, c])

advice[1]: [ADVICE] You might want to enable local-global two-phase optimization by configuring ('table.optimizer.agg-phase-strategy' to 'AUTO').



`GroupAggregate`
`GroupAggregate`

```
SET 'table.exec.mini-batch.enabled' = 'true';
SET 'table.exec.mini-batch.allow-latency' = '5s';
SET 'table.exec.mini-batch.size' = '200';
SET 'table.optimizer.agg-phase-strategy' = 'ONE_PHASE';

CREATE TABLE MyTable (
  a BIGINT,
  b INT NOT NULL,
  c VARCHAR,
  d BIGINT
) WITH (
  'connector' = 'values',
  'bounded' = 'false');

EXPLAIN PLAN_ADVICE
SELECT
  AVG(a) AS avg_a,
  COUNT(*) AS cnt,
  COUNT(b) AS cnt_b,
  MIN(b) AS min_b,
  MAX(c) FILTER (WHERE a > 1) AS max_c
FROM MyTable;

```

`SET 'table.exec.mini-batch.enabled' = 'true';
SET 'table.exec.mini-batch.allow-latency' = '5s';
SET 'table.exec.mini-batch.size' = '200';
SET 'table.optimizer.agg-phase-strategy' = 'ONE_PHASE';

CREATE TABLE MyTable (
  a BIGINT,
  b INT NOT NULL,
  c VARCHAR,
  d BIGINT
) WITH (
  'connector' = 'values',
  'bounded' = 'false');

EXPLAIN PLAN_ADVICE
SELECT
  AVG(a) AS avg_a,
  COUNT(*) AS cnt,
  COUNT(b) AS cnt_b,
  MIN(b) AS min_b,
  MAX(c) FILTER (WHERE a > 1) AS max_c
FROM MyTable;
`

```
== Optimized Physical Plan With Advice ==
Calc(select=[avg_a, cnt, cnt AS cnt_b, min_b, max_c])
+- GroupAggregate(advice=[1], select=[AVG(a) AS avg_a, COUNT(*) AS cnt, MIN(b) AS min_b, MAX(c) FILTER $f3 AS max_c])
   +- Exchange(distribution=[single])
      +- Calc(select=[a, b, c, IS TRUE(>(a, 1)) AS $f3])
         +- MiniBatchAssigner(interval=[10000ms], mode=[ProcTime])
            +- TableSourceScan(table=[[default_catalog, default_database, MyTable, project=[a, b, c], metadata=[]]], fields=[a, b, c])

advice[1]: [ADVICE] You might want to enable local-global two-phase optimization by configuring ('table.optimizer.agg-phase-strategy' to 'AUTO').

```

`== Optimized Physical Plan With Advice ==
Calc(select=[avg_a, cnt, cnt AS cnt_b, min_b, max_c])
+- GroupAggregate(advice=[1], select=[AVG(a) AS avg_a, COUNT(*) AS cnt, MIN(b) AS min_b, MAX(c) FILTER $f3 AS max_c])
   +- Exchange(distribution=[single])
      +- Calc(select=[a, b, c, IS TRUE(>(a, 1)) AS $f3])
         +- MiniBatchAssigner(interval=[10000ms], mode=[ProcTime])
            +- TableSourceScan(table=[[default_catalog, default_database, MyTable, project=[a, b, c], metadata=[]]], fields=[a, b, c])

advice[1]: [ADVICE] You might want to enable local-global two-phase optimization by configuring ('table.optimizer.agg-phase-strategy' to 'AUTO').
`

If NDU issue is detected, the optimizer will append the warning at the end of the physical plan.






SQL2
CREATE TABLE MyTable (
  a INT,
  b BIGINT,
  c STRING,
  d INT,
  `day` AS DATE_FORMAT(CURRENT_TIMESTAMP, 'yyMMdd'),
  PRIMARY KEY (a, c) NOT ENFORCED
) WITH (
  'connector' = 'values',
  'changelog-mode' = 'I,UA,UB,D'  
);

CREATE TABLE MySink (
 a INT,
 b BIGINT,
 c STRING,
 PRIMARY KEY (a) NOT ENFORCED
) WITH (
 'connector' = 'values',
 'sink-insert-only' = 'false'
);

EXPLAIN PLAN_ADVICE
INSERT INTO MySink
SELECT a, b, `day`
FROM MyTable
WHERE b > 100;

QUERY_LEVEL WARNING
== Optimized Physical Plan With Advice ==
Sink(table=[default_catalog.default_database.MySink], fields=[a, b, day], upsertMaterialize=[true])
+- Calc(select=[a, b, DATE_FORMAT(CURRENT_TIMESTAMP(), 'yyMMdd') AS day], where=[>(b, 100)])
   +- TableSourceScan(table=[[default_catalog, default_database, MyTable, filter=[], project=[a, b], metadata=[]]], fields=[a, b])

advice[1]: [WARNING] The column(s): day(generated by non-deterministic function: CURRENT_TIMESTAMP ) can not satisfy the determinism requirement for correctly processing update message('UB'/'UA'/'D' in changelogMode, not 'I' only), this usually happens when input node has no upsertKey(upsertKeys=[{}]) or current node outputs non-deterministic update messages. Please consider removing these non-deterministic columns or making them deterministic by using deterministic functions.

related rel plan:
Calc(select=[a, b, DATE_FORMAT(CURRENT_TIMESTAMP(), _UTF-16LE'yyMMdd') AS day], where=[>(b, 100)], changelogMode=[I,UB,UA,D])
+- TableSourceScan(table=[[default_catalog, default_database, MyTable, filter=[], project=[a, b], metadata=[]]], fields=[a, b], changelogMode=[I,UB,UA,D])




```
CREATE TABLE MyTable (
  a INT,
  b BIGINT,
  c STRING,
  d INT,
  `day` AS DATE_FORMAT(CURRENT_TIMESTAMP, 'yyMMdd'),
  PRIMARY KEY (a, c) NOT ENFORCED
) WITH (
  'connector' = 'values',
  'changelog-mode' = 'I,UA,UB,D'  
);

CREATE TABLE MySink (
 a INT,
 b BIGINT,
 c STRING,
 PRIMARY KEY (a) NOT ENFORCED
) WITH (
 'connector' = 'values',
 'sink-insert-only' = 'false'
);

EXPLAIN PLAN_ADVICE
INSERT INTO MySink
SELECT a, b, `day`
FROM MyTable
WHERE b > 100;

```

`CREATE TABLE MyTable (
  a INT,
  b BIGINT,
  c STRING,
  d INT,
  `day` AS DATE_FORMAT(CURRENT_TIMESTAMP, 'yyMMdd'),
  PRIMARY KEY (a, c) NOT ENFORCED
) WITH (
  'connector' = 'values',
  'changelog-mode' = 'I,UA,UB,D'  
);

CREATE TABLE MySink (
 a INT,
 b BIGINT,
 c STRING,
 PRIMARY KEY (a) NOT ENFORCED
) WITH (
 'connector' = 'values',
 'sink-insert-only' = 'false'
);

EXPLAIN PLAN_ADVICE
INSERT INTO MySink
SELECT a, b, `day`
FROM MyTable
WHERE b > 100;
`

```
== Optimized Physical Plan With Advice ==
Sink(table=[default_catalog.default_database.MySink], fields=[a, b, day], upsertMaterialize=[true])
+- Calc(select=[a, b, DATE_FORMAT(CURRENT_TIMESTAMP(), 'yyMMdd') AS day], where=[>(b, 100)])
   +- TableSourceScan(table=[[default_catalog, default_database, MyTable, filter=[], project=[a, b], metadata=[]]], fields=[a, b])

advice[1]: [WARNING] The column(s): day(generated by non-deterministic function: CURRENT_TIMESTAMP ) can not satisfy the determinism requirement for correctly processing update message('UB'/'UA'/'D' in changelogMode, not 'I' only), this usually happens when input node has no upsertKey(upsertKeys=[{}]) or current node outputs non-deterministic update messages. Please consider removing these non-deterministic columns or making them deterministic by using deterministic functions.

related rel plan:
Calc(select=[a, b, DATE_FORMAT(CURRENT_TIMESTAMP(), _UTF-16LE'yyMMdd') AS day], where=[>(b, 100)], changelogMode=[I,UB,UA,D])
+- TableSourceScan(table=[[default_catalog, default_database, MyTable, filter=[], project=[a, b], metadata=[]]], fields=[a, b], changelogMode=[I,UB,UA,D])

```

`== Optimized Physical Plan With Advice ==
Sink(table=[default_catalog.default_database.MySink], fields=[a, b, day], upsertMaterialize=[true])
+- Calc(select=[a, b, DATE_FORMAT(CURRENT_TIMESTAMP(), 'yyMMdd') AS day], where=[>(b, 100)])
   +- TableSourceScan(table=[[default_catalog, default_database, MyTable, filter=[], project=[a, b], metadata=[]]], fields=[a, b])

advice[1]: [WARNING] The column(s): day(generated by non-deterministic function: CURRENT_TIMESTAMP ) can not satisfy the determinism requirement for correctly processing update message('UB'/'UA'/'D' in changelogMode, not 'I' only), this usually happens when input node has no upsertKey(upsertKeys=[{}]) or current node outputs non-deterministic update messages. Please consider removing these non-deterministic columns or making them deterministic by using deterministic functions.

related rel plan:
Calc(select=[a, b, DATE_FORMAT(CURRENT_TIMESTAMP(), _UTF-16LE'yyMMdd') AS day], where=[>(b, 100)], changelogMode=[I,UB,UA,D])
+- TableSourceScan(table=[[default_catalog, default_database, MyTable, filter=[], project=[a, b], metadata=[]]], fields=[a, b], changelogMode=[I,UB,UA,D])
`

If no warning or advice is detected, the optimizer will append a notice that “No available advice” at the end of the physical plan.






SQL3
CREATE TABLE MyTable (
  a INT,
  b BIGINT,
  c STRING,
  d INT
) WITH (
  'connector' = 'values',
  'changelog-mode' = 'I'  
);

EXPLAIN PLAN_ADVICE
SELECT * FROM MyTable WHERE b > 100;

NO_AVAILABLE ADVICE
== Optimized Physical Plan With Advice ==
Calc(select=[a, b, c, d], where=[>(b, 100)])
+- TableSourceScan(table=[[default_catalog, default_database, MyTable]], fields=[a, b, c, d])

No available advice...




```
CREATE TABLE MyTable (
  a INT,
  b BIGINT,
  c STRING,
  d INT
) WITH (
  'connector' = 'values',
  'changelog-mode' = 'I'  
);

EXPLAIN PLAN_ADVICE
SELECT * FROM MyTable WHERE b > 100;

```

`CREATE TABLE MyTable (
  a INT,
  b BIGINT,
  c STRING,
  d INT
) WITH (
  'connector' = 'values',
  'changelog-mode' = 'I'  
);

EXPLAIN PLAN_ADVICE
SELECT * FROM MyTable WHERE b > 100;
`

```
== Optimized Physical Plan With Advice ==
Calc(select=[a, b, c, d], where=[>(b, 100)])
+- TableSourceScan(table=[[default_catalog, default_database, MyTable]], fields=[a, b, c, d])

No available advice...

```

`== Optimized Physical Plan With Advice ==
Calc(select=[a, b, c, d], where=[>(b, 100)])
+- TableSourceScan(table=[[default_catalog, default_database, MyTable]], fields=[a, b, c, d])

No available advice...
`

JSON_EXECUTION_PLAN


Specify JSON_EXECUTION_PLAN will inform the optimizer to attach the json-format execution plan of the program to the output.

`JSON_EXECUTION_PLAN`

 Back to top


## Syntax#


```
EXPLAIN [([ExplainDetail[, ExplainDetail]*]) | PLAN FOR] <query_statement_or_insert_statement_or_statement_set>

statement_set:
STATEMENT SET
BEGIN
insert_statement;
...
insert_statement;
END;

```

`EXPLAIN [([ExplainDetail[, ExplainDetail]*]) | PLAN FOR] <query_statement_or_insert_statement_or_statement_set>

statement_set:
STATEMENT SET
BEGIN
insert_statement;
...
insert_statement;
END;
`

For query syntax, please refer to Queries page.
For insert syntax, please refer to INSERT page.
