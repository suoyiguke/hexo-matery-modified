---
title: springboot-操作redis的list和set、zset类型(二).md
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
title: springboot-操作redis的list和set、zset类型(二).md
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

好极了，方法是真的多
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8a63d7ca67cc3fe3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


~~~
package com.springboot.study.demo1;

import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.*;
import org.springframework.test.context.junit4.SpringRunner;

import java.time.Duration;
import java.util.*;
import java.util.concurrent.TimeUnit;

/**
 *@description: Test1
 *@author: yinkai
 *@create: 2020/3/7 21:15
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class Test {
    @Autowired
    private ListOperations<String, Object> listOperations;
    @org.junit.Test
    public void set() {


        /**========================= 写 ==========================**/

        //1、 从左边插入指定key的value，key存在则插入在最左边，如果key不存在则为list的第一个元素，返回当前list的长度
        System.out.println(listOperations.leftPush("leftPush","value1"));//1
        System.out.println(listOperations.leftPush("leftPush","value2"));//2
        System.out.println(listOperations.leftPush("leftPush","value4"));//3
        //第二个参数指的是在指定value2后面插入
        System.out.println(listOperations.leftPush("leftPush","value2","value3"));//4

        //2、批量插入指定key的value列表到list左边,返回插入后list的长度
        //可变参数类型
        System.out.println(listOperations.leftPushAll("leftPushAll","value1","value2","value3"));
        //集合类型
        System.out.println(listOperations.leftPushAll("leftPushAll",Arrays.asList(new String[]{"value4","value5","value6"})));

        //3、如果key存在则将value插入至左边，返回list长度。不存在则忽略此次插入，返回0
        System.out.println(listOperations.leftPushIfPresent("leftPushAll","xxxxxx"));
        System.out.println(listOperations.leftPushIfPresent("leftPushIfPresent","xxxxxx"));

        //4、从右边插入指定key的value，key存在则插入在最右边，如果key不存在则为list的第一个元素，返回当前list的长度
        listOperations.rightPush("rightPush","value1");
        listOperations.rightPush("rightPush","value2");
        listOperations.rightPush("rightPush","value4");
        //第二个参数指的是在指定value2后面插入
        listOperations.rightPush("rightPush","value2","value3");

        //5、批量插入指定key的value列表到list右边,返回插入后list的长度
        listOperations.rightPushAll("rightPushAll","value1","value2","value3");
        listOperations.rightPushAll("rightPushAll",Arrays.asList(new String[]{"value4","value5","value6"}));

        //6、如果key存在则将value插入至右边，返回list长度。不存在则忽略此次插入，返回0
        //存在，返回索引
        System.out.println(listOperations.rightPushIfPresent("rightPushAll", "xxx"));
        //不存在，返回0
        System.out.println(listOperations.rightPushIfPresent("rightPushIfPresent", "xxx"));


        listOperations.leftPushAll("set","value1","value2","value4");
        //7、替换list指定索引位置的元素,索引从0开始
        listOperations.set("set",2,"value3");
        System.out.println(listOperations.range("set",0,-1));


        listOperations.leftPushAll("remove","value1","value2","value2","value2","value3");
        System.out.println(listOperations.range("remove",0,-1));
        //8、
            //count> 0：删除count个从头到尾值为value2的元素
            //count <0：删除count个从尾到头值为value2的元素
            //count = 0：删除等于value的所有元素。
        listOperations.remove("remove",1,"value2");
        System.out.println(listOperations.range("remove",0,-1));


        listOperations.leftPushAll("trim","value1","value2","value3","value4","value5","value6");
        //9、只保留索引从1到3的元素，其他元素丢弃。索引从0开始
        listOperations.trim("trim",1,3);
        System.out.println(listOperations.range("trim",0,-1));




        /**========================= 读 ==========================**/


        //10、range 返回存储在键中的列表的指定元素，其中0是列表的第一个元素（列表的头部），-1代表所有元素
        List<Object> list = listOperations.range("range", 0, -1);
        System.out.println(list);


        listOperations.leftPushAll("test_index","value1","value2","value3","value4","value5");
        //11、index 获得索引为4的元素，索引从0开始
        System.out.println(listOperations.index("test_index",4));


        listOperations.leftPushAll("test_leftPop","value1","value2");
        //12、leftPop 弹出最左边的元素，并将此元素返回，弹出之后该值在列表中将不复存在
        System.out.println(listOperations.leftPop("test_leftPop"));
        System.out.println(listOperations.range("test_leftPop",0,-1));
        System.out.println(listOperations.leftPop("test_leftPop"));
        //弹出最左边的元素，并将此元素返回，若列表为空则阻塞直到等待超时或发现可弹出元素为止。超时则报出异常Caused by: io.lettuce.core.RedisCommandTimeoutException: Command timed out after 6 second(s)
        listOperations.leftPop("test_leftPop",10,TimeUnit.SECONDS);


        listOperations.rightPushAll("test_rightPop","value1","value2");
        //13、rightPop弹出最右边的元素，并将此元素返回，弹出之后该值在列表中将不复存在
        System.out.println(listOperations.rightPop("test_rightPop"));
        System.out.println(listOperations.range("test_rightPop",0,-1));
        System.out.println(listOperations.rightPop("test_rightPop"));
        //弹出最左边的元素，并将此元素返回，若列表为空则阻塞直到等待超时或发现可弹出元素为止。超时则报出异常Caused by: io.lettuce.core.RedisCommandTimeoutException: Command timed out after 6 second(s)
        listOperations.rightPop("test_rightPop",10,TimeUnit.SECONDS);


        listOperations.rightPushAll("test_rightPopAndLeftPush1","value1","value2");
        listOperations.rightPushAll("test_rightPopAndLeftPush2","value3","value4");
        //14、用于移除列表的最右边元素，并将该元素添加到另一个列表的最左边并返回该元素。
        System.out.println(listOperations.rightPopAndLeftPush("test_rightPopAndLeftPush1","test_rightPopAndLeftPush2"));
        System.out.println(listOperations.range("test_rightPopAndLeftPush1",0,-1));//[value1]
        System.out.println(listOperations.range("test_rightPopAndLeftPush2",0,-1));//[value2, value3, value4]

        //若列表为空则阻塞直到等待超时或发现可弹出元素
        listOperations.rightPushAll("test_rightPopAndLeftPush3","value1");
        listOperations.rightPushAll("test_rightPopAndLeftPush4","value2","value3");
        System.out.println(listOperations.rightPopAndLeftPush("test_rightPopAndLeftPush3","test_rightPopAndLeftPush4"));
        System.out.println(listOperations.rightPopAndLeftPush("test_rightPopAndLeftPush3","test_rightPopAndLeftPush4",10,TimeUnit.SECONDS));
        System.out.println(listOperations.range("test_rightPopAndLeftPush3",0,-1));//[value1]
        System.out.println(listOperations.range("test_rightPopAndLeftPush4",0,-1));//[value2, value3, value4]

        //15、size 返回list的大小
        System.out.println( listOperations.size("test_rightPopAndLeftPush3"));


    }
}
~~~
