---
title: redis持久化-使用AOF方式恢复数据.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
---
title: redis持久化-使用AOF方式恢复数据.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---

###如果将一个key remove掉，请问可以恢复吗？怎么恢复？
可以恢复。如果开启了AOF方式的持久化，就将aof文件末尾的del命令日志删除，然后重启redis即可恢复。
比如：

 - 删除一个key
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fa681b6651adae2a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 编辑 appendonly.aof 文件，删除掉DEL日志
![image.png](https://upload-images.jianshu.io/upload_images/13965490-551657fff2f75564.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 重启
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8843e2db540030fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 恢复成功
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3e3a7f048249a4c9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

