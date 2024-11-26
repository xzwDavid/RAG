# JOB Statements


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# JOB Statements#


Job statements are used for management of Flink jobs.


Flink SQL supports the following JOB statements for now:

* SHOW JOBS
* DESCRIBE JOB
* STOP JOB

## Run a JOB statement#

`JOB`

```
Flink SQL> SHOW JOBS;
+----------------------------------+----------+---------+-------------------------+
|                           job id | job name |  status |              start time |
+----------------------------------+----------+---------+-------------------------+
| 228d70913eab60dda85c5e7f78b5782c |    myjob | RUNNING | 2023-02-11T05:03:51.523 |
+----------------------------------+----------+---------+-------------------------+

Flink SQL> DESCRIBE JOB '228d70913eab60dda85c5e7f78b5782c';
+----------------------------------+----------+---------+-------------------------+
|                           job id | job name |  status |              start time |
+----------------------------------+----------+---------+-------------------------+
| 228d70913eab60dda85c5e7f78b5782c |    myjob | RUNNING | 2023-02-11T05:03:51.523 |
+----------------------------------+----------+---------+-------------------------+

Flink SQL> SET 'execution.checkpointing.savepoint-dir'='file:/tmp/';
[INFO] Execute statement succeeded.

Flink SQL> STOP JOB '228d70913eab60dda85c5e7f78b5782c' WITH SAVEPOINT;
+-----------------------------------------+
|                          savepoint path |
+-----------------------------------------+
| file:/tmp/savepoint-3addd4-0b224d9311e6 |
+-----------------------------------------+

```

`Flink SQL> SHOW JOBS;
+----------------------------------+----------+---------+-------------------------+
|                           job id | job name |  status |              start time |
+----------------------------------+----------+---------+-------------------------+
| 228d70913eab60dda85c5e7f78b5782c |    myjob | RUNNING | 2023-02-11T05:03:51.523 |
+----------------------------------+----------+---------+-------------------------+

Flink SQL> DESCRIBE JOB '228d70913eab60dda85c5e7f78b5782c';
+----------------------------------+----------+---------+-------------------------+
|                           job id | job name |  status |              start time |
+----------------------------------+----------+---------+-------------------------+
| 228d70913eab60dda85c5e7f78b5782c |    myjob | RUNNING | 2023-02-11T05:03:51.523 |
+----------------------------------+----------+---------+-------------------------+

Flink SQL> SET 'execution.checkpointing.savepoint-dir'='file:/tmp/';
[INFO] Execute statement succeeded.

Flink SQL> STOP JOB '228d70913eab60dda85c5e7f78b5782c' WITH SAVEPOINT;
+-----------------------------------------+
|                          savepoint path |
+-----------------------------------------+
| file:/tmp/savepoint-3addd4-0b224d9311e6 |
+-----------------------------------------+
`

## SHOW JOBS#


```
SHOW JOBS

```

`SHOW JOBS
`

Show the jobs in the Flink cluster.


Attention SHOW JOBS statements only work in SQL CLI or SQL Gateway.


## DESCRIBE JOB#


```
{ DESCRIBE | DESC } JOB '<job_id>'

```

`{ DESCRIBE | DESC } JOB '<job_id>'
`

Show the specified job in the Flink cluster.


Attention DESCRIBE JOB statements only work in SQL CLI or SQL Gateway.


## STOP JOB#


```
STOP JOB '<job_id>' [WITH SAVEPOINT] [WITH DRAIN]

```

`STOP JOB '<job_id>' [WITH SAVEPOINT] [WITH DRAIN]
`

Stop the specified job.


WITH SAVEPOINT
Perform a savepoint right before stopping the job. The savepoint path could be specified with
execution.checkpointing.savepoint-dir either in
the cluster configuration or via SET statements (the latter would take precedence).

`SET`

WITH DRAIN
Increase the watermark to the maximum value before the last checkpoint barrier. Use it when you
want to terminate the job permanently.


Attention STOP JOB statements only work in SQL CLI or SQL Gateway.


 Back to top
