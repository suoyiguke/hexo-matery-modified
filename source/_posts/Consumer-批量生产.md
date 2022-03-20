---
title: Consumer-批量生产.md
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
title: Consumer-批量生产.md
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
Kafka 提供的批量发送消息，它提供了一个 RecordAccumulator 消息收集器，将发送给相同 Topic 的相同 Partition 分区的消息们，“偷偷”收集在一起，当满足条件时候，一次性批量发送提交给 Kafka Broker 。

如下是三个条件，满足任一即会批量发送：  
【数量】batch-size ：超过收集的消息数量的最大条数。 
【空间】buffer-memory ：超过收集的消息占用的最大内存。 
【时间】linger.ms ：超过收集的时间的最大等待时长，单位：毫秒。 下面，我们来实现一个 Producer 批量发送消息的示例。



###配置

批量发送消息添加 额外三个参数，就是我们说的 Producer 批量发送的三个条件：
`spring.kafka.producer.batch-size`
`spring.kafka.producer.buffer-memory`
 `spring.kafka.producer.properties.linger.ms`

> 具体的数值配置多少，根据自己的应用来。这里，我们故意将 `linger.ms` 配置成了 30 秒，主要为了演示之用。

~~~
  kafka:
    # Kafka Producer 配置项
    producer:
      batch-size: 16384 # 每次批量发送消息的最大数量
        buffer-memory: 33554432 # 每次批量发送消息的最大内存
        properties:
          linger:
            ms: 30000 # 批处理延迟时间上限。这里配置为 30 * 1000 ms 过后，不管是否消息数量是否到达 batch-size 或者消息大小到达 buffer-memory 后，都直接发送一次请求。

~~~



**1、测试时间维度**
spring.kafka.producer.properties.linger.ms 设置为30秒
~~~

    /**
     * 批量生产
     */
    @org.junit.Test
    public void batchProducer() throws InterruptedException {

        for (int i = 1; i <= 9; i++) {

            Demo01Message message = new Demo01Message();
            int id = (int) (System.currentTimeMillis() / 1000);
            message.setId(id);
            int finalI = i;
            kafkaTemplate.send(Demo01Message.TOPIC, message).addCallback(
                new ListenableFutureCallback<SendResult<Object, Object>>() {
                    @Override
                    public void onFailure(Throwable e) {
                        logger.error("异步生产失败回调 {}", finalI);
                    }

                    @Override
                    public void onSuccess(SendResult<Object, Object> result) {
                        logger.error("异步生产成功回调 {}", finalI);
                    }
                });

            // 故意每条消息之间，隔离 10 秒
            Thread.sleep(10 * 1000L);

        }

        // 阻塞等待，保证消费
        new CountDownLatch(1).await();

    }

~~~

**2、测试 消息条数维度**
