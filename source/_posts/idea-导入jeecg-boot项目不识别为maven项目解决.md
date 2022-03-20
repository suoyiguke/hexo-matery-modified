---
title: idea-导入jeecg-boot项目不识别为maven项目解决.md
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
title: idea-导入jeecg-boot项目不识别为maven项目解决.md
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
> 自弃者天弃之


打开工程配置
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a8abc19c384a7676.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击import module
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0b41a5cd43918be2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

选择存在pom.xml文件目录即可，这里是 jeecg-boot。而且jeecg-boot项目的pom.xml是分开的，这个pom.xml只是一个父级依赖配置
![image.png](https://upload-images.jianshu.io/upload_images/13965490-630b1b8397242faa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后出现这个，说明有3个maven modules，存在3个pom.xml文件

![image.png](https://upload-images.jianshu.io/upload_images/13965490-94287768fc2c94cf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后点击finished等待加载依赖即可

最终识别为maven工程之后会出现这种高亮显示工程模块名，而且一些文件如 *.java、pom.xml 的显示格式都不同了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-14d006c577352acb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
