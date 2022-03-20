---
title: kafka-单机版本安装.md
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
title: kafka-单机版本安装.md
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
###配置


zk配置文件 zookeeper.properties
~~~
# 指定zk的数据路径（核心）
dataDir=D:/kafka_2.12-2.1.1/kafka_2.12-2.1.1/data/zk-data
# zk端口
clientPort=2181
maxClientCnxns=0
~~~



kafka 配置文件 server.properties
~~~
############################# Server Basics #############################
broker.id=0
############################# Socket Server Settings #############################
# 配置kafka 监听的ip端口（核心）
listeners=PLAINTEXT://localhost:9092
num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
############################# Log Basics #############################
# kafka日志路径（核心）
log.dirs=D:/kafka_2.12-2.1.1/kafka_2.12-2.1.1/data/kafka-logs
num.partitions=1
num.recovery.threads.per.data.dir=1

############################# Internal Topic Settings  #############################
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1

############################# Log Flush Policy #############################



############################# Log Retention Policy #############################
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

############################# Zookeeper #############################
# kafka访问zk的 ip:端口
zookeeper.connect=localhost:2181
zookeeper.connection.timeout.ms=6000
############################# Group Coordinator Settings #############################
group.initial.rebalance.delay.ms=0
# 自动创建topics
auto.create.topics.enable=true
~~~


###启动
1、启动zk：在当前目录下打开dos窗口，并执行如下命令：
~~~
zookeeper-server-start.bat ..\..\config\zookeeper.properties
~~~

2、启动kafka
~~~
kafka-server-start.bat ..\..\config\server.properties
~~~

###测试

1、创建主题
~~~
kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic mytopic
~~~
2、查看创建的主题
~~~
kafka-topics.bat --list --zookeeper localhost:2181
~~~
3、启动生产者
~~~
kafka-console-producer.bat --broker-list localhost:9092 --topic mytopic
~~~
此时，可输入任意字符，等消费者启动后，就能收到了。

4、启动消费者
~~~
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic mytopic --from-beginning
~~~
