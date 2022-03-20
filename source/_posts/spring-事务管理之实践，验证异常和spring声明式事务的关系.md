---
title: spring-事务管理之实践，验证异常和spring声明式事务的关系.md
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
title: spring-事务管理之实践，验证异常和spring声明式事务的关系.md
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
> 实践是检验真理的唯一标准！

######验证==>@Transactional只能回滚运行时异常，不能回滚受检异常。如果要回滚受检异常请使用@Transactional(rollbackFor=Exception.class)同时需要抛出异常

1、验证 ==> @Transactional只能回滚运行时异常
写个controller
~~~
package com.springboot.study.demo1.controller;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.service.UserService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import javax.annotation.Resource;
/**
 *@program: springboot_study
 *@description:
 *@author: yinkai
 *@create: 2020-03-01 13:00
 */
@RestController
@RequestMapping("/test")
public class TestController {

    @Resource
    private UserService userService;

    @RequestMapping("/test1")
    public void test(){
        userService.insertUser(new User(14L,"OK",10,"OK@QQ.COM",123));
    }

}
~~~

在UserServiceImpl中添加方法,上面添加@Transactional注解
在插入一条数据之后，出现除0异常（是一种运行时异常）
~~~
  @Transactional
    @Override
    public Boolean insertUser(User user){
        //插入user记录
        boolean save = save(user);
        //然后出现运行时异常
        int i = 1/0;
        return save;
    }

~~~

启动工程，访问http://localhost:8080/test/test/test1 程序报错后插入数据失败，数据回滚；

2、验证  ==> @Transactional不能回滚受检异常

将方法做如下修改，使用空字符串构造file对象，然后调用其createNewFile()方法。该方法会抛出IOException （是一种受检异常）
~~~
    @Transactional
    @Override
    public Boolean insertUser(User user){
         //插入user记录
        boolean save = save(user);
        //然后出现运行时异常
        File file = new File("");
        try {
            boolean newFile = file.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return save;
    }

~~~
启动工程，访问http://localhost:8080/test/test/test1 程序报错后插入数据成功，事务没有得到回滚。如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a0af2e940c0532bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


3、验证==> 如果要回滚受检异常请使用@Transactional(rollbackFor=Exception.class)同时需要抛出异常

在service的insertUser方法中对IOException 异常进行try/catch 同时`抛出异常`
~~~
  @Transactional(rollbackFor= Exception.class)
    @Override
    public Boolean insertUser(User user) throws IOException {
        //插入user记录
        boolean save = save(user);
        //然后出现运行时异常
        File file = new File("");
        try {
            boolean newFile = file.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
            //抛出异常
            throw e;
        }

        return save;
    }
~~~
回滚成功，表中没有新插入的记录

那如果不抛出呢？事务会回滚吗？
~~~
    @Transactional(rollbackFor= Exception.class)
    @Override
    public Boolean insertUser(User user) throws IOException {
        //插入user记录
        boolean save = save(user);
        //然后出现运行时异常
        File file = new File("");
        try {
            boolean newFile = file.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return save;
    }

~~~
果然，如果不抛出异常。只是service层内部消化掉。是没办法回滚的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c6e0b6b029b67e54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

若只抛出异常，不设置rollbackFor= Exception.class属性，那么事务遇到受检异常会得到回滚吗？
~~~
    @Transactional
    @Override
    public Boolean insertUser(User user) throws IOException {
        //插入user记录
        boolean save = save(user);
        //然后出现运行时异常
        File file = new File("");
        try {
            boolean newFile = file.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
            //抛出异常
            throw e;
        }
        return save;
    }

~~~
没有得到回滚~ 事实证明 抛出异常和设置rollbackFor= Exception.class两者缺一不可

> 所以这条结论是正确的~



######验证==>使用api的形式手动回滚
上面验证了@Transactional注解不加rollbackFor= Exception.class属性和不在方法内抛出受检异常则事务不会回滚；但是其实还有一种手动回滚的方式。如下
~~~
TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
~~~
~~~

    @Transactional
    @Override
    public Boolean insertUser(User user) {
        //插入user记录
        boolean save = save(user);
        //然后出现运行时异常
        File file = new File("");
        try {
            boolean newFile = file.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            //手动回滚
            TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
        }
        return save;
    }

~~~
> 事务回滚！手动回滚的方式可行~ 但是出于代码的优雅性。这种方式不予考虑使用


###### @Transactional不建议使用在接口上。如果切面使用cjlib实现的话则事务无效

先开个坑，等有时间再来验证

##### @Transactional申明的service实现类的方法必须要在对应service接口中有对应的抽象方法
一个serviceImpl 实现类方法就必须对应一个service接口的抽象方法
