---
title: mysql-如何得到innodb主键索引B+树的树高度.md
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
title: mysql-如何得到innodb主键索引B+树的树高度.md
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
B+树的高度通常是1-3; 在InnoDB的表空间文件中，约定 page number 为3的代表主键索引的根页，而在根页偏移量为`64`的地方存放了该B+树的page level。如果page level为1，树高为2，page level为2，则树高为3。索引树高度决定查询的IO次数，当然树高度越大则查询需要的IO次数就越多，查询效率相对来说就越低！


>B+树的高度=page level+1；

我们需要找到这个page level。在实际操作之前，你可以通过InnoDB元数据表确认主键索引根页的 page number 为3。


~~~
mysql> SELECT
	b.NAME,
	a.NAME,
	index_id,
	type,
	a.space,
	a.PAGE_NO 
FROM
	information_schema.INNODB_SYS_INDEXES a,
	information_schema.INNODB_SYS_TABLES b 
WHERE
	a.table_id = b.table_id 
	AND a.space <> 0;
+------------------------------------+-----------------------------+----------+------+-------+---------+
| NAME                               | NAME                        | index_id | type | space | PAGE_NO |
+------------------------------------+-----------------------------+----------+------+-------+---------+

| iam/biz_organization               | PRIMARY                     |      116 |    3 |    95 |       3 |
| iam/biz_patient_pdf_stamp_position | PRIMARY                     |      117 |    3 |    96 |       3 |
| iam/biz_patient_sign_pdf           | PRIMARY                     |      118 |    3 |    97 |       3 |
| iam/biz_patient_sign_pdf_details   | PRIMARY                     |      119 |    3 |    98 |       3 |
| iam/biz_signed_pdf                 | PRIMARY                     |      120 |    3 |    99 |       3 |
| iam/biz_signed_pdf_details         | PRIMARY                     |      121 |    3 |   100 |       3 |
| iam/biz_sys_info                   | PRIMARY                     |      122 |    3 |   101 |       3 |
| iam/biz_ukey_login                 | PRIMARY                     |      123 |    3 |   102 |       3 |
| iam/biz_ukey_login_details         | PRIMARY                     |      124 |    3 |   103 |       3 |
| iam/biz_ukey_sign                  | PRIMARY                     |      125 |    3 |   104 |       3 |
| iam/biz_ukey_sign_details          | PRIMARY                     |      126 |    3 |   105 |       3 |
| iam/biz_ukey_signed_pdf            | PRIMARY                     |      127 |    3 |   106 |       3 |
| iam/biz_ukey_signed_pdf_details    | PRIMARY                     |      128 |    3 |   107 |       3 |
| iam/biz_user                       | PRIMARY                     |      129 |    3 |   108 |       3 |
| iam/biz_user                       | mobile                      |      130 |    0 |   108 |       4 |
| iam/biz_user                       | authentication_mark         |      131 |    0 |   108 |       5 |
| iam/biz_user_employee_num          | PRIMARY                     |      230 |    3 |   188 |       3 |
| iam/biz_user_employee_num          | biz_num                     |      231 |    2 |   188 |       4 |
| iam/book                           | PRIMARY                     |      235 |    3 |   197 |       3 |
| iam/book                           | index_user_id               |      236 |    0 |   197 |       4 |

~~~



可以看出主键索引（PRIMARY）根页的page number均为3，而其他的二级索引page number(PAGE_NO)为4还有5。

**下面我们对数据库表空间文件做想相关的解析：**

~~~
[root@localhost iam]# ls -l *.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_h5_sign_details.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_h5_sign.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_organization.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_patient_pdf_stamp_position.ibd
-rw-r-----. 1 mysql mysql   9437184 10月 30 15:12 biz_patient_sign_pdf_details.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_patient_sign_pdf.ibd
-rw-r-----. 1 mysql mysql    131072 10月 30 15:12 biz_signed_pdf_details.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_signed_pdf.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_sys_info.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_ukey_login_details.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_ukey_login.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_ukey_sign_details.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_ukey_signed_pdf_details.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_ukey_signed_pdf.ibd
-rw-r-----. 1 mysql mysql     98304 10月 30 15:12 biz_ukey_sign.ibd
-rw-r-----. 1 mysql mysql   9437184 10月 30 15:12 biz_user_copy1.ibd
-rw-r-----. 1 mysql mysql   9437184 10月 30 15:12 biz_user_copy2.ibd
-rw-r-----. 1 mysql mysql   9437184 10月 30 15:12 biz_user_copy3.ibd
-rw-r-----. 1 mysql mysql    114688 11月 23 15:12 biz_user_employee_num.ibd
-rw-r-----. 1 mysql mysql   9437184 10月 30 15:12 biz_user.ibd
-rw-r-----. 1 mysql mysql 125829120 1月  26 09:19 book.ibd

~~~

因为主键索引B+树的根页在整个表空间文件中的第3个页开始，所以可以算出它在文件中的偏移量：16384*3=49152（16384为页大小 16KB）。

根页的64偏移量位置前2个字节，保存了page level的值，因此我们想要的page level的值在整个文件中的偏移量为：16384*3+64=49152+64=49216，前2个字节中。

**接下来我们用hexdump工具，查看表空间文件指定偏移量上的数据：**
分别查看book、biz_user、biz_patient_pdf_stamp_position三张表的ibd表空间文件

~~~
[root@localhost iam]# hexdump -s 49216 -n 10 book.ibd
000c040 0200 0000 0000 0000 eb00               
000c04a
[root@localhost iam]# hexdump -s 49216 -n 10 biz_user.ibd
000c040 0100 0000 0000 0000 8100               
000c04a
[root@localhost iam]# hexdump -s 49216 -n 10 biz_patient_pdf_stamp_position.ibd
000c040 0000 0000 0000 0000 7500               
000c04a
[root@localhost iam]# 
~~~

book 表的page level为2，B+树高度为page level+1=3；
biz_user 表的page level为1，B+树高度为page level+1=2；
biz_patient_pdf_stamp_position 表的page level为0，B+树高度为page level+1=1；

这三张表的数据量如下：
~~~
mysql>  select count(*) from book ;
+----------+
| count(*) |
+----------+
|   312221 |
+----------+
1 row in set (0.07 sec)

mysql>  select count(*) from biz_user  ;
+----------+
| count(*) |
+----------+
|     3570 |
+----------+
1 row in set (0.02 sec)

mysql>  select count(*) from biz_patient_pdf_stamp_position   ;
+----------+
| count(*) |
+----------+
|        3 |
+----------+
1 row in set (0.02 sec)
~~~






