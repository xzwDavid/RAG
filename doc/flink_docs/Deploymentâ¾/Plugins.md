# Plugins


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Plugins#


Plugins facilitate a strict separation of code through restricted classloaders. Plugins cannot
access classes from other plugins or from Flink that have not been specifically whitelisted. This
strict isolation allows plugins to contain conflicting versions of the same library without the need
to relocate classes or to converge to common versions. Currently, file systems and metric reporters are pluggable
but in the future, connectors, formats, and even user code should also be pluggable.


## Isolation and plugin structure#


Plugins reside in their own folders and can consist of several jars. The names of the plugin folders
are arbitrary.


```
flink-dist
âââ conf
âââ lib
...
âââ plugins
    âââ s3
    â   âââ aws-credential-provider.jar
    â   âââ flink-s3-fs-hadoop.jar
    âââ azure
        âââ flink-azure-fs-hadoop.jar

```

`flink-dist
âââ conf
âââ lib
...
âââ plugins
    âââ s3
    â   âââ aws-credential-provider.jar
    â   âââ flink-s3-fs-hadoop.jar
    âââ azure
        âââ flink-azure-fs-hadoop.jar
`

Each plugin is loaded through its own classloader and completely isolated from any other plugin.
Hence, the flink-s3-fs-hadoop and flink-azure-fs-hadoop can depend on different conflicting
library versions. There is no need to relocate any class during the creation of fat jars (shading).

`flink-s3-fs-hadoop`
`flink-azure-fs-hadoop`

Plugins may access certain whitelisted packages from Flink’s lib/ folder. In particular, all
necessary service provider interfaces (SPI) are loaded through the system classloader, so that no
two versions of org.apache.flink.core.fs.FileSystem exist at any given time, even if users
accidentally bundle it in their fat jar. This singleton class requirement is strictly necessary so
that the Flink runtime has an entry point into the plugin. Service classes are discovered through
the java.util.ServiceLoader, so make sure to retain the service definitions in META-INF/services
during shading.

`lib/`
`org.apache.flink.core.fs.FileSystem`
`java.util.ServiceLoader`
`META-INF/services`

Note Currently, more Flink core classes are still
accessible from plugins as we flesh out the SPI system.


Furthermore, the most common logger frameworks are whitelisted, such that logging is uniformly
possible across Flink core, plugins, and user code.


## File Systems#


All file systems are pluggable. That means they can and should
be used as plugins. To use a pluggable file system, copy the corresponding JAR file from the opt
directory to a directory under plugins directory of your Flink distribution before starting Flink,
e.g.

`opt`
`plugins`

```
mkdir ./plugins/s3-fs-hadoop
cp ./opt/flink-s3-fs-hadoop-2.0-SNAPSHOT.jar ./plugins/s3-fs-hadoop/

```

`mkdir ./plugins/s3-fs-hadoop
cp ./opt/flink-s3-fs-hadoop-2.0-SNAPSHOT.jar ./plugins/s3-fs-hadoop/
`

> 
  The s3 file systems (flink-s3-fs-presto and
flink-s3-fs-hadoop) can only be used as plugins as we already removed the relocations. Placing them in libs/ will result in system failures.


`flink-s3-fs-presto`
`flink-s3-fs-hadoop`

> 
  Because of the strict isolation, file systems do not have access to credential providers in lib/
anymore. Please add any needed providers to the respective plugin folder.



## Metric Reporters#


All metric reporters that Flink provides can be used as plugins.
See the metrics documentation for more details.


 Back to top
