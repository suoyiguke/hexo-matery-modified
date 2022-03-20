---
title: redis持久化-手动使用RDB方式恢复数据.md
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
title: redis持久化-手动使用RDB方式恢复数据.md
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
在aof和rdb同时开启时，仅仅使用rdb方式恢复时不起作用的，因为redis会优先使用aof恢复，但由于aof不存在则会创建一个新的aof文件，导致恢复的是空的aof指令，同样加载到redis内存中的数据也是空的。


###先手动备份redis数据到rdb文件
1、在redis客户端执行：
~~~
bgsave
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0fd9a8fd4072d56f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- SAVE  和BGSAVE 均是备份rdb文件的命令
- SAVE  保存是阻塞主进程，客户端无法连接redis，等SAVE完成后，主进程才开始工作，客户端可以连接

- BGSAVE  是fork一个save的子进程，在执行save过程中，不影响主进程，客户端可以正常链接redis，等子进程fork执行save完成后，通知主进程，子进程关闭。很明显BGSAVE方式比较适合线上的维护操作，两种方式的使用一定要了解清楚在谨慎选择。
  
2、得到了rdb文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d6a7bf9e2becb72e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 ###使用rdb文件恢复数据
1、关闭aof参数功能
修改redis.conf配置
~~~
appendonly no
~~~
2、将rdb文件放入指定的持久化文件夹

![image.png](https://upload-images.jianshu.io/upload_images/13965490-2a2369163db9dbf1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 这个文件夹路径就是
~~~
# 文件保存路径
dir /home/work/app/redis/data/
~~~
3、启动redis
redis日志显示读取硬盘上的数据
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8c57267d868dabf3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、使用命令重新开启aof
在redis客户端中执行命令：
~~~
config set appendonly yes
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-998c0e414bb9e855.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样redis就会直接从rdb恢复数据并重新生成aof
- 注意重新生成的aof是这样的：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-485e28b03e32f6f4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 大小居然和rdb一样
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1cd2279e10f7216d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 使用命令查看aof配置是否打开
~~~
config get appendonly
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-91c1ed305d9744b1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-0e2362fc4d3e536c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

5、然后再关闭redis服务，将appendonly 设置为yes，开启aof，以后redis服务开启后就直接读取aof文件进行恢复数据了
