# Native Kubernetes


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Native Kubernetes#


This page describes how to deploy Flink natively on Kubernetes.


## Getting Started#


This Getting Started section guides you through setting up a fully functional Flink Cluster on Kubernetes.


### Introduction#


Kubernetes is a popular container-orchestration system for automating computer application deployment, scaling, and management.
Flink’s native Kubernetes integration allows you to directly deploy Flink on a running Kubernetes cluster.
Moreover, Flink is able to dynamically allocate and de-allocate TaskManagers depending on the required resources because it can directly talk to Kubernetes.


Apache Flink also provides a Kubernetes operator for managing Flink clusters on Kubernetes. It supports both standalone and native deployment mode and greatly simplifies deployment, configuration and the life cycle management of Flink resources on Kubernetes.


For more information, please refer to the Flink Kubernetes Operator documentation


### Preparation#


The Getting Started section assumes a running Kubernetes cluster fulfilling the following requirements:

* Kubernetes >= 1.9.
* KubeConfig, which has access to list, create, delete pods and services, configurable via ~/.kube/config. You can verify permissions by running kubectl auth can-i <list|create|edit|delete> pods.
* Enabled Kubernetes DNS.
* default service account with RBAC permissions to create, delete pods.
`~/.kube/config`
`kubectl auth can-i <list|create|edit|delete> pods`
`default`

If you have problems setting up a Kubernetes cluster, then take a look at how to setup a Kubernetes cluster.


### Starting a Flink Session on Kubernetes#


Once you have your Kubernetes cluster running and kubectl is configured to point to it, you can launch a Flink cluster in Session Mode via

`kubectl`

```
# (1) Start Kubernetes session
$ ./bin/kubernetes-session.sh -Dkubernetes.cluster-id=my-first-flink-cluster

# (2) Submit example job
$ ./bin/flink run \
    --target kubernetes-session \
    -Dkubernetes.cluster-id=my-first-flink-cluster \
    ./examples/streaming/TopSpeedWindowing.jar

# (3) Stop Kubernetes session by deleting cluster deployment
$ kubectl delete deployment/my-first-flink-cluster

```

`# (1) Start Kubernetes session
$ ./bin/kubernetes-session.sh -Dkubernetes.cluster-id=my-first-flink-cluster

# (2) Submit example job
$ ./bin/flink run \
    --target kubernetes-session \
    -Dkubernetes.cluster-id=my-first-flink-cluster \
    ./examples/streaming/TopSpeedWindowing.jar

# (3) Stop Kubernetes session by deleting cluster deployment
$ kubectl delete deployment/my-first-flink-cluster
`

> 
  In default, Flinkâs Web UI and REST endpoint are exposed as ClusterIP service. To access the service, please refer to Accessing Flinkâs Web UI for instructions.


`ClusterIP`

Congratulations! You have successfully run a Flink application by deploying Flink on Kubernetes.


 Back to top


## Deployment Modes#


For production use, we recommend deploying Flink Applications in the Application Mode, as these modes provide a better isolation for the Applications.


### Application Mode#


> 
  For high-level intuition behind the application mode, please refer to the deployment mode overview.



The Application Mode requires that the user code is bundled together with the Flink image because it runs the user code’s main() method on the cluster.
The Application Mode makes sure that all Flink components are properly cleaned up after the termination of the application.
Bundling can be done by modifying the base Flink Docker image, or via the User Artifact Management, which makes it possible to upload and download artifacts that are not available locally.

`main()`

#### Modify the Docker image#


The Flink community provides a base Docker image which can be used to bundle the user code:


```
FROM flink
RUN mkdir -p $FLINK_HOME/usrlib
COPY /path/of/my-flink-job.jar $FLINK_HOME/usrlib/my-flink-job.jar

```

`FROM flink
RUN mkdir -p $FLINK_HOME/usrlib
COPY /path/of/my-flink-job.jar $FLINK_HOME/usrlib/my-flink-job.jar
`

After creating and publishing the Docker image under custom-image-name, you can start an Application cluster with the following command:

`custom-image-name`

```
$ ./bin/flink run \
    --target kubernetes-application \
    -Dkubernetes.cluster-id=my-first-application-cluster \
    -Dkubernetes.container.image.ref=custom-image-name \
    local:///opt/flink/usrlib/my-flink-job.jar

```

`$ ./bin/flink run \
    --target kubernetes-application \
    -Dkubernetes.cluster-id=my-first-application-cluster \
    -Dkubernetes.container.image.ref=custom-image-name \
    local:///opt/flink/usrlib/my-flink-job.jar
`

#### Configure User Artifact Management#


In case you have a locally available Flink job JAR, artifact upload can be used so Flink will upload the local artifact to DFS during deployment and fetch it on the deployed JobManager pod:


```
$ ./bin/flink run \
    --target kubernetes-application \
    -Dkubernetes.cluster-id=my-first-application-cluster \
    -Dkubernetes.container.image=custom-image-name \
    -Dkubernetes.artifacts.local-upload-enabled=true \
    -Dkubernetes.artifacts.local-upload-target=s3://my-bucket/ \
    local:///tmp/my-flink-job.jar

```

`$ ./bin/flink run \
    --target kubernetes-application \
    -Dkubernetes.cluster-id=my-first-application-cluster \
    -Dkubernetes.container.image=custom-image-name \
    -Dkubernetes.artifacts.local-upload-enabled=true \
    -Dkubernetes.artifacts.local-upload-target=s3://my-bucket/ \
    local:///tmp/my-flink-job.jar
`

The kubernetes.artifacts.local-upload-enabled enables this feature, and kubernetes.artifacts.local-upload-target has to point to a valid remote target that exists and has the permissions configured properly.
You can add additional artifacts via the user.artifacts.artifact-list config option, which can contain a mix of local and remote artifacts:

`kubernetes.artifacts.local-upload-enabled`
`kubernetes.artifacts.local-upload-target`
`user.artifacts.artifact-list`

```
$ ./bin/flink run \
    --target kubernetes-application \
    -Dkubernetes.cluster-id=my-first-application-cluster \
    -Dkubernetes.container.image=custom-image-name \
    -Dkubernetes.artifacts.local-upload-enabled=true \
    -Dkubernetes.artifacts.local-upload-target=s3://my-bucket/ \
    -Duser.artifacts.artifact-list=local:///tmp/my-flink-udf1.jar\;s3://my-bucket/my-flink-udf2.jar \
    local:///tmp/my-flink-job.jar

```

`$ ./bin/flink run \
    --target kubernetes-application \
    -Dkubernetes.cluster-id=my-first-application-cluster \
    -Dkubernetes.container.image=custom-image-name \
    -Dkubernetes.artifacts.local-upload-enabled=true \
    -Dkubernetes.artifacts.local-upload-target=s3://my-bucket/ \
    -Duser.artifacts.artifact-list=local:///tmp/my-flink-udf1.jar\;s3://my-bucket/my-flink-udf2.jar \
    local:///tmp/my-flink-job.jar
`

In case the job JAR or any additional artifact is already available remotely via DFS or HTTP(S), Flink will simply fetch it on the deployed JobManager pod:


```
# FileSystem
$ ./bin/flink run \
    --target kubernetes-application \
    -Dkubernetes.cluster-id=my-first-application-cluster \
    -Dkubernetes.container.image=custom-image-name \
    s3://my-bucket/my-flink-job.jar

# HTTP(S)
$ ./bin/flink run \
    --target kubernetes-application \
    -Dkubernetes.cluster-id=my-first-application-cluster \
    -Dkubernetes.container.image=custom-image-name \
    https://ip:port/my-flink-job.jar

```

`# FileSystem
$ ./bin/flink run \
    --target kubernetes-application \
    -Dkubernetes.cluster-id=my-first-application-cluster \
    -Dkubernetes.container.image=custom-image-name \
    s3://my-bucket/my-flink-job.jar

# HTTP(S)
$ ./bin/flink run \
    --target kubernetes-application \
    -Dkubernetes.cluster-id=my-first-application-cluster \
    -Dkubernetes.container.image=custom-image-name \
    https://ip:port/my-flink-job.jar
`

> 
  Please be aware that already existing artifacts will not be overwritten during a local upload!



> 
  JAR fetching supports downloading from filesystems or HTTP(S) in Application Mode.
The JAR will be downloaded to
user.artifacts.base-dir/kubernetes.namespace/kubernetes.cluster-id path in image.



The kubernetes.cluster-id option specifies the cluster name and must be unique.
If you do not specify this option, then Flink will generate a random name.

`kubernetes.cluster-id`

The kubernetes.container.image.ref option specifies the image to start the pods with.

`kubernetes.container.image.ref`

Once the application cluster is deployed you can interact with it:


```
# List running job on the cluster
$ ./bin/flink list --target kubernetes-application -Dkubernetes.cluster-id=my-first-application-cluster
# Cancel running job
$ ./bin/flink cancel --target kubernetes-application -Dkubernetes.cluster-id=my-first-application-cluster <jobId>

```

`# List running job on the cluster
$ ./bin/flink list --target kubernetes-application -Dkubernetes.cluster-id=my-first-application-cluster
# Cancel running job
$ ./bin/flink cancel --target kubernetes-application -Dkubernetes.cluster-id=my-first-application-cluster <jobId>
`

You can override configurations set in Flink configuration file by passing key-value pairs -Dkey=value to bin/flink.

`-Dkey=value`
`bin/flink`

### Session Mode#


> 
  For high-level intuition behind the session mode, please refer to the deployment mode overview.



You have seen the deployment of a Session cluster in the Getting Started guide at the top of this page.


The Session Mode can be executed in two modes:

* 
detached mode (default): The kubernetes-session.sh deploys the Flink cluster on Kubernetes and then terminates.

* 
attached mode (-Dexecution.attached=true): The kubernetes-session.sh stays alive and allows entering commands to control the running Flink cluster.
For example, stop stops the running Session cluster.
Type help to list all supported commands.


detached mode (default): The kubernetes-session.sh deploys the Flink cluster on Kubernetes and then terminates.

`kubernetes-session.sh`

attached mode (-Dexecution.attached=true): The kubernetes-session.sh stays alive and allows entering commands to control the running Flink cluster.
For example, stop stops the running Session cluster.
Type help to list all supported commands.

`-Dexecution.attached=true`
`kubernetes-session.sh`
`stop`
`help`

In order to re-attach to a running Session cluster with the cluster id my-first-flink-cluster use the following command:

`my-first-flink-cluster`

```
$ ./bin/kubernetes-session.sh \
    -Dkubernetes.cluster-id=my-first-flink-cluster \
    -Dexecution.attached=true

```

`$ ./bin/kubernetes-session.sh \
    -Dkubernetes.cluster-id=my-first-flink-cluster \
    -Dexecution.attached=true
`

You can override configurations set in Flink configuration file by passing key-value pairs -Dkey=value to bin/kubernetes-session.sh.

`-Dkey=value`
`bin/kubernetes-session.sh`

#### Stop a Running Session Cluster#


In order to stop a running Session Cluster with cluster id my-first-flink-cluster you can either delete the Flink deployment or use:

`my-first-flink-cluster`

```
$ echo 'stop' | ./bin/kubernetes-session.sh \
    -Dkubernetes.cluster-id=my-first-flink-cluster \
    -Dexecution.attached=true

```

`$ echo 'stop' | ./bin/kubernetes-session.sh \
    -Dkubernetes.cluster-id=my-first-flink-cluster \
    -Dexecution.attached=true
`

 Back to top


## Flink on Kubernetes Reference#


### Configuring Flink on Kubernetes#


The Kubernetes-specific configuration options are listed on the configuration page.


Flink uses Fabric8 Kubernetes client to communicate with Kubernetes APIServer to create/delete Kubernetes resources(e.g. Deployment, Pod, ConfigMap, Service, etc.), as well as watch the Pods and ConfigMaps.
Except for the above Flink config options, some expert options of Fabric8 Kubernetes client could be configured via system properties or environment variables.


For example, users could use the following Flink config options to set the concurrent max requests.


```
containerized.master.env.KUBERNETES_MAX_CONCURRENT_REQUESTS: 200
env.java.opts.jobmanager: "-Dkubernetes.max.concurrent.requests=200"

```

`containerized.master.env.KUBERNETES_MAX_CONCURRENT_REQUESTS: 200
env.java.opts.jobmanager: "-Dkubernetes.max.concurrent.requests=200"
`

### Accessing Flink’s Web UI#


Flink’s Web UI and REST endpoint can be exposed in several ways via the kubernetes.rest-service.exposed.type configuration option.

* ClusterIP: Exposes the service on a cluster-internal IP.
The Service is only reachable within the cluster.
If you want to access the JobManager UI or submit job to the existing session, you need to start a local proxy.
You can then use localhost:8081 to submit a Flink job to the session or view the dashboard.
`localhost:8081`

```
$ kubectl port-forward service/<ServiceName> 8081

```

`$ kubectl port-forward service/<ServiceName> 8081
`
* 
NodePort: Exposes the service on each Nodeâs IP at a static port (the NodePort).
<NodeIP>:<NodePort> can be used to contact the JobManager service.

* 
LoadBalancer: Exposes the service externally using a cloud providerâs load balancer.
Since the cloud provider and Kubernetes needs some time to prepare the load balancer, you may get a NodePort JobManager Web Interface in the client log.
You can use kubectl get services/<cluster-id>-rest to get EXTERNAL-IP and construct the load balancer JobManager Web Interface manually http://<EXTERNAL-IP>:8081.


NodePort: Exposes the service on each Nodeâs IP at a static port (the NodePort).
<NodeIP>:<NodePort> can be used to contact the JobManager service.

`NodePort`
`<NodeIP>:<NodePort>`

LoadBalancer: Exposes the service externally using a cloud providerâs load balancer.
Since the cloud provider and Kubernetes needs some time to prepare the load balancer, you may get a NodePort JobManager Web Interface in the client log.
You can use kubectl get services/<cluster-id>-rest to get EXTERNAL-IP and construct the load balancer JobManager Web Interface manually http://<EXTERNAL-IP>:8081.

`NodePort`
`kubectl get services/<cluster-id>-rest`
`http://<EXTERNAL-IP>:8081`

Please refer to the official documentation on publishing services in Kubernetes for more information.


> 
  Depending on your environment, starting a Flink cluster with LoadBalancer REST service exposed type might make the cluster accessible publicly (usually with the ability to execute arbitrary code).


`LoadBalancer`

### Logging#


The Kubernetes integration exposes conf/log4j-console.properties and conf/logback-console.xml as a ConfigMap to the pods.
Changes to these files will be visible to a newly started cluster.

`conf/log4j-console.properties`
`conf/logback-console.xml`

#### Accessing the Logs#


By default, the JobManager and TaskManager will output the logs to the console and /opt/flink/log in each pod simultaneously.
The STDOUT and STDERR output will only be redirected to the console.
You can access them via

`/opt/flink/log`
`STDOUT`
`STDERR`

```
$ kubectl logs <pod-name>

```

`$ kubectl logs <pod-name>
`

If the pod is running, you can also use kubectl exec -it <pod-name> bash to tunnel in and view the logs or debug the process.

`kubectl exec -it <pod-name> bash`

#### Accessing the Logs of the TaskManagers#


Flink will automatically de-allocate idling TaskManagers in order to not waste resources.
This behaviour can make it harder to access the logs of the respective pods.
You can increase the time before idling TaskManagers are released by configuring resourcemanager.taskmanager-timeout so that you have more time to inspect the log files.


#### Changing the Log Level Dynamically#


If you have configured your logger to detect configuration changes automatically, then you can dynamically adapt the log level by changing the respective ConfigMap (assuming that the cluster id is my-first-flink-cluster):

`my-first-flink-cluster`

```
$ kubectl edit cm flink-config-my-first-flink-cluster

```

`$ kubectl edit cm flink-config-my-first-flink-cluster
`

### Using Plugins#


In order to use plugins, you must copy them to the correct location in the Flink JobManager/TaskManager pod.
You can use the built-in plugins without mounting a volume or building a custom Docker image.
For example, use the following command to enable the S3 plugin for your Flink session cluster.


```
$ ./bin/kubernetes-session.sh
    -Dcontainerized.master.env.ENABLE_BUILT_IN_PLUGINS=flink-s3-fs-hadoop-2.0-SNAPSHOT.jar \
    -Dcontainerized.taskmanager.env.ENABLE_BUILT_IN_PLUGINS=flink-s3-fs-hadoop-2.0-SNAPSHOT.jar

```

`$ ./bin/kubernetes-session.sh
    -Dcontainerized.master.env.ENABLE_BUILT_IN_PLUGINS=flink-s3-fs-hadoop-2.0-SNAPSHOT.jar \
    -Dcontainerized.taskmanager.env.ENABLE_BUILT_IN_PLUGINS=flink-s3-fs-hadoop-2.0-SNAPSHOT.jar
`

### Custom Docker Image#


If you want to use a custom Docker image, then you can specify it via the configuration option kubernetes.container.image.ref.
The Flink community provides a rich Flink Docker image which can be a good starting point.
See how to customize Flink’s Docker image for how to enable plugins, add dependencies and other options.

`kubernetes.container.image.ref`

### Using Secrets#


Kubernetes Secrets is an object that contains a small amount of sensitive data such as a password, a token, or a key.
Such information might otherwise be put in a pod specification or in an image.
Flink on Kubernetes can use Secrets in two ways:

* 
Using Secrets as files from a pod;

* 
Using Secrets as environment variables;


Using Secrets as files from a pod;


Using Secrets as environment variables;


#### Using Secrets as Files From a Pod#


The following command will mount the secret mysecret under the path /path/to/secret in the started pods:

`mysecret`
`/path/to/secret`

```
$ ./bin/kubernetes-session.sh -Dkubernetes.secrets=mysecret:/path/to/secret

```

`$ ./bin/kubernetes-session.sh -Dkubernetes.secrets=mysecret:/path/to/secret
`

The username and password of the secret mysecret can then be found stored in the files /path/to/secret/username and /path/to/secret/password.
For more details see the official Kubernetes documentation.

`mysecret`
`/path/to/secret/username`
`/path/to/secret/password`

#### Using Secrets as Environment Variables#


The following command will expose the secret mysecret as environment variable in the started pods:

`mysecret`

```
$ ./bin/kubernetes-session.sh -Dkubernetes.env.secretKeyRef=\
    env:SECRET_USERNAME,secret:mysecret,key:username;\
    env:SECRET_PASSWORD,secret:mysecret,key:password

```

`$ ./bin/kubernetes-session.sh -Dkubernetes.env.secretKeyRef=\
    env:SECRET_USERNAME,secret:mysecret,key:username;\
    env:SECRET_PASSWORD,secret:mysecret,key:password
`

The env variable SECRET_USERNAME contains the username and the env variable SECRET_PASSWORD contains the password of the secret mysecret.
For more details see the official Kubernetes documentation.

`SECRET_USERNAME`
`SECRET_PASSWORD`
`mysecret`

### High-Availability on Kubernetes#


For high availability on Kubernetes, you can use the existing high availability services.


Configure the value of kubernetes.jobmanager.replicas to greater than 1 to start standby JobManagers.
It will help to achieve faster recovery.
Notice that high availability should be enabled when starting standby JobManagers.


### Manual Resource Cleanup#


Flink uses Kubernetes OwnerReference’s to clean up all cluster components.
All the Flink created resources, including ConfigMap, Service, and Pod, have the OwnerReference being set to deployment/<cluster-id>.
When the deployment is deleted, all related resources will be deleted automatically.

`ConfigMap`
`Service`
`Pod`
`OwnerReference`
`deployment/<cluster-id>`

```
$ kubectl delete deployment/<cluster-id>

```

`$ kubectl delete deployment/<cluster-id>
`

### Supported Kubernetes Versions#


Currently, all Kubernetes versions >= 1.9 are supported.

`>= 1.9`

### Namespaces#


Namespaces in Kubernetes divide cluster resources between multiple users via resource quotas.
Flink on Kubernetes can use namespaces to launch Flink clusters.
The namespace can be configured via kubernetes.namespace.


### RBAC#


Role-based access control (RBAC) is a method of regulating access to compute or network resources based on the roles of individual users within an enterprise.
Users can configure RBAC roles and service accounts used by JobManager to access the Kubernetes API server within the Kubernetes cluster.


Every namespace has a default service account. However, the default service account may not have the permission to create or delete pods within the Kubernetes cluster.
Users may need to update the permission of the default service account or specify another service account that has the right role bound.

`default`
`default`

```
$ kubectl create clusterrolebinding flink-role-binding-default --clusterrole=edit --serviceaccount=default:default

```

`$ kubectl create clusterrolebinding flink-role-binding-default --clusterrole=edit --serviceaccount=default:default
`

If you do not want to use the default service account, use the following command to create a new flink-service-account service account and set the role binding.
Then use the config option -Dkubernetes.service-account=flink-service-account to configure the JobManager pod’s service account used to create and delete TaskManager pods and leader ConfigMaps.
Also this will allow the TaskManager to watch leader ConfigMaps to retrieve the address of JobManager and ResourceManager.

`default`
`flink-service-account`
`-Dkubernetes.service-account=flink-service-account`

```
$ kubectl create serviceaccount flink-service-account
$ kubectl create clusterrolebinding flink-role-binding-flink --clusterrole=edit --serviceaccount=default:flink-service-account

```

`$ kubectl create serviceaccount flink-service-account
$ kubectl create clusterrolebinding flink-role-binding-flink --clusterrole=edit --serviceaccount=default:flink-service-account
`

Please refer to the official Kubernetes documentation on RBAC Authorization for more information.


### Pod Template#


Flink allows users to define the JobManager and TaskManager pods via template files. This allows to support advanced features
that are not supported by Flink Kubernetes config options directly.
Use kubernetes.pod-template-file.default
to specify a local file that contains the pod definition. It will be used to initialize the JobManager and TaskManager.
The main container should be defined with name flink-main-container.
Please refer to the pod template example for more information.

`kubernetes.pod-template-file.default`
`flink-main-container`

#### Fields Overwritten by Flink#


Some fields of the pod template will be overwritten by Flink.
The mechanism for resolving effective field values can be categorized as follows:

* 
Defined by Flink: User cannot configure it.

* 
Defined by the user: User can freely specify this value. Flink framework won’t set any additional values and the effective value derives from the config option and the template.
Precedence order: First an explicit config option value is taken, then the value in pod template and at last the default value of a config option if nothing is specified.

* 
Merged with Flink: Flink will merge values for a setting with a user defined value (see precedence order for “Defined by the user”). Flink values have precedence in case of same name fields.


Defined by Flink: User cannot configure it.


Defined by the user: User can freely specify this value. Flink framework won’t set any additional values and the effective value derives from the config option and the template.


Precedence order: First an explicit config option value is taken, then the value in pod template and at last the default value of a config option if nothing is specified.


Merged with Flink: Flink will merge values for a setting with a user defined value (see precedence order for “Defined by the user”). Flink values have precedence in case of same name fields.


Refer to the following tables for the full list of pod fields that will be overwritten.
All the fields defined in the pod template that are not listed in the tables will be unaffected.


Pod Metadata

`<clusterID>-<attempt>-<index>`

Pod Spec


Main Container Spec


#### Example of Pod Template#


pod-template.yaml

`pod-template.yaml`

```
apiVersion: v1
kind: Pod
metadata:
  name: jobmanager-pod-template
spec:
  initContainers:
    - name: artifacts-fetcher
      image: busybox:latest
      # Use wget or other tools to get user jars from remote storage
      command: [ 'wget', 'https://path/of/StateMachineExample.jar', '-O', '/flink-artifact/myjob.jar' ]
      volumeMounts:
        - mountPath: /flink-artifact
          name: flink-artifact
  containers:
    # Do not change the main container name
    - name: flink-main-container
      resources:
        requests:
          ephemeral-storage: 2048Mi
        limits:
          ephemeral-storage: 2048Mi
      volumeMounts:
        - mountPath: /opt/flink/volumes/hostpath
          name: flink-volume-hostpath
        - mountPath: /opt/flink/artifacts
          name: flink-artifact
        - mountPath: /opt/flink/log
          name: flink-logs
      # Use sidecar container to push logs to remote storage or do some other debugging things
    - name: sidecar-log-collector
      image: sidecar-log-collector:latest
      command: [ 'command-to-upload', '/remote/path/of/flink-logs/' ]
      volumeMounts:
        - mountPath: /flink-logs
          name: flink-logs
  volumes:
    - name: flink-volume-hostpath
      hostPath:
        path: /tmp
        type: Directory
    - name: flink-artifact
      emptyDir: { }
    - name: flink-logs
      emptyDir: { }

```

`apiVersion: v1
kind: Pod
metadata:
  name: jobmanager-pod-template
spec:
  initContainers:
    - name: artifacts-fetcher
      image: busybox:latest
      # Use wget or other tools to get user jars from remote storage
      command: [ 'wget', 'https://path/of/StateMachineExample.jar', '-O', '/flink-artifact/myjob.jar' ]
      volumeMounts:
        - mountPath: /flink-artifact
          name: flink-artifact
  containers:
    # Do not change the main container name
    - name: flink-main-container
      resources:
        requests:
          ephemeral-storage: 2048Mi
        limits:
          ephemeral-storage: 2048Mi
      volumeMounts:
        - mountPath: /opt/flink/volumes/hostpath
          name: flink-volume-hostpath
        - mountPath: /opt/flink/artifacts
          name: flink-artifact
        - mountPath: /opt/flink/log
          name: flink-logs
      # Use sidecar container to push logs to remote storage or do some other debugging things
    - name: sidecar-log-collector
      image: sidecar-log-collector:latest
      command: [ 'command-to-upload', '/remote/path/of/flink-logs/' ]
      volumeMounts:
        - mountPath: /flink-logs
          name: flink-logs
  volumes:
    - name: flink-volume-hostpath
      hostPath:
        path: /tmp
        type: Directory
    - name: flink-artifact
      emptyDir: { }
    - name: flink-logs
      emptyDir: { }
`

### User jars & Classpath#


When deploying Flink natively on Kubernetes, the following jars will be recognized as user-jars and included into user classpath:

* Session Mode: The JAR file specified in startup command.
* Application Mode: The JAR file specified in startup command and all JAR files in Flink’s usrlib folder.
`usrlib`

Please refer to the Debugging Classloading Docs for details.


 Back to top
