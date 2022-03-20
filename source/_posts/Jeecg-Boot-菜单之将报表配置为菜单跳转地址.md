---
title: Jeecg-Boot-菜单之将报表配置为菜单跳转地址.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---
---
title: Jeecg-Boot-菜单之将报表配置为菜单跳转地址.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---
> 忍耐力有多大，气量就有多大

我们需要将线上配置的报表配置到菜单的跳转地址中，如下： 
点击左边这个菜单，右边就会跳转到特定报表中
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bfde35b29cb72379.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


首先一级菜单配置：
组件和路由均为 layouts； 且是否路径菜单选项设置为false关
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bccfe3ea3c5c1f80.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

不知道一级菜单为什么 组件和路由都是必填的。所以我设置一个layouts不会让它报错即可。

然后二级菜单配置

![image.png](https://upload-images.jianshu.io/upload_images/13965490-56f1787fefb3a128.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中菜单路径 填上报表的路径，我这里是
>/online/cgreport/7f51ed034e6f4a6fa21f40af3033a402

这个路径可以在定义报表那里点击`配置路径`选项得到
前端组件时固定的，必须填上以下路径

>modules/online/graphreport/auto/OnlGraphreportAutoChart

它的是否路径菜单也需设置为 false
