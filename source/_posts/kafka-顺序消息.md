---
title: kafka-顺序消息.md
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
title: kafka-顺序消息.md
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
> 示例代码对应仓库：[lab-03-kafka-demo-concurrency](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-03-kafka/lab-03-kafka-demo-concurrency) 。

我们先来一起了解下顺序消息的**顺序消息**的定义：

*   普通顺序消息 ：Producer 将相关联的消息发送到相同的消息队列。
*   完全严格顺序 ：在【普通顺序消息】的基础上，Consumer 严格顺序消费。

在上述的示例中，我们看到 Spring-Kafka 在 Consumer 消费消息时，**天然**就支持按照 Topic 下的 Partition 下的消息，**顺序消费**。即使在[「9\. 并发消费」](https://www.iocoder.cn/Spring-Boot/Kafka/#)时，也能保证如此。

那么此时，我们只需要考虑将 Producer 将相关联的消息发送到 Topic 下的相同的 Partition 即可。如果胖友了解 Producer 发送消息的分区策略的话，只要我们发送消息时，指定了消息的 key ，Producer 则会根据 key 的哈希值取模来获取到其在 Topic 下对应的 Partition 。完美~~不了解的 Producer 分区选择策略的胖友，可以看看 [《Kafka 发送消息分区选择策略详解》](https://leokongwq.github.io/2017/02/27/mq-kafka-producer-partitioner.html) 文章。

下面，我们开始本小节的示例。该示例，我们会在[「9\. 并发消费」](https://www.iocoder.cn/Spring-Boot/Kafka/#)的 [lab-03-kafka-demo-concurrency](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-03-kafka/lab-03-kafka-demo-concurrency) 项目中，继续改造。
