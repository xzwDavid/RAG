# 3rd Party Serializers


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# 3rd Party Serializers#


If you use a custom type in your Flink program which cannot be serialized by the
Flink type serializer, Flink falls back to using the generic Kryo
serializer. You may register your own serializer or a serialization system like
Google Protobuf or Apache Thrift with Kryo. To do that, simply register the type
class and the serializer via the configuration option
pipeline.serialization-config:


```
pipeline.serialization-config:
  - org.example.MyCustomType: {type: kryo, kryo-type: registered, class: org.example.MyCustomSerializer}

```

`pipeline.serialization-config:
  - org.example.MyCustomType: {type: kryo, kryo-type: registered, class: org.example.MyCustomSerializer}
`

You could also programmatically set it as follows:


```
Configuration config = new Configuration();

// register the class of the serializer as serializer for a type
config.set(PipelineOptions.SERIALIZATION_CONFIG, 
    "[org.example.MyCustomType: {type: kryo, kryo-type: registered, class: org.example.MyCustomSerializer}]");

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);

```

`Configuration config = new Configuration();

// register the class of the serializer as serializer for a type
config.set(PipelineOptions.SERIALIZATION_CONFIG, 
    "[org.example.MyCustomType: {type: kryo, kryo-type: registered, class: org.example.MyCustomSerializer}]");

StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment(config);
`

Note that your custom serializer has to extend Kryo’s Serializer class. In the
case of Google Protobuf or Apache Thrift, this has already been done for
you.


```
pipeline.serialization-config:
# register the Google Protobuf serializer with Kryo
  - org.example.MyCustomProtobufType: {type: kryo, kryo-type: registered, class: com.twitter.chill.protobuf.ProtobufSerializer}
# register the serializer included with Apache Thrift as the standard serializer
# TBaseSerializer states it should be initialized as a default Kryo serializer
  - org.example.MyCustomThriftType: {type: kryo, kryo-type: default, class: com.twitter.chill.thrift.TBaseSerializer}

```

`pipeline.serialization-config:
# register the Google Protobuf serializer with Kryo
  - org.example.MyCustomProtobufType: {type: kryo, kryo-type: registered, class: com.twitter.chill.protobuf.ProtobufSerializer}
# register the serializer included with Apache Thrift as the standard serializer
# TBaseSerializer states it should be initialized as a default Kryo serializer
  - org.example.MyCustomThriftType: {type: kryo, kryo-type: default, class: com.twitter.chill.thrift.TBaseSerializer}
`

For the above example to work, you need to include the necessary dependencies in
your Maven project file (pom.xml). In the dependency section, add the following
for Apache Thrift:


```

<dependency>
	<groupId>com.twitter</groupId>
	<artifactId>chill-thrift</artifactId>
	<version>0.7.6</version>
	<!-- exclusions for dependency conversion -->
	<exclusions>
		<exclusion>
			<groupId>com.esotericsoftware.kryo</groupId>
			<artifactId>kryo</artifactId>
		</exclusion>
	</exclusions>
</dependency>
<!-- libthrift is required by chill-thrift -->
<dependency>
	<groupId>org.apache.thrift</groupId>
	<artifactId>libthrift</artifactId>
	<version>0.11.0</version>
	<exclusions>
		<exclusion>
			<groupId>javax.servlet</groupId>
			<artifactId>servlet-api</artifactId>
		</exclusion>
		<exclusion>
			<groupId>org.apache.httpcomponents</groupId>
			<artifactId>httpclient</artifactId>
		</exclusion>
	</exclusions>
</dependency>

```

`
<dependency>
	<groupId>com.twitter</groupId>
	<artifactId>chill-thrift</artifactId>
	<version>0.7.6</version>
	<!-- exclusions for dependency conversion -->
	<exclusions>
		<exclusion>
			<groupId>com.esotericsoftware.kryo</groupId>
			<artifactId>kryo</artifactId>
		</exclusion>
	</exclusions>
</dependency>
<!-- libthrift is required by chill-thrift -->
<dependency>
	<groupId>org.apache.thrift</groupId>
	<artifactId>libthrift</artifactId>
	<version>0.11.0</version>
	<exclusions>
		<exclusion>
			<groupId>javax.servlet</groupId>
			<artifactId>servlet-api</artifactId>
		</exclusion>
		<exclusion>
			<groupId>org.apache.httpcomponents</groupId>
			<artifactId>httpclient</artifactId>
		</exclusion>
	</exclusions>
</dependency>
`

For Google Protobuf you need the following Maven dependency:


```

<dependency>
	<groupId>com.twitter</groupId>
	<artifactId>chill-protobuf</artifactId>
	<version>0.7.6</version>
	<!-- exclusions for dependency conversion -->
	<exclusions>
		<exclusion>
			<groupId>com.esotericsoftware.kryo</groupId>
			<artifactId>kryo</artifactId>
		</exclusion>
	</exclusions>
</dependency>
<!-- We need protobuf for chill-protobuf -->
<dependency>
	<groupId>com.google.protobuf</groupId>
	<artifactId>protobuf-java</artifactId>
	<version>3.7.0</version>
</dependency>

```

`
<dependency>
	<groupId>com.twitter</groupId>
	<artifactId>chill-protobuf</artifactId>
	<version>0.7.6</version>
	<!-- exclusions for dependency conversion -->
	<exclusions>
		<exclusion>
			<groupId>com.esotericsoftware.kryo</groupId>
			<artifactId>kryo</artifactId>
		</exclusion>
	</exclusions>
</dependency>
<!-- We need protobuf for chill-protobuf -->
<dependency>
	<groupId>com.google.protobuf</groupId>
	<artifactId>protobuf-java</artifactId>
	<version>3.7.0</version>
</dependency>
`

Please adjust the versions of both libraries as needed.


### Issue with using Kryo’sJavaSerializer#

`JavaSerializer`

If you register Kryo’s JavaSerializer for your custom type, you may
encounter ClassNotFoundExceptions even though your custom type class is
included in the submitted user code jar. This is due to a know issue with
Kryo’s JavaSerializer, which may incorrectly use the wrong classloader.

`JavaSerializer`
`ClassNotFoundException`
`JavaSerializer`

In this case, you should use org.apache.flink.api.java.typeutils.runtime.kryo.JavaSerializer
instead to resolve the issue. This is a reimplemented JavaSerializer in Flink
that makes sure the user code classloader is used.

`org.apache.flink.api.java.typeutils.runtime.kryo.JavaSerializer`
`JavaSerializer`

Please refer to FLINK-6025
for more details.


 Back to top
