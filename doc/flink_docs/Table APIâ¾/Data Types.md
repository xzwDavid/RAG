# Data Types


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Data Types#


This page describes the data types supported in PyFlink Table API.


## Data Type#


A data type describes the logical type of a value in the table ecosystem. It can be used to declare input and/or
output types of Python user-defined functions. Users of the Python Table API work with instances of
pyflink.table.types.DataType within the Python Table API or when defining user-defined functions.

`pyflink.table.types.DataType`

A DataType instance declares the logical type which does not imply a concrete physical representation for transmission
or storage. All pre-defined data types are available in pyflink.table.types and can be instantiated with the utility methods
defined in pyflink.table.types.DataTypes.

`DataType`
`pyflink.table.types`
`pyflink.table.types.DataTypes`

A list of all pre-defined data types can be found below.


## Data Type and Python Type Mapping#


A data type can be used to declare input and/or output types of Python user-defined functions. The inputs
will be converted to Python objects corresponding to the data type and the type of the user-defined functions
result must also match the defined data type.


For vectorized Python UDF, the input types and output type are pandas.Series. The element type
of the pandas.Series corresponds to the specified data type.

`pandas.Series`
`pandas.Series`
`BOOLEAN`
`bool`
`numpy.bool_`
`TINYINT`
`int`
`numpy.int8`
`SMALLINT`
`int`
`numpy.int16`
`INT`
`int`
`numpy.int32`
`BIGINT`
`int`
`numpy.int64`
`FLOAT`
`float`
`numpy.float32`
`DOUBLE`
`float`
`numpy.float64`
`VARCHAR`
`str`
`str`
`VARBINARY`
`bytes`
`bytes`
`DECIMAL`
`decimal.Decimal`
`decimal.Decimal`
`DATE`
`datetime.date`
`datetime.date`
`TIME`
`datetime.time`
`datetime.time`
`TimestampType`
`datetime.datetime`
`datetime.datetime`
`LocalZonedTimestampType`
`datetime.datetime`
`datetime.datetime`
`INTERVAL YEAR TO MONTH`
`int`
`Not Supported Yet`
`INTERVAL DAY TO SECOND`
`datetime.timedelta`
`Not Supported Yet`
`ARRAY`
`list`
`numpy.ndarray`
`MULTISET`
`list`
`Not Supported Yet`
`MAP`
`dict`
`Not Supported Yet`
`ROW`
`Row`
`dict`