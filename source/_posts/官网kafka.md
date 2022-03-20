---
title: 官网kafka.md
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
title: 官网kafka.md
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
http://kafka.apache.org/documentation/#quickstart
2021 5 最新版本 2.8.0

###简单使用
~~~
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.1.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>lab-03-kafka-native</artifactId>

    <dependencies>
        <!-- 引入 Kafka 客户端依赖 -->
        <dependency>
            <groupId>org.apache.kafka</groupId>
            <artifactId>kafka-clients</artifactId>
            <version>2.3.1</version>
        </dependency>
    </dependencies>

</project>

~~~
~~~
package cn.iocoder.springboot.lab03.kafkademo;

import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class ConsumerMain {

    private static Consumer<String, String> createConsumer() {
        // 设置 Producer 的属性
        Properties properties = new Properties();
        properties.put("bootstrap.servers", "192.168.1.117:9092"); // 设置 Broker 的地址
        properties.put("group.id", "demo-consumer-group"); // 消费者分组
        properties.put("auto.offset.reset", "earliest"); // 设置消费者分组最初的消费进度为 earliest 。可参考博客 https://blog.csdn.net/lishuangzhe7047/article/details/74530417 理解
        properties.put("enable.auto.commit", true); // 是否自动提交消费进度
        properties.put("auto.commit.interval.ms", "1000"); // 自动提交消费进度频率
        properties.put("key.deserializer", StringDeserializer.class.getName()); // 消息的 key 的反序列化方式
        properties.put("value.deserializer", StringDeserializer.class.getName()); // 消息的 value 的反序列化方式

        // 创建 KafkaProducer 对象
        // 因为我们消息的 key 和 value 都使用 String 类型，所以创建的 Producer 是 <String, String> 的泛型。
        return new KafkaConsumer<>(properties);
    }

    public static void main(String[] args) {
        // 创建 KafkaConsumer 对象
        Consumer<String, String> consumer = createConsumer();

        // 订阅消息
        consumer.subscribe(Collections.singleton("TestTopic"));

        // 拉取消息
        while (true) {
            // 拉取消息。如果拉取不到消息，阻塞等待最多 10 秒，或者等待拉取到消息。
            ConsumerRecords records = consumer.poll(Duration.ofSeconds(10));
            // 遍历处理消息
            records.forEach(new java.util.function.Consumer<ConsumerRecord>() {

                @Override
                public void accept(ConsumerRecord record) {
                    System.out.println("key==> "+record.key() + ", value==> " + record.value());
                }

            });
        }
    }

}

~~~


~~~
package cn.iocoder.springboot.lab03.kafkademo;

import java.util.Scanner;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;

public class ProducerMain {

    private static Producer<String, String> createProducer() {
        // 设置 Producer 的属性
        Properties properties = new Properties();
        properties.put("bootstrap.servers", "192.168.1.117:9092"); // 设置 Broker 的地址
        properties.put("acks", "1"); // 0-不应答。1-leader 应答。all-所有 leader 和 follower 应答。
        properties.put("retries", 3); // 发送失败时，重试发送的次数
//        properties.put("batch.size", 16384);
//        properties.put("linger.ms", 1);
//        properties.put("client.id", "DemoProducer");
//        properties.put("buffer.memory", 33554432);
        properties.put("key.serializer", StringSerializer.class.getName()); // 消息的 key 的序列化方式
        properties.put("value.serializer", StringSerializer.class.getName()); // 消息的 value 的序列化方式

        // 创建 KafkaProducer 对象
        // 因为我们消息的 key 和 value 都使用 String 类型，所以创建的 Producer 是 <String, String> 的泛型。
        return new KafkaProducer<>(properties);
    }

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        Producer<String, String> producer = createProducer();

        while (true) {

            Scanner input = new Scanner(System.in);
            System.out.print("输入 key: ");
            String key = input.next();
            System.out.print("输入 value: ");
            String value = input.next();

            ProducerRecord<String, String> message = new ProducerRecord<>("TestTopic", key,
                value);

            // 同步发送消息
            Future<RecordMetadata> sendResultFuture = producer.send(message);
            RecordMetadata result = sendResultFuture.get();
            System.out.println(
                "message sent to " + result.topic() + ", partition " + result.partition()
                    + ", offset "
                    + result.offset());

            System.out.println("");
        }

    }

}

~~~



###springboot中

