---
title: RABBITMQ-问题---先启动生产者创建队列，再启动消费者.md
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
title: RABBITMQ-问题---先启动生产者创建队列，再启动消费者.md
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
Caused by: com.rabbitmq.client.ShutdownSignalException: channel error; protocol method: #method<channel.close>(reply-code=404, reply-text=NOT_FOUND - no queue 'handleMessage' in vhost '/', class-id=50, method-id=10)
再启动生产者时就把exchange 和 queue 自动创建好，不然消费者启动会报错

我们可以加个配置，这样在启动工程时就回去创建 `exchange 和 queue `
~~~
package com.gbm.cloud.common.rabbitmq;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitAdmin;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.annotation.PostConstruct;

@Configuration
public class ExchangeQueueBindingConfig {

    @Autowired
    RabbitAdmin rabbitAdmin;

    public static final String MY_QUEUE = "queue_1";
    public static final String MY_EXCHANGE = "exchange_1";

    @Bean
    public Queue createShiXinQueue() {
        return new Queue(MY_QUEUE, true);
    }

    @Bean
    public DirectExchange createShiXinExchange() {
        return new DirectExchange(MY_EXCHANGE, true, false);
    }

    @Bean
    public Binding createShiXinBinding() {
        return BindingBuilder.bind(createShiXinQueue()).to(createShiXinExchange()).with("shixin");
    }


    @Bean
    public RabbitAdmin rabbitAdmin(ConnectionFactory connectionFactory) {
        RabbitAdmin rabbitAdmin = new RabbitAdmin(connectionFactory);
        // 只有设置为 true，spring 才会加载 RabbitAdmin 这个类
        rabbitAdmin.setAutoStartup(true);
        return rabbitAdmin;
    }

    @PostConstruct
    public void createExchangeQueue() {
        rabbitAdmin.declareExchange(createShiXinExchange());
        rabbitAdmin.declareQueue(createShiXinQueue());
    }
}
~~~


###测试

消费者
~~~
    /**
     * 若存在多个消费者，则queue名必须唯一（若queue名相同则只有一个消费者能收到消息）
     * exchange需与生产者定义的exchange保持一致
     * routing key根据需要，若生产者发送多种消息，则可以使用*或#通配符
     */
    @RabbitHandler
    @RabbitListener(
            bindings = @QueueBinding(
                    value = @Queue(value = ExchangeQueueBindingConfig.MY_QUEUE, autoDelete = "true"),
                    exchange = @Exchange(value = ExchangeQueueBindingConfig.MY_EXCHANGE, type = ExchangeTypes.TOPIC)
            )
    )
    public void handleMessageA(Message message, Channel channel) {
        System.out.println(Thread.currentThread().getName());

        String s = new String(message.getBody());
        System.out.println(s);
    }

    @RabbitHandler
    @RabbitListener(
            bindings = @QueueBinding(
                    value = @Queue(value = ExchangeQueueBindingConfig.MY_QUEUE, autoDelete = "true"),
                    exchange = @Exchange(value = ExchangeQueueBindingConfig.MY_EXCHANGE, type = ExchangeTypes.TOPIC)
            )
    )
    public void handleMessageB(Message message, Channel channel) {
        System.out.println(Thread.currentThread().getName());

        String s = new String(message.getBody());
        System.out.println(s);
    }
~~~

生产者
~~~
 rabbitTemplate.send(ExchangeQueueBindingConfig.MY_EXCHANGE,"shixin", message1);
~~~
>注意routingKey也得匹配！











