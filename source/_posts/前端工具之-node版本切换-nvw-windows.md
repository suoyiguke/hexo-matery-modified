---
title: 前端工具之-node版本切换-nvw-windows.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: web
categories: web
---
---
title: 前端工具之-node版本切换-nvw-windows.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: web
categories: web
---
> 非淡泊无以明志

安装前端工程依赖的时候经常出现node版本不符问题，如果要更新到其它版本则当前版本就要干掉。不过幸好我们有这个`nvw-windows`  

这是在win下的node的版本控制工具，可以使用命令轻松切换不同版本的node。
nvw-windows的主页：https://github.com/coreybutler/nvm-windows/releases

点击下载setup版本，点击安装即可

![image.png](https://upload-images.jianshu.io/upload_images/13965490-8143d1fc6979dbd5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

值得注意点的地方是，如果在安装nvm之前，电脑上就已经安装有node的，会看到如下图，询问你是否用nvm管理已经存在的node版本。一定要选‘是’，这个弹窗可能会出现好几次，都点是。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e04dfca84e56ee64.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###常用命令

######使用淘宝node镜像：
~~~
nvm node_mirror https://npm.taobao.org/mirrors/node/
~~~
######使用淘宝npm镜像：
~~~
 nvm npm_mirror https://npm.taobao.org/mirrors/npm/
~~~


######安装指定版本的node：
nvm install 版本号，比如安装 9.7.0：
~~~
nvm install 9.7.0
~~~

######切换到指定版本的node：

nvm use 版本号，比如使用9.7.0：
~~~
 nvm use 9.7.0
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a20f26f9cc31fa1f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######查看本机的所有node版本 
查看当前电脑上已经安装的全部node版本,正在使用中的版本号前有个星号：
~~~
nvm ls
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2e3bd166c940d0d1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######查看全部node版本：
~~~
nvm ls available
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ea4d7cb248899a20.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######若需要安装32位的node
版本号后面加个32即可
~~~
nvm install 9.7.0 32
~~~
