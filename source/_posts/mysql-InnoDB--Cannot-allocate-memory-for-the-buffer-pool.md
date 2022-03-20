---
title: mysql-InnoDB--Cannot-allocate-memory-for-the-buffer-pool.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
---
title: mysql-InnoDB--Cannot-allocate-memory-for-the-buffer-pool.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql底层
categories: mysql底层
---
服务器内存过小，mysql默认分配给 buffer pool的innodb_buffer_pool_size大小是 128M 134217728 字节。
若机器当前状态的空闲内存少于这个值，那么会报错  Cannot allocate memory for the buffer pool

我们可以将innodb_buffer_pool_size 适当调小即可
innodb_buffer_pool_size = 


~~~
2020-06-18 20:26:08 0x25f4  InnoDB: Assertion failure in thread 9716 in file ut0ut.cc line 931
InnoDB: Failing assertion: !m_fatal
InnoDB: We intentionally generate a memory trap.
InnoDB: Submit a detailed bug report to http://bugs.mysql.com.
InnoDB: If you get repeated assertion failures or crashes, even
InnoDB: immediately after the mysqld startup, there may be
InnoDB: corruption in the InnoDB tablespace. Please refer to
InnoDB: http://dev.mysql.com/doc/refman/5.7/en/forcing-innodb-recovery.html
InnoDB: about forcing recovery.
12:26:08 UTC - mysqld got exception 0x80000003 ;
This could be because you hit a bug. It is also possible that this binary
or one of the libraries it was linked against is corrupt, improperly built,
or misconfigured. This error can also be caused by malfunctioning hardware.
Attempting to collect some information that could help diagnose the problem.
As this is a crash and something is definitely wrong, the information
collection process might fail.

key_buffer_size=8388608
read_buffer_size=131072
max_used_connections=14
max_threads=200
thread_count=2
connection_count=2
It is possible that mysqld could use up to 
key_buffer_size + (read_buffer_size + sort_buffer_size)*max_threads = 87423 K  bytes of memory
Hope that's ok; if not, decrease some variables in the equation.

Thread pointer: 0x13b5eec0
Attempting backtrace. You can use the following information to find out
where mysqld died. If you see no messages after this, something went
terribly wrong...
13fed75d2    mysqld.exe!???
7feeebaee1d    MSVCR120.dll!???
7feeebb4a14    MSVCR120.dll!???
13fff3e74    mysqld.exe!???
13fff40ef    mysqld.exe!???
13ff1a7a9    mysqld.exe!???
14001db36    mysqld.exe!???
14001b008    mysqld.exe!???
14000c0b8    mysqld.exe!???
14000b98a    mysqld.exe!???
14005b545    mysqld.exe!???
14010a00c    mysqld.exe!???
140109884    mysqld.exe!???
14010bcd7    mysqld.exe!???
14010c116    mysqld.exe!???
1401082e0    mysqld.exe!???
14010ddda    mysqld.exe!???
140077720    mysqld.exe!???
13ff355fd    mysqld.exe!???
13f79b480    mysqld.exe!???
13f99799e    mysqld.exe!???
13f995488    mysqld.exe!???
13f994623    mysqld.exe!???
13f7c6f85    mysqld.exe!???
13f7c98a3    mysqld.exe!???
13f7c2953    mysqld.exe!???
13f7c398a    mysqld.exe!???
13f76a4dc    mysqld.exe!???
1401c43a2    mysqld.exe!???
13fed743c    mysqld.exe!???
7feeeb64f7f    MSVCR120.dll!???
7feeeb65126    MSVCR120.dll!???
77af59cd    kernel32.dll!???
77c2a561    ntdll.dll!???

Trying to get some variables.
Some pointers may be invalid and cause the dump to abort.
Query (13bfbce0): INSERT INTO TLK_SIGNED_DATA(ID,Authority,BusinessOrgCode,BusinessSystemCode,BusinessTypeCode,SourceData,Base64SourceData,SignedData,Detach,DataDigest,Timestamp,CertInfoID,SignCert,CreatedTime,LastTime) VALUES('df71904a-326d-4412-a652-d3b538f8b16b','BJCA','514403045026825020','1301','004','{"绛惧悕鍘熸枃":"<Data><PatientInfo><inspection_id>鍩哄洜褰?0200615128</inspection_id><instrument>鍩哄洜褰?/instrument><sample_id>128</sample_id><sample_barcode>0700008503</sample_barcode><name>鏋楀績鑾?/name><sex>濂?/sex><age>28</age><department>浣撴绉戔槄</department><bed_no></bed_no><patient_id>2006050084</patient_id><diagnosis>璇婃柇</diagnosis><test_sample>鍒嗘硨鐗?/test_sample><sample_status></sample_status><request_doctor>鏈煡</request_doctor><inspector>鐜嬬惣</inspector><auditor>鍒? 閿?/auditor><request_data>2020-06-05 00:00:00</request_data><collection_date>2020-06-12 08:45:16</collection_date><receive_date>2020-06-12 10:31:13</receive_date><auditor_date>2020-06-18 20:29:24</auditor_date></PatientInfo><Re
Connection ID (thread ID): 26
Status: NOT_KILLED

The manual page at http://dev.mysql.com/doc/mysql/en/crashing.html contains
information that should help you find out what is causing the crash.
2020-06-19T01:03:25.936913Z 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2020-06-19T01:03:25.964257Z 0 [Note] --secure-file-priv is set to NULL. Operations related to importing and exporting data are disabled
2020-06-19T01:03:25.966210Z 0 [Note] MySQL (mysqld 5.7.19) starting as process 22400 ...
2020-06-19T01:03:26.041405Z 0 [Note] InnoDB: Mutexes and rw_locks use Windows interlocked functions
2020-06-19T01:03:26.041405Z 0 [Note] InnoDB: Uses event mutexes
2020-06-19T01:03:26.042382Z 0 [Note] InnoDB: _mm_lfence() and _mm_sfence() are used for memory barrier
2020-06-19T01:03:26.043359Z 0 [Note] InnoDB: Compressed tables use zlib 1.2.3
2020-06-19T01:03:26.064843Z 0 [Note] InnoDB: Number of pools: 1
2020-06-19T01:03:26.073632Z 0 [Note] InnoDB: Not using CPU crc32 instructions
2020-06-19T01:03:26.094140Z 0 [Note] InnoDB: Initializing buffer pool, total size = 128M, instances = 1, chunk size = 128M
2020-06-19T01:03:26.098046Z 0 [Note] InnoDB: VirtualAlloc(137297920 bytes) failed; Windows error 1455
2020-06-19T01:03:26.099023Z 0 [ERROR] InnoDB: Cannot allocate memory for the buffer pool
2020-06-19T01:03:26.099023Z 0 [ERROR] InnoDB: Plugin initialization aborted with error Generic error
2020-06-19T01:03:26.099999Z 0 [ERROR] Plugin 'InnoDB' init function returned error.
2020-06-19T01:03:26.099999Z 0 [ERROR] Plugin 'InnoDB' registration as a STORAGE ENGINE failed.
2020-06-19T01:03:26.100976Z 0 [ERROR] Failed to initialize plugins.
2020-06-19T01:03:26.100976Z 0 [ERROR] Aborting

2020-06-19T01:03:26.101952Z 0 [Note] Binlog end
2020-06-19T01:03:26.104882Z 0 [Note] Shutting down plugin 'CSV'
2020-06-19T01:03:26.107812Z 0 [Note] MySQL: Shutdown complete
~~~
