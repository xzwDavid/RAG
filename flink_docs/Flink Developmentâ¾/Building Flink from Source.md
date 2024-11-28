# Building Flink from Source


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Building Flink from Source#


This page covers how to build Flink 2.0-SNAPSHOT from sources.


## Build Flink#


In order to build Flink you need the source code. Either download the source of a release or clone the git repository.


In addition you need Maven 3.8.6 and a JDK (Java Development Kit). Flink requires Java 8 (deprecated) or Java 11 to build.


To clone from git, enter:


```
git clone https://github.com/apache/flink.git

```

`git clone https://github.com/apache/flink.git
`

The simplest way of building Flink is by running:


```
mvn clean install -DskipTests

```

`mvn clean install -DskipTests
`

This instructs Maven (mvn) to first remove all existing builds (clean) and then create a new Flink binary (install).

`mvn`
`clean`
`install`

To speed up the build you can:

* skip tests by using ’ -DskipTests'
* skip QA plugins and javadoc generation by using the fast Maven profile
* skip the WebUI compilation by using the skip-webui-build Maven profile
* use Maven’s parallel build feature, e.g., ‘mvn package -T 1C’ will attempt to build 1 module for each CPU core in parallel.

  Parallel builds may deadlock due to a bug in the maven-shade-plugin. It is recommended to only use it as a 2 steps process, where you first run mvn validate/test-compile/test in parallel, and then run mvn package/verify/install with a single thread.


`fast`
`skip-webui-build`

> 
  Parallel builds may deadlock due to a bug in the maven-shade-plugin. It is recommended to only use it as a 2 steps process, where you first run mvn validate/test-compile/test in parallel, and then run mvn package/verify/install with a single thread.


`mvn validate/test-compile/test`
`mvn package/verify/install`

The build script will be:


```
mvn clean install -DskipTests -Dfast -Pskip-webui-build -T 1C

```

`mvn clean install -DskipTests -Dfast -Pskip-webui-build -T 1C
`

The fast and skip-webui-build profiles have a significant impact on the build time, particularly on slower storage devices, due to them reading/writing many small files.

`fast`
`skip-webui-build`

## Build PyFlink#


#### Prerequisites#

1. 
Building Flink
If you want to build a PyFlink package that can be used for pip installation, you need to build the Flink project first, as described in Build Flink.

2. 
Python version(3.8, 3.9, 3.10 or 3.11) is required
$ python --version
# the version printed here must be 3.8, 3.9, 3.10 or 3.11

3. 
Build PyFlink with Cython extension support (optional)
To build PyFlink with Cython extension support, youâll need a C compiler. It’s a little different on how to install the C compiler on different operating systems:


Linux Linux operating systems usually come with GCC pre-installed. Otherwise, you need to install it manually. For example, you can install it with command sudo apt-get install build-essential On Ubuntu or Debian.


Mac OS X To install GCC on Mac OS X, you need to download and install “Command Line Tools for Xcode”, which is available in Appleâs developer page.


You also need to install the dependencies with following command:
$ python -m pip install -r flink-python/dev/dev-requirements.txt


Building Flink


If you want to build a PyFlink package that can be used for pip installation, you need to build the Flink project first, as described in Build Flink.


Python version(3.8, 3.9, 3.10 or 3.11) is required


```
$ python --version
# the version printed here must be 3.8, 3.9, 3.10 or 3.11

```

`$ python --version
# the version printed here must be 3.8, 3.9, 3.10 or 3.11
`

Build PyFlink with Cython extension support (optional)


To build PyFlink with Cython extension support, youâll need a C compiler. It’s a little different on how to install the C compiler on different operating systems:

* 
Linux Linux operating systems usually come with GCC pre-installed. Otherwise, you need to install it manually. For example, you can install it with command sudo apt-get install build-essential On Ubuntu or Debian.

* 
Mac OS X To install GCC on Mac OS X, you need to download and install “Command Line Tools for Xcode”, which is available in Appleâs developer page.


Linux Linux operating systems usually come with GCC pre-installed. Otherwise, you need to install it manually. For example, you can install it with command sudo apt-get install build-essential On Ubuntu or Debian.

`sudo apt-get install build-essential`

Mac OS X To install GCC on Mac OS X, you need to download and install “Command Line Tools for Xcode”, which is available in Appleâs developer page.


You also need to install the dependencies with following command:


```
$ python -m pip install -r flink-python/dev/dev-requirements.txt

```

`$ python -m pip install -r flink-python/dev/dev-requirements.txt
`

#### Installation#


Then go to the root directory of flink source code and run this command to build the sdist package and wheel package of apache-flink and apache-flink-libraries:

`apache-flink`
`apache-flink-libraries`

```
cd flink-python; python setup.py sdist bdist_wheel; cd apache-flink-libraries; python setup.py sdist; cd ..;

```

`cd flink-python; python setup.py sdist bdist_wheel; cd apache-flink-libraries; python setup.py sdist; cd ..;
`

The sdist package of apache-flink-libraries will be found under ./flink-python/apache-flink-libraries/dist/. It could be installed as following:

`apache-flink-libraries`
`./flink-python/apache-flink-libraries/dist/`

```
python -m pip install apache-flink-libraries/dist/*.tar.gz

```

`python -m pip install apache-flink-libraries/dist/*.tar.gz
`

The sdist and wheel packages of apache-flink will be found under ./flink-python/dist/. Either of them could be used for installation, such as:

`apache-flink`
`./flink-python/dist/`

```
python -m pip install dist/*.whl

```

`python -m pip install dist/*.whl
`

## Scala Versions#


> 
  Users that purely use the Java APIs and libraries can ignore this section.



Flink has APIs, libraries, and runtime modules written in Scala. Users of the Scala API and libraries may have to match the Scala version of Flink with the Scala version of their projects (because Scala is not strictly backwards compatible).


Since version 1.15 Flink dropped the support of Scala 2.11 and it will use Scala 2.12 to build by default.


To build against a specific binary Scala version you can use:


```
mvn clean install -DskipTests -Dscala.version=<scala version>

```

`mvn clean install -DskipTests -Dscala.version=<scala version>
`

 Back to top


## Encrypted File Systems#


If your home directory is encrypted you might encounter a java.io.IOException: File name too long exception. Some encrypted file systems, like encfs used by Ubuntu, do not allow long filenames, which is the cause of this error.

`java.io.IOException: File name too long`

The workaround is to add:


```
<args>
    <arg>-Xmax-classfile-name</arg>
    <arg>128</arg>
</args>

```

`<args>
    <arg>-Xmax-classfile-name</arg>
    <arg>128</arg>
</args>
`

in the compiler configuration of the pom.xml file of the module causing the error. For example, if the error appears in the flink-yarn module, the above code should be added under the <configuration> tag of scala-maven-plugin. See this issue for more information.

`pom.xml`
`flink-yarn`
`<configuration>`
`scala-maven-plugin`

 Back to top
