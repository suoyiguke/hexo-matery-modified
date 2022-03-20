---
title: mysql-用户操作和权限操作.md
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
title: mysql-用户操作和权限操作.md
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
https://dev.mysql.com/doc/refman/5.7/en/grant.html

###用户管理和权限管理
mysql登录验证是通过三个维度的：用户名、密码、ip

创建david，ip无限制，密码为123
~~~
create user 'david'@'%' identified by '123';
~~~
创建david，ip限制为192.168.1开头，密码为123
~~~
create user 'david'@'192.168.1.*' identified by '123';
~~~
查看当前用户的权限
 show grants;
~~~
(root@localhost) [performance_schema]>show grants;
+-------------------------------------------------------------+
| Grants for root@%                                           |
+-------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION |
+-------------------------------------------------------------+
1 row in set (0.01 sec)

(david@localhost) [(none)]>show grants;
+-----------------------------------+
| Grants for david@%                |
+-----------------------------------+
| GRANT USAGE ON *.* TO 'david'@'%' |
+-----------------------------------+
1 row in set (0.00 sec)
~~~

查看特定用户权限

~~~
(david@localhost) [(none)]>show grunts for 'david'@'%';
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'grunts for 'david'@'%'' at line 1
(david@localhost) [(none)]>show grants for 'david'@'%';
+-----------------------------------+
| Grants for david@%                |
+-----------------------------------+
| GRANT USAGE ON *.* TO 'david'@'%' |
+-----------------------------------+
1 row in set (0.00 sec)
~~~



授权操作，将test.* 的select,update,insert,delete权限授予给 'david'@'%' 用户
~~~
(root@localhost) [performance_schema]>grant select,update,insert,delete on test.* to 'david'@'%';
Query OK, 0 rows affected (0.00 sec)
~~~
>`test.*` 代表test下的所有表，`*.*` 就是全局


>注意：有一种将创建用户和授权操作同时使用的操作，mysql不推荐这样做，未来版本会将这种写法删除。
~~~
(root@localhost) [performance_schema]>grant select,update,insert,delete on test.* to 'amy'@'%' identified by '123';
Query OK, 0 rows affected, 1 warning (0.00 sec)

(root@localhost) [performance_schema]>show warnings;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                   |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+
| Error | 1064 | You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'warning' at line 1 |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

(root@localhost) [performance_schema]>

~~~


修改用户密码
~~~
alter user  'david'@'%' identified by '456';
~~~
添加新的权限
~~~
grant create,index on test.* to 'david'@'%' ;
~~~
收回权限
~~~
revoke create,index on test.* from 'david'@'%';
~~~
>注意：revoke all on *.* to 'david'@'%' ; 将david的所有权限回收并不代表将用户删除了

将自己的权限授予其它用户的权限:with grant option 。

~~~
(root@localhost) [performance_schema]>grant select,update,insert,delete on test.* to 'david'@'%' with grant option ;
Query OK, 0 rows affected (0.00 sec)

(root@localhost) [performance_schema]>show grants for 'david'@'%';
+-----------------------------------------------------------------------------------+
| Grants for david@%                                                                |
+-----------------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'david'@'%'                                                 |
| GRANT SELECT, INSERT, UPDATE, DELETE ON `test`.* TO 'david'@'%' WITH GRANT OPTION |
+-----------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
~~~

这样我在david下就可以将自己的权限授予别人了
~~~
(david@localhost) [(none)]>grant select on test.* to 'amy'@'%';
Query OK, 0 rows affected (0.00 sec)
~~~

###mysql库下四张保存权限的表
user 全局级别
db 库级别
tables_priv 表级别
columns_priv 列级别
~~~

(root@localhost) [mysql]>show tables like 'user';
+------------------------+
| Tables_in_mysql (user) |
+------------------------+
| user                   |
+------------------------+
1 row in set (0.00 sec)

(root@localhost) [mysql]>show tables like 'db';
+----------------------+
| Tables_in_mysql (db) |
+----------------------+
| db                   |
+----------------------+
1 row in set (0.00 sec)

(root@localhost) [mysql]>show tables like 'tables_priv';
+-------------------------------+
| Tables_in_mysql (tables_priv) |
+-------------------------------+
| tables_priv                   |
+-------------------------------+
1 row in set (0.00 sec)

(root@localhost) [mysql]>show tables like 'columns_priv';
+--------------------------------+
| Tables_in_mysql (columns_priv) |
+--------------------------------+
| columns_priv                   |
+--------------------------------+
1 row in set (0.00 sec)

~~~



查询david这个用户在全局的权限
~~~
(root@localhost) [mysql]>select * from user where user='david'\G;
*************************** 1. row ***************************
                  Host: %
                  User: david
           Select_priv: N
           Insert_priv: N
           Update_priv: N
           Delete_priv: N
           Create_priv: N
             Drop_priv: N
           Reload_priv: N
         Shutdown_priv: N
          Process_priv: N
             File_priv: N
            Grant_priv: N
       References_priv: N
            Index_priv: N
            Alter_priv: N
          Show_db_priv: N
            Super_priv: N
 Create_tmp_table_priv: N
      Lock_tables_priv: N
          Execute_priv: N
       Repl_slave_priv: N
      Repl_client_priv: N
      Create_view_priv: N
        Show_view_priv: N
   Create_routine_priv: N
    Alter_routine_priv: N
      Create_user_priv: N
            Event_priv: N
          Trigger_priv: N
Create_tablespace_priv: N
              ssl_type: 
            ssl_cipher: 
           x509_issuer: 
          x509_subject: 
         max_questions: 0
           max_updates: 0
       max_connections: 0
  max_user_connections: 0
                plugin: mysql_native_password
 authentication_string: *531E182E2F72080AB0740FE2F2D689DBE0146E04
      password_expired: N
 password_last_changed: 2021-04-18 18:33:09
     password_lifetime: NULL
        account_locked: N
1 row in set (0.00 sec)
~~~
可以看到全都是N ，说名david在全局下没有权限。

再来看david在库级别的权限
~~~
(root@localhost) [mysql]>select * from db where user='david'\G;
*************************** 1. row ***************************
                 Host: %
                   Db: test
                 User: david
          Select_priv: Y
          Insert_priv: Y
          Update_priv: Y
          Delete_priv: Y
          Create_priv: N
            Drop_priv: N
           Grant_priv: Y
      References_priv: N
           Index_priv: N
           Alter_priv: N
Create_tmp_table_priv: N
     Lock_tables_priv: N
     Create_view_priv: N
       Show_view_priv: N
  Create_routine_priv: N
   Alter_routine_priv: N
         Execute_priv: N
           Event_priv: N
         Trigger_priv: N
1 row in set (0.00 sec)

ERROR: 
No query specified
~~~
可以看到david在库级别下存在Select_priv、Insert_priv、Update_priv、Delete_priv、Grant_priv的权限。说名创建的普通用户权限是在db级别的。

>注意，强烈建议不要直接修改这四张表（user 、db、tables_priv 、columns_priv ）来达到授权目的，请使用grant命令！这样做是存在一定风险的。 

而root权限是保存到user表里的：
~~~
(root@localhost) [mysql]>select * from user where user='root'\G;
*************************** 1. row ***************************
                  Host: %
                  User: root
           Select_priv: Y
           Insert_priv: Y
           Update_priv: Y
           Delete_priv: Y
           Create_priv: Y
             Drop_priv: Y
           Reload_priv: Y
         Shutdown_priv: Y
          Process_priv: Y
             File_priv: Y
            Grant_priv: Y
       References_priv: Y
            Index_priv: Y
            Alter_priv: Y
          Show_db_priv: Y
            Super_priv: Y
 Create_tmp_table_priv: Y
      Lock_tables_priv: Y
          Execute_priv: Y
       Repl_slave_priv: Y
      Repl_client_priv: Y
      Create_view_priv: Y
        Show_view_priv: Y
   Create_routine_priv: Y
    Alter_routine_priv: Y
      Create_user_priv: Y
            Event_priv: Y
          Trigger_priv: Y
Create_tablespace_priv: Y
              ssl_type: 
            ssl_cipher: 
           x509_issuer: 
          x509_subject: 
         max_questions: 0
           max_updates: 0
       max_connections: 0
  max_user_connections: 0
                plugin: mysql_native_password
 authentication_string: *6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9
      password_expired: N
 password_last_changed: 2021-04-18 10:45:46
     password_lifetime: NULL
        account_locked: N
1 row in set (0.00 sec)

~~~


###mysql密码加密方式
简单查询下mysql.user
~~~
(root@localhost) [mysql]>select user,host,authentication_string  from mysql.user;
+---------------+-----------+-------------------------------------------+
| user          | host      | authentication_string                     |
+---------------+-----------+-------------------------------------------+
| root          | %         | *6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9 |
| mysql.session | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| mysql.sys     | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| david         | %         | *531E182E2F72080AB0740FE2F2D689DBE0146E04 |
| amy           | %         | *23AE809DDACAF96AF0FD78ED04B6A265E05AA257 |
+---------------+-----------+-------------------------------------------+
5 rows in set (0.00 sec)
~~~

authentication_string  字段保存了mysql密码的加密后字符串，类似于md5，是一种单向的摘要算法。
内部使用mysql函数：password()来实现，如下：
~~~
(root@localhost) [mysql]>select password('456')
    -> ;
+-------------------------------------------+
| password('456')                           |
+-------------------------------------------+
| *531E182E2F72080AB0740FE2F2D689DBE0146E04 |
+-------------------------------------------+
1 row in set, 1 warning (0.00 sec)
~~~

###资源限制
https://dev.mysql.com/doc/refman/5.7/en/user-resources.html
1、每小时执行查询次数
2、每小时更新次数
3、每小时最大连接数
4、用户最大连接数
max_user_connections 
max_connectios_per_hour 每小时内连接数次数
max_queries_per_hour
max_updates_per_hour


david最多只能有一个用户连接。注意已经连上的用户不纳入记数。
~~~
alter user 'david'@'%' with max_user_connections 1;
[root@localhost ~]# mysql -udavid -p456
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1226 (42000): User 'david' has exceeded the 'max_user_connections' resource (current value: 1)
~~~


###基于角色的权限管理
https://dev.mysql.com/doc/refman/8.0/en/create-role.html
mysql8.0可以做到根据role角色分配权限。

1、创建角色;
~~~
(root@localhost) [(none)]>create role senior_dba,app_dev;
Query OK, 0 rows affected (0.01 sec)
~~~
删除角色，角色被删除后相应授权用户也会移除这个权限：
~~~
(root@localhost) [(none)]>DROP ROLE 'app_dev';
Query OK, 0 rows affected (0.01 sec)
(root@localhost) [(none)]>show grants for leon@'192.168.1.%';
+--------------------------------------------+
| Grants for leon@192.168.1.%                |
+--------------------------------------------+
| GRANT USAGE ON *.* TO `leon`@`192.168.1.%` |
+--------------------------------------------+
1 row in set (0.00 sec)
~~~

2、给角色授权
给senior_dba角色授最高权限;
给app_dev角色授予wp库上的select,insert,update,delete 权限;

~~~
(root@localhost) [(none)]>grant all on *.* to senior_dba with grant option;
Query OK, 0 rows affected (0.01 sec)
(root@localhost) [(none)]>grant select,insert,update,delete on wp.* to app_dev;
Query OK, 0 rows affected (0.00 sec)
~~~

3、创建用户 
创建用户tom@'192.168.1.%' 并给该用户指定senior_dba 角色;
~~~
(root@localhost) [(none)]>create user  tom@'192.168.1.%' identified by '123';
Query OK, 0 rows affected (0.01 sec)
(root@localhost) [(none)]>grant senior_dba to tom@'192.168.1.%';
Query OK, 0 rows affected (0.01 sec)
(root@localhost) [(none)]>
~~~
相反，这样来解除用户的角色：
~~~
REVOKE 'senior_dba' FROM leon@'192.168.1.%';
~~~


4、查看权限
注意show grants 语句查不出详细权限,只能查到用户的角色为senior_dba;后面再加上using senior_dba即可查看具体权限;
~~~
(root@localhost) [(none)]>show grants for tom@'192.168.1.%';
+-----------------------------------------------+
| Grants for tom@192.168.1.%                    |
+-----------------------------------------------+
| GRANT USAGE ON *.* TO `tom`@`192.168.1.%`     |
| GRANT `senior_dba`@`%` TO `tom`@`192.168.1.%` |
+-----------------------------------------------+
2 rows in set (0.00 sec)

(root@localhost) [(none)]>show grants for tom@'192.168.1.%' using senior_dba;
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Grants for tom@192.168.1.%                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, RELOAD, SHUTDOWN, PROCESS, FILE, REFERENCES, INDEX, ALTER, SHOW DATABASES, SUPER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, REPLICATION SLAVE, REPLICATION CLIENT, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, CREATE USER, EVENT, TRIGGER, CREATE TABLESPACE, CREATE ROLE, DROP ROLE ON *.* TO `tom`@`192.168.1.%` WITH GRANT OPTION                                                                                                                                                                                                                    |
| GRANT APPLICATION_PASSWORD_ADMIN,AUDIT_ADMIN,BACKUP_ADMIN,BINLOG_ADMIN,BINLOG_ENCRYPTION_ADMIN,CLONE_ADMIN,CONNECTION_ADMIN,ENCRYPTION_KEY_ADMIN,FLUSH_OPTIMIZER_COSTS,FLUSH_STATUS,FLUSH_TABLES,FLUSH_USER_RESOURCES,GROUP_REPLICATION_ADMIN,INNODB_REDO_LOG_ARCHIVE,INNODB_REDO_LOG_ENABLE,PERSIST_RO_VARIABLES_ADMIN,REPLICATION_APPLIER,REPLICATION_SLAVE_ADMIN,RESOURCE_GROUP_ADMIN,RESOURCE_GROUP_USER,ROLE_ADMIN,SERVICE_CONNECTION_ADMIN,SESSION_VARIABLES_ADMIN,SET_USER_ID,SHOW_ROUTINE,SYSTEM_USER,SYSTEM_VARIABLES_ADMIN,TABLE_ENCRYPTION_ADMIN,XA_RECOVER_ADMIN ON *.* TO `tom`@`192.168.1.%` WITH GRANT OPTION |
| GRANT `senior_dba`@`%` TO `tom`@`192.168.1.%`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.00 sec)
~~~

>基于角色的权限管理在有相同权限用户特别多时非常有用，比如游戏行业。
