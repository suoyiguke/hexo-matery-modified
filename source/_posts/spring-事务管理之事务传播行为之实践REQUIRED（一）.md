---
title: spring-事务管理之事务传播行为之实践REQUIRED（一）.md
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
title: spring-事务管理之事务传播行为之实践REQUIRED（一）.md
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
> 纸上得来终觉浅，绝知此事要躬行

为了深入了解spring的事务传播行为，只是知道概念还是不行。需要自己亲自动手来实践下才能学到细节，而且网络上的一些结论也有被以讹传讹的。自己做的实验自己也就放心很多，我愿意做多数人不愿意做的事。

我们知道spring给我们提供7中传播属性，加上不使用事务注解的一种情况就是8种。按照A方法中调用B方法的最简模型。进行排列组合就是 8 * 8 = 64 种组合方式

######寻找可以感知事务传播的方法
如果需要验证事务的传播行为，就需要通过一定的手段来感知事务传播。我首先想到的是使用 异常回滚的方式，后来发现不可行。因为操作没有回滚其实存在多种情况，有许多不可控因素。如 申明了特定的传播行为导致没有创建事务导致的不回滚、注解使用错误导致不回滚等。。

然后在网上找到了打印当前事务名的方式 
~~~
System.out.println(TransactionSynchronizationManager.getCurrentTransactionName());
~~~  
后来发现只要是加了事务注解，它都会有返回值。其实有些传播行为如@Transactional(propagation=Propagation.SUPPORTS)根本没有创建事务，该方法也打印出了值。。。后来就使用mysql自带的查询语句来打印事务id才搞定，如
~~~
 List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps);
~~~
注意这种方式需要在对数据库发出sql语句之后才能打印出值，所以需要将之放到数据库操作之后；
这种方式经过我使用或发现仍然有问题，如果两个方法返回相同的事务id，那么如何判断该事务是谁创建的？事务是如何传播的？
打印当前事务名的那个方法刚好可以区分~所以将二者结合起来用最好互相弥补缺陷
~~~
 //打印事务名
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());
~~~


###实验准备
> 分别有UserService 和 CuserService 两个service，他们之内都有实现各自的insert方法。且在UserService 接口里有调用CuserService 的接口。我们通过在方法上加上@Transactional注解并指定特定的propagation属性，设置不同的事务传播行为。观察运行结果，验证结论~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f2d5c7b5d4f3b6a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


创建Users和Cuser实体类
~~~
package com.springboot.study.demo1.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 *@description: User 实体类
 *@author: yinkai
 *@create: 2020/2/25 9:21
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Accessors(chain = true)
public class Users {
    private Long id;
    private String name;
    private Integer age;
    private String email;
}

package com.springboot.study.demo1.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 *@description: Cuser 实体类
 *@author: yinkai
 *@create: 2020/2/25 9:21
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Accessors(chain = true)
public class Cuser {
    private Long id;
    private String name;
    private Integer age;
    private String email;
}
~~~
创建 CuserService 和UsersService接口
~~~
package com.springboot.study.demo1.service;
import com.springboot.study.demo1.entity.Cuser;
/**
 * @author ceshi
 * @Title:
 * @Package
 * @Description:
 * @date 2020/3/217:11
 */
public interface CuserService {

     void InsertCuser(Cuser cuser);
}


package com.springboot.study.demo1.service;
import com.springboot.study.demo1.entity.Cuser;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.entity.Users;

/**

/**
 *@program: springboot_study
 *@description:
 *@author: yinkai
 *@create: 2020-03-02 15:30
 */
public interface UsersService {
    void InsertUsers(Users users);


}
~~~
创建CuserServiceImpl和UsersServiceImpl实现类
>- 分别实现InsertUsers () 和 InsertCuser()方法 ; 一个功能为添加User，一个功能为添加Cuser
>- InsertUsers ()方法内部调用了InsertCuser()方法，制造事务冲突环境

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
 *@program: springboot_study
 *@description:
 *@author: yinkai
 *@create: 2020-03-02 15:31
 */
@Service
public class UsersServiceImpl implements UsersService {
    @Autowired
    private JdbcTemplate jdbcTemplate;
    @Autowired
    private CuserService cuserService;

    @Transactional(propagation= Propagation.NOT_SUPPORTED)
    @Override
    public void InsertUsers(Users users) {
        jdbcTemplate.update("INSERT INTO users(id,name, age, email) VALUES (?, ?, ?, ?);",users.getId(), users.getName(), users.getAge(), users.getEmail());
        //调用service中另一个方法
        Cuser cuser = new Cuser(users.getId(), users.getName(), users.getAge(), users.getEmail());
        //打印事务名
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());
        cuserService.InsertCuser(cuser);
    }
}

package com.springboot.study.demo1.service.impl;
import com.springboot.study.demo1.entity.Cuser;
import com.springboot.study.demo1.service.CuserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.support.TransactionSynchronizationManager;
import java.util.List;
import java.util.Map;
/**
 * @program: springboot_study
 * @description:
 * @author: yinkai
 * @create: 2020-03-02 17:12
 */
@Service
public class CuserServiceImpl implements CuserService {
    @Autowired
    private JdbcTemplate jdbcTemplate;
    @Override
    public void InsertCuser(Cuser cuser) {
        jdbcTemplate.update("INSERT INTO cuser(id,name, age, email) VALUES (?, ?, ?, ?);", cuser.getId(), cuser.getName(), cuser.getAge(), cuser.getEmail());
        //打印事务名
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());
    }
}
~~~
创建测试的controller


~~~
package com.springboot.study.demo1.controller;
import com.springboot.study.demo1.entity.Users;
import com.springboot.study.demo1.service.UsersService;
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
    private UsersService usersService;
    @RequestMapping("/test")
    public void test(){
        Users users = new Users(100L,"hello",22,"hello@qq.com");
        usersService.InsertUsers(users);
    }
}
~~~
项目启动后访问 http://localhost:8080/test/test/test即可根据控制台输出判断事务的传播

######首先讲的是spring的默认传播行为REQUIRED
@Transactional(propagation= Propagation.REQUIRED)
一种优先按照调用者事务来，如果调用者没事务则直接创建一个



###开始测试


######1、两种方法都不加事务
~~~
    @Override
    public void InsertUsers(Users users) 
      
    @Override
    public void InsertCuser(Cuser cuser) 
   
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ffe2f9c0e2043771.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这个是意料之中，不加事务注解当然不会开启事务
######2、InsertUser 加上required，InsertCuser 不加事务
~~~
    @Transactional(propagation= Propagation.REQUIRED)
    @Override
    public void InsertUsers(Users users) 
      
    @Override
    public void InsertCuser(Cuser cuser) 
   
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-835dc0ece9c4998d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

InsertUser 将事务传播给InsertCuser ，两者使用InsertUser 上的同一事务；想象一下，调用关系 A-->B-->C--->D-->.... 若只有A上加了required事务注解，那么BCD...都会纳入A的事务中

######3、InsertUser不加事务，InsertCuser 加上 required
~~~
    @Override
    public void InsertUsers(Users users) 

    @Transactional(propagation= Propagation.REQUIRED)
    @Override
    public void InsertCuser(Cuser cuser) 
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0097fca93b68ed9f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

InsertUser没有使用事务，InsertCuser 使用自己的事务

######4、InsertUser 和 InsertCuser  都加上 required
~~~
   @Transactional(propagation= Propagation.REQUIRED)
   @Override
    public void InsertUsers(Users users) 

    @Transactional(propagation= Propagation.REQUIRED)
    @Override
    public void InsertCuser(Cuser cuser) 
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8de0de03d2196ac2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


InsertUser 将事务传播给InsertCuser ，两者使用InsertUser 上的同一事务；


######5、InsertUser 使用 required，InsertCuser 使用 supports
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5424d2ee2975843d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

InsertUser 将事务传播给InsertCuser ，两者使用InsertUser 上的同一事务；

######6、InsertUser 使用 supports ，InsertCuser 使用 required
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1b2db13c45da2377.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

InsertUser 没有创建事务，InsertCuser 使用自己的事务


######7、InsertUser 使用required，InsertCuser 使用 requires_new
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a032ee4807ca2c99.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

InsertUser和 InsertCuser  各自创建了事务，互不影响

######8、InsertUser 使用requires_new，InsertCuser 使用required
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c71ec564d32a5aec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


InsertUser 将事务传播给InsertCuser ，两者使用InsertUser 上的同一事务；



######9、InsertUser 使用 required，InsertCuser 使用 mandatory 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d66f49665f5cb810.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

InsertUser 将事务传播给InsertCuser ，两者使用InsertUser 上的同一事务；


######10、InsertUser 使用 mandatory ，InsertCuser 使用 requires

报异常
>org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'



######11、InsertUser 使用 requires，InsertCuser 使用 not_supported
![image.png](https://upload-images.jianshu.io/upload_images/13965490-211547b7ebb6158d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

InsertUser事务先被挂起，等到InsertCuser 非事务执行完毕后再继续执行

######12、InsertUser 使用not_supported ，InsertCuser 使用 requires
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cc91fb2080add60d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

InsertUser 不会创建事务，InsertCuser 使用自己的事务

######13、InsertUser 使用 requires，InsertCuser 使用 never
报异常
> org.springframework.transaction.IllegalTransactionStateException: Existing transaction found for transaction marked with propagation 'never'

######14、InsertUser 使用 never，InsertCuser 使用  requires 

![image.png](https://upload-images.jianshu.io/upload_images/13965490-37237d84f62b771a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 不使用事务，InsertCuser 使用自己的事务

######15、InsertUser 使用 requires，InsertCuser 使用  nested
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7108566f02dc54e9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 将事务传播给InsertCuser ，两者使用InsertUser 上的同一事务
######16、InsertUser 使用 nested，InsertCuser 使用  requires
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b8adf26c043adabe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
InsertUser 将事务传播给InsertCuser ，两者使用InsertUser 上的同一事务

###大总结

实验|InsertUser `调用者 `|InsertCuser `被调用者`|结果|
 -----------| ----------- | ----------- | ------------ |
1|不加 |不加| 两者都以无事务状态执行 |
2|required |不加| InsertUser 将它的事务传播给了InsertCuser |
3|不加|required |InsertUser 无事务，InsertCuser 创建了事务 |
4|required|required|InsertUser 将事务传播给了InsertCuser  |
5|requires|supports| InsertUser 把事务传播给了InsertCuser |
6|supports|requires| InsertUser无事务，InsertCuser 创建了事务 |
7|requires|mandatory| InsertUser将事务传播给了InsertCuser  |
8|mandatory|requires| InsertUser报异常IllegalTransactionStateException  |
9|requires_new|required| InsertUser 把事务传播给了InsertCuser |
10|required|requires_new|两者使用各自的事务，互不影响 |
11|requires|not_supported| InsertUser事务先被挂起，等到InsertCuser 非事务执行完毕后再继续执行|
12|not_supported|requires|InsertUser 不会创建事务，InsertCuser 使用自己的事务|
13|requires|nerver|InsertCuser 报异常IllegalTransactionStateException|
14|nerver|requires|InsertUser 无事务，InsertCuser 创建了事务|
15|requires|nested|InsertUser 把事务传播给了InsertCuser|
16|nested|requires|InsertUser 把事务传播给了InsertCuser|


第二篇：
https://www.jianshu.com/p/a03ee8451775
