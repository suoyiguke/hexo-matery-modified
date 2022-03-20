---
title: jvm-捕获oom的快照文件hprof和分析快照.md
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
title: jvm-捕获oom的快照文件hprof和分析快照.md
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

    在JAVA_OPTIONS变量中增加

    -XX:+HeapDumpOnOutOfMemoryError  -XX:HeapDumpPath=${目录}。
    例如：export JAVA_OPTS="-Xms2048M -Xmx2048M -Xmn682M -XX:MaxPermSize=96M"

参数说明

（1）-XX:+HeapDumpOnOutOfMemoryError参数表示当JVM发生OOM时，自动生成DUMP文件。

（2）-XX:HeapDumpPath=${目录}参数表示生成DUMP文件的路径，也可以指定文件名称，例如：-XX:HeapDumpPath=${目录}/java_heapdump.hprof。如果不指定文件名，默认为：java_<pid>_<date>_<time>_heapDump.hprof。</pre>


例子
~~~
-Xms100m -Xmx100m -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=D:/oom/java_heapdump.hprof
~~~

###使用jvisualvm.exe工具分析

###使用JProfilerl 工具分析
