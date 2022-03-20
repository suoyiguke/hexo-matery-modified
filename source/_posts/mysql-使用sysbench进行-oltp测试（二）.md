---
title: mysql-使用sysbench进行-oltp测试（二）.md
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
title: mysql-使用sysbench进行-oltp测试（二）.md
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
###OLTP测试

1、准备测试数据

sysbench /usr/local/share/sysbench/oltp_read_write.lua --mysql-host=192.168.1.126 --mysql-port=3306 --mysql-db=test  --mysql-user=root --mysql-password=Sgl20@14 --table_size=200000 --tables=10 --threads=8  --report-interval=10  --rand-type=uniform --time=3600 --percentile=99 prepare


2、进行测试write_only，并将测试结果导出到文件中，便于后续分析。


sysbench /usr/local/share/sysbench/oltp_read_write.lua --mysql-host=192.168.1.126 --mysql-port=3306 --mysql-db=test --mysql-user=root --mysql-password=Sgl20@14 --table_size=200000 --tables=10 --threads=8 --report-interval=10 --rand-type=uniform --time=3600 --percentile=99 run > test.log

测试结果
~~~


~~~

3、清除数据

sysbench /usr/local/share/sysbench/oltp_read_write.lua --mysql-host=192.168.1.126 --mysql-port=3306 --mysql-db=test --mysql-user=root --mysql-password=Sgl20@14 --table_size=200000 --tables=10 --threads=8 --report-interval=10 --rand-type=uniform --time=3600 --percentile=99 cleanup



###命令参数解释
--events    最大请求数量，定义数量后可以不需要--time选项；这个选项会创建这个数目的connections。而mysql有最大连接限制 max_connections



--test=tests/db/oltp.lua 表示调用 tests/db/oltp.lua 脚本进行 oltp 模式测试
--tables=10 表示会生成 10 个测试表 
--table_size=200000  表示每个测试表填充数据量为 200000 
--rand-init=on 表示每个测试表都是用随机数据来填充的


 --threads=8 表示发起 8个并发连接
 --report-interval=10 表示每10秒输出一次测试进度报告 

 --rand-type=uniform 表示随机类型为固定模式，其他几个可选随机模式：uniform(固定),gaussian(高斯),special(特定的),pareto(帕累托)

 --time=3600 表示最大执行时长为 3600秒，也就是1个小时
 --percentile=99 表示设定采样比例，默认是 95%，即丢弃1%的长请求，在剩余的99%里取最大值


即：模拟 对10个表并发OLTP测试，每个表20万行记录，持续压测时间为 1小时。

真实测试场景中，建议持续压测时长不小于30分钟，否则测试数据可能不具参考意义。
