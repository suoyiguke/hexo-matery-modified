---
title: springboot-redis使用之redis事务.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
---
title: springboot-redis使用之redis事务.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
> 保持自信

redis也是有它的事务支持的，我们来看看在springboot中如何使用redis的事务特性吧
###方法一
首先在redis的配置类中开启事务支持
> template.setEnableTransactionSupport(true);
~~~
 @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory){
        Jackson2JsonRedisSerializer<Object> jackson2JsonRedisSerializer = new Jackson2JsonRedisSerializer<Object>(Object.class);
        ObjectMapper om = new ObjectMapper();
        om.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        om.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL);
        jackson2JsonRedisSerializer.setObjectMapper(om);
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(redisConnectionFactory);
        template.setKeySerializer(jackson2JsonRedisSerializer);
        template.setValueSerializer(jackson2JsonRedisSerializer);
        template.setHashKeySerializer(jackson2JsonRedisSerializer);
        template.setHashValueSerializer(jackson2JsonRedisSerializer);
        template.afterPropertiesSet();

        //开启事务支持
        template.setEnableTransactionSupport(true);
        return template;
    }
~~~


验证如下
>- redisTemplate.multi(); 开启事务
>- redisTemplate.exec(); 提交事务
>-  redisTemplate.discard(); 回滚事务
~~~
package com.springboot.study.demo1;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.*;
import org.springframework.test.context.junit4.SpringRunner;
/**
 *@description: Test1
 *@author: yinkai
 *@create: 2020/3/7 21:15
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class Test {
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    @Autowired
    private ValueOperations<String, String> valueOperations;
    @org.junit.Test
    public void set() {
        //收集命令然后在 exec()时执行，不同于mysql这种关系型数据库
        try {
            //开启事务
            redisTemplate.multi();
            valueOperations.set("t1", "hello ");
            int i = 1 / 0;
            valueOperations.set("t2", "world ");
            //提交事务
            redisTemplate.exec();
        }catch (Exception e){
            //取消执行事务
            redisTemplate.discard();
        }
    }
}
~~~

执行后可以发现，因为出现除0异常。redis并没有插入数据。那redis事务的原理是什么呢？
只是把事务内所有的redis操作收集起来，在redisTemplate.exec(); 提交事务时一起执行而已，并不是像mysql这种关系型数据库一样把每条sql都执行了只是没有持久化
###方法二

这种形式我开始以为是异步执行的，就像 jQuery 的ajax请求一样。其实只是写法上的改变。redisTemplate.execute方法的返回值只是一个普通的List，并没有什么异步获取结果的功能。其实只是写法上和方法一不同而已，也没什么优势啊。不过使用这种方式就不需要在redis配置类中开启事务配置了
~~~
package com.springboot.study.demo1;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.dao.DataAccessException;
import org.springframework.data.redis.core.*;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.List;

/**
 *@description: Test1
 *@author: yinkai
 *@create: 2020/3/7 21:15
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class Test {
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    @Autowired
    private ValueOperations<String, String> valueOperations;
    @org.junit.Test
    public void set() {

        //execute a transaction
        List<Object> txResults = redisTemplate.execute(new SessionCallback<List<Object>>() {
            public List<Object> execute(RedisOperations operations) throws DataAccessException {
                operations.multi();
                valueOperations.set("t1", "hello ");
//                int i = 1 / 0;
                valueOperations.set("t2", "world ");

                return operations.exec();
            }
        });
        System.out.println("Number of items added to set: " + txResults.get(0));

    }
}
~~~

关于 redisTemplate.execute的返回值是个List，其实就是execute方法内的所有redis操作语句的返回值集合。上面发出了2条语句。那么这个list就有2个元素了
