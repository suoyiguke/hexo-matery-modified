---
title: kafka-广播消费.md
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
title: kafka-广播消费.md
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
示例代码对应仓库：lab-03-kafka-demo-broadcast 。  在上述的示例中，我们看到的都是使用集群消费。而在一些场景下，我们需要使用广播消费。  广播消费模式下，相同 Consumer Group 的每个 Consumer 实例都接收全量的消息。 不过 Kafka 并不直接提供内置的广播消费的功能！！！此时，我们只能退而求其次，每个 Consumer 独有一个 Consumer Group ，从而保证都能接收到全量的消息。

 例如说，在应用中，缓存了数据字典等配置表在内存中，可以通过 Kafka 广播消费，实现每个应用节点都消费消息，刷新本地内存的缓存。  

又例如说，我们基于 WebSocket 实现了 IM 聊天，在我们给用户主动发送消息时，因为我们不知道用户连接的是哪个提供 WebSocket 的应用，所以可以通过 Kafka 广播消费，每个应用判断当前用户是否是和自己提供的 WebSocket 服务连接，如果是，则推送消息给用户。  下面，我们开始本小节的示例。考虑到不污染上述的示例，我们新建一个 lab-03-kafka-demo-broadcast 项目。
