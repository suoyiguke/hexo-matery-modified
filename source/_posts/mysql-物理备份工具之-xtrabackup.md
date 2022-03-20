---
title: mysql-物理备份工具之-xtrabackup.md
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
title: mysql-物理备份工具之-xtrabackup.md
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
之前使用 mysqldump 备份的 https://www.jianshu.com/p/f34dc0a3c5ce  它是一种备份sql文件的逻辑备份。备份恢复速度慢而且文件体积也大。mysql可以通过xtrabackup 实现物理备份，备份 frm、idb文件

1、备份速度快，物理备份可靠
2、备份过程不会打断正在执行的事务（无需锁表）
3、能够基于压缩等功能节约磁盘空间和流量
4、自动备份校验
5、还原速度快
6、可以流传将备份传输到另外一台机器上
7、在不增加服务器负载的情况备份数据


>xtrabackup一定是安装在mysql服务器上的，因为使用它进行备份需要指定my.cnf文件

###官网安装最新版 8.0.4
https://www.percona.com/downloads/Percona-XtraBackup-LATEST/
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4fd5abdbd00364bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-8.0.4/binary/redhat/7/x86_64/percona-xtrabackup-80-8.0.4-1.el7.x86_64.rpm
yum localinstall percona-xtrabackup-80-8.0.4-1.el7.x86_64.rpm
~~~

~~~
[root@localhost xtrabackupdata]#  xtrabackup --version
xtrabackup: recognized server arguments: --datadir=/data/mysql/mysql-5.7.31-linux-glibc2.12-x86_64/data --log_bin=mysql-bin --server-id=1 
xtrabackup version 8.0.4 based on MySQL server 8.0.13 Linux (x86_64) (revision id: c2c0777)

~~~

几番周折尝试备份，发现不能支持5.7版本的mysql
~~~
xtrabackup --defaults-file=/etc/my.cnf --host=192.168.6.128 --user=root --password=Sgl20@14 --databases=iam --target-dir=/data/mysql/xtrabackupdata  --backup=true
~~~
>This version of Percona XtraBackup can only perform backups and restores against MySQL 8.0 and Percona Server 8.0
Please use Percona XtraBackup 2.4 for this database.


找到了mysql和 xtrabackup版本对应关系
 MySQL 5.6及之前的版本需要安装 Percona XtraBackup 2.3，安装指导请参见官方文档[Percona XtraBackup 2.3](https://www.percona.com/doc/percona-xtrabackup/2.3/installation.html)。
MySQL 5.7版本需要安装 Percona XtraBackup 2.4，安装指导请参见官方文档[Percona XtraBackup 2.4](https://www.percona.com/doc/percona-xtrabackup/2.4/installation.html)。
MySQL 8.0版本需要安装 Percona XtraBackup 8.0，安装指导请参见官方文档[Percona XtraBackup 8.0](https://www.percona.com/doc/percona-xtrabackup/8.0/installation.html)。


###卸载：
~~~
[root@localhost xtrabackupdata]# rpm -qa | grep xtrabackup
percona-xtrabackup-80-8.0.4-1.el7.x86_64
[root@localhost xtrabackupdata]# rpm -e percona-xtrabackup-80-8.0.4-1.el7.x86_64
[root@localhost xtrabackupdata]# rpm -qa | grep xtrabackup
~~~
###安装 percona-xtrabackup 2.4


~~~
[root@localhost xtrabackupdata]# xtrabackup --version
xtrabackup version 2.4.4 based on MySQL server 5.7.13 Linux (x86_64) (revision id: df58cf2)
~~~

###tar压缩归档
~~~

innobackupex --defaults-file=/etc/my.cnf --host=192.168.6.128 --user=root --password=Sgl20@14  --stream=tar /data/mysql/xtrabackupdata |gzip >/data/mysql/xtrabackupdata/`date +%F`.tar.gz

~~~

###发送到远程服务器
~~~
innobackupex --defaults-file=/etc/my.cnf --user=root --password=`Sgl20@14` --host=127.0.0.1 --port=3306 --stream=tar ./ | ssh root@10.0.0.70 -p14573 \ "cat - > /data/dbbackup/backup.tar"

~~~

###使用脚本定时备份
普通的策略是：每周进行一次全备，接下来6天执行增量备份，并保留上一周的一套备份。同时全备也复制一个副本。防止被增量备份应用过后无法恢复。



###全量备份

######全量备份步骤

~~~
innobackupex --defaults-file=/etc/my.cnf --host=192.168.6.128 --user=root --password=Sgl20@14 /data/mysql/xtrabackupdata
~~~
备份完成后的目标文件夹，这里最好不要指定 --databases 只备份目标库，应该把所有库都备份下来。包括mysql库。只备份目标库会导致恢复时后识别不了表，需要重新创建表然后关联表空间。（有个table_id保存在共享表空间文件中）
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9641ccff5bb02753.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######全量恢复步骤

1、执行恢复操作，首先确保mysql data目录为空。可以先将mysql的 data 文件夹更名为其它比如 mv data data.bak，不然恢复的时候会报错的。

2、应用全量备份

~~~
innobackupex --default-file=/etc/my.cnf --apply-log /data/mysql/xtrabackupdata/2020-10-28_17-15-52
~~~

>一般情况下，在备份完成后，数据尚且不能用于恢复操作，因为备份的数据中可能会包含尚未提交的事务或者已经提交但尚未同步至数据文件中的事务。因此，此时数据文件仍处于不一致状态。"准备"的主要作用正是通过回滚未提交的事务及同步已经提交的事务至数据文件也使用得数据文件处于一致性状态。 在实现"准备"的过程中，innobackupex通常还可以使用--user-memory选项来指定其可以使用的内存的大小，默认为100M.如果有足够的内存空间可用，可以多划分一些内存给prepare的过程，以提高其完成备份的速度。



看到innobackupex: completed OK! 表示成功.

3 、拷贝文件
~~~
innobackupex  --default-file=/etc/my.cnf  --copy-back /data/mysql/xtrabackupdata/2020-10-28_17-15-52
~~~

4、修改文件权限

~~~
chown -R mysql.mysql /data/
~~~
5、重启数据库（数据恢复的mysql需要重启）
~~~
 service mysqld  restart
~~~
###增量备份

　　使用innobackupex进行增量备份，每个InnoDB的页面都会包含一个LSN信息，每当相关的数据发生改变，相关的页面的LSN就会自动增长。这正是InnoDB表可以进行增量备份的基础，即innobackupex通过备份上次完全备份之后发生改变的页面来实现。

在进行增量备份时，首先要进行一次全量备份，第一次增量备份是基于全备的，之后的增量备份都是基于上一次的增量备份的，以此类推。比如增量1基于全备、增量2基于增量1。

但是恢复的时候却不是像备份的那样一层一层的应用，而是 增量备份1应用到全量备份，然后紧接着增量备份2再应用到全量备份，增量备份3应用... 依次类推。（增量1、增量2、增量3按时间先后应用）

>需要注意的是，增量备份仅能应用于InnoDB或XtraDB表，对于MyISAM表而言，执行增量备份时其实进行的是完全备份。因为MyISAM不支持事务，而增量备份确是基于事务实现的。原理就是在全量备份上面按时间顺序依次重新执行（重放）各个增量备份中的提交的事务。




######进行增量备份步骤


1、执行增量备份之前都需进行一次全量的备份
~~~
innobackupex --defaults-file=/etc/my.cnf --host=192.168.6.128 --user=root --password=Sgl20@14 /data/mysql/xtrabackupdata
~~~
2、基于之前的备份来进行增量备份
~~~
innobackupex --defaults-file=/etc/my.cnf  --user=root--password=Sgl20@14 --incremental /data/mysql/xtrabackupdata --incremental-basedir=/data/mysql/xtrabackupdata/2020-10-28_17-15-52
~~~
incremental-basedir 指定基于的备份，第一次增量备份就是基于全量的。以后的增量就是基于上一次的增量。


######增量备份的恢复步骤
1、现在已有1个全量和2个增量
![image.png](https://upload-images.jianshu.io/upload_images/13965490-67c057cc56b194ed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


2、要先准备基本备份
~~~
xtrabackup --prepare --apply-log-only --target-dir=/data/mysql/xtrabackupdata/2020-10-29_16-19-39
~~~
target-dir 指定基本备份路径（全量备份）

>"准备"(prepare)增量备份与整理完全备份有着一些不同，尤其要注意的是：
1、需要在每个备份 (包括完全和各个增量备份)上，将已经提交的事务进行"重放"。"重放"之后，所有的备份数据将合并到完全备份上。2、基于所有的备份将未提交的事务进行"回滚"

3、将所有的增量应用到全量之上，有多个增量则按备份时间顺序执行。这里有2个增量则执行2次。

①、将增量1于全量
~~~
xtrabackup --prepare --apply-log-only --target-dir=/data/mysql/xtrabackupdata/2020-10-29_16-19-39 --incremental-dir=/data/mysql/xtrabackupdata/2020-10-29_16-20-37
~~~
incremental-dir 指定增量备份路径。

②、再将增量2应用到全量上
~~~
xtrabackup --prepare --apply-log-only --target-dir=/data/mysql/xtrabackupdata/2020-10-29_16-19-39 --incremental-dir=/data/mysql/xtrabackupdata/2020-10-29_16-22-02
~~~

>1、若在一次恢复数据后又有增量备份3出现，那么现在像想要恢复到增量备份3的话直接将增量3应用到全量上就行了，之前增量1、增量2应用过一次就ok了不需要重复应用。
2、也就是说已经应用了增量备份的全量备份就是等于 全量+增量，再也不能回到之前的全量快照了！所以说想要保持之前的全量备份就必须自己手动copy一份防止出现意外。

4、恢复备份，指定的是第一个基本备份
~~~
 xtrabackup --copy-back --target-dir=/data/mysql/xtrabackupdata/2020-10-29_16-19-39
~~~
同样恢复数据时需要保证data文件夹为空！不然报如下错误：
>xtrabackup version 2.4.4 based on MySQL server 5.7.13 Linux (x86_64) (revision id: df58cf2)
Original data directory /data/mysql/mysql-5.7.31-linux-glibc2.12-x86_64/data is not empty!

5、修改权限
~~~
 chown mysql:mysql  ./data -R *
~~~
6、重启数据库

~~~
 service mysqld  restart
~~~
###可以通过查看xtrabackup_checkpoints文件来区分 备份文件是全量还是增量

全量
~~~
[root@localhost 2020-10-28_18-28-36]# cat xtrabackup_checkpoints
backup_type = full-prepared
from_lsn = 0
to_lsn = 22917932
last_lsn = 22917941
compact = 0
recover_binlog_info = 0
~~~

增量
~~~
[root@localhost 2020-10-29_14-09-10]# cat xtrabackup_checkpoints
backup_type = incremental
from_lsn = 22916945
to_lsn = 22924162
last_lsn = 22924171
compact = 0
recover_binlog_info = 0

~~~

###主从复制下使用需注意
在主从环境，那将master进行恢复后，因恢复过程中没有产生二进制日志（xtrabackup恢复毕竟只是磁盘文件的恢复，并不会写binlog），slave不会恢复到跟master一致，所以也要在slave使用同样的方式进行恢复。


###压缩备份

Percona XtraBackup实施了对压缩备份的支持。它可用于使用xbstream压缩/解压缩本地或流式备份。 

######创建压缩备份 

为了进行压缩备份，您需要使用xtrabackup --compress 选项：
~~~
innobackupex --defaults-file=/etc/my.cnf --host=192.168.6.128 --user=root --password=Sgl20@14 --compress /data/mysql/xtrabackupdata
~~~
如果你想加快压缩速度，你可以使用并行压缩，这可以通过xtrabackup --compress-threads选项启用。以下示例将使用四个线程进行压缩：
~~~
innobackupex --defaults-file=/etc/my.cnf --host=192.168.6.128 --user=root --password=Sgl20@14 --compress --compress-threads=4   /data/mysql/xtrabackupdata
~~~

压缩过的备份文件相对于没有压缩的备份文件多了 `.qp` 结尾
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2fc9a2f3eedf9602.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######恢复压缩备份 
1、在准备备份之前，您需要解压所有文件。 Percona XtraBackup已经实现了可用于解压缩备份的选项 xtrabackup --decompress，但是Innobackupex默认没有集成安装qpress，不安装报错
>201030 14:59:35 [01] decompressing ./xtrabackup_logfile.qp
sh: qpress: 未找到命令
Error: thread 0 failed.

因此需要先手动安装qpress
~~~
wget http://www.quicklz.com/qpress-11-linux-x64.tar
tar xvf qpress-11-linux-x64.tar
cp qpress /usr/bin
~~~

2、然后指定压缩备份进行解压
~~~
innobackupex --decompress --remove-original  /data/mysql/xtrabackupdata/2020-10-30_14-28-07
~~~
会把文件直接解压到当前目录
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c916c03e21525c04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Percona XtraBackup不会自动删除压缩文件。为了清理备份目录，您应该使用 xtrabackup --remove-original 移除原始选项。 

之后的恢复操作就和上面介绍的一样了。


###tar压缩归档
~~~

innobackupex --defaults-file=/etc/my.cnf --host=192.168.6.128 --user=root --password=Sgl20@14  --stream=tar /data/mysql/xtrabackupdata |gzip >/data/mysql/xtrabackupdata/`date +%F`.tar.gz

~~~

###发送到远程服务器
~~~
innobackupex --defaults-file=/etc/my.cnf --user=root --password=`Sgl20@14` --host=127.0.0.1 --port=3306 --stream=tar ./ | ssh root@10.0.0.70 -p14573 \ "cat - > /data/dbbackup/backup.tar"

~~~

###使用脚本定时备份
普通的策略是：每周进行一次全备，接下来6天执行增量备份，并保留上一周的一套备份。同时全备也复制一个副本。防止被增量备份应用过后无法恢复。
