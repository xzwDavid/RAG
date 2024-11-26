# JSON


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Json format#


To use the JSON format you need to add the Flink JSON dependency to your project:


```
<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-json</artifactId>
	<version>2.0-SNAPSHOT</version>
	<scope>provided</scope>
</dependency>

```

`<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-json</artifactId>
	<version>2.0-SNAPSHOT</version>
	<scope>provided</scope>
</dependency>
`

For PyFlink users, you could use it directly in your jobs.


Flink supports reading/writing JSON records via the JsonSerializationSchema/JsonDeserializationSchema.
These utilize the Jackson library, and support any type that is supported by Jackson, including, but not limited to, POJOs and ObjectNode.

`JsonSerializationSchema/JsonDeserializationSchema`
`POJO`
`ObjectNode`

The JsonDeserializationSchema can be used with any connector that supports the DeserializationSchema.

`JsonDeserializationSchema`
`DeserializationSchema`

For example, this is how you use it with a KafkaSource to deserialize a POJO:

`KafkaSource`
`POJO`

```
JsonDeserializationSchema<SomePojo> jsonFormat=new JsonDeserializationSchema<>(SomePojo.class);
KafkaSource<SomePojo> source=
    KafkaSource.<SomePojo>builder()
        .setValueOnlyDeserializer(jsonFormat)
        ...

```

`JsonDeserializationSchema<SomePojo> jsonFormat=new JsonDeserializationSchema<>(SomePojo.class);
KafkaSource<SomePojo> source=
    KafkaSource.<SomePojo>builder()
        .setValueOnlyDeserializer(jsonFormat)
        ...
`

The JsonSerializationSchema can be used with any connector that supports the SerializationSchema.

`JsonSerializationSchema`
`SerializationSchema`

For example, this is how you use it with a KafkaSink to serialize a POJO:

`KafkaSink`
`POJO`

```
JsonSerializationSchema<SomePojo> jsonFormat=new JsonSerializationSchema<>();
KafkaSink<SomePojo> source  = 
    KafkaSink.<SomePojo>builder()
        .setRecordSerializer(
            new KafkaRecordSerializationSchemaBuilder<>()
                .setValueSerializationSchema(jsonFormat)
                ...

```

`JsonSerializationSchema<SomePojo> jsonFormat=new JsonSerializationSchema<>();
KafkaSink<SomePojo> source  = 
    KafkaSink.<SomePojo>builder()
        .setRecordSerializer(
            new KafkaRecordSerializationSchemaBuilder<>()
                .setValueSerializationSchema(jsonFormat)
                ...
`

## Custom Mapper#


Both schemas have constructors that accept a SerializableSupplier<ObjectMapper>, acting a factory for object mappers.
With this factory you gain full control over the created mapper, and can enable/disable various Jackson features or register modules to extend the set of supported types or add additional functionality.

`SerializableSupplier<ObjectMapper>`

```
JsonSerializationSchema<SomeClass> jsonFormat=new JsonSerializationSchema<>(
    () -> new ObjectMapper()
        .enable(SerializationFeature.ORDER_MAP_ENTRIES_BY_KEYS))
        .registerModule(new ParameterNamesModule());

```

`JsonSerializationSchema<SomeClass> jsonFormat=new JsonSerializationSchema<>(
    () -> new ObjectMapper()
        .enable(SerializationFeature.ORDER_MAP_ENTRIES_BY_KEYS))
        .registerModule(new ParameterNamesModule());
`

## Python#


In PyFlink, JsonRowSerializationSchema and JsonRowDeserializationSchema are built-in support for Row type.
For example to use it in KafkaSource and KafkaSink:

`JsonRowSerializationSchema`
`JsonRowDeserializationSchema`
`Row`
`KafkaSource`
`KafkaSink`

```
row_type_info = Types.ROW_NAMED(['name', 'age'], [Types.STRING(), Types.INT()])
json_format = JsonRowDeserializationSchema.builder().type_info(row_type_info).build()

source = KafkaSource.builder() \
    .set_value_only_deserializer(json_format) \
    .build()

```

`row_type_info = Types.ROW_NAMED(['name', 'age'], [Types.STRING(), Types.INT()])
json_format = JsonRowDeserializationSchema.builder().type_info(row_type_info).build()

source = KafkaSource.builder() \
    .set_value_only_deserializer(json_format) \
    .build()
`

```
row_type_info = Types.ROW_NAMED(['name', 'age'], [Types.STRING(), Types.INT()])
json_format = JsonRowSerializationSchema.builder().with_type_info(row_type_info).build()

sink = KafkaSink.builder() \
    .set_record_serializer(
        KafkaRecordSerializationSchema.builder()
            .set_topic('test')
            .set_value_serialization_schema(json_format)
            .build()
    ) \
    .build()

```

`row_type_info = Types.ROW_NAMED(['name', 'age'], [Types.STRING(), Types.INT()])
json_format = JsonRowSerializationSchema.builder().with_type_info(row_type_info).build()

sink = KafkaSink.builder() \
    .set_record_serializer(
        KafkaRecordSerializationSchema.builder()
            .set_topic('test')
            .set_value_serialization_schema(json_format)
            .build()
    ) \
    .build()
`