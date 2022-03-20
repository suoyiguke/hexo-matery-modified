---
title: UUID_SHORT()-函数.md
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
title: UUID_SHORT()-函数.md
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
[`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short)

Returns a “short” universal identifier as a 64-bit unsigned integer. Values returned by [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short) differ from the string-format 128-bit identifiers returned by the [`UUID()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid) function and have different uniqueness properties. The value of [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short) is guaranteed to be unique if the following conditions hold:

*   The [`server_id`](https://dev.mysql.com/doc/refman/8.0/en/replication-options.html#sysvar_server_id) value of the current server is between 0 and 255 and is unique among your set of source and replica servers

*   You do not set back the system time for your server host between [**mysqld**](https://dev.mysql.com/doc/refman/8.0/en/mysqld.html "4.3.1 mysqld — The MySQL Server") restarts

*   You invoke [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short) on average fewer than 16 million times per second between [**mysqld**](https://dev.mysql.com/doc/refman/8.0/en/mysqld.html "4.3.1 mysqld — The MySQL Server") restarts

The [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short) return value is constructed this way:

```
  (server_id & 255) << 56
+ (server_startup_time_in_seconds << 24)
+ incremented_variable++;
```

```
mysql> SELECT UUID_SHORT();
        -> 92395783831158784
```

Note

[`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short) does not work with statement-based replication.



https://blog.csdn.net/xiaohangblog/article/details/89085389



>UUID_SHORT()的值就是 uuid的bigint形式，可以实现自增id的全局唯一性








与uuid返回固定长度字符串不同， uuid_short的返回值是一个unsigned long long类型。MySQL启动后第一次执行的值是通过server_id << 56 + server_start_time << 24来初始化。server_start_time单位是秒。 之后每次执行都加1。
由于每次加1都会加全局mutex锁，因此多线程安全，可以当作sequence来用，只是初始值有点大。


Sequence
 MySQL没有Oracle那样的sequence，在不是很精确的情况下，可以考虑上面提到的uuid_short。有一些不足:

1、初始值太大，无法重设
2、存在一个问题是每次重启后第一次执行的值不是重启前的那个值+1
3、而且如果重启在1s内完成，可能出现不单调递增（虽然这个可能性微乎其微）。

要满足上面的需求，可以考虑用udf实现。
