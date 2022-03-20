---
title: libcrypto-so-1-1-丢失.md
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
title: libcrypto-so-1-1-丢失.md
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
###libprotobuf-lite.so.3.11.4找不到：
[root@localhost mysql8]# bin/mysqld --initialize --user=mysql8
bin/mysqld: error while loading shared libraries: libprotobuf-lite.so.3.11.4: cannot open shared object file: No such file or directory

yum 安裝mysql-tools-community找回依賴，通过centeros镜像站，得知这个so文件在mysql-tools-community中。我们安装之：
~~~
 yum install https://repo.mysql.com/yum/mysql-tools-community/el/7/aarch64/mysql-router-community-8.0.28-1.el7.aarch64.rpm
~~~
找到libprotobuf-lite.so.3.11.4的位置
~~~
[root@localhost mysql8]# find / -name libprotobuf-lite.so.3.11.4
/usr/lib64/mysqlrouter/private/libprotobuf-lite.so.3.11.4
~~~

设置路径
~~~
export LD_LIBRARY_PATH=/usr/lib64/mysqlrouter/private

~~~

再次安装，成功
~~~
[root@localhost mysql8]# bin/mysqld --initialize --user=mysql8
2022-01-19T03:50:29.291771Z 0 [Warning] [MY-011070] [Server] 'Disabling symbolic links using --skip-symbolic-links (or equivalent) is the default. Consider not using this option as it' is deprecated and will be removed in a future release.
2022-01-19T03:50:29.291901Z 0 [System] [MY-013169] [Server] /home/mysql8/bin/mysqld (mysqld 8.0.28) initializing of server in progress as process 8636
2022-01-19T03:50:29.291953Z 0 [ERROR] [MY-010338] [Server] Can't find error-message file '/home/mysql8/share/errmsg.sys'. Check error-message file location and 'lc-messages-dir' configuration directive.
2022-01-19T03:50:29.310095Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
2022-01-19T03:50:30.264141Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
2022-01-19T03:50:30.878181Z 0 [Warning] [MY-013829] [Server] Missing data directory for ICU regular expressions: /home/mysql8/lib/private/.
2022-01-19T03:50:31.227065Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: Nuwo-=e9?)xb
~~~
