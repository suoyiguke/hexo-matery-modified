---
title: mysql-记录一次线上出现的表锁问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: mysql-记录一次线上出现的表锁问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
今天突然线上业务接口出现了一直请求超时，远程到服务器查看日志，报了我们熟悉的 lock time out　错误。查询　SELECT * from information_schema.INNODB_TRX，观察到有事务在00:00:00 凌晨开启，到现在仍然活跃。要么就是事务超级大，要么就是代码哪里没有commit这个事务，导致一直将biz_cert_info表占用，并迟迟不释放。那么就到系统中寻找在00:00:00时开启的定时任务，得到了以下sql。

目标锁定到了这个sql，经过询问，作用是每天将过期的证书状态值设置为2：
~~~
update  biz_cert_info  set STATUS = 2 WHERE valid_to_date < NOW();
~~~
根据现象来看，insert语句也阻塞了，新申请证书的insert操作被阻塞，推测是将全表都锁了，而update的范围条件只会给指定范围的数据行加锁，所以推测是没走索引。update的where 范围条件是非常危险的，一旦没有作用在索引上，或者索引没有真正使用到，那么将把所有记录均加上行锁。这样就类似将整个表都锁上了，于是insert语句被阻塞。若作用在索引之上至少不会阻塞insert。

所以我想到的解决方案是先加索引，尽量走行锁。

1、给biz_cert_info.valid_to_date 加上索引 valid_to_date_index

![image.png](https://upload-images.jianshu.io/upload_images/13965490-60a8f2de945d4524.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、查看biz_cert_info  表 valid_to_date 居然是varchar类型的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bbad613cde851e58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样的话，会先将函数NOW()输出的内容转为字符串，然后再和valid_to_date（varchar） 进行比较，这样会导致索引失效，执行计划如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bac4b4eb2f98b939.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


所以需要改为mysql的时间类型，这里使用datetime
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0e59fe90a2b3a858.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


3、update语句强制走索引
普通的update还是无法使用到刚刚建立的valid_to_date_index索引，执行计划如下：


使用force index，强制使用valid_to_date_index索引
~~~
EXPLAIN update  biz_cert_info   force index(valid_to_date_index) set STATUS = 2 WHERE valid_to_date < NOW();

~~~

4、进行测试

![image.png](https://upload-images.jianshu.io/upload_images/13965490-dc5863142e2da30f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-9b64109fb12a2992.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这下子后执行的valid_to_date >NOW() 的insert语句并没有被阻塞，成功执行！ 当前时间是 2020-08-06，现在只有valid_to_date  < 2020-08-06 的insert语句会被阻塞了。


5、还需要排查下是不是哪里的事务没有提交
当然数据库有提供一种 自动将超时的事务杀死的机制。 procona和mariadb中有innodb_kill_idle_transaction这个参数可以做到
~~~
innodb_kill_idle_transaction
~~~

默认是0秒，你可以根据自己的情况设定阈值。超过这个阈值，服务端自动杀死未提交的空闲事务。

但是mysql5.7并不支持这个参数

