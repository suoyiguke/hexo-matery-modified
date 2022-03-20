---
title: mysql-字符集列表库字符集不同一会导致cpu狂飙出现慢查询.md
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
title: mysql-字符集列表库字符集不同一会导致cpu狂飙出现慢查询.md
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
https://mp.weixin.qq.com/s/9zNIkUv-SNi8wMIEziDCrA

~~~
show status like '%Handler%'
~~~

- 查看Handler的状态，可以看到Handler_read_next的值极高，其实这是一个全表扫描。
- 查看Handler的情况，Handler_read_rnd_next为0，很显然是一个索引扫描。


