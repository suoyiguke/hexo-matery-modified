---
title: mysql-参数调优（13）之-其他参数.md
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
title: mysql-参数调优（13）之-其他参数.md
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
**SKIP_NAME_RESOLVE**
这一项不得不提及，因为仍然有很多人没有添加这一项。你应该添加skip_name_resolve来避免连接时DNS解析。大多数情况下你更改这个会没有什么感觉，因为大多数情况下DNS服务器解析会非常快。不过当DNS服务器失败时，它会出现在你服务器上出现“unauthenticated connections” ，而就是为什么所有的请求都突然开始慢下来了。所以不要等到这种事情发生才更改。现在添加这个变量并且避免基于主机名的授权。

配置修改
~~~
[mysqld]
SKIP_NAME_RESOLVE
~~~

**max_allowed_packet**

insert 插入db中数据太大，或者数据条目太多。会出现这个问题
> Cause: com.mysql.jdbc.PacketTooBigException: Packet for query is too large (8479448 

我们可以修改max_allowed_packet 配置参数。max_allowed_packet 默认是4M；最大值1024M;


会话修改
~~~
SELECT  @@max_allowed_packet
SHOW VARIABLES LIKE '%max_allowed_packet%'
SET GLOBAL max_allowed_packet = 1073741824 -- 1024M
 ~~~

配置修改
~~~
[mysqld]
max_allowed_packet = 1024M
~~~

**innodb_strict_mode**

推荐设置：1
作用：必须开启，没得选择，1，为什么？
从MySQL5.5.X版本开始，你可以开启InnoDB严格检查模式，尤其采用了页数据压缩功能后，最好是开启该功能。开启此功能后，当创建表（CREATE TABLE）、更改表（ALTER TABLE）和创建索引（CREATE INDEX）语句时，如果写法有错误，不会有警告信息，而是直接抛出错误，这样就可直接将问题扼杀在摇篮里。
如果不配的后果：
如果不配碰到开发或者非专业的dba会把旧ddl语句生效在5.7内，另外一个问题就是ddl语句出错时报错不明显，这会影响到“主从复制”，至于dll为什么会影响到主从复制，我们后面会在“slave_skip_errors = ddl_exist_errors”中详细解说。
配置实例：
~~~
[mysqld]
innodb_strict_mode = 1
~~~
**innodb_print_all_deadlocks**

默认0 关闭；推荐设置：1
作用： 当mysql 数据库发生死锁时， innodb status 里面会记录最后一次死锁的相关信息，但mysql 错误日志里面不会记录死锁相关信息，要想记录，启动 innodb_print_all_deadlocks 参数 。
如果不配的后果：不会记录该信息。

配置实例：
~~~
[mysqld]
innodb_print_all_deadlocks = 1
~~~


**innodb_large_prefix**
推荐设置：1
作用：如果你的客户端和服务端的字符集设成了utf8mb4，那么我们需要把这个开关开启，为什么呢？mysql在5.6之前一直都是单列索引限制767，起因是256×3-1。这个3是字符最大占用空间（utf8）。但是在5.6以后，开始支持4个字节的uutf8。255×4>767, 于是增加了这个参数。这个参数默认值是OFF。当改为ON时，允许列索引最大达到3072.
在mysql5.6中这个开关叫on, off。而在5.7中叫0和1，由于我们前面设置了utf8mb4，因此这边我们必须把这个参数开启。
如果不配的后果：不配会有问题，特别是索引会无效、或者不是走最优计划，如果你的字符集是utf8mb4，那么这个值必开启。

配置实例：
~~~
[mysqld]
innodb_large_prefix = 1
~~~

**character_set_client**

推荐设置：utf8mb4
作用：字符集设定，如果前台有连social mobile application一类包括wechat，并且允许有使用emoji表情的，请开启成utf8mb4
如果不配的后果：mysql不支持前端app存表情等字符
配置实例：
~~~
[client]
character_set_client=utf8mb4
~~~


**bind_address**

推荐设置：0.0.0.0
作用：
除非有特殊需要，我们会限制只允许mysql实例被某一个ip方问，不支持多个，生产上都为：0.0.0.0然后使用防火墙策略来控制。
如果不配的后果：默认不允许远程登录

配置实例：
~~~
[mysqld]
bind_address=0.0.0.0
~~~

**autocommit**

推荐设置：1
作用：生产上开启成1，如果你开启的是0会有一个这样的情况：a运行一条insert语句，并未作commit;b去做查询此时b是查询不到的。这种操作一般用于在写store procedure时用到。

如果不配的后果：如果在系统的my.cnf层面把它设成了0，如果在使用时（99%情况是用的1）时，你想要用root在生产运行时把它设成set autocommit = 1都开启不了。而如果你在一开始就把它设置成1，那么当碰到某些特殊场景特别是写store procedure时需要把它设成0时，你是可以手动临时把某一个session给开在0的。

配置实例：
~~~
[mysqld]
autocommit = 1
~~~



**max_connections**



推荐设置：20,000。
作用：最大连接数。最大值100000，如果需要超过这个值的连接数。 最大连接数max_connections值受系统os最大打开连接数限制，因此我们需要做以下2步操作：
1）在 /etc/security/limits.conf 底部增加2行
~~~
mysql hard nofile 65535
mysql soft nofile 65535
~~~
2）在/usr/lib/systemd/system/mysqld.service（视如何安装mysql所决定，用编译安装和yum安装会产生path路径不同。）文件最后添加：
~~~
LimitNOFILE=65535
LimitNPROC=65535
~~~
刷新
~~~
$ systemctl daemon-reload
$ systemctl restart mysqld.service
~~~
如不生效重服务器。如果不配的后果：默认只有150
配置实例：
~~~
[mysqld]
max_connections = 20000
~~~

**max_connect_errors**
推荐设置：生产上开启成10次，开发测试上使用默认即不设。
max_connect_errors是一个MySQL中与安全有关的计数器值，它负责阻止过多尝试失败的客户端以防止暴力破解密码的情况。如果需要设置此数值，手动添加。当此值设置为10时，意味着如果某一客户端尝试连接此MySQL服务器，但是失败（如密码错误等等）10次，则MySQL会无条件强制阻止此客户端连接。相关的登录错误信息会记录到performance_schema.host_cache表中。如果希望重置此计数器的值，则必须重启MySQL服务器或者执行
~~~
Mysql> FLUSH HOSTS;
~~~
当这一客户端成功连接一次MySQL服务器后，针对此客户端的max_connect_errors会清零。可以在防火墙上做策略限制某些ip的远程连接。
如果不配的后果：默认为100
配置实例：
~~~
[mysqld]
max_connect_errors =20000
~~~
**sql_mode**

不需要去设置，使用默认的，这块和性能无关。我们的中台中的sql如果碰到有sql报错，因该是在测试环境上就已经报了，它的作用是用来约束你sql的写法的，如果是一个从头开始开发的应用，我们比如说约束好都是ansi sql写法，对于一个产品，不要去做这种画蛇添足的做法。

**Interactive_timeout 和 wait_timeout**
interactive_timeout：交互式连接超时时间(mysqldump等工具的连接)
wait_timeout：非交互式连接超时时间，默认的连接mysql api程序,jdbc连接数据库等;

Interactive_timeout 推荐设置：600 10分钟

作用：单位为s，系统默认为：28800s即8小时。

1、在高并发的场景下这个timeout会缩短至3-5分钟。若不配置使用默认的8小时那么在mysql中会有大量sleep的连接，这些连接又被称为：`僵尸连接`。僵尸连接一多就会达到max_connections最大限制。你真正要用的时候就会抛：too many connection这样的错，因此对于长久不用的连接，我们一般要使用“踢出机制”。那么多久对于一个活动累的sql进行踢呢？我们说如果有一个长事务，它要执行1小时，我不知道这是不是属于正常？当然如果你设了太短，说1分钟就把它踢了，还真不一定踢的对。你有一条sql连着，10分钟不用，我就把它踢了，这也算正常。

应用端要有相应的validate sql一类的操作来keep alived。不过我更推荐使用”连接池内连接的生存周期（idleConnectionTestPeriod）”来做设置，把这个置设成小用mysql内的这两个值将会是最好，同时，idleConnectionTestPeriod会使用到异步的方式去做超时check。如c3p0中的：idleConnectionTestPeriod=true和testConnectionOnCheckin=false相当可靠。


2、传统行业应用不建议这个参数，不建议把这个参数改小，因为改小后很容易就会去创建新连接了这对数据库资源也是一种消耗而且还必须轮询发select 1来保证连接不被踢出。默认情况下8小时并不会出现问题。（8小时内都没有访问数据库这种情况应该很少吧？如果出现连接失效的问题那就只能去轮询发select 1了）



配置实例：
~~~
[mysqld]
interactive_timeout = 600
wait_timeout= 600
~~~

~~~
SET SESSION Interactive_timeout = 600
SET GLOBAL Interactive_timeout = 600
SET SESSION wait_timeout = 600
SET GLOBAL wait_timeout = 600
~~~

**read_buffer_size**
推荐设置：4194304
作用：这个值其实轻易是用不到的，因为，它只对2种场景的full table scan产生影响而不是所有的full table scan，同时从mysql5.6以后开始没有数据块多块读的功能,与是否设置 read_buffer_size参数无关。

应用场景：
1）SELECT INTO … OUTFILE ‘fileName‘
2）When filesort is used, during merge buffers and when merged results are written to a temporary file, then writes are buffered
一般保留默认:64k，保守作法是设置在1～4M，不过它的应用场景很有限，对于互联网场景真的不太用，我推荐设成4M
如果不配的后果：默认为64k
配置实例：
~~~
[mysqld]
read_buffer_size = 4194304
~~~





**innodb_file_format**
推荐设置：Barracuda 梭子鱼模式
作用：推荐使用Barracuda模式。它是启用表压缩用的，如：
~~~
CREATE TABLE `test_1` (
`x` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;
~~~
建完后可以通过：show table status like 'test_1';来查看是否已经启用了表压缩了。innodb_file_format有这么几种模式：
Antelope-羚羊模式，支持Redundant（冗余）、Compact（紧凑）模式
Barracuda-梭子鱼,是InnoDB Plugin支持的文件格式，在原来的基础上新增了两种数据表格式的支持：Dynamic 和 Compressed 因此我推荐使用：Barracude模式，因为它可以兼容其它数据模式。
它也可以在运行时动态改变：SET GLOBAL innodb_file_format_max = barracuda;
如果不配的后果：它默认使用的是叫“联合模式”，即不是棱子鱼也不是羚羊。
配置实例：
~~~
mysqld
innodb_file_format = Barracuda
innodb_file_format_max = Barracuda
~~~
这个参数必须和innodb_file_format参数一致，一定记住，要不然不生效。
