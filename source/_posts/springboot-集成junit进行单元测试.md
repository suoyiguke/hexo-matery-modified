---
title: springboot-集成junit进行单元测试.md
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
title: springboot-集成junit进行单元测试.md
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
为接口编写单元测试是一个非常好的习惯，使用junit能够快速加载spring中指定模块，而不需要将工程整个启动

spiringboot中只需要引入spring-boot-starter-test依赖即可以集成junit4
因为有依赖传递
![image.png](https://upload-images.jianshu.io/upload_images/13965490-eddba4f18b3a9963.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


引入maven依赖
~~~
        <!--springboot的测试框架,里面有对junit4的依赖-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

~~~

######简单使用
这个例子实现了依赖注入，对userService.list()方法进行测试
>- 需要在类上添加@RunWith(SpringRunner.class)和@SpringBootTest注解
>- 在需要进行单元测试的方法上加上@Test即可
>- junit环境能够像正式环境一样，使用@Resource注解进行依赖注入
~~~
package com.springboot.study.demo1;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.service.UserService;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import javax.annotation.Resource;
import java.util.List;

/**
 *@program: springboot_study
 *@author: yinkai
 *@create: 2020-02-29 14:23
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class Test {
    @Resource
    UserService userService;

    @org.junit.Test
    public  void test(){
        List<User> list = userService.list();
        System.out.println(list);
    }
}

~~~

######单元测试对事务的影响
> 如果在使用了@Transactional注解，那么在单元测试中的事务默认回滚。需要在方法上添加 @Rollback(value=false) 才会提交事务。
> 在测试中，处于对数据库的保护考虑，请使用@Rollback(value=true) 显式的回滚

![image.png](https://upload-images.jianshu.io/upload_images/13965490-9d1cd4754c56b10d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
~~~
package com.springboot.study.demo1;

import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.service.UserService;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.util.List;

/**
 *@program: springboot_study
 *@author: yinkai
 *@create: 2020-02-29 14:23
 */
@RunWith(SpringRunner.class)
@SpringBootTest
@Transactional
public class Test {
    @Resource
    UserService userService;

    @Transactional
    @org.junit.Test
    public void test(){
        List<User> list = userService.list();
        for (User user : list) {
            //所有user的age字段加1
            user.setAge(user.getAge()+1);
        }
        //保存
        userService.saveOrUpdateBatch(list);
    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-277e46bb598c217b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1ede0c5b27bf3460.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在添加事务注解的情况下事务默认回滚！

使用@Rollback(value=false) 
~~~
@Rollback(value=false)
    @Transactional
    @org.junit.Test
    public void test(){
        List<User> list = userService.list();
        for (User user : list) {
            //所有user的age字段加1
            user.setAge(user.getAge()+1);
        }
        //保存
        userService.saveOrUpdateBatch(list);
    }
~~~
执行结果，事务提交！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8063c65f0e03791a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ef7b18a9b7c0e88c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###注意一个问题

在junit4中执行多线程代码，可能springboot会在主线程直接退出后直接将所有的线程强制退出，而且无任何报错信息。所以需要使用countDownLatch将主线程await()，避免因为主线程退出而整个程序退出！
