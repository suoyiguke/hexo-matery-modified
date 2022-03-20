---
title: kafak-原理（一）了解基本概念.md
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
title: kafak-原理（一）了解基本概念.md
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
###先看图
![](https://upload-images.jianshu.io/upload_images/13965490-1e04555e61352dfa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

zookeeper集群，kafka是配合zookeeper进行工作的。
kafka集群中可以看到有若干个Broker，其中一个broker是leader，其他的broker是follower。
consumer外面包裹了一层Consumer group。


###基本术语

Broker：Kafka 集群包含一个或多个服务器，这种服务器被称为 broker。

Topic：每条发布到 Kafka 集群的消息都有一个类别（主题），这个类别被称为 Topic。（物理上不同 Topic 的消息分开存储，逻辑上一个 Topic 的消息虽然保存于一个或多个 broker 上，但用户只需指定消息的 Topic 即可生产或消费数据而不必关心数据存于何处）。kafka中消息订阅和发送都是基于某个topic。比如有个topic叫做NBA赛事信息，那么producer会把NBA赛事信息的消息发送到此topic下面。所有订阅此topic的consumer将会拉取到此topic下的消息。Topic就像一个特定主题的收件箱，producer往里丢，consumer取走。

Partition：Partition 是物理上的概念，每个 Topic 包含一个或多个 Partition。

Producer：负责发布消息到 Kafka broker。

Consumer：消息消费者，向 Kafka broker 读取消息的客户端。

Consumer Group：每个 Consumer 属于一个特定的 Consumer Group（可为每个 Consumer 指定 group name，若不指定 group name 则属于默认的 group）。



###分区概念 partition：
  一个Topic可以认为是一类消息，每个topic将被分成多个partition(区),每个partition在存储层面是append log文件。任何发布到此partition的消息都会被直接追加到log文件的尾部，每条消息在文件中的位置称为offset（偏移量），offset为一个long型数字，它用来唯一标记某个分区内的一条消息。kafka并没有提供其它额外的索引机制来存储offset，因为在kafka中几乎不允许对消息进行“随机读写”。







###Consumer与topic关系以及机制
Kafka和其它消息系统有一个不一样的设计，在consumer之上加了一层group。

1、同一个group的consumer可以并行消费同一个topic的消息，但是同group的consumer，不会重复消费。这就好比多个consumer组成了一个团队，一起干活，当然干活的速度就上来了。如果所有的consumer都具有相同的group，这种情况和JMS queue模式很像，消息将会在consumers之间负载均衡。（类似于简书 pc端和电脑端的消息通，消息在pc端被消费，那么app端也就不会再推送这条消息）

2、如果同一个topic需要被多次消费，可以通过设立多个consumer group来实现。每个group分别消费，互不影响。如果所有的consumer都具有不同的group，那这就是"发布-订阅"，消息将会广播给所有的消费者。（需要被多次消费的消息，类似简书的关注功能。被关注用户的发帖消息会推送到每个关注用户上）


###消费这个动作的先后顺序
在kafka中，一个partition中的消息只会被group中的一个consumer消费(同一时刻)，每个group中consumer消息消费互相独立，我们可以认为一个group是一个"订阅"者。一个Topic中的每个partions只会被一个"订阅者"中的一个consumer消费，不过一个consumer可以同时消费多个partitions中的消息。

kafka只能保证一个partition中的消息被某个consumer消费时是顺序的。事实上，从Topic角度来说,，当有多个partitions时，消息仍不是全局有序的。

通常情况下，一个group中会包含多个consumer，这样不仅可以提高topic中消息的并发消费能力，而且还能提高"故障容错"性。如果group中的某个consumer失效，那么其消费的partitions将会有其他consumer自动接管。kafka的设计原理决定对于一个topic，同一个group中不能有多于partitions个数的consumer同时消费，否则将意味着某些consumer将无法得到消息。

