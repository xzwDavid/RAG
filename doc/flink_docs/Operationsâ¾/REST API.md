# REST API


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# REST API#


Flink has a monitoring API that can be used to query status and statistics of running jobs, as well as recent completed jobs.
This monitoring API is used by Flink’s own dashboard, but is designed to be used also by custom monitoring tools.


The monitoring API is a REST-ful API that accepts HTTP requests and responds with JSON data.


## Overview#


The monitoring API is backed by a web server that runs as part of the JobManager. By default, this server listens at port 8081, which can be configured in Flink configuration file via rest.port. Note that the monitoring API web server and the web dashboard web server are currently the same and thus run together at the same port. They respond to different HTTP URLs, though.

`8081`
`rest.port`

In the case of multiple JobManagers (for high availability), each JobManager will run its own instance of the monitoring API, which offers information about completed and running job while that JobManager was elected the cluster leader.


## Developing#


The REST API backend is in the flink-runtime project. The core class is org.apache.flink.runtime.webmonitor.WebMonitorEndpoint, which sets up the server and the request routing.

`flink-runtime`
`org.apache.flink.runtime.webmonitor.WebMonitorEndpoint`

We use Netty and the Netty Router library to handle REST requests and translate URLs. This choice was made because this combination has lightweight dependencies, and the performance of Netty HTTP is very good.


To add new requests, one needs to

* add a new MessageHeaders class which serves as an interface for the new request,
* add a new AbstractRestHandler class which handles the request according to the added MessageHeaders class,
* add the handler to org.apache.flink.runtime.webmonitor.WebMonitorEndpoint#initializeHandlers().
`MessageHeaders`
`AbstractRestHandler`
`MessageHeaders`
`org.apache.flink.runtime.webmonitor.WebMonitorEndpoint#initializeHandlers()`

A good example is the org.apache.flink.runtime.rest.handler.job.JobExceptionsHandler that uses the org.apache.flink.runtime.rest.messages.JobExceptionsHeaders.

`org.apache.flink.runtime.rest.handler.job.JobExceptionsHandler`
`org.apache.flink.runtime.rest.messages.JobExceptionsHeaders`

## API#


The REST API is versioned, with specific versions being queryable by prefixing the url with the version prefix. Prefixes are always of the form v[version_number].
For example, to access version 1 of /foo/bar one would query /v1/foo/bar.

`v[version_number]`
`/foo/bar`
`/v1/foo/bar`

If no version is specified Flink will default to the oldest version supporting the request.


Querying unsupported/non-existing versions will return a 404 error.


There exist several async operations among these APIs, e.g. trigger savepoint, rescale a job. They would return a triggerid to identify the operation you just POST and then you need to use that triggerid to query for the status of the operation.

`trigger savepoint`
`rescale a job`
`triggerid`
`triggerid`

For (stop-with-)savepoint operations you can control this triggerId by setting it in the body of the request that triggers the operation.
This allow you to safely* retry such operations without triggering multiple savepoints.

`triggerId`

> 
  The retry is only safe until the async operation store duration has elapsed.



### JobManager#


OpenAPI specification


> 
  The OpenAPI specification is still experimental.



#### API reference#


##### /cluster

`DELETE`
`200 OK`

```
{}
```

`{}`

```
{}
```

`{}`

##### /config

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:DashboardConfiguration",
  "properties" : {
    "features" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:DashboardConfiguration:Features",
      "properties" : {
        "web-cancel" : {
          "type" : "boolean"
        },
        "web-history" : {
          "type" : "boolean"
        },
        "web-rescale" : {
          "type" : "boolean"
        },
        "web-submit" : {
          "type" : "boolean"
        }
      }
    },
    "flink-revision" : {
      "type" : "string"
    },
    "flink-version" : {
      "type" : "string"
    },
    "refresh-interval" : {
      "type" : "integer"
    },
    "timezone-name" : {
      "type" : "string"
    },
    "timezone-offset" : {
      "type" : "integer"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:DashboardConfiguration",
  "properties" : {
    "features" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:DashboardConfiguration:Features",
      "properties" : {
        "web-cancel" : {
          "type" : "boolean"
        },
        "web-history" : {
          "type" : "boolean"
        },
        "web-rescale" : {
          "type" : "boolean"
        },
        "web-submit" : {
          "type" : "boolean"
        }
      }
    },
    "flink-revision" : {
      "type" : "string"
    },
    "flink-version" : {
      "type" : "string"
    },
    "refresh-interval" : {
      "type" : "integer"
    },
    "timezone-name" : {
      "type" : "string"
    },
    "timezone-offset" : {
      "type" : "integer"
    }
  }
}`

##### /datasets

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:dataset:ClusterDataSetListResponseBody",
  "properties" : {
    "dataSets" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:dataset:ClusterDataSetEntry",
        "properties" : {
          "id" : {
            "type" : "string"
          },
          "isComplete" : {
            "type" : "boolean"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:dataset:ClusterDataSetListResponseBody",
  "properties" : {
    "dataSets" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:dataset:ClusterDataSetEntry",
        "properties" : {
          "id" : {
            "type" : "string"
          },
          "isComplete" : {
            "type" : "boolean"
          }
        }
      }
    }
  }
}`

##### /datasets/delete/:triggerid

`GET`
`200 OK`
* triggerid - 32-character hexadecimal string that identifies an asynchronous operation trigger ID. The ID was returned then the operation was triggered.
`triggerid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationResult",
  "properties" : {
    "operation" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationInfo",
      "properties" : {
        "failure-cause" : {
          "type" : "any"
        }
      }
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationResult",
  "properties" : {
    "operation" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationInfo",
      "properties" : {
        "failure-cause" : {
          "type" : "any"
        }
      }
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}`

##### /datasets/:datasetid

`DELETE`
`202 Accepted`
* datasetid - 32-character hexadecimal string value that identifies a cluster data set.
`datasetid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}`

##### /jars

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarListInfo",
  "properties" : {
    "address" : {
      "type" : "string"
    },
    "files" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarListInfo:JarFileInfo",
        "properties" : {
          "entry" : {
            "type" : "array",
            "items" : {
              "type" : "object",
              "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarListInfo:JarEntryInfo",
              "properties" : {
                "description" : {
                  "type" : "string"
                },
                "name" : {
                  "type" : "string"
                }
              }
            }
          },
          "id" : {
            "type" : "string"
          },
          "name" : {
            "type" : "string"
          },
          "uploaded" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarListInfo",
  "properties" : {
    "address" : {
      "type" : "string"
    },
    "files" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarListInfo:JarFileInfo",
        "properties" : {
          "entry" : {
            "type" : "array",
            "items" : {
              "type" : "object",
              "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarListInfo:JarEntryInfo",
              "properties" : {
                "description" : {
                  "type" : "string"
                },
                "name" : {
                  "type" : "string"
                }
              }
            }
          },
          "id" : {
            "type" : "string"
          },
          "name" : {
            "type" : "string"
          },
          "uploaded" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}`

##### /jars/upload

`POST`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarUploadResponseBody",
  "properties" : {
    "filename" : {
      "type" : "string"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "success" ]
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarUploadResponseBody",
  "properties" : {
    "filename" : {
      "type" : "string"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "success" ]
    }
  }
}`

##### /jars/:jarid

`DELETE`
`200 OK`
* jarid - String value that identifies a jar. When uploading the jar a path is returned, where the filename is the ID. This value is equivalent to the `id` field in the list of uploaded jars (/jars).
`jarid`

```
{}
```

`{}`

```
{}
```

`{}`

##### /jars/:jarid/plan

`POST`
`200 OK`
* jarid - String value that identifies a jar. When uploading the jar a path is returned, where the filename is the ID. This value is equivalent to the `id` field in the list of uploaded jars (/jars).
`jarid`
* programArg (optional): Comma-separated list of program arguments.
* entry-class (optional): String value that specifies the fully qualified name of the entry point class. Overrides the class defined in the jar file manifest.
* parallelism (optional): Positive integer value that specifies the desired parallelism for the job.
`programArg`
`entry-class`
`parallelism`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarPlanRequestBody",
  "properties" : {
    "entryClass" : {
      "type" : "string"
    },
    "flinkConfiguration" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "jobId" : {
      "type" : "any"
    },
    "parallelism" : {
      "type" : "integer"
    },
    "programArgsList" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarPlanRequestBody",
  "properties" : {
    "entryClass" : {
      "type" : "string"
    },
    "flinkConfiguration" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "jobId" : {
      "type" : "any"
    },
    "parallelism" : {
      "type" : "integer"
    },
    "programArgsList" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobPlanInfo",
  "properties" : {
    "plan" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobPlanInfo:RawJson"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobPlanInfo",
  "properties" : {
    "plan" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobPlanInfo:RawJson"
    }
  }
}`

##### /jars/:jarid/run

`POST`
`200 OK`
* jarid - String value that identifies a jar. When uploading the jar a path is returned, where the filename is the ID. This value is equivalent to the `id` field in the list of uploaded jars (/jars).
`jarid`
* allowNonRestoredState (optional): Boolean value that specifies whether the job submission should be rejected if the savepoint contains state that cannot be mapped back to the job.
* savepointPath (optional): String value that specifies the path of the savepoint to restore the job from.
* programArg (optional): Comma-separated list of program arguments.
* entry-class (optional): String value that specifies the fully qualified name of the entry point class. Overrides the class defined in the jar file manifest.
* parallelism (optional): Positive integer value that specifies the desired parallelism for the job.
`allowNonRestoredState`
`savepointPath`
`programArg`
`entry-class`
`parallelism`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarRunRequestBody",
  "properties" : {
    "allowNonRestoredState" : {
      "type" : "boolean"
    },
    "claimMode" : {
      "type" : "string",
      "enum" : [ "CLAIM", "NO_CLAIM", "LEGACY" ]
    },
    "entryClass" : {
      "type" : "string"
    },
    "flinkConfiguration" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "jobId" : {
      "type" : "any"
    },
    "parallelism" : {
      "type" : "integer"
    },
    "programArgsList" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "restoreMode" : {
      "type" : "string",
      "enum" : [ "CLAIM", "NO_CLAIM", "LEGACY" ]
    },
    "savepointPath" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarRunRequestBody",
  "properties" : {
    "allowNonRestoredState" : {
      "type" : "boolean"
    },
    "claimMode" : {
      "type" : "string",
      "enum" : [ "CLAIM", "NO_CLAIM", "LEGACY" ]
    },
    "entryClass" : {
      "type" : "string"
    },
    "flinkConfiguration" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "jobId" : {
      "type" : "any"
    },
    "parallelism" : {
      "type" : "integer"
    },
    "programArgsList" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "restoreMode" : {
      "type" : "string",
      "enum" : [ "CLAIM", "NO_CLAIM", "LEGACY" ]
    },
    "savepointPath" : {
      "type" : "string"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarRunResponseBody",
  "properties" : {
    "jobid" : {
      "type" : "any"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:handlers:JarRunResponseBody",
  "properties" : {
    "jobid" : {
      "type" : "any"
    }
  }
}`

##### /jobmanager/config

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "array",
  "items" : {
    "type" : "object",
    "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ConfigurationInfoEntry",
    "properties" : {
      "key" : {
        "type" : "string"
      },
      "value" : {
        "type" : "string"
      }
    }
  }
}
```

`{
  "type" : "array",
  "items" : {
    "type" : "object",
    "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ConfigurationInfoEntry",
    "properties" : {
      "key" : {
        "type" : "string"
      },
      "value" : {
        "type" : "string"
      }
    }
  }
}`

##### /jobmanager/environment

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:EnvironmentInfo",
  "properties" : {
    "classpath" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "jvm" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:EnvironmentInfo:JVMInfo",
      "properties" : {
        "arch" : {
          "type" : "string"
        },
        "options" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "version" : {
          "type" : "string"
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:EnvironmentInfo",
  "properties" : {
    "classpath" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "jvm" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:EnvironmentInfo:JVMInfo",
      "properties" : {
        "arch" : {
          "type" : "string"
        },
        "options" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "version" : {
          "type" : "string"
        }
      }
    }
  }
}`

##### /jobmanager/logs

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogListInfo",
  "properties" : {
    "logs" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogInfo",
        "properties" : {
          "mtime" : {
            "type" : "integer"
          },
          "name" : {
            "type" : "string"
          },
          "size" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogListInfo",
  "properties" : {
    "logs" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogInfo",
        "properties" : {
          "mtime" : {
            "type" : "integer"
          },
          "name" : {
            "type" : "string"
          },
          "size" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}`

##### /jobmanager/metrics

`GET`
`200 OK`
* get (optional): Comma-separated list of string values to select specific metrics.
`get`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /jobmanager/thread-dump

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ThreadDumpInfo",
  "properties" : {
    "threadInfos" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ThreadDumpInfo:ThreadInfo",
        "properties" : {
          "stringifiedThreadInfo" : {
            "type" : "string"
          },
          "threadName" : {
            "type" : "string"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ThreadDumpInfo",
  "properties" : {
    "threadInfos" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ThreadDumpInfo:ThreadInfo",
        "properties" : {
          "stringifiedThreadInfo" : {
            "type" : "string"
          },
          "threadName" : {
            "type" : "string"
          }
        }
      }
    }
  }
}`

##### /jobs

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:messages:webmonitor:JobIdsWithStatusOverview",
  "properties" : {
    "jobs" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:messages:webmonitor:JobIdsWithStatusOverview:JobIdWithStatus",
        "properties" : {
          "id" : {
            "type" : "any"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "INITIALIZING", "CREATED", "RUNNING", "FAILING", "FAILED", "CANCELLING", "CANCELED", "FINISHED", "RESTARTING", "SUSPENDED", "RECONCILING" ]
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:messages:webmonitor:JobIdsWithStatusOverview",
  "properties" : {
    "jobs" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:messages:webmonitor:JobIdsWithStatusOverview:JobIdWithStatus",
        "properties" : {
          "id" : {
            "type" : "any"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "INITIALIZING", "CREATED", "RUNNING", "FAILING", "FAILED", "CANCELLING", "CANCELED", "FINISHED", "RESTARTING", "SUSPENDED", "RECONCILING" ]
          }
        }
      }
    }
  }
}`

##### /jobs/metrics

`GET`
`200 OK`
* get (optional): Comma-separated list of string values to select specific metrics.
* agg (optional): Comma-separated list of aggregation modes which should be calculated. Available aggregations are: "min, max, sum, avg, skew".
* jobs (optional): Comma-separated list of 32-character hexadecimal strings to select specific jobs.
`get`
`agg`
`jobs`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /jobs/overview

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:messages:webmonitor:MultipleJobsDetails",
  "properties" : {
    "jobs" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:messages:webmonitor:JobDetails",
        "properties" : {
          "duration" : {
            "type" : "integer"
          },
          "end-time" : {
            "type" : "integer"
          },
          "jid" : {
            "type" : "any"
          },
          "last-modification" : {
            "type" : "integer"
          },
          "name" : {
            "type" : "string"
          },
          "start-time" : {
            "type" : "integer"
          },
          "state" : {
            "type" : "string",
            "enum" : [ "INITIALIZING", "CREATED", "RUNNING", "FAILING", "FAILED", "CANCELLING", "CANCELED", "FINISHED", "RESTARTING", "SUSPENDED", "RECONCILING" ]
          },
          "tasks" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:messages:webmonitor:MultipleJobsDetails",
  "properties" : {
    "jobs" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:messages:webmonitor:JobDetails",
        "properties" : {
          "duration" : {
            "type" : "integer"
          },
          "end-time" : {
            "type" : "integer"
          },
          "jid" : {
            "type" : "any"
          },
          "last-modification" : {
            "type" : "integer"
          },
          "name" : {
            "type" : "string"
          },
          "start-time" : {
            "type" : "integer"
          },
          "state" : {
            "type" : "string",
            "enum" : [ "INITIALIZING", "CREATED", "RUNNING", "FAILING", "FAILED", "CANCELLING", "CANCELED", "FINISHED", "RESTARTING", "SUSPENDED", "RECONCILING" ]
          },
          "tasks" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:JobDetailsInfo",
  "properties" : {
    "duration" : {
      "type" : "integer"
    },
    "end-time" : {
      "type" : "integer"
    },
    "isStoppable" : {
      "type" : "boolean"
    },
    "jid" : {
      "type" : "any"
    },
    "job-type" : {
      "type" : "string",
      "enum" : [ "BATCH", "STREAMING" ]
    },
    "maxParallelism" : {
      "type" : "integer"
    },
    "name" : {
      "type" : "string"
    },
    "now" : {
      "type" : "integer"
    },
    "plan" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobPlanInfo:RawJson"
    },
    "start-time" : {
      "type" : "integer"
    },
    "state" : {
      "type" : "string",
      "enum" : [ "INITIALIZING", "CREATED", "RUNNING", "FAILING", "FAILED", "CANCELLING", "CANCELED", "FINISHED", "RESTARTING", "SUSPENDED", "RECONCILING" ]
    },
    "status-counts" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "integer"
      }
    },
    "timestamps" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "integer"
      }
    },
    "vertices" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:JobDetailsInfo:JobVertexDetailsInfo",
        "properties" : {
          "duration" : {
            "type" : "integer"
          },
          "end-time" : {
            "type" : "integer"
          },
          "id" : {
            "type" : "any"
          },
          "maxParallelism" : {
            "type" : "integer"
          },
          "metrics" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:metrics:IOMetricsInfo",
            "properties" : {
              "accumulated-backpressured-time" : {
                "type" : "integer"
              },
              "accumulated-busy-time" : {
                "type" : "number"
              },
              "accumulated-idle-time" : {
                "type" : "integer"
              },
              "read-bytes" : {
                "type" : "integer"
              },
              "read-bytes-complete" : {
                "type" : "boolean"
              },
              "read-records" : {
                "type" : "integer"
              },
              "read-records-complete" : {
                "type" : "boolean"
              },
              "write-bytes" : {
                "type" : "integer"
              },
              "write-bytes-complete" : {
                "type" : "boolean"
              },
              "write-records" : {
                "type" : "integer"
              },
              "write-records-complete" : {
                "type" : "boolean"
              }
            }
          },
          "name" : {
            "type" : "string"
          },
          "parallelism" : {
            "type" : "integer"
          },
          "slotSharingGroupId" : {
            "type" : "any"
          },
          "start-time" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "CREATED", "SCHEDULED", "DEPLOYING", "RUNNING", "FINISHED", "CANCELING", "CANCELED", "FAILED", "RECONCILING", "INITIALIZING" ]
          },
          "tasks" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:JobDetailsInfo",
  "properties" : {
    "duration" : {
      "type" : "integer"
    },
    "end-time" : {
      "type" : "integer"
    },
    "isStoppable" : {
      "type" : "boolean"
    },
    "jid" : {
      "type" : "any"
    },
    "job-type" : {
      "type" : "string",
      "enum" : [ "BATCH", "STREAMING" ]
    },
    "maxParallelism" : {
      "type" : "integer"
    },
    "name" : {
      "type" : "string"
    },
    "now" : {
      "type" : "integer"
    },
    "plan" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobPlanInfo:RawJson"
    },
    "start-time" : {
      "type" : "integer"
    },
    "state" : {
      "type" : "string",
      "enum" : [ "INITIALIZING", "CREATED", "RUNNING", "FAILING", "FAILED", "CANCELLING", "CANCELED", "FINISHED", "RESTARTING", "SUSPENDED", "RECONCILING" ]
    },
    "status-counts" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "integer"
      }
    },
    "timestamps" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "integer"
      }
    },
    "vertices" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:JobDetailsInfo:JobVertexDetailsInfo",
        "properties" : {
          "duration" : {
            "type" : "integer"
          },
          "end-time" : {
            "type" : "integer"
          },
          "id" : {
            "type" : "any"
          },
          "maxParallelism" : {
            "type" : "integer"
          },
          "metrics" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:metrics:IOMetricsInfo",
            "properties" : {
              "accumulated-backpressured-time" : {
                "type" : "integer"
              },
              "accumulated-busy-time" : {
                "type" : "number"
              },
              "accumulated-idle-time" : {
                "type" : "integer"
              },
              "read-bytes" : {
                "type" : "integer"
              },
              "read-bytes-complete" : {
                "type" : "boolean"
              },
              "read-records" : {
                "type" : "integer"
              },
              "read-records-complete" : {
                "type" : "boolean"
              },
              "write-bytes" : {
                "type" : "integer"
              },
              "write-bytes-complete" : {
                "type" : "boolean"
              },
              "write-records" : {
                "type" : "integer"
              },
              "write-records-complete" : {
                "type" : "boolean"
              }
            }
          },
          "name" : {
            "type" : "string"
          },
          "parallelism" : {
            "type" : "integer"
          },
          "slotSharingGroupId" : {
            "type" : "any"
          },
          "start-time" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "CREATED", "SCHEDULED", "DEPLOYING", "RUNNING", "FINISHED", "CANCELING", "CANCELED", "FAILED", "RECONCILING", "INITIALIZING" ]
          },
          "tasks" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid

`PATCH`
`202 Accepted`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`
* mode (optional): String value that specifies the termination mode. The only supported value is: "cancel".
`mode`

```
{}
```

`{}`

```
{}
```

`{}`

##### /jobs/:jobid/accumulators

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`
* includeSerializedValue (optional): Boolean value that specifies whether serialized user task accumulators should be included in the response.
`includeSerializedValue`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobAccumulatorsInfo",
  "properties" : {
    "job-accumulators" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobAccumulatorsInfo:JobAccumulator"
      }
    },
    "serialized-user-task-accumulators" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "any"
      }
    },
    "user-task-accumulators" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobAccumulatorsInfo:UserTaskAccumulator",
        "properties" : {
          "name" : {
            "type" : "string"
          },
          "type" : {
            "type" : "string"
          },
          "value" : {
            "type" : "string"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobAccumulatorsInfo",
  "properties" : {
    "job-accumulators" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobAccumulatorsInfo:JobAccumulator"
      }
    },
    "serialized-user-task-accumulators" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "any"
      }
    },
    "user-task-accumulators" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobAccumulatorsInfo:UserTaskAccumulator",
        "properties" : {
          "name" : {
            "type" : "string"
          },
          "type" : {
            "type" : "string"
          },
          "value" : {
            "type" : "string"
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid/checkpoints

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointingStatistics",
  "properties" : {
    "counts" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointingStatistics:Counts",
      "properties" : {
        "completed" : {
          "type" : "integer"
        },
        "failed" : {
          "type" : "integer"
        },
        "in_progress" : {
          "type" : "integer"
        },
        "restored" : {
          "type" : "integer"
        },
        "total" : {
          "type" : "integer"
        }
      }
    },
    "history" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointStatistics",
        "properties" : {
          "alignment_buffered" : {
            "type" : "integer"
          },
          "checkpoint_type" : {
            "type" : "string",
            "enum" : [ "CHECKPOINT", "UNALIGNED_CHECKPOINT", "SAVEPOINT", "SYNC_SAVEPOINT" ]
          },
          "checkpointed_size" : {
            "type" : "integer"
          },
          "end_to_end_duration" : {
            "type" : "integer"
          },
          "id" : {
            "type" : "integer"
          },
          "is_savepoint" : {
            "type" : "boolean"
          },
          "latest_ack_timestamp" : {
            "type" : "integer"
          },
          "num_acknowledged_subtasks" : {
            "type" : "integer"
          },
          "num_subtasks" : {
            "type" : "integer"
          },
          "persisted_data" : {
            "type" : "integer"
          },
          "processed_data" : {
            "type" : "integer"
          },
          "savepointFormat" : {
            "type" : "string"
          },
          "state_size" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
          },
          "tasks" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatistics"
            }
          },
          "trigger_timestamp" : {
            "type" : "integer"
          }
        }
      }
    },
    "latest" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointingStatistics:LatestCheckpoints",
      "properties" : {
        "completed" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointStatistics:CompletedCheckpointStatistics",
          "properties" : {
            "alignment_buffered" : {
              "type" : "integer"
            },
            "checkpoint_type" : {
              "type" : "string",
              "enum" : [ "CHECKPOINT", "UNALIGNED_CHECKPOINT", "SAVEPOINT", "SYNC_SAVEPOINT" ]
            },
            "checkpointed_size" : {
              "type" : "integer"
            },
            "discarded" : {
              "type" : "boolean"
            },
            "end_to_end_duration" : {
              "type" : "integer"
            },
            "external_path" : {
              "type" : "string"
            },
            "id" : {
              "type" : "integer"
            },
            "is_savepoint" : {
              "type" : "boolean"
            },
            "latest_ack_timestamp" : {
              "type" : "integer"
            },
            "num_acknowledged_subtasks" : {
              "type" : "integer"
            },
            "num_subtasks" : {
              "type" : "integer"
            },
            "persisted_data" : {
              "type" : "integer"
            },
            "processed_data" : {
              "type" : "integer"
            },
            "savepointFormat" : {
              "type" : "string"
            },
            "state_size" : {
              "type" : "integer"
            },
            "status" : {
              "type" : "string",
              "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
            },
            "tasks" : {
              "type" : "object",
              "additionalProperties" : {
                "type" : "object",
                "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatistics",
                "properties" : {
                  "alignment_buffered" : {
                    "type" : "integer"
                  },
                  "checkpointed_size" : {
                    "type" : "integer"
                  },
                  "end_to_end_duration" : {
                    "type" : "integer"
                  },
                  "id" : {
                    "type" : "integer"
                  },
                  "latest_ack_timestamp" : {
                    "type" : "integer"
                  },
                  "num_acknowledged_subtasks" : {
                    "type" : "integer"
                  },
                  "num_subtasks" : {
                    "type" : "integer"
                  },
                  "persisted_data" : {
                    "type" : "integer"
                  },
                  "processed_data" : {
                    "type" : "integer"
                  },
                  "state_size" : {
                    "type" : "integer"
                  },
                  "status" : {
                    "type" : "string",
                    "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
                  }
                }
              }
            },
            "trigger_timestamp" : {
              "type" : "integer"
            }
          }
        },
        "failed" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointStatistics:FailedCheckpointStatistics",
          "properties" : {
            "alignment_buffered" : {
              "type" : "integer"
            },
            "checkpoint_type" : {
              "type" : "string",
              "enum" : [ "CHECKPOINT", "UNALIGNED_CHECKPOINT", "SAVEPOINT", "SYNC_SAVEPOINT" ]
            },
            "checkpointed_size" : {
              "type" : "integer"
            },
            "end_to_end_duration" : {
              "type" : "integer"
            },
            "failure_message" : {
              "type" : "string"
            },
            "failure_timestamp" : {
              "type" : "integer"
            },
            "id" : {
              "type" : "integer"
            },
            "is_savepoint" : {
              "type" : "boolean"
            },
            "latest_ack_timestamp" : {
              "type" : "integer"
            },
            "num_acknowledged_subtasks" : {
              "type" : "integer"
            },
            "num_subtasks" : {
              "type" : "integer"
            },
            "persisted_data" : {
              "type" : "integer"
            },
            "processed_data" : {
              "type" : "integer"
            },
            "savepointFormat" : {
              "type" : "string"
            },
            "state_size" : {
              "type" : "integer"
            },
            "status" : {
              "type" : "string",
              "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
            },
            "tasks" : {
              "type" : "object",
              "additionalProperties" : {
                "type" : "object",
                "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatistics"
              }
            },
            "trigger_timestamp" : {
              "type" : "integer"
            }
          }
        },
        "restored" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointingStatistics:RestoredCheckpointStatistics",
          "properties" : {
            "external_path" : {
              "type" : "string"
            },
            "id" : {
              "type" : "integer"
            },
            "is_savepoint" : {
              "type" : "boolean"
            },
            "restore_timestamp" : {
              "type" : "integer"
            }
          }
        },
        "savepoint" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointStatistics:CompletedCheckpointStatistics"
        }
      }
    },
    "summary" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointingStatistics:Summary",
      "properties" : {
        "alignment_buffered" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "checkpointed_size" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto",
          "properties" : {
            "avg" : {
              "type" : "integer"
            },
            "max" : {
              "type" : "integer"
            },
            "min" : {
              "type" : "integer"
            },
            "p50" : {
              "type" : "number"
            },
            "p90" : {
              "type" : "number"
            },
            "p95" : {
              "type" : "number"
            },
            "p99" : {
              "type" : "number"
            },
            "p999" : {
              "type" : "number"
            }
          }
        },
        "end_to_end_duration" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "persisted_data" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "processed_data" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "state_size" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointingStatistics",
  "properties" : {
    "counts" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointingStatistics:Counts",
      "properties" : {
        "completed" : {
          "type" : "integer"
        },
        "failed" : {
          "type" : "integer"
        },
        "in_progress" : {
          "type" : "integer"
        },
        "restored" : {
          "type" : "integer"
        },
        "total" : {
          "type" : "integer"
        }
      }
    },
    "history" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointStatistics",
        "properties" : {
          "alignment_buffered" : {
            "type" : "integer"
          },
          "checkpoint_type" : {
            "type" : "string",
            "enum" : [ "CHECKPOINT", "UNALIGNED_CHECKPOINT", "SAVEPOINT", "SYNC_SAVEPOINT" ]
          },
          "checkpointed_size" : {
            "type" : "integer"
          },
          "end_to_end_duration" : {
            "type" : "integer"
          },
          "id" : {
            "type" : "integer"
          },
          "is_savepoint" : {
            "type" : "boolean"
          },
          "latest_ack_timestamp" : {
            "type" : "integer"
          },
          "num_acknowledged_subtasks" : {
            "type" : "integer"
          },
          "num_subtasks" : {
            "type" : "integer"
          },
          "persisted_data" : {
            "type" : "integer"
          },
          "processed_data" : {
            "type" : "integer"
          },
          "savepointFormat" : {
            "type" : "string"
          },
          "state_size" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
          },
          "tasks" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatistics"
            }
          },
          "trigger_timestamp" : {
            "type" : "integer"
          }
        }
      }
    },
    "latest" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointingStatistics:LatestCheckpoints",
      "properties" : {
        "completed" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointStatistics:CompletedCheckpointStatistics",
          "properties" : {
            "alignment_buffered" : {
              "type" : "integer"
            },
            "checkpoint_type" : {
              "type" : "string",
              "enum" : [ "CHECKPOINT", "UNALIGNED_CHECKPOINT", "SAVEPOINT", "SYNC_SAVEPOINT" ]
            },
            "checkpointed_size" : {
              "type" : "integer"
            },
            "discarded" : {
              "type" : "boolean"
            },
            "end_to_end_duration" : {
              "type" : "integer"
            },
            "external_path" : {
              "type" : "string"
            },
            "id" : {
              "type" : "integer"
            },
            "is_savepoint" : {
              "type" : "boolean"
            },
            "latest_ack_timestamp" : {
              "type" : "integer"
            },
            "num_acknowledged_subtasks" : {
              "type" : "integer"
            },
            "num_subtasks" : {
              "type" : "integer"
            },
            "persisted_data" : {
              "type" : "integer"
            },
            "processed_data" : {
              "type" : "integer"
            },
            "savepointFormat" : {
              "type" : "string"
            },
            "state_size" : {
              "type" : "integer"
            },
            "status" : {
              "type" : "string",
              "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
            },
            "tasks" : {
              "type" : "object",
              "additionalProperties" : {
                "type" : "object",
                "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatistics",
                "properties" : {
                  "alignment_buffered" : {
                    "type" : "integer"
                  },
                  "checkpointed_size" : {
                    "type" : "integer"
                  },
                  "end_to_end_duration" : {
                    "type" : "integer"
                  },
                  "id" : {
                    "type" : "integer"
                  },
                  "latest_ack_timestamp" : {
                    "type" : "integer"
                  },
                  "num_acknowledged_subtasks" : {
                    "type" : "integer"
                  },
                  "num_subtasks" : {
                    "type" : "integer"
                  },
                  "persisted_data" : {
                    "type" : "integer"
                  },
                  "processed_data" : {
                    "type" : "integer"
                  },
                  "state_size" : {
                    "type" : "integer"
                  },
                  "status" : {
                    "type" : "string",
                    "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
                  }
                }
              }
            },
            "trigger_timestamp" : {
              "type" : "integer"
            }
          }
        },
        "failed" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointStatistics:FailedCheckpointStatistics",
          "properties" : {
            "alignment_buffered" : {
              "type" : "integer"
            },
            "checkpoint_type" : {
              "type" : "string",
              "enum" : [ "CHECKPOINT", "UNALIGNED_CHECKPOINT", "SAVEPOINT", "SYNC_SAVEPOINT" ]
            },
            "checkpointed_size" : {
              "type" : "integer"
            },
            "end_to_end_duration" : {
              "type" : "integer"
            },
            "failure_message" : {
              "type" : "string"
            },
            "failure_timestamp" : {
              "type" : "integer"
            },
            "id" : {
              "type" : "integer"
            },
            "is_savepoint" : {
              "type" : "boolean"
            },
            "latest_ack_timestamp" : {
              "type" : "integer"
            },
            "num_acknowledged_subtasks" : {
              "type" : "integer"
            },
            "num_subtasks" : {
              "type" : "integer"
            },
            "persisted_data" : {
              "type" : "integer"
            },
            "processed_data" : {
              "type" : "integer"
            },
            "savepointFormat" : {
              "type" : "string"
            },
            "state_size" : {
              "type" : "integer"
            },
            "status" : {
              "type" : "string",
              "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
            },
            "tasks" : {
              "type" : "object",
              "additionalProperties" : {
                "type" : "object",
                "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatistics"
              }
            },
            "trigger_timestamp" : {
              "type" : "integer"
            }
          }
        },
        "restored" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointingStatistics:RestoredCheckpointStatistics",
          "properties" : {
            "external_path" : {
              "type" : "string"
            },
            "id" : {
              "type" : "integer"
            },
            "is_savepoint" : {
              "type" : "boolean"
            },
            "restore_timestamp" : {
              "type" : "integer"
            }
          }
        },
        "savepoint" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointStatistics:CompletedCheckpointStatistics"
        }
      }
    },
    "summary" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointingStatistics:Summary",
      "properties" : {
        "alignment_buffered" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "checkpointed_size" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto",
          "properties" : {
            "avg" : {
              "type" : "integer"
            },
            "max" : {
              "type" : "integer"
            },
            "min" : {
              "type" : "integer"
            },
            "p50" : {
              "type" : "number"
            },
            "p90" : {
              "type" : "number"
            },
            "p95" : {
              "type" : "number"
            },
            "p99" : {
              "type" : "number"
            },
            "p999" : {
              "type" : "number"
            }
          }
        },
        "end_to_end_duration" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "persisted_data" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "processed_data" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "state_size" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        }
      }
    }
  }
}`

##### /jobs/:jobid/checkpoints

`POST`
`202 Accepted`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointTriggerRequestBody",
  "properties" : {
    "checkpointType" : {
      "type" : "string",
      "enum" : [ "CONFIGURED", "FULL", "INCREMENTAL" ]
    },
    "triggerId" : {
      "type" : "any"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointTriggerRequestBody",
  "properties" : {
    "checkpointType" : {
      "type" : "string",
      "enum" : [ "CONFIGURED", "FULL", "INCREMENTAL" ]
    },
    "triggerId" : {
      "type" : "any"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}`

##### /jobs/:jobid/checkpoints/config

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointConfigInfo",
  "properties" : {
    "aligned_checkpoint_timeout" : {
      "type" : "integer"
    },
    "changelog_periodic_materialization_interval" : {
      "type" : "integer"
    },
    "changelog_storage" : {
      "type" : "string"
    },
    "checkpoint_storage" : {
      "type" : "string"
    },
    "checkpoints_after_tasks_finish" : {
      "type" : "boolean"
    },
    "externalization" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointConfigInfo:ExternalizedCheckpointInfo",
      "properties" : {
        "delete_on_cancellation" : {
          "type" : "boolean"
        },
        "enabled" : {
          "type" : "boolean"
        }
      }
    },
    "interval" : {
      "type" : "integer"
    },
    "max_concurrent" : {
      "type" : "integer"
    },
    "min_pause" : {
      "type" : "integer"
    },
    "mode" : {
      "type" : "any"
    },
    "state_backend" : {
      "type" : "string"
    },
    "state_changelog_enabled" : {
      "type" : "boolean"
    },
    "timeout" : {
      "type" : "integer"
    },
    "tolerable_failed_checkpoints" : {
      "type" : "integer"
    },
    "unaligned_checkpoints" : {
      "type" : "boolean"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointConfigInfo",
  "properties" : {
    "aligned_checkpoint_timeout" : {
      "type" : "integer"
    },
    "changelog_periodic_materialization_interval" : {
      "type" : "integer"
    },
    "changelog_storage" : {
      "type" : "string"
    },
    "checkpoint_storage" : {
      "type" : "string"
    },
    "checkpoints_after_tasks_finish" : {
      "type" : "boolean"
    },
    "externalization" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointConfigInfo:ExternalizedCheckpointInfo",
      "properties" : {
        "delete_on_cancellation" : {
          "type" : "boolean"
        },
        "enabled" : {
          "type" : "boolean"
        }
      }
    },
    "interval" : {
      "type" : "integer"
    },
    "max_concurrent" : {
      "type" : "integer"
    },
    "min_pause" : {
      "type" : "integer"
    },
    "mode" : {
      "type" : "any"
    },
    "state_backend" : {
      "type" : "string"
    },
    "state_changelog_enabled" : {
      "type" : "boolean"
    },
    "timeout" : {
      "type" : "integer"
    },
    "tolerable_failed_checkpoints" : {
      "type" : "integer"
    },
    "unaligned_checkpoints" : {
      "type" : "boolean"
    }
  }
}`

##### /jobs/:jobid/checkpoints/details/:checkpointid

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* checkpointid - Long value that identifies a checkpoint.
`jobid`
`checkpointid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointStatistics",
  "properties" : {
    "alignment_buffered" : {
      "type" : "integer"
    },
    "checkpoint_type" : {
      "type" : "string",
      "enum" : [ "CHECKPOINT", "UNALIGNED_CHECKPOINT", "SAVEPOINT", "SYNC_SAVEPOINT" ]
    },
    "checkpointed_size" : {
      "type" : "integer"
    },
    "end_to_end_duration" : {
      "type" : "integer"
    },
    "id" : {
      "type" : "integer"
    },
    "is_savepoint" : {
      "type" : "boolean"
    },
    "latest_ack_timestamp" : {
      "type" : "integer"
    },
    "num_acknowledged_subtasks" : {
      "type" : "integer"
    },
    "num_subtasks" : {
      "type" : "integer"
    },
    "persisted_data" : {
      "type" : "integer"
    },
    "processed_data" : {
      "type" : "integer"
    },
    "savepointFormat" : {
      "type" : "string"
    },
    "state_size" : {
      "type" : "integer"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
    },
    "tasks" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatistics",
        "properties" : {
          "alignment_buffered" : {
            "type" : "integer"
          },
          "checkpointed_size" : {
            "type" : "integer"
          },
          "end_to_end_duration" : {
            "type" : "integer"
          },
          "id" : {
            "type" : "integer"
          },
          "latest_ack_timestamp" : {
            "type" : "integer"
          },
          "num_acknowledged_subtasks" : {
            "type" : "integer"
          },
          "num_subtasks" : {
            "type" : "integer"
          },
          "persisted_data" : {
            "type" : "integer"
          },
          "processed_data" : {
            "type" : "integer"
          },
          "state_size" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
          }
        }
      }
    },
    "trigger_timestamp" : {
      "type" : "integer"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointStatistics",
  "properties" : {
    "alignment_buffered" : {
      "type" : "integer"
    },
    "checkpoint_type" : {
      "type" : "string",
      "enum" : [ "CHECKPOINT", "UNALIGNED_CHECKPOINT", "SAVEPOINT", "SYNC_SAVEPOINT" ]
    },
    "checkpointed_size" : {
      "type" : "integer"
    },
    "end_to_end_duration" : {
      "type" : "integer"
    },
    "id" : {
      "type" : "integer"
    },
    "is_savepoint" : {
      "type" : "boolean"
    },
    "latest_ack_timestamp" : {
      "type" : "integer"
    },
    "num_acknowledged_subtasks" : {
      "type" : "integer"
    },
    "num_subtasks" : {
      "type" : "integer"
    },
    "persisted_data" : {
      "type" : "integer"
    },
    "processed_data" : {
      "type" : "integer"
    },
    "savepointFormat" : {
      "type" : "string"
    },
    "state_size" : {
      "type" : "integer"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
    },
    "tasks" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatistics",
        "properties" : {
          "alignment_buffered" : {
            "type" : "integer"
          },
          "checkpointed_size" : {
            "type" : "integer"
          },
          "end_to_end_duration" : {
            "type" : "integer"
          },
          "id" : {
            "type" : "integer"
          },
          "latest_ack_timestamp" : {
            "type" : "integer"
          },
          "num_acknowledged_subtasks" : {
            "type" : "integer"
          },
          "num_subtasks" : {
            "type" : "integer"
          },
          "persisted_data" : {
            "type" : "integer"
          },
          "processed_data" : {
            "type" : "integer"
          },
          "state_size" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
          }
        }
      }
    },
    "trigger_timestamp" : {
      "type" : "integer"
    }
  }
}`

##### /jobs/:jobid/checkpoints/details/:checkpointid/subtasks/:vertexid

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* checkpointid - Long value that identifies a checkpoint.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`checkpointid`
`vertexid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatisticsWithSubtaskDetails",
  "properties" : {
    "alignment_buffered" : {
      "type" : "integer"
    },
    "checkpointed_size" : {
      "type" : "integer"
    },
    "end_to_end_duration" : {
      "type" : "integer"
    },
    "id" : {
      "type" : "integer"
    },
    "latest_ack_timestamp" : {
      "type" : "integer"
    },
    "num_acknowledged_subtasks" : {
      "type" : "integer"
    },
    "num_subtasks" : {
      "type" : "integer"
    },
    "persisted_data" : {
      "type" : "integer"
    },
    "processed_data" : {
      "type" : "integer"
    },
    "state_size" : {
      "type" : "integer"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
    },
    "subtasks" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:SubtaskCheckpointStatistics",
        "properties" : {
          "index" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string"
          }
        }
      }
    },
    "summary" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatisticsWithSubtaskDetails:Summary",
      "properties" : {
        "alignment" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatisticsWithSubtaskDetails:CheckpointAlignment",
          "properties" : {
            "buffered" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            },
            "duration" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            },
            "persisted" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            },
            "processed" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            }
          }
        },
        "checkpoint_duration" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatisticsWithSubtaskDetails:CheckpointDuration",
          "properties" : {
            "async" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            },
            "sync" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            }
          }
        },
        "checkpointed_size" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto",
          "properties" : {
            "avg" : {
              "type" : "integer"
            },
            "max" : {
              "type" : "integer"
            },
            "min" : {
              "type" : "integer"
            },
            "p50" : {
              "type" : "number"
            },
            "p90" : {
              "type" : "number"
            },
            "p95" : {
              "type" : "number"
            },
            "p99" : {
              "type" : "number"
            },
            "p999" : {
              "type" : "number"
            }
          }
        },
        "end_to_end_duration" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "start_delay" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "state_size" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatisticsWithSubtaskDetails",
  "properties" : {
    "alignment_buffered" : {
      "type" : "integer"
    },
    "checkpointed_size" : {
      "type" : "integer"
    },
    "end_to_end_duration" : {
      "type" : "integer"
    },
    "id" : {
      "type" : "integer"
    },
    "latest_ack_timestamp" : {
      "type" : "integer"
    },
    "num_acknowledged_subtasks" : {
      "type" : "integer"
    },
    "num_subtasks" : {
      "type" : "integer"
    },
    "persisted_data" : {
      "type" : "integer"
    },
    "processed_data" : {
      "type" : "integer"
    },
    "state_size" : {
      "type" : "integer"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "IN_PROGRESS", "COMPLETED", "FAILED" ]
    },
    "subtasks" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:SubtaskCheckpointStatistics",
        "properties" : {
          "index" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string"
          }
        }
      }
    },
    "summary" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatisticsWithSubtaskDetails:Summary",
      "properties" : {
        "alignment" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatisticsWithSubtaskDetails:CheckpointAlignment",
          "properties" : {
            "buffered" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            },
            "duration" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            },
            "persisted" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            },
            "processed" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            }
          }
        },
        "checkpoint_duration" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:TaskCheckpointStatisticsWithSubtaskDetails:CheckpointDuration",
          "properties" : {
            "async" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            },
            "sync" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
            }
          }
        },
        "checkpointed_size" : {
          "type" : "object",
          "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto",
          "properties" : {
            "avg" : {
              "type" : "integer"
            },
            "max" : {
              "type" : "integer"
            },
            "min" : {
              "type" : "integer"
            },
            "p50" : {
              "type" : "number"
            },
            "p90" : {
              "type" : "number"
            },
            "p95" : {
              "type" : "number"
            },
            "p99" : {
              "type" : "number"
            },
            "p999" : {
              "type" : "number"
            }
          }
        },
        "end_to_end_duration" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "start_delay" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        },
        "state_size" : {
          "type" : "object",
          "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:StatsSummaryDto"
        }
      }
    }
  }
}`

##### /jobs/:jobid/checkpoints/:triggerid

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* triggerid - 32-character hexadecimal string that identifies an asynchronous operation trigger ID. The ID was returned then the operation was triggered.
`jobid`
`triggerid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationResult",
  "properties" : {
    "operation" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointInfo",
      "properties" : {
        "checkpointId" : {
          "type" : "integer"
        },
        "failureCause" : {
          "type" : "any"
        }
      }
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationResult",
  "properties" : {
    "operation" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:checkpoints:CheckpointInfo",
      "properties" : {
        "checkpointId" : {
          "type" : "integer"
        },
        "failureCause" : {
          "type" : "any"
        }
      }
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}`

##### /jobs/:jobid/clientHeartbeat

`PATCH`
`202 Accepted`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobClientHeartbeatRequestBody",
  "properties" : {
    "expiredTimestamp" : {
      "type" : "integer"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobClientHeartbeatRequestBody",
  "properties" : {
    "expiredTimestamp" : {
      "type" : "integer"
    }
  }
}`

```
{}
```

`{}`

##### /jobs/:jobid/config

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /jobs/:jobid/exceptions

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`
* maxExceptions (optional): Comma-separated list of integer values that specifies the upper limit of exceptions to return.
* failureLabelFilter (optional): Collection of string values working as a filter in the form of `key:value` pairs allowing only exceptions with ALL of the specified failure labels to be returned.
`maxExceptions`
`failureLabelFilter`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobExceptionsInfoWithHistory",
  "properties" : {
    "exceptionHistory" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobExceptionsInfoWithHistory:JobExceptionHistory",
      "properties" : {
        "entries" : {
          "type" : "array",
          "items" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobExceptionsInfoWithHistory:RootExceptionInfo",
            "properties" : {
              "concurrentExceptions" : {
                "type" : "array",
                "items" : {
                  "type" : "object",
                  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobExceptionsInfoWithHistory:ExceptionInfo",
                  "properties" : {
                    "endpoint" : {
                      "type" : "string"
                    },
                    "exceptionName" : {
                      "type" : "string"
                    },
                    "failureLabels" : {
                      "type" : "object",
                      "additionalProperties" : {
                        "type" : "string"
                      }
                    },
                    "stacktrace" : {
                      "type" : "string"
                    },
                    "taskManagerId" : {
                      "type" : "string"
                    },
                    "taskName" : {
                      "type" : "string"
                    },
                    "timestamp" : {
                      "type" : "integer"
                    }
                  }
                }
              },
              "endpoint" : {
                "type" : "string"
              },
              "exceptionName" : {
                "type" : "string"
              },
              "failureLabels" : {
                "type" : "object",
                "additionalProperties" : {
                  "type" : "string"
                }
              },
              "stacktrace" : {
                "type" : "string"
              },
              "taskManagerId" : {
                "type" : "string"
              },
              "taskName" : {
                "type" : "string"
              },
              "timestamp" : {
                "type" : "integer"
              }
            }
          }
        },
        "truncated" : {
          "type" : "boolean"
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobExceptionsInfoWithHistory",
  "properties" : {
    "exceptionHistory" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobExceptionsInfoWithHistory:JobExceptionHistory",
      "properties" : {
        "entries" : {
          "type" : "array",
          "items" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobExceptionsInfoWithHistory:RootExceptionInfo",
            "properties" : {
              "concurrentExceptions" : {
                "type" : "array",
                "items" : {
                  "type" : "object",
                  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobExceptionsInfoWithHistory:ExceptionInfo",
                  "properties" : {
                    "endpoint" : {
                      "type" : "string"
                    },
                    "exceptionName" : {
                      "type" : "string"
                    },
                    "failureLabels" : {
                      "type" : "object",
                      "additionalProperties" : {
                        "type" : "string"
                      }
                    },
                    "stacktrace" : {
                      "type" : "string"
                    },
                    "taskManagerId" : {
                      "type" : "string"
                    },
                    "taskName" : {
                      "type" : "string"
                    },
                    "timestamp" : {
                      "type" : "integer"
                    }
                  }
                }
              },
              "endpoint" : {
                "type" : "string"
              },
              "exceptionName" : {
                "type" : "string"
              },
              "failureLabels" : {
                "type" : "object",
                "additionalProperties" : {
                  "type" : "string"
                }
              },
              "stacktrace" : {
                "type" : "string"
              },
              "taskManagerId" : {
                "type" : "string"
              },
              "taskName" : {
                "type" : "string"
              },
              "timestamp" : {
                "type" : "integer"
              }
            }
          }
        },
        "truncated" : {
          "type" : "boolean"
        }
      }
    }
  }
}`

##### /jobs/:jobid/execution-result

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:JobExecutionResultResponseBody",
  "properties" : {
    "job-execution-result" : {
      "type" : "any"
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "required" : true,
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:JobExecutionResultResponseBody",
  "properties" : {
    "job-execution-result" : {
      "type" : "any"
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "required" : true,
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}`

##### /jobs/:jobid/jobmanager/config

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "array",
  "items" : {
    "type" : "object",
    "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ConfigurationInfoEntry",
    "properties" : {
      "key" : {
        "type" : "string"
      },
      "value" : {
        "type" : "string"
      }
    }
  }
}
```

`{
  "type" : "array",
  "items" : {
    "type" : "object",
    "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ConfigurationInfoEntry",
    "properties" : {
      "key" : {
        "type" : "string"
      },
      "value" : {
        "type" : "string"
      }
    }
  }
}`

##### /jobs/:jobid/jobmanager/environment

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:EnvironmentInfo",
  "properties" : {
    "classpath" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "jvm" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:EnvironmentInfo:JVMInfo",
      "properties" : {
        "arch" : {
          "type" : "string"
        },
        "options" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "version" : {
          "type" : "string"
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:EnvironmentInfo",
  "properties" : {
    "classpath" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    },
    "jvm" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:EnvironmentInfo:JVMInfo",
      "properties" : {
        "arch" : {
          "type" : "string"
        },
        "options" : {
          "type" : "array",
          "items" : {
            "type" : "string"
          }
        },
        "version" : {
          "type" : "string"
        }
      }
    }
  }
}`

##### /jobs/:jobid/jobmanager/log-url

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogUrlResponse",
  "properties" : {
    "url" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogUrlResponse",
  "properties" : {
    "url" : {
      "type" : "string"
    }
  }
}`

##### /jobs/:jobid/metrics

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`
* get (optional): Comma-separated list of string values to select specific metrics.
`get`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /jobs/:jobid/plan

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobPlanInfo",
  "properties" : {
    "plan" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobPlanInfo:RawJson"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobPlanInfo",
  "properties" : {
    "plan" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobPlanInfo:RawJson"
    }
  }
}`

##### /jobs/:jobid/rescaling

`PATCH`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`
* parallelism (mandatory): Positive integer value that specifies the desired parallelism.
`parallelism`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}`

##### /jobs/:jobid/rescaling/:triggerid

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* triggerid - 32-character hexadecimal string that identifies an asynchronous operation trigger ID. The ID was returned then the operation was triggered.
`jobid`
`triggerid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationResult",
  "properties" : {
    "operation" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationInfo",
      "properties" : {
        "failure-cause" : {
          "type" : "any"
        }
      }
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationResult",
  "properties" : {
    "operation" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationInfo",
      "properties" : {
        "failure-cause" : {
          "type" : "any"
        }
      }
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}`

##### /jobs/:jobid/resource-requirements

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:JobResourceRequirementsBody",
  "additionalProperties" : {
    "type" : "object",
    "id" : "urn:jsonschema:org:apache:flink:runtime:jobgraph:JobVertexResourceRequirements",
    "properties" : {
      "parallelism" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:jobgraph:JobVertexResourceRequirements:Parallelism",
        "properties" : {
          "lowerBound" : {
            "type" : "integer"
          },
          "upperBound" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:JobResourceRequirementsBody",
  "additionalProperties" : {
    "type" : "object",
    "id" : "urn:jsonschema:org:apache:flink:runtime:jobgraph:JobVertexResourceRequirements",
    "properties" : {
      "parallelism" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:jobgraph:JobVertexResourceRequirements:Parallelism",
        "properties" : {
          "lowerBound" : {
            "type" : "integer"
          },
          "upperBound" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid/resource-requirements

`PUT`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:JobResourceRequirementsBody",
  "additionalProperties" : {
    "type" : "object",
    "id" : "urn:jsonschema:org:apache:flink:runtime:jobgraph:JobVertexResourceRequirements",
    "properties" : {
      "parallelism" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:jobgraph:JobVertexResourceRequirements:Parallelism",
        "properties" : {
          "lowerBound" : {
            "type" : "integer"
          },
          "upperBound" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:JobResourceRequirementsBody",
  "additionalProperties" : {
    "type" : "object",
    "id" : "urn:jsonschema:org:apache:flink:runtime:jobgraph:JobVertexResourceRequirements",
    "properties" : {
      "parallelism" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:jobgraph:JobVertexResourceRequirements:Parallelism",
        "properties" : {
          "lowerBound" : {
            "type" : "integer"
          },
          "upperBound" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}`

```
{}
```

`{}`

##### /jobs/:jobid/savepoints

`POST`
`202 Accepted`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:savepoints:SavepointTriggerRequestBody",
  "properties" : {
    "cancel-job" : {
      "type" : "boolean"
    },
    "formatType" : {
      "type" : "string",
      "enum" : [ "CANONICAL", "NATIVE" ]
    },
    "target-directory" : {
      "type" : "string"
    },
    "triggerId" : {
      "type" : "any"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:savepoints:SavepointTriggerRequestBody",
  "properties" : {
    "cancel-job" : {
      "type" : "boolean"
    },
    "formatType" : {
      "type" : "string",
      "enum" : [ "CANONICAL", "NATIVE" ]
    },
    "target-directory" : {
      "type" : "string"
    },
    "triggerId" : {
      "type" : "any"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}`

##### /jobs/:jobid/savepoints/:triggerid

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* triggerid - 32-character hexadecimal string that identifies an asynchronous operation trigger ID. The ID was returned then the operation was triggered.
`jobid`
`triggerid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationResult",
  "properties" : {
    "operation" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:savepoints:SavepointInfo",
      "properties" : {
        "failure-cause" : {
          "type" : "any"
        },
        "location" : {
          "type" : "string"
        }
      }
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationResult",
  "properties" : {
    "operation" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:savepoints:SavepointInfo",
      "properties" : {
        "failure-cause" : {
          "type" : "any"
        },
        "location" : {
          "type" : "string"
        }
      }
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}`

##### /jobs/:jobid/status

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:messages:webmonitor:JobStatusInfo",
  "properties" : {
    "status" : {
      "type" : "string",
      "enum" : [ "INITIALIZING", "CREATED", "RUNNING", "FAILING", "FAILED", "CANCELLING", "CANCELED", "FINISHED", "RESTARTING", "SUSPENDED", "RECONCILING" ]
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:messages:webmonitor:JobStatusInfo",
  "properties" : {
    "status" : {
      "type" : "string",
      "enum" : [ "INITIALIZING", "CREATED", "RUNNING", "FAILING", "FAILED", "CANCELLING", "CANCELED", "FINISHED", "RESTARTING", "SUSPENDED", "RECONCILING" ]
    }
  }
}`

##### /jobs/:jobid/stop

`POST`
`202 Accepted`
* jobid - 32-character hexadecimal string value that identifies a job.
`jobid`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:savepoints:stop:StopWithSavepointRequestBody",
  "properties" : {
    "drain" : {
      "type" : "boolean"
    },
    "formatType" : {
      "type" : "string",
      "enum" : [ "CANONICAL", "NATIVE" ]
    },
    "targetDirectory" : {
      "type" : "string"
    },
    "triggerId" : {
      "type" : "any"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:savepoints:stop:StopWithSavepointRequestBody",
  "properties" : {
    "drain" : {
      "type" : "boolean"
    },
    "formatType" : {
      "type" : "string",
      "enum" : [ "CANONICAL", "NATIVE" ]
    },
    "targetDirectory" : {
      "type" : "string"
    },
    "triggerId" : {
      "type" : "any"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}`

##### /jobs/:jobid/taskmanagers/:taskmanagerid/log-url

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* taskmanagerid - 32-character hexadecimal string that identifies a task manager.
`jobid`
`taskmanagerid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogUrlResponse",
  "properties" : {
    "url" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogUrlResponse",
  "properties" : {
    "url" : {
      "type" : "string"
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexDetailsInfo",
  "properties" : {
    "aggregated" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:AggregatedTaskDetailsInfo",
      "properties" : {
        "metrics" : {
          "type" : "object",
          "additionalProperties" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          }
        },
        "status-duration" : {
          "type" : "object",
          "additionalProperties" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          }
        }
      }
    },
    "id" : {
      "type" : "any"
    },
    "maxParallelism" : {
      "type" : "integer"
    },
    "name" : {
      "type" : "string"
    },
    "now" : {
      "type" : "integer"
    },
    "parallelism" : {
      "type" : "integer"
    },
    "subtasks" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo",
        "properties" : {
          "attempt" : {
            "type" : "integer"
          },
          "duration" : {
            "type" : "integer"
          },
          "end-time" : {
            "type" : "integer"
          },
          "endpoint" : {
            "type" : "string"
          },
          "metrics" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:metrics:IOMetricsInfo",
            "properties" : {
              "accumulated-backpressured-time" : {
                "type" : "integer"
              },
              "accumulated-busy-time" : {
                "type" : "number"
              },
              "accumulated-idle-time" : {
                "type" : "integer"
              },
              "read-bytes" : {
                "type" : "integer"
              },
              "read-bytes-complete" : {
                "type" : "boolean"
              },
              "read-records" : {
                "type" : "integer"
              },
              "read-records-complete" : {
                "type" : "boolean"
              },
              "write-bytes" : {
                "type" : "integer"
              },
              "write-bytes-complete" : {
                "type" : "boolean"
              },
              "write-records" : {
                "type" : "integer"
              },
              "write-records-complete" : {
                "type" : "boolean"
              }
            }
          },
          "other-concurrent-attempts" : {
            "type" : "array",
            "items" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo"
            }
          },
          "start-time" : {
            "type" : "integer"
          },
          "start_time" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "CREATED", "SCHEDULED", "DEPLOYING", "RUNNING", "FINISHED", "CANCELING", "CANCELED", "FAILED", "RECONCILING", "INITIALIZING" ]
          },
          "status-duration" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          },
          "subtask" : {
            "type" : "integer"
          },
          "taskmanager-id" : {
            "type" : "string"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexDetailsInfo",
  "properties" : {
    "aggregated" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:AggregatedTaskDetailsInfo",
      "properties" : {
        "metrics" : {
          "type" : "object",
          "additionalProperties" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          }
        },
        "status-duration" : {
          "type" : "object",
          "additionalProperties" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          }
        }
      }
    },
    "id" : {
      "type" : "any"
    },
    "maxParallelism" : {
      "type" : "integer"
    },
    "name" : {
      "type" : "string"
    },
    "now" : {
      "type" : "integer"
    },
    "parallelism" : {
      "type" : "integer"
    },
    "subtasks" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo",
        "properties" : {
          "attempt" : {
            "type" : "integer"
          },
          "duration" : {
            "type" : "integer"
          },
          "end-time" : {
            "type" : "integer"
          },
          "endpoint" : {
            "type" : "string"
          },
          "metrics" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:metrics:IOMetricsInfo",
            "properties" : {
              "accumulated-backpressured-time" : {
                "type" : "integer"
              },
              "accumulated-busy-time" : {
                "type" : "number"
              },
              "accumulated-idle-time" : {
                "type" : "integer"
              },
              "read-bytes" : {
                "type" : "integer"
              },
              "read-bytes-complete" : {
                "type" : "boolean"
              },
              "read-records" : {
                "type" : "integer"
              },
              "read-records-complete" : {
                "type" : "boolean"
              },
              "write-bytes" : {
                "type" : "integer"
              },
              "write-bytes-complete" : {
                "type" : "boolean"
              },
              "write-records" : {
                "type" : "integer"
              },
              "write-records-complete" : {
                "type" : "boolean"
              }
            }
          },
          "other-concurrent-attempts" : {
            "type" : "array",
            "items" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo"
            }
          },
          "start-time" : {
            "type" : "integer"
          },
          "start_time" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "CREATED", "SCHEDULED", "DEPLOYING", "RUNNING", "FINISHED", "CANCELING", "CANCELED", "FAILED", "RECONCILING", "INITIALIZING" ]
          },
          "status-duration" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          },
          "subtask" : {
            "type" : "integer"
          },
          "taskmanager-id" : {
            "type" : "string"
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid/accumulators

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexAccumulatorsInfo",
  "properties" : {
    "id" : {
      "type" : "string"
    },
    "user-accumulators" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:UserAccumulator",
        "properties" : {
          "name" : {
            "type" : "string"
          },
          "type" : {
            "type" : "string"
          },
          "value" : {
            "type" : "string"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexAccumulatorsInfo",
  "properties" : {
    "id" : {
      "type" : "string"
    },
    "user-accumulators" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:UserAccumulator",
        "properties" : {
          "name" : {
            "type" : "string"
          },
          "type" : {
            "type" : "string"
          },
          "value" : {
            "type" : "string"
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid/backpressure

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexBackPressureInfo",
  "properties" : {
    "backpressure-level" : {
      "type" : "string",
      "enum" : [ "ok", "low", "high" ]
    },
    "backpressureLevel" : {
      "type" : "string",
      "enum" : [ "ok", "low", "high" ]
    },
    "end-timestamp" : {
      "type" : "integer"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "deprecated", "ok" ]
    },
    "subtasks" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexBackPressureInfo:SubtaskBackPressureInfo",
        "properties" : {
          "attempt-number" : {
            "type" : "integer"
          },
          "backpressure-level" : {
            "type" : "string",
            "enum" : [ "ok", "low", "high" ]
          },
          "backpressureLevel" : {
            "type" : "string",
            "enum" : [ "ok", "low", "high" ]
          },
          "busyRatio" : {
            "type" : "number"
          },
          "idleRatio" : {
            "type" : "number"
          },
          "other-concurrent-attempts" : {
            "type" : "array",
            "items" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexBackPressureInfo:SubtaskBackPressureInfo"
            }
          },
          "ratio" : {
            "type" : "number"
          },
          "subtask" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexBackPressureInfo",
  "properties" : {
    "backpressure-level" : {
      "type" : "string",
      "enum" : [ "ok", "low", "high" ]
    },
    "backpressureLevel" : {
      "type" : "string",
      "enum" : [ "ok", "low", "high" ]
    },
    "end-timestamp" : {
      "type" : "integer"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "deprecated", "ok" ]
    },
    "subtasks" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexBackPressureInfo:SubtaskBackPressureInfo",
        "properties" : {
          "attempt-number" : {
            "type" : "integer"
          },
          "backpressure-level" : {
            "type" : "string",
            "enum" : [ "ok", "low", "high" ]
          },
          "backpressureLevel" : {
            "type" : "string",
            "enum" : [ "ok", "low", "high" ]
          },
          "busyRatio" : {
            "type" : "number"
          },
          "idleRatio" : {
            "type" : "number"
          },
          "other-concurrent-attempts" : {
            "type" : "array",
            "items" : {
              "type" : "object",
              "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexBackPressureInfo:SubtaskBackPressureInfo"
            }
          },
          "ratio" : {
            "type" : "number"
          },
          "subtask" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid/flamegraph

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`
* type (optional): String value that specifies the Flame Graph type. Supported options are: "[FULL, ON_CPU, OFF_CPU]".
* subtaskindex (optional): Positive integer value that identifies a subtask.
`type`
`subtaskindex`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:threadinfo:VertexFlameGraph",
  "properties" : {
    "data" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:threadinfo:VertexFlameGraph:Node",
      "properties" : {
        "children" : {
          "type" : "array",
          "items" : {
            "type" : "object",
            "$ref" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:threadinfo:VertexFlameGraph:Node"
          }
        },
        "name" : {
          "type" : "string"
        },
        "value" : {
          "type" : "integer"
        }
      }
    },
    "endTimestamp" : {
      "type" : "integer"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:threadinfo:VertexFlameGraph",
  "properties" : {
    "data" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:threadinfo:VertexFlameGraph:Node",
      "properties" : {
        "children" : {
          "type" : "array",
          "items" : {
            "type" : "object",
            "$ref" : "urn:jsonschema:org:apache:flink:runtime:webmonitor:threadinfo:VertexFlameGraph:Node"
          }
        },
        "name" : {
          "type" : "string"
        },
        "value" : {
          "type" : "integer"
        }
      }
    },
    "endTimestamp" : {
      "type" : "integer"
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid/jm-operator-metrics

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`
* get (optional): Comma-separated list of string values to select specific metrics.
`get`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /jobs/:jobid/vertices/:vertexid/metrics

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`
* get (optional): Comma-separated list of string values to select specific metrics.
`get`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /jobs/:jobid/vertices/:vertexid/subtasks/accumulators

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtasksAllAccumulatorsInfo",
  "properties" : {
    "id" : {
      "type" : "any"
    },
    "parallelism" : {
      "type" : "integer"
    },
    "subtasks" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtasksAllAccumulatorsInfo:SubtaskAccumulatorsInfo",
        "properties" : {
          "attempt" : {
            "type" : "integer"
          },
          "endpoint" : {
            "type" : "string"
          },
          "subtask" : {
            "type" : "integer"
          },
          "user-accumulators" : {
            "type" : "array",
            "items" : {
              "type" : "object",
              "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:UserAccumulator",
              "properties" : {
                "name" : {
                  "type" : "string"
                },
                "type" : {
                  "type" : "string"
                },
                "value" : {
                  "type" : "string"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtasksAllAccumulatorsInfo",
  "properties" : {
    "id" : {
      "type" : "any"
    },
    "parallelism" : {
      "type" : "integer"
    },
    "subtasks" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtasksAllAccumulatorsInfo:SubtaskAccumulatorsInfo",
        "properties" : {
          "attempt" : {
            "type" : "integer"
          },
          "endpoint" : {
            "type" : "string"
          },
          "subtask" : {
            "type" : "integer"
          },
          "user-accumulators" : {
            "type" : "array",
            "items" : {
              "type" : "object",
              "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:UserAccumulator",
              "properties" : {
                "name" : {
                  "type" : "string"
                },
                "type" : {
                  "type" : "string"
                },
                "value" : {
                  "type" : "string"
                }
              }
            }
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid/subtasks/metrics

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`
* get (optional): Comma-separated list of string values to select specific metrics.
* agg (optional): Comma-separated list of aggregation modes which should be calculated. Available aggregations are: "min, max, sum, avg, skew".
* subtasks (optional): Comma-separated list of integer ranges (e.g. "1,3,5-9") to select specific subtasks.
`get`
`agg`
`subtasks`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /jobs/:jobid/vertices/:vertexid/subtasks/:subtaskindex

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
* subtaskindex - Positive integer value that identifies a subtask.
`jobid`
`vertexid`
`subtaskindex`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo",
  "properties" : {
    "attempt" : {
      "type" : "integer"
    },
    "duration" : {
      "type" : "integer"
    },
    "end-time" : {
      "type" : "integer"
    },
    "endpoint" : {
      "type" : "string"
    },
    "metrics" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:metrics:IOMetricsInfo",
      "properties" : {
        "accumulated-backpressured-time" : {
          "type" : "integer"
        },
        "accumulated-busy-time" : {
          "type" : "number"
        },
        "accumulated-idle-time" : {
          "type" : "integer"
        },
        "read-bytes" : {
          "type" : "integer"
        },
        "read-bytes-complete" : {
          "type" : "boolean"
        },
        "read-records" : {
          "type" : "integer"
        },
        "read-records-complete" : {
          "type" : "boolean"
        },
        "write-bytes" : {
          "type" : "integer"
        },
        "write-bytes-complete" : {
          "type" : "boolean"
        },
        "write-records" : {
          "type" : "integer"
        },
        "write-records-complete" : {
          "type" : "boolean"
        }
      }
    },
    "other-concurrent-attempts" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo"
      }
    },
    "start-time" : {
      "type" : "integer"
    },
    "start_time" : {
      "type" : "integer"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "CREATED", "SCHEDULED", "DEPLOYING", "RUNNING", "FINISHED", "CANCELING", "CANCELED", "FAILED", "RECONCILING", "INITIALIZING" ]
    },
    "status-duration" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "integer"
      }
    },
    "subtask" : {
      "type" : "integer"
    },
    "taskmanager-id" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo",
  "properties" : {
    "attempt" : {
      "type" : "integer"
    },
    "duration" : {
      "type" : "integer"
    },
    "end-time" : {
      "type" : "integer"
    },
    "endpoint" : {
      "type" : "string"
    },
    "metrics" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:metrics:IOMetricsInfo",
      "properties" : {
        "accumulated-backpressured-time" : {
          "type" : "integer"
        },
        "accumulated-busy-time" : {
          "type" : "number"
        },
        "accumulated-idle-time" : {
          "type" : "integer"
        },
        "read-bytes" : {
          "type" : "integer"
        },
        "read-bytes-complete" : {
          "type" : "boolean"
        },
        "read-records" : {
          "type" : "integer"
        },
        "read-records-complete" : {
          "type" : "boolean"
        },
        "write-bytes" : {
          "type" : "integer"
        },
        "write-bytes-complete" : {
          "type" : "boolean"
        },
        "write-records" : {
          "type" : "integer"
        },
        "write-records-complete" : {
          "type" : "boolean"
        }
      }
    },
    "other-concurrent-attempts" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo"
      }
    },
    "start-time" : {
      "type" : "integer"
    },
    "start_time" : {
      "type" : "integer"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "CREATED", "SCHEDULED", "DEPLOYING", "RUNNING", "FINISHED", "CANCELING", "CANCELED", "FAILED", "RECONCILING", "INITIALIZING" ]
    },
    "status-duration" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "integer"
      }
    },
    "subtask" : {
      "type" : "integer"
    },
    "taskmanager-id" : {
      "type" : "string"
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid/subtasks/:subtaskindex/attempts/:attempt

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
* subtaskindex - Positive integer value that identifies a subtask.
* attempt - Positive integer value that identifies an execution attempt.
`jobid`
`vertexid`
`subtaskindex`
`attempt`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo",
  "properties" : {
    "attempt" : {
      "type" : "integer"
    },
    "duration" : {
      "type" : "integer"
    },
    "end-time" : {
      "type" : "integer"
    },
    "endpoint" : {
      "type" : "string"
    },
    "metrics" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:metrics:IOMetricsInfo",
      "properties" : {
        "accumulated-backpressured-time" : {
          "type" : "integer"
        },
        "accumulated-busy-time" : {
          "type" : "number"
        },
        "accumulated-idle-time" : {
          "type" : "integer"
        },
        "read-bytes" : {
          "type" : "integer"
        },
        "read-bytes-complete" : {
          "type" : "boolean"
        },
        "read-records" : {
          "type" : "integer"
        },
        "read-records-complete" : {
          "type" : "boolean"
        },
        "write-bytes" : {
          "type" : "integer"
        },
        "write-bytes-complete" : {
          "type" : "boolean"
        },
        "write-records" : {
          "type" : "integer"
        },
        "write-records-complete" : {
          "type" : "boolean"
        }
      }
    },
    "other-concurrent-attempts" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo"
      }
    },
    "start-time" : {
      "type" : "integer"
    },
    "start_time" : {
      "type" : "integer"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "CREATED", "SCHEDULED", "DEPLOYING", "RUNNING", "FINISHED", "CANCELING", "CANCELED", "FAILED", "RECONCILING", "INITIALIZING" ]
    },
    "status-duration" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "integer"
      }
    },
    "subtask" : {
      "type" : "integer"
    },
    "taskmanager-id" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo",
  "properties" : {
    "attempt" : {
      "type" : "integer"
    },
    "duration" : {
      "type" : "integer"
    },
    "end-time" : {
      "type" : "integer"
    },
    "endpoint" : {
      "type" : "string"
    },
    "metrics" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:metrics:IOMetricsInfo",
      "properties" : {
        "accumulated-backpressured-time" : {
          "type" : "integer"
        },
        "accumulated-busy-time" : {
          "type" : "number"
        },
        "accumulated-idle-time" : {
          "type" : "integer"
        },
        "read-bytes" : {
          "type" : "integer"
        },
        "read-bytes-complete" : {
          "type" : "boolean"
        },
        "read-records" : {
          "type" : "integer"
        },
        "read-records-complete" : {
          "type" : "boolean"
        },
        "write-bytes" : {
          "type" : "integer"
        },
        "write-bytes-complete" : {
          "type" : "boolean"
        },
        "write-records" : {
          "type" : "integer"
        },
        "write-records-complete" : {
          "type" : "boolean"
        }
      }
    },
    "other-concurrent-attempts" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptDetailsInfo"
      }
    },
    "start-time" : {
      "type" : "integer"
    },
    "start_time" : {
      "type" : "integer"
    },
    "status" : {
      "type" : "string",
      "enum" : [ "CREATED", "SCHEDULED", "DEPLOYING", "RUNNING", "FINISHED", "CANCELING", "CANCELED", "FAILED", "RECONCILING", "INITIALIZING" ]
    },
    "status-duration" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "integer"
      }
    },
    "subtask" : {
      "type" : "integer"
    },
    "taskmanager-id" : {
      "type" : "string"
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid/subtasks/:subtaskindex/attempts/:attempt/accumulators

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
* subtaskindex - Positive integer value that identifies a subtask.
* attempt - Positive integer value that identifies an execution attempt.
`jobid`
`vertexid`
`subtaskindex`
`attempt`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptAccumulatorsInfo",
  "properties" : {
    "attempt" : {
      "type" : "integer"
    },
    "id" : {
      "type" : "string"
    },
    "subtask" : {
      "type" : "integer"
    },
    "user-accumulators" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:UserAccumulator",
        "properties" : {
          "name" : {
            "type" : "string"
          },
          "type" : {
            "type" : "string"
          },
          "value" : {
            "type" : "string"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:SubtaskExecutionAttemptAccumulatorsInfo",
  "properties" : {
    "attempt" : {
      "type" : "integer"
    },
    "id" : {
      "type" : "string"
    },
    "subtask" : {
      "type" : "integer"
    },
    "user-accumulators" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:UserAccumulator",
        "properties" : {
          "name" : {
            "type" : "string"
          },
          "type" : {
            "type" : "string"
          },
          "value" : {
            "type" : "string"
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid/subtasks/:subtaskindex/metrics

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
* subtaskindex - Positive integer value that identifies a subtask.
`jobid`
`vertexid`
`subtaskindex`
* get (optional): Comma-separated list of string values to select specific metrics.
`get`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /jobs/:jobid/vertices/:vertexid/subtasktimes

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:SubtasksTimesInfo",
  "properties" : {
    "id" : {
      "type" : "string"
    },
    "name" : {
      "type" : "string"
    },
    "now" : {
      "type" : "integer"
    },
    "subtasks" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:SubtasksTimesInfo:SubtaskTimeInfo",
        "properties" : {
          "duration" : {
            "type" : "integer"
          },
          "endpoint" : {
            "type" : "string"
          },
          "subtask" : {
            "type" : "integer"
          },
          "timestamps" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:SubtasksTimesInfo",
  "properties" : {
    "id" : {
      "type" : "string"
    },
    "name" : {
      "type" : "string"
    },
    "now" : {
      "type" : "integer"
    },
    "subtasks" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:SubtasksTimesInfo:SubtaskTimeInfo",
        "properties" : {
          "duration" : {
            "type" : "integer"
          },
          "endpoint" : {
            "type" : "string"
          },
          "subtask" : {
            "type" : "integer"
          },
          "timestamps" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid/taskmanagers

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexTaskManagersInfo",
  "properties" : {
    "id" : {
      "type" : "any"
    },
    "name" : {
      "type" : "string"
    },
    "now" : {
      "type" : "integer"
    },
    "taskmanagers" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexTaskManagersInfo:TaskManagersInfo",
        "properties" : {
          "aggregated" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:AggregatedTaskDetailsInfo",
            "properties" : {
              "metrics" : {
                "type" : "object",
                "additionalProperties" : {
                  "type" : "object",
                  "additionalProperties" : {
                    "type" : "integer"
                  }
                }
              },
              "status-duration" : {
                "type" : "object",
                "additionalProperties" : {
                  "type" : "object",
                  "additionalProperties" : {
                    "type" : "integer"
                  }
                }
              }
            }
          },
          "duration" : {
            "type" : "integer"
          },
          "end-time" : {
            "type" : "integer"
          },
          "endpoint" : {
            "type" : "string"
          },
          "metrics" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:metrics:IOMetricsInfo",
            "properties" : {
              "accumulated-backpressured-time" : {
                "type" : "integer"
              },
              "accumulated-busy-time" : {
                "type" : "number"
              },
              "accumulated-idle-time" : {
                "type" : "integer"
              },
              "read-bytes" : {
                "type" : "integer"
              },
              "read-bytes-complete" : {
                "type" : "boolean"
              },
              "read-records" : {
                "type" : "integer"
              },
              "read-records-complete" : {
                "type" : "boolean"
              },
              "write-bytes" : {
                "type" : "integer"
              },
              "write-bytes-complete" : {
                "type" : "boolean"
              },
              "write-records" : {
                "type" : "integer"
              },
              "write-records-complete" : {
                "type" : "boolean"
              }
            }
          },
          "start-time" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "CREATED", "SCHEDULED", "DEPLOYING", "RUNNING", "FINISHED", "CANCELING", "CANCELED", "FAILED", "RECONCILING", "INITIALIZING" ]
          },
          "status-counts" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          },
          "taskmanager-id" : {
            "type" : "string"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexTaskManagersInfo",
  "properties" : {
    "id" : {
      "type" : "any"
    },
    "name" : {
      "type" : "string"
    },
    "now" : {
      "type" : "integer"
    },
    "taskmanagers" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:JobVertexTaskManagersInfo:TaskManagersInfo",
        "properties" : {
          "aggregated" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:AggregatedTaskDetailsInfo",
            "properties" : {
              "metrics" : {
                "type" : "object",
                "additionalProperties" : {
                  "type" : "object",
                  "additionalProperties" : {
                    "type" : "integer"
                  }
                }
              },
              "status-duration" : {
                "type" : "object",
                "additionalProperties" : {
                  "type" : "object",
                  "additionalProperties" : {
                    "type" : "integer"
                  }
                }
              }
            }
          },
          "duration" : {
            "type" : "integer"
          },
          "end-time" : {
            "type" : "integer"
          },
          "endpoint" : {
            "type" : "string"
          },
          "metrics" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:metrics:IOMetricsInfo",
            "properties" : {
              "accumulated-backpressured-time" : {
                "type" : "integer"
              },
              "accumulated-busy-time" : {
                "type" : "number"
              },
              "accumulated-idle-time" : {
                "type" : "integer"
              },
              "read-bytes" : {
                "type" : "integer"
              },
              "read-bytes-complete" : {
                "type" : "boolean"
              },
              "read-records" : {
                "type" : "integer"
              },
              "read-records-complete" : {
                "type" : "boolean"
              },
              "write-bytes" : {
                "type" : "integer"
              },
              "write-bytes-complete" : {
                "type" : "boolean"
              },
              "write-records" : {
                "type" : "integer"
              },
              "write-records-complete" : {
                "type" : "boolean"
              }
            }
          },
          "start-time" : {
            "type" : "integer"
          },
          "status" : {
            "type" : "string",
            "enum" : [ "CREATED", "SCHEDULED", "DEPLOYING", "RUNNING", "FINISHED", "CANCELING", "CANCELED", "FAILED", "RECONCILING", "INITIALIZING" ]
          },
          "status-counts" : {
            "type" : "object",
            "additionalProperties" : {
              "type" : "integer"
            }
          },
          "taskmanager-id" : {
            "type" : "string"
          }
        }
      }
    }
  }
}`

##### /jobs/:jobid/vertices/:vertexid/watermarks

`GET`
`200 OK`
* jobid - 32-character hexadecimal string value that identifies a job.
* vertexid - 32-character hexadecimal string value that identifies a job vertex.
`jobid`
`vertexid`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /overview

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:legacy:messages:ClusterOverviewWithVersion",
  "properties" : {
    "flink-commit" : {
      "type" : "string"
    },
    "flink-version" : {
      "type" : "string"
    },
    "jobs-cancelled" : {
      "type" : "integer"
    },
    "jobs-failed" : {
      "type" : "integer"
    },
    "jobs-finished" : {
      "type" : "integer"
    },
    "jobs-running" : {
      "type" : "integer"
    },
    "slots-available" : {
      "type" : "integer"
    },
    "slots-free-and-blocked" : {
      "type" : "integer"
    },
    "slots-total" : {
      "type" : "integer"
    },
    "taskmanagers" : {
      "type" : "integer"
    },
    "taskmanagers-blocked" : {
      "type" : "integer"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:legacy:messages:ClusterOverviewWithVersion",
  "properties" : {
    "flink-commit" : {
      "type" : "string"
    },
    "flink-version" : {
      "type" : "string"
    },
    "jobs-cancelled" : {
      "type" : "integer"
    },
    "jobs-failed" : {
      "type" : "integer"
    },
    "jobs-finished" : {
      "type" : "integer"
    },
    "jobs-running" : {
      "type" : "integer"
    },
    "slots-available" : {
      "type" : "integer"
    },
    "slots-free-and-blocked" : {
      "type" : "integer"
    },
    "slots-total" : {
      "type" : "integer"
    },
    "taskmanagers" : {
      "type" : "integer"
    },
    "taskmanagers-blocked" : {
      "type" : "integer"
    }
  }
}`

##### /savepoint-disposal

`POST`
`200 OK`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:savepoints:SavepointDisposalRequest",
  "properties" : {
    "savepoint-path" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:job:savepoints:SavepointDisposalRequest",
  "properties" : {
    "savepoint-path" : {
      "type" : "string"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:TriggerResponse",
  "properties" : {
    "request-id" : {
      "type" : "any"
    }
  }
}`

##### /savepoint-disposal/:triggerid

`GET`
`200 OK`
* triggerid - 32-character hexadecimal string that identifies an asynchronous operation trigger ID. The ID was returned then the operation was triggered.
`triggerid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationResult",
  "properties" : {
    "operation" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationInfo",
      "properties" : {
        "failure-cause" : {
          "type" : "any"
        }
      }
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationResult",
  "properties" : {
    "operation" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:handler:async:AsynchronousOperationInfo",
      "properties" : {
        "failure-cause" : {
          "type" : "any"
        }
      }
    },
    "status" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:queue:QueueStatus",
      "properties" : {
        "id" : {
          "type" : "string",
          "required" : true,
          "enum" : [ "IN_PROGRESS", "COMPLETED" ]
        }
      }
    }
  }
}`

##### /taskmanagers

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:TaskManagersInfo",
  "properties" : {
    "taskmanagers" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:TaskManagerInfo",
        "properties" : {
          "blocked" : {
            "type" : "boolean"
          },
          "dataPort" : {
            "type" : "integer"
          },
          "freeResource" : {
            "type" : "object",
            "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ResourceProfileInfo"
          },
          "freeSlots" : {
            "type" : "integer"
          },
          "hardware" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:instance:HardwareDescription",
            "properties" : {
              "cpuCores" : {
                "type" : "integer"
              },
              "freeMemory" : {
                "type" : "integer"
              },
              "managedMemory" : {
                "type" : "integer"
              },
              "physicalMemory" : {
                "type" : "integer"
              }
            }
          },
          "id" : {
            "type" : "any"
          },
          "jmxPort" : {
            "type" : "integer"
          },
          "memoryConfiguration" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:taskexecutor:TaskExecutorMemoryConfiguration",
            "properties" : {
              "frameworkHeap" : {
                "type" : "integer"
              },
              "frameworkOffHeap" : {
                "type" : "integer"
              },
              "jvmMetaspace" : {
                "type" : "integer"
              },
              "jvmOverhead" : {
                "type" : "integer"
              },
              "managedMemory" : {
                "type" : "integer"
              },
              "networkMemory" : {
                "type" : "integer"
              },
              "taskHeap" : {
                "type" : "integer"
              },
              "taskOffHeap" : {
                "type" : "integer"
              },
              "totalFlinkMemory" : {
                "type" : "integer"
              },
              "totalProcessMemory" : {
                "type" : "integer"
              }
            }
          },
          "path" : {
            "type" : "string"
          },
          "slotsNumber" : {
            "type" : "integer"
          },
          "timeSinceLastHeartbeat" : {
            "type" : "integer"
          },
          "totalResource" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ResourceProfileInfo",
            "properties" : {
              "cpuCores" : {
                "type" : "number"
              },
              "extendedResources" : {
                "type" : "object",
                "additionalProperties" : {
                  "type" : "number"
                }
              },
              "managedMemory" : {
                "type" : "integer"
              },
              "networkMemory" : {
                "type" : "integer"
              },
              "taskHeapMemory" : {
                "type" : "integer"
              },
              "taskOffHeapMemory" : {
                "type" : "integer"
              }
            }
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:TaskManagersInfo",
  "properties" : {
    "taskmanagers" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:TaskManagerInfo",
        "properties" : {
          "blocked" : {
            "type" : "boolean"
          },
          "dataPort" : {
            "type" : "integer"
          },
          "freeResource" : {
            "type" : "object",
            "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ResourceProfileInfo"
          },
          "freeSlots" : {
            "type" : "integer"
          },
          "hardware" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:instance:HardwareDescription",
            "properties" : {
              "cpuCores" : {
                "type" : "integer"
              },
              "freeMemory" : {
                "type" : "integer"
              },
              "managedMemory" : {
                "type" : "integer"
              },
              "physicalMemory" : {
                "type" : "integer"
              }
            }
          },
          "id" : {
            "type" : "any"
          },
          "jmxPort" : {
            "type" : "integer"
          },
          "memoryConfiguration" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:taskexecutor:TaskExecutorMemoryConfiguration",
            "properties" : {
              "frameworkHeap" : {
                "type" : "integer"
              },
              "frameworkOffHeap" : {
                "type" : "integer"
              },
              "jvmMetaspace" : {
                "type" : "integer"
              },
              "jvmOverhead" : {
                "type" : "integer"
              },
              "managedMemory" : {
                "type" : "integer"
              },
              "networkMemory" : {
                "type" : "integer"
              },
              "taskHeap" : {
                "type" : "integer"
              },
              "taskOffHeap" : {
                "type" : "integer"
              },
              "totalFlinkMemory" : {
                "type" : "integer"
              },
              "totalProcessMemory" : {
                "type" : "integer"
              }
            }
          },
          "path" : {
            "type" : "string"
          },
          "slotsNumber" : {
            "type" : "integer"
          },
          "timeSinceLastHeartbeat" : {
            "type" : "integer"
          },
          "totalResource" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ResourceProfileInfo",
            "properties" : {
              "cpuCores" : {
                "type" : "number"
              },
              "extendedResources" : {
                "type" : "object",
                "additionalProperties" : {
                  "type" : "number"
                }
              },
              "managedMemory" : {
                "type" : "integer"
              },
              "networkMemory" : {
                "type" : "integer"
              },
              "taskHeapMemory" : {
                "type" : "integer"
              },
              "taskOffHeapMemory" : {
                "type" : "integer"
              }
            }
          }
        }
      }
    }
  }
}`

##### /taskmanagers/metrics

`GET`
`200 OK`
* get (optional): Comma-separated list of string values to select specific metrics.
* agg (optional): Comma-separated list of aggregation modes which should be calculated. Available aggregations are: "min, max, sum, avg, skew".
* taskmanagers (optional): Comma-separated list of 32-character hexadecimal strings to select specific task managers.
`get`
`agg`
`taskmanagers`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /taskmanagers/:taskmanagerid

`GET`
`200 OK`
* taskmanagerid - 32-character hexadecimal string that identifies a task manager.
`taskmanagerid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:TaskManagerDetailsInfo",
  "properties" : {
    "allocatedSlots" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:SlotInfo",
        "properties" : {
          "jobId" : {
            "type" : "any"
          },
          "resource" : {
            "type" : "object",
            "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ResourceProfileInfo"
          }
        }
      }
    },
    "blocked" : {
      "type" : "boolean"
    },
    "dataPort" : {
      "type" : "integer"
    },
    "freeResource" : {
      "type" : "object",
      "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ResourceProfileInfo"
    },
    "freeSlots" : {
      "type" : "integer"
    },
    "hardware" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:instance:HardwareDescription",
      "properties" : {
        "cpuCores" : {
          "type" : "integer"
        },
        "freeMemory" : {
          "type" : "integer"
        },
        "managedMemory" : {
          "type" : "integer"
        },
        "physicalMemory" : {
          "type" : "integer"
        }
      }
    },
    "id" : {
      "type" : "any"
    },
    "jmxPort" : {
      "type" : "integer"
    },
    "memoryConfiguration" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:taskexecutor:TaskExecutorMemoryConfiguration",
      "properties" : {
        "frameworkHeap" : {
          "type" : "integer"
        },
        "frameworkOffHeap" : {
          "type" : "integer"
        },
        "jvmMetaspace" : {
          "type" : "integer"
        },
        "jvmOverhead" : {
          "type" : "integer"
        },
        "managedMemory" : {
          "type" : "integer"
        },
        "networkMemory" : {
          "type" : "integer"
        },
        "taskHeap" : {
          "type" : "integer"
        },
        "taskOffHeap" : {
          "type" : "integer"
        },
        "totalFlinkMemory" : {
          "type" : "integer"
        },
        "totalProcessMemory" : {
          "type" : "integer"
        }
      }
    },
    "metrics" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:TaskManagerMetricsInfo",
      "properties" : {
        "directCount" : {
          "type" : "integer"
        },
        "directMax" : {
          "type" : "integer"
        },
        "directUsed" : {
          "type" : "integer"
        },
        "garbageCollectors" : {
          "type" : "array",
          "items" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:TaskManagerMetricsInfo:GarbageCollectorInfo",
            "properties" : {
              "count" : {
                "type" : "integer"
              },
              "name" : {
                "type" : "string"
              },
              "time" : {
                "type" : "integer"
              }
            }
          }
        },
        "heapCommitted" : {
          "type" : "integer"
        },
        "heapMax" : {
          "type" : "integer"
        },
        "heapUsed" : {
          "type" : "integer"
        },
        "mappedCount" : {
          "type" : "integer"
        },
        "mappedMax" : {
          "type" : "integer"
        },
        "mappedUsed" : {
          "type" : "integer"
        },
        "nettyShuffleMemoryAvailable" : {
          "type" : "integer"
        },
        "nettyShuffleMemorySegmentsAvailable" : {
          "type" : "integer"
        },
        "nettyShuffleMemorySegmentsTotal" : {
          "type" : "integer"
        },
        "nettyShuffleMemorySegmentsUsed" : {
          "type" : "integer"
        },
        "nettyShuffleMemoryTotal" : {
          "type" : "integer"
        },
        "nettyShuffleMemoryUsed" : {
          "type" : "integer"
        },
        "nonHeapCommitted" : {
          "type" : "integer"
        },
        "nonHeapMax" : {
          "type" : "integer"
        },
        "nonHeapUsed" : {
          "type" : "integer"
        }
      }
    },
    "path" : {
      "type" : "string"
    },
    "slotsNumber" : {
      "type" : "integer"
    },
    "timeSinceLastHeartbeat" : {
      "type" : "integer"
    },
    "totalResource" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ResourceProfileInfo",
      "properties" : {
        "cpuCores" : {
          "type" : "number"
        },
        "extendedResources" : {
          "type" : "object",
          "additionalProperties" : {
            "type" : "number"
          }
        },
        "managedMemory" : {
          "type" : "integer"
        },
        "networkMemory" : {
          "type" : "integer"
        },
        "taskHeapMemory" : {
          "type" : "integer"
        },
        "taskOffHeapMemory" : {
          "type" : "integer"
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:TaskManagerDetailsInfo",
  "properties" : {
    "allocatedSlots" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:SlotInfo",
        "properties" : {
          "jobId" : {
            "type" : "any"
          },
          "resource" : {
            "type" : "object",
            "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ResourceProfileInfo"
          }
        }
      }
    },
    "blocked" : {
      "type" : "boolean"
    },
    "dataPort" : {
      "type" : "integer"
    },
    "freeResource" : {
      "type" : "object",
      "$ref" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ResourceProfileInfo"
    },
    "freeSlots" : {
      "type" : "integer"
    },
    "hardware" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:instance:HardwareDescription",
      "properties" : {
        "cpuCores" : {
          "type" : "integer"
        },
        "freeMemory" : {
          "type" : "integer"
        },
        "managedMemory" : {
          "type" : "integer"
        },
        "physicalMemory" : {
          "type" : "integer"
        }
      }
    },
    "id" : {
      "type" : "any"
    },
    "jmxPort" : {
      "type" : "integer"
    },
    "memoryConfiguration" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:taskexecutor:TaskExecutorMemoryConfiguration",
      "properties" : {
        "frameworkHeap" : {
          "type" : "integer"
        },
        "frameworkOffHeap" : {
          "type" : "integer"
        },
        "jvmMetaspace" : {
          "type" : "integer"
        },
        "jvmOverhead" : {
          "type" : "integer"
        },
        "managedMemory" : {
          "type" : "integer"
        },
        "networkMemory" : {
          "type" : "integer"
        },
        "taskHeap" : {
          "type" : "integer"
        },
        "taskOffHeap" : {
          "type" : "integer"
        },
        "totalFlinkMemory" : {
          "type" : "integer"
        },
        "totalProcessMemory" : {
          "type" : "integer"
        }
      }
    },
    "metrics" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:TaskManagerMetricsInfo",
      "properties" : {
        "directCount" : {
          "type" : "integer"
        },
        "directMax" : {
          "type" : "integer"
        },
        "directUsed" : {
          "type" : "integer"
        },
        "garbageCollectors" : {
          "type" : "array",
          "items" : {
            "type" : "object",
            "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:taskmanager:TaskManagerMetricsInfo:GarbageCollectorInfo",
            "properties" : {
              "count" : {
                "type" : "integer"
              },
              "name" : {
                "type" : "string"
              },
              "time" : {
                "type" : "integer"
              }
            }
          }
        },
        "heapCommitted" : {
          "type" : "integer"
        },
        "heapMax" : {
          "type" : "integer"
        },
        "heapUsed" : {
          "type" : "integer"
        },
        "mappedCount" : {
          "type" : "integer"
        },
        "mappedMax" : {
          "type" : "integer"
        },
        "mappedUsed" : {
          "type" : "integer"
        },
        "nettyShuffleMemoryAvailable" : {
          "type" : "integer"
        },
        "nettyShuffleMemorySegmentsAvailable" : {
          "type" : "integer"
        },
        "nettyShuffleMemorySegmentsTotal" : {
          "type" : "integer"
        },
        "nettyShuffleMemorySegmentsUsed" : {
          "type" : "integer"
        },
        "nettyShuffleMemoryTotal" : {
          "type" : "integer"
        },
        "nettyShuffleMemoryUsed" : {
          "type" : "integer"
        },
        "nonHeapCommitted" : {
          "type" : "integer"
        },
        "nonHeapMax" : {
          "type" : "integer"
        },
        "nonHeapUsed" : {
          "type" : "integer"
        }
      }
    },
    "path" : {
      "type" : "string"
    },
    "slotsNumber" : {
      "type" : "integer"
    },
    "timeSinceLastHeartbeat" : {
      "type" : "integer"
    },
    "totalResource" : {
      "type" : "object",
      "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ResourceProfileInfo",
      "properties" : {
        "cpuCores" : {
          "type" : "number"
        },
        "extendedResources" : {
          "type" : "object",
          "additionalProperties" : {
            "type" : "number"
          }
        },
        "managedMemory" : {
          "type" : "integer"
        },
        "networkMemory" : {
          "type" : "integer"
        },
        "taskHeapMemory" : {
          "type" : "integer"
        },
        "taskOffHeapMemory" : {
          "type" : "integer"
        }
      }
    }
  }
}`

##### /taskmanagers/:taskmanagerid/logs

`GET`
`200 OK`
* taskmanagerid - 32-character hexadecimal string that identifies a task manager.
`taskmanagerid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogListInfo",
  "properties" : {
    "logs" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogInfo",
        "properties" : {
          "mtime" : {
            "type" : "integer"
          },
          "name" : {
            "type" : "string"
          },
          "size" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogListInfo",
  "properties" : {
    "logs" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:LogInfo",
        "properties" : {
          "mtime" : {
            "type" : "integer"
          },
          "name" : {
            "type" : "string"
          },
          "size" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}`

##### /taskmanagers/:taskmanagerid/metrics

`GET`
`200 OK`
* taskmanagerid - 32-character hexadecimal string that identifies a task manager.
`taskmanagerid`
* get (optional): Comma-separated list of string values to select specific metrics.
`get`

```
{}
```

`{}`

```
{
  "type" : "any"
}
```

`{
  "type" : "any"
}`

##### /taskmanagers/:taskmanagerid/thread-dump

`GET`
`200 OK`
* taskmanagerid - 32-character hexadecimal string that identifies a task manager.
`taskmanagerid`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ThreadDumpInfo",
  "properties" : {
    "threadInfos" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ThreadDumpInfo:ThreadInfo",
        "properties" : {
          "stringifiedThreadInfo" : {
            "type" : "string"
          },
          "threadName" : {
            "type" : "string"
          }
        }
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ThreadDumpInfo",
  "properties" : {
    "threadInfos" : {
      "type" : "array",
      "items" : {
        "type" : "object",
        "id" : "urn:jsonschema:org:apache:flink:runtime:rest:messages:ThreadDumpInfo:ThreadInfo",
        "properties" : {
          "stringifiedThreadInfo" : {
            "type" : "string"
          },
          "threadName" : {
            "type" : "string"
          }
        }
      }
    }
  }
}`