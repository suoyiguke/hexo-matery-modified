---
title: kakfa消息序列化.md
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
title: kakfa消息序列化.md
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
对于胖友来说，可能最关心的是，消息 Message 是怎么序列化的。

*   在序列化时，我们使用了 JsonSerializer 序列化 Message 消息对象，它会在 Kafka 消息 [Headers](https://kafka.apache.org/0110/javadoc/index.html?org/apache/kafka/common/header/Headers.html) 的 `__TypeId__` 上，值为 Message 消息对应的**类全名**。
*   在反序列化时，我们使用了 JsonDeserializer 序列化出 Message 消息对象，它会根据 Kafka 消息 [Headers](https://kafka.apache.org/0110/javadoc/index.html?org/apache/kafka/common/header/Headers.html) 的 `__TypeId__` 的值，反序列化消息内容成该 Message 对象。
