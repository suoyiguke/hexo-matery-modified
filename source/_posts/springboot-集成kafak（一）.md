---
title: springboot-集成kafak（一）.md
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
title: springboot-集成kafak（一）.md
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
~~~
    <dependency>
      <groupId>org.springframework.kafka</groupId>
      <artifactId>spring-kafka</artifactId>
    </dependency>
~~~

配置

~~~
############################Kafka##################################################
kafka.bootstrap-servers=localhost:9092

kafka.topic.basic=test_topic
kafka.topic.json=json_topic
kafka.topic.batch=batch_topic
kafka.topic.manual=manual_topic

kafka.topic.transactional=transactional_topic
kafka.topic.reply=reply_topic
kafka.topic.reply.to=reply_to_topic
kafka.topic.filter=filter_topic
kafka.topic.error=error_topic

#############################################################################################

~~~


消费者配置
~~~
package org.szwj.ca.identityauthsrv.kafka;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.KafkaListenerContainerFactory;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import java.util.HashMap;
import java.util.Map;


@Configuration
@EnableKafka
public class BatchConsumerConfig {
    @Value("${kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Value("${kafka.topic.batch}")
    private String topic;

    /**
     * 多线程-批量消费
     * @return
     */
    @Bean
    public KafkaListenerContainerFactory<?> batchFactory(){
        ConcurrentKafkaListenerContainerFactory<String, String> factory =
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        // 控制多线程消费
        // 并发数(如果topic有3各分区。设置成3，并发数就是3个线程，加快消费)
        // 不设置setConcurrency就会变成单线程配置, MAX_POLL_RECORDS_CONFIG也会失效，
        // 接收的消息列表也不会是ConsumerRecord
        factory.setConcurrency(10);
        // poll超时时间
        factory.getContainerProperties().setPollTimeout(1500);
        // 控制批量消费
        // 设置为批量消费，每个批次数量在Kafka配置参数中设置（max.poll.records）
        factory.setBatchListener(true);
        return factory;
    }

    public ConsumerFactory<String, String> consumerFactory() {
        return new DefaultKafkaConsumerFactory<>(consumerConfigs());
    }

    /**
     * 消费者配置
     * @return
     */
    public Map<String, Object> consumerConfigs() {
        Map<String, Object> configProps = new HashMap<>();
        // 不用指定全部的broker，它将自动发现集群中的其余的borker, 最好指定多个，万一有服务器故障
        configProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        // key序列化方式
        configProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        // value序列化方式
        configProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        // GroupID
        configProps.put(ConsumerConfig.GROUP_ID_CONFIG, "test-group");
        // 批量消费消息数量  10000
        configProps.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 10000);

        // -----------------------------额外配置，可选--------------------------

        // 自动提交偏移量
        // 如果设置成true,偏移量由auto.commit.interval.ms控制自动提交的频率
        // 如果设置成false,不需要定时的提交offset，可以自己控制offset，当消息认为已消费过了，这个时候再去提交它们的偏移量。
        // 这个很有用的，当消费的消息结合了一些处理逻辑，这个消息就不应该认为是已经消费的，直到它完成了整个处理。
        configProps.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true");
        // 自动提交的频率
        configProps.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000");
        // Session超时设置
        configProps.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, "15000");

        // 该属性指定了消费者在读取一个没有偏移量的分区或者偏移量无效的情况下该作何处理：
        // latest（默认值）在偏移量无效的情况下，消费者将从最新的记录开始读取数据（在消费者启动之后生成的记录）
        // earliest ：在偏移量无效的情况下，消费者将从起始位置读取分区的记录
        configProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");


        return configProps;
    }
}


~~~

生产者配置
~~~
package org.szwj.ca.identityauthsrv.kafka;

import java.util.HashMap;
import java.util.Map;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;


@Configuration
public class BatchProducerConfig {
    @Value("${kafka.bootstrap-servers}")
    private String bootstrapServers;


    @Bean
    public KafkaTemplate<String, String> batchKafkaTemplate() {
        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

        // -----------------------------额外配置，可选--------------------------
        // 重试，0为不启用重试机制
        configProps.put(ProducerConfig.RETRIES_CONFIG, 0);
        // 控制批处理大小，单位为字节。(批量发送)
        // 当批次被填满时，批次里的所有消息被发送出去，不过生产者不一定都会等到批次被填满才发送，半满的或者
        // 一个消息的批次也可能被发送。
        configProps.put(ProducerConfig.BATCH_SIZE_CONFIG, 16384);
        // 批量发送，延迟为1毫秒，启用该功能能有效减少生产者发送消息次数，从而提高并发量（批量发送）
        // 该参数指定了生产者在发送批次之前等待更多消息加入批次的时间。
        // 批次填满或者linger.ms达到上限时把批次发送出去。
        configProps.put(ProducerConfig.LINGER_MS_CONFIG, 1);
        // 生产者可以使用的总内存字节来缓冲等待发送到服务器的记录
        configProps.put(ProducerConfig.BUFFER_MEMORY_CONFIG, 1024000);

        return new KafkaTemplate<>(new DefaultKafkaProducerFactory<>(configProps));

    }

}

~~~



消息监听器
~~~
package org.szwj.ca.identityauthsrv.kafka;

import groovy.util.logging.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
import java.util.List;
import java.util.Optional;

@Component
public class BatchConsumer {

    private static final Logger log = LoggerFactory.getLogger(KafkaConsumer.class);

    /**
     * 批量消息
     *
     * @param records
     */
    @KafkaListener(topics = "${kafka.topic.batch}", containerFactory = "batchFactory")
    public void consumerBatch(List<ConsumerRecord<?, ?>> records) {
        log.info("接收到消息数量：{}", records.size());
        for (ConsumerRecord record : records) {
            Optional<?> kafkaMessage = Optional.ofNullable(record.value());
            log.info("Received: " + record);
            if (kafkaMessage.isPresent()) {
                Object message = record.value();
                String topic = record.topic();
                System.out.println("接收到消息：" + message);
            }
        }
    }

}
~~~

生产者工具
~~~
package org.szwj.ca.identityauthsrv.kafka;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;
import java.util.concurrent.ExecutionException;


@Component
public class BatchProducer {
    @Autowired
    @Qualifier("batchKafkaTemplate")
    private KafkaTemplate<String, String> kafkaTemplate;

    @Value("${kafka.topic.batch}")
    private String batchTopic;

    /**
     * 异步发送
     * @param message
     */
    public void send(String message) {
        kafkaTemplate.send(batchTopic, message);
    }

    /**
     *  同步发送，默认异步
     * @param message
     */
    public void sendSync(String message) {
        try {
            kafkaTemplate.send(batchTopic, message).get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
    }

}
~~~



单元测试
~~~
package org.szwj.ca.identityauthsrv;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.szwj.ca.identityauthsrv.kafka.BatchProducer;

@RunWith(SpringRunner.class)
@SpringBootTest
public class IdentityauthsrvApplicationTests {

	@Autowired
	private BatchProducer batchProducer;

	@Test
	public void batchProducer() {
		for (int i = 0; i < 5; i++) {
			batchProducer.send("Message【" + i + "】:哈哈哈，我是批处理消息");
		}

		try {
			Thread.sleep(1000 * 2);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
}

~~~
