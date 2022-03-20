---
title: spring--事务管理之传播行为对回滚的影响（一）.md
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
title: spring--事务管理之传播行为对回滚的影响（一）.md
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
>学如逆水行舟，不进则退

背景： A方法调用B方法。验证事务的回滚情况。
A方法对应下面例子的InsertUsers方法
B方法对应InsertCuser方法

###代码准备

InsertUsers()方法如下
>InsertUsers()方法中调用了InsertCuser()方法，制造事务传播的条件
~~~
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
~~~
InsertCuser()方法如下
~~~
    @Override
    public void InsertCuser(Cuser cuser) {
        jdbcTemplate.update("INSERT INTO cuser(id,name, age, email) VALUES (?, ?, ?, ?);", cuser.getId(), cuser.getName(), cuser.getAge(), cuser.getEmail());
        //打印事务名
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());

    }
~~~




###A方法和B方法均没有开启事务

无论出现什么异常 A、B事务均不会回滚。这种情况毋庸置疑，就不验证了。当然要考虑出现异常代码的位置，因为在调用B方法之前出现异常，B方法都不会执行，这样最终结果就不同了。

###A方法将事务传播给B方法，两者属于同一事务
 A方法抛出异常或B方法抛出异常都会导致整体事务的回滚

>给两个方法上都加上REQUIRED级别的事务传播行为，这样两个方法属于同一个事务管理
~~~
    @Transactional(propagation = Propagation.REQUIRED)
    public void InsertUsers(Users users){
    。。。
    }

    @Transactional(propagation= Propagation.REQUIRED)
    public void InsertCuser(Cuser cuser){
     。。。
    }
~~~
>然后分别将下列引发运行时异常的语句放到A方法或B方法中，观察事务回滚情况
~~~
//运行时异常
int i = 1/0;
~~~

经过试验，两者属于同一事务时。一个方法中有抛出异常则整体失败回滚~ 
也可能出现在调用B方法之前A方法出现异常，B方法没有执行的情况。`当然这种情况的结果和AB方法一起回滚的最终结果是一致的`






###A方法和 B方法各自开启事务
 
  两者理应互相隔离执行，互不影响。但是却在下面的情景模式中B事务出错，A事务也被回滚。到底是什么原因呢？我们来看看下面



######`重要`A方法调用B方法，两个独立事务。B方法出现异常，A、B 均回滚的问题

猜想：按照两者的传播行为，InsertUsers方法和InsertCuser各自会开启事务。InsertCuser()异常方法回滚不会影响到InsertUsers()

首先我们需要制造一种两个方法各自持有一个事务的情景模式：
>我们给InsertUsers加上REQUIRED
~~~
    @Transactional(propagation= Propagation.REQUIRED)
    public void InsertUsers(Users users) {
     。。。
    }
~~~

>我们给InsertCuser加上REQUIRES_NEW
~~~
@Transactional(propagation= Propagation.REQUIRES_NEW)
public void InsertCuser(Cuser cuser) {
     。。。
    }
~~~

>在InsertCuser()方法内部添加一行除0异常代码（运行时异常）
~~~
 @Transactional(propagation= Propagation.REQUIRES_NEW)
 @Override
    public void InsertCuser(Cuser cuser) {
        jdbcTemplate.update("INSERT INTO cuser(id,name, age, email) VALUES (?, ?, ?, ?);", cuser.getId(), cuser.getName(), cuser.getAge(), cuser.getEmail());
        //打印事务名
        List<Map<String, Object>> maps = jdbcTemplate.queryForList("SELECT TRX_ID FROM INFORMATION_SCHEMA.INNODB_TRX WHERE TRX_MYSQL_THREAD_ID = CONNECTION_ID( );");
        System.out.println(maps + TransactionSynchronizationManager.getCurrentTransactionName());

        //运行时异常
        int i = 1/0;
    }
~~~



添加各自的传播行为后。运行程序，经过我的测试，这次两个事务都回滚了! 因为数据库users表和 cuser表中都不存在插入的记录。若只有InsertCuser()事务回滚，那么users表中应该要有数据。如图两表均为空，说明两个事务一起回滚
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f174b2f5eee6b382.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


那应该如何解决这个问题，让事务InsertUsers()方法的事务不要跟着回滚呢？
我们知道，要达到回滚的目的就必须在本事务方法中将异常抛出（throw）。而`运行时异常`会自动回滚的，说明`运行时异常`总是被隐式抛出到上层调用者。也就是说java中会隐式抛出运行时异常。那如果我们在上层将异常捕获，不进行抛出让内部消化掉是不是就能防止回滚了呢？ 
说干就干，如下面代码。将InsertUsers()方法修改如下，调用InsertCuser方法的地方使用try/catch包裹起来，不进行抛出
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
        //将InsertCuser方法抛出的异常捕获，不进行抛出。则InsertUsers事务不会回滚~
        try {
            cuserService.InsertCuser(cuser);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
~~~

运行后，users表中有数据记录，cuser表中无数据。说明InsertUsers()方法事务成功提交。问题完美解决~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-ee58f29bf87ffa60.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-61ba4a90e8130d6f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######A方法调用B方法，两个独立事务。A方法在调用B方法之前出现异常
这样B方法根本得不到执行，A事务回滚了。预测两个表中均无插入数据
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ee5932994a033d11.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######A方法调用B方法，两个独立事务。A方法在调用B方法之后出现异常

这样A、B属于不同事务管理，A在调用B后出现异常是不会影响到B的。 预测 users表中无插入数据，cuser表中有插入数据
![image.png](https://upload-images.jianshu.io/upload_images/13965490-62a083d73f9a2154.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



关于两个方法中只有一个方法纳入事务管理的情况比较复杂，可以继续看下我的这篇文章：https://www.jianshu.com/p/49c87a91e153


