---
title: docker-compose实现redis的一主三从三哨兵的集群.md
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
title: docker-compose实现redis的一主三从三哨兵的集群.md
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
###哨兵模式

- Master 状态监测，如果Master 异常，则会进行Master-slave 转换，将其中一个Slave作为Master，将之前的Master作为Slave ；

- Master-Slave切换后，master_redis.conf、slave_redis.conf和sentinel.conf的内容都会发生改变，即master_redis.conf中会多一行slaveof的配置，sentinel.conf的监控目标会随之调换 。


![image](https://upload-images.jianshu.io/upload_images/13965490-8de3dd54bb90e3d1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image](https://upload-images.jianshu.io/upload_images/13965490-48c829d8068003e5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###哨兵是如何工作的？

①、每个Sentinel以每秒钟一次的频率向它所知的Master，Slave以及其他 Sentinel 实例发送一个 PING 命令 
②、服务器在down-after-milliseconds给定的毫秒数之内， 没有返回 Sentinel 实例发送的 PING 命令的回复， 或者返回一个错误， 则这个实例会被 Sentinel 标记为主观下线。 
③、如果一个Master被标记为主观下线，则正在监视这个Master的所有 Sentinel 要以每秒一次的频率确认Master的确进入了主观下线状态。 
④、当有足够数量的 Sentinel（大于等于配置文件指定的值）在指定的时间范围内确认Master的确进入了主观下线状态， 则Master会被标记为客观下线，才会发生故障迁移，客观下线只适用于主服务器 ；
⑤、在一般情况下， 每个 Sentinel 会以每 10 秒一次的频率向它已知的所有Master，Slave发送 INFO 命令 ，当Master被 Sentinel 标记为客观下线时，Sentinel 向下线的 Master 的所有 Slave 发送 INFO 命令的频率会从 10 秒一次改为每秒一次 ；

⑥、若没有足够数量的Sentinel同意Master已经下线，Master的客观下线状态就会被移除。 若重新发送的PING命令返回有效回复，Master的主观下线状态就会被移除。



###搭建前需要注意的
1、7个机器（7个docker容器）
  1master+3slave+3sentinel
服务器| ip |  端口| 注释
-|-|-|-
master| 10.10.10.1 | 6379 |  主节点|
slave1| 10.10.10.2 | 6380 | 从节点1 |
slave2| 10.10.10.3| 6381  | 从节点2|
slave3| 10.10.10.4| 6382  | 从节点3|
sentinel1| 10.10.10.5| 6383  | 哨兵1|
sentinel2| 10.10.10.6| 6384  | 哨兵2|
sentinel3| 10.10.10.7| 6385  | 哨兵3|

2、配置文件一览
![image.png](https://upload-images.jianshu.io/upload_images/13965490-045c8af5f1f25c44.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###开始搭建
1、编辑docker-compose.yml
~~~
version: '3'
services:
  # 主节点的容器
  redis-server-master:
    image: redis
    container_name: redis-server-master
    ports:
      - 6379:6379
    restart: always
    # 指定时区，保证容器内时间正确
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      # 映射配置文件和数据目录
      - ./redis-master.conf:/usr/local/etc/redis/redis.conf
      - ./data/redis-master:/data
    sysctls:
      net.core.somaxconn: '511'
    command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
    networks:
      hx_net:
        ipv4_address: 10.10.10.1

  # 从节点1的容器
  redis-server-slave-1:
    image: redis
    container_name: redis-server-slave-1
    ports:
      - 6380:6379
    restart: always
    depends_on:
      - redis-server-master
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./redis-slave1.conf:/usr/local/etc/redis/redis.conf
      - ./data/redis-slave-1:/data
    sysctls:
      net.core.somaxconn: '511'
    command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
    networks:
      hx_net:
        ipv4_address: 10.10.10.2
  # 从节点2的容器
  redis-server-slave-2:
    image: redis
    container_name: redis-server-slave-2
    ports:
      - 6381:6379
    restart: always
    depends_on:
      - redis-server-master
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./redis-slave2.conf:/usr/local/etc/redis/redis.conf
      - ./data/redis-slave-2:/data
    sysctls:
      net.core.somaxconn: '511'
    command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
    networks:
      hx_net:
        ipv4_address: 10.10.10.3
   # 从节点3的容器
  redis-server-slave-3:
    image: redis
    container_name: redis-server-slave-3
    ports:
      - 6382:6379
    restart: always
    depends_on:
      - redis-server-master
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./redis-slave3.conf:/usr/local/etc/redis/redis.conf
      - ./data/redis-slave-3:/data
    sysctls:
      net.core.somaxconn: '511'
    command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
    networks:
      hx_net:
        ipv4_address: 10.10.10.4

  redis-server-sentinel-1:
    image: redis
    container_name: redis-server-sentinel-1
    ports:
      - "6383:26379"
    restart: always
    depends_on:
      - redis-server-master
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./redis-sentinel1.conf:/usr/local/etc/redis/sentinel.conf
    sysctls:
      net.core.somaxconn: '511'
    command: ["redis-sentinel","/usr/local/etc/redis/sentinel.conf"]
    networks:
      hx_net:
        ipv4_address: 10.10.10.5
  redis-server-sentinel-2:
    image: redis
    container_name: redis-server-sentinel-2
    ports:
      - "6384:26379"
    restart: always
    depends_on:
      - redis-server-master
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./redis-sentinel2.conf:/usr/local/etc/redis/sentinel.conf
    command: ["redis-sentinel","/usr/local/etc/redis/sentinel.conf"]
    sysctls:
      net.core.somaxconn: '511'
    networks:
      hx_net:
        ipv4_address: 10.10.10.6
  redis-server-sentinel-3:
    image: redis
    container_name: redis-server-sentinel-3
    ports:
      - "6385:26379"
    restart: always
    depends_on:
      - redis-server-master
    environment:
      TZ: "Asia/Shanghai"
    volumes:
      - ./redis-sentinel3.conf:/usr/local/etc/redis/sentinel.conf
    sysctls:
      net.core.somaxconn: '511'
    command: ["redis-sentinel","/usr/local/etc/redis/sentinel.conf"]
    networks:
      hx_net:
        ipv4_address: 10.10.10.7
networks:
    hx_net:
      driver: bridge
      ipam:
        config:
          - subnet: 10.10.10.0/16

~~~

2、编辑master的配置文件redis-master.conf
~~~
bind 10.10.10.1

# 启用保护模式
# 即在没有使用bind指令绑定具体地址时
# 或在没有设定密码时
# Redis将拒绝来自外部的连接
protected-mode yes

# 监听端口
port 6379

# 启动时不打印logo
# 这个不重要，想看logo就打开它
always-show-logo no

# 设定master的密码认证
requirepass "redis"

# 禁用KEYS命令
# 一方面 KEYS * 命令可以列出所有的键，会影响数据安全
# 另一方面 KEYS 命令会阻塞数据库，在数据库中存储了大量数据时，该命令会消耗很长时间
# 期间对Redis的访问也会被阻塞，而当锁释放的一瞬间，大量请求涌入Redis，会造成Redis直接崩溃
rename-command KEYS ""

dir "/data"

# 为了能够在master断开之后重新连接成为集群中的slave，就需要配置下集群的密码
masterauth "redis"

~~~

3、编辑slave1的配置文件 redis-slave1.conf
~~~
bind 10.10.10.2

# 启用保护模式
# 即在没有使用bind指令绑定具体地址时
# 或在没有设定密码时
# Redis将拒绝来自外部的连接
protected-mode yes

# 监听端口
port 6379

# 启动时不打印logo
# 这个不重要，想看logo就打开它
always-show-logo no

# 设定密码认证
requirepass "redis"

# 禁用KEYS命令
# 一方面 KEYS * 命令可以列出所有的键，会影响数据安全
# 另一方面 KEYS 命令会阻塞数据库，在数据库中存储了大量数据时，该命令会消耗很长时间
# 期间对Redis的访问也会被阻塞，而当锁释放的一瞬间，大量请求涌入Redis，会造成Redis直接崩溃
rename-command KEYS ""

# 此外还应禁止 FLUSHALL 和 FLUSHDB 命令
# 这两个命令会清空数据，并且不会失败

# 配置master节点信息
# 格式：
# slaveof <masterip> <masterport>
# 此处masterip所指定的redis-server-master是运行master节点的容器名
# Docker容器间可以使用容器名代替实际的IP地址来通信
replicaof 10.10.10.1 6379

# 设定连接主节点所使用的密码
masterauth "redis"
dir "/data"

~~~

4、编辑slave2的配置文件 redis-slave2.conf
~~~
bind 10.10.10.3

# 启用保护模式
# 即在没有使用bind指令绑定具体地址时
# 或在没有设定密码时
# Redis将拒绝来自外部的连接
protected-mode yes

# 监听端口
port 6379

# 启动时不打印logo
# 这个不重要，想看logo就打开它
always-show-logo no

# 设定密码认证
requirepass "redis"

# 禁用KEYS命令
# 一方面 KEYS * 命令可以列出所有的键，会影响数据安全
# 另一方面 KEYS 命令会阻塞数据库，在数据库中存储了大量数据时，该命令会消耗很长时间
# 期间对Redis的访问也会被阻塞，而当锁释放的一瞬间，大量请求涌入Redis，会造成Redis直接崩溃
rename-command KEYS ""

# 此外还应禁止 FLUSHALL 和 FLUSHDB 命令
# 这两个命令会清空数据，并且不会失败

# 配置master节点信息
# 格式：
#slaveof <masterip> <masterport>
# 此处masterip所指定的redis-server-master是运行master节点的容器名
# Docker容器间可以使用容器名代替实际的IP地址来通信
replicaof 10.10.10.1 6379

# 设定连接主节点所使用的密码
masterauth "redis"
dir "/data"

~~~
5、编辑slave3的配置文件 redis-slave3.conf
~~~
bind 10.10.10.4

# 启用保护模式
# 即在没有使用bind指令绑定具体地址时
# 或在没有设定密码时
# Redis将拒绝来自外部的连接
protected-mode yes

# 监听端口
port 6379

# 启动时不打印logo
# 这个不重要，想看logo就打开它
always-show-logo no

# 设定密码认证
requirepass "redis"

# 禁用KEYS命令
# 一方面 KEYS * 命令可以列出所有的键，会影响数据安全
# 另一方面 KEYS 命令会阻塞数据库，在数据库中存储了大量数据时，该命令会消耗很长时间
# 期间对Redis的访问也会被阻塞，而当锁释放的一瞬间，大量请求涌入Redis，会造成Redis直接崩溃
rename-command KEYS ""

# 此外还应禁止 FLUSHALL 和 FLUSHDB 命令
# 这两个命令会清空数据，并且不会失败

# 配置master节点信息
# 格式：
#slaveof <masterip> <masterport>
# 此处masterip所指定的redis-server-master是运行master节点的容器名
# Docker容器间可以使用容器名代替实际的IP地址来通信
replicaof 10.10.10.1 6379

# 设定连接主节点所使用的密码
masterauth "redis"
dir "/data"
~~~

6、编辑sentinel1的配置文件redis-sentinel1.conf
~~~
bind 10.10.10.5
protected-mode yes
port 26379
sentinel myid 0a353690ac056095f3d33671d3f3b6fd316ec9be
sentinel deny-scripts-reconfig yes
sentinel monitor mymaster 10.10.10.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel auth-pass mymaster redis
dir "/data"
~~~
7、编辑sentinel2的配置文件redis-sentinel2.conf

~~~
bind 10.10.10.6
protected-mode yes
port 26379
sentinel myid be47a103d66f41f79c07503db4243f7cf4e2217e
sentinel deny-scripts-reconfig yes
sentinel monitor mymaster 10.10.10.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel auth-pass mymaster redis
dir "/data"
~~~
8、编辑sentinel3的配置文件redis-sentinel3.conf
~~~
bind 10.10.10.7
protected-mode yes
port 26379
sentinel myid 6556d69081a155942a3505aaa37f5085acf88fc4
sentinel deny-scripts-reconfig yes
sentinel monitor mymaster 10.10.10.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel auth-pass mymaster redis
dir "/data"

~~~

9、docker-compose up 启动
~~~
[root@localhost redis-cluser]# docker-compose up
Creating network "rediscluser_hx_net" with driver "bridge"
Creating redis-server-sentinel-1 ... done
Creating redis-server-slave-3 ... 
Creating redis-server-slave-2 ... 
Creating redis-server-slave-1 ... 
Creating redis-server-sentinel-1 ... 
Creating redis-server-sentinel-2 ... 
Creating redis-server-sentinel-3 ... 
Attaching to redis-server-master, redis-server-slave-2, redis-server-slave-3, redis-server-sentinel-2, redis-server-slave-1, redis-server-sentinel-3, redis-server-sentinel-1
redis-server-master        | 1:C 01 Feb 2020 20:23:09.606 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-server-master        | 1:C 01 Feb 2020 20:23:09.606 # Redis version=5.0.7, bits=64, commit=00000000, modified=0, pid=1, just started
redis-server-master        | 1:C 01 Feb 2020 20:23:09.606 # Configuration loaded
redis-server-master        | 1:M 01 Feb 2020 20:23:09.607 * Running mode=standalone, port=6379.
redis-server-slave-2       | 1:C 01 Feb 2020 20:23:10.983 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-server-slave-2       | 1:C 01 Feb 2020 20:23:10.983 # Redis version=5.0.7, bits=64, commit=00000000, modified=0, pid=1, just started
redis-server-slave-2       | 1:C 01 Feb 2020 20:23:10.983 # Configuration loaded
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.985 * Running mode=standalone, port=6379.
redis-server-master        | 1:M 01 Feb 2020 20:23:09.608 # Server initialized
redis-server-master        | 1:M 01 Feb 2020 20:23:09.608 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
redis-server-master        | 1:M 01 Feb 2020 20:23:09.608 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
redis-server-master        | 1:M 01 Feb 2020 20:23:09.608 * Ready to accept connections
redis-server-master        | 1:M 01 Feb 2020 20:23:10.988 * Replica 10.10.10.3:6379 asks for synchronization
redis-server-master        | 1:M 01 Feb 2020 20:23:10.988 * Full resync requested by replica 10.10.10.3:6379
redis-server-master        | 1:M 01 Feb 2020 20:23:10.988 * Starting BGSAVE for SYNC with target: disk
redis-server-master        | 1:M 01 Feb 2020 20:23:10.988 * Background saving started by pid 19
redis-server-master        | 19:C 01 Feb 2020 20:23:10.990 * DB saved on disk
redis-server-master        | 19:C 01 Feb 2020 20:23:10.990 * RDB: 0 MB of memory used by copy-on-write
redis-server-master        | 1:M 01 Feb 2020 20:23:11.016 * Background saving terminated with success
redis-server-master        | 1:M 01 Feb 2020 20:23:11.016 * Synchronization with replica 10.10.10.3:6379 succeeded
redis-server-master        | 1:M 01 Feb 2020 20:23:11.155 * Replica 10.10.10.4:6379 asks for synchronization
redis-server-master        | 1:M 01 Feb 2020 20:23:11.155 * Full resync requested by replica 10.10.10.4:6379
redis-server-master        | 1:M 01 Feb 2020 20:23:11.155 * Starting BGSAVE for SYNC with target: disk
redis-server-master        | 1:M 01 Feb 2020 20:23:11.155 * Background saving started by pid 20
redis-server-master        | 20:C 01 Feb 2020 20:23:11.157 * DB saved on disk
redis-server-master        | 20:C 01 Feb 2020 20:23:11.158 * RDB: 0 MB of memory used by copy-on-write
redis-server-master        | 1:M 01 Feb 2020 20:23:11.204 * Replica 10.10.10.2:6379 asks for synchronization
redis-server-master        | 1:M 01 Feb 2020 20:23:11.205 * Full resync requested by replica 10.10.10.2:6379
redis-server-master        | 1:M 01 Feb 2020 20:23:11.205 * Waiting for end of BGSAVE for SYNC
redis-server-master        | 1:M 01 Feb 2020 20:23:11.216 * Background saving terminated with success
redis-server-master        | 1:M 01 Feb 2020 20:23:11.216 * Synchronization with replica 10.10.10.4:6379 succeeded
redis-server-master        | 1:M 01 Feb 2020 20:23:11.217 * Synchronization with replica 10.10.10.2:6379 succeeded
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.985 # Server initialized
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.985 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.985 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.985 * Ready to accept connections
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.985 * Connecting to MASTER 10.10.10.1:6379
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.986 * MASTER <-> REPLICA sync started
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.986 * Non blocking connect for SYNC fired the event.
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.987 * Master replied to PING, replication can continue...
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.988 * Partial resynchronization not possible (no cached master)
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:10.989 * Full resync from master: b629d758c97bf4d1ceaa4e552f18bcb41bbbec0d:0
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:11.016 * MASTER <-> REPLICA sync: receiving 175 bytes from master
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:11.016 * MASTER <-> REPLICA sync: Flushing old data
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:11.016 * MASTER <-> REPLICA sync: Loading DB in memory
redis-server-slave-2       | 1:S 01 Feb 2020 20:23:11.016 * MASTER <-> REPLICA sync: Finished with success
redis-server-slave-3       | 1:C 01 Feb 2020 20:23:11.150 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-server-slave-3       | 1:C 01 Feb 2020 20:23:11.150 # Redis version=5.0.7, bits=64, commit=00000000, modified=0, pid=1, just started
redis-server-slave-3       | 1:C 01 Feb 2020 20:23:11.150 # Configuration loaded
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.152 * Running mode=standalone, port=6379.
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.152 # Server initialized
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.152 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.152 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.153 * Ready to accept connections
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.153 * Connecting to MASTER 10.10.10.1:6379
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.154 * MASTER <-> REPLICA sync started
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.154 * Non blocking connect for SYNC fired the event.
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.154 * Master replied to PING, replication can continue...
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.155 * Partial resynchronization not possible (no cached master)
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.157 * Full resync from master: b629d758c97bf4d1ceaa4e552f18bcb41bbbec0d:0
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.217 * MASTER <-> REPLICA sync: receiving 175 bytes from master
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.217 * MASTER <-> REPLICA sync: Flushing old data
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.217 * MASTER <-> REPLICA sync: Loading DB in memory
redis-server-slave-3       | 1:S 01 Feb 2020 20:23:11.217 * MASTER <-> REPLICA sync: Finished with success
redis-server-sentinel-2    | 1:X 01 Feb 2020 20:23:11.138 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-server-sentinel-2    | 1:X 01 Feb 2020 20:23:11.138 # Redis version=5.0.7, bits=64, commit=00000000, modified=0, pid=1, just started
redis-server-sentinel-2    | 1:X 01 Feb 2020 20:23:11.138 # Configuration loaded
redis-server-sentinel-2    | 1:X 01 Feb 2020 20:23:11.139 * Running mode=sentinel, port=26379.
redis-server-sentinel-2    | 1:X 01 Feb 2020 20:23:11.140 # Sentinel ID is be47a103d66f41f79c07503db4243f7cf4e2217e
redis-server-sentinel-2    | 1:X 01 Feb 2020 20:23:11.140 # +monitor master mymaster 10.10.10.1 6379 quorum 2
redis-server-slave-1       | 1:C 01 Feb 2020 20:23:11.201 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-server-slave-1       | 1:C 01 Feb 2020 20:23:11.201 # Redis version=5.0.7, bits=64, commit=00000000, modified=0, pid=1, just started
redis-server-slave-1       | 1:C 01 Feb 2020 20:23:11.201 # Configuration loaded
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.202 * Running mode=standalone, port=6379.
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.203 # Server initialized
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.203 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.203 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.203 * Ready to accept connections
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.203 * Connecting to MASTER 10.10.10.1:6379
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.203 * MASTER <-> REPLICA sync started
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.204 * Non blocking connect for SYNC fired the event.
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.204 * Master replied to PING, replication can continue...
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.204 * Partial resynchronization not possible (no cached master)
redis-server-sentinel-1    | 1:X 01 Feb 2020 20:23:11.243 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-server-sentinel-3    | 1:X 01 Feb 2020 20:23:11.245 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-server-sentinel-3    | 1:X 01 Feb 2020 20:23:11.245 # Redis version=5.0.7, bits=64, commit=00000000, modified=0, pid=1, just started
redis-server-sentinel-3    | 1:X 01 Feb 2020 20:23:11.245 # Configuration loaded
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.205 * Full resync from master: b629d758c97bf4d1ceaa4e552f18bcb41bbbec0d:0
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.217 * MASTER <-> REPLICA sync: receiving 175 bytes from master
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.217 * MASTER <-> REPLICA sync: Flushing old data
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.217 * MASTER <-> REPLICA sync: Loading DB in memory
redis-server-slave-1       | 1:S 01 Feb 2020 20:23:11.217 * MASTER <-> REPLICA sync: Finished with success
redis-server-sentinel-1    | 1:X 01 Feb 2020 20:23:11.243 # Redis version=5.0.7, bits=64, commit=00000000, modified=0, pid=1, just started
redis-server-sentinel-1    | 1:X 01 Feb 2020 20:23:11.243 # Configuration loaded
redis-server-sentinel-1    | 1:X 01 Feb 2020 20:23:11.245 * Running mode=sentinel, port=26379.
redis-server-sentinel-1    | 1:X 01 Feb 2020 20:23:11.247 # Sentinel ID is 0a353690ac056095f3d33671d3f3b6fd316ec9be
redis-server-sentinel-1    | 1:X 01 Feb 2020 20:23:11.247 # +monitor master mymaster 10.10.10.1 6379 quorum 2
redis-server-sentinel-3    | 1:X 01 Feb 2020 20:23:11.247 * Running mode=sentinel, port=26379.
redis-server-sentinel-3    | 1:X 01 Feb 2020 20:23:11.247 # Sentinel ID is 6556d69081a155942a3505aaa37f5085acf88fc4
redis-server-sentinel-3    | 1:X 01 Feb 2020 20:23:11.247 # +monitor master mymaster 10.10.10.1 6379 quorum 2


~~~

###测试一下同步情况
1、使用redis客户端连上四个redis服务
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cbdf1c9660abc84f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、在master上添加一个kv
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5e9ffd31a1802bfc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、查看slave1和slave2、slave3
![image.png](https://upload-images.jianshu.io/upload_images/13965490-77b2ed775304f1f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

同步成功！！
查看生成的文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cf4bb23717e87eb3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###验证主从切换
当master意外宕机，sentinel哨兵会在slave中进行选举

1、停掉master
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7e82d6373ac94d9e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
2、查看sentinel-1的日志
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f4e9a4be62bc5679.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
3、给slave1添加kv
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4a05ef0449b8b2b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
4、查看slave2、slave3是否同步到
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2c196433730d9fb0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
同步成功！主从切换成功！！！
5、查看配置文件更改情况
- 被升级成master的slave1 的配置 redis-slave1.conf 
 可以看出 replicaof 10.10.10.1 6379 一行配置被redis自己删除了，证明它自己要当master了就不需要再指向之前的master

~~~
[root@localhost redis-cluser]# vi redis-slave1.conf 

bind 10.10.10.2

# 启用保护模式
# 即在没有使用bind指令绑定具体地址时
# 或在没有设定密码时
# Redis将拒绝来自外部的连接
protected-mode yes

# 监听端口
port 6379

# 启动时不打印logo
# 这个不重要，想看logo就打开它
always-show-logo no

# 设定密码认证
requirepass "redis"

# 禁用KEYS命令
# 一方面 KEYS * 命令可以列出所有的键，会影响数据安全
# 另一方面 KEYS 命令会阻塞数据库，在数据库中存储了大量数据时，该命令会消耗很长时间
# 期间对Redis的访问也会被阻塞，而当锁释放的一瞬间，大量请求涌入Redis，会造成Redis直接崩溃
rename-command KEYS ""

# 此外还应禁止 FLUSHALL 和 FLUSHDB 命令
# 这两个命令会清空数据，并且不会失败

# 配置master节点信息
# 格式：
# slaveof <masterip> <masterport>
# 此处masterip所指定的redis-server-master是运行master节点的容器名
# Docker容器间可以使用容器名代替实际的IP地址来通信

# 设定连接主节点所使用的密码
masterauth "redis"
dir "/data"

~~~

- sentinel1的配置 redis-sentinel1.conf
生成了很多行其它命令；sentinel monitor mymaster 10.10.10.2 6379 2指向的master端口改成了10.10.10.2 salve1的ip
~~~
[root@localhost redis-cluser]# vi redis-sentinel1.conf

bind 10.10.10.5
protected-mode yes
port 26379
sentinel myid 0a353690ac056095f3d33671d3f3b6fd316ec9be
sentinel deny-scripts-reconfig yes
sentinel monitor mymaster 10.10.10.2 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel auth-pass mymaster redis
dir "/data"

# Generated by CONFIG REWRITE
sentinel config-epoch mymaster 1
sentinel leader-epoch mymaster 1
sentinel known-replica mymaster 10.10.10.1 6379
sentinel known-replica mymaster 10.10.10.4 6379
sentinel known-replica mymaster 10.10.10.3 6379
sentinel known-sentinel mymaster 10.10.10.7 26379 6556d69081a155942a3505aaa37f5085acf88fc4
sentinel known-sentinel mymaster 10.10.10.6 26379 be47a103d66f41f79c07503db4243f7cf4e2217e
sentinel current-epoch 1
~                                                                                
~~~
- redis-slave2.conf的配置
replicaof 10.10.10.2 6379被redis改成了slave1的ip10.10.10.2
~~~
[root@localhost redis-cluser]# vi redis-slave2.conf

bind 10.10.10.3

# 启用保护模式
# 即在没有使用bind指令绑定具体地址时
# 或在没有设定密码时
# Redis将拒绝来自外部的连接
protected-mode yes

# 监听端口
port 6379

# 启动时不打印logo
# 这个不重要，想看logo就打开它
always-show-logo no

# 设定密码认证
requirepass "redis"

# 禁用KEYS命令
# 一方面 KEYS * 命令可以列出所有的键，会影响数据安全
# 另一方面 KEYS 命令会阻塞数据库，在数据库中存储了大量数据时，该命令会消耗很长时间
# 期间对Redis的访问也会被阻塞，而当锁释放的一瞬间，大量请求涌入Redis，会造成Redis直接崩溃
rename-command KEYS ""

# 此外还应禁止 FLUSHALL 和 FLUSHDB 命令
# 这两个命令会清空数据，并且不会失败

# 配置master节点信息
# 格式：
#slaveof <masterip> <masterport>
# 此处masterip所指定的redis-server-master是运行master节点的容器名
# Docker容器间可以使用容器名代替实际的IP地址来通信
replicaof 10.10.10.2 6379

# 设定连接主节点所使用的密码
masterauth "redis"
dir "/data"


~~~
###验证重启master，之前的master是否会当做slave
1、重启master
![image.png](https://upload-images.jianshu.io/upload_images/13965490-128fe05351ab3ace.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、查看sentinel1的日志
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c947b33b5b0669b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
3、查看master（10.10.10.1）的日志
![image.png](https://upload-images.jianshu.io/upload_images/13965490-233b5bcc9b635407.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
现在的master是slave1的从机
4、给salve1添加kv，看看master能不能同步的到
![image.png](https://upload-images.jianshu.io/upload_images/13965490-53a60ee202ed76ed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

同步成功！验证重启master成为从机是ok的！！！

5、查看master的配置文件被redis修改成什么样了
可以看出生成了配置 replicaof 10.10.10.2 6379
指向了slave2

~~~
[root@localhost redis-cluser]# vi redis-master.conf

bind 10.10.10.1

# 启用保护模式
# 即在没有使用bind指令绑定具体地址时
# 或在没有设定密码时
# Redis将拒绝来自外部的连接
protected-mode yes

# 监听端口
port 6379

# 启动时不打印logo
# 这个不重要，想看logo就打开它
always-show-logo no

# 设定master的密码认证
requirepass "redis"

# 禁用KEYS命令
# 一方面 KEYS * 命令可以列出所有的键，会影响数据安全
# 另一方面 KEYS 命令会阻塞数据库，在数据库中存储了大量数据时，该命令会消耗很长时间
# 期间对Redis的访问也会被阻塞，而当锁释放的一瞬间，大量请求涌入Redis，会造成Redis直接崩溃
rename-command KEYS ""

dir "/data"

# 为了能够在master断开之后重新连接成为集群中的slave，就需要配置下集群的密码
masterauth "redis"
# Generated by CONFIG REWRITE
replicaof 10.10.10.2 6379

~~~


###查看集群信息
- 进入容器 
~~~
docker exec -it redis-server-sentinel-1 bash
~~~
- 登录sentinel1
~~~
  redis-cli -p 26379 -h 10.10.10.6 
~~~
- 查看集群状态 
~~~
sentinel master mymaster
~~~
~~~
10.10.10.6:26379> sentinel master mymaster
 1) "name"
 2) "mymaster"
 3) "ip"
 4) "10.10.10.2"
 5) "port"
 6) "6379"
 7) "runid"
 8) "46c19ffd38b061386e514f7ea40bb035e0f55117"
 9) "flags"
10) "master"
11) "link-pending-commands"
12) "0"
13) "link-refcount"
14) "1"
15) "last-ping-sent"
16) "0"
17) "last-ok-ping-reply"
18) "32"
19) "last-ping-reply"
20) "32"
21) "down-after-milliseconds"
22) "5000"
23) "info-refresh"
24) "5429"
25) "role-reported"
26) "master"
27) "role-reported-time"
28) "1832078"
29) "config-epoch"
30) "1"
31) "num-slaves"
32) "3"
33) "num-other-sentinels"
34) "2"
35) "quorum"
36) "2"
37) "failover-timeout"
38) "180000"
39) "parallel-syncs"
40) "1"

~~~

###完整项目
[https://github.com/suoyiguke/docker-compose-redis-cluser](https://github.com/suoyiguke/docker-compose-redis-cluser)
感兴趣的话点个star吧~~

