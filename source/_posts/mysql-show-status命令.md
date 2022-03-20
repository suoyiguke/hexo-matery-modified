---
title: mysql-show-status命令.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: mysql-show-status命令.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
###不同的show status命令
1、服务级别。 `SHOW GLOBAL STATUS` 查看mysql开机以后的所有记录，重启后重新记录
2、连接级别。`SHOW [SESSION 缺省 ] STATUS` 查看mysql此次连接的记录，重新开启连接重新记录
3、sql级别。navicat中执行一条sql，都会有一个`状态`的tab返回集如下。这里就是当前sql的信息了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8f0e5d4c93dda712.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###show status 的结果解析
>Aborted_clients	0
Aborted_connects	0
Binlog_cache_disk_use	0
Binlog_cache_use	0
Binlog_stmt_cache_disk_use	0
Binlog_stmt_cache_use	0
`Bytes_received	6893 客户端发送到服务器的数据(sql语句数据大小)`
`Bytes_sent	871898117  服务器发送的数据（返回结果集数据大小）`
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
Com_change_db	1
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
Com_flush	0
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
Com_select	34
Com_set_option	22
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
Com_show_databases	0
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
Com_show_status	56
Com_show_storage_engines	0
Com_show_table_status	0
Com_show_tables	0
Com_show_triggers	0
Com_show_variables	7
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
Compression	OFF
Connection_errors_accept	0
Connection_errors_internal	0
Connection_errors_max_connections	0
Connection_errors_peer_address	0
Connection_errors_select	0
Connection_errors_tcpwrap	0
Connections	4
Created_tmp_disk_tables	0
Created_tmp_files	4
Created_tmp_tables	63
Delayed_errors	0
Delayed_insert_threads	0
Delayed_writes	0
Flush_commands	1
Handler_commit	6
Handler_delete	0
Handler_discover	0
Handler_external_lock	26
Handler_mrr_init	0
Handler_prepare	0
Handler_read_first	6
Handler_read_key	4779
Handler_read_last	0
Handler_read_next	0
Handler_read_prev	0
Handler_read_rnd	508
Handler_read_rnd_next	6169200
Handler_rollback	0
Handler_savepoint	0
Handler_savepoint_rollback	0
Handler_update	4265
Handler_write	13098
Innodb_buffer_pool_dump_status	Dumping of buffer pool not started
Innodb_buffer_pool_load_status	Buffer pool(s) load completed at 200427 22:59:49
Innodb_buffer_pool_resize_status	
Innodb_buffer_pool_pages_data	7168
Innodb_buffer_pool_bytes_data	117440512
Innodb_buffer_pool_pages_dirty	0
Innodb_buffer_pool_bytes_dirty	0
Innodb_buffer_pool_pages_flushed	54
Innodb_buffer_pool_pages_free	1024
Innodb_buffer_pool_pages_misc	0
Innodb_buffer_pool_pages_total	8192
Innodb_buffer_pool_read_ahead_rnd	0
Innodb_buffer_pool_read_ahead	15098
Innodb_buffer_pool_read_ahead_evicted	600
Innodb_buffer_pool_read_requests	766801
Innodb_buffer_pool_reads	13150
Innodb_buffer_pool_wait_free	0
Innodb_buffer_pool_write_requests	445
Innodb_data_fsyncs	7
Innodb_data_pending_fsyncs	0
Innodb_data_pending_reads	0
Innodb_data_pending_writes	0
Innodb_data_read	462885376
Innodb_data_reads	28306
Innodb_data_writes	71
Innodb_data_written	919552
Innodb_dblwr_pages_written	2
Innodb_dblwr_writes	1
Innodb_log_waits	0
Innodb_log_write_requests	0
Innodb_log_writes	2
Innodb_os_log_fsyncs	4
Innodb_os_log_pending_fsyncs	0
Innodb_os_log_pending_writes	0
Innodb_os_log_written	1024
Innodb_page_size	16384
Innodb_pages_created	35
Innodb_pages_read	28247
Innodb_pages_written	54
Innodb_row_lock_current_waits	0
Innodb_row_lock_time	0
Innodb_row_lock_time_avg	0
Innodb_row_lock_time_max	0
Innodb_row_lock_waits	0
Innodb_rows_deleted	0
Innodb_rows_inserted	90
Innodb_rows_read	6152540
Innodb_rows_updated	0
Innodb_num_open_files	50
Innodb_truncated_status_writes	0
Innodb_available_undo_logs	128
Key_blocks_not_flushed	0
Key_blocks_unused	6695
Key_blocks_used	3
Key_read_requests	6
Key_reads	3
Key_write_requests	0
Key_writes	0
Last_query_cost	12.499000
Last_query_partial_plans	1
Locked_connects	0
Max_execution_time_exceeded	0
Max_execution_time_set	0
Max_execution_time_set_failed	0
Max_used_connections	2
Max_used_connections_time	2020-04-27 23:06:18
Not_flushed_delayed_rows	0
Ongoing_anonymous_transaction_count	0
Open_files	17
Open_streams	0
Open_table_definitions	109
Open_tables	106
Opened_files	147
Opened_table_definitions	1
Opened_tables	2
Performance_schema_accounts_lost	0
Performance_schema_cond_classes_lost	0
Performance_schema_cond_instances_lost	0
Performance_schema_digest_lost	0
Performance_schema_file_classes_lost	0
Performance_schema_file_handles_lost	0
Performance_schema_file_instances_lost	0
Performance_schema_hosts_lost	0
Performance_schema_index_stat_lost	0
Performance_schema_locker_lost	0
Performance_schema_memory_classes_lost	0
Performance_schema_metadata_lock_lost	0
Performance_schema_mutex_classes_lost	0
Performance_schema_mutex_instances_lost	0
Performance_schema_nested_statement_lost	0
Performance_schema_prepared_statements_lost	0
Performance_schema_program_lost	0
Performance_schema_rwlock_classes_lost	0
Performance_schema_rwlock_instances_lost	0
Performance_schema_session_connect_attrs_lost	0
Performance_schema_socket_classes_lost	0
Performance_schema_socket_instances_lost	0
Performance_schema_stage_classes_lost	0
Performance_schema_statement_classes_lost	0
Performance_schema_table_handles_lost	0
Performance_schema_table_instances_lost	0
Performance_schema_table_lock_stat_lost	0
Performance_schema_thread_classes_lost	0
Performance_schema_thread_instances_lost	0
Performance_schema_users_lost	0
Prepared_stmt_count	0
Qcache_free_blocks	1
Qcache_free_memory	67091648
Qcache_hits	0
Qcache_inserts	0
Qcache_lowmem_prunes	0
Qcache_not_cached	44
Qcache_queries_in_cache	0
Qcache_total_blocks	1
Queries	151
Questions	124
Select_full_join	0
Select_full_range_join	0
Select_range	0
Select_range_check	0
Select_scan	48
Slave_open_temp_tables	0
Slow_launch_threads	0
Slow_queries	0
Sort_merge_passes	0
Sort_range	0
Sort_rows	508
Sort_scan	28
Ssl_accept_renegotiates	0
Ssl_accepts	0
Ssl_callback_cache_hits	0
Ssl_cipher	
Ssl_cipher_list	
Ssl_client_connects	0
Ssl_connect_renegotiates	0
Ssl_ctx_verify_depth	0
Ssl_ctx_verify_mode	0
Ssl_default_timeout	0
Ssl_finished_accepts	0
Ssl_finished_connects	0
Ssl_server_not_after	
Ssl_server_not_before	
Ssl_session_cache_hits	0
Ssl_session_cache_misses	0
Ssl_session_cache_mode	NONE
Ssl_session_cache_overflows	0
Ssl_session_cache_size	0
Ssl_session_cache_timeouts	0
Ssl_sessions_reused	0
Ssl_used_session_cache_entries	0
Ssl_verify_depth	0
Ssl_verify_mode	0
Ssl_version	
Table_locks_immediate	161
Table_locks_waited	0
Table_open_cache_hits	11
Table_open_cache_misses	2
Table_open_cache_overflows	0
Tc_log_max_pages_used	0
Tc_log_page_size	0
Tc_log_page_waits	0
Threads_cached	0
Threads_connected	2
Threads_created	2
Threads_running	1
Uptime	894
Uptime_since_flush_status	894


~~~
Bytes_received
~~~
###常用的:

--查看查询时间超过long_query_time秒的查询的个数。

show status like 'slow_queries';

--查看创建时间超过slow_launch_time秒的线程数。

show status like 'slow_launch_threads';

--查看不能立即获得的表的锁的次数。如果该值较高，并且有性能问题，你应首先优化查询，然后拆分表或使用复制。

show status like 'table_locks_waited';

--查看立即获得的表的锁的次数。

show status like 'table_locks_immediate';

--查看激活的(非睡眠状态)线程数。

show status like 'threads_running';

--查看创建用来处理连接的线程数。如果Threads_created较大，你可能要增加thread_cache_size值。

show status like 'threads_created';

--查看当前打开的连接的数量。

show status like 'threads_connected';

--查看线程缓存内的线程的数量。

show status like 'threads_cached';

--查看试图连接到MySQL(不管是否连接成功)的连接数

show status like 'connections';

--查看delete语句的执行数

show [global] status like 'com_delete';

--查看update语句的执行数

show [global] status like 'com_update';

--查看insert语句的执行数

show [global] status like 'com_insert';

--查看select语句的执行数

show [global] status like 'com_select';

--查看MySQL本次启动后的运行时间(单位：秒)

show status like 'uptime';


###详细信息
http://blog.sina.com.cn/s/blog_68baf43d0100vu2x.html
