---
title: redis-中出现了其它多余字符.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
---
title: redis-中出现了其它多余字符.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5c2c9777eb8fbed5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

spring默认采用defaultSerializer = new JdkSerializationRedisSerializer();来对key，value进行序列化操作。请将new JdkSerializationRedisSerializer()换成new StringRedisSerializer()
~~~
        //设置键的序列化
        redisTemplate.setKeySerializer(new StringRedisSerializer());
        //设置值得序列化
        redisTemplate.setValueSerializer(new StringRedisSerializer());
~~~


注意，若之前使用的是JdkSerializationRedisSerializer生成了额外字符，后来又换成StringRedisSerializer。这样get读取时转json会出错，会带出多余字符然后转json。注意这一点，若不接受清空redis的情况那最好不要改。
