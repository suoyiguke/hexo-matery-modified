---
title: kafka配置公网访问.md
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
title: kafka配置公网访问.md
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

###通过内网穿透，这种情况比较特殊
现在有一台公网ip为14.127.73.253的服务器，通过内网穿透可以提供公网访问。
将kafka端口9092映射到了43398。
zookeeper 部署在2181端口，zookeeper没有进行端口映射，因为zookeeper不需要共公网访问。

那么需要如下配置即可在公网访问kafka。
1、listeners 指定 0.0.0.0:本地端口
2、advertised.listeners指定 公网ip:公网端口
~~~
listeners=PLAINTEXT://0.0.0.0:9092
advertised.listeners=PLAINTEXT://14.127.73.253:43398
zookeeper.connect=localhost:2181
~~~14.127.75.87
