---
title: mysql-基准测试sysbench-安装（一）.md
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
title: mysql-基准测试sysbench-安装（一）.md
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
SysBench是一个模块化的、跨平台、多线程基准测试工具，主要用于评估测试各种不同系统参数下的数据库负载情况。
https://github.com/akopytov/sysbench
###sysbench的测试可运用：

1、CPU性能
2、磁盘IO性能
3、调动程序性能
4、内存分配及传输速度
5、POSIX线程性能
6、数据库性能(OLTP基准测试)      
7、sysbench可以快速对MySQL进行造数据。以后不用再写存储过程来insert了

###源码安装
1、centeros安装前准备
~~~
yum -y install make automake libtool pkgconfig libaio-devel
# For MySQL support, replace with mysql-devel on RHEL/CentOS 5
yum -y install mariadb-devel openssl-devel
# For PostgreSQL support
yum -y install postgresql-devel
~~~

2、下载源码
~~~
git clone https://github.com/akopytov/sysbench
~~~

3、安装
进入源码目录安装
~~~
#生产configure 文件
./autogen.sh 
# 使用 --with-mysql-includes指定mysql的include文件夹； --with-mysql-libs指定lib文件夹
./configure --with-mysql-includes=/data/mysql/mysql-5.7.31-linux-glibc2.12-x86_64/include --with-mysql-libs=/data/mysql/mysql-5.7.31-linux-glibc2.12-x86_64/lib --with-mysql
#编译安装
make && make install
~~~

4、检测

报错
[root@localhost sysbench]# sysbench --version
sysbench: error while loading shared libraries: libmysqlclient.so.20: cannot open shared object file: No such file or directory

先在本地找下这个 libmysqlclient.so.20文件存在不，按理说安装了mysql就会有的。
~~~
[root@localhost sysbench]# find / -name libmysqlclient.so.20
/data/mysql/mysql-5.7.31-linux-glibc2.12-x86_64/lib/libmysqlclient.so.20
~~~
然后创建软连接到  /usr/lib/libmysqlclient.so.20

~~~
ln -s /data/mysql/mysql-5.7.31-linux-glibc2.12-x86_64/lib/libmysqlclient.so.20 /usr/lib/libmysqlclient.so.20
~~~
编辑/ld.so.cnf文件 vi /etc/ld.so.cnf，将/usr/lib加入到文件中
~~~
/usr/lib
~~~
执行
~~~
/sbin/ldconfig -v
~~~

再次执行sysbench测试
~~~
[root@localhost sysbench]# sysbench --version
sysbench 1.1.0-bbee5d5
~~~

###Testname
包括两种：内建脚本和lua脚本

######内建脚本

  fileio - File I/O test
  cpu - CPU performance test
  memory - Memory functions speed test
  threads - Threads subsystem performance test
  mutex - Mutex performance test
 
######lua文件
lua脚本如下：
/root/sysbench/src/lua 目录下就是我们经常执行的lua脚本了

~~~
[root@localhost ~]# cd /root/sysbench/src/lua 
[root@localhost lua]# ll
总用量 132
-rwxr-xr-x. 1 root root  1446 6月  18 17:40 bulk_insert.lua
-rw-r--r--. 1 root root  1307 6月  18 17:40 empty-test.lua
drwxr-xr-x. 2 root root  4096 6月  18 17:41 internal
-rw-r--r--. 1 root root 25425 6月  18 17:40 Makefile
-rw-r--r--. 1 root root  1219 6月  18 17:40 Makefile.am
-rw-r--r--. 1 root root 24760 6月  18 17:40 Makefile.in
-rw-r--r--. 1 root root 14878 6月  18 17:40 oltp_common.lua
-rwxr-xr-x. 1 root root  1312 6月  18 17:40 oltp_delete.lua
-rwxr-xr-x. 1 root root  2437 6月  18 17:40 oltp_insert.lua
-rwxr-xr-x. 1 root root  1287 6月  18 17:40 oltp_point_select.lua
-rwxr-xr-x. 1 root root  1671 6月  18 17:40 oltp_read_only.lua
-rwxr-xr-x. 1 root root  1846 6月  18 17:40 oltp_read_write.lua
-rwxr-xr-x. 1 root root  1139 6月  18 17:40 oltp_update_index.lua
-rwxr-xr-x. 1 root root  1149 6月  18 17:40 oltp_update_non_index.lua
-rwxr-xr-x. 1 root root  1462 6月  18 17:40 oltp_write_only.lua
-rw-r--r--. 1 root root  1631 6月  18 17:40 prime-test.lua
-rwxr-xr-x. 1 root root  1955 6月  18 17:40 select_random_points.lua
-rwxr-xr-x. 1 root root  2154 6月  18 17:40 select_random_ranges.lua

~~~


###命令汇总

######1、基本命令
~~~
[root@localhost ~]# sysbench --help
Usage:
  sysbench [options]... [testname] [command]

Commands implemented by most tests: prepare run cleanup help

General options:
  --threads=N                     number of threads to use [1]
  --events=N                      limit for total number of events [0]
  --time=N                        limit for total execution time in seconds [10]
  --warmup-time=N                 execute events for this many seconds with statistics disabled before the actual benchmark run with statistics enabled [0]
  --forced-shutdown=STRING        number of seconds to wait after the --time limit before forcing shutdown, or 'off' to disable [off]
  --thread-stack-size=SIZE        size of stack per thread [64K]
  --thread-init-timeout=N         wait time in seconds for worker threads to initialize [30]
  --rate=N                        average transactions rate. 0 for unlimited rate [0]
  --report-interval=N             periodically report intermediate statistics with a specified interval in seconds. 0 disables intermediate reports [0]
  --report-checkpoints=[LIST,...] dump full statistics and reset all counters at specified points in time. The argument is a list of comma-separated values representing the amount of time in seconds elapsed from start of test when report checkpoint(s) must be performed. Report checkpoints are off by default. []
  --debug[=on|off]                print more debugging info [off]
  --validate[=on|off]             perform validation checks where possible [off]
  --help[=on|off]                 print help and exit [off]
  --version[=on|off]              print version and exit [off]
  --config-file=FILENAME          File containing command line options
  --luajit-cmd=STRING             perform LuaJIT control command. This option is equivalent to 'luajit -j'. See LuaJIT documentation for more information

Pseudo-Random Numbers Generator options:
  --rand-type=STRING   random numbers distribution {uniform, gaussian, pareto, zipfian} to use by default [uniform]
  --rand-seed=N        seed for random number generator. When 0, the current time is used as an RNG seed. [0]
  --rand-pareto-h=N    shape parameter for the Pareto distribution [0.2]
  --rand-zipfian-exp=N shape parameter (exponent, theta) for the Zipfian distribution [0.8]

Log options:
  --verbosity=N verbosity level {5 - debug, 0 - only critical messages} [3]

  --percentile=N       percentile to calculate in latency statistics (1-100). Use the special value of 0 to disable percentile calculations [95]
  --histogram[=on|off] print latency histogram in report [off]

General database options:

  --db-driver=STRING  specifies database driver to use ('help' to get list of available drivers) [mysql]
  --db-ps-mode=STRING prepared statements usage mode {auto, disable} [auto]
  --db-debug[=on|off] print database-specific debug information [off]


Compiled-in database drivers:
  mysql - MySQL driver

mysql options:
  --mysql-host=[LIST,...]          MySQL server host [localhost]
  --mysql-port=[LIST,...]          MySQL server port [3306]
  --mysql-socket=[LIST,...]        MySQL socket
  --mysql-user=STRING              MySQL user [sbtest]
  --mysql-password=STRING          MySQL password []
  --mysql-db=STRING                MySQL database name [sbtest]
  --mysql-ssl=STRING               SSL mode. This accepts the same values as the --ssl-mode option in the MySQL client utilities. Disabled by default [disabled]
  --mysql-ssl-key=STRING           path name of the client private key file
  --mysql-ssl-ca=STRING            path name of the CA file
  --mysql-ssl-cert=STRING          path name of the client public key certificate file
  --mysql-ssl-cipher=STRING        use specific cipher for SSL connections []
  --mysql-compression[=on|off]     use compression, if available in the client library [off]
  --mysql-debug[=on|off]           trace all client library calls [off]
  --mysql-ignore-errors=[LIST,...] list of errors to ignore, or "all" [1213,1020,1205]
  --mysql-dry-run[=on|off]         Dry run, pretend that all MySQL client API calls are successful without executing them [off]

Compiled-in tests:
  fileio - File I/O test
  cpu - CPU performance test
  memory - Memory functions speed test
  threads - Threads subsystem performance test
  mutex - Mutex performance test

See 'sysbench <testname> help' for a list of options for each test.
~~~





######２、oltp命令

~~~

[root@localhost ~]# sysbench  oltp_read_write  help
sysbench 1.1.0-bbee5d5 (using bundled LuaJIT 2.1.0-beta3)

oltp_read_write options:
  --auto_inc[=on|off]           Use AUTO_INCREMENT column as Primary Key (for MySQL), or its alternatives in other DBMS. When disabled, use client-generated IDs [on]
  --create_secondary[=on|off]   Create a secondary index in addition to the PRIMARY KEY [on]
  --create_table_options=STRING Extra CREATE TABLE options []
  --delete_inserts=N            Number of DELETE/INSERT combinations per transaction [1]
  --distinct_ranges=N           Number of SELECT DISTINCT queries per transaction [1]
  --index_updates=N             Number of UPDATE index queries per transaction [1]
  --mysql_storage_engine=STRING Storage engine, if MySQL is used [innodb]
  --non_index_updates=N         Number of UPDATE non-index queries per transaction [1]
  --order_ranges=N              Number of SELECT ORDER BY queries per transaction [1]
  --pgsql_variant=STRING        Use this PostgreSQL variant when running with the PostgreSQL driver. The only currently supported variant is 'redshift'. When enabled, create_secondary is automatically disabled, and delete_inserts is set to 0
  --point_selects=N             Number of point SELECT queries per transaction [10]
  --range_selects[=on|off]      Enable/disable all range SELECT queries [on]
  --range_size=N                Range size for range SELECT queries [100]
  --reconnect=N                 Reconnect after every N events. The default (0) is to not reconnect [0]
  --secondary[=on|off]          Use a secondary index in place of the PRIMARY KEY [off]
  --simple_ranges=N             Number of simple range SELECT queries per transaction [1]
  --skip_trx[=on|off]           Don't start explicit transactions and execute all queries in the AUTOCOMMIT mode [off]
  --sum_ranges=N                Number of SELECT SUM() queries per transaction [1]
  --table_size=N                Number of rows per table [10000]
  --tables=N                    Number of tables [1]

~~~
