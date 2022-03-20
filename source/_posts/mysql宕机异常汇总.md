---
title: mysql宕机异常汇总.md
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
title: mysql宕机异常汇总.md
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
1、用着用着宕机
~~~
2021-04-21T04:03:38.303917Z 96 [Note] Access denied for user 'root'@'localhost' (using password: NO)
2021-04-21T10:17:36.764323Z 0 [ERROR] InnoDB: Operating system error number 8 in a file operation.
2021-04-21T10:17:36.765323Z 0 [Note] InnoDB: Some operating system error numbers are described at http://dev.mysql.com/doc/refman/5.7/en/operating-system-error-codes.html
2021-04-21T10:17:36.789324Z 0 [ERROR] InnoDB: File (unknown): 'flush' returned OS error 108. Cannot continue operation
2021-04-21T10:17:36.795325Z 0 [ERROR] InnoDB: Cannot continue operation.
2021-04-21T10:17:39.229464Z 0 [Note] InnoDB: FTS optimize thread exiting.
2021-04-21T10:19:16.918052Z 0 [Warning] InnoDB: 4 threads created by InnoDB had not exited at shutdown!
2021-04-21T10:48:54.494723Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2021-04-21T10:48:54.496723Z 0 [Warning] 'NO_ZERO_DATE', 'NO_ZERO_IN_DATE' and 'ERROR_FOR_DIVISION_BY_ZERO' sql modes should be used with strict mode. They will be merged with strict mode in a future release.
2021-04-21T10:48:54.496723Z 0 [Warning] 'NO_AUTO_CREATE_USER' sql mode was not set.
2021-04-21T10:48:54.496723Z 0 [Note] --secure-file-priv is set to NULL. Operations related to importing and exporting data are disabled
2021-04-21T10:48:54.497723Z 0 [Note] MySQL (mysqld 5.7.19) starting as process 1976 ...
2021-04-21T10:48:54.572728Z 0 [Note] InnoDB: Mutexes and rw_locks use Windows interlocked functions
2021-04-21T10:48:54.572728Z 0 [Note] InnoDB: Uses event mutexes
2021-04-21T10:48:54.573728Z 0 [Note] InnoDB: _mm_lfence() and _mm_sfence() are used for memory barrier
2021-04-21T10:48:54.573728Z 0 [Note] InnoDB: Compressed tables use zlib 1.2.3
2021-04-21T10:48:54.580728Z 0 [Note] InnoDB: Number of pools: 1
2021-04-21T10:48:54.584728Z 0 [Note] InnoDB: Not using CPU crc32 instructions
2021-04-21T10:48:54.590729Z 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2021-04-21T10:48:54.605729Z 0 [Note] InnoDB: Completed initialization of buffer pool
2021-04-21T10:48:54.641732Z 0 [Note] InnoDB: Highest supported file format is Barracuda.
2021-04-21T10:48:54.647732Z 0 [Note] InnoDB: Log scan progressed past the checkpoint lsn 33582134503
2021-04-21T10:48:54.648732Z 0 [Note] InnoDB: Doing recovery: scanned up to log sequence number 33582134619
2021-04-21T10:48:54.682734Z 0 [Note] InnoDB: Database was not shutdown normally!
2021-04-21T10:48:54.682734Z 0 [Note] InnoDB: Starting crash recovery.
2021-04-21T10:48:55.249766Z 0 [Note] InnoDB: Removed temporary tablespace data file: "ibtmp1"
2021-04-21T10:48:55.250766Z 0 [Note] InnoDB: Creating shared tablespace for temporary tables
2021-04-21T10:48:55.252766Z 0 [Note] InnoDB: Setting file '.\ibtmp1' size to 12 MB. Physically writing the file full; Please wait ...
2021-04-21T10:48:55.301769Z 0 [Note] InnoDB: File '.\ibtmp1' size is now 12 MB.
2021-04-21T10:48:55.304769Z 0 [Note] InnoDB: 96 redo rollback segment(s) found. 96 redo rollback segment(s) are active.
2021-04-21T10:48:55.305769Z 0 [Note] InnoDB: 32 non-redo rollback segment(s) are active.
2021-04-21T10:48:55.306770Z 0 [Note] InnoDB: Waiting for purge to start
2021-04-21T10:48:55.357772Z 0 [Note] InnoDB: 5.7.19 started; log sequence number 33582134619
2021-04-21T10:48:55.358773Z 0 [Note] InnoDB: Loading buffer pool(s) from D:\ca\mysql-5.7.19-winx64\data\ib_buffer_pool
2021-04-21T10:48:55.359773Z 0 [Note] Plugin 'FEDERATED' is disabled.
2021-04-21T10:48:55.389774Z 0 [Warning] Failed to set up SSL because of the following SSL library error: SSL context is not usable without certificate and private key
2021-04-21T10:48:55.389774Z 0 [Note] Server hostname (bind-address): '*'; port: 3306
2021-04-21T10:48:55.391774Z 0 [Note] IPv6 is available.
2021-04-21T10:48:55.392774Z 0 [Note]   - '::' resolves to '::';
2021-04-21T10:48:55.393775Z 0 [Note] Server socket created on IP: '::'.
2021-04-21T10:48:55.528782Z 0 [Note] InnoDB: Buffer pool(s) load completed at 210421 18:48:55
2021-04-21T10:48:55.672790Z 0 [Note] Event Scheduler: Loaded 0 events
2021-04-21T10:48:55.673791Z 0 [Note] MySQL: ready for connections.
Version: '5.7.19'  socket: ''  port: 3306  MySQL Community Server (GPL)
2021-04-21T10:48:55.674791Z 0 [Note] Executing 'SELECT * FROM INFORMATION_SCHEMA.TABLES;' to get a list of tables using the deprecated partition engine. You may use the startup option '--disable-partition-engine-check' to skip this check. 
2021-04-21T10:48:55.675791Z 0 [Note] Beginning of list of non-natively partitioned tables
2021-04-21T10:48:55.932805Z 0 [Note] End of list of non-natively partitioned tables
2021-04-21T13:50:22.388475Z 0 [ERROR] Can't create thread to handle new connection(errno= 1)
2021-04-21T13:50:27.592773Z 7 [ERROR] InnoDB: os_file_get_status_win32: Failed to get the volume path name for: .\iam\biz_ukey_sign_details.frm- OS error number 8
2021-04-21T13:50:27.593773Z 7 [ERROR] MySQL: Out of memory (Needed 11528 bytes)
2021-04-21T13:50:27.593773Z 7 [ERROR] MySQL: Out of memory (Needed 5968 bytes)
2021-04-21T13:51:06.354990Z 5 [ERROR] InnoDB: Cannot allocate 1064984 bytes of memory after 60 retries over 60 seconds. OS error: Not enough space (12). Check if you should increase the swap file or ulimits of your operating system. Note that on most 32-bit computers the process memory space is limited to 2 GB or 4 GB.
2021-04-21 21:51:06 0xec0  InnoDB: Assertion failure in thread 3776 in file ut0ut.cc line 931
InnoDB: Failing assertion: !m_fatal
InnoDB: We intentionally generate a memory trap.
InnoDB: Submit a detailed bug report to http://bugs.mysql.com.
InnoDB: If you get repeated assertion failures or crashes, even
InnoDB: immediately after the mysqld startup, there may be
InnoDB: corruption in the InnoDB tablespace. Please refer to
InnoDB: http://dev.mysql.com/doc/refman/5.7/en/forcing-innodb-recovery.html
InnoDB: about forcing recovery.
13:51:06 UTC - mysqld got exception 0x80000003 ;
This could be because you hit a bug. It is also possible that this binary
or one of the libraries it was linked against is corrupt, improperly built,
or misconfigured. This error can also be caused by malfunctioning hardware.
Attempting to collect some information that could help diagnose the problem.
As this is a crash and something is definitely wrong, the information
collection process might fail.

key_buffer_size=8388608
read_buffer_size=131072
max_used_connections=6
max_threads=200
thread_count=6
connection_count=6
It is possible that mysqld could use up to 
key_buffer_size + (read_buffer_size + sort_buffer_size)*max_threads = 87423 K  bytes of memory
Hope that's ok; if not, decrease some variables in the equation.

Thread pointer: 0x13773430
Attempting backtrace. You can use the following information to find out
where mysqld died. If you see no messages after this, something went
terribly wrong...
1404e75d2    
7fee67bee1d    
16    
7fe046e088a    
2    
77c8bcba    
140bcfdba    
7fee677eb8d    
188bb488    
1    
100    
140bd7ef0    
140bcfdba    
7fee67c4a14    
7fe00000001    
100000000    
ec0    
3a3    
140bcfdba    
140603e74    
7fee682c4a0    
ec0    
3a3    
140bcfdba    
3a3    

Trying to get some variables.
Some pointers may be invalid and cause the dump to abort.
Query (13981d20): INSERT INTO BIZ_UKEY_SIGN_DETAILS(`id`, `base64_source_data`, `source_data`, `cert_id`, `signed_data`, `timestamp`) VALUES(417079, 'ew0KIjIwMjEwNDIxIDA5OjQ4ICAgICAgICAgICAgICAgICAgICDmnK_liY3orqjorroKICAgIOiuqOiuuuaXpeacn--8mjIwMjEwNDIxIDA5OjQ5CiAgICDkuLsg5oyBIOS6uu-8muWImOWkp-azouS4u-S7u-WMu-W4iAogICAg5Y-C5LiO6K6o6K665Lq65ZGY77ya6ZKf5bu65paH5Li75Lu75Yy75biI44CB56iL6LaF5Ymv5Li75Lu75Yy75biI44CB5LuH5Lmm6KaB5Ymv5Li75Lu75Yy75biI44CB5ZGo5a6c6b6Z5Ymv5Li75Lu75Yy75biI44CB6aG65oiQ5Li75rK75Yy75biI44CB5p2o5p2O5by65L2P6Zmi5Yy75biI44CB6ZmI5YWw5L2P6Zmi5Yy75biI44CB5pm65pWP5oqk5aOr6ZW_44CB6buE6ZSm6bi_5oqk5biICiAgICDmiYvmnK_nuqfliKvvvJrkuInnuqcKICAgIOakjeWFpeexu-WMu-eUqOiAl-adkOS9v-eUqOaDheWGte-8muaXoAogICAg6K6h5YiS5YiG5qyh6L-b6KGM5omL5pyv77ya5ZCmCiAgICDorqjorrrmgLvnu5PvvJrnu4_ov4forqjorrrvvIznu5PlkIjmgqPlhL_nl4fnirbjgIHkvZPlvoHjgIHovoXliqnmo4Dmn6XvvIzmnK_liY3or4rmlq3kuLrvvJox44CB5omB5qGD5L2T6IKl5aSn5Ly05pyJ6IW65qC35L2T6IKl5aSnMuOAgemYu-WhnuaAp-edoeecoOWRvOWQuOaaguWBnOe7vOWQiOW-gSjvvJ8p77yb55Sx5LqO5oKj5YS_5Li05bqK55eH54q25piO
Connection ID (thread ID): 5
Status: NOT_KILLED

The manual page at http://dev.mysql.com/doc/mysql/en/crashing.html contains
information that should help you find out what is causing the crash.
2021-04-21T14:13:18.051158Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2021-04-21T14:13:18.054159Z 0 [Warning] 'NO_ZERO_DATE', 'NO_ZERO_IN_DATE' and 'ERROR_FOR_DIVISION_BY_ZERO' sql modes should be used with strict mode. They will be merged with strict mode in a future release.
2021-04-21T14:13:18.054159Z 0 [Warning] 'NO_AUTO_CREATE_USER' sql mode was not set.
2021-04-21T14:13:18.054159Z 0 [Note] --secure-file-priv is set to NULL. Operations related to importing and exporting data are disabled
2021-04-21T14:13:18.056159Z 0 [Note] MySQL (mysqld 5.7.19) starting as process 3208 ...
2021-04-21T14:13:18.321174Z 0 [Note] InnoDB: Mutexes and rw_locks use Windows interlocked functions
2021-04-21T14:13:18.322174Z 0 [Note] InnoDB: Uses event mutexes
2021-04-21T14:13:18.322174Z 0 [Note] InnoDB: _mm_lfence() and _mm_sfence() are used for memory barrier
2021-04-21T14:13:18.323174Z 0 [Note] InnoDB: Compressed tables use zlib 1.2.3
2021-04-21T14:13:18.352176Z 0 [Note] InnoDB: Number of pools: 1
2021-04-21T14:13:18.360176Z 0 [Note] InnoDB: Not using CPU crc32 instructions
2021-04-21T14:13:18.372177Z 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2021-04-21T14:13:18.381177Z 0 [Note] InnoDB: VirtualAlloc(137297920 bytes) failed; Windows error 1455
2021-04-21T14:13:18.382177Z 0 [ERROR] InnoDB: Cannot allocate memory for the buffer pool
2021-04-21T14:13:18.382177Z 0 [ERROR] InnoDB: Plugin initialization aborted with error Generic error
2021-04-21T14:13:18.383177Z 0 [ERROR] Plugin 'InnoDB' init function returned error.
2021-04-21T14:13:18.384177Z 0 [ERROR] Plugin 'InnoDB' registration as a STORAGE ENGINE failed.
2021-04-21T14:13:18.384177Z 0 [ERROR] Failed to initialize plugins.
2021-04-21T14:13:18.384177Z 0 [ERROR] Aborting

2021-04-21T14:13:18.387178Z 0 [Note] Binlog end
2021-04-21T14:13:18.400178Z 0 [Note] Shutting down plugin 'CSV'
2021-04-21T14:13:18.411179Z 0 [Note] MySQL: Shutdown complete

2021-04-21T14:13:25.755599Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2021-04-21T14:13:25.758599Z 0 [Warning] 'NO_ZERO_DATE', 'NO_ZERO_IN_DATE' and 'ERROR_FOR_DIVISION_BY_ZERO' sql modes should be used with strict mode. They will be merged with strict mode in a future release.
2021-04-21T14:13:25.758599Z 0 [Warning] 'NO_AUTO_CREATE_USER' sql mode was not set.
2021-04-21T14:13:25.758599Z 0 [Note] --secure-file-priv is set to NULL. Operations related to importing and exporting data are disabled
2021-04-21T14:13:25.759599Z 0 [Note] MySQL (mysqld 5.7.19) starting as process 3720 ...
2021-04-21T14:13:25.802602Z 0 [Note] InnoDB: Mutexes and rw_locks use Windows interlocked functions
2021-04-21T14:13:25.802602Z 0 [Note] InnoDB: Uses event mutexes
2021-04-21T14:13:25.803602Z 0 [Note] InnoDB: _mm_lfence() and _mm_sfence() are used for memory barrier
2021-04-21T14:13:25.803602Z 0 [Note] InnoDB: Compressed tables use zlib 1.2.3
2021-04-21T14:13:25.809602Z 0 [Note] InnoDB: Number of pools: 1
2021-04-21T14:13:25.813602Z 0 [Note] InnoDB: Not using CPU crc32 instructions
2021-04-21T14:13:25.820603Z 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2021-04-21T14:13:25.821603Z 0 [Note] InnoDB: VirtualAlloc(137297920 bytes) failed; Windows error 1455
2021-04-21T14:13:25.822603Z 0 [ERROR] InnoDB: Cannot allocate memory for the buffer pool
2021-04-21T14:13:25.823603Z 0 [ERROR] InnoDB: Plugin initialization aborted with error Generic error
2021-04-21T14:13:25.823603Z 0 [ERROR] Plugin 'InnoDB' init function returned error.
2021-04-21T14:13:25.824603Z 0 [ERROR] Plugin 'InnoDB' registration as a STORAGE ENGINE failed.
2021-04-21T14:13:25.824603Z 0 [ERROR] Failed to initialize plugins.
2021-04-21T14:13:25.825603Z 0 [ERROR] Aborting

2021-04-21T14:13:25.825603Z 0 [Note] Binlog end
2021-04-21T14:13:25.828603Z 0 [Note] Shutting down plugin 'CSV'
2021-04-21T14:13:25.832603Z 0 [Note] MySQL: Shutdown complete

2021-04-21T14:16:41.927819Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2021-04-21T14:16:41.931820Z 0 [Warning] 'NO_ZERO_DATE', 'NO_ZERO_IN_DATE' and 'ERROR_FOR_DIVISION_BY_ZERO' sql modes should be used with strict mode. They will be merged with strict mode in a future release.
2021-04-21T14:16:41.931820Z 0 [Warning] 'NO_AUTO_CREATE_USER' sql mode was not set.
2021-04-21T14:16:41.931820Z 0 [Note] --secure-file-priv is set to NULL. Operations related to importing and exporting data are disabled
2021-04-21T14:16:41.934820Z 0 [Note] MySQL (mysqld 5.7.19) starting as process 1252 ...
2021-04-21T14:16:42.016825Z 0 [Note] InnoDB: Mutexes and rw_locks use Windows interlocked functions
2021-04-21T14:16:42.016825Z 0 [Note] InnoDB: Uses event mutexes
2021-04-21T14:16:42.017825Z 0 [Note] InnoDB: _mm_lfence() and _mm_sfence() are used for memory barrier
2021-04-21T14:16:42.017825Z 0 [Note] InnoDB: Compressed tables use zlib 1.2.3
2021-04-21T14:16:42.025825Z 0 [Note] InnoDB: Number of pools: 1
2021-04-21T14:16:42.031825Z 0 [Note] InnoDB: Not using CPU crc32 instructions
2021-04-21T14:16:42.039826Z 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2021-04-21T14:16:42.044826Z 0 [Note] InnoDB: VirtualAlloc(137297920 bytes) failed; Windows error 1455
2021-04-21T14:16:42.045826Z 0 [ERROR] InnoDB: Cannot allocate memory for the buffer pool
2021-04-21T14:16:42.045826Z 0 [ERROR] InnoDB: Plugin initialization aborted with error Generic error
2021-04-21T14:16:42.046826Z 0 [ERROR] Plugin 'InnoDB' init function returned error.
2021-04-21T14:16:42.047826Z 0 [ERROR] Plugin 'InnoDB' registration as a STORAGE ENGINE failed.
2021-04-21T14:16:42.047826Z 0 [ERROR] Failed to initialize plugins.
2021-04-21T14:16:42.048826Z 0 [ERROR] Aborting

2021-04-21T14:16:42.049826Z 0 [Note] Binlog end
2021-04-21T14:16:42.051827Z 0 [Note] Shutting down plugin 'CSV'
2021-04-21T14:16:42.054827Z 0 [Note] MySQL: Shutdown complete

2021-04-21T14:21:10.833430Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2021-04-21T14:21:10.833430Z 0 [Warning] 'NO_ZERO_DATE', 'NO_ZERO_IN_DATE' and 'ERROR_FOR_DIVISION_BY_ZERO' sql modes should be used with strict mode. They will be merged with strict mode in a future release.
2021-04-21T14:21:10.833430Z 0 [Warning] 'NO_AUTO_CREATE_USER' sql mode was not set.
2021-04-21T14:21:10.833430Z 0 [Note] --secure-file-priv is set to NULL. Operations related to importing and exporting data are disabled
2021-04-21T14:21:10.833430Z 0 [Note] MySQL (mysqld 5.7.19) starting as process 1696 ...
2021-04-21T14:21:10.927030Z 0 [Note] InnoDB: Mutexes and rw_locks use Windows interlocked functions
2021-04-21T14:21:10.927030Z 0 [Note] InnoDB: Uses event mutexes
2021-04-21T14:21:10.927030Z 0 [Note] InnoDB: _mm_lfence() and _mm_sfence() are used for memory barrier
2021-04-21T14:21:10.927030Z 0 [Note] InnoDB: Compressed tables use zlib 1.2.3
2021-04-21T14:21:10.927030Z 0 [Note] InnoDB: Number of pools: 1
2021-04-21T14:21:10.927030Z 0 [Note] InnoDB: Not using CPU crc32 instructions
2021-04-21T14:21:10.942630Z 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2021-04-21T14:21:10.958230Z 0 [Note] InnoDB: Completed initialization of buffer pool
2021-04-21T14:21:11.005030Z 0 [Note] InnoDB: Highest supported file format is Barracuda.
2021-04-21T14:21:11.005030Z 0 [Note] InnoDB: Log scan progressed past the checkpoint lsn 33614271533
2021-04-21T14:21:11.005030Z 0 [Note] InnoDB: Doing recovery: scanned up to log sequence number 33614271542
2021-04-21T14:21:11.005030Z 0 [Note] InnoDB: Database was not shutdown normally!
2021-04-21T14:21:11.005030Z 0 [Note] InnoDB: Starting crash recovery.
2021-04-21T14:21:11.254631Z 0 [Note] InnoDB: 5 transaction(s) which must be rolled back or cleaned up in total 6 row operations to undo
2021-04-21T14:21:11.254631Z 0 [Note] InnoDB: Trx id counter is 3358976
2021-04-21T14:21:11.772432Z 0 [Note] InnoDB: Starting in background the rollback of uncommitted transactions
2021-04-21T14:21:11.772432Z 0 [Note] InnoDB: Removed temporary tablespace data file: "ibtmp1"
2021-04-21T14:21:11.772432Z 0 [Note] InnoDB: Rolling back trx with id 3358513, 1 rows to undo
2021-04-21T14:21:11.772432Z 0 [Note] InnoDB: Creating shared tablespace for temporary tables
2021-04-21T14:21:11.772432Z 0 [Note] InnoDB: Setting file '.\ibtmp1' size to 12 MB. Physically writing the file full; Please wait ...
2021-04-21T14:21:11.772432Z 0 [Note] InnoDB: Rollback of trx with id 3358513 completed
2021-04-21T14:21:11.772432Z 0 [Note] InnoDB: Rolling back trx with id 3358507, 1 rows to undo
2021-04-21T14:21:11.772432Z 0 [Note] InnoDB: Rollback of trx with id 3358507 completed
2021-04-21T14:21:11.772432Z 0 [Note] InnoDB: Rolling back trx with id 3358503, 1 rows to undo
2021-04-21T14:21:11.788032Z 0 [Note] InnoDB: Rollback of trx with id 3358503 completed
2021-04-21T14:21:11.788032Z 0 [Note] InnoDB: Rolling back trx with id 3358500, 1 rows to undo
2021-04-21T14:21:11.788032Z 0 [Note] InnoDB: Rollback of trx with id 3358500 completed
2021-04-21T14:21:11.788032Z 0 [Note] InnoDB: Rolling back trx with id 3358499, 2 rows to undo
2021-04-21T14:21:11.788032Z 0 [Note] InnoDB: Rollback of trx with id 3358499 completed
2021-04-21T14:21:11.788032Z 0 [Note] InnoDB: Rollback of non-prepared transactions completed
2021-04-21T14:21:11.819232Z 0 [Note] InnoDB: File '.\ibtmp1' size is now 12 MB.
2021-04-21T14:21:11.834832Z 0 [Note] InnoDB: 96 redo rollback segment(s) found. 96 redo rollback segment(s) are active.
2021-04-21T14:21:11.834832Z 0 [Note] InnoDB: 32 non-redo rollback segment(s) are active.
2021-04-21T14:21:11.834832Z 0 [Note] InnoDB: Waiting for purge to start
2021-04-21T14:21:11.897232Z 0 [Note] InnoDB: 5.7.19 started; log sequence number 33614271542
2021-04-21T14:21:11.897232Z 0 [Note] InnoDB: Loading buffer pool(s) from D:\ca\mysql-5.7.19-winx64\data\ib_buffer_pool
2021-04-21T14:21:11.897232Z 0 [Note] Plugin 'FEDERATED' is disabled.
2021-04-21T14:21:11.928432Z 0 [Warning] Failed to set up SSL because of the following SSL library error: SSL context is not usable without certificate and private key
2021-04-21T14:21:11.928432Z 0 [Note] Server hostname (bind-address): '*'; port: 3306
2021-04-21T14:21:11.928432Z 0 [Note] IPv6 is available.
2021-04-21T14:21:11.928432Z 0 [Note]   - '::' resolves to '::';
2021-04-21T14:21:11.928432Z 0 [Note] Server socket created on IP: '::'.
2021-04-21T14:21:12.084432Z 0 [Note] InnoDB: Buffer pool(s) load completed at 210421 22:21:12
2021-04-21T14:21:12.131232Z 0 [Note] Event Scheduler: Loaded 0 events
2021-04-21T14:21:12.131232Z 0 [Note] MySQL: ready for connections.
Version: '5.7.19'  socket: ''  port: 3306  MySQL Community Server (GPL)
2021-04-21T14:21:12.131232Z 0 [Note] Executing 'SELECT * FROM INFORMATION_SCHEMA.TABLES;' to get a list of tables using the deprecated partition engine. You may use the startup option '--disable-partition-engine-check' to skip this check. 
2021-04-21T14:21:12.131232Z 0 [Note] Beginning of list of non-natively partitioned tables
2021-04-21T14:21:12.349633Z 0 [Note] End of list of non-natively partitioned tables
2021-04-21T14:22:11.843530Z 3 [Note] Aborted connection 3 to db: 'iam' user: 'root' host: 'localhost' (Got an error reading communication packets)
2021-04-21T14:22:11.843530Z 4 [Note] Aborted connection 4 to db: 'iam' user: 'root' host: 'localhost' (Got an error reading communication packets)
2021-04-21T14:22:11.843530Z 5 [Note] Aborted connection 5 to db: 'iam' user: 'root' host: 'localhost' (Got an error reading communication packets)
2021-04-21T14:22:11.843530Z 7 [Note] Aborted connection 7 to db: 'iam' user: 'root' host: 'localhost' (Got an error reading communication packets)
2021-04-21T14:22:11.843530Z 8 [Note] Aborted connection 8 to db: 'iam' user: 'root' host: 'localhost' (Got an error reading communication packets)
2021-04-21T14:22:11.843530Z 6 [Note] Aborted connection 6 to db: 'iam' user: 'root' host: 'localhost' (Got an error reading communication packets)
2021-04-21T14:22:11.843530Z 9 [Note] Aborted connection 9 to db: 'iam' user: 'root' host: 'localhost' (Got an error reading communication packets)
2021-04-21T14:22:11.843530Z 10 [Note] Aborted connection 10 to db: 'iam' user: 'root' host: 'localhost' (Got an error reading communication packets)
2021-04-21T14:22:11.843530Z 11 [Note] Aborted connection 11 to db: 'iam' user: 'root' host: 'localhost' (Got an error reading communication packets)
2021-04-21T14:22:11.843530Z 12 [Note] Aborted connection 12 to db: 'iam' user: 'root' host: 'localhost' (Got an error reading communication packets)
2021-04-21T22:22:30.903056Z 13 [Note] Aborted connection 13 to db: 'unconnected' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:22:31.020063Z 14 [Note] Aborted connection 14 to db: 'iam' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:22:31.032063Z 15 [Note] Aborted connection 15 to db: 'iam' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:22:31.035063Z 16 [Note] Aborted connection 16 to db: 'iam' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:22:31.039064Z 17 [Note] Aborted connection 17 to db: 'iam' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:22:31.043064Z 18 [Note] Aborted connection 18 to db: 'iam' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:22:31.047064Z 19 [Note] Aborted connection 19 to db: 'iam' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:22:31.051064Z 20 [Note] Aborted connection 20 to db: 'iam' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:22:31.055065Z 21 [Note] Aborted connection 21 to db: 'iam' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:22:31.059065Z 22 [Note] Aborted connection 22 to db: 'iam' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:22:33.676215Z 24 [Note] Aborted connection 24 to db: 'iam' user: 'root' host: 'localhost' (Got timeout reading communication packets)
2021-04-21T22:29:24.023685Z 26 [Note] Aborted connection 26 to db: 'mysql' user: 'root' host: 'localhost' (Got timeout reading communication packets)

~~~

南医大
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2e6623f67df613d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

windows server 2008 r2 enterprise
