---
title: 在线ddl解决方案之pt-online-schema-change-工具在线ddl不影响线上.md
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
title: 在线ddl解决方案之pt-online-schema-change-工具在线ddl不影响线上.md
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
###原理
1、为什么delete 加 ignore？
~~~
 pt-online-schema-change  --alter="ADD COLUMN m varchar(255) NOT NULL DEFAULT '' D=test,t=book --execute
~~~



###安装
~~~
$ wget http://search.cpan.org/CPAN/authors/id/T/TI/TIMB/DBI-1.625.tar.gz
$ tar xvfz DBI-1.625.tar.gz
$ cd DBI-1.625
$ perl Makefile.PL
$ make
$ make install
~~~

~~~
# 安装DBD-mysql插件
下载地址:
wget https://cpan.metacpan.org/authors/id/C/CA/CAPTTOFU/DBD-mysql-4.023.tar.gz
tar -zxvf DBD-mysql-4.023.tar.gz
cd DBD-mysql-4.023
perl  Makefile.PL --mysql_config=/data/mysql/mysql-5.7.31-linux-glibc2.12-x86_64/bin/mysql_config --with-mysql=/data/mysql/mysql-5.7.31-linux-glibc2.12-x86_64
make
make install
~~~
###背景
目测是长事务引起的。
快速恢复的办法就是立刻kill掉所有DML连接，还有问题就再kill一遍sleep连接，业务秒级抖动，然后就恢复了
ddl保险的方式是通过pt-osc或者gh-ost之类的工具去搞（我觉得主从切换一点也不保险，还有可能影响数据准确性）
即使是inplace的DDL在主库不影响读写，同步还是会造成延迟的。

###yum安装安装
1、yum安装percona的源
>yum install https://downloads.percona.com/downloads/percona-release/percona-release-1.0-9/redhat/percona-release-1.0-9.noarch.rpm

2、列出
>yum list | grep percona-toolkit

~~~
[root@localhost bin]# yum list | grep percona-toolkit

percona-toolkit.x86_64                    3.2.1-1.el7                    @percona-release-x86_64
percona-toolkit.noarch                    2.2.20-1                       percona-release-noarch
percona-toolkit-debuginfo.x86_64          3.0.13-1.el7                   percona-release-x86_64

~~~
3、安装pt-osc 工具：
>yum install percona-toolkit-3.2.1-1.el7.x86_64


###安装包安装

1、下载percona-toolkit 安装包
https://downloads.percona.com/downloads/percona-toolkit/3.2.1/binary/redhat/7/x86_64/percona-toolkit-3.2.1-1.el7.x86_64.rpm

2、安装percona-toolkit    
yum install percona-toolkit-3.2.1-1.el7.x86_64 





###简单使用
1、查看安装路径
~~~
[root@localhost bin]# find / -name pt-online-schema-change
/usr/bin/pt-online-schema-change
~~~

2、help 命令解释
~~~
[root@localhost bin]# ./pt-online-schema-change --help
pt-online-schema-change alters a table's structure without blocking reads or
writes.  Specify the database and table in the DSN.  Do not use this tool before
reading its documentation and checking your backups carefully.  For more
details, please use the --help option, or try 'perldoc
./pt-online-schema-change' for complete documentation.

Usage: pt-online-schema-change [OPTIONS] DSN

Options:

  --alter=s                        The schema modification, without the ALTER
                                   TABLE keywords
  --alter-foreign-keys-method=s    How to modify foreign keys so they reference
                                   the new table
  --[no]analyze-before-swap        Execute ANALYZE TABLE on the new table
                                   before swapping with the old one (default
                                   yes)
  --ask-pass                       Prompt for a password when connecting to
                                   MySQL
  --channel=s                      Channel name used when connected to a server
                                   using replication channels
  --charset=s                  -A  Default character set
  --[no]check-alter                Parses the --alter specified and tries to
                                   warn of possible unintended behavior (
                                   default yes)
  --[no]check-foreign-keys         Check for self-referencing foreign keys (
                                   default yes)
  --check-interval=m               Sleep time between checks for --max-lag (
                                   default 1).  Optional suffix s=seconds, m=
                                   minutes, h=hours, d=days; if no suffix, s is
                                   used.
  --[no]check-plan                 Check query execution plans for safety (
                                   default yes)
  --[no]check-replication-filters  Abort if any replication filter is set on
                                   any server (default yes)
  --check-slave-lag=s              Pause the data copy until this replica's lag
                                   is less than --max-lag
  --[no]check-unique-key-change    Avoid pt-online-schema-change to run if the
                                   specified statement for --alter is trying to
                                   add an unique index (default yes)
  --chunk-index=s                  Prefer this index for chunking tables
  --chunk-index-columns=i          Use only this many left-most columns of a --
                                   chunk-index
  --chunk-size=z                   Number of rows to select for each chunk
                                   copied (default 1000)
  --chunk-size-limit=f             Do not copy chunks this much larger than the
                                   desired chunk size (default 4.0)
  --chunk-time=f                   Adjust the chunk size dynamically so each
                                   data-copy query takes this long to execute (
                                   default 0.5)
  --config=A                       Read this comma-separated list of config
                                   files; if specified, this must be the first
                                   option on the command line
  --critical-load=A                Examine SHOW GLOBAL STATUS after every
                                   chunk, and abort if the load is too high (
                                   default Threads_running=50)
  --data-dir=s                     Create the new table on a different
                                   partition using the DATA DIRECTORY feature
  --database=s                 -D  Connect to this database
  --default-engine                 Remove ENGINE from the new table
  --defaults-file=s            -F  Only read mysql options from the given file
  --[no]drop-new-table             Drop the new table if copying the original
                                   table fails (default yes)
  --[no]drop-old-table             Drop the original table after renaming it (
                                   default yes)
  --[no]drop-triggers              Drop triggers on the old table. --no-drop-
                                   triggers forces --no-drop-old-table (default
                                   yes)
  --dry-run                        Create and alter the new table, but do not
                                   create triggers, copy data, or replace the
                                   original table
  --execute                        Indicate that you have read the
                                   documentation and want to alter the table
  --force                          This options bypasses confirmation in case
                                   of using alter-foreign-keys-method = none ,
                                   which might break foreign key constraints
  --help                           Show help and exit
  --host=s                     -h  Connect to host
  --max-flow-ctl=f                 Somewhat similar to --max-lag but for PXC
                                   clusters
  --max-lag=m                      Pause the data copy until all replicas' lag
                                   is less than this value (default 1s).
                                   Optional suffix s=seconds, m=minutes, h=
                                   hours, d=days; if no suffix, s is used.
  --max-load=A                     Examine SHOW GLOBAL STATUS after every
                                   chunk, and pause if any status variables are
                                   higher than their thresholds (default
                                   Threads_running=25)
  --new-table-name=s               New table name before it is swapped. %T is
                                   replaced with the original table name (
                                   default %T_new)
  --null-to-not-null               Allows MODIFYing a column that allows NULL
                                   values to one that doesn't allow them
  --only-same-schema-fks           Check foreigns keys only on tables on the
                                   same schema than the original table
  --password=s                 -p  Password to use when connecting
  --pause-file=s                   Execution will be paused while the file
                                   specified by this param exists
  --pid=s                          Create the given PID file
  --plugin=s                       Perl module file that defines a
                                   pt_online_schema_change_plugin class
  --port=i                     -P  Port number to use for connection
  --preserve-triggers              Preserves old triggers when specified
  --print                          Print SQL statements to STDOUT
  --progress=a                     Print progress reports to STDERR while
                                   copying rows (default time,30)
  --quiet                      -q  Do not print messages to STDOUT (disables --
                                   progress)
  --recurse=i                      Number of levels to recurse in the hierarchy
                                   when discovering replicas
  --recursion-method=a             Preferred recursion method for discovering
                                   replicas (default processlist,hosts)
  --remove-data-dir                If the original table was created using the
                                   DATA DIRECTORY feature, remove it and create
                                   the new table in MySQL default directory
                                   without creating a new isl file (default no)
  --set-vars=A                     Set the MySQL variables in this comma-
                                   separated list of variable=value pairs
  --skip-check-slave-lag=d         DSN to skip when checking slave lag
  --slave-password=s               Sets the password to be used to connect to
                                   the slaves
  --slave-user=s                   Sets the user to be used to connect to the
                                   slaves
  --sleep=f                        How long to sleep (in seconds) after copying
                                   each chunk (default 0)
  --socket=s                   -S  Socket file to use for connection
  --statistics                     Print statistics about internal counters
  --[no]swap-tables                Swap the original table and the new, altered
                                   table (default yes)
  --tries=a                        How many times to try critical operations
  --user=s                     -u  User for login if not current user
  --version                        Show version and exit
  --[no]version-check              Check for the latest version of Percona
                                   Toolkit, MySQL, and other programs (default
                                   yes)

Option types: s=string, i=integer, f=float, h/H/a/A=comma-separated list, d=DSN, z=size, m=time

Rules:

  --dry-run and --execute are mutually exclusive.
  This tool accepts additional command-line arguments. Refer to the SYNOPSIS and usage information for details.

DSN syntax is key=value[,key=value...]  Allowable DSN keys:

  KEY  COPY  MEANING
  ===  ====  =============================================
  A    yes   Default character set
  D    no    Database for the old and new table
  F    yes   Only read default options from the given file
  P    no    Port number to use for connection
  S    yes   Socket file to use for connection
  h    yes   Connect to host
  p    yes   Password to use when connecting
  t    no    Table to alter
  u    yes   User for login if not current user

  If the DSN is a bareword, the word is treated as the 'h' key.

Options and values after processing arguments:

  --alter                          (No value)
  --alter-foreign-keys-method      (No value)
  --analyze-before-swap            TRUE
  --ask-pass                       FALSE
  --channel                        (No value)
  --charset                        (No value)
  --check-alter                    TRUE
  --check-foreign-keys             TRUE
  --check-interval                 1
  --check-plan                     TRUE
  --check-replication-filters      TRUE
  --check-slave-lag                (No value)
  --check-unique-key-change        TRUE
  --chunk-index                    (No value)
  --chunk-index-columns            (No value)
  --chunk-size                     1000
  --chunk-size-limit               4.0
  --chunk-time                     0.5
  --config                         /etc/percona-toolkit/percona-toolkit.conf,/etc/percona-toolkit/pt-online-schema-change.conf,/root/.percona-toolkit.conf,/root/.pt-online-schema-change.conf
  --critical-load                  Threads_running=50
  --data-dir                       (No value)
  --database                       (No value)
  --default-engine                 FALSE
  --defaults-file                  (No value)
  --drop-new-table                 TRUE
  --drop-old-table                 TRUE
  --drop-triggers                  TRUE
  --dry-run                        FALSE
  --execute                        FALSE
  --force                          FALSE
  --help                           TRUE
  --host                           (No value)
  --max-flow-ctl                   (No value)
  --max-lag                        1
  --max-load                       Threads_running=25
  --new-table-name                 %T_new
  --null-to-not-null               FALSE
  --only-same-schema-fks           FALSE
  --password                       (No value)
  --pause-file                     (No value)
  --pid                            (No value)
  --plugin                         (No value)
  --port                           (No value)
  --preserve-triggers              FALSE
  --print                          FALSE
  --progress                       time,30
  --quiet                          FALSE
  --recurse                        (No value)
  --recursion-method               processlist,hosts
  --remove-data-dir                TRUE
  --set-vars                       
  --skip-check-slave-lag           (No value)
  --slave-password                 (No value)
  --slave-user                     (No value)
  --sleep                          0
  --socket                         (No value)
  --statistics                     FALSE
  --swap-tables                    TRUE
  --tries                          (No value)
  --user                           (No value)
  --version                        FALSE
  --version-check                  TRUE

~~~
>可以把find / -name pt-online-schema-change的路径放到path环境变量下。这样就方便执行了，不用每次进入特定目录

###开始使用

--user=        连接mysql的用户名
--password=    连接mysql的密码
--host=        连接mysql的地址
P=3306         连接mysql的端口号
D=             连接mysql的库名
t=             连接mysql的表名
--alter        修改表结构的语句
--execute      执行修改表结构
--charset=utf8 使用utf8编码，避免中文乱码
--no-version-check  不检查版本，在阿里云服务器中一般加入此参数，否则会报错linux


~~~
[root@localhost home]# pt-online-schema-change --user=root --password=Sgl20@14 --host=192.168.1.11 --port=3306 --charset=utf8 --nodrop-old-table --alter=" ADD COLUMN m varchar(255) NOT NULL DEFAULT '' " D=test,t=book --exec
Cannot connect to MySQL: install_driver(mysql) failed: Attempt to reload DBD/mysql.pm aborted.
Compilation failed in require at (eval 30) line 3.

 at /usr/bin/pt-online-schema-change line 2345.
~~~~



###执行报错解决

install_driver(mysql) failed: Attempt to reload DBD/mysql.pm aborted.

~~~
root@localhost mysql]# ldd /usr/lib64/perl5/vendor_perl/auto/DBD/mysql/mysql.so
	linux-vdso.so.1 =>  (0x00007ffe43f52000)
	libmysqlclient.so.18 => not found
	libpthread.so.0 => /lib64/libpthread.so.0 (0x00007ffa5308f000)
	libz.so.1 => /lib64/libz.so.1 (0x00007ffa52e79000)
	libm.so.6 => /lib64/libm.so.6 (0x00007ffa52b77000)
	libssl.so.10 => /lib64/libssl.so.10 (0x00007ffa52905000)
	libcrypto.so.10 => /lib64/libcrypto.so.10 (0x00007ffa524a2000)
	libdl.so.2 => /lib64/libdl.so.2 (0x00007ffa5229e000)
	libc.so.6 => /lib64/libc.so.6 (0x00007ffa51ed0000)
	/lib64/ld-linux-x86-64.so.2 (0x00007ffa534c7000)
	libgssapi_krb5.so.2 => /lib64/libgssapi_krb5.so.2 (0x00007ffa51c83000)
	libkrb5.so.3 => /lib64/libkrb5.so.3 (0x00007ffa5199a000)
	libcom_err.so.2 => /lib64/libcom_err.so.2 (0x00007ffa51796000)
	libk5crypto.so.3 => /lib64/libk5crypto.so.3 (0x00007ffa51563000)
	libkrb5support.so.0 => /lib64/libkrb5support.so.0 (0x00007ffa51353000)
	libkeyutils.so.1 => /lib64/libkeyutils.so.1 (0x00007ffa5114f000)
	libresolv.so.2 => /lib64/libresolv.so.2 (0x00007ffa50f35000)
	libselinux.so.1 => /lib64/libselinux.so.1 (0x00007ffa50d0e000)
	libpcre.so.1 => /lib64/libpcre.so.1 (0x00007ffa50aac000)

~~~

>libmysqlclient.so.18 => not found


找下这个文件libmysqlclient.so.18
~~~
# find / -name libmysqlclient.so.18
/home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/lib/libmysqlclient.so.18
~~~

进入 /lib64/目录创建软链
~~~
[root@localhost mysql]# cd  /lib64/
[root@localhost lib64]# ln -s /home/mysql5.6/mysql-5.6.51-linux-glibc2.12-x86_64/lib/libmysqlclient.so.18
~~~

这次正常了
~~~
[root@localhost lib64]# ldd /usr/lib64/perl5/vendor_perl/auto/DBD/mysql/mysql.so
	linux-vdso.so.1 =>  (0x00007ffff235d000)
	libmysqlclient.so.18 => /lib64/libmysqlclient.so.18 (0x00007f1057cb1000)
	libpthread.so.0 => /lib64/libpthread.so.0 (0x00007f1057a95000)
	libz.so.1 => /lib64/libz.so.1 (0x00007f105787f000)
	libm.so.6 => /lib64/libm.so.6 (0x00007f105757d000)
	libssl.so.10 => /lib64/libssl.so.10 (0x00007f105730b000)
	libcrypto.so.10 => /lib64/libcrypto.so.10 (0x00007f1056ea8000)
	libdl.so.2 => /lib64/libdl.so.2 (0x00007f1056ca4000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f10568d6000)
	librt.so.1 => /lib64/librt.so.1 (0x00007f10566ce000)
	libstdc++.so.6 => /lib64/libstdc++.so.6 (0x00007f10563c7000)
	libgcc_s.so.1 => /lib64/libgcc_s.so.1 (0x00007f10561b1000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f10586f6000)
	libgssapi_krb5.so.2 => /lib64/libgssapi_krb5.so.2 (0x00007f1055f64000)
	libkrb5.so.3 => /lib64/libkrb5.so.3 (0x00007f1055c7b000)
	libcom_err.so.2 => /lib64/libcom_err.so.2 (0x00007f1055a77000)
	libk5crypto.so.3 => /lib64/libk5crypto.so.3 (0x00007f1055844000)
	libkrb5support.so.0 => /lib64/libkrb5support.so.0 (0x00007f1055634000)
	libkeyutils.so.1 => /lib64/libkeyutils.so.1 (0x00007f1055430000)
	libresolv.so.2 => /lib64/libresolv.so.2 (0x00007f1055216000)
	libselinux.so.1 => /lib64/libselinux.so.1 (0x00007f1054fef000)
	libpcre.so.1 => /lib64/libpcre.so.1 (0x00007f1054d8d000)
~~~

执行
~~~
[root@localhost bin]# ./pt-online-schema-change --alter="ADD COLUMN m varchar(255) NOT NULL DEFAULT ''" D=dbt3,t=orders --execute
No slaves found.  See --recursion-method if host localhost.localdomain has slaves.
Not checking slave lag because no slaves were found and --check-slave-lag was not specified.
Operation, tries, wait:
  analyze_table, 10, 1
  copy_rows, 10, 0.25
  create_triggers, 10, 1
  drop_triggers, 10, 1
  swap_tables, 10, 1
  update_foreign_keys, 10, 1
Altering `dbt3`.`orders`...
Creating new table...
Created new table dbt3._orders_new OK.
Altering new table...
Altered `dbt3`.`_orders_new` OK.
2021-07-18T21:37:32 Creating triggers...
2021-07-18T21:37:32 Created triggers OK.
2021-07-18T21:37:32 Copying approximately 1372000 rows...
Copying `dbt3`.`orders`:  33% 00:58 remain
Copying `dbt3`.`orders`:  47% 01:05 remain
Copying `dbt3`.`orders`:  57% 01:07 remain
Copying `dbt3`.`orders`:  66% 01:01 remain
Copying `dbt3`.`orders`:  75% 00:47 remain
Copying `dbt3`.`orders`:  86% 00:28 remain
Copying `dbt3`.`orders`:  96% 00:07 remain
2021-07-18T21:41:39 Copied rows OK.
2021-07-18T21:41:39 Analyzing new table...
2021-07-18T21:41:39 Swapping tables...
2021-07-18T21:41:39 Swapped original and new tables OK.
2021-07-18T21:41:39 Dropping old table...
2021-07-18T21:41:39 Dropped old table `dbt3`.`_orders_old` OK.
2021-07-18T21:41:39 Dropping triggers...
2021-07-18T21:41:39 Dropped triggers OK.
Successfully altered `dbt3`.`orders`.

~~~
