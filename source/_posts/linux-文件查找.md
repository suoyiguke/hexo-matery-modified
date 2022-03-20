---
title: linux-文件查找.md
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
title: linux-文件查找.md
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
######按文件名查找指定内容，返回文件路径

~~~
 find ./ -name "index.html" | xargs grep  "#content dl dd{ padding-bottom:10px;border-bottom:1px solid #efefef;"
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d50880fcda5a5bb0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
