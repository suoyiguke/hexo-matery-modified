---
title: spring-事务管理之只读事务@Transactional(readOnly-=-true).md
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
title: spring-事务管理之只读事务@Transactional(readOnly-=-true).md
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
我们可以使用 @Transactional(readOnly = true) 来设置只读事务

在将事务设置成只读后，当前只读事务就不能进行写的操作，否则报错。如下
> Cause: java.sql.SQLException: Connection is read-only. Queries leading to data modification are not allowed; 

###需不需要在只有查询的方法上加上@Transactional注解？

需要分为两种情况来看
- 若一个事务里只发出一条select语句，则没有必要启用事务支持，数据库默认支持sql执行期间的读一致性。此时可以不加@Transactional注解

- 若一个事务里先后发出了多条select语句。 @Transactional注解表明被申明方法是一个整体事务。在mysql的RR隔离级别下，普通的无锁select是镜像读，多次查询结果不会改变，所以能保证`读一致性`（可重复读）;相反若不加 @Transactional注解，`则多条select都是独立的事务`在前条select之后，后条select之前，数据被其他事务改变，则该次整体的查询将会出现读数据不一致的现象。此时需要添加@Transactional注解



###需不需要在只有查询的方法上使用@Transactional(readOnly = true)申明为一个只读事务？
需要，因为存在`可能的优化`

我们可以看一下@Transactional注解的源码，其中的readOnly 属性的解释
~~~
	/**
	 * A boolean flag that can be set to {@code true} if the transaction is
	 * effectively read-only, allowing for corresponding optimizations at runtime.
	 * <p>Defaults to {@code false}.
	 * <p>This just serves as a hint for the actual transaction subsystem;
	 * it will <i>not necessarily</i> cause failure of write access attempts.
	 * A transaction manager which cannot interpret the read-only hint will
	 * <i>not</i> throw an exception when asked for a read-only transaction
	 * but rather silently ignore the hint.
	 * @see org.springframework.transaction.interceptor.TransactionAttribute#isReadOnly()
	 * @see org.springframework.transaction.support.TransactionSynchronizationManager#isCurrentTransactionReadOnly()
	 */
	boolean readOnly() default false;
~~~
这段文字的说明如下：
- 一个布尔标志，如果事务设置为只读，`允许在运行时进行相应的优化`。默认为false；
- 这只是对实际事务子系统的提示，它不一定会导致写入访问尝试失败。无法解析只读提示的事务管理器也不会引发异常而是默默地忽略这个属性。

###对读一致性的验证
如下单元测试代码中testSelect()方法先后查询2次（没有加 @Transactional注解），testInsert()方法在2次查询前插入数据
~~~
package com.springboot.study.demo1;
import com.springboot.study.demo1.entity.User;
import com.springboot.study.demo1.mapper.UserMapper;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;
import javax.annotation.Resource;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 *@program: springboot_study
 *@description:
 *@author: yinkai
 *@create: 2020-02-29 12:03
 */
@RunWith(SpringRunner.class)
@SpringBootTest
@Rollback(value=false)//事务提交而不是回滚
public class TestTran {


    @Resource
    private UserMapper mapper;


    @Test
    public void testSelect() throws InterruptedException {

        List<User> list1 = mapper.selectList(null);
        System.out.println(list1.size());
        //睡眠5秒给insert事务提供时间
        System.out.println("=================睡眠20s==============");
        TimeUnit.SECONDS.sleep(20);
        //再次查询
        List<User> list2 = mapper.selectList(null);
        System.out.println(list2.size());

    }

    @Test
    @Rollback(value=false)//事务提交而不是回滚
    @Transactional
    public void testInsert(){
        User user = new User(11L,"YINKAI",25,"YINKAI@ALIYUN.COM",213);
        mapper.insert(user);
    }


}
~~~
运行测试方法testSelect()，该方法在第一次查询之后睡眠20秒（查询记录为18条）。然后执行testInsert()方法，插入了一条数据后testSelect()睡眠时间到继续执行，再次查询记录为19条。两次查询结果不一致，这也是一种`幻读现象`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-af9a79bc2b973e7a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

进行对比试验，在testSelect()方法上加上@Transactional(readOnly = true)注解
~~~

    @Test
    @Transactional(readOnly = true)
    public void testSelect() throws InterruptedException {

        List<User> list1 = mapper.selectList(null);
        System.out.println(list1.size());
        //睡眠5秒给insert事务提供时间
        System.out.println("=================睡眠20s==============");
        TimeUnit.SECONDS.sleep(20);
        //再次查询
        List<User> list2 = mapper.selectList(null);
        System.out.println(list2.size());

    }
~~~
再次运行testSelect()和testInsert()方法，发现两次结果相同。而且只发出了一条sql语句(这个优化并不是readOnly = true所带来的，事实上只要加上@Transactional注解就会有这种优化)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f3c92e6caaa14201.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


再次进行对比试验，在testSelect()方法上加上@Transactional注解（不包含readOnly 属性）
~~~
    @Test
    @Transactional
    public void testSelect() throws InterruptedException {
        List<User> list1 = mapper.selectList(null);
        System.out.println(list1.size());
        //睡眠5秒给insert事务提供时间
        System.out.println("=================睡眠20s==============");
        TimeUnit.SECONDS.sleep(20);
        //再次查询
        List<User> list2 = mapper.selectList(null);
        System.out.println(list2.size());
    }
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-47fc20ce603b6e3d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用@Transactional注解不加readOnly=true 也只是发出一条sql，这就是一种优化。但是此优化并非readOnly=true所带来的;两次查询结果相同，说明单单使用@Transactional注解就能够带来 读一致性(可重复读)







###大总结
在开发中我们需要在只发出查询语句的方法上添加@Transactional(readOnly = true)注解，将之申明为只读事务。

- 多条查询下要使用该注解，能够防止多次查询到的数据不一致（维持可重复读）。而且有一定的优化，比如上面的两次的查询只发出一条sql；
- 尽管在单条查询下不会出现数据不一致现象，但是使用@Transactional(readOnly = true)注解能够优化查询，源码中提到readOnly = true也存在着`可能的优化`！

加上@Transactional(readOnly = true)可以`保证读一致性`和`查询优化`以及一些`可能的优化`，即使数据库和驱动底层不支持readOnly 属性，那也不会报错。我们何乐而不为呢？


###如何证明readOnly = true带来了优化？

事实上readOnly 和spring没有任何关系，spring事务仅仅是一层封装，最后都要调用底层驱动的setReadonly方法来开启。所以readOnly 是否能到来优化还是要看 `数据库类型和驱动类型`；所以readonly语义不是所有的数据库驱动都支持的

比如Oracle对于只读事务，不启动回滚段，不记录回滚log。又比如在spring+hibernate的条件下，readonly有一些优化  

spring doc 有如下描述
~~~
Read-only status: A read-only transaction can be used when your code
reads but does not modify data. Read-only transactions can be a useful
optimization in some cases, such as when you are using Hibernate.
~~~
这句话解释如下：
只读状态:当代码读取但不修改数据时，可以使用只读事务。在某些情况下，只读事务可能是一种有用的优化，例如当您使用hibernate时


