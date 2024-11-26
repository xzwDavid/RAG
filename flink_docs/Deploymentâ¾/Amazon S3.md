# Amazon S3


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Amazon S3#


Amazon Simple Storage Service (Amazon S3) provides cloud object storage for a variety of use cases. You can use S3 with Flink for reading and writing data as well in conjunction with the streaming state backends.


You can use S3 objects like regular files by specifying paths in the following format:


```
s3://<your-bucket>/<endpoint>

```

`s3://<your-bucket>/<endpoint>
`

The endpoint can either be a single file or a directory, for example:


```
// Read from S3 bucket
env.readTextFile("s3://<bucket>/<endpoint>");

// Write to S3 bucket
stream.writeAsText("s3://<bucket>/<endpoint>");

// Use S3 as checkpoint storage
Configuration config = new Configuration();
config.set(CheckpointingOptions.CHECKPOINT_STORAGE, "filesystem");
config.set(CheckpointingOptions.CHECKPOINTS_DIRECTORY, "s3://<your-bucket>/<endpoint>");
env.configure(config);

```

`// Read from S3 bucket
env.readTextFile("s3://<bucket>/<endpoint>");

// Write to S3 bucket
stream.writeAsText("s3://<bucket>/<endpoint>");

// Use S3 as checkpoint storage
Configuration config = new Configuration();
config.set(CheckpointingOptions.CHECKPOINT_STORAGE, "filesystem");
config.set(CheckpointingOptions.CHECKPOINTS_DIRECTORY, "s3://<your-bucket>/<endpoint>");
env.configure(config);
`

Note that these examples are not exhaustive and you can use S3 in other places as well, including your high availability setup or the EmbeddedRocksDBStateBackend; everywhere that Flink expects a FileSystem URI (unless otherwise stated).


For most use cases, you may use one of our flink-s3-fs-hadoop and flink-s3-fs-presto S3 filesystem plugins which are self-contained and easy to set up.
For some cases, however, e.g., for using S3 as YARN’s resource storage dir, it may be necessary to set up a specific Hadoop S3 filesystem implementation.

`flink-s3-fs-hadoop`
`flink-s3-fs-presto`

### Hadoop/Presto S3 File Systems plugins#


> 
  You don’t have to configure this manually if you are running Flink on EMR.



Flink provides two file systems to talk to Amazon S3, flink-s3-fs-presto and flink-s3-fs-hadoop.
Both implementations are self-contained with no dependency footprint, so there is no need to add Hadoop to the classpath to use them.

`flink-s3-fs-presto`
`flink-s3-fs-hadoop`
* 
flink-s3-fs-presto, registered under the scheme s3:// and s3p://, is based on code from the Presto project.
You can configure it using the same configuration keys as the Presto file system, by adding the configurations to your Flink configuration file. The Presto S3 implementation is the recommended file system for checkpointing to S3.

* 
flink-s3-fs-hadoop, registered under s3:// and s3a://, based on code from the Hadoop Project.
The file system can be configured using Hadoop’s s3a configuration keys by adding the configurations to your Flink configuration file.
For example, Hadoop has a fs.s3a.connection.maximum configuration key. If you want to change it, you need to put s3.connection.maximum: xyz to the Flink configuration file. Flink will internally translate this back to fs.s3a.connection.maximum. There is no need to pass configuration parameters using Hadoop’s XML configuration files.
It is the only S3 file system with support for the FileSystem.


flink-s3-fs-presto, registered under the scheme s3:// and s3p://, is based on code from the Presto project.
You can configure it using the same configuration keys as the Presto file system, by adding the configurations to your Flink configuration file. The Presto S3 implementation is the recommended file system for checkpointing to S3.

`flink-s3-fs-presto`

flink-s3-fs-hadoop, registered under s3:// and s3a://, based on code from the Hadoop Project.
The file system can be configured using Hadoop’s s3a configuration keys by adding the configurations to your Flink configuration file.

`flink-s3-fs-hadoop`

For example, Hadoop has a fs.s3a.connection.maximum configuration key. If you want to change it, you need to put s3.connection.maximum: xyz to the Flink configuration file. Flink will internally translate this back to fs.s3a.connection.maximum. There is no need to pass configuration parameters using Hadoop’s XML configuration files.

`fs.s3a.connection.maximum`
`s3.connection.maximum: xyz`
`fs.s3a.connection.maximum`

It is the only S3 file system with support for the FileSystem.


Both flink-s3-fs-hadoop and flink-s3-fs-presto register default FileSystem
wrappers for URIs with the s3:// scheme, flink-s3-fs-hadoop also registers
for s3a:// and flink-s3-fs-presto also registers for s3p://, so you can
use this to use both at the same time.
For example, the job uses the FileSystem which only supports Hadoop, but uses Presto for checkpointing.
In this case, you should explicitly use s3a:// as a scheme for the sink (Hadoop) and s3p:// for checkpointing (Presto).

`flink-s3-fs-hadoop`
`flink-s3-fs-presto`
`flink-s3-fs-hadoop`
`flink-s3-fs-presto`

To use flink-s3-fs-hadoop or flink-s3-fs-presto, copy the respective JAR file from the opt directory to the plugins directory of your Flink distribution before starting Flink, e.g.

`flink-s3-fs-hadoop`
`flink-s3-fs-presto`
`opt`
`plugins`

```
mkdir ./plugins/s3-fs-presto
cp ./opt/flink-s3-fs-presto-2.0-SNAPSHOT.jar ./plugins/s3-fs-presto/

```

`mkdir ./plugins/s3-fs-presto
cp ./opt/flink-s3-fs-presto-2.0-SNAPSHOT.jar ./plugins/s3-fs-presto/
`

#### Configure Access Credentials#


After setting up the S3 FileSystem wrapper, you need to make sure that Flink is allowed to access your S3 buckets.


##### Identity and Access Management (IAM) (Recommended)#


The recommended way of setting up credentials on AWS is via Identity and Access Management (IAM). You can use IAM features to securely give Flink instances the credentials that they need to access S3 buckets. Details about how to do this are beyond the scope of this documentation. Please refer to the AWS user guide. What you are looking for are IAM Roles.


If you set this up correctly, you can manage access to S3 within AWS and don’t need to distribute any access keys to Flink.


##### Access Keys (Discouraged)#


Access to S3 can be granted via your access and secret key pair. Please note that this is discouraged since the introduction of IAM roles.


You need to configure both s3.access-key and s3.secret-key  in Flink’s  Flink configuration file:

`s3.access-key`
`s3.secret-key`

```
s3.access-key: your-access-key
s3.secret-key: your-secret-key

```

`s3.access-key: your-access-key
s3.secret-key: your-secret-key
`

You can limit this configuration to JobManagers by using Flink configuration file.


```
# flink-s3-fs-hadoop
fs.s3a.aws.credentials.provider: org.apache.flink.fs.s3.common.token.DynamicTemporaryAWSCredentialsProvider
# flink-s3-fs-presto
presto.s3.credential-provider: org.apache.flink.fs.s3.common.token.DynamicTemporaryAWSCredentialsProvider

```

`# flink-s3-fs-hadoop
fs.s3a.aws.credentials.provider: org.apache.flink.fs.s3.common.token.DynamicTemporaryAWSCredentialsProvider
# flink-s3-fs-presto
presto.s3.credential-provider: org.apache.flink.fs.s3.common.token.DynamicTemporaryAWSCredentialsProvider
`

## Configure Non-S3 Endpoint#


The S3 Filesystems also support using S3 compliant object stores such as IBM’s Cloud Object Storage and MinIO.
To do so, configure your endpoint in Flink configuration file.


```
s3.endpoint: your-endpoint-hostname

```

`s3.endpoint: your-endpoint-hostname
`

## Configure Path Style Access#


Some S3 compliant object stores might not have virtual host style addressing enabled by default, for example when using Standalone MinIO for testing purpose. In such cases, you will have to provide the property to enable path style access in Flink configuration file.


```
s3.path.style.access: true

```

`s3.path.style.access: true
`

## Entropy injection for S3 file systems#


The bundled S3 file systems (flink-s3-fs-presto and flink-s3-fs-hadoop) support entropy injection. Entropy injection is
a technique to improve the scalability of AWS S3 buckets through adding some random characters near the beginning of the key.

`flink-s3-fs-presto`
`flink-s3-fs-hadoop`

If entropy injection is activated, a configured substring in the path is replaced with random characters. For example, path
s3://my-bucket/_entropy_/checkpoints/dashboard-job/ would be replaced by something like s3://my-bucket/gf36ikvg/checkpoints/dashboard-job/.
This only happens when the file creation passes the option to inject entropy!
Otherwise, the file path removes the entropy key substring entirely. See FileSystem.create(Path, WriteOption)
for details.

`s3://my-bucket/_entropy_/checkpoints/dashboard-job/`
`s3://my-bucket/gf36ikvg/checkpoints/dashboard-job/`

> 
  The Flink runtime currently passes the option to inject entropy only to checkpoint data files. All other files, including checkpoint metadata and external URI, do not inject entropy to keep checkpoint URIs predictable.



To enable entropy injection, configure the entropy key and the entropy length parameters.


```
s3.entropy.key: _entropy_
s3.entropy.length: 4 (default)

```

`s3.entropy.key: _entropy_
s3.entropy.length: 4 (default)
`

The s3.entropy.key defines the string in paths that is replaced by the random characters. Paths that do not contain the entropy key are left unchanged.
If a file system operation does not pass the “inject entropy” write option, the entropy key substring is simply removed.
The s3.entropy.length defines the number of random alphanumeric characters used for entropy.

`s3.entropy.key`
`s3.entropy.length`

## s5cmd#


Both flink-s3-fs-hadoop and flink-s3-fs-presto can be configured to use the s5cmd tool for faster file upload and download.
Benchmark results are showing that s5cmd can be over 2 times more CPU efficient.
Which means either using half the CPU to upload or download the same set of files, or doing that twice as fast with the same amount of available CPU.

`flink-s3-fs-hadoop`
`flink-s3-fs-presto`
`s5cmd`

In order to use this feature, the s5cmd binary has to be present and accessible to the Flink’s task managers, for example via embedding it in the used docker image.
Secondly, the path to the s5cmd has to be configured via:

`s5cmd`
`s5cmd`

```
s3.s5cmd.path: /path/to/the/s5cmd

```

`s3.s5cmd.path: /path/to/the/s5cmd
`

The remaining configuration options (with their default value listed below) are:


```
# Extra arguments that will be passed directly to the s5cmd call. Please refer to the s5cmd's official documentation.
s3.s5cmd.args: -r 0
# Maximum size of files that will be uploaded via a single s5cmd call.
s3.s5cmd.batch.max-size: 1024mb
# Maximum number of files that will be uploaded via a single s5cmd call.
s3.s5cmd.batch.max-files: 100

```

`# Extra arguments that will be passed directly to the s5cmd call. Please refer to the s5cmd's official documentation.
s3.s5cmd.args: -r 0
# Maximum size of files that will be uploaded via a single s5cmd call.
s3.s5cmd.batch.max-size: 1024mb
# Maximum number of files that will be uploaded via a single s5cmd call.
s3.s5cmd.batch.max-files: 100
`

Both s3.s5cmd.batch.max-size and s3.s5cmd.batch.max-files are used to control resource usage of the s5cmd binary, to prevent it from overloading the task manager.

`s3.s5cmd.batch.max-size`
`s3.s5cmd.batch.max-files`
`s5cmd`

It is recommended to first configure and making sure Flink works without using s5cmd and only then enabling this feature.

`s5cmd`

### Credentials#


If you are using access keys, they will be passed to the s5cmd.
Apart from that s5cmd has its own independent (but similar) of Flink way of using credentials.

`s5cmd`
`s5cmd`

### Limitations#


Currently, Flink will use s5cmd only during recovery, when downloading state files from S3 and using RocksDB.

`s5cmd`

 Back to top
