# Kubernetes


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# Kubernetes Setup#


## Getting Started#


This Getting Started guide describes how to deploy a Session cluster on Kubernetes.


### Introduction#


This page describes deploying a standalone Flink cluster on top of Kubernetes, using Flink’s standalone deployment.
We generally recommend new users to deploy Flink on Kubernetes using native Kubernetes deployments.


Apache Flink also provides a Kubernetes operator for managing Flink clusters on Kubernetes. It supports both standalone and native deployment mode and greatly simplifies deployment, configuration and the life cycle management of Flink resources on Kubernetes.


For more information, please refer to the Flink Kubernetes Operator documentation


### Preparation#


This guide expects a Kubernetes environment to be present. You can ensure that your Kubernetes setup is working by running a command like kubectl get nodes, which lists all connected Kubelets.

`kubectl get nodes`

If you want to run Kubernetes locally, we recommend using MiniKube.


> 
  If using MiniKube please make sure to execute minikube ssh 'sudo ip link set docker0 promisc on' before deploying a Flink cluster. Otherwise Flink components are not able to reference themselves through a Kubernetes service.


`minikube ssh 'sudo ip link set docker0 promisc on'`

### Starting a Kubernetes Cluster (Session Mode)#


A Flink Session cluster is executed as a long-running Kubernetes Deployment. You can run multiple Flink jobs on a Session cluster.
Each job needs to be submitted to the cluster after the cluster has been deployed.


A Flink Session cluster deployment in Kubernetes has at least three components:

* a Deployment which runs a JobManager
* a Deployment for a pool of TaskManagers
* a Service exposing the JobManager’s REST and UI ports

Using the file contents provided in the the common resource definitions, create the following files, and create the respective components with the kubectl command:

`kubectl`

```
    # Configuration and service definition
    $ kubectl create -f flink-configuration-configmap.yaml
    $ kubectl create -f jobmanager-service.yaml
    # Create the deployments for the cluster
    $ kubectl create -f jobmanager-session-deployment-non-ha.yaml
    $ kubectl create -f taskmanager-session-deployment.yaml

```

`    # Configuration and service definition
    $ kubectl create -f flink-configuration-configmap.yaml
    $ kubectl create -f jobmanager-service.yaml
    # Create the deployments for the cluster
    $ kubectl create -f jobmanager-session-deployment-non-ha.yaml
    $ kubectl create -f taskmanager-session-deployment.yaml
`

Next, we set up a port forward to access the Flink UI and submit jobs:

1. Run kubectl port-forward ${flink-jobmanager-pod} 8081:8081 to forward your jobmanager’s web ui port to local 8081.
2. Navigate to http://localhost:8081 in your browser.
3. Moreover, you could use the following command below to submit jobs to the cluster:
`kubectl port-forward ${flink-jobmanager-pod} 8081:8081`

```
$ ./bin/flink run -m localhost:8081 ./examples/streaming/TopSpeedWindowing.jar

```

`$ ./bin/flink run -m localhost:8081 ./examples/streaming/TopSpeedWindowing.jar
`

You can tear down the cluster using the following commands:


```
    $ kubectl delete -f jobmanager-service.yaml
    $ kubectl delete -f flink-configuration-configmap.yaml
    $ kubectl delete -f taskmanager-session-deployment.yaml
    $ kubectl delete -f jobmanager-session-deployment-non-ha.yaml

```

`    $ kubectl delete -f jobmanager-service.yaml
    $ kubectl delete -f flink-configuration-configmap.yaml
    $ kubectl delete -f taskmanager-session-deployment.yaml
    $ kubectl delete -f jobmanager-session-deployment-non-ha.yaml
`

 Back to top


## Deployment Modes#


### Application Mode#


> 
  For high-level intuition behind the application mode, please refer to the deployment mode overview.



A Flink Application cluster is a dedicated cluster which runs a single application, which needs to be available at deployment time.


A basic Flink Application cluster deployment in Kubernetes has three components:

* an Application which runs a JobManager
* a Deployment for a pool of TaskManagers
* a Service exposing the JobManager’s REST and UI ports

Check the Application cluster specific resource definitions and adjust them accordingly:


The args attribute in the jobmanager-application-non-ha.yaml has to specify the main class of the user job.
See also how to specify the JobManager arguments to understand
how to pass other args to the Flink image in the jobmanager-application-non-ha.yaml.

`args`
`jobmanager-application-non-ha.yaml`
`args`
`jobmanager-application-non-ha.yaml`

The job artifacts could be provided by these wayï¼

* The job artifacts could be available from the job-artifacts-volume in the resource definition examples.
The definition examples mount the volume as a local directory of the host assuming that you create the components in a minikube cluster.
If you do not use a minikube cluster, you can use any other type of volume, available in your Kubernetes cluster, to supply the job artifacts.
* You can build a custom image which already contains the artifacts instead.
* You can pass artifacts via the –jars option that are stored locally, on remote DFS, or accessible via an HTTP(S) endpoint.
`job-artifacts-volume`

After creating the common cluster components, use the Application cluster specific resource definitions to launch the cluster with the kubectl command:

`kubectl`

```
    $ kubectl create -f jobmanager-application-non-ha.yaml
    $ kubectl create -f taskmanager-job-deployment.yaml

```

`    $ kubectl create -f jobmanager-application-non-ha.yaml
    $ kubectl create -f taskmanager-job-deployment.yaml
`

To terminate the single application cluster, these components can be deleted along with the common ones
with the kubectl command:

`kubectl`

```
    $ kubectl delete -f taskmanager-job-deployment.yaml
    $ kubectl delete -f jobmanager-application-non-ha.yaml

```

`    $ kubectl delete -f taskmanager-job-deployment.yaml
    $ kubectl delete -f jobmanager-application-non-ha.yaml
`

### Session Mode#


> 
  For high-level intuition behind the session mode, please refer to the deployment mode overview.



Deployment of a Session cluster is explained in the Getting Started guide at the top of this page.


 Back to top


## Flink on Standalone Kubernetes Reference#


### Configuration#


All configuration options are listed on the configuration page. Configuration options can be added to the Flink configuration file section of the flink-configuration-configmap.yaml config map.

`flink-configuration-configmap.yaml`

### Accessing Flink in Kubernetes#


You can then access the Flink UI and submit jobs via different ways:

* 
kubectl proxy:

Run kubectl proxy in a terminal.
Navigate to http://localhost:8001/api/v1/namespaces/default/services/flink-jobmanager:webui/proxy in your browser.


* 
kubectl port-forward:

Run kubectl port-forward ${flink-jobmanager-pod} 8081:8081 to forward your jobmanager’s web ui port to local 8081.
Navigate to http://localhost:8081 in your browser.
Moreover, you can use the following command below to submit jobs to the cluster:

$ ./bin/flink run -m localhost:8081 ./examples/streaming/TopSpeedWindowing.jar

* 
Create a NodePort service on the rest service of jobmanager:

Run kubectl create -f jobmanager-rest-service.yaml to create the NodePort service on jobmanager. The example of jobmanager-rest-service.yaml can be found in appendix.
Run kubectl get svc flink-jobmanager-rest to know the node-port of this service and navigate to http://<public-node-ip>:<node-port> in your browser.
If you use minikube, you can get its public ip by running minikube ip.
Similarly to the port-forward solution, you can also use the following command below to submit jobs to the cluster:

$ ./bin/flink run -m <public-node-ip>:<node-port> ./examples/streaming/TopSpeedWindowing.jar


kubectl proxy:

`kubectl proxy`
1. Run kubectl proxy in a terminal.
2. Navigate to http://localhost:8001/api/v1/namespaces/default/services/flink-jobmanager:webui/proxy in your browser.
`kubectl proxy`

kubectl port-forward:

`kubectl port-forward`
1. Run kubectl port-forward ${flink-jobmanager-pod} 8081:8081 to forward your jobmanager’s web ui port to local 8081.
2. Navigate to http://localhost:8081 in your browser.
3. Moreover, you can use the following command below to submit jobs to the cluster:
`kubectl port-forward ${flink-jobmanager-pod} 8081:8081`

```
$ ./bin/flink run -m localhost:8081 ./examples/streaming/TopSpeedWindowing.jar

```

`$ ./bin/flink run -m localhost:8081 ./examples/streaming/TopSpeedWindowing.jar
`

Create a NodePort service on the rest service of jobmanager:

`NodePort`
1. Run kubectl create -f jobmanager-rest-service.yaml to create the NodePort service on jobmanager. The example of jobmanager-rest-service.yaml can be found in appendix.
2. Run kubectl get svc flink-jobmanager-rest to know the node-port of this service and navigate to http://<public-node-ip>:<node-port> in your browser.
3. If you use minikube, you can get its public ip by running minikube ip.
4. Similarly to the port-forward solution, you can also use the following command below to submit jobs to the cluster:
`kubectl create -f jobmanager-rest-service.yaml`
`NodePort`
`jobmanager-rest-service.yaml`
`kubectl get svc flink-jobmanager-rest`
`node-port`
`minikube ip`
`port-forward`

```
$ ./bin/flink run -m <public-node-ip>:<node-port> ./examples/streaming/TopSpeedWindowing.jar

```

`$ ./bin/flink run -m <public-node-ip>:<node-port> ./examples/streaming/TopSpeedWindowing.jar
`

### Debugging and Log Access#


Many common errors are easy to detect by checking Flink’s log files. If you have access to Flink’s web user interface, you can access the JobManager and TaskManager logs from there.


If there are problems starting Flink, you can also use Kubernetes utilities to access the logs. Use kubectl get pods to see all running pods.
For the quickstart example from above, you should see three pods:

`kubectl get pods`

```
$ kubectl get pods
NAME                                 READY   STATUS             RESTARTS   AGE
flink-jobmanager-589967dcfc-m49xv    1/1     Running            3          3m32s
flink-taskmanager-64847444ff-7rdl4   1/1     Running            3          3m28s
flink-taskmanager-64847444ff-nnd6m   1/1     Running            3          3m28s

```

`$ kubectl get pods
NAME                                 READY   STATUS             RESTARTS   AGE
flink-jobmanager-589967dcfc-m49xv    1/1     Running            3          3m32s
flink-taskmanager-64847444ff-7rdl4   1/1     Running            3          3m28s
flink-taskmanager-64847444ff-nnd6m   1/1     Running            3          3m28s
`

You can now access the logs by running kubectl logs flink-jobmanager-589967dcfc-m49xv

`kubectl logs flink-jobmanager-589967dcfc-m49xv`

### High-Availability with Standalone Kubernetes#


For high availability on Kubernetes, you can use the existing high availability services.


#### Kubernetes High-Availability Services#


Session Mode and Application Mode clusters support using the Kubernetes high availability service.
You need to add the following Flink config options to flink-configuration-configmap.yaml.


Note The filesystem which corresponds to the scheme of your configured HA storage directory must be available to the runtime. Refer to custom Flink image and enable plugins for more information.


```
apiVersion: v1
kind: ConfigMap
metadata:
  name: flink-config
  labels:
    app: flink
data:
  config.yaml: |+
  ...
    kubernetes.cluster-id: <cluster-id>
    high-availability.type: kubernetes
    high-availability.storageDir: hdfs:///flink/recovery
    restart-strategy.type: fixed-delay
    restart-strategy.fixed-delay.attempts: 10
  ...  

```

`apiVersion: v1
kind: ConfigMap
metadata:
  name: flink-config
  labels:
    app: flink
data:
  config.yaml: |+
  ...
    kubernetes.cluster-id: <cluster-id>
    high-availability.type: kubernetes
    high-availability.storageDir: hdfs:///flink/recovery
    restart-strategy.type: fixed-delay
    restart-strategy.fixed-delay.attempts: 10
  ...  
`

Moreover, you have to start the JobManager and TaskManager pods with a service account which has the permissions to create, edit, delete ConfigMaps.
See how to configure service accounts for pods for more information.


When High-Availability is enabled, Flink will use its own HA-services for service discovery.
Therefore, JobManager pods should be started with their IP address instead of a Kubernetes service as its jobmanager.rpc.address.
Refer to the appendix for full configuration.

`jobmanager.rpc.address`

#### Standby JobManagers#


Usually, it is enough to only start a single JobManager pod, because Kubernetes will restart it once the pod crashes.
If you want to achieve faster recovery, configure the replicas in jobmanager-session-deployment-ha.yaml or parallelism in jobmanager-application-ha.yaml to a value greater than 1 to start standby JobManagers.

`replicas`
`jobmanager-session-deployment-ha.yaml`
`parallelism`
`jobmanager-application-ha.yaml`
`1`

### Using Standalone Kubernetes with Reactive Mode#


Reactive Mode allows to run Flink in a mode, where the Application Cluster is always adjusting the job parallelism to the available resources. In combination with Kubernetes, the replica count of the TaskManager deployment determines the available resources. Increasing the replica count will scale up the job, reducing it will trigger a scale down. This can also be done automatically by using a Horizontal Pod Autoscaler.


To use Reactive Mode on Kubernetes, follow the same steps as for deploying a job using an Application Cluster. But instead of flink-configuration-configmap.yaml use this config map: flink-reactive-mode-configuration-configmap.yaml. It contains the scheduler-mode: reactive setting for Flink.

`flink-configuration-configmap.yaml`
`flink-reactive-mode-configuration-configmap.yaml`
`scheduler-mode: reactive`

Once you have deployed the Application Cluster, you can scale your job up or down by changing the replica count in the flink-taskmanager deployment.

`flink-taskmanager`

### Enabling Local Recovery Across Pod Restarts#


In order to speed up recoveries in case of pod failures, you can leverage Flink’s working directory feature together with local recovery.
If the working directory is configured to reside on a persistent volume that gets remounted to a restarted TaskManager pod, then Flink is able to recover state locally.
With the StatefulSet, Kubernetes gives you the exact tool you need to map a pod to a persistent volume.


Deploying TaskManagers as a StatefulSet, allows you to configure a volume claim template that is used to mount persistent volumes to the TaskManagers.
Additionally, you need to configure a deterministic taskmanager.resource-id.
A suitable value is the pod name, that you expose using environment variables.
For an example StatefulSet configuration take a look at the appendix.

`taskmanager.resource-id`

 Back to top


## Appendix#


### Common cluster resource definitions#


flink-configuration-configmap.yaml

`flink-configuration-configmap.yaml`

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: flink-config
  labels:
    app: flink
data:
  config.yaml: |+
    jobmanager.rpc.address: flink-jobmanager
    taskmanager.numberOfTaskSlots: 2
    blob.server.port: 6124
    jobmanager.rpc.port: 6123
    taskmanager.rpc.port: 6122
    jobmanager.memory.process.size: 1600m
    taskmanager.memory.process.size: 1728m
    parallelism.default: 2    
  log4j-console.properties: |+
    # This affects logging for both user code and Flink
    rootLogger.level = INFO
    rootLogger.appenderRef.console.ref = ConsoleAppender
    rootLogger.appenderRef.rolling.ref = RollingFileAppender

    # Uncomment this if you want to _only_ change Flink's logging
    #logger.flink.name = org.apache.flink
    #logger.flink.level = INFO

    # The following lines keep the log level of common libraries/connectors on
    # log level INFO. The root logger does not override this. You have to manually
    # change the log levels here.
    logger.pekko.name = org.apache.pekko
    logger.pekko.level = INFO
    logger.kafka.name= org.apache.kafka
    logger.kafka.level = INFO
    logger.hadoop.name = org.apache.hadoop
    logger.hadoop.level = INFO
    logger.zookeeper.name = org.apache.zookeeper
    logger.zookeeper.level = INFO

    # Log all infos to the console
    appender.console.name = ConsoleAppender
    appender.console.type = CONSOLE
    appender.console.layout.type = PatternLayout
    appender.console.layout.pattern = %d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n

    # Log all infos in the given rolling file
    appender.rolling.name = RollingFileAppender
    appender.rolling.type = RollingFile
    appender.rolling.append = false
    appender.rolling.fileName = ${sys:log.file}
    appender.rolling.filePattern = ${sys:log.file}.%i
    appender.rolling.layout.type = PatternLayout
    appender.rolling.layout.pattern = %d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n
    appender.rolling.policies.type = Policies
    appender.rolling.policies.size.type = SizeBasedTriggeringPolicy
    appender.rolling.policies.size.size=100MB
    appender.rolling.strategy.type = DefaultRolloverStrategy
    appender.rolling.strategy.max = 10

    # Suppress the irrelevant (wrong) warnings from the Netty channel handler
    logger.netty.name = org.jboss.netty.channel.DefaultChannelPipeline
    logger.netty.level = OFF    

```

`apiVersion: v1
kind: ConfigMap
metadata:
  name: flink-config
  labels:
    app: flink
data:
  config.yaml: |+
    jobmanager.rpc.address: flink-jobmanager
    taskmanager.numberOfTaskSlots: 2
    blob.server.port: 6124
    jobmanager.rpc.port: 6123
    taskmanager.rpc.port: 6122
    jobmanager.memory.process.size: 1600m
    taskmanager.memory.process.size: 1728m
    parallelism.default: 2    
  log4j-console.properties: |+
    # This affects logging for both user code and Flink
    rootLogger.level = INFO
    rootLogger.appenderRef.console.ref = ConsoleAppender
    rootLogger.appenderRef.rolling.ref = RollingFileAppender

    # Uncomment this if you want to _only_ change Flink's logging
    #logger.flink.name = org.apache.flink
    #logger.flink.level = INFO

    # The following lines keep the log level of common libraries/connectors on
    # log level INFO. The root logger does not override this. You have to manually
    # change the log levels here.
    logger.pekko.name = org.apache.pekko
    logger.pekko.level = INFO
    logger.kafka.name= org.apache.kafka
    logger.kafka.level = INFO
    logger.hadoop.name = org.apache.hadoop
    logger.hadoop.level = INFO
    logger.zookeeper.name = org.apache.zookeeper
    logger.zookeeper.level = INFO

    # Log all infos to the console
    appender.console.name = ConsoleAppender
    appender.console.type = CONSOLE
    appender.console.layout.type = PatternLayout
    appender.console.layout.pattern = %d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n

    # Log all infos in the given rolling file
    appender.rolling.name = RollingFileAppender
    appender.rolling.type = RollingFile
    appender.rolling.append = false
    appender.rolling.fileName = ${sys:log.file}
    appender.rolling.filePattern = ${sys:log.file}.%i
    appender.rolling.layout.type = PatternLayout
    appender.rolling.layout.pattern = %d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n
    appender.rolling.policies.type = Policies
    appender.rolling.policies.size.type = SizeBasedTriggeringPolicy
    appender.rolling.policies.size.size=100MB
    appender.rolling.strategy.type = DefaultRolloverStrategy
    appender.rolling.strategy.max = 10

    # Suppress the irrelevant (wrong) warnings from the Netty channel handler
    logger.netty.name = org.jboss.netty.channel.DefaultChannelPipeline
    logger.netty.level = OFF    
`

flink-reactive-mode-configuration-configmap.yaml

`flink-reactive-mode-configuration-configmap.yaml`

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: flink-config
  labels:
    app: flink
data:
  config.yaml: |+
    jobmanager.rpc.address: flink-jobmanager
    taskmanager.numberOfTaskSlots: 2
    blob.server.port: 6124
    jobmanager.rpc.port: 6123
    taskmanager.rpc.port: 6122
    jobmanager.memory.process.size: 1600m
    taskmanager.memory.process.size: 1728m
    parallelism.default: 2
    scheduler-mode: reactive
    execution.checkpointing.interval: 10s    
  log4j-console.properties: |+
    # This affects logging for both user code and Flink
    rootLogger.level = INFO
    rootLogger.appenderRef.console.ref = ConsoleAppender
    rootLogger.appenderRef.rolling.ref = RollingFileAppender

    # Uncomment this if you want to _only_ change Flink's logging
    #logger.flink.name = org.apache.flink
    #logger.flink.level = INFO

    # The following lines keep the log level of common libraries/connectors on
    # log level INFO. The root logger does not override this. You have to manually
    # change the log levels here.
    logger.pekko.name = org.apache.pekko
    logger.pekko.level = INFO
    logger.kafka.name= org.apache.kafka
    logger.kafka.level = INFO
    logger.hadoop.name = org.apache.hadoop
    logger.hadoop.level = INFO
    logger.zookeeper.name = org.apache.zookeeper
    logger.zookeeper.level = INFO

    # Log all infos to the console
    appender.console.name = ConsoleAppender
    appender.console.type = CONSOLE
    appender.console.layout.type = PatternLayout
    appender.console.layout.pattern = %d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n

    # Log all infos in the given rolling file
    appender.rolling.name = RollingFileAppender
    appender.rolling.type = RollingFile
    appender.rolling.append = false
    appender.rolling.fileName = ${sys:log.file}
    appender.rolling.filePattern = ${sys:log.file}.%i
    appender.rolling.layout.type = PatternLayout
    appender.rolling.layout.pattern = %d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n
    appender.rolling.policies.type = Policies
    appender.rolling.policies.size.type = SizeBasedTriggeringPolicy
    appender.rolling.policies.size.size=100MB
    appender.rolling.strategy.type = DefaultRolloverStrategy
    appender.rolling.strategy.max = 10

    # Suppress the irrelevant (wrong) warnings from the Netty channel handler
    logger.netty.name = org.jboss.netty.channel.DefaultChannelPipeline
    logger.netty.level = OFF    

```

`apiVersion: v1
kind: ConfigMap
metadata:
  name: flink-config
  labels:
    app: flink
data:
  config.yaml: |+
    jobmanager.rpc.address: flink-jobmanager
    taskmanager.numberOfTaskSlots: 2
    blob.server.port: 6124
    jobmanager.rpc.port: 6123
    taskmanager.rpc.port: 6122
    jobmanager.memory.process.size: 1600m
    taskmanager.memory.process.size: 1728m
    parallelism.default: 2
    scheduler-mode: reactive
    execution.checkpointing.interval: 10s    
  log4j-console.properties: |+
    # This affects logging for both user code and Flink
    rootLogger.level = INFO
    rootLogger.appenderRef.console.ref = ConsoleAppender
    rootLogger.appenderRef.rolling.ref = RollingFileAppender

    # Uncomment this if you want to _only_ change Flink's logging
    #logger.flink.name = org.apache.flink
    #logger.flink.level = INFO

    # The following lines keep the log level of common libraries/connectors on
    # log level INFO. The root logger does not override this. You have to manually
    # change the log levels here.
    logger.pekko.name = org.apache.pekko
    logger.pekko.level = INFO
    logger.kafka.name= org.apache.kafka
    logger.kafka.level = INFO
    logger.hadoop.name = org.apache.hadoop
    logger.hadoop.level = INFO
    logger.zookeeper.name = org.apache.zookeeper
    logger.zookeeper.level = INFO

    # Log all infos to the console
    appender.console.name = ConsoleAppender
    appender.console.type = CONSOLE
    appender.console.layout.type = PatternLayout
    appender.console.layout.pattern = %d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n

    # Log all infos in the given rolling file
    appender.rolling.name = RollingFileAppender
    appender.rolling.type = RollingFile
    appender.rolling.append = false
    appender.rolling.fileName = ${sys:log.file}
    appender.rolling.filePattern = ${sys:log.file}.%i
    appender.rolling.layout.type = PatternLayout
    appender.rolling.layout.pattern = %d{yyyy-MM-dd HH:mm:ss,SSS} %-5p %-60c %x - %m%n
    appender.rolling.policies.type = Policies
    appender.rolling.policies.size.type = SizeBasedTriggeringPolicy
    appender.rolling.policies.size.size=100MB
    appender.rolling.strategy.type = DefaultRolloverStrategy
    appender.rolling.strategy.max = 10

    # Suppress the irrelevant (wrong) warnings from the Netty channel handler
    logger.netty.name = org.jboss.netty.channel.DefaultChannelPipeline
    logger.netty.level = OFF    
`

jobmanager-service.yaml Optional service, which is only necessary for non-HA mode.

`jobmanager-service.yaml`

```
apiVersion: v1
kind: Service
metadata:
  name: flink-jobmanager
spec:
  type: ClusterIP
  ports:
  - name: rpc
    port: 6123
  - name: blob-server
    port: 6124
  - name: webui
    port: 8081
  selector:
    app: flink
    component: jobmanager

```

`apiVersion: v1
kind: Service
metadata:
  name: flink-jobmanager
spec:
  type: ClusterIP
  ports:
  - name: rpc
    port: 6123
  - name: blob-server
    port: 6124
  - name: webui
    port: 8081
  selector:
    app: flink
    component: jobmanager
`

jobmanager-rest-service.yaml. Optional service, that exposes the jobmanager rest port as public Kubernetes node’s port.

`jobmanager-rest-service.yaml`
`rest`

```
apiVersion: v1
kind: Service
metadata:
  name: flink-jobmanager-rest
spec:
  type: NodePort
  ports:
  - name: rest
    port: 8081
    targetPort: 8081
    nodePort: 30081
  selector:
    app: flink
    component: jobmanager

```

`apiVersion: v1
kind: Service
metadata:
  name: flink-jobmanager-rest
spec:
  type: NodePort
  ports:
  - name: rest
    port: 8081
    targetPort: 8081
    nodePort: 30081
  selector:
    app: flink
    component: jobmanager
`

### Session cluster resource definitions#


jobmanager-session-deployment-non-ha.yaml

`jobmanager-session-deployment-non-ha.yaml`

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flink-jobmanager
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flink
      component: jobmanager
  template:
    metadata:
      labels:
        app: flink
        component: jobmanager
    spec:
      containers:
      - name: jobmanager
        image: apache/flink:latest
        args: ["jobmanager"]
        ports:
        - containerPort: 6123
          name: rpc
        - containerPort: 6124
          name: blob-server
        - containerPort: 8081
          name: webui
        livenessProbe:
          tcpSocket:
            port: 6123
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: flink-config-volume
          mountPath: /opt/flink/conf
        securityContext:
          runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      volumes:
      - name: flink-config-volume
        configMap:
          name: flink-config
          items:
          - key: config.yaml
            path: config.yaml
          - key: log4j-console.properties
            path: log4j-console.properties

```

`apiVersion: apps/v1
kind: Deployment
metadata:
  name: flink-jobmanager
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flink
      component: jobmanager
  template:
    metadata:
      labels:
        app: flink
        component: jobmanager
    spec:
      containers:
      - name: jobmanager
        image: apache/flink:latest
        args: ["jobmanager"]
        ports:
        - containerPort: 6123
          name: rpc
        - containerPort: 6124
          name: blob-server
        - containerPort: 8081
          name: webui
        livenessProbe:
          tcpSocket:
            port: 6123
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: flink-config-volume
          mountPath: /opt/flink/conf
        securityContext:
          runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      volumes:
      - name: flink-config-volume
        configMap:
          name: flink-config
          items:
          - key: config.yaml
            path: config.yaml
          - key: log4j-console.properties
            path: log4j-console.properties
`

jobmanager-session-deployment-ha.yaml

`jobmanager-session-deployment-ha.yaml`

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flink-jobmanager
spec:
  replicas: 1 # Set the value to greater than 1 to start standby JobManagers
  selector:
    matchLabels:
      app: flink
      component: jobmanager
  template:
    metadata:
      labels:
        app: flink
        component: jobmanager
    spec:
      containers:
      - name: jobmanager
        image: apache/flink:latest
        env:
        - name: POD_IP
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: status.podIP
        # The following args overwrite the value of jobmanager.rpc.address configured in the configuration config map to POD_IP.
        args: ["jobmanager", "$(POD_IP)"]
        ports:
        - containerPort: 6123
          name: rpc
        - containerPort: 6124
          name: blob-server
        - containerPort: 8081
          name: webui
        livenessProbe:
          tcpSocket:
            port: 6123
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: flink-config-volume
          mountPath: /opt/flink/conf
        securityContext:
          runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      serviceAccountName: flink-service-account # Service account which has the permissions to create, edit, delete ConfigMaps
      volumes:
      - name: flink-config-volume
        configMap:
          name: flink-config
          items:
          - key: config.yaml
            path: config.yaml
          - key: log4j-console.properties
            path: log4j-console.properties

```

`apiVersion: apps/v1
kind: Deployment
metadata:
  name: flink-jobmanager
spec:
  replicas: 1 # Set the value to greater than 1 to start standby JobManagers
  selector:
    matchLabels:
      app: flink
      component: jobmanager
  template:
    metadata:
      labels:
        app: flink
        component: jobmanager
    spec:
      containers:
      - name: jobmanager
        image: apache/flink:latest
        env:
        - name: POD_IP
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: status.podIP
        # The following args overwrite the value of jobmanager.rpc.address configured in the configuration config map to POD_IP.
        args: ["jobmanager", "$(POD_IP)"]
        ports:
        - containerPort: 6123
          name: rpc
        - containerPort: 6124
          name: blob-server
        - containerPort: 8081
          name: webui
        livenessProbe:
          tcpSocket:
            port: 6123
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: flink-config-volume
          mountPath: /opt/flink/conf
        securityContext:
          runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      serviceAccountName: flink-service-account # Service account which has the permissions to create, edit, delete ConfigMaps
      volumes:
      - name: flink-config-volume
        configMap:
          name: flink-config
          items:
          - key: config.yaml
            path: config.yaml
          - key: log4j-console.properties
            path: log4j-console.properties
`

taskmanager-session-deployment.yaml

`taskmanager-session-deployment.yaml`

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flink-taskmanager
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flink
      component: taskmanager
  template:
    metadata:
      labels:
        app: flink
        component: taskmanager
    spec:
      containers:
      - name: taskmanager
        image: apache/flink:latest
        args: ["taskmanager"]
        ports:
        - containerPort: 6122
          name: rpc
        livenessProbe:
          tcpSocket:
            port: 6122
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: flink-config-volume
          mountPath: /opt/flink/conf/
        securityContext:
          runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      volumes:
      - name: flink-config-volume
        configMap:
          name: flink-config
          items:
          - key: config.yaml
            path: config.yaml
          - key: log4j-console.properties
            path: log4j-console.properties

```

`apiVersion: apps/v1
kind: Deployment
metadata:
  name: flink-taskmanager
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flink
      component: taskmanager
  template:
    metadata:
      labels:
        app: flink
        component: taskmanager
    spec:
      containers:
      - name: taskmanager
        image: apache/flink:latest
        args: ["taskmanager"]
        ports:
        - containerPort: 6122
          name: rpc
        livenessProbe:
          tcpSocket:
            port: 6122
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: flink-config-volume
          mountPath: /opt/flink/conf/
        securityContext:
          runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      volumes:
      - name: flink-config-volume
        configMap:
          name: flink-config
          items:
          - key: config.yaml
            path: config.yaml
          - key: log4j-console.properties
            path: log4j-console.properties
`

### Application cluster resource definitions#


jobmanager-application-non-ha.yaml

`jobmanager-application-non-ha.yaml`

```
apiVersion: batch/v1
kind: Job
metadata:
  name: flink-jobmanager
spec:
  template:
    metadata:
      labels:
        app: flink
        component: jobmanager
    spec:
      restartPolicy: OnFailure
      containers:
        - name: jobmanager
          image: apache/flink:latest
          env:
          args: ["standalone-job", "--job-classname", "com.job.ClassName", <optional arguments>, <job arguments>] # optional arguments: ["--job-id", "<job id>", "--jars", "/path/to/artifact1,/path/to/artifact2", "--fromSavepoint", "/path/to/savepoint", "--allowNonRestoredState"]
          ports:
            - containerPort: 6123
              name: rpc
            - containerPort: 6124
              name: blob-server
            - containerPort: 8081
              name: webui
          livenessProbe:
            tcpSocket:
              port: 6123
            initialDelaySeconds: 30
            periodSeconds: 60
          volumeMounts:
            - name: flink-config-volume
              mountPath: /opt/flink/conf
            - name: job-artifacts-volume
              mountPath: /opt/flink/usrlib
          securityContext:
            runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      volumes:
        - name: flink-config-volume
          configMap:
            name: flink-config
            items:
              - key: config.yaml
                path: config.yaml
              - key: log4j-console.properties
                path: log4j-console.properties
        - name: job-artifacts-volume
          hostPath:
            path: /host/path/to/job/artifacts

```

`apiVersion: batch/v1
kind: Job
metadata:
  name: flink-jobmanager
spec:
  template:
    metadata:
      labels:
        app: flink
        component: jobmanager
    spec:
      restartPolicy: OnFailure
      containers:
        - name: jobmanager
          image: apache/flink:latest
          env:
          args: ["standalone-job", "--job-classname", "com.job.ClassName", <optional arguments>, <job arguments>] # optional arguments: ["--job-id", "<job id>", "--jars", "/path/to/artifact1,/path/to/artifact2", "--fromSavepoint", "/path/to/savepoint", "--allowNonRestoredState"]
          ports:
            - containerPort: 6123
              name: rpc
            - containerPort: 6124
              name: blob-server
            - containerPort: 8081
              name: webui
          livenessProbe:
            tcpSocket:
              port: 6123
            initialDelaySeconds: 30
            periodSeconds: 60
          volumeMounts:
            - name: flink-config-volume
              mountPath: /opt/flink/conf
            - name: job-artifacts-volume
              mountPath: /opt/flink/usrlib
          securityContext:
            runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      volumes:
        - name: flink-config-volume
          configMap:
            name: flink-config
            items:
              - key: config.yaml
                path: config.yaml
              - key: log4j-console.properties
                path: log4j-console.properties
        - name: job-artifacts-volume
          hostPath:
            path: /host/path/to/job/artifacts
`

jobmanager-application-ha.yaml

`jobmanager-application-ha.yaml`

```
apiVersion: batch/v1
kind: Job
metadata:
  name: flink-jobmanager
spec:
  parallelism: 1 # Set the value to greater than 1 to start standby JobManagers
  template:
    metadata:
      labels:
        app: flink
        component: jobmanager
    spec:
      restartPolicy: OnFailure
      containers:
        - name: jobmanager
          image: apache/flink:latest
          env:
          - name: POD_IP
            valueFrom:
              fieldRef:
                apiVersion: v1
                fieldPath: status.podIP
          # The following args overwrite the value of jobmanager.rpc.address configured in the configuration config map to POD_IP.
          args: ["standalone-job", "--host", "$(POD_IP)", "--job-classname", "com.job.ClassName", <optional arguments>, <job arguments>] # optional arguments: ["--job-id", "<job id>", "--jars", "/path/to/artifact1,/path/to/artifact2", "--fromSavepoint", "/path/to/savepoint", "--allowNonRestoredState"]
          ports:
            - containerPort: 6123
              name: rpc
            - containerPort: 6124
              name: blob-server
            - containerPort: 8081
              name: webui
          livenessProbe:
            tcpSocket:
              port: 6123
            initialDelaySeconds: 30
            periodSeconds: 60
          volumeMounts:
            - name: flink-config-volume
              mountPath: /opt/flink/conf
            - name: job-artifacts-volume
              mountPath: /opt/flink/usrlib
          securityContext:
            runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      serviceAccountName: flink-service-account # Service account which has the permissions to create, edit, delete ConfigMaps
      volumes:
        - name: flink-config-volume
          configMap:
            name: flink-config
            items:
              - key: config.yaml
                path: config.yaml
              - key: log4j-console.properties
                path: log4j-console.properties
        - name: job-artifacts-volume
          hostPath:
            path: /host/path/to/job/artifacts

```

`apiVersion: batch/v1
kind: Job
metadata:
  name: flink-jobmanager
spec:
  parallelism: 1 # Set the value to greater than 1 to start standby JobManagers
  template:
    metadata:
      labels:
        app: flink
        component: jobmanager
    spec:
      restartPolicy: OnFailure
      containers:
        - name: jobmanager
          image: apache/flink:latest
          env:
          - name: POD_IP
            valueFrom:
              fieldRef:
                apiVersion: v1
                fieldPath: status.podIP
          # The following args overwrite the value of jobmanager.rpc.address configured in the configuration config map to POD_IP.
          args: ["standalone-job", "--host", "$(POD_IP)", "--job-classname", "com.job.ClassName", <optional arguments>, <job arguments>] # optional arguments: ["--job-id", "<job id>", "--jars", "/path/to/artifact1,/path/to/artifact2", "--fromSavepoint", "/path/to/savepoint", "--allowNonRestoredState"]
          ports:
            - containerPort: 6123
              name: rpc
            - containerPort: 6124
              name: blob-server
            - containerPort: 8081
              name: webui
          livenessProbe:
            tcpSocket:
              port: 6123
            initialDelaySeconds: 30
            periodSeconds: 60
          volumeMounts:
            - name: flink-config-volume
              mountPath: /opt/flink/conf
            - name: job-artifacts-volume
              mountPath: /opt/flink/usrlib
          securityContext:
            runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      serviceAccountName: flink-service-account # Service account which has the permissions to create, edit, delete ConfigMaps
      volumes:
        - name: flink-config-volume
          configMap:
            name: flink-config
            items:
              - key: config.yaml
                path: config.yaml
              - key: log4j-console.properties
                path: log4j-console.properties
        - name: job-artifacts-volume
          hostPath:
            path: /host/path/to/job/artifacts
`

taskmanager-job-deployment.yaml

`taskmanager-job-deployment.yaml`

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flink-taskmanager
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flink
      component: taskmanager
  template:
    metadata:
      labels:
        app: flink
        component: taskmanager
    spec:
      containers:
      - name: taskmanager
        image: apache/flink:latest
        env:
        args: ["taskmanager"]
        ports:
        - containerPort: 6122
          name: rpc
        livenessProbe:
          tcpSocket:
            port: 6122
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: flink-config-volume
          mountPath: /opt/flink/conf/
        - name: job-artifacts-volume
          mountPath: /opt/flink/usrlib
        securityContext:
          runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      volumes:
      - name: flink-config-volume
        configMap:
          name: flink-config
          items:
          - key: config.yaml
            path: config.yaml
          - key: log4j-console.properties
            path: log4j-console.properties
      - name: job-artifacts-volume
        hostPath:
          path: /host/path/to/job/artifacts

```

`apiVersion: apps/v1
kind: Deployment
metadata:
  name: flink-taskmanager
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flink
      component: taskmanager
  template:
    metadata:
      labels:
        app: flink
        component: taskmanager
    spec:
      containers:
      - name: taskmanager
        image: apache/flink:latest
        env:
        args: ["taskmanager"]
        ports:
        - containerPort: 6122
          name: rpc
        livenessProbe:
          tcpSocket:
            port: 6122
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: flink-config-volume
          mountPath: /opt/flink/conf/
        - name: job-artifacts-volume
          mountPath: /opt/flink/usrlib
        securityContext:
          runAsUser: 9999  # refers to user _flink_ from official flink image, change if necessary
      volumes:
      - name: flink-config-volume
        configMap:
          name: flink-config
          items:
          - key: config.yaml
            path: config.yaml
          - key: log4j-console.properties
            path: log4j-console.properties
      - name: job-artifacts-volume
        hostPath:
          path: /host/path/to/job/artifacts
`

### Local Recovery Enabled TaskManager StatefulSet#


```
apiVersion: v1
kind: ConfigMap
metadata:
  name: flink-config
  labels:
    app: flink
data:
  config.yaml: |+
    jobmanager.rpc.address: flink-jobmanager
    taskmanager.numberOfTaskSlots: 2
    blob.server.port: 6124
    jobmanager.rpc.port: 6123
    taskmanager.rpc.port: 6122
    state.backend.local-recovery: true
    process.taskmanager.working-dir: /pv    
---
apiVersion: v1
kind: Service
metadata:
  name: taskmanager-hl
spec:
  clusterIP: None
  selector:
    app: flink
    component: taskmanager
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: flink-taskmanager
spec:
  serviceName: taskmanager-hl
  replicas: 2
  selector:
    matchLabels:
      app: flink
      component: taskmanager
  template:
    metadata:
      labels:
        app: flink
        component: taskmanager
    spec:
      securityContext:
        runAsUser: 9999
        fsGroup: 9999
      containers:
      - name: taskmanager
        image: apache/flink:latest
        env:
          - name: POD_NAME
            valueFrom:
              fieldRef:
                fieldPath: metadata.name
        args: ["taskmanager", "-Dtaskmanager.resource-id=$(POD_NAME)"]
        ports:
        - containerPort: 6122
          name: rpc
        - containerPort: 6121
          name: metrics
        livenessProbe:
          tcpSocket:
            port: 6122
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: flink-config-volume
          mountPath: /opt/flink/conf/
        - name: pv
          mountPath: /pv
      volumes:
      - name: flink-config-volume
        configMap:
          name: flink-config
          items:
          - key: config.yaml
            path: config.yaml
          - key: log4j-console.properties
            path: log4j-console.properties
  volumeClaimTemplates:
  - metadata:
      name: pv
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 50Gi

```

`apiVersion: v1
kind: ConfigMap
metadata:
  name: flink-config
  labels:
    app: flink
data:
  config.yaml: |+
    jobmanager.rpc.address: flink-jobmanager
    taskmanager.numberOfTaskSlots: 2
    blob.server.port: 6124
    jobmanager.rpc.port: 6123
    taskmanager.rpc.port: 6122
    state.backend.local-recovery: true
    process.taskmanager.working-dir: /pv    
---
apiVersion: v1
kind: Service
metadata:
  name: taskmanager-hl
spec:
  clusterIP: None
  selector:
    app: flink
    component: taskmanager
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: flink-taskmanager
spec:
  serviceName: taskmanager-hl
  replicas: 2
  selector:
    matchLabels:
      app: flink
      component: taskmanager
  template:
    metadata:
      labels:
        app: flink
        component: taskmanager
    spec:
      securityContext:
        runAsUser: 9999
        fsGroup: 9999
      containers:
      - name: taskmanager
        image: apache/flink:latest
        env:
          - name: POD_NAME
            valueFrom:
              fieldRef:
                fieldPath: metadata.name
        args: ["taskmanager", "-Dtaskmanager.resource-id=$(POD_NAME)"]
        ports:
        - containerPort: 6122
          name: rpc
        - containerPort: 6121
          name: metrics
        livenessProbe:
          tcpSocket:
            port: 6122
          initialDelaySeconds: 30
          periodSeconds: 60
        volumeMounts:
        - name: flink-config-volume
          mountPath: /opt/flink/conf/
        - name: pv
          mountPath: /pv
      volumes:
      - name: flink-config-volume
        configMap:
          name: flink-config
          items:
          - key: config.yaml
            path: config.yaml
          - key: log4j-console.properties
            path: log4j-console.properties
  volumeClaimTemplates:
  - metadata:
      name: pv
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 50Gi
`

 Back to top
