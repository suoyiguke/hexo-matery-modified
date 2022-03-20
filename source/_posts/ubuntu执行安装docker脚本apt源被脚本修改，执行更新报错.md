---
title: ubuntu执行安装docker脚本apt源被脚本修改，执行更新报错.md
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
title: ubuntu执行安装docker脚本apt源被脚本修改，执行更新报错.md
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


这条命令
~~~
curl -sSL http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet | sh -
~~~

如果进行更新源操作，这个源压根在 /etc/apt/sources.list中找不到
![image.png](https://upload-images.jianshu.io/upload_images/13965490-79a7f2ea107b0c83.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

思路：既然是执行了脚本，那打开这个脚本看看它做了什么吧

打开这个服务器上的脚本 http://acs-public-mirror.oss-cn-hangzhou.aliyuncs.com/docker-engine/internet 
可以看到有写入文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-03f7ef1d92ebf430.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
可以看到这个安装脚本有写入文件
/etc/apt/sources.list.d/docker.list

打开它
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8eca116009c95879.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

删除之即可
