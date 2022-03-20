---
title: idea-配置tomcat.md
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
title: idea-配置tomcat.md
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
https://blog.csdn.net/chendeyou5/article/details/80359716


1、export模式 和archive 模式区别

export模式下有jsp热部署









On Upate Action 与 On Frame Deactivation  这两个选项的设置，依赖于 项目的部署方式 是war包 还是 exploded ，看下面的gif：


这里实在是太灵活了，如果要讲 太费时间了，我们只讲exploded模式下的设置，因为这个我们用的最多，开发模式，开发完成后 直接用maven的 package命令打包就行了，所以用的最多的 也是最灵活的就是exploded 开发模式。exploded模式 实际运行的就是target目录下的kao文件夹。

首先来看 on update action 相关的解释，从字面上理解 就是 手工触发 update 动作的时候 做什么：

[图片上传中...(image-a0c20b-1628766717237-0)] 

![技术分享](https://upload-images.jianshu.io/upload_images/13965490-4091fdc9b3c4bbab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

update resources ---- 更新静态的资源，比如html,js,css等 运行模式和调试模式都是立即生效。

update classes and resources ---- 更新java,jsp和静态资源（

1\. java 修改后，会被编译成.class 然后覆盖到target/kao文件夹下，IDE调试模式的情况下，立即生效。IDE运行模式下，不立即生效，需要redeployed才可生效。

2\. jsp修改后，再次被访问的时候，会自动更新，重新编译成.java---->.class 保存在tomcat的work目录下。由于是访问时才检测是否修改，是否需要重新编译，所以 IDE 运行模式 和 IDE调试模式下，都是立即生效。刷新下页面就可）；

redeployed ----- 重新部署，发布到tomcat里，不重启tomcat，而是把原来的删掉，然后重新发布；

restart server ----- 重启tomcat

------------------------------------------------------------------------------------------------------------------------

再来看on frame deactivation ，意思是 IDE 失活时 做什么，就是说 IDE 失去焦点时 做什么。

![技术分享](https://upload-images.jianshu.io/upload_images/13965490-e84f02f3bdbcaa06.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

Do nothing --------- 什么都不做

update resources ---- 更新静态的资源，比如html,js,css等 运行模式和调试模式都是立即生效。

update classes and resources ---- 更新java,jsp和静态资源 同上。
