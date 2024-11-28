# Importing Flink into an IDE


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Importing Flink into an IDE#


The sections below describe how to import the Flink project into an IDE
for the development of Flink itself. For writing Flink programs, please
refer to the Java API
and the Scala API
quickstart guides.


> 
  Whenever something is not working in your IDE, try with the Maven
command line first (mvn clean package -DskipTests) as it might be your IDE
that has a bug or is not properly set up.


`mvn clean package -DskipTests`

## Preparation#


To get started, please first checkout the Flink sources from one of our
repositories,
e.g.


```
git clone https://github.com/apache/flink.git

```

`git clone https://github.com/apache/flink.git
`

### Ignoring Refactoring Commits#


We keep a list of big refactoring commits in .git-blame-ignore-revs. When looking at change
annotations using git blame it’s helpful to ignore these. You can configure git and your IDE to
do so using:

`.git-blame-ignore-revs`
`git blame`

```
git config blame.ignoreRevsFile .git-blame-ignore-revs

```

`git config blame.ignoreRevsFile .git-blame-ignore-revs
`

## IntelliJ IDEA#


The following guide has been written for IntelliJ IDEA
2021.2. Some details might differ in other versions. Please make sure to follow all steps
accurately.


### Importing Flink#

1. Choose “New” â “Project from Existing Sources”.
2. Select the root folder of the cloned Flink repository.
3. Choose “Import project from external model” and select “Maven”.
4. Leave the default options and successively click “Next” until you reach the SDK section.
5. If there is no SDK listed, create one using the “+” sign on the top left.
Select “JDK”, choose the JDK home directory and click “OK”.
Select the most suitable JDK version. NOTE: A good rule of thumb is to select
the JDK version matching the active Maven profile.
6. Continue by clicking “Next” until the import is finished.
7. Open the “Maven” tab (or right-click on the imported project and find “Maven”) and run
“Generate Sources and Update Folders”. Alternatively, you can run
mvn clean package -DskipTests.
8. Build the Project (“Build” â “Build Project”).
`mvn clean package -DskipTests`

### Copyright Profile#


Every file needs to include the Apache license as a header. This can be automated in IntelliJ by
adding a Copyright profile:

1. 
Go to “Settings” â “Editor” â “Copyright” â “Copyright Profiles”.

2. 
Add a new profile and name it “Apache”.

3. 
Add the following text as the license text:
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and 
limitations under the License.

4. 
Go to “Editor” â “Copyright” and choose the “Apache” profile as the default profile for this
project.

5. 
Click “Apply”.


Go to “Settings” â “Editor” â “Copyright” â “Copyright Profiles”.


Add a new profile and name it “Apache”.


Add the following text as the license text:


```
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and 
limitations under the License.

```

`Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and 
limitations under the License.
`

Go to “Editor” â “Copyright” and choose the “Apache” profile as the default profile for this
project.


Click “Apply”.


### Required Plugins#


Go to “Settings” â “Plugins” and select the “Marketplace” tab. Search for the following plugins,
install them, and restart the IDE if prompted:

* Scala
* Python â Required for PyFlink. If you do not
intend to work on PyFlink, you can skip this.
* Save Actions
* Checkstyle-IDEA

You will also need to install the google-java-format
plugin. However, a specific version of this plugin is required. Download
google-java-format v1.7.0.6
and install it as follows. Make sure to never update this plugin.

1. Go to “Settings” â “Plugins”.
2. Click the gear icon and select “Install Plugin from Disk”.
3. Navigate to the downloaded ZIP file and select it.

#### Code Formatting#


Flink uses Spotless together with
google-java-format to format the Java code.
For Scala, it uses Spotless with scalafmt.


It is recommended to automatically format your code by applying the following settings:

1. Go to “Settings” â “Other Settings” â “google-java-format Settings”.
2. Tick the checkbox to enable the plugin.
3. Change the code style to “Android Open Source Project (AOSP) style”.
4. Go to “Settings” â Editor â Code Style â Scala.
5. Change the “Formatter” to “scalafmt”.
6. Go to “Settings” â “Tools” â “Actions on Save”.
7. Under “Formatting Actions”, select “Optimize imports” and “Reformat code”.
8. From the “All file types list” next to “Reformat code”, select Java and Scala.

For earlier IntelliJ IDEA versions:

1. Go to “Settings” â “Other Settings” â “Save Actions”.
2. Under “General”, enable your preferred settings for when to format the code, e.g. “Activate save actions on save”.
3. Under “Formatting Actions”, select “Optimize imports” and “Reformat file”.
4. Under “File Path Inclusions”, add an entry for .*\.java and .*\.scala to avoid formatting other file types.
`.*\.java`
`.*\.scala`

You can also format the whole project (both Java and Scala) via Maven by using mvn spotless:apply.

`mvn spotless:apply`

#### Checkstyle For Java#


Checkstyle is used to enforce static coding guidelines.


> 
  Some modules are not covered by Checkstyle, e.g. flink-core, flink-optimizer, and flink-runtime.
Nevertheless, please make sure to conform to the checkstyle rules in these modules if you work in
any of these modules.


1. Go to “Settings” â “Tools” â “Checkstyle”.
2. Set “Scan Scope” to “Only Java sources (including tests)”.
3. For “Checkstyle Version” select “10.18.2”.
4. Under “Configuration File” click the “+” icon to add a new configuration.
5. Set “Description” to “Flink”.
6. Select “Use a local Checkstyle file” and point it to tools/maven/checkstyle.xml located within
your cloned repository.
7. Select “Store relative to project location” and click “Next”.
8. Configure the property checkstyle.suppressions.file with the value suppressions.xml and click
“Next”.
9. Click “Finish”.
10. Select “Flink” as the only active configuration file and click “Apply”.
`tools/maven/checkstyle.xml`
`checkstyle.suppressions.file`
`suppressions.xml`

You can now import the Checkstyle configuration for the Java code formatter.

1. Go to “Settings” â “Editor” â “Code Style” â “Java”.
2. Click the gear icon next to “Scheme” and select “Import Scheme” â “Checkstyle Configuration”.
3. Navigate to and select tools/maven/checkstyle.xml located within your cloned repository.
`tools/maven/checkstyle.xml`

To verify the setup, click “View” â “Tool Windows” â “Checkstyle” and find the “Check Module”
button in the opened tool window. It should report no violations.


#### Python for PyFlink#


Working on the flink-python module requires both a Java SDK and a Python SDK. However, IntelliJ IDEA
only supports one configured SDK per module. If you intend to work actively on PyFlink, it is
recommended to import the flink-python module as a separate project either in PyCharm
or IntelliJ IDEA for working with Python.


If you only occasionally need to work on flink-python and would like to get Python to work in
IntelliJ IDEA, e.g. to run Python tests, you can use the following guide.

1. Follow Configure a virtual environment
to create a new Virtualenv Python SDK in your Flink project.
2. Find the flink-python module in the Project Explorer, right-click on it and choose
“Open Module Settings”. Alternatively, go to “Project Structure” â “Modules” and find the module
there.
3. Change “Module SDK” to the Virtualenv Python SDK you created earlier.
4. Open the file flink-python/setup.py and install the dependencies when IntelliJ prompts you to
do so.
`flink-python/setup.py`

You can verify your setup by running some of the Python tests located in flink-python.


### Common Problems#


This section lists issues that developers have run into in the past when working with IntelliJ.


#### Compilation fails withinvalid flag: --add-exports=java.base/sun.net.util=ALL-UNNAMED#

`invalid flag: --add-exports=java.base/sun.net.util=ALL-UNNAMED`

This happens if the “java11” Maven profile is active, but an older JDK version is used. Go to
“View” â “Tool Windows” â “Maven” and uncheck the “java11” profile. Afterwards, reimport the
project.


#### Compilation fails withcannot find symbol: symbol: method defineClass(...) location: class sun.misc.Unsafe#

`cannot find symbol: symbol: method defineClass(...) location: class sun.misc.Unsafe`

This happens if you are using JDK 11, but are working on a Flink version which doesn’t yet support
Java 11 (<= 1.9). Go to “Project Structure” â “Project Settings” â “Project” and select JDK 8 as
the Project SDK.


When switching back to newer Flink versions you may have to revert this change again.


#### Compilation fails withpackage sun.misc does not exist#

`package sun.misc does not exist`

This happens if you are using JDK 11 and compile to Java 8 with the --release option. This option is currently incompatible with our build setup.
Go to “Settings” â “Build, Execution, Deployment” â “Compiler” â “Java Compiler” and uncheck the “Use ‘–release’ option for cross-compilation (Java 9 and later)”.

`--release`

#### Examples fail with aNoClassDefFoundErrorfor Flink classes.#

`NoClassDefFoundError`

This happens if Flink dependencies are set to “provided”, resulting in them not being available
on the classpath. You can either check “Include dependencies with ‘Provided’ scope” in your
run configuration, or create a test that calls the main() method of the example.

`main()`

## Eclipse#


Using Eclipse with Flink is currently not supported and discouraged. Please use
IntelliJ IDEA instead.


## PyCharm#


If you intend to work on PyFlink, it is recommended to use
PyCharm as a separate IDE for the flink-python
module. The following guide has been written for 2019.1.3. Some details might differ in other
versions.


### Importing flink-python#

1. Open the PyCharm IDE and choose (“File” â) “Open”.
2. Select the “flink-python” folder within your located repository.

### Checkstyle For Python#


Flake8 is used to enforce some coding guidelines.

1. Install flake8 for your Python interpreter using pip install flake8.
2. In PyCharm go to “Settings” â “Tools” â “External Tools”.
3. Select the “+” button to add a new external tool.
4. Set “Name” to “flake8”.
5. Set “Description” to “Code Style Check”.
6. Set “Program” to the path of your Python interpreter, e.g. /usr/bin/python.
7. Set “Arguments” to -m flake8 --config=tox.ini.
8. Set “Working Directory” to $ProjectFileDir$.
`pip install flake8`
`/usr/bin/python`
`-m flake8 --config=tox.ini`
`$ProjectFileDir$`

You can verify the setup by right-clicking on any file or folder in the flink-python project
and running “External Tools” â “flake8”.


 Back to top
