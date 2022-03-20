---
title: oracle-之-PL-SQL-导入导出-pde文件.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: oracle
categories: oracle
---
---
title: oracle-之-PL-SQL-导入导出-pde文件.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: oracle
categories: oracle
---
###导出


###导入
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0f3721344108aea6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意可能出现报错如下：

1、用户名找不到

2、表空间找不到

因为oracle的二进制导入的 当前用户和表空间必须要和之前导出的文件保持一致！而我们的sql脚本就不存在这个问题了。所以必须先创建指定用户，然后创建表空间并且指定用户的默认表空间。
