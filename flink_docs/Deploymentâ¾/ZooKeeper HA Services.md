# ZooKeeper HA Services


> 
        This documentation is for an unreleased version of Apache Flink. We recommend you use the latest stable version.
    


# ZooKeeper HA Services#


Flink’s ZooKeeper HA services use ZooKeeper for high availability services.


Flink leverages ZooKeeper for distributed coordination between all running JobManager instances.
ZooKeeper is a separate service from Flink, which provides highly reliable distributed coordination via leader election and light-weight consistent state storage.
Check out ZooKeeper’s Getting Started Guide for more information about ZooKeeper.
Flink includes scripts to bootstrap a simple ZooKeeper installation.


## Configuration#


In order to start an HA-cluster you have to configure the following configuration keys:

* 
high-availability.type (required):
The high-availability.type option has to be set to zookeeper.
high-availability.type: zookeeper

* 
high-availability.storageDir (required):
JobManager metadata is persisted in the file system high-availability.storageDir and only a pointer to this state is stored in ZooKeeper.
high-availability.storageDir: hdfs:///flink/recovery
The storageDir stores all metadata needed to recover a JobManager failure.

* 
high-availability.zookeeper.quorum (required):
A ZooKeeper quorum is a replicated group of ZooKeeper servers, which provide the distributed coordination service.
high-availability.zookeeper.quorum: address1:2181[,...],addressX:2181
Each addressX:port refers to a ZooKeeper server, which is reachable by Flink at the given address and port.

* 
high-availability.zookeeper.path.root (recommended):
The root ZooKeeper node, under which all cluster nodes are placed.
high-availability.zookeeper.path.root: /flink

* 
high-availability.cluster-id (recommended):
The cluster-id ZooKeeper node, under which all required coordination data for a cluster is placed.
high-availability.cluster-id: /default_ns # important: customize per cluster
Important:
You should not set this value manually when running on YARN, native Kubernetes or on another cluster manager.
In those cases a cluster-id is being automatically generated.
If you are running multiple Flink HA clusters on bare metal, you have to manually configure separate cluster-ids for each cluster.


high-availability.type (required):
The high-availability.type option has to be set to zookeeper.

`high-availability.type`
`zookeeper`

```
high-availability.type: zookeeper
```


high-availability.storageDir (required):
JobManager metadata is persisted in the file system high-availability.storageDir and only a pointer to this state is stored in ZooKeeper.

`high-availability.storageDir`

```
high-availability.storageDir: hdfs:///flink/recovery
```


The storageDir stores all metadata needed to recover a JobManager failure.

`storageDir`

high-availability.zookeeper.quorum (required):
A ZooKeeper quorum is a replicated group of ZooKeeper servers, which provide the distributed coordination service.


```
high-availability.zookeeper.quorum: address1:2181[,...],addressX:2181
```


Each addressX:port refers to a ZooKeeper server, which is reachable by Flink at the given address and port.

`addressX:port`

high-availability.zookeeper.path.root (recommended):
The root ZooKeeper node, under which all cluster nodes are placed.


```
high-availability.zookeeper.path.root: /flink
```


high-availability.cluster-id (recommended):
The cluster-id ZooKeeper node, under which all required coordination data for a cluster is placed.


```
high-availability.cluster-id: /default_ns # important: customize per cluster
```


Important:
You should not set this value manually when running on YARN, native Kubernetes or on another cluster manager.
In those cases a cluster-id is being automatically generated.
If you are running multiple Flink HA clusters on bare metal, you have to manually configure separate cluster-ids for each cluster.


### Example configuration#


Configure high availability mode and ZooKeeper quorum in Flink configuration file:


```
high-availability.type: zookeeper
high-availability.zookeeper.quorum: localhost:2181
high-availability.zookeeper.path.root: /flink
high-availability.cluster-id: /cluster_one # important: customize per cluster
high-availability.storageDir: hdfs:///flink/recovery

```

`high-availability.type: zookeeper
high-availability.zookeeper.quorum: localhost:2181
high-availability.zookeeper.path.root: /flink
high-availability.cluster-id: /cluster_one # important: customize per cluster
high-availability.storageDir: hdfs:///flink/recovery
`

 Back to top


## Configuring for ZooKeeper Security#


If ZooKeeper is running in secure mode with Kerberos, you can override the following configurations in Flink configuration file as necessary:


```
# default is "zookeeper". If the ZooKeeper quorum is configured
# with a different service name then it can be supplied here.

zookeeper.sasl.service-name: zookeeper 

# default is "Client". The value needs to match one of the values
# configured in "security.kerberos.login.contexts".   
zookeeper.sasl.login-context-name: Client  

```

`# default is "zookeeper". If the ZooKeeper quorum is configured
# with a different service name then it can be supplied here.

zookeeper.sasl.service-name: zookeeper 

# default is "Client". The value needs to match one of the values
# configured in "security.kerberos.login.contexts".   
zookeeper.sasl.login-context-name: Client  
`

For more information on Flink configuration for Kerberos security, please refer to the security section of the Flink configuration page.
You can also find further details on how Flink sets up Kerberos-based security internally.


 Back to top


## Advanced Configuration#


### Tolerating Suspended ZooKeeper Connections#


Per default, Flink’s ZooKeeper client treats suspended ZooKeeper connections as an error.
This means that Flink will invalidate all leaderships of its components and thereby triggering a failover if a connection is suspended.


This behaviour might be too disruptive in some cases (e.g., unstable network environment).
If you are willing to take a more aggressive approach, then you can tolerate suspended ZooKeeper connections and only treat lost connections as an error via high-availability.zookeeper.client.tolerate-suspended-connections.
Enabling this feature will make Flink more resilient against temporary connection problems but also increase the risk of running into ZooKeeper timing problems.


For more information take a look at Curator’s error handling.


## Bootstrap ZooKeeper#


If you don’t have a running ZooKeeper installation, you can use the helper scripts, which ship with Flink.


There is a ZooKeeper configuration template in conf/zoo.cfg.
You can configure the hosts to run ZooKeeper on with the server.X entries, where X is a unique ID of each server:

`conf/zoo.cfg`
`server.X`

```
server.X=addressX:peerPort:leaderPort
[...]
server.Y=addressY:peerPort:leaderPort

```

`server.X=addressX:peerPort:leaderPort
[...]
server.Y=addressY:peerPort:leaderPort
`

The script bin/start-zookeeper-quorum.sh will start a ZooKeeper server on each of the configured hosts.
The started processes start ZooKeeper servers via a Flink wrapper, which reads the configuration from conf/zoo.cfg and makes sure to set some required configuration values for convenience.
In production setups, it is recommended to manage your own ZooKeeper installation.

`bin/start-zookeeper-quorum.sh`
`conf/zoo.cfg`

 Back to top
