# Installation


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Installation#


## Environment Requirements#


> 
  Python version (3.8, 3.9, 3.10 or 3.11) is required for PyFlink. Please run the following command to make sure that it meets the requirements:



```
$ python --version
# the version printed here must be 3.8, 3.9, 3.10 or 3.11

```

`$ python --version
# the version printed here must be 3.8, 3.9, 3.10 or 3.11
`

## Environment Setup#


Your system may include multiple Python versions, and thus also include multiple Python binary executables. You can run the following
ls command to find out what Python binary executables are available in your system:

`ls`

```
$ ls /usr/bin/python*

```

`$ ls /usr/bin/python*
`

To satisfy the PyFlink requirement regarding the Python environment version, you can choose to soft link python to point to your python3 interpreter:

`python`
`python3`

```
ln -s /usr/bin/python3 python

```

`ln -s /usr/bin/python3 python
`

In addition to creating a soft link, you can also choose to create a Python virtual environment (venv). You can refer to the Preparing Python Virtual Environment documentation page for details on how to achieve that setup.

`venv`

If you donât want to use a soft link to change the system’s python interpreter point to, you can use the configuration way to specify the Python interpreter.
For specifying the Python interpreter used to compile the jobs, you can refer to the configuration python.client.executable.
For specifying the Python interpreter used to execute the Python UDF, you can refer to the configuration python.executable.

`python`

## Installation of PyFlink#


PyFlink is available in PyPi and can be installed as follows:



$ python -m pip install apache-flink



```
$ python -m pip install apache-flink

```

`$ python -m pip install apache-flink
`

You can also build PyFlink from source by following the development guide.


Note Starting from Flink 1.11, itâs also supported to run
PyFlink jobs locally on Windows and so you could develop and debug PyFlink jobs on Windows.
