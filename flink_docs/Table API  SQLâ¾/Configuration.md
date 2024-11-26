# Configuration


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Configuration#


By default, the Table & SQL API is preconfigured for producing accurate results with acceptable
performance.


Depending on the requirements of a table program, it might be necessary to adjust
certain parameters for optimization. For example, unbounded streaming programs may need to ensure
that the required state size is capped (see streaming concepts).


### Overview#


When instantiating a TableEnvironment, EnvironmentSettings can be used to pass the desired
configuration for the current session, by passing a Configuration object to the
EnvironmentSettings.

`TableEnvironment`
`EnvironmentSettings`
`Configuration`
`EnvironmentSettings`

Additionally, in every table environment, the TableConfig offers options for configuring the
current session.

`TableConfig`

For common or important configuration options, the TableConfig provides getters and setters methods
with detailed inline documentation.

`TableConfig`

For more advanced configuration, users can directly access the underlying key-value map. The following
sections list all available options that can be used to adjust Flink Table & SQL API programs.


Attention Because options are read at different point in time
when performing operations, it is recommended to set configuration options early after instantiating a
table environment.


```
// instantiate table environment
Configuration configuration = new Configuration();
// set low-level key-value options
configuration.setString("table.exec.mini-batch.enabled", "true");
configuration.setString("table.exec.mini-batch.allow-latency", "5 s");
configuration.setString("table.exec.mini-batch.size", "5000");
EnvironmentSettings settings = EnvironmentSettings.newInstance()
        .inStreamingMode().withConfiguration(configuration).build();
TableEnvironment tEnv = TableEnvironment.create(settings);

// access flink configuration after table environment instantiation
TableConfig tableConfig = tEnv.getConfig();
// set low-level key-value options
tableConfig.set("table.exec.mini-batch.enabled", "true");
tableConfig.set("table.exec.mini-batch.allow-latency", "5 s");
tableConfig.set("table.exec.mini-batch.size", "5000");

```

`// instantiate table environment
Configuration configuration = new Configuration();
// set low-level key-value options
configuration.setString("table.exec.mini-batch.enabled", "true");
configuration.setString("table.exec.mini-batch.allow-latency", "5 s");
configuration.setString("table.exec.mini-batch.size", "5000");
EnvironmentSettings settings = EnvironmentSettings.newInstance()
        .inStreamingMode().withConfiguration(configuration).build();
TableEnvironment tEnv = TableEnvironment.create(settings);

// access flink configuration after table environment instantiation
TableConfig tableConfig = tEnv.getConfig();
// set low-level key-value options
tableConfig.set("table.exec.mini-batch.enabled", "true");
tableConfig.set("table.exec.mini-batch.allow-latency", "5 s");
tableConfig.set("table.exec.mini-batch.size", "5000");
`

```
// instantiate table environment
val configuration = new Configuration;
// set low-level key-value options
configuration.setString("table.exec.mini-batch.enabled", "true")
configuration.setString("table.exec.mini-batch.allow-latency", "5 s")
configuration.setString("table.exec.mini-batch.size", "5000")
val settings = EnvironmentSettings.newInstance
  .inStreamingMode.withConfiguration(configuration).build
val tEnv: TableEnvironment = TableEnvironment.create(settings)

// access flink configuration after table environment instantiation
val tableConfig = tEnv.getConfig()
// set low-level key-value options
tableConfig.set("table.exec.mini-batch.enabled", "true")
tableConfig.set("table.exec.mini-batch.allow-latency", "5 s")
tableConfig.set("table.exec.mini-batch.size", "5000")

```

`// instantiate table environment
val configuration = new Configuration;
// set low-level key-value options
configuration.setString("table.exec.mini-batch.enabled", "true")
configuration.setString("table.exec.mini-batch.allow-latency", "5 s")
configuration.setString("table.exec.mini-batch.size", "5000")
val settings = EnvironmentSettings.newInstance
  .inStreamingMode.withConfiguration(configuration).build
val tEnv: TableEnvironment = TableEnvironment.create(settings)

// access flink configuration after table environment instantiation
val tableConfig = tEnv.getConfig()
// set low-level key-value options
tableConfig.set("table.exec.mini-batch.enabled", "true")
tableConfig.set("table.exec.mini-batch.allow-latency", "5 s")
tableConfig.set("table.exec.mini-batch.size", "5000")
`

```
# instantiate table environment
configuration = Configuration()
configuration.set("table.exec.mini-batch.enabled", "true")
configuration.set("table.exec.mini-batch.allow-latency", "5 s")
configuration.set("table.exec.mini-batch.size", "5000")
settings = EnvironmentSettings.new_instance() \
...     .in_streaming_mode() \
...     .with_configuration(configuration) \
...     .build()

t_env = TableEnvironment.create(settings)

# access flink configuration after table environment instantiation
table_config = t_env.get_config()
# set low-level key-value options
table_config.set("table.exec.mini-batch.enabled", "true")
table_config.set("table.exec.mini-batch.allow-latency", "5 s")
table_config.set("table.exec.mini-batch.size", "5000")

```

`# instantiate table environment
configuration = Configuration()
configuration.set("table.exec.mini-batch.enabled", "true")
configuration.set("table.exec.mini-batch.allow-latency", "5 s")
configuration.set("table.exec.mini-batch.size", "5000")
settings = EnvironmentSettings.new_instance() \
...     .in_streaming_mode() \
...     .with_configuration(configuration) \
...     .build()

t_env = TableEnvironment.create(settings)

# access flink configuration after table environment instantiation
table_config = t_env.get_config()
# set low-level key-value options
table_config.set("table.exec.mini-batch.enabled", "true")
table_config.set("table.exec.mini-batch.allow-latency", "5 s")
table_config.set("table.exec.mini-batch.size", "5000")
`

```
Flink SQL> SET 'table.exec.mini-batch.enabled' = 'true';
Flink SQL> SET 'table.exec.mini-batch.allow-latency' = '5s';
Flink SQL> SET 'table.exec.mini-batch.size' = '5000';

```

`Flink SQL> SET 'table.exec.mini-batch.enabled' = 'true';
Flink SQL> SET 'table.exec.mini-batch.allow-latency' = '5s';
Flink SQL> SET 'table.exec.mini-batch.size' = '5000';
`

> 
Note: All of the following configuration options can also be set globally in
Flink configuration file and can be later
on overridden in the application, through EnvironmentSettings, before instantiating
the TableEnvironment, or through the TableConfig of the TableEnvironment.


`EnvironmentSettings`
`TableEnvironment`
`TableConfig`
`TableEnvironment`

### Execution Options#


The following options can be used to tune the performance of the query execution.


##### table.exec.async-lookup.buffer-capacity


##### table.exec.async-lookup.output-mode


Enum

* "ORDERED"
* "ALLOW_UNORDERED"

##### table.exec.async-lookup.timeout


##### table.exec.async-scalar.buffer-capacity


##### table.exec.async-scalar.max-attempts


##### table.exec.async-scalar.retry-delay


##### table.exec.async-scalar.retry-strategy


Enum

* "NO_RETRY"
* "FIXED_DELAY"

##### table.exec.async-scalar.timeout


##### table.exec.async-state.enabled


##### table.exec.deduplicate.insert-update-after-sensitive-enabled


##### table.exec.deduplicate.mini-batch.compact-changes-enabled


##### table.exec.disabled-operators


##### table.exec.interval-join.min-cleanup-interval


##### table.exec.legacy-cast-behaviour


Enum

* "ENABLED": CAST will operate following the legacy behaviour.
* "DISABLED": CAST will operate following the new correct behaviour.

##### table.exec.local-hash-agg.adaptive.distinct-value-rate-threshold


##### table.exec.local-hash-agg.adaptive.enabled


##### table.exec.local-hash-agg.adaptive.sampling-threshold


##### table.exec.mini-batch.allow-latency


##### table.exec.mini-batch.enabled


##### table.exec.mini-batch.size


##### table.exec.operator-fusion-codegen.enabled


##### table.exec.rank.topn-cache-size


##### table.exec.resource.default-parallelism


##### table.exec.simplify-operator-name-enabled


##### table.exec.sink.keyed-shuffle


Enum

* "NONE"
* "AUTO"
* "FORCE"

##### table.exec.sink.not-null-enforcer


Enum

* "ERROR": Throw a runtime exception when writing null values into NOT NULL column.
* "DROP": Drop records silently if a null value would have to be inserted into a NOT NULL column.

##### table.exec.sink.rowtime-inserter


Enum

* "ENABLED": Insert a rowtime attribute (if available) into the underlying stream record. This requires at most one time attribute in the input for the sink.
* "DISABLED": Do not insert the rowtime attribute into the underlying stream record.

##### table.exec.sink.type-length-enforcer


Enum

* "IGNORE": Don't apply any trimming and padding, and instead ignore the CHAR/VARCHAR/BINARY/VARBINARY length directive.
* "TRIM_PAD": Trim and pad string and binary values to match the length defined by the CHAR/VARCHAR/BINARY/VARBINARY length.

##### table.exec.sink.upsert-materialize


Enum

* "NONE"
* "AUTO"
* "FORCE"

##### table.exec.sort.async-merge-enabled


##### table.exec.sort.default-limit


##### table.exec.sort.max-num-file-handles


##### table.exec.source.cdc-events-duplicate


##### table.exec.source.idle-timeout


##### table.exec.spill-compression.block-size


##### table.exec.spill-compression.enabled


##### table.exec.state.ttl


##### table.exec.uid.format


##### table.exec.uid.generation


Enum

* "PLAN_ONLY": Sets UIDs on streaming transformations if and only if the pipeline definition comes from a compiled plan. Pipelines that have been constructed in the API without a compilation step will not set an explicit UID as it might not be stable across multiple translations.
* "ALWAYS": Always sets UIDs on streaming transformations. This strategy is for experts only! Pipelines that have been constructed in the API without a compilation step might not be able to be restored properly. The UID generation depends on previously declared pipelines (potentially across jobs if the same JVM is used). Thus, a stable environment must be ensured. Pipeline definitions that come from a compiled plan are safe to use.
* "DISABLED": No explicit UIDs will be set.

##### table.exec.window-agg.buffer-size-limit


### Optimizer Options#


The following options can be used to adjust the behavior of the query optimizer to get a better execution plan.


##### table.optimizer.agg-phase-strategy


Enum

* "AUTO"
* "ONE_PHASE"
* "TWO_PHASE"

##### table.optimizer.bushy-join-reorder-threshold


##### table.optimizer.distinct-agg.split.bucket-num


##### table.optimizer.distinct-agg.split.enabled


##### table.optimizer.dynamic-filtering.enabled


##### table.optimizer.incremental-agg-enabled


##### table.optimizer.join-reorder-enabled


##### table.optimizer.join.broadcast-threshold


##### table.optimizer.multiple-input-enabled


##### table.optimizer.non-deterministic-update.strategy


Enum

* "TRY_RESOLVE"
* "IGNORE"

##### table.optimizer.reuse-optimize-block-with-digest-enabled


##### table.optimizer.reuse-source-enabled


##### table.optimizer.reuse-sub-plan-enabled


##### table.optimizer.runtime-filter.enabled


##### table.optimizer.runtime-filter.max-build-data-size


##### table.optimizer.runtime-filter.min-filter-ratio


##### table.optimizer.runtime-filter.min-probe-data-size

`table.optimizer.runtime-filter.max-build-data-size`

##### table.optimizer.source.report-statistics-enabled


##### table.optimizer.sql2rel.project-merge.enabled


##### table.optimizer.union-all-as-breakpoint-enabled


### Table Options#


The following options can be used to adjust the behavior of the table planner.


##### table.builtin-catalog-name


##### table.builtin-database-name


##### table.catalog-modification.listeners


##### table.column-expansion-strategy


List<Enum>

* "EXCLUDE_ALIASED_VIRTUAL_METADATA_COLUMNS": Excludes virtual metadata columns that reference a metadata key via an alias. For example, a column declared as 'c METADATA VIRTUAL FROM k' is not selected by default if the strategy is applied.
* "EXCLUDE_DEFAULT_VIRTUAL_METADATA_COLUMNS": Excludes virtual metadata columns that directly reference a metadata key. For example, a column declared as 'k METADATA VIRTUAL' is not selected by default if the strategy is applied.

##### table.display.max-column-width


##### table.dml-sync


##### table.dynamic-table-options.enabled


##### table.generated-code.max-length


##### table.local-time-zone


##### table.plan.compile.catalog-objects


Enum

* "ALL": All metadata about catalog tables, functions, or data types will be persisted into the plan during compilation. For catalog tables, this includes the table's identifier, schema, and options. For catalog functions, this includes the function's identifier and class. For catalog data types, this includes the identifier and entire type structure. With this strategy, the catalog's metadata doesn't have to be available anymore during a restore operation.
* "SCHEMA": In addition to an identifier, schema information about catalog tables, functions, or data types will be persisted into the plan during compilation. A schema allows for detecting incompatible changes in the catalog during a plan restore operation. However, all other metadata will still be retrieved from the catalog.
* "IDENTIFIER": Only the identifier of catalog tables, functions, or data types will be persisted into the plan during compilation. All metadata will be retrieved from the catalog during a restore operation. With this strategy, plans become less verbose.

##### table.plan.force-recompile


##### table.plan.restore.catalog-objects


Enum

* "ALL": Reads all metadata about catalog tables, functions, or data types that has been persisted in the plan. The strategy performs a catalog lookup by identifier to fill in missing information or enrich mutable options. If the original object is not available in the catalog anymore, pipelines can still be restored if all information necessary is contained in the plan.
* "ALL_ENFORCED": Requires that all metadata about catalog tables, functions, or data types has been persisted in the plan. The strategy will neither perform a catalog lookup by identifier nor enrich mutable options with catalog information. A restore will fail if not all information necessary is contained in the plan.
* "IDENTIFIER": Uses only the identifier of catalog tables, functions, or data types and always performs a catalog lookup. A restore will fail if the original object is not available in the catalog anymore. Additional metadata that might be contained in the plan will be ignored.

##### table.resources.download-dir


##### table.rtas-ctas.atomicity-enabled


##### table.sql-dialect


### Materialized Table Options#


The following options can be used to adjust the behavior of the materialized table.


##### materialized-table.refresh-mode.freshness-threshold


##### partition.fields.#.date-formatter


### SQL Client Options#


The following options can be used to adjust the behavior of the sql client.


##### sql-client.display.color-schema


##### sql-client.display.print-time-cost


##### sql-client.display.show-line-numbers


##### sql-client.execution.max-table-result.rows


##### sql-client.execution.result-mode


Enum

* "TABLE": Materializes results in memory and visualizes them in a regular, paginated table representation.
* "CHANGELOG": Visualizes the result stream that is produced by a continuous query.
* "TABLEAU": Display results in the screen directly in a tableau format.

##### sql-client.verbose
