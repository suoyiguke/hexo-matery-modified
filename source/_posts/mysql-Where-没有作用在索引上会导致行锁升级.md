---
title: mysql-Where-没有作用在索引上会导致行锁升级.md
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
title: mysql-Where-没有作用在索引上会导致行锁升级.md
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
同事的接口总是有插入多条的问题，之前给加了事务注解暂时解决了查出多条的问题。现在又有插入了多条的问题。
我怀疑是出现了幻读，毕竟mysql在RR级别下是可能发生幻读的------在insert和update的当前读下(MVCC机制)，因此可以给加一个s锁，让其他事务不能在提交前进行修改和插入操作。

但是总是出现死锁Deadlock 问题，觉得这个用户应该只有我一人在测试而已。为什么导致这么频繁的锁竞争？
```
### Cause: com.mysql.jdbc.exceptions.jdbc4.MySQLTransactionRollbackException: Deadlock found when trying to get lock; try restarting transaction
```

```
<select id="selectByUserIdAndRecordTimeAndStatus" resultType="io.renren.modules.api.entity.Record">
   select * from tb_record where user_id=#{userId} and record_time = #{recordTime} and user_status = #{status} lock in share mode;
</select>
```
自己实验了下，在查询后打个断点，保证事务没有被提交。让当前事务持有锁
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2000e51c7c558cad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

再次发起请求，发现被阻塞，在意料之中。注意userId为276

![image.png](https://upload-images.jianshu.io/upload_images/13965490-35c8323ab8f0c211.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

修改请求参数的userId为70 再次请求，还是被阻塞！说明行锁升级成表锁了

添加三个字段的联合索引
![image.png](https://upload-images.jianshu.io/upload_images/13965490-83480a131a301315.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
再次发起 userId为 70的请求， 正常！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d406d2b4ae7ae1ed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这样接口在常规情况，一个账号一个用户下是不会出现lock wait的，也杜绝了幻读
