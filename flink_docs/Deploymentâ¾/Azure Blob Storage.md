# Azure Blob Storage


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Azure Blob Storage#


Azure Blob Storage is a Microsoft-managed service providing cloud storage for a variety of use cases.
You can use Azure Blob Storage with Flink for reading and writing data as well in conjunction with the streaming state backends


Flink supports accessing Azure Blob Storage using both wasb:// or abfs://.


> 
  Azure recommends using abfs:// for accessing ADLS Gen2 storage accounts even though wasb:// works through backward compatibility.



> 
  abfs:// can be used for accessing the ADLS Gen2 storage accounts only. Please visit Azure documentation on how to identify ADLS Gen2 storage account.



You can use Azure Blob Storage objects like regular files by specifying paths in the following format:


```
// WASB unencrypted access
wasb://<your-container>@$<your-azure-account>.blob.core.windows.net/<object-path>

// WASB SSL encrypted access
wasbs://<your-container>@$<your-azure-account>.blob.core.windows.net/<object-path>

// ABFS unecrypted access
abfs://<your-container>@$<your-azure-account>.dfs.core.windows.net/<object-path>

// ABFS SSL encrypted access
abfss://<your-container>@$<your-azure-account>.dfs.core.windows.net/<object-path>

```

`// WASB unencrypted access
wasb://<your-container>@$<your-azure-account>.blob.core.windows.net/<object-path>

// WASB SSL encrypted access
wasbs://<your-container>@$<your-azure-account>.blob.core.windows.net/<object-path>

// ABFS unecrypted access
abfs://<your-container>@$<your-azure-account>.dfs.core.windows.net/<object-path>

// ABFS SSL encrypted access
abfss://<your-container>@$<your-azure-account>.dfs.core.windows.net/<object-path>
`

See below for how to use Azure Blob Storage in a Flink job:


```
// Read from Azure Blob storage
env.readTextFile("wasb://<your-container>@$<your-azure-account>.blob.core.windows.net/<object-path>");

// Write to Azure Blob storage
stream.writeAsText("wasb://<your-container>@$<your-azure-account>.blob.core.windows.net/<object-path>");

// Use Azure Blob Storage as checkpoint storage
Configuration config = new Configuration();
config.set(CheckpointingOptions.CHECKPOINT_STORAGE, "filesystem");
config.set(CheckpointingOptions.CHECKPOINTS_DIRECTORY, "wasb://<your-container>@$<your-azure-account>.blob.core.windows.net/<object-path>");
env.configure(config);

```

`// Read from Azure Blob storage
env.readTextFile("wasb://<your-container>@$<your-azure-account>.blob.core.windows.net/<object-path>");

// Write to Azure Blob storage
stream.writeAsText("wasb://<your-container>@$<your-azure-account>.blob.core.windows.net/<object-path>");

// Use Azure Blob Storage as checkpoint storage
Configuration config = new Configuration();
config.set(CheckpointingOptions.CHECKPOINT_STORAGE, "filesystem");
config.set(CheckpointingOptions.CHECKPOINTS_DIRECTORY, "wasb://<your-container>@$<your-azure-account>.blob.core.windows.net/<object-path>");
env.configure(config);
`

### Shaded Hadoop Azure Blob Storage file system#


To use flink-azure-fs-hadoop, copy the respective JAR file from the opt directory to the plugins directory of your Flink distribution before starting Flink, e.g.

`flink-azure-fs-hadoop`
`opt`
`plugins`

```
mkdir ./plugins/azure-fs-hadoop
cp ./opt/flink-azure-fs-hadoop-2.0-SNAPSHOT.jar ./plugins/azure-fs-hadoop/

```

`mkdir ./plugins/azure-fs-hadoop
cp ./opt/flink-azure-fs-hadoop-2.0-SNAPSHOT.jar ./plugins/azure-fs-hadoop/
`

flink-azure-fs-hadoop registers default FileSystem wrappers for URIs with the wasb:// and wasbs:// (SSL encrypted access) scheme.

`flink-azure-fs-hadoop`

## Credentials Configuration#


### WASB#


Hadoop’s WASB Azure Filesystem supports configuration of credentials via the Hadoop configuration as
outlined in the Hadoop Azure Blob Storage documentation.
For convenience Flink forwards all Flink configurations with a key prefix of fs.azure to the
Hadoop configuration of the filesystem. Consequently, the azure blob storage key can be configured
in Flink configuration file via:

`fs.azure`

```
fs.azure.account.key.<account_name>.blob.core.windows.net: <azure_storage_key>

```

`fs.azure.account.key.<account_name>.blob.core.windows.net: <azure_storage_key>
`

Alternatively, the filesystem can be configured to read the Azure Blob Storage key from an
environment variable AZURE_STORAGE_KEY by setting the following configuration keys in
Flink configuration file.

`AZURE_STORAGE_KEY`

```
fs.azure.account.keyprovider.<account_name>.blob.core.windows.net: org.apache.flink.fs.azurefs.EnvironmentVariableKeyProvider

```

`fs.azure.account.keyprovider.<account_name>.blob.core.windows.net: org.apache.flink.fs.azurefs.EnvironmentVariableKeyProvider
`

### ABFS#


Hadoop’s ABFS Azure Filesystem supports several ways of configuring authentication. Please visit the Hadoop ABFS documentation documentation on how to configure.


> 
Azure recommends using Azure managed identity to access the ADLS Gen2 storage accounts using abfs. Please refer to Azure managed identities documentation for more details.
Please visit the page for the list of services that support Managed Identities. Flink clusters deployed in those Azure services can take advantage of Managed Identities.



Azure recommends using Azure managed identity to access the ADLS Gen2 storage accounts using abfs. Please refer to Azure managed identities documentation for more details.


Please visit the page for the list of services that support Managed Identities. Flink clusters deployed in those Azure services can take advantage of Managed Identities.


##### Accessing ABFS using storage Keys (Discouraged)#


Azure blob storage key can be configured in Flink configuration file via:


```
fs.azure.account.key.<account_name>.dfs.core.windows.net: <azure_storage_key>

```

`fs.azure.account.key.<account_name>.dfs.core.windows.net: <azure_storage_key>
`

 Back to top
