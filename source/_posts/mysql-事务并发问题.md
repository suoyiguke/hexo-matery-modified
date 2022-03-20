---
title: mysql-事务并发问题.md
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
title: mysql-事务并发问题.md
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
###脏读
事务A读取到了事务B已经修改但`尚未提交`的数据，如果B事务回滚，A读取的数据无效，不符合事务特性中的 `一致性`

>- `脏读` 针对的是A事务读到B事务`（没有提交的事务）`对数据库的更改
>- 出现在 RU 下

######在Read uncommitted下进行验证“脏读”

![image.png](https://upload-images.jianshu.io/upload_images/13965490-328c8bba8ee617c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c2a34ae4851558d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
######在 Read committed 下做对比试验
理论上RC下不会出现“脏读”

![image.png](https://upload-images.jianshu.io/upload_images/13965490-22df144c25f45ed8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5b1b6f6d46258525.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###不可重复读
事务A读取到了事务B已经提交的修改数据，不符合事务特性中的`隔离性`

>- `不可重复读` 针对的是B事务的 update操作的提交对A事务的影响(注意B事务需要提交)
>- 出现在 RU、RC 下

######在Read committed下验证“不可重复读”
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c3aeeabe3022672d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-9fb728755de68158.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
######在Repeatable Read下测试对比
理论上RR下不会出现“不可重复读”的问题。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-64f9477b3620b445.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a60f798fa619328f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###幻读(幻影读)
事务A读取到了事务B提交的新增数据，不符合事务特性中的`隔离性`

>- `幻影读` 针对的是B事务中insert 操作的提交对A事务的影响(注意B事务需要提交)
>- 出现在 RU、RC、RR 下

######在Read committed下验证 “幻影读”
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0c2e27b27e3473ac.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8a560ac7b800fcd7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######在Repeatable Read下验证 “幻影读”
  因为RR下存在MVCC机制，select是`快照读`，select不会出现幻读；但是insert和update是`当前读` 因此事务B中insert操作提交的相同id记录会报主键冲突错误
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bafd026ee3646981.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-29f145a81836fb72.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 在Serializable下做对比试验，理论上SE下不会出现幻读
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c30b99f4a016a240.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f84ea01855dcb38a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###事务更新丢失
两个事务同时操作相同的数据，后提交的事务会`覆盖`先提交的事务处理结果;它在RC、RU、RR 下均会发生，唯独在SE下不会

我的这篇博客有详细验证这个问题
https://www.jianshu.com/p/bfd7c684412d
