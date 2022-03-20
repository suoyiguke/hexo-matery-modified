---
title: redis常用配置.md
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
title: redis常用配置.md
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
https://codeload.github.com/uglide/RedisDesktopManager/zip/2019.5

###使用docker-compose部署单机redis
vi docker-compose.yml
~~~
version: "2"
services:
  redis:
    image: redis
    network_mode: host
    command:
      redis-server /usr/local/etc/redis/redis.conf
    volumes:
      - ./data:/data
      - ./redis.conf:/usr/local/etc/redis/redis.conf
      - /etc/localtime:/etc/localtime
    restart: always

~~~

准备一份redis.conf 文件，指定密码为123456

docker-compose up 运行
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f0b530077a398f1f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



### 启动时不打印logo
always-show-logo no

###禁用KEYS命令
-  一方面 KEYS * 命令可以列出所有的键，会影响数据安全
- 另一方面 KEYS 命令会阻塞数据库，在数据库中存储了大量数据时，该命令会消耗很长时间，期间对Redis的访问也会被阻塞，而当锁释放的一瞬间，大量请求涌入Redis，会造成Redis直接崩溃
rename-command KEYS ""


###端口
 port 6379
 指定Redis监听端口，默认端口为6379，作者在自己的一篇博文中解释了为什么选用6379作为默认端口，因为6379在手机按键上MERZ对应的号码，而MERZ取自意大利歌女Alessia Merz的名字

###redis远程访问
> protected-mode 和 bind 需要同开同关
有时bind注释后会出现 Creating Server TCP listening socket *:6379: listen: Unknown error 。
这时需要 bind 0.0.0.0

redis3.2版本后新增protected-mode配置，默认是yes，即开启。设置外部网络连接redis服务，设置方式如下：

1、关闭protected-mode模式，此时外部网络可以直接访问;这里需要注意把bind注释掉
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3fb2892e4ebfffe3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、开启protected-mode保护模式，需配置bind ip
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5ecf0e4396b6e27b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这里的ip请填上服务器ip，表示只有通过这个ip才能连上redis

###开启密码验证
![image.png](https://upload-images.jianshu.io/upload_images/13965490-08c98850bfc3e401.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###数据库数量配置
databases 16。
对应数据库的索引值为0 - (databases -1)，即16个数据库，索引值为0-15。设置数据库的数量，默认数据库为16，可以使用SELECT <dbid>命令在连接上指定数据库id
![image.png](https://upload-images.jianshu.io/upload_images/13965490-82937d5cbd22f8a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



### redis中的单位
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8542f5cb20e9a3d5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 配置大小单位,开头定义了一些基本的度量单位，只支持bytes，不支持bit
- 对大小写不敏感
- 注意k和kb的区别

###引入其他配置文件
 include /path/to/local.conf
   和我们的Struts2配置文件类似，可以通过includes包含，redis.conf可以作为总闸，包含其他

###以守护线程方式启动

- redis.conf配置文件中daemonize守护线程，默认是NO。
- daemonize是用来指定redis是否要用守护线程的方式启动。

- daemonize:yes  redis采用的是单进程多线程的模式。当redis.conf中选项daemonize设置成yes时，代表开启守护进程模式。在该模式下，redis会在后台运行，并将进程pid号写入至redis.conf选项pidfile设置的文件中，此时redis将一直运行，除非手动kill该进程。

- daemonize:no  当daemonize选项设置成no时，当前界面将进入redis的命令行界面，exit强制退出或者关闭连接工具(putty,xshell等)都会导致redis进程退出。

###pid文件路径
pidfile /var/run/redis_6379.pid

 当Redis以守护进程方式运行时，Redis默认会把pid写入/var/run/redis.pid文件，可以通过pidfile指定
###tcp-backlog

tcp-backlog 511
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0127b9bd494548d7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 设置tcp的backlog，backlog其实是一个连接队列，backlog队列总和=未完成三次握手队列 + 已经完成三次握手队列。
- 在高并发环境下你需要一个高backlog值来避免慢客户端连接问题。注意Linux内核会将这个值减小到/proc/sys/net/core/somaxconn的值，所以需要确认增大somaxconn和tcp_max_syn_backlog两个值

![image.png](https://upload-images.jianshu.io/upload_images/13965490-17c2442d28f18e3c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###超时关闭客户端连接
timeout 0 单位秒，设置为0则永久连接
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9817c464de92179f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###tcp-keepalive 

tcp-keepalive 300
单位为秒，如果设置为0，则不会进行Keepalive检测，建议设置成60 

###日志

- 指定日志记录级别，Redis总共支持四个级别：debug、verbose、notice、warning，默认为verbose

  loglevel verbose

- 日志记录方式，默认为标准输出，如果配置Redis为守护进程方式运行，而这里又配置为日志记录方式为标准输出，则日志将会发送给/dev/null

  logfile stdout

###内存限制策略

####设置最大客户端连接数
maxclients 0

设置同一时间最大客户端连接数，默认无限制，Redis可以同时打开的客户端连接数为Redis进程可以打开的最大文件描述符数，如果设置 maxclients 0，表示不作限制。当客户端连接数到达限制时，Redis会关闭新的连接并向客户端返回max number of clients reached错误信息

### 设置redis可以使用的内存量
maxmemory <bytes>
`设置redis可以使用的内存量。`一旦到达内存使用上限，redis将会试图移除内部数据，移除规则可以通过maxmemory-policy来指定。如果redis无法根据移除规则来移除内存中的数据，或者设置了“不允许移除”，那么redis则会针对那些需要申请内存的指令返回错误信息，比如SET、LPUSH等。

但是对于无内存申请的指令，仍然会正常响应，比如GET等。如果你的redis是主redis（说明你的redis有从redis），那么在设置内存使用上限时，需要在系统中留出一些内存空间给同步队列缓存，只有在你设置的是“不移除”的情况下，才不用考虑这个因素


###设置移除key的策略
maxmemory-policy `重要`
- volatile-lru：使用LRU算法移除key，只对设置了过期时间的键
- allkeys-lru：使用LRU算法移除key
- volatile-random：在过期集合中移除随机的key，只对设置了过期时间的键
- allkeys-random：移除随机的key
- volatile-ttl：移除那些TTL值最小的key，即那些最近要过期的key
- noeviction：不进行移除。针对写操作，只是返回错误信息

###设置样本数量
 maxmemory-samples 5
`设置样本数量`，LRU算法和最小TTL算法都并非是精确的算法，而是估算值，redis内部会用样本进行测试。所以你可以设置样本的大小,`redis默认会检查这么多个key并选择其中LRU的那个`

###启动
./redis-server redis.conf
