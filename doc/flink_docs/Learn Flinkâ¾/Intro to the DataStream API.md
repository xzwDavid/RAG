# Intro to the DataStream API


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Intro to the DataStream API#


The focus of this training is to broadly cover the DataStream API well enough that you will be able
to get started writing streaming applications.


## What can be Streamed?#


Flink’s DataStream APIs will let you stream anything they can serialize. Flink’s
own serializer is used for

* basic types, i.e., String, Long, Integer, Boolean, Array
* composite types: Tuples, POJOs, and Scala case classes

and Flink falls back to Kryo for other types. It is also possible to use other serializers with
Flink. Avro, in particular, is well supported.


### Java tuples and POJOs#


Flink’s native serializer can operate efficiently on tuples and POJOs.


#### Tuples#


For Java, Flink defines its own Tuple0 thru Tuple25 types.

`Tuple0`
`Tuple25`

```
Tuple2<String, Integer> person = Tuple2.of("Fred", 35);

// zero based index!  
String name = person.f0;
Integer age = person.f1;

```

`Tuple2<String, Integer> person = Tuple2.of("Fred", 35);

// zero based index!  
String name = person.f0;
Integer age = person.f1;
`

#### POJOs#


Flink recognizes a data type as a POJO type (and allows âby-nameâ field referencing) if the following conditions are fulfilled:

* The class is public and standalone (no non-static inner class)
* The class has a public no-argument constructor
* All non-static, non-transient fields in the class (and all superclasses) are either public (and
non-final) or have public getter- and setter- methods that follow the Java beans naming
conventions for getters and setters.

Example:


```
public class Person {
    public String name;  
    public Integer age;  
    public Person() {}
    public Person(String name, Integer age) {  
        . . .
    }
}  

Person person = new Person("Fred Flintstone", 35);

```

`public class Person {
    public String name;  
    public Integer age;  
    public Person() {}
    public Person(String name, Integer age) {  
        . . .
    }
}  

Person person = new Person("Fred Flintstone", 35);
`

Flink’s serializer supports schema evolution for POJO types.


### Scala tuples and case classes#


These work just as you’d expect.


> 
All Flink Scala APIs are deprecated and will be removed in a future Flink version. You can still build your application in Scala, but you should move to the Java version of either the DataStream and/or Table API.
See FLIP-265 Deprecate and remove Scala API support



All Flink Scala APIs are deprecated and will be removed in a future Flink version. You can still build your application in Scala, but you should move to the Java version of either the DataStream and/or Table API.


See FLIP-265 Deprecate and remove Scala API support


 Back to top


## A Complete Example#


This example takes a stream of records about people as input, and filters it to only include the adults.


```
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.functions.FilterFunction;

public class Example {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<Person> flintstones = env.fromElements(
                new Person("Fred", 35),
                new Person("Wilma", 35),
                new Person("Pebbles", 2));

        DataStream<Person> adults = flintstones.filter(new FilterFunction<Person>() {
            @Override
            public boolean filter(Person person) throws Exception {
                return person.age >= 18;
            }
        });

        adults.print();

        env.execute();
    }

    public static class Person {
        public String name;
        public Integer age;
        public Person() {}

        public Person(String name, Integer age) {
            this.name = name;
            this.age = age;
        }

        public String toString() {
            return this.name.toString() + ": age " + this.age.toString();
        }
    }
}

```

`import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.functions.FilterFunction;

public class Example {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<Person> flintstones = env.fromElements(
                new Person("Fred", 35),
                new Person("Wilma", 35),
                new Person("Pebbles", 2));

        DataStream<Person> adults = flintstones.filter(new FilterFunction<Person>() {
            @Override
            public boolean filter(Person person) throws Exception {
                return person.age >= 18;
            }
        });

        adults.print();

        env.execute();
    }

    public static class Person {
        public String name;
        public Integer age;
        public Person() {}

        public Person(String name, Integer age) {
            this.name = name;
            this.age = age;
        }

        public String toString() {
            return this.name.toString() + ": age " + this.age.toString();
        }
    }
}
`

### Stream execution environment#


Every Flink application needs an execution environment, env in this example. Streaming
applications need to use a StreamExecutionEnvironment.

`env`
`StreamExecutionEnvironment`

The DataStream API calls made in your application build a job graph that is attached to the
StreamExecutionEnvironment. When env.execute() is called this graph is packaged up and sent to
the JobManager, which parallelizes the job and distributes slices of it to the Task Managers for
execution. Each parallel slice of your job will be executed in a task slot.

`StreamExecutionEnvironment`
`env.execute()`

Note that if you don’t call execute(), your application won’t be run.


This distributed runtime depends on your application being serializable. It also requires that all
dependencies are available to each node in the cluster.


### Basic stream sources#


The example above constructs a DataStream<Person> using env.fromElements(...). This is a
convenient way to throw together a simple stream for use in a prototype or test. There is also a
fromCollection(Collection) method on StreamExecutionEnvironment. So instead, you could do this:

`DataStream<Person>`
`env.fromElements(...)`
`fromCollection(Collection)`
`StreamExecutionEnvironment`

```
List<Person> people = new ArrayList<Person>();

people.add(new Person("Fred", 35));
people.add(new Person("Wilma", 35));
people.add(new Person("Pebbles", 2));

DataStream<Person> flintstones = env.fromCollection(people);

```

`List<Person> people = new ArrayList<Person>();

people.add(new Person("Fred", 35));
people.add(new Person("Wilma", 35));
people.add(new Person("Pebbles", 2));

DataStream<Person> flintstones = env.fromCollection(people);
`

Another convenient way to get some data into a stream while prototyping is to use a socket


```
DataStream<String> lines = env.socketTextStream("localhost", 9999);

```

`DataStream<String> lines = env.socketTextStream("localhost", 9999);
`

or a file


```
DataStream<String> lines = env.readTextFile("file:///path");

```

`DataStream<String> lines = env.readTextFile("file:///path");
`

In real applications the most commonly used data sources are those that support low-latency, high
throughput parallel reads in combination with rewind and replay – the prerequisites for high
performance and fault tolerance – such as Apache Kafka, Kinesis, and various filesystems. REST APIs
and databases are also frequently used for stream enrichment.


### Basic stream sinks#


The example above uses adults.print() to print its results to the task manager logs (which will
appear in your IDE’s console, when running in an IDE). This will call toString() on each element
of the stream.

`adults.print()`
`toString()`

The output looks something like this


```
1> Fred: age 35
2> Wilma: age 35

```

`1> Fred: age 35
2> Wilma: age 35
`

where 1> and 2> indicate which sub-task (i.e., thread) produced the output.


In production, commonly used sinks include the FileSink, various databases,
and several pub-sub systems.


### Debugging#


In production, your application will run in a remote cluster or set of containers. And if it fails,
it will fail remotely. The JobManager and TaskManager logs can be very helpful in debugging such
failures, but it is much easier to do local debugging inside an IDE, which is something that Flink
supports. You can set breakpoints, examine local variables, and step through your code. You can also
step into Flink’s code, which can be a great way to learn more about its internals if you are
curious to see how Flink works.


 Back to top


## Hands-on#


At this point you know enough to get started coding and running a simple DataStream application.
Clone the 

    flink-training-repo


, and after following the
instructions in the README, do the first exercise: 

    Filtering a Stream (Ride Cleansing)

.


 Back to top


## Further Reading#

* Flink Serialization Tuning Vol. 1: Choosing your Serializer â if you can
* Anatomy of a Flink Program
* Data Sources
* Data Sinks
* DataStream Connectors

 Back to top
