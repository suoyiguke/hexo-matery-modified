---
title: spring-事务传播行为之本类中事务方法调用另一个事务方法导致的事务失效问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: spring-事务传播行为之本类中事务方法调用另一个事务方法导致的事务失效问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
> 生于忧患，死于安乐

在UsersServiceImpl中有两个事务方法
>- InsertUsers() 和InsertCuser() 都是被事务注解所申明的方法；且InsertUsers中调用了InsertCuser
>- InsertUsers使用REQUIRED行为传播
>- InsertCusers使用REQUIRES_NEW行为传播
~~~
package com.springboot.study.demo1.service.impl;

import com.springboot.study.demo1.entity.Cuser;
import com.springboot.study.demo1.entity.Users;
import com.springboot.study.demo1.service.CuserService;
import com.springboot.study.demo1.service.UsersService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionSynchronizationManager;

import java.util.List;
import java.util.Map;

/**
 * @program: springboot_study
 * @description:
 * @author: yinkai
 * @create: 2020-03-02 15:31
 */
@Service
public class UsersServiceImpl implements UsersService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Autowired
    private UsersService usersService;

    @Transactional(propagation = Propagation.REQUIRED)
    @Override
    public void InsertUsers() {

        jdbcTemplate.update("INSERT INTO users(id,name, age, email) VALUES (?, ?, ?, ?);", 111, "InsertUsers", 24, "InsertUsers@qq.com");
        //打印事务id
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());

        //调用本service中另一个方法
        usersService.InsertCuser();

    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    @Override
    public void InsertCuser() {

        jdbcTemplate.update("INSERT INTO users(id,name, age, email) VALUES (?, ?, ?, ?);", 112, "InsertUsers", 24, "InsertUsers@qq.com");
        //打印事务id
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());
    }
}
~~~

我们来看看执行日志，可以看到两者打印的事务id相同。使用的是同一个事务。这违背了REQUIRES_NEW传播行为的语义了！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-83c307be146af5cd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
######理论上此时两个方法分别会开启自己的事务才对呀？为什么InsertCuser方法没有开启事务？
如果理解了spring实现申明式事务的原理就都明白了。我们都知道spring底层是使用动态代理来实现事务切面的。所以就必须走代理对象调用方法才能使方法增强生效!
注意看代码中是如何调用InsertCuser方法的：`InsertCuser(cuser);`这就相当于同过this调用本类方法 `this.InsertCuser(cuser);`

此处的this指向目标对象而不是代理对象，因此调用this.InsertCuser()将不会执行InsertCuser事务切面，即不会执行事务增强，因此b方法的事务定义`@Transactional(propagation = Propagation.REQUIRES_NEW)`将不会实施，即结果是InsertCuser和InsertUsers方法的事务定义是一样的。

所以只要得到usersService的代理对象就行了~


######可以使用`自我注入`的方式解决这个问题

代码修改如下

在UsersService 类中再注入一个UsersService 实例，然后通过这个实例属性进行InsertCuser方法的调用。岂不美哉？

~~~
package com.springboot.study.demo1.service.impl;

import com.springboot.study.demo1.entity.Cuser;
import com.springboot.study.demo1.entity.Users;
import com.springboot.study.demo1.service.CuserService;
import com.springboot.study.demo1.service.UsersService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionSynchronizationManager;

import java.util.List;
import java.util.Map;

/**
 * @program: springboot_study
 * @description:
 * @author: yinkai
 * @create: 2020-03-02 15:31
 */
@Service
public class UsersServiceImpl implements UsersService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Autowired
    private UsersService usersService;

    @Transactional(propagation = Propagation.REQUIRED)
    @Override
    public void InsertUsers() {

        jdbcTemplate.update("INSERT INTO users(id,name, age, email) VALUES (?, ?, ?, ?);", 111, "InsertUsers", 24, "InsertUsers@qq.com");
        //打印事务id
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());

        //调用本service中另一个方法
        usersService.InsertCuser();

    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    @Override
    public void InsertCuser() {

        jdbcTemplate.update("INSERT INTO users(id,name, age, email) VALUES (?, ?, ?, ?);", 112, "InsertUsers", 24, "InsertUsers@qq.com");
        //打印事务id
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());
    }
}
~~~


执行如下，已经不是同一个事务了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-145476824671c189.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###还可以使用这种较为优雅的方式
~~~
 ((UsersService) AopContext.currentProxy())
~~~

加上注解
@EnableAspectJAutoProxy(exposeProxy = true)
