---
title: junit5-断言.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: junit5-断言.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
~~~
package com.gbm.cloud;


import com.taobao.api.ApiException;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.RedisTemplate;

import java.text.ParseException;

@SpringBootTest
class MgbTreasureSystemApplicationTests {

    @Autowired
    private RedisTemplate redisTemplate;

    @Test
    public void test() throws ApiException, ParseException {
        //使用断言
        String s = "Hello Maven";
        Assert.assertEquals("Hell Maven", s);


    }
}


~~~
