# History Server


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# History Server#


Flink has a history server that can be used to query the statistics of completed jobs after the corresponding Flink cluster has been shut down.


Furthermore, it exposes a REST API that accepts HTTP requests and responds with JSON data.


## Overview#


The HistoryServer allows you to query the status and statistics of completed jobs that have been archived by a JobManager.


After you have configured the HistoryServer and JobManager, you start and stop the HistoryServer via its corresponding startup script:


```
# Start or stop the HistoryServer
bin/historyserver.sh (start|start-foreground|stop)

```

`# Start or stop the HistoryServer
bin/historyserver.sh (start|start-foreground|stop)
`

By default, this server binds to localhost and listens at port 8082.

`localhost`
`8082`

Currently, you can only run it as a standalone process.


## Configuration#


The configuration keys jobmanager.archive.fs.dir and historyserver.archive.fs.refresh-interval need to be adjusted for archiving and displaying archived jobs.

`jobmanager.archive.fs.dir`
`historyserver.archive.fs.refresh-interval`

JobManager


The archiving of completed jobs happens on the JobManager, which uploads the archived job information to a file system directory. You can configure the directory to archive completed jobs in Flink configuration file by setting a directory via jobmanager.archive.fs.dir.

`jobmanager.archive.fs.dir`

```
# Directory to upload completed job information
jobmanager.archive.fs.dir: hdfs:///completed-jobs

```

`# Directory to upload completed job information
jobmanager.archive.fs.dir: hdfs:///completed-jobs
`

HistoryServer


The HistoryServer can be configured to monitor a comma-separated list of directories in via historyserver.archive.fs.dir. The configured directories are regularly polled for new archives; the polling interval can be configured via historyserver.archive.fs.refresh-interval.

`historyserver.archive.fs.dir`
`historyserver.archive.fs.refresh-interval`

```
# Monitor the following directories for completed jobs
historyserver.archive.fs.dir: hdfs:///completed-jobs

# Refresh every 10 seconds
historyserver.archive.fs.refresh-interval: 10000

```

`# Monitor the following directories for completed jobs
historyserver.archive.fs.dir: hdfs:///completed-jobs

# Refresh every 10 seconds
historyserver.archive.fs.refresh-interval: 10000
`

The contained archives are downloaded and cached in the local filesystem. The local directory for this is configured via historyserver.web.tmpdir.

`historyserver.web.tmpdir`

Check out the configuration page for a complete list of configuration options.


## Log Integration#


Flink does not provide built-in methods for archiving logs of completed jobs.
However, if you already have log archiving and browsing services, you can configure HistoryServer to integrate them
(via historyserver.log.jobmanager.url-pattern
and historyserver.log.taskmanager.url-pattern).
In this way, you can directly link from HistoryServer WebUI to logs of the relevant JobManager / TaskManagers.

`historyserver.log.jobmanager.url-pattern`
`historyserver.log.taskmanager.url-pattern`

```
# HistoryServer will replace <jobid> with the relevant job id
historyserver.log.jobmanager.url-pattern: http://my.log-browsing.url/<jobid>

# HistoryServer will replace <jobid> and <tmid> with the relevant job id and taskmanager id
historyserver.log.taskmanager.url-pattern: http://my.log-browsing.url/<jobid>/<tmid>

```

`# HistoryServer will replace <jobid> with the relevant job id
historyserver.log.jobmanager.url-pattern: http://my.log-browsing.url/<jobid>

# HistoryServer will replace <jobid> and <tmid> with the relevant job id and taskmanager id
historyserver.log.taskmanager.url-pattern: http://my.log-browsing.url/<jobid>/<tmid>
`

## Available Requests#


Below is a list of available requests, with a sample JSON response. All requests are of the sample form http://hostname:8082/jobs, below we list only the path part of the URLs.

`http://hostname:8082/jobs`

Values in angle brackets are variables, for example http://hostname:port/jobs/<jobid>/exceptions will have to requested for example as http://hostname:port/jobs/7684be6004e4e955c2a558a9bc463f65/exceptions.

`http://hostname:port/jobs/<jobid>/exceptions`
`http://hostname:port/jobs/7684be6004e4e955c2a558a9bc463f65/exceptions`
* /config
* /jobs/overview
* /jobs/<jobid>
* /jobs/<jobid>/vertices
* /jobs/<jobid>/config
* /jobs/<jobid>/exceptions
* /jobs/<jobid>/accumulators
* /jobs/<jobid>/vertices/<vertexid>
* /jobs/<jobid>/vertices/<vertexid>/subtasktimes
* /jobs/<jobid>/vertices/<vertexid>/taskmanagers
* /jobs/<jobid>/vertices/<vertexid>/accumulators
* /jobs/<jobid>/vertices/<vertexid>/subtasks/accumulators
* /jobs/<jobid>/vertices/<vertexid>/subtasks/<subtasknum>
* /jobs/<jobid>/vertices/<vertexid>/subtasks/<subtasknum>/attempts/<attempt>
* /jobs/<jobid>/vertices/<vertexid>/subtasks/<subtasknum>/attempts/<attempt>/accumulators
* /jobs/<jobid>/plan
* /jobs/<jobid>/jobmanager/config
* /jobs/<jobid>/jobmanager/environment
* /jobs/<jobid>/jobmanager/log-url
* /jobs/<jobid>/taskmanagers/<taskmanagerid>/log-url
`/config`
`/jobs/overview`
`/jobs/<jobid>`
`/jobs/<jobid>/vertices`
`/jobs/<jobid>/config`
`/jobs/<jobid>/exceptions`
`/jobs/<jobid>/accumulators`
`/jobs/<jobid>/vertices/<vertexid>`
`/jobs/<jobid>/vertices/<vertexid>/subtasktimes`
`/jobs/<jobid>/vertices/<vertexid>/taskmanagers`
`/jobs/<jobid>/vertices/<vertexid>/accumulators`
`/jobs/<jobid>/vertices/<vertexid>/subtasks/accumulators`
`/jobs/<jobid>/vertices/<vertexid>/subtasks/<subtasknum>`
`/jobs/<jobid>/vertices/<vertexid>/subtasks/<subtasknum>/attempts/<attempt>`
`/jobs/<jobid>/vertices/<vertexid>/subtasks/<subtasknum>/attempts/<attempt>/accumulators`
`/jobs/<jobid>/plan`
`/jobs/<jobid>/jobmanager/config`
`/jobs/<jobid>/jobmanager/environment`
`/jobs/<jobid>/jobmanager/log-url`
`/jobs/<jobid>/taskmanagers/<taskmanagerid>/log-url`

 Back to top
