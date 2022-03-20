---
title: idea-将包指定含main方法的class打成jar包.md
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
title: idea-将包指定含main方法的class打成jar包.md
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
有时候我们整个工程需要集成一些sdk，而这些sdk只能在特定网络环境下才能调用。而为了调试又去部署一套开发环境是很麻烦的，而且只需要其中特定的模块和依赖。所以我们只需要将调试demo打成一个jar包放到特定网络环境的机器上运行即可。

那么我们来看下如何将普通的class打包成jar

Artifacts-->JAR-->From modules with dependencies
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fea5a52078618848.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

指定class所在maven modules

![image.png](https://upload-images.jianshu.io/upload_images/13965490-ad5a01329d78187d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以在这里查看刚新建的 JAR Artifacets
Artifacets-->
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2dc76a0b64099d22.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Build-->Build Artifacets-->选中我们刚构建的Artifacets-->Build
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ef72df9c2857c7c1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1dbf779b9f08cf64.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###运行时直接指定
java -cp szwj-business.jar com.ruoyi.business.Main
