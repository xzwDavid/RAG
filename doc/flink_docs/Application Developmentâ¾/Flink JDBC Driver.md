# Flink JDBC Driver


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Flink JDBC Driver#


The Flink JDBC Driver is a Java library for enabling clients to send Flink SQL to your Flink cluster via the SQL Gateway.


You can also use the Hive JDBC Driver with Flink. This is beneficial if you are running Hive dialect SQL and want to make use of the Hive Catalog. To use Hive JDBC with Flink you need to run the SQL Gateway with the HiveServer2 endpoint.


## Usage#


Before using the Flink JDBC driver you need to start a SQL Gateway with REST endpoint. This acts as the JDBC server and binds it with your Flink cluster.


The examples below assume that you have a gateway started and connected to a running Flink cluster.


## Dependency#


All dependencies for JDBC driver have been packaged in flink-sql-jdbc-driver-bundle, you can download and add the jar file in your project.

`flink-sql-jdbc-driver-bundle`
`org.apache.flink`
`flink-sql-jdbc-driver-bundle`

You can also add dependency of Flink JDBC driver in your maven or gradle project.


Maven Dependency


```
    <dependency>
      <groupId>org.apache.flink</groupId>
      <artifactId>flink-sql-jdbc-driver-bundle</artifactId>
      <version>{VERSION}</version>
    </dependency>

```

`    <dependency>
      <groupId>org.apache.flink</groupId>
      <artifactId>flink-sql-jdbc-driver-bundle</artifactId>
      <version>{VERSION}</version>
    </dependency>
`

## JDBC Clients#


The Flink JDBC driver is not included with the Flink distribution. You can download it from Maven.


You may also need the SLF4J (slf4j-api-{slf4j.version}.jar) jar.

`slf4j-api-{slf4j.version}.jar`

### Beeline#


Beeline is the command line tool for accessing Apache Hive, but it also supports general JDBC drivers. To install Hive and beeline, see Hive documentation.

1. 
Download flink-jdbc-driver-bundle-{VERSION}.jar from download page and add it to $HIVE_HOME/lib.

2. 
Run beeline and connect to a Flink SQL gateway. As Flink SQL gateway currently ignores user names and passwords, just leave them empty.
beeline> !connect jdbc:flink://localhost:8083

3. 
Execute any statement you want.


Download flink-jdbc-driver-bundle-{VERSION}.jar from download page and add it to $HIVE_HOME/lib.

`$HIVE_HOME/lib`

Run beeline and connect to a Flink SQL gateway. As Flink SQL gateway currently ignores user names and passwords, just leave them empty.


```
beeline> !connect jdbc:flink://localhost:8083

```

`beeline> !connect jdbc:flink://localhost:8083
`

Execute any statement you want.


Sample Commands


```
Beeline version 3.1.3 by Apache Hive
beeline> !connect jdbc:flink://localhost:8083
Connecting to jdbc:flink://localhost:8083
Enter username for jdbc:flink://localhost:8083: 
Enter password for jdbc:flink://localhost:8083: 
Connected to: Flink JDBC Driver (version 1.18-SNAPSHOT)
Driver: org.apache.flink.table.jdbc.FlinkDriver (version 1.18-SNAPSHOT)
0: jdbc:flink://localhost:8083> CREATE TABLE T(
. . . . . . . . . . . . . . . >     a INT,
. . . . . . . . . . . . . . . >     b VARCHAR(10)
. . . . . . . . . . . . . . . > ) WITH (
. . . . . . . . . . . . . . . >     'connector' = 'filesystem',
. . . . . . . . . . . . . . . >     'path' = 'file:///tmp/T.csv',
. . . . . . . . . . . . . . . >     'format' = 'csv'
. . . . . . . . . . . . . . . > );
No rows affected (0.108 seconds)
0: jdbc:flink://localhost:8083> INSERT INTO T VALUES (1, 'Hi'), (2, 'Hello');
+-----------------------------------+
|              job id               |
+-----------------------------------+
| da22010cf1c962b377493fc4fc509527  |
+-----------------------------------+
1 row selected (0.952 seconds)
0: jdbc:flink://localhost:8083> SELECT * FROM T;
+----+--------+
| a  |   b    |
+----+--------+
| 1  | Hi     |
| 2  | Hello  |
+----+--------+
2 rows selected (1.142 seconds)
0: jdbc:flink://localhost:8083> 

```

`Beeline version 3.1.3 by Apache Hive
beeline> !connect jdbc:flink://localhost:8083
Connecting to jdbc:flink://localhost:8083
Enter username for jdbc:flink://localhost:8083: 
Enter password for jdbc:flink://localhost:8083: 
Connected to: Flink JDBC Driver (version 1.18-SNAPSHOT)
Driver: org.apache.flink.table.jdbc.FlinkDriver (version 1.18-SNAPSHOT)
0: jdbc:flink://localhost:8083> CREATE TABLE T(
. . . . . . . . . . . . . . . >     a INT,
. . . . . . . . . . . . . . . >     b VARCHAR(10)
. . . . . . . . . . . . . . . > ) WITH (
. . . . . . . . . . . . . . . >     'connector' = 'filesystem',
. . . . . . . . . . . . . . . >     'path' = 'file:///tmp/T.csv',
. . . . . . . . . . . . . . . >     'format' = 'csv'
. . . . . . . . . . . . . . . > );
No rows affected (0.108 seconds)
0: jdbc:flink://localhost:8083> INSERT INTO T VALUES (1, 'Hi'), (2, 'Hello');
+-----------------------------------+
|              job id               |
+-----------------------------------+
| da22010cf1c962b377493fc4fc509527  |
+-----------------------------------+
1 row selected (0.952 seconds)
0: jdbc:flink://localhost:8083> SELECT * FROM T;
+----+--------+
| a  |   b    |
+----+--------+
| 1  | Hi     |
| 2  | Hello  |
+----+--------+
2 rows selected (1.142 seconds)
0: jdbc:flink://localhost:8083> 
`

### SQLLine#


SQLLine is a lightweight JDBC command line tool that supports general JDBC drivers.


To use SQLLine you will need to clone the GitHub repository and compile the project first (./mvnw package -DskipTests).

`./mvnw package -DskipTests`
1. 
Download the following JARs and add them both to the target directory of SQLLine project:

Flink JDBC Driver (flink-jdbc-driver-bundle-{VERSION}.jar)
SLF4J (slf4j-api-{slf4j.version}.jar)


2. 
Run SQLLine with command ./bin/sqlline

3. 
From SQLLine, connect to a Flink SQL gateway using the !connect command.
Since the Flink SQL gateway currently ignores user names and passwords just leave them empty.
sqlline version 1.13.0-SNAPSHOT
sqlline> !connect jdbc:flink://localhost:8083
Enter username for jdbc:flink://localhost:8083:
Enter password for jdbc:flink://localhost:8083:
0: jdbc:flink://localhost:8083>

4. 
You can now execute any Flink SQL statement you want.


Download the following JARs and add them both to the target directory of SQLLine project:

`target`
1. Flink JDBC Driver (flink-jdbc-driver-bundle-{VERSION}.jar)
2. SLF4J (slf4j-api-{slf4j.version}.jar)
`flink-jdbc-driver-bundle-{VERSION}.jar`
`slf4j-api-{slf4j.version}.jar`

Run SQLLine with command ./bin/sqlline

`./bin/sqlline`

From SQLLine, connect to a Flink SQL gateway using the !connect command.

`!connect`

Since the Flink SQL gateway currently ignores user names and passwords just leave them empty.


```
sqlline version 1.13.0-SNAPSHOT
sqlline> !connect jdbc:flink://localhost:8083
Enter username for jdbc:flink://localhost:8083:
Enter password for jdbc:flink://localhost:8083:
0: jdbc:flink://localhost:8083>

```

`sqlline version 1.13.0-SNAPSHOT
sqlline> !connect jdbc:flink://localhost:8083
Enter username for jdbc:flink://localhost:8083:
Enter password for jdbc:flink://localhost:8083:
0: jdbc:flink://localhost:8083>
`

You can now execute any Flink SQL statement you want.


Sample Commands


```
0: jdbc:flink://localhost:8083> CREATE TABLE T(
. . . . . . . . . . . . . . .)>      a INT,
. . . . . . . . . . . . . . .)>      b VARCHAR(10)
. . . . . . . . . . . . . . .)>  ) WITH (
. . . . . . . . . . . . . . .)>      'connector' = 'filesystem',
. . . . . . . . . . . . . . .)>      'path' = 'file:///tmp/T.csv',
. . . . . . . . . . . . . . .)>      'format' = 'csv'
. . . . . . . . . . . . . . .)>  );
No rows affected (0.122 seconds)

0: jdbc:flink://localhost:8083> INSERT INTO T VALUES (1, 'Hi'), (2, 'Hello');
+----------------------------------+
|              job id              |
+----------------------------------+
| fbade1ab4450fc57ebd5269fdf60dcfd |
+----------------------------------+
1 row selected (1.282 seconds)

0: jdbc:flink://localhost:8083> SELECT * FROM T;
+---+-------+
| a |   b   |
+---+-------+
| 1 | Hi    |
| 2 | Hello |
+---+-------+
2 rows selected (1.955 seconds)
0: jdbc:flink://localhost:8083>

```

`0: jdbc:flink://localhost:8083> CREATE TABLE T(
. . . . . . . . . . . . . . .)>      a INT,
. . . . . . . . . . . . . . .)>      b VARCHAR(10)
. . . . . . . . . . . . . . .)>  ) WITH (
. . . . . . . . . . . . . . .)>      'connector' = 'filesystem',
. . . . . . . . . . . . . . .)>      'path' = 'file:///tmp/T.csv',
. . . . . . . . . . . . . . .)>      'format' = 'csv'
. . . . . . . . . . . . . . .)>  );
No rows affected (0.122 seconds)

0: jdbc:flink://localhost:8083> INSERT INTO T VALUES (1, 'Hi'), (2, 'Hello');
+----------------------------------+
|              job id              |
+----------------------------------+
| fbade1ab4450fc57ebd5269fdf60dcfd |
+----------------------------------+
1 row selected (1.282 seconds)

0: jdbc:flink://localhost:8083> SELECT * FROM T;
+---+-------+
| a |   b   |
+---+-------+
| 1 | Hi    |
| 2 | Hello |
+---+-------+
2 rows selected (1.955 seconds)
0: jdbc:flink://localhost:8083>
`

### Tableau#


Tableau is an interactive data visualization software. It supports Other Database (JDBC) connection from version 2018.3. You’ll need Tableau with version >= 2018.3 to use Flink JDBC driver. For general usage of Other Database (JDBC) in Tableau, see Tableau documentation.

1. Download flink-jdbc-driver-(VERSION).jar from the download page and add it to Tableau driver path.

Windows: C:\Program Files\Tableau\Drivers
Mac: ~/Library/Tableau/Drivers
Linux: /opt/tableau/tableau_driver/jdbc


2. Select Other Database (JDBC) under Connect and fill in the url of Flink SQL gateway. Select SQL92 dialect and leave user name and password empty.
3. Hit Login button and use Tableau as usual.
* Windows: C:\Program Files\Tableau\Drivers
* Mac: ~/Library/Tableau/Drivers
* Linux: /opt/tableau/tableau_driver/jdbc
`C:\Program Files\Tableau\Drivers`
`~/Library/Tableau/Drivers`
`/opt/tableau/tableau_driver/jdbc`

### Use with other JDBC Tools#


Any tool supporting JDBC API can be used with Flink JDBC driver and Flink SQL gateway. See the documentation of your desired tool on how to use a custom JDBC driver.


## Use with Application#


### Java#


The Flink JDBC driver is a library for accessing Flink clusters through the JDBC API. For the general usage of JDBC in Java, see JDBC tutorial.

1. Add the following dependency in pom.xml of project or download flink-jdbc-driver-bundle-{VERSION}.jar and add it to your classpath.
2. Connect to a Flink SQL gateway in your Java code with specific url.
3. Execute any statement you want.

Sample.java


```
public class Sample {
	public static void main(String[] args) throws Exception {
		try (Connection connection = DriverManager.getConnection("jdbc:flink://localhost:8083")) {
			try (Statement statement = connection.createStatement()) {
				statement.execute("CREATE TABLE T(\n" +
						"  a INT,\n" +
						"  b VARCHAR(10)\n" +
						") WITH (\n" +
						"  'connector' = 'filesystem',\n" +
						"  'path' = 'file:///tmp/T.csv',\n" +
						"  'format' = 'csv'\n" +
						")");
				statement.execute("INSERT INTO T VALUES (1, 'Hi'), (2, 'Hello')");
				try (ResultSet rs = statement.executeQuery("SELECT * FROM T")) {
					while (rs.next()) {
						System.out.println(rs.getInt(1) + ", " + rs.getString(2));
					}
				}
			}
		}
	}
}

```

`public class Sample {
	public static void main(String[] args) throws Exception {
		try (Connection connection = DriverManager.getConnection("jdbc:flink://localhost:8083")) {
			try (Statement statement = connection.createStatement()) {
				statement.execute("CREATE TABLE T(\n" +
						"  a INT,\n" +
						"  b VARCHAR(10)\n" +
						") WITH (\n" +
						"  'connector' = 'filesystem',\n" +
						"  'path' = 'file:///tmp/T.csv',\n" +
						"  'format' = 'csv'\n" +
						")");
				statement.execute("INSERT INTO T VALUES (1, 'Hi'), (2, 'Hello')");
				try (ResultSet rs = statement.executeQuery("SELECT * FROM T")) {
					while (rs.next()) {
						System.out.println(rs.getInt(1) + ", " + rs.getString(2));
					}
				}
			}
		}
	}
}
`

Output


```
1, Hi
2, Hello

```

`1, Hi
2, Hello
`

Besides DriverManager, Flink JDBC driver supports DataSource and you can also create connection from it.

`DriverManager`
`DataSource`

DataSource.java


```
public class Sample {
	public static void main(String[] args) throws Exception {
		DataSource dataSource = new FlinkDataSource("jdbc:flink://localhost:8083", new Properties());
		try (Connection connection = dataSource.getConnection()) {
			try (Statement statement = connection.createStatement()) {
				statement.execute("CREATE TABLE T(\n" +
						"  a INT,\n" +
						"  b VARCHAR(10)\n" +
						") WITH (\n" +
						"  'connector' = 'filesystem',\n" +
						"  'path' = 'file:///tmp/T.csv',\n" +
						"  'format' = 'csv'\n" +
						")");
				statement.execute("INSERT INTO T VALUES (1, 'Hi'), (2, 'Hello')");
				try (ResultSet rs = statement.executeQuery("SELECT * FROM T")) {
					while (rs.next()) {
						System.out.println(rs.getInt(1) + ", " + rs.getString(2));
					}
				}
			}
		}
	}
}

```

`public class Sample {
	public static void main(String[] args) throws Exception {
		DataSource dataSource = new FlinkDataSource("jdbc:flink://localhost:8083", new Properties());
		try (Connection connection = dataSource.getConnection()) {
			try (Statement statement = connection.createStatement()) {
				statement.execute("CREATE TABLE T(\n" +
						"  a INT,\n" +
						"  b VARCHAR(10)\n" +
						") WITH (\n" +
						"  'connector' = 'filesystem',\n" +
						"  'path' = 'file:///tmp/T.csv',\n" +
						"  'format' = 'csv'\n" +
						")");
				statement.execute("INSERT INTO T VALUES (1, 'Hi'), (2, 'Hello')");
				try (ResultSet rs = statement.executeQuery("SELECT * FROM T")) {
					while (rs.next()) {
						System.out.println(rs.getInt(1) + ", " + rs.getString(2));
					}
				}
			}
		}
	}
}
`

### Other languages#


In addition to Java, the Flink JDBC driver can be used by any JVM language such as Scala, Kotlin etc. Add the dependency of Flink JDBC driver in your project and use it directly.


Many applications access data in SQL databases, either directly, or through frameworks like JOOQ, MyBatis, and Spring Data. You can configure these applications and frameworks to use the Flink JDBC driver so that they perform SQL queries on a Flink cluster instead of a regular database.
