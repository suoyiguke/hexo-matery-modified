---
title: redis持久化-介绍.md
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
title: redis持久化-介绍.md
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
redis中文文档： http://www.redis.cn/topics/persistence.html

###Redis为持久化提供了两种方式：

- RDB：在指定的时间间隔能对你的数据进行`快照`存储。
- AOF：记录redis的`操作日志`，当服务器重启的时候会重新执行这些命令来恢复原始的数据。



##AOF方式

~~~
# 是否开启aof
appendonly yes

# 文件名称
appendfilename "appendonly.aof"

# 同步方式
appendfsync everysec

# aof重写期间是否同步
no-appendfsync-on-rewrite no

# 重写触发配置
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# 加载aof时如果有错如何处理
aof-load-truncated yes

# 文件重写策略
aof-rewrite-incremental-fsync yes
~~~

- appendfsync everysec 它其实有三种模式:

   always：把每个写命令都立即同步到aof，很慢，但是很安全
everysec：每秒同步一次，是折中方案
no：redis不处理交给OS来处理，非常快，但是也最不安全
一般情况下都采用 everysec 配置，这样可以兼顾速度与安全，最多损失1s的数据。



- aof-load-truncated yes 如果该配置启用，在加载时发现aof尾部不正确是，会向客户端写入一个log，但是会继续执行，如果设置为 no ，发现错误就会停止，必须修复后才能重新加载。

查看AOF文件
一个set 操作包含7个指令：
~~~
SET
$4
2995
$4
2995
*3
$3
~~~
一个remove包含3个指令：
~~~
DEL
$6
yinkai
~~~
一个SELECT包含5个指令
~~~
SELECT
$1
2
*2
$3
~~~

一份完整的AOF文件
~~~
SET
$4
2995
$4
2995
*3
$3
SET
$4
2996
$4
2996
*3
$3
SET
$4
2997
$4
2997
*3
$3
SET
$4
2998
$4
2998
*3
$3
SET
$4
2999
$4
2999

~~~

####AOF 优缺点
优势：数据完整性好
劣势：相同数据集的数据而言aof文件要远大于rdb文件，恢复速度慢于rdb；Aof运行效率要慢于rdb,每秒同步策略效率较好，不同步策略效率和rdb相同

##RDB方式
~~~
# 时间策略
save 900 1
save 300 10
save 60 10000

# 文件名称
dbfilename dump.rdb

# 文件保存路径
dir /home/work/app/redis/data/

# 如果持久化出错，主进程是否停止写入
stop-writes-on-bgsave-error yes

# 是否压缩
rdbcompression yes

# 导入时是否检查
rdbchecksum yes
~~~
- 持久化的时间策略
  save 900 1 表示900s内如果有1条是写入命令，就触发产生一次快照，可以理解为就进行一次备份

  save 300 10 表示300s内有10条写入，就产生快照
下面的类似，那么为什么需要配置这么多条规则呢？因为Redis每个时段的读写请求肯定不是均衡的，为了平衡性能与数据安全，我们可以自由定制什么情况下触发备份。所以这里就是根据自身Redis写入情况来进行合理配置。

- stop-writes-on-bgsave-error yes 这个配置也是非常重要的一项配置，这是当备份进程出错时，主进程就停止接受新的写入操作，是为了保护持久化的数据一致性问题。如果自己的业务有完善的监控系统，可以禁止此项配置， 否则请开启。

- 关于压缩的配置 rdbcompression yes ，建议没有必要开启，毕竟Redis本身就属于CPU密集型服务器，再开启压缩会带来更多的CPU消耗，相比硬盘成本，CPU更值钱。

- 动态设定文件名和保存路径：Redis启动后也可以动态修改RDB存储路径，在磁盘损害或空间不足时非常有用；执行命令为
~~~
config set dir /data/redis/
config set dbfilename  newname.rdb
~~~

- 当然如果你想要禁用RDB配置，也是非常容易的

 1、可以在redis客户端执行
~~~
config set save ""
~~~
   2、可以修改redis.conf文件，注释掉自动触发save n m
~~~
save ""
#   save 900 1
#   save 300 10
#   save 60 10000
~~~

####RDB方式的优势和劣势

优势：适合大规模的数据恢复；对数据完整性和一致性要求不高
缺点：在一定间隔时间做一次备份，所以如果redis意外down掉的话，就会丢失最后一次快照后的所有修改；Fork的时候，内存中的数据被克隆了一份，大致2倍的膨胀性需要考虑


##恢复数据
重新启动Redis就可以恢复数据
###恢复数据的具体流程：
启动时会先检查AOF文件是否存在，如果不存在就尝试加载RDB。那么为什么会优先加载AOF呢？因为AOF保存的数据更完整，通过上面的分析我们知道AOF基本上最多损失1s的数据。

###两种方式的原理

####Redis内部的定时任务机制
定时任务执行的频率可以在配置文件中通过 hz 10 来设置（这个配置表示1s内执行10次，也就是每100ms触发一次定时任务）。该值最大能够设置为：500，但是不建议超过：100，因为值越大说明执行频率越频繁越高，这会带来CPU的更多消耗，从而影响主进程读写性能。


###RDB的原理
####RDB持久化的触发分为两种：自己手动触发与Redis定时触发。

- 手动触发 save：会阻塞当前Redis服务器，直到持久化完成，线上应该禁止使用。

- 自动触发 bgsave：该触发方式会开启一个子进程，由子进程负责持久化过程，因此阻塞只会发生在开启子进程的时候。

####而自动触发的场景主要是有以下几点：

- 根据设置的触发事件策略 save 900 1 配置规则自动触发；
- redis集群中从节点进行全量复制时，主节点发送rdb文件给从节点完成复制操作，主节点会触发 bgsave；
- 执行 debug reload 时；
- 手动关闭redis，执行 shutdown时，如果没有开启aof，也会触发。


###AOF的原理
AOF 重写和 RDB 创建快照一样，都巧妙地利用了写时复制机制:

- Redis 执行 fork() ，现在同时拥有父进程和子进程。
- 子进程开始将新 AOF 文件的内容写入到临时文件。
- 对于所有新执行的写入命令，父进程一边将它们累积到一个内存缓存中，一边将这些改动追加到现有 AOF 文件的末尾,这样样即使在重写的中途发生停机，现有的 AOF 文件也还是安全的。
- 当子进程完成重写工作时，它给父进程发送一个信号，父进程在接收到信号之后，将内存缓存中的所有数据追加到新 AOF 文件的末尾。搞定！现在 Redis 原子地用新文件替换旧文件，之后所有命令都会直接追加到新 AOF 文件的末尾。



###如何选择使用哪种持久化方式？
同时使用两种持久化功能

