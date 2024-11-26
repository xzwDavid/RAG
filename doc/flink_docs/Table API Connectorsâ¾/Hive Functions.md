# Hive Functions


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Hive Functions#


## Use Hive Built-in Functions via HiveModule#


The HiveModule provides Hive built-in functions as Flink system (built-in) functions to Flink SQL and Table API users.

`HiveModule`

For detailed information, please refer to HiveModule.


```

String name            = "myhive";
String version         = "2.3.4";

tableEnv.loadModue(name, new HiveModule(version));

```

`
String name            = "myhive";
String version         = "2.3.4";

tableEnv.loadModue(name, new HiveModule(version));
`

```

val name            = "myhive"
val version         = "2.3.4"

tableEnv.loadModue(name, new HiveModule(version));

```

`
val name            = "myhive"
val version         = "2.3.4"

tableEnv.loadModue(name, new HiveModule(version));
`

```
from pyflink.table.module import HiveModule

name = "myhive"
version = "2.3.4"

t_env.load_module(name, HiveModule(version))

```

`from pyflink.table.module import HiveModule

name = "myhive"
version = "2.3.4"

t_env.load_module(name, HiveModule(version))
`

```
LOAD MODULE hive WITH ('hive-version' = '2.3.4');

```

`LOAD MODULE hive WITH ('hive-version' = '2.3.4');
`

> 
  Some Hive built-in functions in older versions have thread safety issues.
We recommend users patch their own Hive to fix them.



## Use Native Hive Aggregate Functions#


If HiveModule is loaded with a higher priority than CoreModule, Flink will try to use the Hive built-in function first. And then for Hive built-in aggregation functions,
Flink can only use the sort-based aggregation operator now. From Flink 1.17, we have introduced some native hive aggregation functions, which can be executed using the hash-based aggregation operator.
Currently, only five functions are supported, namely sum/count/avg/min/max, and more aggregation functions will be supported in the future. Users can use the native aggregation function by turning on
the option table.exec.hive.native-agg-function.enabled, which brings significant performance improvement to the job.

`table.exec.hive.native-agg-function.enabled`

##### table.exec.hive.native-agg-function.enabled


Attention The ability of the native aggregation functions doesn’t fully align with Hive built-in aggregation functions now, for example, some data types are not supported. If performance is not a bottleneck, you don’t need to turn on this option.
In addition, table.exec.hive.native-agg-function.enabled option can’t be turned on per job when using it via SqlClient, currently, only the module level is supported. Users should turn on this option first and then load HiveModule. This issue will be fixed in the future.

`table.exec.hive.native-agg-function.enabled`

## Hive User Defined Functions#


Users can use their existing Hive User Defined Functions in Flink.


Supported UDF types include:

* UDF
* GenericUDF
* GenericUDTF
* UDAF
* GenericUDAFResolver2

Upon query planning and execution, Hive’s UDF and GenericUDF are automatically translated into Flink’s ScalarFunction,
Hive’s GenericUDTF is automatically translated into Flink’s TableFunction,
and Hive’s UDAF and GenericUDAFResolver2 are translated into Flink’s AggregateFunction.


To use a Hive User Defined Function, user have to

* set a HiveCatalog backed by Hive Metastore that contains that function as current catalog of the session
* include a jar that contains that function in Flink’s classpath

## Using Hive User Defined Functions#


Assuming we have the following Hive functions registered in Hive Metastore:


```
/**
 * Test simple udf. Registered under name 'myudf'
 */
public class TestHiveSimpleUDF extends UDF {

	public IntWritable evaluate(IntWritable i) {
		return new IntWritable(i.get());
	}

	public Text evaluate(Text text) {
		return new Text(text.toString());
	}
}

/**
 * Test generic udf. Registered under name 'mygenericudf'
 */
public class TestHiveGenericUDF extends GenericUDF {

	@Override
	public ObjectInspector initialize(ObjectInspector[] arguments) throws UDFArgumentException {
		checkArgument(arguments.length == 2);

		checkArgument(arguments[1] instanceof ConstantObjectInspector);
		Object constant = ((ConstantObjectInspector) arguments[1]).getWritableConstantValue();
		checkArgument(constant instanceof IntWritable);
		checkArgument(((IntWritable) constant).get() == 1);

		if (arguments[0] instanceof IntObjectInspector ||
				arguments[0] instanceof StringObjectInspector) {
			return arguments[0];
		} else {
			throw new RuntimeException("Not support argument: " + arguments[0]);
		}
	}

	@Override
	public Object evaluate(DeferredObject[] arguments) throws HiveException {
		return arguments[0].get();
	}

	@Override
	public String getDisplayString(String[] children) {
		return "TestHiveGenericUDF";
	}
}

/**
 * Test split udtf. Registered under name 'mygenericudtf'
 */
public class TestHiveUDTF extends GenericUDTF {

	@Override
	public StructObjectInspector initialize(ObjectInspector[] argOIs) throws UDFArgumentException {
		checkArgument(argOIs.length == 2);

		// TEST for constant arguments
		checkArgument(argOIs[1] instanceof ConstantObjectInspector);
		Object constant = ((ConstantObjectInspector) argOIs[1]).getWritableConstantValue();
		checkArgument(constant instanceof IntWritable);
		checkArgument(((IntWritable) constant).get() == 1);

		return ObjectInspectorFactory.getStandardStructObjectInspector(
			Collections.singletonList("col1"),
			Collections.singletonList(PrimitiveObjectInspectorFactory.javaStringObjectInspector));
	}

	@Override
	public void process(Object[] args) throws HiveException {
		String str = (String) args[0];
		for (String s : str.split(",")) {
			forward(s);
			forward(s);
		}
	}

	@Override
	public void close() {
	}
}

```

`/**
 * Test simple udf. Registered under name 'myudf'
 */
public class TestHiveSimpleUDF extends UDF {

	public IntWritable evaluate(IntWritable i) {
		return new IntWritable(i.get());
	}

	public Text evaluate(Text text) {
		return new Text(text.toString());
	}
}

/**
 * Test generic udf. Registered under name 'mygenericudf'
 */
public class TestHiveGenericUDF extends GenericUDF {

	@Override
	public ObjectInspector initialize(ObjectInspector[] arguments) throws UDFArgumentException {
		checkArgument(arguments.length == 2);

		checkArgument(arguments[1] instanceof ConstantObjectInspector);
		Object constant = ((ConstantObjectInspector) arguments[1]).getWritableConstantValue();
		checkArgument(constant instanceof IntWritable);
		checkArgument(((IntWritable) constant).get() == 1);

		if (arguments[0] instanceof IntObjectInspector ||
				arguments[0] instanceof StringObjectInspector) {
			return arguments[0];
		} else {
			throw new RuntimeException("Not support argument: " + arguments[0]);
		}
	}

	@Override
	public Object evaluate(DeferredObject[] arguments) throws HiveException {
		return arguments[0].get();
	}

	@Override
	public String getDisplayString(String[] children) {
		return "TestHiveGenericUDF";
	}
}

/**
 * Test split udtf. Registered under name 'mygenericudtf'
 */
public class TestHiveUDTF extends GenericUDTF {

	@Override
	public StructObjectInspector initialize(ObjectInspector[] argOIs) throws UDFArgumentException {
		checkArgument(argOIs.length == 2);

		// TEST for constant arguments
		checkArgument(argOIs[1] instanceof ConstantObjectInspector);
		Object constant = ((ConstantObjectInspector) argOIs[1]).getWritableConstantValue();
		checkArgument(constant instanceof IntWritable);
		checkArgument(((IntWritable) constant).get() == 1);

		return ObjectInspectorFactory.getStandardStructObjectInspector(
			Collections.singletonList("col1"),
			Collections.singletonList(PrimitiveObjectInspectorFactory.javaStringObjectInspector));
	}

	@Override
	public void process(Object[] args) throws HiveException {
		String str = (String) args[0];
		for (String s : str.split(",")) {
			forward(s);
			forward(s);
		}
	}

	@Override
	public void close() {
	}
}
`

From Hive CLI, we can see they are registered:


```
hive> show functions;
OK
......
mygenericudf
myudf
myudtf

```

`hive> show functions;
OK
......
mygenericudf
myudf
myudtf
`

Then, users can use them in SQL as:


```

Flink SQL> select mygenericudf(myudf(name), 1) as a, mygenericudf(myudf(age), 1) as b, s from mysourcetable, lateral table(myudtf(name, 1)) as T(s);

```

`
Flink SQL> select mygenericudf(myudf(name), 1) as a, mygenericudf(myudf(age), 1) as b, s from mysourcetable, lateral table(myudtf(name, 1)) as T(s);
`