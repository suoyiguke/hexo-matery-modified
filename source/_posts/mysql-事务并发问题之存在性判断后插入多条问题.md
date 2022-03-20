---
title: mysql-事务并发问题之存在性判断后插入多条问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: mysql-事务并发问题之存在性判断后插入多条问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
> 古之学者必有师。师者，所以传道受业解惑也。

一个简单的需求，先判断表中是否存在对应的记录。不存在则插入，存在则忽略。
如果使用先select查询是否存在，然后使用insert语句插入数据这种方式。在事务并发执行下会出现`插入多条`的事务并发问题。这个问题就像之前遇到的`更新丢失`的问题一样。关于更新丢失可以看看这篇文章 https://www.jianshu.com/p/bfd7c684412d

原理如下： 事务并发执行。A事务和B事务开始时都看到的是数据是不存在的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-802d35dccdcb8a9f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





接下来我们做个验证

######准备数据环境
~~~
CREATE TABLE `jdbcstudy`.`test`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `a` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `b` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `c` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `d` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
~~~

写个service接口
~~~
package com.springboot.study.demo1.service;

/**
 *@program: springboot_study
 *@description:
 *@author: yinkai
 *@create: 2020-03-05 09:45
 */
public interface TestService {

    void insertOrIgnore(String a,String b,String c,String d) ;
}
~~~

service实现类
>- 使用  @Transactional注解表示本方法需在一个事务中执行，隔离级别是RR，传播属性是 REQUIRED
>- insertOrIgnore方法先判断符合a,b,c,d字段的记录是不是存在，若不存在则插入，存在则忽略
>- 为了测试结果更明显。在判断之后，插入之前添加了睡眠3秒
~~~
package com.springboot.study.demo1.service.impl;

import com.springboot.study.demo1.service.TestService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

/**
 *@program: springboot_study
 *@description:
 *@author: yinkai
 *@create: 2020-03-05 09:46
 */
@Service
public class TestServiceImpl implements TestService {
    @Autowired
    JdbcTemplate jdbcTemplate;

    @Transactional(rollbackFor = Exception.class,isolation = Isolation.REPEATABLE_READ,propagation = Propagation.REQUIRED)
    @Override
    public void insertOrIgnore(String a,String b,String c,String d)  {
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("select count(1) isOne from test where a = ? and b = ? and c = ? and d = ? for update;",a,b,c,d);
        Long isOne = (Long) maps.get(0).get("isOne");

        //查询后睡三秒
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        //返回记录为0，插入
        if(0 == isOne){
            jdbcTemplate.update("INSERT INTO jdbcstudy.test(a, b, c, d) VALUES (?,?, ?, ?);",a,b,c,d);
        }


    }
}
~~~

写个测试类
>- 测试类里开了三个线程去执行testService.insertOrIgnore()方法
~~~
package com.springboot.study.demo1;

import com.springboot.study.demo1.service.TestService;
import lombok.SneakyThrows;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.junit4.SpringRunner;

/**
 *@program: springboot_study
 *@author: yinkai
 *@create: 2020-02-29 14:23
 */
@RunWith(SpringRunner.class)
@SpringBootTest
public class Test {

    @Autowired
    TestService testService;

    @Rollback(value = false)
    @org.junit.Test
    public void test() throws InterruptedException {
        System.out.println("123");

        Thread  thread = null;
        //开3个线程对应三个事务，并发插入。看看结果如何
        for (int i = 1; i <= 3; i++) {
             thread = new Thread(new Runnable() {
                @Override
                public void run() {
                    testService.insertOrIgnore("a1", "b1", "c1", "d1");
                }
            }, Integer.toString(i));

            thread.start();
        }
        thread.join();
    }

}

~~~
来看看执行结果，果然表中被插入了多条数据
![image.png](https://upload-images.jianshu.io/upload_images/13965490-345708adec4295d7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
既然问题出现了，那总得解决呀？

######解决方法1，使用悲观锁、排他锁、X锁
将insert代码修改如下，后面加个 for update
~~~
List<Map<String, Object>> maps = jdbcTemplate.queryForList("select count(1) isOne from test where a = ? and b = ? and c = ? and d = ? for update;",a,b,c,d);
~~~
然后需要添加一个联合索引 index_a_b_c_d(a,b,c,d)。因为mysql的innodb引擎的行锁实现是依赖索引的，如果不加索引则会锁住全表。若插入a=a2,b=b2,c=c2,d=d2 也会被阻塞，这个问题等下再讨论~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b0cf2bd824ebf51b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
完了再次执行程序，报出异常如下
>Exception in thread "3" Exception in thread "1" org.springframework.dao.DeadlockLoserDataAccessException: PreparedStatementCallback; SQL [INSERT INTO jdbcstudy.test(a, b, c, d) VALUES (?,?, ?, ?);]; Deadlock found when trying to get lock; try restarting transaction; nested exception is 
按照翻译理解就是事务发生`死锁`了,这个提示未免有些笼统。其实这里根本不是死锁问题呀，只是锁等到超时而已。因为只有一个事务持锁

不过程序的执行结果是ok的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3e4016bb680e3493.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######解决方法二，使用mysql自带关键字解决

>使用 IGNORE 关键字可以完美解决这个问题；注意也需要添加联合索引，且索引的类型必须是UNIQUE的，这是IGNORE 的特性

![image.png](https://upload-images.jianshu.io/upload_images/13965490-32a7613063b9b72a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

TestServiceImpl 代码可以改成这样，在insert语句上加上IGNORE 关键字
~~~
package com.springboot.study.demo1.service.impl;

import com.springboot.study.demo1.service.TestService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.concurrent.TimeUnit;

/**
 * @program: springboot_study
 * @description:
 * @author: yinkai
 * @create: 2020-03-05 09:46
 */
@Service
public class TestServiceImpl implements TestService {
    @Autowired
    JdbcTemplate jdbcTemplate;

    @Transactional(rollbackFor = Exception.class, isolation = Isolation.REPEATABLE_READ, propagation = Propagation.REQUIRED)
    @Override
    public void insertOrIgnore(String a, String b, String c, String d) {

        //查询后睡三秒
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        jdbcTemplate.update("INSERT  IGNORE  INTO jdbcstudy.test(a, b, c, d) VALUES (?,?, ?, ?);", a, b, c, d);

    }
}
~~~

执行后查看表数据，完全ok
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ccaa01b6fe2d692b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


