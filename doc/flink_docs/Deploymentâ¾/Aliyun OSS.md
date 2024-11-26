# Aliyun OSS


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Aliyun Object Storage Service (OSS)#


## OSS: Object Storage Service#


Aliyun Object Storage Service (Aliyun OSS) is widely used, particularly popular among Chinaâs cloud users, and it provides cloud object storage for a variety of use cases.
You can use OSS with Flink for reading and writing data as well in conjunction with the streaming state backends


You can use OSS objects like regular files by specifying paths in the following format:


```
oss://<your-bucket>/<object-name>

```

`oss://<your-bucket>/<object-name>
`

Below shows how to use OSS in a Flink job:


```
// Read from OSS bucket
env.readTextFile("oss://<your-bucket>/<object-name>");

// Write to OSS bucket
stream.writeAsText("oss://<your-bucket>/<object-name>");

// Use OSS as checkpoint storage
Configuration config = new Configuration();
config.set(CheckpointingOptions.CHECKPOINT_STORAGE, "filesystem");
config.set(CheckpointingOptions.CHECKPOINTS_DIRECTORY, "oss://<your-bucket>/<object-name>");
env.configure(config);

```

`// Read from OSS bucket
env.readTextFile("oss://<your-bucket>/<object-name>");

// Write to OSS bucket
stream.writeAsText("oss://<your-bucket>/<object-name>");

// Use OSS as checkpoint storage
Configuration config = new Configuration();
config.set(CheckpointingOptions.CHECKPOINT_STORAGE, "filesystem");
config.set(CheckpointingOptions.CHECKPOINTS_DIRECTORY, "oss://<your-bucket>/<object-name>");
env.configure(config);
`

### Shaded Hadoop OSS file system#


To use flink-oss-fs-hadoop, copy the respective JAR file from the opt directory to a directory in plugins directory of your Flink distribution before starting Flink, e.g.

`flink-oss-fs-hadoop`
`opt`
`plugins`

```
mkdir ./plugins/oss-fs-hadoop
cp ./opt/flink-oss-fs-hadoop-2.0-SNAPSHOT.jar ./plugins/oss-fs-hadoop/

```

`mkdir ./plugins/oss-fs-hadoop
cp ./opt/flink-oss-fs-hadoop-2.0-SNAPSHOT.jar ./plugins/oss-fs-hadoop/
`

flink-oss-fs-hadoop registers default FileSystem wrappers for URIs with the oss:// scheme.

`flink-oss-fs-hadoop`

#### Configurations setup#


After setting up the OSS FileSystem wrapper, you need to add some configurations to make sure that Flink is allowed to access your OSS buckets.


To allow for easy adoption, you can use the same configuration keys in Flink configuration file as in Hadoop’s core-site.xml

`core-site.xml`

You can see the configuration keys in the Hadoop OSS documentation.


There are some required configurations that must be added to Flink configuration file (Other configurations defined in Hadoop OSS documentation are advanced configurations which used by performance tuning):


```
fs.oss.endpoint: Aliyun OSS endpoint to connect to
fs.oss.accessKeyId: Aliyun access key ID
fs.oss.accessKeySecret: Aliyun access key secret

```

`fs.oss.endpoint: Aliyun OSS endpoint to connect to
fs.oss.accessKeyId: Aliyun access key ID
fs.oss.accessKeySecret: Aliyun access key secret
`

An alternative CredentialsProvider can also be configured in the Flink configuration file, e.g.

`CredentialsProvider`

```
# Read Credentials from OSS_ACCESS_KEY_ID and OSS_ACCESS_KEY_SECRET
fs.oss.credentials.provider: com.aliyun.oss.common.auth.EnvironmentVariableCredentialsProvider

```

`# Read Credentials from OSS_ACCESS_KEY_ID and OSS_ACCESS_KEY_SECRET
fs.oss.credentials.provider: com.aliyun.oss.common.auth.EnvironmentVariableCredentialsProvider
`

Other credential providers can be found under here.


 Back to top
