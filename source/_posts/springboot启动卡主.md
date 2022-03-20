---
title: springboot启动卡主.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
---
title: springboot启动卡主.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
卡死原因是springboot-name实例名变了
~~~
2022-01-19 07:28:35 | [main] INFO  org.springframework.amqp.rabbit.connection.CachingConnectionFactory - Attempting to connect to: [192.168.1.54:5672]
2022-01-19 07:28:35 | [DiscoveryClient-InstanceInfoReplicator-0] INFO  com.netflix.discovery.DiscoveryClient - DiscoveryClient_SERVICE-TREASURE-PLATFORM-TEST2/172.17.0.2:10010 - registration status: 204
2022-01-19 07:28:35 | [main] INFO  org.springframework.amqp.rabbit.connection.CachingConnectionFactory - Created new connection: rabbitConnectionFactory#1640190a:0/SimpleConnection@5ef85555 [delegate=amqp://user@192.168.1.54:5672/, localPort= 46610]
2022-01-19 07:28:35 | [main] INFO  com.gbm.cloud.MgbTreasureSystemApplication - Started MgbTreasureSystemApplication in 25.544 seconds (JVM running for 26.297)
2022-01-19 07:28:35 | [main] INFO  com.gbm.cloud.MgbTreasureSystemApplication - <==========启动成功=========>

~~~

这里应该还会输出三行：
2022-01-19 17:07:00 | [RMI TCP Connection(3)-192.168.2.26] INFO  org.apache.catalina.core.ContainerBase.[Tomcat].[localhost].[/] - Initializing Spring DispatcherServlet 'dispatcherServlet'
2022-01-19 17:07:00 | [RMI TCP Connection(3)-192.168.2.26] INFO  org.springframework.web.servlet.DispatcherServlet - Initializing Servlet 'dispatcherServlet'
2022-01-19 17:07:00 | [RMI TCP Connection(3)-192.168.2.26] INFO  org.springframework.web.servlet.DispatcherServlet - Completed initialization in 28 ms
