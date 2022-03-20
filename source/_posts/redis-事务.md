---
title: redis-事务.md
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
title: redis-事务.md
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
http://www.redis.cn/topics/transactions.html

## 用法

[MULTI](http://www.redis.cn/commands/multi.html) 命令用于开启一个事务，它总是返回 `OK` 。 [MULTI](http://www.redis.cn/commands/multi.html) 执行之后， 客户端可以继续向服务器发送任意多条命令， 这些命令不会立即被执行， 而是被放到一个队列中， 当 [EXEC](http://www.redis.cn/commands/exec.html)命令被调用时， 所有队列中的命令才会被执行。

另一方面， 通过调用 [DISCARD](http://www.redis.cn/commands/discard.html) ， 客户端可以清空事务队列， 并放弃执行事务。

以下是一个事务例子， 它原子地增加了 `foo` 和 `bar` 两个键的值：

```
> MULTI
OK
> INCR foo
QUEUED
> INCR bar
QUEUED
> EXEC
1) (integer) 1
2) (integer) 1
```


## 放弃事务

当执行 [DISCARD](http://www.redis.cn/commands/discard.html) 命令时， 事务会被放弃， 事务队列会被清空， 并且客户端会从事务状态中退出：

```
> SET foo 1
OK
> MULTI
OK
> INCR foo
QUEUED
> DISCARD
OK
> GET foo
"1"
```


###java中
~~~

package com.imooc.ad.service;

import com.imooc.ad.Application;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.dao.DataAccessException;
import org.springframework.data.redis.core.RedisOperations;
import org.springframework.data.redis.core.SessionCallback;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.test.context.junit4.SpringRunner;

/**

Redis 事务测试
Created by Qinyi.
*/
@RunWith(SpringRunner.class)
@SpringBootTest(classes = {Application.class}, webEnvironment = SpringBootTest.WebEnvironment.NONE)
public class RedisTransTest {
/** 注入 StringRedisTemplate, 使用默认配置 /
@Autowired
private StringRedisTemplate stringRedisTemplate;
错误的用法
/*

没有开启事务支持: 事务执行会失败
*/
@Test
public void testMultiFailure() {
stringRedisTemplate.multi();
stringRedisTemplate.opsForValue().set(“name”, “qinyi”);
stringRedisTemplate.opsForValue().set(“gender”, “male”);
stringRedisTemplate.opsForValue().set(“age”, “19”);
System.out.println(stringRedisTemplate.exec());
}
~~~
执行以上测试用例，会抛出如下的异常信息：

Error in execution; nested exception is io.lettuce.core.RedisCommandExecutionException: ERR EXEC without MULTI
这里给出的错误信息显示：在执行 EXEC 命令之前，没有执行 MULTI 命令。这很奇怪，我们明明在测试方法的第一句就执行了 MULTI。通过追踪 multi、exec 等方法，我们可以看到如下的执行源码（spring-data-redis）：
~~~
public T execute(RedisCallback action, boolean exposeConnection, boolean pipeline) {
Assert.isTrue(initialized, “template not initialized; call afterPropertiesSet() before using it”);
Assert.notNull(action, “Callback object must not be null”);

RedisConnectionFactory factory = getRequiredConnectionFactory();
RedisConnection conn = null;
try {
// RedisTemplate 的 enableTransactionSupport 属性标识是否开启了事务支持，默认是 false
if (enableTransactionSupport) {
// only bind resources in case of potential transaction synchronization
conn = RedisConnectionUtils.bindConnection(factory, enableTransactionSupport);
} else {
conn = RedisConnectionUtils.getConnection(factory);
}

 boolean existingConnection = TransactionSynchronizationManager.hasResource(factory);
~~~
源码中已经给出了答案：由于 enableTransactionSupport 属性的默认值是 false，导致了每一个 RedisConnection 都是重新获取的。所以，我们刚刚执行的 MULTI 和 EXEC 这两个命令不在同一个 Connection 中。

###设置 enableTransactionSupport 开启事务支持

解决上述示例的问题，最简单的办法就是让 RedisTemplate 开启事务支持，即设置 enableTransactionSupport 为 true 就可以了。测试代码如下：
~~~

/**
 * <h2>开启事务支持: 成功执行事务</h2>
 * */
@Test
public void testMultiSuccess() {
  // 开启事务支持，在同一个 Connection 中执行命令
  stringRedisTemplate.setEnableTransactionSupport(true);

  stringRedisTemplate.multi();
  stringRedisTemplate.opsForValue().set("name", "qinyi");
  stringRedisTemplate.opsForValue().set("gender", "male");
  stringRedisTemplate.opsForValue().set("age", "19");
  System.out.println(stringRedisTemplate.exec());     // [true, true, true]
}
~~~







###SessionCallback
通过 SessionCallback，保证所有的操作都在同一个 Session 中完成
更常见的写法仍是采用 RedisTemplate 的默认配置，即不开启事务支持。但是，我们可以通过使用 SessionCallback，该接口保证其内部所有操作都是在同一个Session中。测试代码如下：


~~~
/**
 * &lt;h2&gt;使用 SessionCallback, 在同一个 Redis Connection 中执行事务: 成功执行事务&lt;/h2&gt;
 * */
@Test
@SuppressWarnings("all")
public void testSessionCallback() {

    SessionCallback;  callback = new SessionCallback Object() {
        @Override
        public Object execute(RedisOperations operations) throws DataAccessException {
            operations.multi();
            operations.opsForValue().set("name", "qinyi");
            operations.opsForValue().set("gender", "male");
            operations.opsForValue().set("age", "19");
            return operations.exec();
        }
    };

    // [true, true, true]
    System.out.println(stringRedisTemplate.execute(callback));
}

~~~
总结：我们在 SpringBoot 中操作 Redis 时，使用 RedisTemplate 的默认配置已经能够满足大部分的场景了。如果要执行事务操作，使用 SessionCallback 是比较好，也是比较常用的选择。


###问题
1、查询和修改放在一个事务。那么查询会返回null

所以，查询请不要放在一个事务中！

