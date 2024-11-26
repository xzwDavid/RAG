# Python REPL


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Python REPL#


Flink comes with an integrated interactive Python Shell.
It can be used in a local setup as well as in a cluster setup.
See the standalone resource provider page for more information about how to setup a local Flink.
You can also build a local setup from source.


Note The Python Shell will run the command âpythonâ. Please refer to the Python Table API installation guide on how to set up the Python execution environments.


To use the shell with an integrated Flink cluster, you can simply install PyFlink with PyPi and execute the shell directly:


```
# install PyFlink
$ python -m pip install apache-flink
# execute the shell
$ pyflink-shell.sh local

```

`# install PyFlink
$ python -m pip install apache-flink
# execute the shell
$ pyflink-shell.sh local
`

To run the shell on a cluster, please see the Setup section below.


## Usage#


The shell only supports Table API currently.
The Table Environments are automatically prebound after startup.
Use “bt_env” and “st_env” to access BatchTableEnvironment and StreamTableEnvironment respectively.


### Table API#


The example below is a simple program in the Python shell:






stream
>>> import tempfile
>>> import os
>>> import shutil
>>> sink_path = tempfile.gettempdir() + '/streaming.csv'
>>> if os.path.exists(sink_path):
...     if os.path.isfile(sink_path):
...         os.remove(sink_path)
...     else:
...         shutil.rmtree(sink_path)
>>> s_env.set_parallelism(1)
>>> t = st_env.from_elements([(1, 'hi', 'hello'), (2, 'hi', 'hello')], ['a', 'b', 'c'])
>>> st_env.create_temporary_table("stream_sink", TableDescriptor.for_connector("filesystem")
...     .schema(Schema.new_builder()
...         .column("a", DataTypes.BIGINT())
...         .column("b", DataTypes.STRING())
...         .column("c", DataTypes.STRING())
...         .build())
...     .option("path", path)
...     .format(FormatDescriptor.for_format("csv")
...         .option("field-delimiter", ",")
...         .build())
...     .build())
>>> t.select("a + 1, b, c")\
...     .execute_insert("stream_sink").wait()
>>> # If the job runs in local mode, you can exec following code in Python shell to see the result:
>>> with open(os.path.join(sink_path, os.listdir(sink_path)[0]), 'r') as f:
...     print(f.read())

batch
>>> import tempfile
>>> import os
>>> import shutil
>>> sink_path = tempfile.gettempdir() + '/batch.csv'
>>> if os.path.exists(sink_path):
...     if os.path.isfile(sink_path):
...         os.remove(sink_path)
...     else:
...         shutil.rmtree(sink_path)
>>> b_env.set_parallelism(1)
>>> t = bt_env.from_elements([(1, 'hi', 'hello'), (2, 'hi', 'hello')], ['a', 'b', 'c'])
>>> st_env.create_temporary_table("batch_sink", TableDescriptor.for_connector("filesystem")
...     .schema(Schema.new_builder()
...         .column("a", DataTypes.BIGINT())
...         .column("b", DataTypes.STRING())
...         .column("c", DataTypes.STRING())
...         .build())
...     .option("path", path)
...     .format(FormatDescriptor.for_format("csv")
...         .option("field-delimiter", ",")
...         .build())
...     .build())
>>> t.select("a + 1, b, c")\
...     .execute_insert("batch_sink").wait()
>>> # If the job runs in local mode, you can exec following code in Python shell to see the result:
>>> with open(os.path.join(sink_path, os.listdir(sink_path)[0]), 'r') as f:
...     print(f.read())




```
>>> import tempfile
>>> import os
>>> import shutil
>>> sink_path = tempfile.gettempdir() + '/streaming.csv'
>>> if os.path.exists(sink_path):
...     if os.path.isfile(sink_path):
...         os.remove(sink_path)
...     else:
...         shutil.rmtree(sink_path)
>>> s_env.set_parallelism(1)
>>> t = st_env.from_elements([(1, 'hi', 'hello'), (2, 'hi', 'hello')], ['a', 'b', 'c'])
>>> st_env.create_temporary_table("stream_sink", TableDescriptor.for_connector("filesystem")
...     .schema(Schema.new_builder()
...         .column("a", DataTypes.BIGINT())
...         .column("b", DataTypes.STRING())
...         .column("c", DataTypes.STRING())
...         .build())
...     .option("path", path)
...     .format(FormatDescriptor.for_format("csv")
...         .option("field-delimiter", ",")
...         .build())
...     .build())
>>> t.select("a + 1, b, c")\
...     .execute_insert("stream_sink").wait()
>>> # If the job runs in local mode, you can exec following code in Python shell to see the result:
>>> with open(os.path.join(sink_path, os.listdir(sink_path)[0]), 'r') as f:
...     print(f.read())

```

`>>> import tempfile
>>> import os
>>> import shutil
>>> sink_path = tempfile.gettempdir() + '/streaming.csv'
>>> if os.path.exists(sink_path):
...     if os.path.isfile(sink_path):
...         os.remove(sink_path)
...     else:
...         shutil.rmtree(sink_path)
>>> s_env.set_parallelism(1)
>>> t = st_env.from_elements([(1, 'hi', 'hello'), (2, 'hi', 'hello')], ['a', 'b', 'c'])
>>> st_env.create_temporary_table("stream_sink", TableDescriptor.for_connector("filesystem")
...     .schema(Schema.new_builder()
...         .column("a", DataTypes.BIGINT())
...         .column("b", DataTypes.STRING())
...         .column("c", DataTypes.STRING())
...         .build())
...     .option("path", path)
...     .format(FormatDescriptor.for_format("csv")
...         .option("field-delimiter", ",")
...         .build())
...     .build())
>>> t.select("a + 1, b, c")\
...     .execute_insert("stream_sink").wait()
>>> # If the job runs in local mode, you can exec following code in Python shell to see the result:
>>> with open(os.path.join(sink_path, os.listdir(sink_path)[0]), 'r') as f:
...     print(f.read())
`

```
>>> import tempfile
>>> import os
>>> import shutil
>>> sink_path = tempfile.gettempdir() + '/batch.csv'
>>> if os.path.exists(sink_path):
...     if os.path.isfile(sink_path):
...         os.remove(sink_path)
...     else:
...         shutil.rmtree(sink_path)
>>> b_env.set_parallelism(1)
>>> t = bt_env.from_elements([(1, 'hi', 'hello'), (2, 'hi', 'hello')], ['a', 'b', 'c'])
>>> st_env.create_temporary_table("batch_sink", TableDescriptor.for_connector("filesystem")
...     .schema(Schema.new_builder()
...         .column("a", DataTypes.BIGINT())
...         .column("b", DataTypes.STRING())
...         .column("c", DataTypes.STRING())
...         .build())
...     .option("path", path)
...     .format(FormatDescriptor.for_format("csv")
...         .option("field-delimiter", ",")
...         .build())
...     .build())
>>> t.select("a + 1, b, c")\
...     .execute_insert("batch_sink").wait()
>>> # If the job runs in local mode, you can exec following code in Python shell to see the result:
>>> with open(os.path.join(sink_path, os.listdir(sink_path)[0]), 'r') as f:
...     print(f.read())

```

`>>> import tempfile
>>> import os
>>> import shutil
>>> sink_path = tempfile.gettempdir() + '/batch.csv'
>>> if os.path.exists(sink_path):
...     if os.path.isfile(sink_path):
...         os.remove(sink_path)
...     else:
...         shutil.rmtree(sink_path)
>>> b_env.set_parallelism(1)
>>> t = bt_env.from_elements([(1, 'hi', 'hello'), (2, 'hi', 'hello')], ['a', 'b', 'c'])
>>> st_env.create_temporary_table("batch_sink", TableDescriptor.for_connector("filesystem")
...     .schema(Schema.new_builder()
...         .column("a", DataTypes.BIGINT())
...         .column("b", DataTypes.STRING())
...         .column("c", DataTypes.STRING())
...         .build())
...     .option("path", path)
...     .format(FormatDescriptor.for_format("csv")
...         .option("field-delimiter", ",")
...         .build())
...     .build())
>>> t.select("a + 1, b, c")\
...     .execute_insert("batch_sink").wait()
>>> # If the job runs in local mode, you can exec following code in Python shell to see the result:
>>> with open(os.path.join(sink_path, os.listdir(sink_path)[0]), 'r') as f:
...     print(f.read())
`

## Setup#


To get an overview of what options the Python Shell provides, please use


```
pyflink-shell.sh --help

```

`pyflink-shell.sh --help
`

### Local#


To use the shell with an integrated Flink cluster just execute:


```
pyflink-shell.sh local

```

`pyflink-shell.sh local
`

### Remote#


To use it with a running cluster, please start the Python shell with the keyword remote
and supply the host and port of the JobManager with:

`remote`

```
pyflink-shell.sh remote <hostname> <portnumber>

```

`pyflink-shell.sh remote <hostname> <portnumber>
`

### Yarn Python Shell cluster#


The shell can deploy a Flink cluster to YARN, which is used exclusively by the
shell.
The shell deploys a new Flink cluster on YARN and connects the
cluster. You can also specify options for YARN cluster such as memory for
JobManager, name of YARN application, etc.


For example, to start a Yarn cluster for the Python Shell with two TaskManagers
use the following:


```
pyflink-shell.sh yarn -n 2

```

`pyflink-shell.sh yarn -n 2
`

For all other options, see the full reference at the bottom.


### Yarn Session#


If you have previously deployed a Flink cluster using the Flink Yarn Session,
the Python shell can connect with it using the following command:


```
pyflink-shell.sh yarn

```

`pyflink-shell.sh yarn
`

## Full Reference#


```
Flink Python Shell
Usage: pyflink-shell.sh [local|remote|yarn] [options] <args>...

Command: local [options]
Starts Flink Python shell with a local Flink cluster
usage:
     -h,--help   Show the help message with descriptions of all options.
Command: remote [options] <host> <port>
Starts Flink Python shell connecting to a remote cluster
  <host>
        Remote host name as string
  <port>
        Remote port as integer

usage:
     -h,--help   Show the help message with descriptions of all options.
Command: yarn [options]
Starts Flink Python shell connecting to a yarn cluster
usage:
     -h,--help                       Show the help message with descriptions of
                                     all options.
     -jm,--jobManagerMemory <arg>    Memory for JobManager Container with
                                     optional unit (default: MB)
     -nm,--name <arg>                Set a custom name for the application on
                                     YARN
     -qu,--queue <arg>               Specify YARN queue.
     -s,--slots <arg>                Number of slots per TaskManager
     -tm,--taskManagerMemory <arg>   Memory per TaskManager Container with
                                     optional unit (default: MB)
-h | --help
      Prints this usage text

```

`Flink Python Shell
Usage: pyflink-shell.sh [local|remote|yarn] [options] <args>...

Command: local [options]
Starts Flink Python shell with a local Flink cluster
usage:
     -h,--help   Show the help message with descriptions of all options.
Command: remote [options] <host> <port>
Starts Flink Python shell connecting to a remote cluster
  <host>
        Remote host name as string
  <port>
        Remote port as integer

usage:
     -h,--help   Show the help message with descriptions of all options.
Command: yarn [options]
Starts Flink Python shell connecting to a yarn cluster
usage:
     -h,--help                       Show the help message with descriptions of
                                     all options.
     -jm,--jobManagerMemory <arg>    Memory for JobManager Container with
                                     optional unit (default: MB)
     -nm,--name <arg>                Set a custom name for the application on
                                     YARN
     -qu,--queue <arg>               Specify YARN queue.
     -s,--slots <arg>                Number of slots per TaskManager
     -tm,--taskManagerMemory <arg>   Memory per TaskManager Container with
                                     optional unit (default: MB)
-h | --help
      Prints this usage text
`

 Back to top
