# Common Configurations


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Common Configurations#


Apache Flink provides several standard configuration settings that work across all file system implementations.


## Default File System#


A default scheme (and authority) is used if paths to files do not explicitly specify a file system scheme (and authority).


```
fs.default-scheme: <default-fs>

```

`fs.default-scheme: <default-fs>
`

For example, if the default file system configured as fs.default-scheme: hdfs://localhost:9000/, then a file path of
/user/hugo/in.txt is interpreted as hdfs://localhost:9000/user/hugo/in.txt.

`fs.default-scheme: hdfs://localhost:9000/`
`/user/hugo/in.txt`
`hdfs://localhost:9000/user/hugo/in.txt`

## Connection limiting#


You can limit the total number of connections that a file system can concurrently open which is useful when the file system cannot handle a large number
of concurrent reads/writes or open connections at the same time.


For example, small HDFS clusters with few RPC handlers can sometimes be overwhelmed by a large Flink job trying to build up many connections during a checkpoint.


To limit a specific file system’s connections, add the following entries to the Flink configuration. The file system to be limited is identified by
its scheme.


```
fs.<scheme>.limit.total: (number, 0/-1 mean no limit)
fs.<scheme>.limit.input: (number, 0/-1 mean no limit)
fs.<scheme>.limit.output: (number, 0/-1 mean no limit)
fs.<scheme>.limit.timeout: (milliseconds, 0 means infinite)
fs.<scheme>.limit.stream-timeout: (milliseconds, 0 means infinite)

```

`fs.<scheme>.limit.total: (number, 0/-1 mean no limit)
fs.<scheme>.limit.input: (number, 0/-1 mean no limit)
fs.<scheme>.limit.output: (number, 0/-1 mean no limit)
fs.<scheme>.limit.timeout: (milliseconds, 0 means infinite)
fs.<scheme>.limit.stream-timeout: (milliseconds, 0 means infinite)
`

You can limit the number of input/output connections (streams) separately (fs.<scheme>.limit.input and fs.<scheme>.limit.output), as well as impose a limit on
the total number of concurrent streams (fs.<scheme>.limit.total). If the file system tries to open more streams, the operation blocks until some streams close.
If the opening of the stream takes longer than fs.<scheme>.limit.timeout, the stream opening fails.

`fs.<scheme>.limit.input`
`fs.<scheme>.limit.output`
`fs.<scheme>.limit.total`
`fs.<scheme>.limit.timeout`

To prevent inactive streams from taking up the full pool (preventing new connections to be opened), you can add an inactivity timeout which forcibly closes them if they do not read/write any bytes for at least that amount of time: fs.<scheme>.limit.stream-timeout.

`fs.<scheme>.limit.stream-timeout`

Limit enforcement on a per TaskManager/file system basis.
Because file systems creation occurs per scheme and authority, different
authorities have independent connection pools. For example hdfs://myhdfs:50010/ and hdfs://anotherhdfs:4399/ will have separate pools.

`hdfs://myhdfs:50010/`
`hdfs://anotherhdfs:4399/`

 Back to top
