---
title: kafak-原理（二）-分区概念.md
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
title: kafak-原理（二）-分区概念.md
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
 **分区（Partition）**

大多数消息系统，同一个topic下的消息，存储在一个队列。

>分区的概念就是把这个队列划分为若干个小队列，每一个小队列就是一个分区，如下图：

![image](https://upload-images.jianshu.io/upload_images/13965490-1eca643f7f1092ce?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样做的好处是什么呢？其实从上图已经可以看出来。无分区时，一个topic只有一个消费者在消费这个消息队列。采用分区后，如果有两个分区，最多两个消费者同时消费，消费的速度肯定会更快。如果觉得不够快，可以加到四个分区，让四个消费者并行消费。分区的设计大大的提升了kafka的吞吐量！！

我们再结合下图继续讲解Partition。

![image](https://upload-images.jianshu.io/upload_images/13965490-988885efb20dc4c2?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

此图包含如下几个知识点：

1、一个partition只能被同组的一个consumer消费（图中只会有一个箭头指向一个partition）
2、同一个组里的一个consumer可以消费多个partition（图中第一个consumer消费Partition 0和3）
3、消费效率最高的情况是partition和consumer数量相同。这样确保每个consumer专职负责一个partition。
4、consumer数量不能大于partition数量。由于第一点的限制，当consumer多于partition时，就会有consumer闲置。
5、consumer group可以认为是一个订阅者的集群，其中的每个consumer负责自己所消费的分区
