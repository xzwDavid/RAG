# Overview


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Operators#


Operators transform one or more DataStreams into a new DataStream. Programs can combine multiple transformations into
sophisticated dataflow topologies.


## DataStream Transformations#


DataStream programs in Flink are regular programs that implement transformations on data streams (e.g., mapping,
filtering, reducing). Please see operators
for an overview of the available transformations in Python DataStream API.


## Functions#


Transformations accept user-defined functions as input to define the functionality of the transformations.
The following section describes different ways of defining Python user-defined functions in Python DataStream API.


### Implementing Function Interfaces#


Different Function interfaces are provided for different transformations in the Python DataStream API. For example,
MapFunction is provided for the map transformation, FilterFunction is provided for the filter transformation, etc.
Users can implement the corresponding Function interface according to the type of the transformation. Take MapFunction for
instance:

`MapFunction`
`map`
`FilterFunction`
`filter`

```
# Implementing MapFunction
class MyMapFunction(MapFunction):
    
    def map(self, value):
        return value + 1
        
data_stream = env.from_collection([1, 2, 3, 4, 5], type_info=Types.INT())
mapped_stream = data_stream.map(MyMapFunction(), output_type=Types.INT())

```

`# Implementing MapFunction
class MyMapFunction(MapFunction):
    
    def map(self, value):
        return value + 1
        
data_stream = env.from_collection([1, 2, 3, 4, 5], type_info=Types.INT())
mapped_stream = data_stream.map(MyMapFunction(), output_type=Types.INT())
`

### Lambda Function#


As shown in the following example, the transformations can also accept a lambda function to define the functionality of the transformation:


```
data_stream = env.from_collection([1, 2, 3, 4, 5], type_info=Types.INT())
mapped_stream = data_stream.map(lambda x: x + 1, output_type=Types.INT())

```

`data_stream = env.from_collection([1, 2, 3, 4, 5], type_info=Types.INT())
mapped_stream = data_stream.map(lambda x: x + 1, output_type=Types.INT())
`

Note ConnectedStream.map() and ConnectedStream.flat_map() do not support
lambda function and must accept CoMapFunction and CoFlatMapFunction separately.

`ConnectedStream.map()`
`ConnectedStream.flat_map()`
`CoMapFunction`
`CoFlatMapFunction`

### Python Function#


Users could also use Python function to define the functionality of the transformation:


```
def my_map_func(value):
    return value + 1

data_stream = env.from_collection([1, 2, 3, 4, 5], type_info=Types.INT())
mapped_stream = data_stream.map(my_map_func, output_type=Types.INT())

```

`def my_map_func(value):
    return value + 1

data_stream = env.from_collection([1, 2, 3, 4, 5], type_info=Types.INT())
mapped_stream = data_stream.map(my_map_func, output_type=Types.INT())
`

## Output Type#


Users could specify the output type information of the transformation explicitly in Python DataStream API. If not
specified, the output type will be Types.PICKLED_BYTE_ARRAY by default, and the result data will be serialized using pickle serializer.
For more details about the pickle serializer, please refer to Pickle Serialization.

`Types.PICKLED_BYTE_ARRAY`

Generally, the output type needs to be specified in the following scenarios.


### Convert DataStream into Table#


```
from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment


def data_stream_api_demo():
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(stream_execution_environment=env)

    t_env.execute_sql("""
            CREATE TABLE my_source (
              a INT,
              b VARCHAR
            ) WITH (
              'connector' = 'datagen',
              'number-of-rows' = '10'
            )
        """)

    ds = t_env.to_append_stream(
        t_env.from_path('my_source'),
        Types.ROW([Types.INT(), Types.STRING()]))

    def split(s):
        splits = s[1].split("|")
        for sp in splits:
            yield s[0], sp

    ds = ds.map(lambda i: (i[0] + 1, i[1])) \
           .flat_map(split, Types.TUPLE([Types.INT(), Types.STRING()])) \
           .key_by(lambda i: i[1]) \
           .reduce(lambda i, j: (i[0] + j[0], i[1]))

    t_env.execute_sql("""
            CREATE TABLE my_sink (
              a INT,
              b VARCHAR
            ) WITH (
              'connector' = 'print'
            )
        """)

    table = t_env.from_data_stream(ds)
    table_result = table.execute_insert("my_sink")

    # 1ï¼wait for job finishes and only used in local execution, otherwise, it may happen that the script exits with the job is still running
    # 2ï¼should be removed when submitting the job to a remote cluster such as YARN, standalone, K8s etc in detach mode
    table_result.wait()


if __name__ == '__main__':
    data_stream_api_demo()

```

`from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment


def data_stream_api_demo():
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(stream_execution_environment=env)

    t_env.execute_sql("""
            CREATE TABLE my_source (
              a INT,
              b VARCHAR
            ) WITH (
              'connector' = 'datagen',
              'number-of-rows' = '10'
            )
        """)

    ds = t_env.to_append_stream(
        t_env.from_path('my_source'),
        Types.ROW([Types.INT(), Types.STRING()]))

    def split(s):
        splits = s[1].split("|")
        for sp in splits:
            yield s[0], sp

    ds = ds.map(lambda i: (i[0] + 1, i[1])) \
           .flat_map(split, Types.TUPLE([Types.INT(), Types.STRING()])) \
           .key_by(lambda i: i[1]) \
           .reduce(lambda i, j: (i[0] + j[0], i[1]))

    t_env.execute_sql("""
            CREATE TABLE my_sink (
              a INT,
              b VARCHAR
            ) WITH (
              'connector' = 'print'
            )
        """)

    table = t_env.from_data_stream(ds)
    table_result = table.execute_insert("my_sink")

    # 1ï¼wait for job finishes and only used in local execution, otherwise, it may happen that the script exits with the job is still running
    # 2ï¼should be removed when submitting the job to a remote cluster such as YARN, standalone, K8s etc in detach mode
    table_result.wait()


if __name__ == '__main__':
    data_stream_api_demo()
`

The output type must be specified for the flat_map operation in the above example which will be used as
the output type of the reduce operation implicitly. The reason is that
t_env.from_data_stream(ds) requires the output type of ds must be a composite type.

`t_env.from_data_stream(ds)`
`ds`

### Write DataStream to Sink#


```
from pyflink.common.typeinfo import Types

def split(s):
    splits = s[1].split("|")
    for sp in splits:
        yield s[0], sp

ds.map(lambda i: (i[0] + 1, i[1]), Types.TUPLE([Types.INT(), Types.STRING()])) \
  .sink_to(...)

```

`from pyflink.common.typeinfo import Types

def split(s):
    splits = s[1].split("|")
    for sp in splits:
        yield s[0], sp

ds.map(lambda i: (i[0] + 1, i[1]), Types.TUPLE([Types.INT(), Types.STRING()])) \
  .sink_to(...)
`

Generally, the output type needs to be specified for the map operation in the above example if the sink only accepts special kinds of data, e.g. Row, etc.


## Operator Chaining#


By default, multiple non-shuffle Python functions will be chained together to avoid the serialization and
deserialization and improve the performance. There are also cases where you may want to disable
the chaining, e.g., there is a flatmap function which will produce a large number of elements for
each input element and disabling the chaining allows to process its output in a different parallelism.

`flatmap`

Operator chaining could be disabled in one of the following ways:

* Disable chaining with following operators by adding a key_by operation,
shuffle operation,
rescale operation,
rebalance operation or
partition_custom operation
after the current operator.
* Disable chaining with preceding operators by applying a
start_new_chain operation for the current operator.
* Disable chaining with preceding and following operators by applying a
disable_chaining operation for the current operator.
* Disable chaining of two operators by setting different parallelisms or different
slot sharing group for them.
* You could also disable all the operator chaining via configuration
python.operator-chaining.enabled.
`key_by`
`shuffle`
`rescale`
`rebalance`
`partition_custom`
`start_new_chain`
`disable_chaining`
`python.operator-chaining.enabled`

## Bundling Python Functions#


To run Python functions in any non-local mode, it is strongly recommended
bundling your Python functions definitions using the config option python-files,
if your Python functions live outside the file where the main() function is defined.
Otherwise, you may run into ModuleNotFoundError: No module named 'my_function'
if you define Python functions in a file called my_function.py.

`python-files`
`main()`
`ModuleNotFoundError: No module named 'my_function'`
`my_function.py`

## Loading resources in Python Functions#


There are scenarios when you want to load some resources in Python functions first,
then running computation over and over again, without having to re-load the resources.
For example, you may want to load a large deep learning model only once,
then run batch prediction against the model multiple times.


Overriding the open method inherited from the base class Function is exactly what you need.

`open`
`Function`

```
class Predict(MapFunction):
    def open(self, runtime_context: RuntimeContext):
        import pickle

        with open("resources.zip/resources/model.pkl", "rb") as f:
            self.model = pickle.load(f)

    def eval(self, x):
        return self.model.predict(x)

```

`class Predict(MapFunction):
    def open(self, runtime_context: RuntimeContext):
        import pickle

        with open("resources.zip/resources/model.pkl", "rb") as f:
            self.model = pickle.load(f)

    def eval(self, x):
        return self.model.predict(x)
`