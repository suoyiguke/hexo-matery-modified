---
title: rabbitmq--测试环境指定消费者.md
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
title: rabbitmq--测试环境指定消费者.md
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
~~~
package com.gbm.cloud.common.rabbitmq.group;

import com.gbm.cloud.common.rabbitmq.MqExchangeConst;
import com.rabbitmq.client.Channel;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitHandler;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.amqp.support.converter.SimpleMessageConverter;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.net.InetAddress;

@Slf4j
@Component
public class TestReceiver {

    @RabbitHandler
    @RabbitListener(queues = MqExchangeConst.EXCHANGE_ORDER_PUSH, ackMode = "MANUAL")
    public void handleMessage(Message message, Channel channel){

        long tag = message.getMessageProperties().getDeliveryTag();
        String appId = message.getMessageProperties().getAppId();
        log.info("{}-{}, 消息出队", tag, appId);
        String receiveMsg = "";
        try {
            //核对标识，决定是否消费消息
            String ip = InetAddress.getLocalHost().getHostAddress();
            if (!ip.equals(appId)) {
                log.info("这不是我需要的消息。放回队列。{}", receiveMsg);
                channel.basicReject(tag, true);
                return;
            }

            MessageConverter messageConverter = new SimpleMessageConverter();
            receiveMsg = String.valueOf(messageConverter.fromMessage(message));
            log.info("success " + receiveMsg);
            channel.basicAck(tag, false);

        } catch (Exception e) {
            log.error("receive message has an error, ", e);
            try {
                channel.basicNack(tag, false, true);
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }

}
~~~




~~~
package com.gbm.cloud;


import com.alibaba.fastjson.JSONObject;
import com.gbm.cloud.common.rabbitmq.MqExchangeConst;
import com.gbm.cloud.treasure.entity.mgbUndertakesOrder.MbUndertakesOrderDto;
import com.taobao.api.ApiException;
import org.junit.jupiter.api.Test;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageProperties;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.amqp.support.converter.SimpleMessageConverter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.RedisTemplate;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.text.ParseException;
import java.util.ArrayList;

@SpringBootTest
class MgbTreasureSystemApplicationTests {

    @Autowired
    private RedisTemplate redisTemplate;
    @Autowired
    private RabbitTemplate rabbitTemplate;
    @Test
    public void test() throws ApiException, ParseException {
        ArrayList<MbUndertakesOrderDto> list = new ArrayList<>();
        MbUndertakesOrderDto mbUndertakesOrderDto = new MbUndertakesOrderDto();
        mbUndertakesOrderDto.setId(1L);
        list.add(mbUndertakesOrderDto);
        String s = JSONObject.toJSONString(list);
        while (true){
            try {
                MessageProperties messageProperties = new MessageProperties();
                String ip = InetAddress.getLocalHost().getHostAddress();
                messageProperties.setAppId(ip);
                MessageConverter messageConverter = new SimpleMessageConverter();
                Message message1 = messageConverter.toMessage(s, messageProperties);
                rabbitTemplate.send(MqExchangeConst.EXCHANGE_ORDER_PUSH, message1);
                System.out.println("入队完成");
            } catch (UnknownHostException e) {
                e.printStackTrace();
            }

        }



    }

}


~~~
