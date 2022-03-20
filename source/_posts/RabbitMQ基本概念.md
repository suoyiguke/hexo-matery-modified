---
title: RabbitMQ基本概念.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mq
categories: mq
---
---
title: RabbitMQ基本概念.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mq
categories: mq
---
exchange 唯一，queue 唯一


###Queue
消息队列，用来保存消息直到发送给消费者。它是消息的容器，也是消息的终点。一个消息可投入一个或多个队列。消息一直在队列里面，等待消费者连接到这个队列将其取走。

###Exchange
交换器，用来接收生产者发送的消息并将这些消息路由给服务器中的队列。

###routingKey
将Queue和Exchange 绑定需要设置 routingKey /binding key 

###Binding
绑定，用于消息队列Queue和交换器Exchange 之间的关联。一个绑定就是基于路由键将交换器和消息队列连接起来的路由规则，所以可以将交换器理解成一个由绑定构成的路由表。

- 当一个队列被绑定为binding key为”#”时，它将会接收所有的消息，这类似于广播形式的交换机模式。
- 当binding key不包含”*”和”#”时，类似于Direct Exchange直连交换机模式。

>BindingBuilder.bind(createShiXinQueue()).to(createShiXinExchange()).with("routingKey/bindingKey");


###Publisher
消息的生产者，也是一个向交换器发布消息的客户端应用程序。

###Consumer
消息的消费者，表示一个从消息队列中取得消息的客户端应用程序。


###Connection
网络连接，比如一个TCP连接。

###Channel
信道，多路复用连接中的一条独立的双向数据流通道。信道是建立在真实的TCP连接内地虚拟连接，AMQP 命令都是通过信道发出去的，不管是发布消息、订阅队列还是接收消息，这些动作都是通过信道完成。因为对于操作系统来说建立和销毁 TCP 都是非常昂贵的开销，所以引入了信道的概念，**以复用一条 TCP 连接**。



###Virtual Host
虚拟主机，表示一批交换器、消息队列和相关对象。虚拟主机是共享相同的身份认证和加密环境的独立服务器域。每个 vhost 本质上就是一个 mini 版的 RabbitMQ 服务器，拥有自己的队列、交换器、绑定和权限机制。vhost 是 AMQP 概念的基础，必须在连接时指定，RabbitMQ 默认的 vhost 是 / 。

###Broker
表示消息队列服务器实体。

###Message
消息，消息是不具名的，它由消息头和消息体组成。消息体是不透明的，而消息头则由一系列的可选属性组成，这些属性包括routing-key（路由键）、priority（相对于其他消息的优先权）、delivery-mode（指出该消息可能需要持久性存储）等。


###Exchange 类型
Exchange分发消息时根据类型的不同分发策略有区别，目前共四种类型：direct、fanout、topic、headers 。下面只讲前三种模式。

1、Direct Exchange 

直连型交换机，根据消息携带的路由键将消息投递给对应队列。
消息中的路由键（routing key）如果和 Binding 中的 binding key 一致， 交换器就将消息发到对应的队列中。路由键与队列名完全匹配

> 发消息 rabbitTemplate.send(ExchangeQueueBindingConfig.MY_EXCHANGE,`"bindingKey"`, message1);
> Binding BindingBuilder.bind(createShiXinQueue()).to(createShiXinExchange()).with(`"routingKey"`);


2、Fanout Exchange

扇型交换机，这个交换机没有路由键概念，就算你绑了路由键也是无视的。 这个交换机在接收到消息后，会直接转发到绑定到它上面的所有队列。


3、Topic Exchange

主题交换机，这个交换机其实跟直连交换机流程差不多，但是它的特点就是在它的路由键和绑定键之间是有规则的。
简单地介绍下规则：

>\*  (星号) 用来表示一个单词 (必须出现的)
\#  (井号) 用来表示任意数量（零个或多个）单词


通配的绑定键是跟队列进行绑定的，举个小例子
队列Q1 绑定键为 *.TT.*          队列Q2绑定键为  TT.#
如果一条消息携带的路由键为 A.TT.B，那么队列Q1将会收到；
如果一条消息携带的路由键为TT.AA.BB，那么队列Q2将会收到；

**主题交换机是非常强大的**，为啥这么膨胀？
- 当一个队列的绑定键为 "#"（井号） 的时候，这个队列将会无视消息的路由键，接收所有的消息。此时主题交换机就拥有的扇形交换机行为。
~~~
    @Bean
    public Binding createShiXinBinding() {
        return BindingBuilder.bind(createShiXinQueue()).to(createShiXinExchange()).with("#");
    }
~~~
- 当 * (星号) 和 # (井号) 这两个特殊字符都未在绑定键中出现的时候，此时主题交换机就拥有的直连交换机的行为。
~~~
    @Bean
    public Binding createShiXinBinding() {
        return BindingBuilder.bind(createShiXinQueue()).to(createShiXinExchange()).with("code");
    }
~~~
>所以主题交换机也就实现了扇形交换机的功能，和直连交换机的功能。

4、另外还有 Header Exchange 头交换机 

5、Default Exchange 默认交换机

6、Dead Letter Exchange 死信交换机





###拓展：ExchangeTypes 类里定义了这5种消息模式
~~~
/*
 * Copyright 2002-2019 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.springframework.amqp.core;

/**
 * Constants for the standard Exchange type names.
 *
 * @author Mark Fisher
 * @author Gary Russell
 */
public abstract class ExchangeTypes {
	/**
	 * Direct exchange.
	 */
	public static final String DIRECT = "direct";
	/**
	 * Topic exchange.
	 */
	public static final String TOPIC = "topic";
	/**
	 * Fanout exchange.
	 */
	public static final String FANOUT = "fanout";
	/**
	 * Headers exchange.
	 */
	public static final String HEADERS = "headers";
	/**
	 * System exchange.
	 */
	public static final String SYSTEM = "system";
}
~~~
