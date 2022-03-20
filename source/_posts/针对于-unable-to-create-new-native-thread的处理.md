---
title: 针对于-unable-to-create-new-native-thread的处理.md
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
title: 针对于-unable-to-create-new-native-thread的处理.md
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
>会不会是因为springboot创建了太多线程导致的？

unable to create new native thread 
使用jstack命令查看线程dump。
~~~
jstack 56288（pid）
~~~
当然也可以使用jvisualvm.exe查看线程dump
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ca544869477d6fca.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/13965490-c6b4a10528cbb3a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


工程里使用的http工具是 java.net.HttpURLConnection，会不会是它的bug？或者是我们没用好
