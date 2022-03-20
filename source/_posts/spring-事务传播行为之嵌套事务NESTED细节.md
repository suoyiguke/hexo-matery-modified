---
title: spring-事务传播行为之嵌套事务NESTED细节.md
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
title: spring-事务传播行为之嵌套事务NESTED细节.md
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
> 逖不能兴中原而复济者，有如大江！

经过我之前的实践，可以看出 NESTED事务申明在调用者上会新建一个独立事务。申明在被调用者上，若调用者存在事务则加入调用者事务。调用者不存在事务则新建一个独立事务。

这个功能好像和spring默认的事务传播行为REQUIRED一样的？
不，它的功能可是比REQUIRED要强大！


######我来通过实验证明NESTED和REQUIRED的区别
这个例子是基于 https://www.jianshu.com/p/bc3cbacf9e70 这个文章的代码

>首先，InsertUsers和InsertCuser方法上都申明了REQUIRED，让他们属于同一个事务。将引发异常的语句 ` int i = 1/0;` 放到 InsertCuser方法里
~~~
    @Transactional(propagation = Propagation.REQUIRED)
    @Override
    public void InsertUsers(Users users) {
        jdbcTemplate.update("INSERT INTO users(id,name, age, email) VALUES (?, ?, ?, ?);", users.getId(), users.getName(), users.getAge(), users.getEmail());
        //调用service中另一个方法
        Cuser cuser = new Cuser(users.getId(), users.getName(), users.getAge(), users.getEmail());
        //打印事务名
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());
        //对InsertCuser抛出的异常进行捕获处理，并且不再向上抛出
        try {
            cuserService.InsertCuser(cuser);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
~~~

~~~
  @Transactional(propagation=Propagation.REQUIRED)
    @Override
    public void InsertCuser(Cuser cuser) {

        jdbcTemplate.update("INSERT INTO cuser(id,name, age, email) VALUES (?, ?, ?, ?);", cuser.getId(), cuser.getName(), cuser.getAge(), cuser.getEmail());
        //打印事务名
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());
        int i = 1/0;
    }
~~~

######`注意` 为什么要加try/catch包裹cuserService.InsertCuser(cuser);语句？
> 为了杜绝InsertCuser中抛出的异常影响InsertUsers方法的实验结果
~~~
try {
            cuserService.InsertCuser(cuser);
        } catch (Exception e) {
            e.printStackTrace();
        }
~~~



程序运行，结果是InsertCuser中出现异常，导致事务回滚、users表和cuser表均无数据插入。由于两个方法被纳入同一个事务，因此两者都会回滚。即使在cuserService.InsertCuser(cuser);上使用try/catch捕获并不抛出异常也没用（此方法能保证调用者方法中的独立事务不受被调用者抛出的异常影响而回滚）


>我们再来看，将上面环境的InsertCuser方法传播行为改成NESTED

~~~
   @Transactional(propagation=Propagation.NESTED)
    @Override
    public void InsertCuser(Cuser cuser) {

        jdbcTemplate.update("INSERT INTO cuser(id,name, age, email) VALUES (?, ?, ?, ?);", cuser.getId(), cuser.getName(), cuser.getAge(), cuser.getEmail());
        //打印事务名
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());
        int i = 1/0;
    }
~~~
再次运行，可以看到日志的打印情况。两方法的事务的id一致，说明的确是相同事务
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f551ed258ff816bf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
users表中插入了数据说明InsertUsers方法提交成功，cuser表中没有数据说明InsertCuser方法回滚
![image.png](https://upload-images.jianshu.io/upload_images/13965490-49efcc641feb9525.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

那么现在就有一个问题了，既然两个方法使用同一个事务，为什么没有一起回滚？

这就是NESTED嵌套事务的奥秘之处-----它能让事务部分回滚

我在网上找到了一句话：
> NESTED申明在被调用方法上，若调用者方法有开启事务。此时NESTED会开始一个 "嵌套的" 事务，  它是已经存在事务的一个真正的子事务。 潜套事务开始执行时， 它将取得一个 `savepoint`。 如果这个嵌套事务失败， 我们将回滚到此 `savepoint`。 潜套事务是外部事务的一部分, 只有外部事务结束后它才会被提交。

这段话中提到的 `savepoint` 其实是mysql的innodb引擎的特性，为了去了解它我在mysql客户端对它进行了简单使用，可以看看这篇文章https://www.jianshu.com/p/c93c1730e5dc 。 总之它就是一个保存点，生成一个保存点就是生成一个数据镜像。然后无论经过了什么sql操作，只要使用回滚至此保存点的命令即可恢复至创建保存点的数据状态。

那么上面代码的演示结果也就说的通了。即使InsertUsers和InsertCuser方法属于同一个事务，被NESTED嵌套事务申明的InsertCuser方法出现异常也没导致REQUIRED申明的InsertUsers的`全部回滚`，只是`部分回滚`到了调用InsertCuser方法之前。因为在调用InsertCuser方法时会自动生成一个`savepoint`


######InsertUsers方法里出现异常会导致InsertCuser方法嵌套事务回滚吗？

将出现异常的代码行放到这里，结果都回滚了，毕竟是同一个事务
![image.png](https://upload-images.jianshu.io/upload_images/13965490-52df2c4dec9d3f00.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######总结下NESTED的回滚特性
- 主事务和嵌套事务属于同一个事务
- 嵌套事务出错回滚不会影响到主事务
- 主事务回滚会将嵌套事务一起回滚了

######进一步证明NESTED嵌套事务的savepoint机制

可以通过阅读spring源码的方式来验证NESTED是不是使用savepoint机制来实现的，我现在的水平还不足以去阅读源码。但是我会很快就有这个能力的，我相信！ 不过有简友已经分析过了，可以去看看。写的很好~
https://www.jianshu.com/p/2f79ee33c8ad




