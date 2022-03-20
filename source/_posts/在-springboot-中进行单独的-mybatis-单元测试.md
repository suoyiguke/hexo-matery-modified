---
title: 在-springboot-中进行单独的-mybatis-单元测试.md
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
title: 在-springboot-中进行单独的-mybatis-单元测试.md
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
###@SpringBootTest
~~~
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
    </dependency>
~~~
使用普通的@SpringBootTest进行单元测试时会将整个应用都启动，和正常启动工程没什么区别。非常耗时。
~~~
@RunWith(SpringRunner.class)
@SpringBootTest
~~~
如下，启动测试。将web层也启动了。事实上根本不需要启动这个。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bec2bc3cad19d085.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###@MybatisTest 

我们只需要启动dao就行了。在这里我们使用mybatis-spring-boot-starter-test这个依赖
~~~
    <dependency>
      <groupId>org.mybatis.spring.boot</groupId>
      <artifactId>mybatis-spring-boot-starter-test</artifactId>
      <version>1.3.2</version>
      <scope>test</scope>
    </dependency>
~~~

测试例子
~~~
package org.szwj.ca.identityauthsrv;


import java.util.List;
import org.junit.runner.RunWith;
import org.mybatis.spring.boot.test.autoconfigure.MybatisTest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.junit4.SpringRunner;
import org.szwj.ca.identityauthsrv.entity.dao.TlkSignedDataWithBLOBs;

//@SpringbootTest
@MybatisTest    //缓存mybatsitest注解
@RunWith(SpringJUnit4ClassRunner.class)
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)    //这个是启用自己配置的数据元，不加则采用虚拟数据源
@Rollback(false)    //这个是默认是回滚，不会commit入数据库，改成false 则commit
public class Test1 {

    @Autowired
    org.szwj.ca.identityauthsrv.dao.TlkSignedDataDao tlkSignedDataDao;

    @org.junit.Test
    public  void test(){
        List<TlkSignedDataWithBLOBs> select = tlkSignedDataDao.select();
        for (TlkSignedDataWithBLOBs s: select) {
            System.out.println(s);

        }
//
//        TlkSignedDataWithBLOBs tlkSignedDataWithBLOBs = tlkSignedDataDao.selectByPrimaryKey("70866692a60a11ea9988b025aa26adf7");
//        System.out.println(tlkSignedDataWithBLOBs);
    }



~~~

打印sql
~~~
logging.level.org.szwj.ca.identityauthsrv.dao: debug
~~~

###使用问题
1、java.lang.IllegalStateException: Unable to find a @SpringBootConfiguration, you need to use @ContextConfiguration or @SpringBootTest(classes=...) with your test
需要和springboot main方法放到同一级包下

2、Caused by: org.springframework.beans.BeanInstantiationException: Failed to instantiate [com.zaxxer.hikari.HikariDataSource]: Factory method 'dataSource' threw exception; nested exception is org.springframework.boot.autoconfigure.jdbc.DataSourceProperties$DataSourceBeanCreationException: Failed to determine a suitable driver class

若依工程引入这个真的有点难，推荐还是使用@SpringBootTest的方式

###注意事项

普通单数据源请配置如下：spring.datasource.url的形式；否则单元测试启动报错'url' attribute is not specified and no embedded datasource could be configured.
~~~
# 数据源配置
spring:
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    driverClassName: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.1.82:3306/iam-vue?useUnicode=true&characterEncoding=utf8&zeroDateTimeBehavior=convertToNull&useSSL=true&serverTimezone=GMT%2B8
    username: root
    password: Sgl20@14
    # 初始连接数
    initialSize: 5
    # 最小连接池数量
    minIdle: 10
    # 最大连接池数量
    maxActive: 20
    # 配置获取连接等待超时的时间
    maxWait: 60000
    # 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒
    timeBetweenEvictionRunsMillis: 60000
    # 配置一个连接在池中最小生存的时间，单位是毫秒
    minEvictableIdleTimeMillis: 300000
    # 配置一个连接在池中最大生存的时间，单位是毫秒
    maxEvictableIdleTimeMillis: 900000
    # 配置检测连接是否有效
    validationQuery: SELECT 1 FROM DUAL
    testWhileIdle: true
    testOnBorrow: false
    testOnReturn: false
    webStatFilter:
      enabled: true
    statViewServlet:
      enabled: true
      # 设置白名单，不填则允许所有访问
      allow:
      url-pattern: /druid/*
      # 控制台管理用户名和密码
      login-username:
      login-password:
    filter:
      stat:
        enabled: true
        # 慢SQL记录
        log-slow-sql: true
        slow-sql-millis: 1000
        merge-sql: true
      wall:
        config:
          multi-statement-allow: true

~~~


有多个数据源时才去配置这样，spring.datasource.druid.master.url；
~~~
# 数据源配置
spring:
    datasource:
        type: com.alibaba.druid.pool.DruidDataSource
        driverClassName: com.mysql.cj.jdbc.Driver
        druid:
            # 主库数据源
            master:
                url: jdbc:mysql://localhost:3306/eas-vue?useUnicode=true&characterEncoding=utf8&zeroDateTimeBehavior=convertToNull&useSSL=true&serverTimezone=GMT%2B8
                username: root
                password: Sgl20@14
            # 从库数据源
            slave:
                # 从数据源开关/默认关闭
                enabled: false
                url: 
                username: 
                password: 
~~~
