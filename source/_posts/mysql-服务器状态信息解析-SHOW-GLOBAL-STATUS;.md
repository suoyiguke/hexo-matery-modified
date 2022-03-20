---
title: mysql-服务器状态信息解析-SHOW-GLOBAL-STATUS;.md
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
title: mysql-服务器状态信息解析-SHOW-GLOBAL-STATUS;.md
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
https://dev.mysql.com/doc/refman/5.7/en/server-status-variables.html#statvar_Aborted_clients


###连接相关

*   [`Aborted_clients`] 由于客户端在没有正确关闭连接的情况下死亡而中止的连接数。参见第B.3.2.9节“通信错误和中断的连接”。

*   [`Aborted_connects`] 尝试连接MySQL服务器失败的次数。参见第B.3.2.9节“通信错误和中断的连接”。

###binlog相关

*   [`Binlog_cache_disk_use`] 使用binlog缓存但超过binlog_cache_size值并使用临时文件存储事务语句的事务数。

*   [`Binlog_cache_use`] 使用binlog缓存的事务数。


*   [`Binlog_stmt_cache_disk_use`] 使用binlog缓存但超过binlog_stmt_cache_size值并使用临时文件存储这些语句的非事务语句数。

*   [`Binlog_stmt_cache_use`] 使用binlog缓存的非事务语句数。


###其它
*   [`Bytes_received`] 从所有客户端接收的字节数。

*   [`Bytes_sent`] 发送到所有客户端的字节数。


###Com_*xxx 统计每种语句的次数
  
>这些变量代表准备好的语句命令。它们的名字指的是网络层使用的COM_xxx命令集。换句话说，每当执行诸如mysql_stmt_prepare()，mysql_stmt_execute()等准备好的语句API调用时，它们的值都会增加。然而，COm _ stmt _ PRESENT、Com_stmt_execute和Com_stmt_close也分别增加了PRESENT、execute或DELACATE PRESENT。此外，对于PRIVATE、execute和DEALLOCATE PREPARE语句，较旧的语句计数器变量Com _ prepare _ sql、Com_execute_sql和Com_dealloc_sql的值会增加。Com_stmt_fetch代表从游标提取时发出的网络往返总数。



1、Com_xxx语句计数器变量指示每个xxx语句被执行的次数。每种类型的语句都有一个状态变量。例如，Com_delete和Com_update分别计数delete和update语句。

2、Com_delete_multi和Com_update_multi类似，但适用于使用多表语法的delete和update语句。

3、如果从查询缓存返回查询结果，服务器将增加Qcache_hits状态变量，而不是Com_select。请参见8.10.3.4章节“查询缓存状态和维护”。

4、即使准备好的语句参数未知或执行过程中出现错误，所有的Com_stmt_xxx变量都会增加。换句话说，它们的值对应于发出的请求数，而不是成功完成的请求数。例如，因为状态变量是为每次服务器启动而初始化的，并且不会在重新启动后持续存在，所以跟踪关机语句的Com_shutdown变量通常具有零值，但是如果关机语句已执行但失败，则该值可以是非零的。


5、Com _ stmt _ reprepare表示在对语句引用的表或视图进行元数据更改后，服务器自动重新表示语句的次数。repar pare操作递增Com _ stmt _ reprepare，也递增Com_stmt_prepare。

6、com _ DELAY _ other表示执行的解释连接语句的数量。参见第8.8.4节“获取命名连接的执行计划信息”。

7、Com_change_repl_filter指示执行的更改复制筛选器语句的数量。
~~~
Com_admin_commands	0
Com_assign_to_keycache	0
Com_alter_db	0
Com_alter_db_upgrade	0
Com_alter_event	0
Com_alter_function	0
Com_alter_instance	0
Com_alter_procedure	0
Com_alter_server	0
Com_alter_table	0
Com_alter_tablespace	0
Com_alter_user	0
Com_analyze	0
Com_begin	0
Com_binlog	0
Com_call_procedure	0
Com_change_db	25
Com_change_master	0
Com_change_repl_filter	0
Com_check	0
Com_checksum	0
Com_commit	0
Com_create_db	0
Com_create_event	0
Com_create_function	0
Com_create_index	0
Com_create_procedure	0
Com_create_server	0
Com_create_table	0
Com_create_trigger	0
Com_create_udf	0
Com_create_user	0
Com_create_view	0
Com_dealloc_sql	0
Com_delete	0
Com_delete_multi	0
Com_do	0
Com_drop_db	0
Com_drop_event	0
Com_drop_function	0
Com_drop_index	0
Com_drop_procedure	0
Com_drop_server	0
Com_drop_table	0
Com_drop_trigger	0
Com_drop_user	0
Com_drop_view	0
Com_empty_query	0
Com_execute_sql	0
Com_explain_other	0
Com_flush	1
Com_get_diagnostics	0
Com_grant	0
Com_ha_close	0
Com_ha_open	0
Com_ha_read	0
Com_help	0
Com_insert	0
Com_insert_select	0
Com_install_plugin	0
Com_kill	0
Com_load	0
Com_lock_tables	0
Com_optimize	0
Com_preload_keys	0
Com_prepare_sql	0
Com_purge	0
Com_purge_before_date	0
Com_release_savepoint	0
Com_rename_table	0
Com_rename_user	0
Com_repair	0
Com_replace	0
Com_replace_select	0
Com_reset	0
Com_resignal	0
Com_revoke	0
Com_revoke_all	0
Com_rollback	0
Com_rollback_to_savepoint	0
Com_savepoint	0
Com_select	26
Com_set_option	17
Com_signal	0
Com_show_binlog_events	0
Com_show_binlogs	0
Com_show_charsets	0
Com_show_collations	0
Com_show_create_db	0
Com_show_create_event	0
Com_show_create_func	0
Com_show_create_proc	0
Com_show_create_table	0
Com_show_create_trigger	0
Com_show_databases	10
Com_show_engine_logs	0
Com_show_engine_mutex	0
Com_show_engine_status	0
Com_show_events	0
Com_show_errors	0
Com_show_fields	0
Com_show_function_code	0
Com_show_function_status	0
Com_show_grants	0
Com_show_keys	0
Com_show_master_status	0
Com_show_open_tables	0
Com_show_plugins	0
Com_show_privileges	0
Com_show_procedure_code	0
Com_show_procedure_status	0
Com_show_processlist	0
Com_show_profile	0
Com_show_profiles	0
Com_show_relaylog_events	0
Com_show_slave_hosts	0
Com_show_slave_status	0
Com_show_status	10
Com_show_storage_engines	0
Com_show_table_status	10
Com_show_tables	1
Com_show_triggers	0
Com_show_variables	2
Com_show_warnings	0
Com_show_create_user	0
Com_shutdown	0
Com_slave_start	0
Com_slave_stop	0
Com_group_replication_start	0
Com_group_replication_stop	0
Com_stmt_execute	0
Com_stmt_close	0
Com_stmt_fetch	0
Com_stmt_prepare	0
Com_stmt_reset	0
Com_stmt_send_long_data	0
Com_truncate	0
Com_uninstall_plugin	0
Com_unlock_tables	0
Com_update	0
Com_update_multi	0
Com_xa_commit	0
Com_xa_end	0
Com_xa_prepare	0
Com_xa_recover	0
Com_xa_rollback	0
Com_xa_start	0
Com_stmt_reprepare	0
~~~
