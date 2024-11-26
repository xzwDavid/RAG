# Kubernetes HA Services


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Kubernetes HA Services#


Flink’s Kubernetes HA services use Kubernetes for high availability services.


Kubernetes high availability services can only be used when deploying to Kubernetes.
Consequently, they can be configured when using standalone Flink on Kubernetes or the native Kubernetes integration


## Prerequisites#


In order to use Flink’s Kubernetes HA services you must fulfill the following prerequisites:

* Kubernetes >= 1.9.
* Service account with permissions to create, edit, delete ConfigMaps.
Take a look at how to configure a service account for Flink’s native Kubernetes integration and standalone Flink on Kubernetes for more information.

## Configuration#


In order to start an HA-cluster you have to configure the following configuration keys:

* high-availability.type (required):
The high-availability.type option has to be set to kubernetes.
`high-availability.type`
`kubernetes`

```
high-availability.type: kubernetes

```

`high-availability.type: kubernetes
`
* high-availability.storageDir (required):
JobManager metadata is persisted in the file system high-availability.storageDir and only a pointer to this state is stored in Kubernetes.
`high-availability.storageDir`

```
high-availability.storageDir: s3://flink/recovery

```

`high-availability.storageDir: s3://flink/recovery
`

The storageDir stores all metadata needed to recover a JobManager failure.

`storageDir`
* kubernetes.cluster-id (required):
In order to identify the Flink cluster, you have to specify a kubernetes.cluster-id.
`kubernetes.cluster-id`

```
kubernetes.cluster-id: cluster1337

```

`kubernetes.cluster-id: cluster1337
`

### Example configuration#


Configure high availability mode in Flink configuration file:


```
kubernetes.cluster-id: <cluster-id>
high-availability.type: kubernetes
high-availability.storageDir: hdfs:///flink/recovery

```

`kubernetes.cluster-id: <cluster-id>
high-availability.type: kubernetes
high-availability.storageDir: hdfs:///flink/recovery
`

 Back to top


## High availability data clean up#


To keep HA data while restarting the Flink cluster, simply delete the deployment (via kubectl delete deployment <cluster-id>).
All the Flink cluster related resources will be deleted (e.g. JobManager Deployment, TaskManager pods, services, Flink conf ConfigMap).
HA related ConfigMaps will be retained because they do not set the owner reference.
When restarting the cluster, all previously running jobs will be recovered and restarted from the latest successful checkpoint.

`kubectl delete deployment <cluster-id>`

 Back to top
