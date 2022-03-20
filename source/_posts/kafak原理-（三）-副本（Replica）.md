---
title: kafak原理-（三）-副本（Replica）.md
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
title: kafak原理-（三）-副本（Replica）.md
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
副本（Replica）

提到副本，肯定就会想到正本。副本是正本的拷贝。在kafka中，正本和副本都称之为副本（Repalica），但存在leader和follower之分。活跃的称之为leader，其他的是follower。

每个分区的数据都会有多份副本，以此来保证Kafka的高可用。

Topic、partition、replica的关系如下图：

![image](https://upload-images.jianshu.io/upload_images/13965490-2e21d70d8456e39f?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

topic下会划分多个partition，每个partition都有自己的replica，其中只有一个是leader replica，其余的是follower replica。

消息进来的时候会先存入leader replica，然后从leader replica复制到follower replica。只有复制全部完成时，consumer才可以消费此条消息。这是为了确保意外发生时，数据可以恢复。consumer的消费也是从leader replica读取的。

由此可见，leader replica做了大量的工作。所以如果不同partition的leader replica在kafka集群的broker上分布不均匀，就会造成负载不均衡。

kafka通过轮询算法保证leader replica是均匀分布在多个broker上。如下图。

![image](https://upload-images.jianshu.io/upload_images/13965490-4ae6ba6903846849?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看到每个partition的leader replica均匀的分布在三个broker上，follower replica也是均匀分布的。

关于Replica，有如下知识点：
1、Replica均匀分配在Broker上，同一个partition的replica不会在同一个borker上
2、同一个partition的Replica数量不能多于broker数量。多个replica为了数据安全，一台server存多个replica没有意义。server挂掉，上面的副本都要挂掉。
3、分区的leader replica均衡分布在broker上。此时集群的负载是均衡的。这就叫做分区平衡

分区平衡是个很重要的概念，接下来我们就来讲解分区平衡。
