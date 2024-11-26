# Debugging


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Debugging#


This page describes how to debug in PyFlink.


## Logging Infos#


### Client Side Logging#


You can log contextual and debug information via print or standard Python logging modules in
PyFlink jobs in places outside Python UDFs. The logging messages will be printed in the log files
of the client during job submission.

`print`

```
from pyflink.table import EnvironmentSettings, TableEnvironment

# create a TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')])

# use logging modules
import logging
logging.warning(table.get_schema())

# use print function
print(table.get_schema())

```

`from pyflink.table import EnvironmentSettings, TableEnvironment

# create a TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')])

# use logging modules
import logging
logging.warning(table.get_schema())

# use print function
print(table.get_schema())
`

Note: The default logging level at client side is WARNING and so only messages with logging
level WARNING or above will appear in the log files of the client.

`WARNING`
`WARNING`

### Server Side Logging#


You can log contextual and debug information via print or standard Python logging modules in Python UDFs.
The logging messages will be printed in the log files of the TaskManagers during job execution.

`print`
`TaskManagers`

```
from pyflink.table import DataTypes
from pyflink.table.udf import udf

import logging

@udf(result_type=DataTypes.BIGINT())
def add(i, j):
    # use logging modules
    logging.info("debug")
    # use print function
    print('debug')
    return i + j

```

`from pyflink.table import DataTypes
from pyflink.table.udf import udf

import logging

@udf(result_type=DataTypes.BIGINT())
def add(i, j):
    # use logging modules
    logging.info("debug")
    # use print function
    print('debug')
    return i + j
`

Note: The default logging level at server side is INFO and so only messages with logging level INFO or above
will appear in the log files of the TaskManagers.

`INFO`
`INFO`
`TaskManagers`

## Accessing Logs#


If environment variable FLINK_HOME is set, logs will be written in the log directory under FLINK_HOME.
Otherwise, logs will be placed in the directory of the PyFlink module. You can execute the following command to find
the log directory of the PyFlink module:

`FLINK_HOME`
`FLINK_HOME`

```
$ python -c "import pyflink;import os;print(os.path.dirname(os.path.abspath(pyflink.__file__))+'/log')"

```

`$ python -c "import pyflink;import os;print(os.path.dirname(os.path.abspath(pyflink.__file__))+'/log')"
`

## Debugging Python UDFs#


### Local Debug#


You can debug your python functions directly in IDEs such as PyCharm.


### Remote Debug#


You can make use of the pydevd_pycharm tool of PyCharm to debug Python UDFs.

`pydevd_pycharm`
1. 
Create a Python Remote Debug in PyCharm
run -> Python Remote Debug -> + -> choose a port (e.g. 6789)

2. 
Install the pydevd-pycharm tool
$ pip install pydevd-pycharm

3. 
Add the following command in your Python UDF
import pydevd_pycharm
pydevd_pycharm.settrace('localhost', port=6789, stdoutToServer=True, stderrToServer=True)

4. 
Start the previously created Python Remote Debug Server

5. 
Run your Python Code


Create a Python Remote Debug in PyCharm


run -> Python Remote Debug -> + -> choose a port (e.g. 6789)


Install the pydevd-pycharm tool

`pydevd-pycharm`

```
$ pip install pydevd-pycharm

```

`$ pip install pydevd-pycharm
`

Add the following command in your Python UDF


```
import pydevd_pycharm
pydevd_pycharm.settrace('localhost', port=6789, stdoutToServer=True, stderrToServer=True)

```

`import pydevd_pycharm
pydevd_pycharm.settrace('localhost', port=6789, stdoutToServer=True, stderrToServer=True)
`

Start the previously created Python Remote Debug Server


Run your Python Code


## Profiling Python UDFs#


You can enable the profile to analyze performance bottlenecks.


```
t_env.get_config().set("python.profile.enabled", "true")

```

`t_env.get_config().set("python.profile.enabled", "true")
`

Then you can see the profile result in logs
