---
title: kafka-kafka-配置之-listeners-和-advertised-listeners.md
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
title: kafka-kafka-配置之-listeners-和-advertised-listeners.md
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
## 内网访问

在内网部署及访问kafka时，只需要配置listeners参数即可，比如

~~~
# The address the socket server listens on. It will get the value returned from 
# java.net.InetAddress.getCanonicalHostName() if not configured.
#   FORMAT:
#     listeners = listener_name://host_name:port
#   EXAMPLE:
#     listeners = PLAINTEXT://your.host.name:9092
listeners=PLAINTEXT://192.168.133.11:9092
~~~

若只配置 listeners ，此时advertised.listeners默认值等于listeners参数的值

## 内外网访问

在内网部署kafka服务，并且生产者或者消费者在外网环境时，需要添加额外的配置，比如
~~~
# Hostname and port the broker will advertise to producers and consumers. If not set, 
# it uses the value for "listeners" if configured.  Otherwise, it will use the value
# returned from java.net.InetAddress.getCanonicalHostName().
listener.security.protocol.map=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
listeners=INTERNAL://192.168.133.11:9092,EXTERNAL://192.168.133.11:9093
advertised.listeners=INTERNAL://192.168.133.11:9092,EXTERNAL://<公网ip>:<端口>
inter.broker.listener.name=INTERNAL
~~~
