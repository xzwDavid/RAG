# Job Status Changed Listener


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


## Job status changed listener#


Flink provides a pluggable interface for users to register their custom logic for handling with the job status changes in which lineage info about source/sink is provided.
This enables users to implement their own flink lineage reporter to send lineage info to third party data lineage systems for example Datahub and Openlineage.


The job status changed listeners are triggered every time status change happened for the application. The data lineage info is included in the JobCreatedEvent.


### Implement a plugin for your custom enricher#


To implement a custom JobStatusChangedListener plugin, you need to:

* 
Add your own JobStatusChangedListener by implementing the 

    JobStatusChangedListener

 interface.

* 
Add your own JobStatusChangedListenerFactory by implementing the 

    JobStatusChangedListenerFactory

 interface.

* 
Add a service entry. Create a file META-INF/services/org.apache.flink.core.execution.JobStatusChangedListenerFactory which contains the class name of your job status changed listener factory class (see Java Service Loader docs for more details).


Add your own JobStatusChangedListener by implementing the 

    JobStatusChangedListener

 interface.


Add your own JobStatusChangedListenerFactory by implementing the 

    JobStatusChangedListenerFactory

 interface.


Add a service entry. Create a file META-INF/services/org.apache.flink.core.execution.JobStatusChangedListenerFactory which contains the class name of your job status changed listener factory class (see Java Service Loader docs for more details).

`META-INF/services/org.apache.flink.core.execution.JobStatusChangedListenerFactory`

Then, create a jar which includes your JobStatusChangedListener, JobStatusChangedListenerFactory, META-INF/services/ and all external dependencies.
Make a directory in plugins/ of your Flink distribution with an arbitrary name, e.g. “job-status-changed-listener”, and put the jar into this directory.
See Flink Plugin for more details.

`JobStatusChangedListener`
`JobStatusChangedListenerFactory`
`META-INF/services/`
`plugins/`

JobStatusChangedListenerFactory example:


```
package org.apache.flink.test.execution;

public static class TestingJobStatusChangedListenerFactory
        implements JobStatusChangedListenerFactory {

    @Override
    public JobStatusChangedListener createListener(Context context) {
        return new TestingJobStatusChangedListener();
    }
}

```

`package org.apache.flink.test.execution;

public static class TestingJobStatusChangedListenerFactory
        implements JobStatusChangedListenerFactory {

    @Override
    public JobStatusChangedListener createListener(Context context) {
        return new TestingJobStatusChangedListener();
    }
}
`

JobStatusChangedListener example:


```
package org.apache.flink.test.execution;

private static class TestingJobStatusChangedListener implements JobStatusChangedListener {

    @Override
    public void onEvent(JobStatusChangedEvent event) {
        statusChangedEvents.add(event);
    }
}

```

`package org.apache.flink.test.execution;

private static class TestingJobStatusChangedListener implements JobStatusChangedListener {

    @Override
    public void onEvent(JobStatusChangedEvent event) {
        statusChangedEvents.add(event);
    }
}
`

### Configuration#


Flink components loads JobStatusChangedListener plugins at startup. To make sure your JobStatusChangedListeners are loaded all class names should be defined as part of execution.job-status-changed-listeners.
If this configuration is empty, NO enrichers will be started. Example:


```
    execution.job-status-changed-listeners = org.apache.flink.test.execution.TestingJobStatusChangedListenerFactory

```

`    execution.job-status-changed-listeners = org.apache.flink.test.execution.TestingJobStatusChangedListenerFactory
`