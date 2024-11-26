# Google Cloud Storage


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Google Cloud Storage#


Google Cloud Storage (GCS) provides cloud storage for a variety of use cases. You can use it for reading and writing data, and for checkpoint storage when using FileSystemCheckpointStorage) with the streaming state backends.

`FileSystemCheckpointStorage`

You can use GCS objects like regular files by specifying paths in the following format:


```
gs://<your-bucket>/<endpoint>

```

`gs://<your-bucket>/<endpoint>
`

The endpoint can either be a single file or a directory, for example:


```
// Read from GCS bucket
env.readTextFile("gs://<bucket>/<endpoint>");

// Write to GCS bucket
stream.writeAsText("gs://<bucket>/<endpoint>");

// Use GCS as checkpoint storage
Configuration config = new Configuration();
config.set(CheckpointingOptions.CHECKPOINT_STORAGE, "filesystem");
config.set(CheckpointingOptions.CHECKPOINTS_DIRECTORY, "gs://<bucket>/<endpoint>");
env.configure(config);

```

`// Read from GCS bucket
env.readTextFile("gs://<bucket>/<endpoint>");

// Write to GCS bucket
stream.writeAsText("gs://<bucket>/<endpoint>");

// Use GCS as checkpoint storage
Configuration config = new Configuration();
config.set(CheckpointingOptions.CHECKPOINT_STORAGE, "filesystem");
config.set(CheckpointingOptions.CHECKPOINTS_DIRECTORY, "gs://<bucket>/<endpoint>");
env.configure(config);
`

Note that these examples are not exhaustive and you can use GCS in other places as well, including your high availability setup or the EmbeddedRocksDBStateBackend; everywhere that Flink expects a FileSystem URI.


### GCS File System plugin#


Flink provides the flink-gs-fs-hadoop file system to write to GCS.
This implementation is self-contained with no dependency footprint, so there is no need to add Hadoop to the classpath to use it.

`flink-gs-fs-hadoop`

flink-gs-fs-hadoop registers a FileSystem wrapper for URIs with the gs:// scheme. It uses Google’s gcs-connector Hadoop library to access GCS. It also uses Google’s google-cloud-storage library to provide RecoverableWriter support.

`flink-gs-fs-hadoop`
`FileSystem`
`RecoverableWriter`

This file system can be used with the FileSystem connector.


To use flink-gs-fs-hadoop, copy the JAR file from the opt directory to the plugins directory of your Flink distribution before starting Flink, i.e.

`flink-gs-fs-hadoop`
`opt`
`plugins`

```
mkdir ./plugins/gs-fs-hadoop
cp ./opt/flink-gs-fs-hadoop-2.0-SNAPSHOT.jar ./plugins/gs-fs-hadoop/

```

`mkdir ./plugins/gs-fs-hadoop
cp ./opt/flink-gs-fs-hadoop-2.0-SNAPSHOT.jar ./plugins/gs-fs-hadoop/
`

### Configuration#


The underlying Hadoop file system can be configured using the Hadoop configuration keys for gcs-connector by adding the configurations to your Flink configuration file.

`gcs-connector`

For example, gcs-connector has a fs.gs.http.connect-timeout configuration key. If you want to change it, you need to set gs.http.connect-timeout: xyz in Flink configuration file. Flink will internally translate this back to fs.gs.http.connect-timeout.

`gcs-connector`
`fs.gs.http.connect-timeout`
`gs.http.connect-timeout: xyz`
`fs.gs.http.connect-timeout`

You can also set gcs-connector options directly in the Hadoop core-site.xml configuration file, so long as the Hadoop configuration directory is made known to Flink via the env.hadoop.conf.dir Flink option or via the HADOOP_CONF_DIR environment variable.

`gcs-connector`
`core-site.xml`
`env.hadoop.conf.dir`
`HADOOP_CONF_DIR`

flink-gs-fs-hadoop can also be configured by setting the following options in Flink configuration file:

`flink-gs-fs-hadoop`
`RecoverableWriter`
`.inprogress/`
`RecoverableWriter`

### Authentication to access GCS#


Most operations on GCS require authentication. To provide authentication credentials, either:

* 
Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of the JSON credentials file, as described here, where JobManagers and TaskManagers run. This is the recommended method.

* 
Set the google.cloud.auth.service.account.json.keyfile property in core-site.xml to the path to the JSON credentials file (and make sure that the Hadoop configuration directory is specified to Flink as described above):


Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of the JSON credentials file, as described here, where JobManagers and TaskManagers run. This is the recommended method.

`GOOGLE_APPLICATION_CREDENTIALS`

Set the google.cloud.auth.service.account.json.keyfile property in core-site.xml to the path to the JSON credentials file (and make sure that the Hadoop configuration directory is specified to Flink as described above):

`google.cloud.auth.service.account.json.keyfile`
`core-site.xml`

```
<configuration>
  <property>
    <name>google.cloud.auth.service.account.json.keyfile</name>
    <value>PATH TO GOOGLE AUTHENTICATION JSON FILE</value>
  </property>
</configuration>

```

`<configuration>
  <property>
    <name>google.cloud.auth.service.account.json.keyfile</name>
    <value>PATH TO GOOGLE AUTHENTICATION JSON FILE</value>
  </property>
</configuration>
`

For flink-gs-fs-hadoop to use credentials via either of these two methods, the use of service accounts for authentication must be enabled. This is enabled by default; however, it can be disabled in core-site.xml by setting:

`flink-gs-fs-hadoop`
`core-site.xml`

```
<configuration>
  <property>
    <name>google.cloud.auth.service.account.enable</name>
    <value>false</value>
  </property>
</configuration>

```

`<configuration>
  <property>
    <name>google.cloud.auth.service.account.enable</name>
    <value>false</value>
  </property>
</configuration>
`

> 
gcs-connector supports additional options to provide authentication credentials besides the google.cloud.auth.service.account.json.keyfile option described above.
However, if you use any of those other options, the provided credentials will not be used by the google-cloud-storage library, which provides RecoverableWriter support, so Flink recoverable-write operations would be expected to fail.
For this reason, use of the gcs-connector authentication-credentials options other than google.cloud.auth.service.account.json.keyfile is not recommended.



gcs-connector supports additional options to provide authentication credentials besides the google.cloud.auth.service.account.json.keyfile option described above.

`gcs-connector`
`google.cloud.auth.service.account.json.keyfile`

However, if you use any of those other options, the provided credentials will not be used by the google-cloud-storage library, which provides RecoverableWriter support, so Flink recoverable-write operations would be expected to fail.

`google-cloud-storage`
`RecoverableWriter`

For this reason, use of the gcs-connector authentication-credentials options other than google.cloud.auth.service.account.json.keyfile is not recommended.

`gcs-connector`
`google.cloud.auth.service.account.json.keyfile`

 Back to top
