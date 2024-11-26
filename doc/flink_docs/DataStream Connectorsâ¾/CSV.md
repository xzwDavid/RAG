# CSV


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# CSV format#


To use the CSV format you need to add the Flink CSV dependency to your project:


```
<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-csv</artifactId>
	<version>2.0-SNAPSHOT</version>
</dependency>

```

`<dependency>
	<groupId>org.apache.flink</groupId>
	<artifactId>flink-csv</artifactId>
	<version>2.0-SNAPSHOT</version>
</dependency>
`

For PyFlink users, you could use it directly in your jobs.


Flink supports reading CSV files using CsvReaderFormat. The reader utilizes Jackson library and allows passing the corresponding configuration for the CSV schema and parsing options.

`CsvReaderFormat`

CsvReaderFormat can be initialized and used like this:

`CsvReaderFormat`

```
CsvReaderFormat<SomePojo> csvFormat = CsvReaderFormat.forPojo(SomePojo.class);
FileSource<SomePojo> source = 
        FileSource.forRecordStreamFormat(csvFormat, Path.fromLocalFile(...)).build();

```

`CsvReaderFormat<SomePojo> csvFormat = CsvReaderFormat.forPojo(SomePojo.class);
FileSource<SomePojo> source = 
        FileSource.forRecordStreamFormat(csvFormat, Path.fromLocalFile(...)).build();
`

The schema for CSV parsing, in this case, is automatically derived based on the fields of the SomePojo class using the Jackson library.

`SomePojo`
`Jackson`

> 
  Note: you might need to add @JsonPropertyOrder({field1, field2, ...}) annotation to your class definition with the fields order exactly matching those of the CSV file columns.


`@JsonPropertyOrder({field1, field2, ...})`

### Advanced configuration#


If you need more fine-grained control over the CSV schema or the parsing options, use the more low-level forSchema static factory method of CsvReaderFormat:

`forSchema`
`CsvReaderFormat`

```
CsvReaderFormat<T> forSchema(Supplier<CsvMapper> mapperFactory, 
                             Function<CsvMapper, CsvSchema> schemaGenerator, 
                             TypeInformation<T> typeInformation) 

```

`CsvReaderFormat<T> forSchema(Supplier<CsvMapper> mapperFactory, 
                             Function<CsvMapper, CsvSchema> schemaGenerator, 
                             TypeInformation<T> typeInformation) 
`

Below is an example of reading a POJO with a custom columns’ separator:


```
//Has to match the exact order of columns in the CSV file
@JsonPropertyOrder({"city","lat","lng","country","iso2",
                    "adminName","capital","population"})
    public static class CityPojo {
    public String city;
    public BigDecimal lat;
    public BigDecimal lng;
    public String country;
    public String iso2;
    public String adminName;
    public String capital;
    public long population;
}

Function<CsvMapper, CsvSchema> schemaGenerator = mapper ->
        mapper.schemaFor(CityPojo.class).withoutQuoteChar().withColumnSeparator('|');

CsvReaderFormat<CityPojo> csvFormat =
        CsvReaderFormat.forSchema(() -> new CsvMapper(), schemaGenerator, TypeInformation.of(CityPojo.class));

FileSource<CityPojo> source =
        FileSource.forRecordStreamFormat(csvFormat, Path.fromLocalFile(...)).build();

```

`//Has to match the exact order of columns in the CSV file
@JsonPropertyOrder({"city","lat","lng","country","iso2",
                    "adminName","capital","population"})
    public static class CityPojo {
    public String city;
    public BigDecimal lat;
    public BigDecimal lng;
    public String country;
    public String iso2;
    public String adminName;
    public String capital;
    public long population;
}

Function<CsvMapper, CsvSchema> schemaGenerator = mapper ->
        mapper.schemaFor(CityPojo.class).withoutQuoteChar().withColumnSeparator('|');

CsvReaderFormat<CityPojo> csvFormat =
        CsvReaderFormat.forSchema(() -> new CsvMapper(), schemaGenerator, TypeInformation.of(CityPojo.class));

FileSource<CityPojo> source =
        FileSource.forRecordStreamFormat(csvFormat, Path.fromLocalFile(...)).build();
`

The corresponding CSV file:


```
Berlin|52.5167|13.3833|Germany|DE|Berlin|primary|3644826
San Francisco|37.7562|-122.443|United States|US|California||3592294
Beijing|39.905|116.3914|China|CN|Beijing|primary|19433000

```

`Berlin|52.5167|13.3833|Germany|DE|Berlin|primary|3644826
San Francisco|37.7562|-122.443|United States|US|California||3592294
Beijing|39.905|116.3914|China|CN|Beijing|primary|19433000
`

It is also possible to read more complex data types using fine-grained Jackson settings:

`Jackson`

```
public static class ComplexPojo {
    private long id;
    private int[] array;
}

CsvReaderFormat<ComplexPojo> csvFormat =
        CsvReaderFormat.forSchema(
                CsvSchema.builder()
                        .addColumn(
                                new CsvSchema.Column(0, "id", CsvSchema.ColumnType.NUMBER))
                        .addColumn(
                                new CsvSchema.Column(4, "array", CsvSchema.ColumnType.ARRAY)
                                        .withArrayElementSeparator("#"))
                        .build(),
                TypeInformation.of(ComplexPojo.class));

```

`public static class ComplexPojo {
    private long id;
    private int[] array;
}

CsvReaderFormat<ComplexPojo> csvFormat =
        CsvReaderFormat.forSchema(
                CsvSchema.builder()
                        .addColumn(
                                new CsvSchema.Column(0, "id", CsvSchema.ColumnType.NUMBER))
                        .addColumn(
                                new CsvSchema.Column(4, "array", CsvSchema.ColumnType.ARRAY)
                                        .withArrayElementSeparator("#"))
                        .build(),
                TypeInformation.of(ComplexPojo.class));
`

For PyFlink users, a csv schema can be defined by manually adding columns, and the output type of the csv source will be a Row with each column mapped to a field.


```
schema = CsvSchema.builder() \
    .add_number_column('id', number_type=DataTypes.BIGINT()) \
    .add_array_column('array', separator='#', element_type=DataTypes.INT()) \
    .set_column_separator(',') \
    .build()

source = FileSource.for_record_stream_format(
    CsvReaderFormat.for_schema(schema), CSV_FILE_PATH).build()

# the type of record will be Types.ROW_NAMED(['id', 'array'], [Types.LONG(), Types.LIST(Types.INT())])
ds = env.from_source(source, WatermarkStrategy.no_watermarks(), 'csv-source')

```

`schema = CsvSchema.builder() \
    .add_number_column('id', number_type=DataTypes.BIGINT()) \
    .add_array_column('array', separator='#', element_type=DataTypes.INT()) \
    .set_column_separator(',') \
    .build()

source = FileSource.for_record_stream_format(
    CsvReaderFormat.for_schema(schema), CSV_FILE_PATH).build()

# the type of record will be Types.ROW_NAMED(['id', 'array'], [Types.LONG(), Types.LIST(Types.INT())])
ds = env.from_source(source, WatermarkStrategy.no_watermarks(), 'csv-source')
`

The corresponding CSV file:


```
0,1#2#3
1,
2,1

```

`0,1#2#3
1,
2,1
`

Similarly to the TextLineInputFormat, CsvReaderFormat can be used in both continues and batch modes (see TextLineInputFormat  for examples).

`TextLineInputFormat`
`CsvReaderFormat`

For PyFlink users, CsvBulkWriters could be used to create BulkWriterFactory to write records to files in CSV format.

`CsvBulkWriters`
`BulkWriterFactory`

```
schema = CsvSchema.builder() \
    .add_number_column('id', number_type=DataTypes.BIGINT()) \
    .add_array_column('array', separator='#', element_type=DataTypes.INT()) \
    .set_column_separator(',') \
    .build()

sink = FileSink.for_bulk_format(
    OUTPUT_DIR, CsvBulkWriters.for_schema(schema)).build()

ds.sink_to(sink)

```

`schema = CsvSchema.builder() \
    .add_number_column('id', number_type=DataTypes.BIGINT()) \
    .add_array_column('array', separator='#', element_type=DataTypes.INT()) \
    .set_column_separator(',') \
    .build()

sink = FileSink.for_bulk_format(
    OUTPUT_DIR, CsvBulkWriters.for_schema(schema)).build()

ds.sink_to(sink)
`