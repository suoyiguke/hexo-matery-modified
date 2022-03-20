---
title: mysqld--Out-of-memory-(Needed-4194704-bytes)-请问哪个参数可以解决这个问题？.md
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
title: mysqld--Out-of-memory-(Needed-4194704-bytes)-请问哪个参数可以解决这个问题？.md
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
戒糖低盐轻碳水:
超过内存了，buffer_pool设置大了吧

不会游泳的鱼:
给小点吧

走失的小老虎儿:
设置的是1g 

走失的小老虎儿:

set global read_buffer_size=131072;
set global read_rnd_buffer_size=262144;
set global sort_buffer_size=2097152;
set global join_buffer_size=262144;
后来就把其它参数适当改小了

走失的小老虎儿:
innodb_buffer_pool_size=1024M

走失的小老虎儿:
改下了还是不行。

不会游泳的鱼:
服务器内存多少

走失的小老虎儿:
物理内存确实不大，但是改什么参数可以直观的看到效果。

走失的小老虎儿:
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5f7125eeccddcd39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

走失的小老虎儿:
不能重启进程，只能改改参数

戒糖低盐轻碳水:
free完全没了？

此去依然:
那么多缓存？

戒糖低盐轻碳水:
你进程不都挂了么

不会游泳的鱼:
这块放一下

不会游泳的鱼:
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f44484a8fcbc2088.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


此去依然:
你该设置一下系统内核参数

走失的小老虎儿:
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8c75c1011225253d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


不会游泳的鱼:
echo 3 >

此去依然:
服务器先调好

此去依然:
Swap也不关的吗

走失的小老虎儿:
服务器还有其它应用运行。 

走失的小老虎儿:
 swap 默认设置

戒糖低盐轻碳水:
跟应用装一起本身就是禁忌

走失的小老虎儿:
改哪个？

走失的小老虎儿:
32位系统，忘了告大家

戒糖低盐轻碳水:
。。。。

走失的小老虎儿:
很多年前的。 

走失的小老虎儿:


戒糖低盐轻碳水:
你这是把所有坑都踩了一遍啊

许天云:


走失的小老虎儿:
以前我从来没用过32位的

许天云:
想起了项目上在64位系统上装了32位的sqlserver，内存最多用4G.

此去依然:
你先把内核参数刷脏页的参数改了，然后echo 3>/proc/sys/vm/drop_caches

走失的小老虎儿:
改什么参数？大家给出个主意

不会游泳的鱼:
echo 3 > /proc/sys/vm/drop_caches　

戒糖低盐轻碳水:
只能释放cache腾出内存

不会游泳的鱼:
这就是我和大神的区别 我只知道释放所有缓存，内核参数刷脏页完全不知道

此去依然:
![image.png](https://upload-images.jianshu.io/upload_images/13965490-777bff1c0d03e9bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



此去依然:
主要就这三个参数

戒糖低盐轻碳水:


走失的小老虎儿:
@成都-华三-胡鹏元 会不会挂掉？刮掉的话，会出大事的！

此去依然:
哎，那你得先看看谁用的这么多缓存

不会游泳的鱼:
释放缓存应该没多大问题吧

此去依然:
不行就先清dentry和inodes

此去依然:
slabtop看一下dentry多不多

走失的小老虎儿:
嗯，开完会了看看！

此去依然:
你们这重要环境都没有监控的吗，实验环境挂就挂了无所谓

走失的小老虎儿:
32位，进程调用内存可以超出4g

走失的小老虎儿:
吗？

走失的小老虎儿:
用户的系统

戒糖低盐轻碳水:
都32位系统，数据库和应用混装了，还想监控

走失的小老虎儿:


戒糖低盐轻碳水:
能想到监控就不会这么玩了

走失的小老虎儿:
增加内存是不可能的了！

走失的小老虎儿:
只能调参数！

走失的小老虎儿:


此去依然:
[动画表情]

走失的小老虎儿:
mysqld进程都3050m了！

走失的小老虎儿:
都是有故事的机器了。

戒糖低盐轻碳水:
那你得控制其它程序的内存上限，不然内存容易爆，然后用swap或者oom了吧

走失的小老虎儿:
应用是不可能改的，也限制不了！

走失的小老虎儿:


戒糖低盐轻碳水:


走失的小老虎儿:
应用谁开发的都不一定找得到！

挽弓如月:
暂时的方法只能调整ibp 到1G，重启mysql释放内存，用了那么久没出事，就算不释放内存会慢慢增大，也能撑一段时间

空、白:
ps -auxw|head -n 1;ps -auxw|sort -rn -k 4|head -n 5

空、白:
看下内存都被谁使用了

此去依然:
条件太艰苦了

此去依然:
我上次在招行看到的服务器，整个机房都是700+G的内存

李贵平:
内存用了3G太艰苦了
