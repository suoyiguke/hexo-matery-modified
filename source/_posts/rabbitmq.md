---
title: rabbitmq.md
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
title: rabbitmq.md
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


消费
~~~
package com.gbm.cloud.common.rabbitmq.group;

import com.gbm.cloud.common.rabbitmq.MqExchangeConst;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class TestReceiver {


    @RabbitListener(queues = MqExchangeConst.EXCHANGE_ORDER_PUSH)
    public void handleMessage(Message message){
        System.out.println("====消费消息===handleMessage(message)");
        System.out.println(message.getMessageProperties());
        System.out.println(new String(message.getBody()));
    }

}
~~~


生产
~~~
package com.gbm.cloud;


import com.alibaba.fastjson.JSONObject;
import com.gbm.cloud.common.rabbitmq.MqExchangeConst;
import com.gbm.cloud.treasure.entity.mgbUndertakesOrder.MbUndertakesOrderDto;
import com.taobao.api.ApiException;
import org.junit.jupiter.api.Test;
import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.RedisTemplate;

import java.text.ParseException;
import java.util.ArrayList;

@SpringBootTest
class MgbTreasureSystemApplicationTests {

    @Autowired
    private RedisTemplate redisTemplate;
    @Autowired
    private RabbitTemplate rabbitTemplate;
    @Autowired
    AmqpTemplate amqpTemplate;
    @Test
    public void test() throws ApiException, ParseException {
        ArrayList<MbUndertakesOrderDto> list = new ArrayList<>();
        MbUndertakesOrderDto mbUndertakesOrderDto = new MbUndertakesOrderDto();
        mbUndertakesOrderDto.setId(1L);
        list.add(mbUndertakesOrderDto);
        String s = JSONObject.toJSONString(list);
        System.out.println(s);
        while (true){
            rabbitTemplate.convertAndSend(MqExchangeConst.EXCHANGE_ORDER_PUSH,s);
        }



    }

}


~~~


###界面使用
http://192.168.1.54:15672/#/



1、查看多少个消费者

![image.png](https://upload-images.jianshu.io/upload_images/13965490-0d056605a6c9cdc6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/13965490-44dfc36301c9efc8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>发现自己发出4次消息才有一次被监听到。这是因为别人监听走了


2、手动发送消息
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8b504bad9cf4ef22.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
