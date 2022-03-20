---
title: eureka.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springcloud
categories: springcloud
---
---
title: eureka.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springcloud
categories: springcloud
---
###eureka 注册中心原理
1、服务到注册中心 Aplication Server-->Eureka Server
- Register 注册
- Renew  服务向注册中心发送心跳包
- Cancel  下线服务

 2、注册中心之间
- Replicate 同步数据  Eureka Server-->Eureka Server

3、服务消费者到注册中心 Aplication Client -->Eureka Server
- Get Register 拉服务列表取

4、消费者到服务生产者  Aplication Client --> Aplication Server
- Make Remote Call  完成服务的远程调用


###有两种原因导致微服务与eureka之间出现问题
- 微服务自己的故障
- 微服务与eureka之前出现网络故障

####eureka自我保护统计模式
eureka server在运行期间会统计心跳失败比例在15分钟之内是否低于85%。低于则将该服务实例保护起来，
让它不会因为到了90秒而过期，同时出现一个警告。这种算法称为eureka server的自我保护模式。

####如何关闭自我保护
~~~
eureka:
  server:
    enable-self-preservation: false # 关闭自我保护机制
    eviction-interval-timer-in-ms: 60000 # 清理间隔 60秒
~~~

###优雅停服
主动下线服务
actuator  


###注册中心安全认证



### 相关配置
eureka 如果是单机则需要把这两个参数都设置为false。单机为true的话自己会注册自己，会有问题！

注册到eureka
- register-with-eureka: false
拉取配置信息
- fetch-registry: false

使用ip地址注册。否则会默认使用主机名
- prefer-ip-address: true 
- instance-id: ${spring.cloud.client.ip-address}:${server.port}

~~~
server:
  port: 8888
spring:
  application:
    name: EUREKA-CENTER
eureka:
  instance:
    hostname: localhost
    prefer-ip-address: true # 使用ip地址注册。否则会默认使用主机名
    instance-id: ${spring.cloud.client.ip-address}:${server.port}
  client:
    #是否将自己注册到eureka服务注册中心，默认为true
    register-with-eureka: true
    #是否从服务注册中心获取可用的服务清单，默认为true
    fetch-registry: true
    serviceUrl:
      defaultZone: http://localhost:8888/eureka/
~~~

启动后访问 http://localhost:8888/ 会看到eureka的配置面板
