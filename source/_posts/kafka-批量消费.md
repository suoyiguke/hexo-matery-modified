---
title: kafka-批量消费.md
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
title: kafka-批量消费.md
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
在一些业务场景下，我们希望使用 Consumer 批量消费消息，提高消费速度。要注意，Consumer 的批量消费消息，和 Producer 的[「4\. 批量发送消息」](https://www.iocoder.cn/Spring-Boot/Kafka/#) 没有直接关联哈。

下面，我们来实现一个 Consumer 批量消费消息的示例。考虑到不污染[「4\. 批量发送消息」](https://www.iocoder.cn/Spring-Boot/Kafka/#) 的示例，我们在 [lab-03-kafka-demo-batch](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-03-kafka/lab-03-kafka-demo-batch) 项目的基础上，复制出一个 [lab-03-kafka-demo-batch-consume](https://github.com/YunaiV/SpringBoot-Labs/tree/master/lab-03-kafka/lab-03-kafka-demo-batch-consume) 项目。😈 酱紫，我们也能少写点代码，哈哈哈~

## 5.1 应用配置文件

增加了四个配置项

*   `spring.kafka.listener.type`
*   `spring.kafka.consumer.max-poll-records`
*   `spring.kafka.consumer.fetch-min-size`
*   `spring.kafka.consumer.fetch-max-wait`



~~~
    # Kafka Consumer 配置项
    consumer:
      auto-offset-reset: earliest # 设置消费者分组最初的消费进度为 earliest 。可参考博客 https://blog.csdn.net/lishuangzhe7047/article/details/74530417 理解
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      fetch-max-wait: 10000 # poll 一次拉取的阻塞的最大时长，单位：毫秒。这里指的是阻塞拉取需要满足至少 fetch-min-size 大小的消息
      fetch-min-size: 10 # poll 一次消息拉取的最小数据量，单位：字节
      max-poll-records: 100 # poll 一次消息拉取的最大数量
      properties:
        spring:
          json:
            trusted:
              packages: com.ruoyi.web.kafka
    # Kafka Consumer Listener 监听器配置
    listener:
      type: BATCH # 监听器类型，默认为 SINGLE ，只监听单条消息。这里我们配置 BATCH ，监听多条消息，批量消费
      missing-topics-fatal: false # 消费监听接口监听的主题不存在时，默认会报错。所以通过设置为 false ，解决报错

~~~



消费者，改成批量消费消息。代码如下：
~~~
@Component
public class Demo02Consumer {
    private Logger logger = LoggerFactory.getLogger(getClass());
    @KafkaListener(topics = Demo02Message.TOPIC,
            groupId = "demo02-consumer-group-" + Demo02Message.TOPIC)
    public void onMessage(List<Demo02Message> messages) {
        logger.info("[onMessage][线程编号:{} 消息数量：{}]", Thread.currentThread().getId(), messages.size());
    }
}

~~~
方法上的参数变成了 List 数组。

