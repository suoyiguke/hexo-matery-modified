---
title: mysql-Utilities官方工具集之mysqlfrm脱机解析frm表结构文件.md
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
title: mysql-Utilities官方工具集之mysqlfrm脱机解析frm表结构文件.md
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
 ./mysqlfrm --diagnostic user.frm
~~~
[root@localhost mysql]# ./mysqlfrm --diagnostic user.frm
-bash: ./mysqlfrm: 没有那个文件或目录
[root@localhost mysql]# mysqlfrm --diagnostic user.frm
# WARNING: Cannot generate character set or collation names without the --server option.
# CAUTION: The diagnostic mode is a best-effort parse of the .frm file. As such, it may not identify all of the components of the table correctly. This is especially true for damaged files. It will also not read the default values for the columns and the resulting statement may not be syntactically correct.
# Reading .frm file for user.frm:
# The .frm file is a TABLE.
# CREATE TABLE Statement:

CREATE TABLE `user` (
  `Host` char(180) NOT NULL, 
  `User` char(96) NOT NULL, 
  `Select_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Insert_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Update_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Delete_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Create_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Drop_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Reload_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Shutdown_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Process_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `File_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Grant_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `References_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Index_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Alter_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Show_db_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Super_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Create_tmp_table_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Lock_tables_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Execute_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Repl_slave_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Repl_client_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Create_view_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Show_view_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Create_routine_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Alter_routine_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Create_user_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Event_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Trigger_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `Create_tablespace_priv` enum('N','Y') CHARACTER SET <UNKNOWN> NOT NULL, 
  `ssl_type` enum('ANY','X509','SPECIFIED') CHARACTER SET <UNKNOWN> NOT NULL, 
  `ssl_cipher` blob CHARACTER SET <UNKNOWN>, 
  `x509_issuer` blob CHARACTER SET <UNKNOWN>, 
  `x509_subject` blob CHARACTER SET <UNKNOWN>, 
  `max_questions` int(11) unsigned NOT NULL, 
  `max_updates` int(11) unsigned NOT NULL, 
  `max_connections` int(11) unsigned NOT NULL, 
  `max_user_connections` int(11) unsigned NOT NULL, 
  `plugin` char(192) NOT NULL, 
  `authentication_string` text DEFAULT NULL, 
  `password_expired` enum('ANY','X509','SPECIFIED') CHARACTER SET <UNKNOWN> NOT NULL, 
  `password_last_changed` timestamp DEFAULT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
  `password_lifetime` smallint(5) unsigned DEFAULT NULL, 
  `account_locked` enum('ANY','X509','SPECIFIED') CHARACTER SET <UNKNOWN> NOT NULL, 
PRIMARY KEY `PRIMARY` (`Host`,`User`)
) ENGINE=MyISAM COMMENT 'Users and global privileges';

#...done.
[root@localhost mysql]# 
~~~

有个问题
1、字符集CHARACTER 是<UNKNOWN>。如果想要得到字段字符集设置。还得加上参数连上mysql。
2、由于不知道字符集所以char 长度乘以3
解决


 mysqlfrm --help 查看下参数
~~~
Options:
  --version             show program's version number and exit
  --license             display program's license and exit
  --help                
  --basedir=BASEDIR     the base directory for the server
  --diagnostic          read the frm files byte-by-byte to form the CREATE
                        statement. May require the --server or --basedir
                        options to decipher character set information
  --new-storage-engine=NEW_ENGINE
                        change ENGINE clause to use this engine.
  --frmdir=FRMDIR       save the new .frm files in this directory. Used and
                        valid with --new-storage-engine only.
  --port=PORT           Port to use for the spawned server.
  -s, --show-stats      show file statistics and general table information.
  --server=SERVER       connection information for the server in the form:
                        <user>[:<password>]@<host>[:<port>][:<socket>] or
                        <login-path>[:<port>][:<socket>] (optional) - if
                        provided, the storage engine and character set
                        information will be validated against this server.
  --user=USER           user account to launch spawned server. Required if
                        running as root user. Used only in the default mode.
  --start-timeout=START_TIMEOUT
                        Number of seconds to wait for spawned server to start.
                        Default = 10.
  -v, --verbose         control how much information is displayed. e.g., -v =
                        verbose, -vv = more verbose, -vvv = debug
  -q, --quiet           turn off all messages for quiet execution.
  --ssl-ca=SSL_CA       path to a file that contains a list of trusted SSL
                        CAs.
  --ssl-cert=SSL_CERT   name of the SSL certificate file to use for
                        establishing a secure connection.
  --ssl-key=SSL_KEY     name of the SSL key file to use for establishing a
                        secure connection.
  --ssl=SSL             specifies if the server connection requires use of
                        SSL. If an encrypted connection cannot be established,
                        the connection attempt fails. By default 0 (SSL not
                        required).

~~~

需要加上--server参数连上mysql。
 mysqlfrm --diagnostic user.frm --server=root:1111aaA_@localhost
如下输出的表结构语句是完整的。
~~~

[root@localhost mysql]# mysqlfrm --diagnostic user.frm --server=root:1111aaA_@localhost
WARNING: Using a password on the command line interface can be insecure.
# Source on localhost: ... connected.
# CAUTION: The diagnostic mode is a best-effort parse of the .frm file. As such, it may not identify all of the components of the table correctly. This is especially true for damaged files. It will also not read the default values for the columns and the resulting statement may not be syntactically correct.
# Reading .frm file for user.frm:
# The .frm file is a TABLE.
# CREATE TABLE Statement:

CREATE TABLE `user` (
  `Host` char(60) COLLATE `utf8_bin` NOT NULL, 
  `User` char(32) COLLATE `utf8_bin` NOT NULL, 
  `Select_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Insert_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Update_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Delete_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Create_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Drop_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Reload_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Shutdown_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Process_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `File_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Grant_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `References_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Index_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Alter_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Show_db_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Super_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Create_tmp_table_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Lock_tables_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Execute_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Repl_slave_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Repl_client_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Create_view_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Show_view_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Create_routine_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Alter_routine_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Create_user_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Event_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Trigger_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `Create_tablespace_priv` enum('N','Y') COLLATE `utf8_general_ci` NOT NULL, 
  `ssl_type` enum('ANY','X509','SPECIFIED') COLLATE `utf8_general_ci` NOT NULL, 
  `ssl_cipher` blob COLLATE `binary`, 
  `x509_issuer` blob COLLATE `binary`, 
  `x509_subject` blob COLLATE `binary`, 
  `max_questions` int(11) unsigned NOT NULL, 
  `max_updates` int(11) unsigned NOT NULL, 
  `max_connections` int(11) unsigned NOT NULL, 
  `max_user_connections` int(11) unsigned NOT NULL, 
  `plugin` char(64) COLLATE `utf8_bin` NOT NULL, 
  `authentication_string` text COLLATE `utf8_bin` DEFAULT NULL, 
  `password_expired` enum('ANY','X509','SPECIFIED') COLLATE `utf8_general_ci` NOT NULL, 
  `password_last_changed` timestamp DEFAULT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
  `password_lifetime` smallint(5) unsigned DEFAULT NULL, 
  `account_locked` enum('ANY','X509','SPECIFIED') COLLATE `utf8_general_ci` NOT NULL, 
PRIMARY KEY `PRIMARY` (`Host`,`User`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8, COMMENT 'Users and global privileges';
~~~

但是既然能连上mysql服务，我们为啥要用mysqlfrm 呢？。。。的确这是mysqlfrm 工具的一个问题。
