---
title: git-生成补丁和打补丁.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: git
categories: git
---
---
title: git-生成补丁和打补丁.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: git
categories: git
---
生成补丁
![image.png](https://upload-images.jianshu.io/upload_images/13965490-08a3745dd02e0a54.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


打补丁
git apply sql_log_redis-config_config_config.patch


>使用打补丁功能可以方便的应用一些不需要提交的代码和配置。比如热部署配置，Redis配置改为localhost等一些文件修改的commit都可以直接生成相应的补丁文件！然后在需要的时候应用下就行了
