---
title: jvm-监控命令工具之--jps-查看Java进程.md
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
title: jvm-监控命令工具之--jps-查看Java进程.md
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
**Java Virtual Machine Process Status Tool**

**Java进程和操作系统中的进程相同**


`jps`: 显示Java进程号和主类名称

`jps -q`:只显示Java进程号

`jps -l`:显示主类全类名

`jps -m`:显示主类main()的参数

`jps -v`:显示进程启动的JVM参数


C:\Users\yinkai>jps -l
10704 org.jetbrains.idea.maven.server.RemoteMavenServer36
180948 org.jetbrains.jps.cmdline.Launcher
13784
253128 jdk.jcmd/sun.tools.jps.Jps
105308
