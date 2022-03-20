---
title: mysql-导出数据.md
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
title: mysql-导出数据.md
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
### MySQL自带，服务端生成数据文件

在客户端连接里使用SELECT * INTO OUTFILE  和 load data 方式

show variables like '%secure%';


~~~
mysql> show variables like '%secure%';
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| require_secure_transport | OFF   |
| secure_auth              | ON    |
| secure_file_priv         | NULL  |
+--------------------------+-------+
3 rows in set (0.02 sec)

mysql> 
~~~

secure_file_priv         为NULL 默认不允许导出
开启
~~~
[mysqld]
#路劲不支持中文
secure_file_priv = F:/
~~~


实例

~~~
# 导出
SELECT * FROM tlk_signed_data -- 可以加where条件
INTO OUTFILE 'F:/work1' -- 导出文件位置
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' -- 字段分割符和包含符
LINES TERMINATED BY '\n';-- 换行符



# 导入
load data infile 'F:/work1' -- 默认指定服务器文件夹
ignore into table tlk_signed_data_c -- 允许重复记录插入
fields terminated by ','  -- 判断字段通过逗号标识来分隔开
lines terminated by '\n'(ID, Authority, BusinessOrgCode, BusinessSystemCode, BusinessTypeCode, SourceData, Base64SourceData, SignedData, Detach, DataDigest, Timestamp, CertInfoID, SignCert, CreatedTime, LastTime);-- 通过换行标识来解析成为每一条数据和插入到我指定的字段



CREATE TABLE tlk_signed_data_c LIKE tlk_signed_data
~~~
>导出操作完成后会在服务器磁盘F上生成数据文件

>用MySQL自带导出/导入优点是速度极快，缺点是：只能导出文件是在服务器主机所在的本机地址，而且需要root权限。不过好在对于字段/内容较少的报表第三方客户端工具导出速度也不算特别慢；

###在客户端得到数据文件
使用mysqldump 命令
