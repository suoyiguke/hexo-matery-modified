---
title: redis持久化-的AOF文件重写.md
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
title: redis持久化-的AOF文件重写.md
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
###AOF重写


文件重写之所以能够压缩AOF文件，原因在于：

*   过期的数据不再写入文件
*   无效的命令不再写入文件：如有些数据被重复设值、有些数据被删除了等等
*   多条命令可以合并为一个

通过上述内容可以看出，由于重写后AOF执行的命令减少了，文件重写既可以减少文件占用的空间，也可以加快恢复速度。

###文件重写的触发

文件重写的触发，分为手动触发和自动触发：

*   手动触发：直接调用bgrewriteaof命令，该命令的执行与bgsave有些类似：都是fork子进程进行具体的工作，且都只有在fork时阻塞。

![image.png](https://upload-images.jianshu.io/upload_images/13965490-de9e6183aeb2fa32.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


此时服务器执行日志如下：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f83bc26d7e95a5e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


*   自动触发：根据auto-aof-rewrite-min-size和auto-aof-rewrite-percentage参数，以及aof_current_size和aof_base_size状态确定触发时机。

*   auto-aof-rewrite-min-size：执行AOF重写时，文件的最小体积，默认值为64MB。

*   auto-aof-rewrite-percentage：执行AOF重写时，当前AOF大小(即aof_current_size)和上一次重写时AOF大小(aof_base_size)的比值。

其中，参数可以通过config get命令查看：
~~~
192.168.10.11:0>config get auto-aof-rewrite-min-size
 1)  "auto-aof-rewrite-min-size"
 2)  "67108864"
192.168.10.11:0>config get auto-aof-rewrite-percentage
 1)  "auto-aof-rewrite-percentage"
 2)  "100"
192.168.10.11:0>
~~~

状态可以通过info persistence查看：

![image](https://upload-images.jianshu.io/upload_images/13965490-efb32262b753901c?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

只有当auto-aof-rewrite-min-size和auto-aof-rewrite-percentage两个参数同时满足时，才会自动触发AOF重写，即bgrewriteaof操作。

自动触发bgrewriteaof时，可以看到服务器日志如下：

![image](https://upload-images.jianshu.io/upload_images/13965490-abfee9c4696badc4?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###文件重写的流程


![image](https://upload-images.jianshu.io/upload_images/13965490-f5be5ec5a1b0a7db?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

关于文件重写的流程，有两点需要特别注意：

*   重写由父进程fork子进程进行；

*   重写期间Redis执行的写命令，需要追加到新的AOF文件中，为此Redis引入了aof_rewrite_buf缓存。

对照上图，文件重写的流程如下：

*   Redis父进程首先判断当前是否存在正在执行 bgsave/bgrewriteaof的子进程，如果存在则bgrewriteaof命令直接返回，如果存在bgsave命令则等bgsave执行完成后再执行。前面曾介绍过，这个主要是基于性能方面的考虑。

*   父进程执行fork操作创建子进程，这个过程中父进程是阻塞的。

*   父进程fork后，bgrewriteaof命令返回”Background append only file rewrite started”信息并不再阻塞父进程，并可以响应其他命令。Redis的所有写命令依然写入AOF缓冲区，并根据appendfsync策略同步到硬盘，保证原有AOF机制的正确。

    由于fork操作使用写时复制技术，子进程只能共享fork操作时的内存数据。由于父进程依然在响应命令，因此Redis使用AOF重写缓冲区(图中的aof_rewrite_buf)保存这部分数据，防止新AOF文件生成期间丢失这部分数据。也就是说，bgrewriteaof执行期间，Redis的写命令同时追加到aof_buf和aof_rewirte_buf两个缓冲区。

*   子进程根据内存快照，按照命令合并规则写入到新的AOF文件。

*   子进程写完新的AOF文件后，向父进程发信号，父进程更新统计信息，具体可以通过info persistence查看。

    父进程把AOF重写缓冲区的数据写入到新的AOF文件，这样就保证了新AOF文件所保存的数据库状态和服务器当前状态一致。

    使用新的AOF文件替换老文件，完成AOF重写。


###BGREWRITEAOF 命令


Redis `BGREWRITEAOF` 命令用于异步执行一个 AOF（AppendOnly File）文件重写操作。重写会创建一个当前AOF文件的体积优化版本。

即使 `BGREWRITEAOF` 执行失败，也不会有任何数据丢失，因为旧的AOF文件在`BGREWRITEAOF` 成功之前不会被修改。

AOF 重写由 Redis 自行触发， `BGREWRITEAOF`仅仅用于手动触发重写操作。

具体内容:

*   如果一个子Redis是通过磁盘快照创建的，AOF重写将会在RDB终止后才开始保存。这种情况下`BGREWRITEAOF`任然会返回OK状态码。从Redis 2.6起你可以通过 INFO 命令查看AOF重写执行情况。
*   如果只在执行的AOF重写返回一个错误，AOF重写将会在稍后一点的时间重新调用。

从 Redis 2.4 开始，AOF重写由 Redis 自行触发，`BGREWRITEAOF`仅仅用于手动触发重写操作。

## 返回值

[simple-string-reply](http://www.redis.cn/topics/protocol.html#simple-string-reply): 总是返回 `OK`。


###清除掉所有数据然后进行AOF文件重写
- 原来的AOF文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5337f45d769100a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 干掉所有数据
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6b29f9f2642bc76a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 重写AOF 
执行 
~~~
BGREWRITEAOF
~~~ 

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f9fb45cfd4104e2d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- AOF文件缩小了很多，里面有一些乱码
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f2c64a6ea2f86ff6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- aof重写的同时导致了RDB文件的重新生成，因此注意执行这个命令后RDB文件会发生变化。之前的RDB文件要备份好
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fe47f64552e136d1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###进行叠加redis重写
- 执行这个python程序，让age字段迭加3000次
~~~
import redis


class TestRedis(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='192.168.10.11',port=6379, db=2,password='123456')


    def  setItem(self,key,value):
        """set -- 设置单个键值"""
        rest = self.r.set(key, value)
        return rest # 返回True or Flase

    def getItem(self,key):
        """get -- 获取单个键值"""
        rest = self.r.get(key)
        return rest

def initData():
    redis = TestRedis();
    #直接刷数据
    for item in list(range(4000,8000)):
        print(item)
        redis.setItem(item,item)

def incrData():
    redis = TestRedis();
    redis.r.set('age',1)
    for item in list(range(1000,4000)):
        print("加一")
        rest = redis.r.incr('age')
    return rest # 但会增加后键值结果

if __name__ == '__main__':
    incrData()

~~~
- aof文件大小
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3f8822cdb9c73b87.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- aof文件详情
![image.png](https://upload-images.jianshu.io/upload_images/13965490-af5c44b8ba230421.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 数据情况
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2b864659f40ad11d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 执行
~~~
BGREWRITEAOF
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-879a0bd69d0aea54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- aof文件体积明显缩小到了105
![image.png](https://upload-images.jianshu.io/upload_images/13965490-356133ba0a5a9ea1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 数据还是这样，没有变化
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d7266ce465683ef7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
