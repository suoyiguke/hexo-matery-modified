---
title: mysql-基于docker-compose配置主从复制（一主一从）.md
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
title: mysql-基于docker-compose配置主从复制（一主一从）.md
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
###MySQL主从复制有那些好处
1、做数据的热备，作为后备数据库，主数据库服务器故障后，可切换到从数据库继续工作，避免数据丢失。
2、架构的扩展。业务量越来越大，I/O访问频率过高，单机无法满足，此时做多库的存储，降低磁盘I/O访问的频率，提高单个机器的I/O性能。
3、读写分离，使数据库能支撑更大的并发。


###MySQL复制过程

- master将改变记录到二进制日志（binary log）。这些记录过程叫做二进制日志事件，binary log events；

- slave将master的binary log events拷贝到它的中继日志（relay log）；

- slave重做中继日志中的事件，将改变应用到自己的数据库中。MySQL复制是异步的且串行化的

###操作之前需要注意的地方
- master和slave都在一台linux上，IP是192.168.10.11
- master 端口为33065；slave端口为33066
- 工程目录是 /data/docker/mysql
- 默认创建了test库
- 两个mysql的账号密码均为 root
- 我这里使用的mysql版本是mysql5.7
###搭建过程
1、目录结构
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3dc3659e7013fa2f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-24a6dd50d3c2bb96.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、编辑 docker-compose.yml
~~~
version: '2'
services:
 mysql-master:
   image: "docker.io/mysql:5.7"
   environment:
    - "MYSQL_ROOT_PASSWORD=root"
    - "MYSQL_DATABASE=test"
   volumes:
    - "./master/data:/var/lib/mysql"
    - "./master/my.cnf:/etc/mysql/my.cnf"
   links:
    - mysql-slave
   ports:
    - "33065:3306"
   restart: always
   hostname: mysql-master
 mysql-slave:
   image: "docker.io/mysql:5.7"
   environment:
    - "MYSQL_ROOT_PASSWORD=root"
    - "MYSQL_DATABASE=test"
   volumes:
    - "./slave/data:/var/lib/mysql"
    - "./slave/my.cnf:/etc/mysql/my.cnf"
   ports:
    - "33066:3306"
   restart: always
   hostname: mysql-slave

~~~
3、编辑master的配置文件
vi /data/docker/mysql/master/my.cnf
> binlog-do-db=test 指定需要主从备份的数据库为test库
~~~
[mysqld]
## server_id，一般设置为IP，注意要唯一
server_id=1
log_bin=mysql-bin
## 需要主从复制的数据库
binlog-do-db=test
## 复制过滤：也就是指定哪个数据库不用同步（mysql库一般不同步）
binlog-ignore-db=mysql
## 为每个session分配的内存，在事务过程中用来存储二进制日志的缓存
binlog_cache_size=1M
## 主从复制的格式（mixed,statement,row，默认格式是statement。建议是设置为row，主从复制时数据更加能够统一）
binlog_format=row
## 二进制日志自动删除/过期的天数。默认值为0，表示不自动删除。
expire_logs_days=7
## 跳过主从复制中遇到的所有错误或指定类型的错误，避免slave端复制中断。
## 如：1062错误是指一些主键重复，1032错误是因为主从数据库数据不一致
slave_skip_errors=1062
~~~
4、编辑slave的配置文件
vi /data/docker/mysql/slave/my.cnf
> binlog-do-db=test 指定需要主从备份的数据库为test库

~~~
[mysqld]
## 设置server_id，一般设置为IP，注意要唯一
server_id=2
## 需要主从复制的数据库
replicate-do-db=test
## 复制过滤：也就是指定哪个数据库不用同步（mysql库一般不同步）
binlog-ignore-db=mysql
## 开启二进制日志功能，以备Slave作为其它Slave的Master时使用
log_bin = mysql-bin
## 为每个session 分配的内存，在事务过程中用来存储二进制日志的缓存
binlog_cache_size=1M
## 主从复制的格式（mixed,statement,row，默认格式是statement）
binlog_format=row
## 二进制日志自动删除/过期的天数。默认值为0，表示不自动删除。
expire_logs_days=7
## 跳过主从复制中遇到的所有错误或指定类型的错误，避免slave端复制中断。
## 如：1062错误是指一些主键重复，1032错误是因为主从数据库数据不一致
slave_skip_errors=1062
## relay_log配置中继日志
relay_log=replicas-mysql-relay-bin
## log_slave_updates表示slave将复制事件写进自己的二进制日志
log_slave_updates=1
## 防止改变数据(除了特殊的线程)
read_only=1

~~~

5、设置目录文件权限
在/data/docker/mysql下执行授权
~~~
chmod 644 -R *
~~~

6、启动mysql服务

~~~
docker-compose up
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9eab34b4a50821de.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
启动成功！

7、在master里准备数据，创建test表；并插入三条数据
~~~


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test`  (
  `id` int(11) NOT NULL COMMENT 'id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of test
-- ----------------------------
INSERT INTO `test` VALUES (1);
INSERT INTO `test` VALUES (2);
INSERT INTO `test` VALUES (3);

SET FOREIGN_KEY_CHECKS = 1;

~~~
8、在master中查看binlog的版本参数
~~~
show master status;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bc48a249628bfbdb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
File  和  Position两个参数会在下面用到

9、在slave中执行命令
~~~
change master to master_host='192.168.10.11',master_port=33065,master_user='root',master_password='root',master_log_file='mysql-bin.000003',master_log_pos=1259;
~~~
- master_host master的ip
- master_port master的端口
- master_user master 用户名
- master_password master 密码
- master_log_file master中此时的File  参数
- master_log_pos master中此时的Position 参数

salve中启动主从复制
~~~
start slave;
~~~



查看从机的复制状态
~~~
show slave status;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ed498778700366e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
Waiting for master to send event 即等待主服务器发送事件；现在到master里新增一条记录
下面两个参数都是YES，则说明主从配置成功！Slave_IO_Running:Yes和Slave_SQL_Running:Yes
![image.png](https://upload-images.jianshu.io/upload_images/13965490-afcfa3a50687e081.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
INSERT INTO `test`.`test`(`id`) VALUES (4);
~~~
slave再次执行
~~~
show slave status;
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ead5b0ac90247b63.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
提示slave中test表不存在，难道mysql在主从复制过程中只是同步变更，而之前master中已经存在的表结构和表数据不会被同步？那么就先将master中的表结构和数据一起复制到slave中，然后进行insert：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d1b7e12b138f5cf8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
同步成功！！

10、同步停止方式
slave 中执行
~~~
stop slave;
~~~

###注意事项
1、在停止一次主从复制后如果需要再次启用，需要再次到master中执行show master status; 生成最新的File  和  Position
2、开启同步后，master中已经存在的表结构和表数据不会被同步到slave中；将master中的数据迁移至slave，实现master和slave一致之后就可以实现同步了。那么如何保证 master复制数据到slave之后、 slave开启同步之前的一段时间里的数据也被同步到？

3、binlog格式binlog_format请使用 row类型而不是statement或者mixed，虽然基于行的binlog占用空间会比较大，但是这种方式会屏蔽掉很多问题的

4、expire_logs_days 指定二进制日志自动删除/过期的天数。默认值为0，表示不自动删除。指定7就是7天后删除

5、slave机需要配置中继日志

~~~
[mysqld]
## relay_log配置中继日志
relay_log=replicas-mysql-relay-bin
~~~

6、master和slave的server_id必须不同，如果省略server-id（而且不能设置为0，server-id的默认值就是0），则主服务器拒绝来自从服务器的任何连接。
