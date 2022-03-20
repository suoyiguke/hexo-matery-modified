---
title: 获得dump文件方式的总结.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: 获得dump文件方式的总结.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
###jmap 

先找到PID
ps -ef | grep java

jmap 转存快照
jmap -dump:format=b,file=/opt/dump/test.dump {PID}


###JVM启动参数
第二种是通过配置JVM启动参数

当程序出现OutofMemory时，将会在相应的目录下生成一份dump文件，如果不指定选项HeapDumpPath则在当前目录下生成dump文件
-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/opt/dumps

