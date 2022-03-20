---
title: kafka运行问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mq-kafka
categories: mq-kafka
---
---
title: kafka运行问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mq-kafka
categories: mq-kafka
---

1、kafak连接zookeeper超时

>kafka.zookeeper.ZooKeeperClientTimeoutException: Timed out waiting for connection while in state: CONNECTING

解决：
重启zookeeper


2、我在WIN7系统电脑启动kafka的服务端，启动后启动窗口报错，如下：

>[2020-08-21 14:49:05,426] ERROR [ReplicaManager broker=0] Error while making broker the leader for partition Topic: __consumer_offsets; Partition: 13; Leader: None; AllReplicas: ; InSyncReplicas:  in dir None (kafka.server.ReplicaManager)

删除kafka-logs下的所有日志即可解决，亲测有效。

**kafka在windows平台就是有这个BUG，没办法。只能手动删除\kafka-logs里的日志文件重启kafka**





3、生产者发送消息


> Error when sending message to topic mytopic with key: null, value: 3 bytes with error: (org.apache.kafka.clients.producer.internals.ErrorLoggingCallback)


出现该异常，很有可能你的topic已死，要不新建一个其他名字的topic。要不就修改kafka的配置文件：server.properties,添加配置auto.create.topics.enable=true，让生产者自动创建。 
一定先找日志，定位具体原因！！！



4、Kafka启动报错：ERROR Shutdown broker because all log dirs in D:\kafka\kafka_2.12-2.2.0\kafkakafka_2.12-2.2.0logs have failed (kafka.log.LogManager)

解决方法：删除Zookeeper的日志即可




5、生产者，发送消息报错
>WARN [Producer clientId=console-producer] Error while fetching metadata with correlation id 1 : {mytopic=LEADER_NOT_AVAILABLE} (org.apache.kafka.clients.NetworkClient)

6、启动消费者，kafka立即报错
>org.apache.kafka.common.errors.KafkaStorageException: Error while creating log for __consumer_offsets-35 in dir D:\kafka_2.12-2.1.1\kafka_2.12-2.1.1\data\kafka-logs
Caused by: java.io.IOException: Map failed

检查下环境变量 java_home下的 路径，看看Java版本是不是32位的。请使用64位的java 运行


7、出现这种原因就是ip和端口错了

Connection to node 0 (/14.127.73.253:43398) could not be established. Broker may not be available.
