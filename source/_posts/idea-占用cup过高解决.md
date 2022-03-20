---
title: idea-占用cup过高解决.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开发工具
categories: 开发工具
---
---
title: idea-占用cup过高解决.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开发工具
categories: 开发工具
---
打开一个idea的项目cpu占用 40%
1、参数调整如下
~~~
-Xms1024m
-Xmx2080m
-XX:MaxPermSize=512m 
-XX:ReservedCodeCacheSize=256m 
-ea 
-Dsun.io.useCanonCaches=false
-Dsun.awt.keepWorkingSetOnMinimize=true
-Djava.net.preferIPv4Stack=true
-Djsse.enableSNIExtension=false
-XX:+UseCodeCacheFlushing 
-XX:+UseConcMarkSweepGC 
-XX:SoftRefLRUPolicyMSPerMB=50
-javaagent:G:\IDEA\IntelliJ IDEA 2019.3\jetbrains-agent.jar
~~~

2、关闭代码检查
