# Conversions between PyFlink Table and Pandas DataFrame


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Conversions between PyFlink Table and Pandas DataFrame#


PyFlink Table API supports conversion between PyFlink Table and Pandas DataFrame.


## Convert Pandas DataFrame to PyFlink Table#


Pandas DataFrames can be converted into a PyFlink Table.
Internally, PyFlink will serialize the Pandas DataFrame using Arrow columnar format on the client.
The serialized data will be processed and deserialized in Arrow source during execution.
The Arrow source can also be used in streaming jobs, and is integrated with checkpointing to
provide exactly-once guarantees.


The following example shows how to create a PyFlink Table from a Pandas DataFrame:


```
from pyflink.table import DataTypes

import pandas as pd
import numpy as np

# Create a Pandas DataFrame
pdf = pd.DataFrame(np.random.rand(1000, 2))

# Create a PyFlink Table from a Pandas DataFrame
table = t_env.from_pandas(pdf)

# Create a PyFlink Table from a Pandas DataFrame with the specified column names
table = t_env.from_pandas(pdf, ['f0', 'f1'])

# Create a PyFlink Table from a Pandas DataFrame with the specified column types
table = t_env.from_pandas(pdf, [DataTypes.DOUBLE(), DataTypes.DOUBLE()])

# Create a PyFlink Table from a Pandas DataFrame with the specified row type
table = t_env.from_pandas(pdf,
                          DataTypes.ROW([DataTypes.FIELD("f0", DataTypes.DOUBLE()),
                                         DataTypes.FIELD("f1", DataTypes.DOUBLE())]))

```

`from pyflink.table import DataTypes

import pandas as pd
import numpy as np

# Create a Pandas DataFrame
pdf = pd.DataFrame(np.random.rand(1000, 2))

# Create a PyFlink Table from a Pandas DataFrame
table = t_env.from_pandas(pdf)

# Create a PyFlink Table from a Pandas DataFrame with the specified column names
table = t_env.from_pandas(pdf, ['f0', 'f1'])

# Create a PyFlink Table from a Pandas DataFrame with the specified column types
table = t_env.from_pandas(pdf, [DataTypes.DOUBLE(), DataTypes.DOUBLE()])

# Create a PyFlink Table from a Pandas DataFrame with the specified row type
table = t_env.from_pandas(pdf,
                          DataTypes.ROW([DataTypes.FIELD("f0", DataTypes.DOUBLE()),
                                         DataTypes.FIELD("f1", DataTypes.DOUBLE())]))
`

## Convert PyFlink Table to Pandas DataFrame#


PyFlink Tables can additionally be converted into a Pandas DataFrame.
The resulting rows will be serialized as multiple Arrow batches of Arrow columnar format on the client.
The maximum Arrow batch size is configured via the option python.fn-execution.arrow.batch.size.
The serialized data will then be converted to a Pandas DataFrame.
Because the contents of the table will be collected on the client, please ensure that the results of the table can fit in memory before calling this method.
You can limit the number of rows collected to client side via 



    Table.limit




The following example shows how to convert a PyFlink Table to a Pandas DataFrame:


```
from pyflink.table.expressions import col

import pandas as pd
import numpy as np

# Create a PyFlink Table
pdf = pd.DataFrame(np.random.rand(1000, 2))
table = t_env.from_pandas(pdf, ["a", "b"]).filter(col('a') > 0.5)

# Convert the PyFlink Table to a Pandas DataFrame
pdf = table.limit(100).to_pandas()

```

`from pyflink.table.expressions import col

import pandas as pd
import numpy as np

# Create a PyFlink Table
pdf = pd.DataFrame(np.random.rand(1000, 2))
table = t_env.from_pandas(pdf, ["a", "b"]).filter(col('a') > 0.5)

# Convert the PyFlink Table to a Pandas DataFrame
pdf = table.limit(100).to_pandas()
`