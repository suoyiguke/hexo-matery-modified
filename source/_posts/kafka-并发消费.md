---
title: kafka-并发消费.md
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
title: kafka-并发消费.md
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

在上述的示例中，我们配置的每一个 Spring-Kafka `@KafkaListener` ，都是**串行**消费的。显然，这在监听的 Topic 每秒消息量比较大的时候，会导致消费不及时，导致消息积压的问题。

虽然说，我们可以通过启动多个 JVM 进程，实现**多进程的并发消费**，从而加速消费的速度。但是问题是，否能够实现**多线程**的并发消费呢？答案是**有**。

在[「3.9 @KafkaListener」](https://www.iocoder.cn/Spring-Boot/Kafka/#)小节中，我们可以看到该注解有 `concurrency` 属性，它可以指定并发消费的线程数。例如说，如果设置 `concurrency=4` 时，Spring-Kafka 就会为**该** `@KafkaListener` 创建 4 个线程，进行并发消费。

考虑到让胖友能够更好的理解 `concurrency` 属性，我们来简单说说 Spring-Kafka 在这块的实现方式。我们来举个例子：

*   首先，我们来创建一个 Topic 为 `"DEMO_06"` ，并且设置其 Partition 分区数为 **10** 。
*   然后，我们创建一个 Demo06Consumer 类，并在其消费方法上，添加 `@KafkaListener(concurrency=2)` 注解。
*   再然后，我们启动项目。Spring-Kafka 会根据 `@KafkaListener(concurrency=2)` 注解，创建 **2** 个 Kafka Consumer 。注意噢，是 **2** 个 Kafka Consumer 呢！！！后续，每个 Kafka Consumer 会被**单独**分配到一个线程中，进行拉取消息，消费消息。
*   之后，Kafka Broker 会将 Topic 为 `"DEMO_06"` 分配给创建的 **2** 个 Kafka Consumer 各 **5** 个 Partition 。😈 如果不了解 Kafka Broker “分配区分”机制单独胖友，可以看看 [《Kafka 消费者如何分配分区》](http://www.iocoder.cn/Fight/How-do-Kafka-consumers-allocate-partitions/?self) 文章。
*   这样，因为 `@KafkaListener(concurrency=2)` 注解，创建 **2** 个 Kafka Consumer ，就在**各自的线程中**，拉取各自的 Topic 为 `"DEMO_06"` 的 Partition 的消息，各自**串行**消费。从而，实现**多线程**的并发消费。

酱紫讲解一下，胖友对 Spring-Kafka 实现**多线程**的并发消费的机制，是否理解了。不过有一点要注意，不要配置 `concurrency` 属性过大，则创建的 Kafka Consumer 分配不到消费 Topic 的 Partition 分区，导致不断的空轮询。

> 友情提示：可以选择不看。
> 
> 在理解 Spring-Kafka 提供的**并发消费**机制，花费了好几个小时，主要陷入到了一个误区。
> 
> 如果胖友有使用过 RocketMQ 的并发消费，会发现只要创建一个 RocketMQ Consumer 对象，然后 Consumer 拉取完消息之后，丢到 Consumer 的线程池中执行消费，从而实现并发消费。
> 
> 而在 Spring-Kafka 提供的并发消费，会发现需要创建多个 Kafka Consumer 对象，并且每个 Consumer 都单独分配一个线程，然后 Consumer 拉取完消息之后，在各自的线程中执行消费。
> 
> 又或者说，Spring-Kafka 提供的并发消费，很像 RocketMQ 的顺序消费。😈 从感受上来说，Spring-Kafka 的并发消费像 BIO ，RocketMQ 的并发消费像 NIO 。
> 
> 不过，理论来说，在原生的 Kafka 客户端，也是能封装出和 RocketMQ Consumer 一样的并发消费的机制。
> 
> 也因此，在使用 Kafka 的时候，每个 Topic 的 Partition 在消息量大的时候，要注意设置的相对大一些。

下面，我们开始本小节的示例。本示例就是上述举例的具体实现。考虑到不污染上述的示例，我们新建一个 [lab-03-kafka-demo-concurrency](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-03-kafka/lab-03-kafka-demo-concurrency) 项目。

## 9.1 引入
