---
title: navicat.md
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
title: navicat.md
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
>naviact简直是神器啊！



###导入数据
![image.png](https://upload-images.jianshu.io/upload_images/13965490-121ab32ad46ab7cb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-66482f25d80382f3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1、可以把excel直接导入成 mysql数据表，会自动使用表头当字段名
2、还有其它的格式如 JSON、XML的结构化数据也能直接导入数据库

###导入*.sql文件
如果报错，尝试把勾去掉
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b90250bac96f410b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





###两个数据库之间的操作

1、数据传输
![image.png](https://upload-images.jianshu.io/upload_images/13965490-031a8959c8790d29.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
将目标表删除，创建源表后导入数据；
>注意，数据传输不是将源表中存在，目标表中不存在的数据导入到目标表！它会强制先drop目标表，导致目标表中原来的数据丢失！

2、数据同步

3、结构同步
