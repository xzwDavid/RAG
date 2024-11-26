# FAQ


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# FAQ#


This page describes the solutions to some common questions for PyFlink users.


## Preparing Python Virtual Environment#


You can download a convenience script to prepare a Python virtual env zip which can be used on Mac OS and most Linux distributions.
You can specify the PyFlink version to generate a Python virtual environment required for the corresponding PyFlink version, otherwise the most recent version will be installed.



$ sh setup-pyflink-virtual-env.sh



```
$ sh setup-pyflink-virtual-env.sh

```

`$ sh setup-pyflink-virtual-env.sh
`

## Execute PyFlink jobs with Python virtual environment#


After setting up a python virtual environment, as described in the previous section, you should activate the environment before executing the PyFlink job.


#### Local#


```
# activate the conda python virtual environment
$ source venv/bin/activate
$ python xxx.py

```

`# activate the conda python virtual environment
$ source venv/bin/activate
$ python xxx.py
`

#### Cluster#


```
$ # specify the Python virtual environment
$ table_env.add_python_archive("venv.zip")
$ # specify the path of the python interpreter which is used to execute the python UDF workers
$ table_env.get_config().set_python_executable("venv.zip/venv/bin/python")

```

`$ # specify the Python virtual environment
$ table_env.add_python_archive("venv.zip")
$ # specify the path of the python interpreter which is used to execute the python UDF workers
$ table_env.get_config().set_python_executable("venv.zip/venv/bin/python")
`

For details on the usage of add_python_archive and set_python_executable, you can refer to the relevant documentation.

`add_python_archive`
`set_python_executable`

## Adding Jar Files#


A PyFlink job may depend on jar files, i.e. connectors, Java UDFs, etc.
You can specify the dependencies with the following Python Table APIs or through command-line arguments directly when submitting the job.


```
# NOTE: Only local file URLs (start with "file:") are supported.
table_env.get_config().set("pipeline.jars", "file:///my/jar/path/connector.jar;file:///my/jar/path/udf.jar")

# NOTE: The Paths must specify a protocol (e.g. "file") and users should ensure that the URLs are accessible on both the client and the cluster.
table_env.get_config().set("pipeline.classpaths", "file:///my/jar/path/connector.jar;file:///my/jar/path/udf.jar")

```

`# NOTE: Only local file URLs (start with "file:") are supported.
table_env.get_config().set("pipeline.jars", "file:///my/jar/path/connector.jar;file:///my/jar/path/udf.jar")

# NOTE: The Paths must specify a protocol (e.g. "file") and users should ensure that the URLs are accessible on both the client and the cluster.
table_env.get_config().set("pipeline.classpaths", "file:///my/jar/path/connector.jar;file:///my/jar/path/udf.jar")
`

For details about the APIs of adding Java dependency, you can refer to the relevant documentation


## Adding Python Files#


You can use the command-line arguments pyfs or the API add_python_file of TableEnvironment to add python file dependencies which could be python files, python packages or local directories.
For example, if you have a directory named myDir which has the following hierarchy:

`pyfs`
`add_python_file`
`TableEnvironment`
`myDir`

```
myDir
âââutils
    âââ__init__.py
    âââmy_util.py

```

`myDir
âââutils
    âââ__init__.py
    âââmy_util.py
`

You can add the Python files of directory myDir as following:

`myDir`

```
table_env.add_python_file('myDir')

def my_udf():
    from utils import my_util

```

`table_env.add_python_file('myDir')

def my_udf():
    from utils import my_util
`

## Wait for jobs to finish when executing jobs in mini cluster#


When executing jobs in mini cluster(e.g. when executing jobs in IDE) and using the following APIs in the jobs(
e.g. TableEnvironment.execute_sql, StatementSet.execute, etc in the Python Table API; StreamExecutionEnvironment.execute_async
in the Python DataStream API), please remember to explicitly wait for the job execution to finish as these APIs are asynchronous.
Otherwise you may could not find the execution results as the program will exit before the job execution finishes. Please refer
to the following example on how to do that:


```
# execute SQL / Table API query asynchronously
t_result = table_env.execute_sql(...)
t_result.wait()

# execute DataStream Job asynchronously
job_client = stream_execution_env.execute_async('My DataStream Job')
job_client.get_job_execution_result().result()

```

`# execute SQL / Table API query asynchronously
t_result = table_env.execute_sql(...)
t_result.wait()

# execute DataStream Job asynchronously
job_client = stream_execution_env.execute_async('My DataStream Job')
job_client.get_job_execution_result().result()
`

Note: There is no need to wait for the job execution to finish when executing jobs in remote cluster and so remember to remove these codes when executing jobs in remote cluster.
