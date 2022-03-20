---
title: http请求别的服务器，post的json参数中的中文乱码解决.md
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
title: http请求别的服务器，post的json参数中的中文乱码解决.md
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
http请求别的服务器，参数中的中文乱码解决：添加 `-Dfile.encoding=utf-8`
然后功能没问题，控制台又出现中文乱码，是因为 windows默认GBK。解决，在前面加 chcp 65001 
~~~
chcp 65001 
java -Dfile.encoding=utf-8 -jar Arrange1.0.jar
~~~

windows server 2008 版本会出现中文乱码，特别是 三个字的名字的第三个字乱码！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-54cbec18003bd694.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



chcp 命令找不到：解决
在系统变量PATH下添加路径C:\WINDOWS\system32;
