---
title: java持久化-使用P6Spy来监控sql.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: java持久化-使用P6Spy来监控sql.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
######P6Spy集成到springboot
引入依赖
~~~
        <dependency>
            <groupId>p6spy</groupId>
            <artifactId>p6spy</artifactId>
            <version>3.7.0</version>
        </dependency>
~~~

编辑配置application.yml
- driver-class-name: com.mysql.jdbc.Driver 换成driver-class-name: com.p6spy.engine.spy.P6SpyDriver
-  url: jdbc:mysql://localhost:3306/jdbcstudy?allowMultiQueries=true&useUnicode=true&characterEncoding=UTF-8&useSSL=false
换成
url: jdbc`:p6spy:`mysql://localhost:3306/jdbcstudy?allowMultiQueries=true&useUnicode=true&characterEncoding=UTF-8&useSSL=false

~~~
datasource:
        druid:
            type: com.alibaba.druid.pool.DruidDataSource
            driver-class-name: com.p6spy.engine.spy.P6SpyDriver
            url: jdbc:p6spy:mysql://localhost:3306/jdbcstudy?allowMultiQueries=true&useUnicode=true&characterEncoding=UTF-8&useSSL=false
~~~

创建P6Spy自定义输出类
~~~
package com.springboot.study.demo1.config;
import com.p6spy.engine.spy.appender.MessageFormattingStrategy;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

/**
 *@description: P6SpyLogger P6Spy的自定义输出类
 *@author: yinkai
 *@create: 2020/2/25 12:05
 */
@NoArgsConstructor
public class P6SpyLogger implements MessageFormattingStrategy {


    @Override
    public String formatMessage(int connectionId, String now, long elapsed, String category, String prepared, String sql) {
        return !"".equals(sql.trim()) ? "[ " + LocalDateTime.now() + " ] --- | 耗时 "
                + elapsed + "ms | " + category + " | 活跃的连接数 " + connectionId + "\n "
                + sql + ";" : "";
    }
}
~~~

编辑配置spy.properties，没有就在resources目录下创建一个
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1c7308ff00e94551.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
driverlist=com.mysql.jdbc.Driver
autoflush=true
dateformat=MM-dd-yy HH:mm:ss:SS
appender=com.p6spy.engine.spy.appender.StdoutLogger
logfile=spy.log
logMessageFormat=com.springboot.study.demo1.config.P6SpyLogger
~~~
注意

- logMessageFormat=com.springboot.study.demo1.config.P6SpyLogger参数的值即是上面创建的配置类的全限定名，表示通过该类进行输出sql
######运行结果
运行项目，发起一个请求
控制台打印了执行的sql和sql执行时间，有利于进行sql调优分析。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4d39fb6c40a2bbe8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

事实上我们使用的druid连接池自带了sql监控的功能
