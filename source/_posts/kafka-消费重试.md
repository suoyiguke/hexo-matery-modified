---
title: kafka-消费重试.md
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
title: kafka-消费重试.md
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
Spring-Kafka 提供**消费重试**的机制。在消息**消费失败**的时候，Spring-Kafka 会通过**消费重试**机制，重新投递该消息给 Consumer ，让 Consumer 有机会重新消费消息，实现消费成功。

当然，Spring-Kafka 并不会无限重新投递消息给 Consumer 重新消费，而是在默认情况下，达到 N 次重试次数时，Consumer 还是消费失败时，该消息就会进入到**死信队列**。

> 死信队列用于处理无法被正常消费的消息。当一条消息初次消费失败，Spring-Kafka 会自动进行消息重试；达到最大重试次数后，若消费依然失败，则表明消费者在正常情况下无法正确地消费该消息，此时，Spring-Kafka 不会立刻将消息丢弃，而是将其发送到该消费者对应的特殊队列中。
> 
> Spring-Kafka 将这种正常情况下无法被消费的消息称为死信消息（Dead-Letter Message），将存储死信消息的特殊队列称为死信队列（Dead-Letter Queue）。后续，我们可以通过对死信队列中的消息进行重发，来使得消费者实例再次进行消费。

*   在[《芋道 Spring Boot 消息队列 RocketMQ 入门》](http://www.iocoder.cn/Spring-Boot/RocketMQ/?self)的[「6\. 消费重试」](https://www.iocoder.cn/Spring-Boot/Kafka/#)小节中，我们可以看到，消费重试和死信队列，是 RocketMQ 自带的功能。
*   而在 Kafka 中，消费重试和死信队列，是由 Spring-Kafka 所封装提供的。

每条消息的失败重试，是可以配置一定的**间隔时间**。具体，我们在示例的代码中，来进行具体的解释。

下面，我们开始本小节的示例。该示例，我们会在[「3\. 快速入门」](https://www.iocoder.cn/Spring-Boot/Kafka/#)的 [lab-31-kafka-demo](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-03-kafka/lab-03-kafka-demo) 项目中，继续改造。


https://www.iocoder.cn/Spring-Boot/Kafka/
