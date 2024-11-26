# REST Endpoint


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# REST Endpoint#


The REST endpoint allows user to connect to SQL Gateway with REST API.


## Overview of SQL Processing#


### Open Session#


When the client connects to the SQL Gateway, the SQL Gateway creates a Session as the context to store the users-specified information
during the interactions between the client and SQL Gateway. After the creation of the Session, the SQL Gateway server returns an identifier named
SessionHandle for later interactions.

`Session`
`Session`
`SessionHandle`

### Submit SQL#


After the registration of the Session, the client can submit the SQL to the SQL Gateway server. When submitting the SQL,
the SQL is translated to an Operation and an identifier named OperationHandle is returned for fetch results later. The Operation has
its lifecycle, the client is able to cancel the execution of the Operation or close the Operation to release the resources used by the Operation.

`Session`
`Operation`
`OperationHandle`
`Operation`
`Operation`
`Operation`

### Fetch Results#


With the OperationHandle, the client can fetch the results from the Operation. If the Operation is ready, the SQL Gateway will return a batch
of the data with the corresponding schema and a URI that is used to fetch the next batch of the data. When all results have been fetched, the
SQL Gateway will fill the resultType in the response with value EOS and the URI to the next batch of the data is null.

`OperationHandle`
`Operation`
`Operation`
`resultType`
`EOS`

## Endpoint Options#


##### sql-gateway.endpoint.rest.address


##### sql-gateway.endpoint.rest.bind-address


##### sql-gateway.endpoint.rest.bind-port


##### sql-gateway.endpoint.rest.port


## REST API#


The available OpenAPI specification is as follows. The default version is v3.


> 
  The OpenAPI specification is still experimental.



#### API reference#


##### /api_versions

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetApiVersionResponseBody",
  "properties" : {
    "versions" : {
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
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetApiVersionResponseBody",
  "properties" : {
    "versions" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    }
  }
}`

##### /info

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetInfoResponseBody",
  "properties" : {
    "productName" : {
      "type" : "string"
    },
    "version" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetInfoResponseBody",
  "properties" : {
    "productName" : {
      "type" : "string"
    },
    "version" : {
      "type" : "string"
    }
  }
}`

##### /sessions

`POST`
`200 OK`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionRequestBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "sessionName" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionRequestBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "sessionName" : {
      "type" : "string"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionResponseBody",
  "properties" : {
    "sessionHandle" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionResponseBody",
  "properties" : {
    "sessionHandle" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle

`DELETE`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:CloseSessionResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:CloseSessionResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:GetSessionConfigResponseBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:GetSessionConfigResponseBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    }
  }
}`

##### /sessions/:session_handle/complete-statement

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:CompleteStatementRequestBody",
  "properties" : {
    "position" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:CompleteStatementRequestBody",
  "properties" : {
    "position" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:CompleteStatementResponseBody",
  "properties" : {
    "candidates" : {
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
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:CompleteStatementResponseBody",
  "properties" : {
    "candidates" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    }
  }
}`

##### /sessions/:session_handle/configure-session

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:ConfigureSessionRequestBody",
  "properties" : {
    "executionTimeout" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:ConfigureSessionRequestBody",
  "properties" : {
    "executionTimeout" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}`

```
{}
```

`{}`

##### /sessions/:session_handle/heartbeat

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{}
```

`{}`

```
{}
```

`{}`

##### /sessions/:session_handle/materialized-tables/:identifier/refresh

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* identifier - The fully qualified string that identifies a materialized table.
`session_handle`
`identifier`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:materializedtable:RefreshMaterializedTableRequestBody",
  "properties" : {
    "dynamicOptions" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "executionConfig" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "isPeriodic" : {
      "type" : "boolean"
    },
    "periodic" : {
      "type" : "boolean"
    },
    "scheduleTime" : {
      "type" : "string"
    },
    "staticPartitions" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:materializedtable:RefreshMaterializedTableRequestBody",
  "properties" : {
    "dynamicOptions" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "executionConfig" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "isPeriodic" : {
      "type" : "boolean"
    },
    "periodic" : {
      "type" : "boolean"
    },
    "scheduleTime" : {
      "type" : "string"
    },
    "staticPartitions" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:materializedtable:RefreshMaterializedTableResponseBody",
  "properties" : {
    "operationHandle" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:materializedtable:RefreshMaterializedTableResponseBody",
  "properties" : {
    "operationHandle" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle/operations/:operation_handle/cancel

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
`session_handle`
`operation_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle/operations/:operation_handle/close

`DELETE`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
`session_handle`
`operation_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle/operations/:operation_handle/result/:token

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
* token - The token that identifies which batch of data to fetch.
`session_handle`
`operation_handle`
`token`
* rowFormat (mandatory): The row format to serialize the RowData.
`rowFormat`

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

##### /sessions/:session_handle/operations/:operation_handle/status

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
`session_handle`
`operation_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle/statements

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementRequestBody",
  "properties" : {
    "executionConfig" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "executionTimeout" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementRequestBody",
  "properties" : {
    "executionConfig" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "executionTimeout" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementResponseBody",
  "properties" : {
    "operationHandle" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementResponseBody",
  "properties" : {
    "operationHandle" : {
      "type" : "string"
    }
  }
}`

##### /api_versions

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetApiVersionResponseBody",
  "properties" : {
    "versions" : {
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
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetApiVersionResponseBody",
  "properties" : {
    "versions" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    }
  }
}`

##### /info

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetInfoResponseBody",
  "properties" : {
    "productName" : {
      "type" : "string"
    },
    "version" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetInfoResponseBody",
  "properties" : {
    "productName" : {
      "type" : "string"
    },
    "version" : {
      "type" : "string"
    }
  }
}`

##### /sessions

`POST`
`200 OK`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionRequestBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "sessionName" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionRequestBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "sessionName" : {
      "type" : "string"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionResponseBody",
  "properties" : {
    "sessionHandle" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionResponseBody",
  "properties" : {
    "sessionHandle" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle

`DELETE`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:CloseSessionResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:CloseSessionResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:GetSessionConfigResponseBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:GetSessionConfigResponseBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    }
  }
}`

##### /sessions/:session_handle/complete-statement

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:CompleteStatementRequestBody",
  "properties" : {
    "position" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:CompleteStatementRequestBody",
  "properties" : {
    "position" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:CompleteStatementResponseBody",
  "properties" : {
    "candidates" : {
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
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:CompleteStatementResponseBody",
  "properties" : {
    "candidates" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    }
  }
}`

##### /sessions/:session_handle/configure-session

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:ConfigureSessionRequestBody",
  "properties" : {
    "executionTimeout" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:ConfigureSessionRequestBody",
  "properties" : {
    "executionTimeout" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}`

```
{}
```

`{}`

##### /sessions/:session_handle/heartbeat

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{}
```

`{}`

```
{}
```

`{}`

##### /sessions/:session_handle/operations/:operation_handle/cancel

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
`session_handle`
`operation_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle/operations/:operation_handle/close

`DELETE`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
`session_handle`
`operation_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle/operations/:operation_handle/result/:token

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
* token - The token that identifies which batch of data to fetch.
`session_handle`
`operation_handle`
`token`
* rowFormat (mandatory): The row format to serialize the RowData.
`rowFormat`

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

##### /sessions/:session_handle/operations/:operation_handle/status

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
`session_handle`
`operation_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle/statements

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementRequestBody",
  "properties" : {
    "executionConfig" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "executionTimeout" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementRequestBody",
  "properties" : {
    "executionConfig" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "executionTimeout" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementResponseBody",
  "properties" : {
    "operationHandle" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementResponseBody",
  "properties" : {
    "operationHandle" : {
      "type" : "string"
    }
  }
}`

##### /api_versions

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetApiVersionResponseBody",
  "properties" : {
    "versions" : {
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
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetApiVersionResponseBody",
  "properties" : {
    "versions" : {
      "type" : "array",
      "items" : {
        "type" : "string"
      }
    }
  }
}`

##### /info

`GET`
`200 OK`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetInfoResponseBody",
  "properties" : {
    "productName" : {
      "type" : "string"
    },
    "version" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:util:GetInfoResponseBody",
  "properties" : {
    "productName" : {
      "type" : "string"
    },
    "version" : {
      "type" : "string"
    }
  }
}`

##### /sessions

`POST`
`200 OK`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionRequestBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "sessionName" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionRequestBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "sessionName" : {
      "type" : "string"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionResponseBody",
  "properties" : {
    "sessionHandle" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:OpenSessionResponseBody",
  "properties" : {
    "sessionHandle" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle

`DELETE`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:CloseSessionResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:CloseSessionResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:GetSessionConfigResponseBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:session:GetSessionConfigResponseBody",
  "properties" : {
    "properties" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    }
  }
}`

##### /sessions/:session_handle/heartbeat

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{}
```

`{}`

```
{}
```

`{}`

##### /sessions/:session_handle/operations/:operation_handle/cancel

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
`session_handle`
`operation_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle/operations/:operation_handle/close

`DELETE`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
`session_handle`
`operation_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle/operations/:operation_handle/result/:token

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
* token - The token that identifies which batch of data to fetch.
`session_handle`
`operation_handle`
`token`

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

##### /sessions/:session_handle/operations/:operation_handle/status

`GET`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
* operation_handle - The OperationHandle that identifies a operation.
`session_handle`
`operation_handle`

```
{}
```

`{}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:operation:OperationStatusResponseBody",
  "properties" : {
    "status" : {
      "type" : "string"
    }
  }
}`

##### /sessions/:session_handle/statements

`POST`
`200 OK`
* session_handle - The SessionHandle that identifies a session.
`session_handle`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementRequestBody",
  "properties" : {
    "executionConfig" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "executionTimeout" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementRequestBody",
  "properties" : {
    "executionConfig" : {
      "type" : "object",
      "additionalProperties" : {
        "type" : "string"
      }
    },
    "executionTimeout" : {
      "type" : "integer"
    },
    "statement" : {
      "type" : "string"
    }
  }
}`

```
{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementResponseBody",
  "properties" : {
    "operationHandle" : {
      "type" : "string"
    }
  }
}
```

`{
  "type" : "object",
  "id" : "urn:jsonschema:org:apache:flink:table:gateway:rest:message:statement:ExecuteStatementResponseBody",
  "properties" : {
    "operationHandle" : {
      "type" : "string"
    }
  }
}`

## Data Type Mapping#


Currently, REST endpoint supports to serialize the RowData with query parameter rowFormat. REST endpoint uses JSON format to serialize
the Table Objects. Please refer JSON format to the mappings.

`RowData`
`rowFormat`

REST endpoint also supports to serialize the RowData with PLAIN_TEXT format that automatically cast all columns to the String.

`RowData`
`PLAIN_TEXT`
`String`

 Back to top
