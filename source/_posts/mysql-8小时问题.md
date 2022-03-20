---
title: mysql-8小时问题.md
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
title: mysql-8小时问题.md
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

mysql5中已经不支持autoReconnect的方式了，网上的那些都是错的。只能轮询去发select 1 来保证连接不被踢出

**重现问题**
将wait_timeout 设置为1秒时，jdbc访问就报错
~~~

**c**
SET SESSION Interactive_timeout = 1
SET GLOBAL Interactive_timeout = 1
SET SESSION wait_timeout = 1
SET GLOBAL wait_timeout = 1
~~~

>Caused by: com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
Caused by: java.net.SocketException: Software caused connection abort: recv failed


