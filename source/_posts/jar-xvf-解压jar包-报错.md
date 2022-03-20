---
title: jar-xvf-解压jar包-报错.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
---
title: jar-xvf-解压jar包-报错.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
[root@VM_16_11_centos work]# jar xvf box-1.jar BOOT-INF/classes/jeecg/jeecg_database.properties
java.util.zip.ZipException: zip END header not found
	at java.base/java.util.zip.ZipFile$Source.zerror(ZipFile.java:1527)
	at java.base/java.util.zip.ZipFile$Source.findEND(ZipFile.java:1428)
	at java.base/java.util.zip.ZipFile$Source.initCEN(ZipFile.java:1435)
	at java.base/java.util.zip.ZipFile$Source.<init>(ZipFile.java:1266)
	at java.base/java.util.zip.ZipFile$Source.get(ZipFile.java:1229)
	at java.base/java.util.zip.ZipFile$CleanableResource.<init>(ZipFile.java:727)
	at java.base/java.util.zip.ZipFile$CleanableResource.get(ZipFile.java:845)
	at java.base/java.util.zip.ZipFile.<init>(ZipFile.java:245)
	at java.base/java.util.zip.ZipFile.<init>(ZipFile.java:175)
	at java.base/java.util.zip.ZipFile.<init>(ZipFile.java:146)
	at jdk.jartool/sun.tools.jar.Main.extract(Main.java:1377)
	at jdk.jartool/sun.tools.jar.Main.run(Main.java:396)
	at jdk.jartool/sun.tools.jar.Main.main(Main.java:1669)
