---
title: uibot之流程图.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: uibot
categories: uibot
---
---
title: uibot之流程图.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: uibot
categories: uibot
---
###流程节点之间怎么传递变量参数？

数据抓取节点填写上arrayData做输出参数
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ac30a0a4f84f8db1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
在代码里retrun下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c845c922b7c881e8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
return arrayData
~~~


数据入库节点，填写输入参数
![image.png](https://upload-images.jianshu.io/upload_images/13965490-63f47cf9bddb9531.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
使用Self.Input 接受参数
~~~
dim arrayData = Self.Input 
~~~
