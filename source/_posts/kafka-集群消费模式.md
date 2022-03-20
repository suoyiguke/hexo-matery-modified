---
title: kafka-集群消费模式.md
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
title: kafka-集群消费模式.md
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
符合集群消费的机制：集群消费模式下，相同 Consumer Group 的每个 Consumer 实例平均分摊消息。。



也就是说，如果我们发送一条 Topic 为 "DEMO_01" 的消息，可以分别被 "demo01-A-consumer-group-DEMO_01" 和 "demo01-consumer-group-DEMO_01" 都消费一次。

但是，如果我们启动两个该示例的实例，则消费者分组 "demo01-A-consumer-group-DEMO_01" 和 "demo01-consumer-group-DEMO_01" 都会有多个 Consumer 示例。此时，我们再发送一条 Topic 为 "DEMO_01" 的消息，只会被 "demo01-A-consumer-group-DEMO_01" 的一个 Consumer 消费一次，也同样只会被 "demo01-A-consumer-group-DEMO_01" 的一个 Consumer 消费一次。

好好理解上述的两段话，非常重要。
>同一消费者组中的所有不同topic的消费者都会去消费一次。
若还有多个相同的topic实例的话，也有其中一个topic会进行消费。

通过集群消费的机制，我们可以实现针对`相同 Topic ，不同消费者分组`实现各自的业务逻辑。例如说：用户注册成功时，发送一条 Topic 为 "USER_REGISTER" 的消息。然后，不同模块使用不同的消费者分组，订阅该 Topic ，实现各自的拓展逻辑：

积分模块：判断如果是手机注册，给用户增加 20 积分。
优惠劵模块：因为是新用户，所以发放新用户专享优惠劵。
站内信模块：因为是新用户，所以发送新用户的欢迎语的站内信。
... 等等


在代码上体现就是：
~~~
@KafkaListener(topics = "topics", groupId = "groupId")
~~~
1、topics 相同，groupId id不同就是 `相同 Topic ，不同消费者分组`。都会去消费
2、topics 和 groupId 都相同就是属于“只会有其中一个消费者实例消费的到”


还有个特性：
新groupId 消费者会将属于当前topic下所有历史消息都消费！

###举个例子
~~~
    <dependency>
            <groupId>org.springframework.kafka</groupId>
            <artifactId>spring-kafka</artifactId>
            <version>2.3.3.RELEASE</version>
        </dependency>
~~~

~~~
# Spring配置
spring:
  # Kafka 配置项，对应 KafkaProperties 配置类
  kafka:
    bootstrap-servers: 192.168.1.117:9092 # 指定 Kafka Broker 地址，可以设置多个，以逗号分隔
    # Kafka Producer 配置项
    producer:
      acks: 1 # 0-不应答。1-leader 应答。all-所有 leader 和 follower 应答。
      retries: 3 # 发送失败时，重试发送的次数
      key-serializer: org.apache.kafka.common.serialization.StringSerializer # 消息的 key 的序列化
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer # 消息的 value 的序列化
    # Kafka Consumer 配置项
    consumer:
      auto-offset-reset: earliest # 设置消费者分组最初的消费进度为 earliest 。可参考博客 https://blog.csdn.net/lishuangzhe7047/article/details/74530417 理解
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      properties:
        spring:
          json:
            trusted:
              packages: com.ruoyi.web.kafka

~~~


消费者
~~~
package com.ruoyi.web.kafka;

// Demo01AConsumer.java

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class Demo01AConsumer {

    private Logger logger = LoggerFactory.getLogger(getClass());

    //A和B其中之一会去消费
    @KafkaListener(topics = Demo01Message.TOPIC,
        groupId = "demo01-A-consumer-group-" + Demo01Message.TOPIC)
    public void onMessageA(ConsumerRecord<Integer, String> record) {
        logger.info("[onMessage][线程编号:{} 消息内容：{}]", Thread.currentThread().getId(), record);
    }

    //A和B其中之一会去消费
    @KafkaListener(topics = Demo01Message.TOPIC,
        groupId = "demo01-A-consumer-group-" + Demo01Message.TOPIC)
    public void onMessageB(ConsumerRecord<Integer, String> record) {
        logger.info("[onMessage][线程编号:{} 消息内容：{}]", Thread.currentThread().getId(), record);
    }

    //C一定会去消费
    @KafkaListener(topics = Demo01Message.TOPIC,
        groupId = "demo01-C-consumer-group-" + Demo01Message.TOPIC)
    public void onMessagC(ConsumerRecord<Integer, String> record) {
        logger.info("[onMessage][线程编号:{} 消息内容：{}]", Thread.currentThread().getId(), record);
    }

}
~~~

生产者
~~~
package com.ruoyi.web.kafka;

// Demo01Producer.java

import java.util.concurrent.ExecutionException;
import javax.annotation.Resource;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Component;
import org.springframework.util.concurrent.ListenableFuture;

@Component
public class Demo01Producer {

    @Resource
    private KafkaTemplate<Object, Object> kafkaTemplate;

    public SendResult syncSend(Integer id) throws ExecutionException, InterruptedException {
        // 创建 Demo01Message 消息
        Demo01Message message = new Demo01Message();
        message.setId(id);
        // 同步发送消息
        return kafkaTemplate.send(Demo01Message.TOPIC, message).get();
    }

    public ListenableFuture<SendResult<Object, Object>> asyncSend(Integer id) {
        // 创建 Demo01Message 消息
        Demo01Message message = new Demo01Message();
        message.setId(id);
        // 异步发送消息
        return kafkaTemplate.send(Demo01Message.TOPIC, message);
    }

}
~~~

消息类
~~~
package com.ruoyi.web.kafka;

// Demo01Message.java

import java.io.Serializable;

public class Demo01Message implements Serializable {

    public static final String TOPIC = "DEMO_01";

    /**
     * 编号
     */
    private Integer id;

    // ... 省略 set/get/toString 方法


    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}
~~~

测试类

~~~
package com.ruoyi.web.kafka;

import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.framework.web.domain.Server;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.support.SendResult;
import org.springframework.util.concurrent.ListenableFutureCallback;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RequestMapping("/kafka")
@RestController("testKafkaController")
public class KafkaController {

    private static final Logger logger = LoggerFactory.getLogger(KafkaController.class);

    public AjaxResult getInfo() throws Exception {
        Server server = new Server();
        server.copyTo();
        return AjaxResult.success(server);
    }


    @Autowired
    private Demo01Producer producer;

    @GetMapping("/testSyncSend")
    public void testSyncSend() throws ExecutionException, InterruptedException {
        int id = (int) (System.currentTimeMillis() / 1000);
        SendResult result = producer.syncSend(id);
        logger.info("[testSyncSend][发送编号：[{}] 发送结果：[{}]]", id, result);

        // 阻塞等待，保证消费
        new CountDownLatch(1).await();
    }

    @GetMapping("/testASyncSend")
    public void testASyncSend() throws InterruptedException {
        int id = (int) (System.currentTimeMillis() / 1000);
        producer.asyncSend(id)
            .addCallback(new ListenableFutureCallback<SendResult<Object, Object>>() {

                @Override
                public void onFailure(Throwable e) {
                    logger.info("[testASyncSend][发送编号：[{}] 发送异常]]", id, e);
                }

                @Override
                public void onSuccess(SendResult<Object, Object> result) {
                    logger.info("[testASyncSend][发送编号：[{}] 发送成功，结果为：[{}]]", id, result);
                }

            });

        // 阻塞等待，保证消费
        new CountDownLatch(1).await();
    }


}

~~~
