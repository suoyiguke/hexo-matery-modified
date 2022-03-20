---
title: webflux-介绍.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
---
title: webflux-介绍.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
# 一、关于WebFlux

　　我们知道传统的Web框架，比如说：struts2，springmvc等都是基于Servlet API与Servlet容器基础之上运行的，在Servlet3.1之后才有了异步非阻塞的支持。而WebFlux是一个典型非阻塞异步的框架，它的核心是基于Reactor的相关API实现的。相对于传统的web框架来说，它可以运行在诸如Netty，Undertow及支持Servlet3.1的容器上，因此它的运行环境的可选择行要比传统web框架多的多。

　　根据官方的说法，webflux主要在如下两方面体现出独有的优势：

　　1）非阻塞式

　　　　其实在servlet3.1提供了非阻塞的API，WebFlux提供了一种比其更完美的解决方案。使用非阻塞的方式可以利用较小的线程或硬件资源来处理并发进而提高其可伸缩性

　　2) 函数式编程端点

老生常谈的编程方式了，Spring5必须让你使用java8，那么函数式编程就是java8重要的特点之一，而WebFlux支持函数式编程来定义路由端点处理请求。

# 二、SpringMVC与SpringWebFlux

我们先来看官网的一张图：

![image](https://upload-images.jianshu.io/upload_images/13965490-c7906017fea2529c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

　　它们都可以用注解式编程模型，都可以运行在tomcat，jetty，undertow等servlet容器当中。但是SpringMVC采用命令式编程方式，代码一句一句的执行，这样更有利于理解与调试，而WebFlux则是基于异步响应式编程，对于初次接触的码农们来说会不习惯。对于这两种框架官方给出的建议是：

　　1）如果原先使用用SpringMVC好好的话，则没必要迁移。因为命令式编程是编写、理解和调试代码的最简单方法。因为老项目的类库与代码都是基于阻塞式的。

　　2）如果你的团队打算使用非阻塞式web框架，WebFlux确实是一个可考虑的技术路线，而且它支持类似于SpringMvc的Annotation的方式实现编程模式，也可以在微服务架构中让WebMvc与WebFlux共用Controller，切换使用的成本相当小

　　3）在SpringMVC项目里如果需要调用远程服务的话，你不妨考虑一下使用WebClient，而且方法的返回值可以考虑使用Reactive Type类型的，当每个调用的延迟时间越长，或者调用之间的相互依赖程度越高，其好处就越大

　　我个人意见是：官网明确指出，SpringWebFlux并不是让你的程序运行的更快(相对于SpringMVC来说)，而是在有限的资源下提高系统的伸缩性，因此当你对响应式编程非常熟练的情况下并将其应用于新的系统中，还是值得考虑的，否则还是老老实实的使用WebMVC吧


>最后，也是非常重要的一点：异步非阻塞并不会使程序运行得更快。WebFlux 并不能使接口的响应时间缩短，它仅仅能够提升吞吐量和伸缩性。
Spring WebFlux 是一个异步非阻塞的 Web 框架，所以，它特别适合应用在 IO 密集型的服务中，比如微服务网关这样的应用中。
Reactive and non-blocking generally do not make applications run faster.

###优势

WebFlux从调用者(浏览器)的角度而言，是感知不到有什么变化的，因为都是得等待5s才返回数据。但是，从服务端的日志我们可以看出，WebFlux是直接返回Mono对象的(而不是像SpringMVC一直同步阻塞5s，线程才返回)。

>这正是WebFlux的好处：能够以固定的线程来处理高并发（充分发挥机器的性能）。

WebFlux还支持服务器推送(SSE - >Server Send Event)

