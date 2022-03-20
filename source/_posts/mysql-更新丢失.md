---
title: mysql-更新丢失.md
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
title: mysql-更新丢失.md
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
###更新丢失经典场景：
财务系统加工资，若公司本次调薪决定给员工张三加1k人民币，财务部两名操作人员A和B，过程情况若是这样的：
1）A操作员在应用系统的页面上查询出张三的薪水信息，然后选择薪水记录进行修改，打开修改页面但A突然有事离开了，页面放在那没有做任何的提交。
2）这时候B操作员同样在应用中查询出张三的薪水信息，然后选择薪水记录进行修改，录入增加薪水额1000，然后提交了。
3）这时候A操作员回来了，在自己之前打开的薪水修改页面上也录入了增加薪水额1000，然后提交了。
其实上面例子操作员A和B只要一前一后做提交，悲剧就出来了。后台修改薪水的sql：update 工资表 setsalary = salary + 增加薪水额 where staff_id = ‘员工ID’。这个过程走下来后结果是：张三开心了这次涨了2k，操作员A和B都郁闷了。



###解决方式

~~~
package com.gbm.cloud;

import com.taobao.api.ApiException;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.support.rowset.SqlRowSet;
import org.springframework.test.annotation.Rollback;
import org.springframework.transaction.TransactionDefinition;
import org.springframework.transaction.TransactionStatus;
import org.springframework.transaction.support.DefaultTransactionDefinition;

import java.text.ParseException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@SpringBootTest
@Rollback(value = false)
class MgbTreasureSystemApplicationTests {

    @Autowired
    JdbcTemplate jdbcTemplate;
    @Autowired
    private DataSourceTransactionManager dstManager;


    @Test
    public void test() throws ApiException, ParseException {

        CountDownLatch countDownLatch = new CountDownLatch(1);
        ExecutorService executorService = Executors.newFixedThreadPool(2);
        executorService.execute(new Runnable() {
            @Override
            public void run() {
                try {
                    countDownLatch.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                DefaultTransactionDefinition def = new DefaultTransactionDefinition();
                def.setPropagationBehavior(TransactionDefinition.PROPAGATION_REQUIRES_NEW);
                TransactionStatus transaction= dstManager.getTransaction(def); // 获得事务状态

                SqlRowSet sqlRowSet = jdbcTemplate.queryForRowSet("select version from test where id = 1");
                boolean next = sqlRowSet.next();
                int version = 0;
                if (next) {
                    version = sqlRowSet.getInt("version");
                }

                int update = jdbcTemplate.update("UPDATE `test` SET `num` = num+100 ,version=version+1  WHERE `id` = 1 and version = " + version);

                dstManager.commit(transaction);
                if(update==0){
                    System.out.println("a 修改失败");
                }
            }
        });


        executorService.execute(new Runnable() {
            @Override
            public void run() {
                try {
                    countDownLatch.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                DefaultTransactionDefinition def = new DefaultTransactionDefinition();
                def.setPropagationBehavior(TransactionDefinition.PROPAGATION_REQUIRES_NEW);
                TransactionStatus transaction= dstManager.getTransaction(def); // 获得事务状态
                SqlRowSet sqlRowSet = jdbcTemplate.queryForRowSet("select version from test where id = 1");
                boolean next = sqlRowSet.next();
                int version = 0;
                if (next) {
                    version = sqlRowSet.getInt("version");
                }

                int update = jdbcTemplate.update("UPDATE `test` SET `num` = num+100,version=version+1   WHERE `id` = 1 and version = " + version);
                dstManager.commit(transaction);

                if(update==0){
                    System.out.println("b 修改失败");
                }
            }
        });


        countDownLatch.countDown();

        try {
            Thread.sleep(1000 * 10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }

}


~~~

###减库存场景
反之库存被减为负数
~~~
package com.gbm.cloud;

import com.taobao.api.ApiException;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.Rollback;

import java.text.ParseException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@SpringBootTest
@Rollback(value = false)
class MgbTreasureSystemApplicationTests {

    @Autowired
    JdbcTemplate jdbcTemplate;


    @Test
    public void test() throws ApiException, ParseException {

        CountDownLatch countDownLatch = new CountDownLatch(1);
        ExecutorService executorService = Executors.newFixedThreadPool(100);
        for (int i = 0; i < 100; i++) {
            executorService.execute(new Runnable() {
                @Override
                public void run() {
                    try {
                        countDownLatch.await();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    int update = jdbcTemplate.update("UPDATE `test` SET `num` = num-1  WHERE `id` = 1 and num >= 1 ");
                    if(update==0){
                        System.out.println("a 修改失败");
                    }
                }
            });
        }

        countDownLatch.countDown();

        try {
            Thread.sleep(1000 * 10);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }

}


~~~

###分析
- 当多个事务并发更新同一个字段时可能会出现 更新丢失
- 看业务场景，是不是需要自旋直到修改成功。修改工资肯定需要直接失败
- 解决更新丢失的手段有乐观锁和悲观锁。


悲观锁
~~~
begin;
select * from emp where id = 1 for update;
update emp set name = 'zhang3' where id = 1;
commit;
~~~

乐观锁
>乐观锁 的工作原理：读取出数据时，将此版本号一同读出，之后更新时，对此版本号加一。此时，将提交数据的版本数据与数据库表对应记录的当前版本信息进行比对，如果提交的数据版本号大于数据库表当前版本号，则予以更新，否则认为是过期数据。需要重新查询再修改。

~~~
begin;
select * from emp where id = 1;
update emp set name = 'zhang3' where id = 1 and version = 1;
commit;

~~~


- 这样写update是不存在更新丢失的。因为sql本身就具备原子性，这种情况注意不要滥用乐观锁和悲观锁！
>UPDATE `test` SET `num` = `num` -1  WHERE `id` = 1；

~~~
    @Autowired
    JdbcTemplate jdbcTemplate;

    @Test
    public void test() throws ApiException, ParseException {
        ExecutorService executorService = Executors.newFixedThreadPool(1000);
        for (int i = 0; i < 1000; i++) {
            executorService.execute(new Runnable() {
                @Override
                public void run() {
                    jdbcTemplate.update("UPDATE `test` SET `num` = `num` -1  WHERE `id` = 1");
                }
            });
        }
    }
~~~










