---
title: docker-使用harbor私服推送和拉取镜像.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: docker
categories: docker
---
---
title: docker-使用harbor私服推送和拉取镜像.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: docker
categories: docker
---
>水滴石穿


这篇文章讲到到了docker、docker-compose和harbor私服的安装部署 https://www.jianshu.com/p/7e44556ddc08

在实际开发中，常常会将harbor部署到公网，并配置好域名和https。在开发者机器上build好镜像之后，再push到公网的harbor上。最后项目上线时再到服务器上pull镜像。因为harbor在公网上所以咱们的服务也能访问的到。


接下来看看如何将自己打包好的镜像推送到harbor私服，然后在其它机器上拉取镜像
###安装后的一些配置

######首先需要创建一个用户
点击创建用户
![image.png](https://upload-images.jianshu.io/upload_images/13965490-674946d00961c082.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



输入用户名密码邮箱这些不用多说，注意这些信息在推送镜像的时候会用到，不要随便设一个！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0d4651f86a8f6a69.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
创建用户后如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-40335c776fe40510.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######然后创建一个镜像仓库
先来看公开仓库，点击这个按钮
![image.png](https://upload-images.jianshu.io/upload_images/13965490-10c35ca9d1317afd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

为仓库起名后点击确定
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aaf0aaa9bf5b6de3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这样就创建了一个镜像仓库了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-134706342664c70d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点进去给这个镜像仓库分配管理用户
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d431d2c37bcab475.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
输入之前创建的用户名，确定即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cc3ac23aa7965a2f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######推送本地docker镜像到harbor私服
接下就是样演示推送镜像到harbor私服了，点击镜像仓库这一栏。有一个推送镜像的按钮。点一下会出现推送命令。注意必须使用这个推送命令所示的前缀，不然是推送不了的。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7a37d30e00b93c58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


首先我的本机linux上有名为 `192.168.10.11:81/test/demo1:latest`  的镜像，需要推送到harbor私服上。注意我这里已经是改完镜像名字符合上面要求的前缀了，关于镜像的改名可以看看我的这篇文章https://www.jianshu.com/p/caecb4fc0c35
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aa5bfa137a4ada45.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



使用命令推送
~~~
docker push 192.168.10.11:81/test/demo1:latest
~~~
报错如下
>The push refers to repository [192.168.10.11:81/test/demo1]
Get https://192.168.10.11:81/v2/: http: server gave HTTP response to HTTPS client

提示推送镜像报docker客户端需要https请求，要么给harbor配置域名+https，要么修改dockr客户端配置，让它支持http。如果私服只是内网使用当然改docker客户端比较方便啦~

编辑daemon.json文件，加上insecure-registries的配置
vi /etc/docker/daemon.json

>注意这个192.168.10.11:81 的 81 端口是 harbor的http访问端口，通过它来访问harbor的UI管理页面。当然它默认是80，我将之改为了81
~~~
{
  "registry-mirrors": ["http://hub-mirror.c.163.com"],"insecure-registries":["192.168.10.11:81"]
}

~~~

改完后重启docker服务
~~~
 systemctl daemon-reload
 systemctl restart docker

~~~

再次执行推送命令，报错
>[root@localhost harbor]# docker push 192.168.10.11:81/test/demo1:latest
The push refers to repository [192.168.10.11:81/test/demo1]
f8c4d6c65078: Preparing 
d132b54fabdd: Preparing 
35c20f26d188: Preparing 
c3fe59dd9556: Preparing 
6ed1a81ba5b6: Preparing 
a3483ce177ce: Waiting 
ce6c8756685b: Waiting 
30339f20ced0: Waiting 
0eb22bfb707d: Waiting 
a2ae92ffcd29: Waiting 
denied: requested access to the resource is denied

因为没有登录到harbor私服的原因，那么就登录吧
>- 注意使用docker login 192.168.10.11:81 登录的 81端口也是harbor的web端口，默认是80。被我改成81了
~~~
[root@localhost harbor]#  docker login 192.168.10.11:81
Username: yinkai
Password: 
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store
Login Succeeded
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-5b8dbdadf34e6868.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


再次推送，这样子算是成功了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fb1d341fecab4a81.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

查看test项目下果然有镜像了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9874508f88d36fd9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点进去看看
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7ce77ef08d5df537.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######在其它机器上拉取已上传的镜像
最后来看看如何拉取私服上的镜像。首先点击去镜像仓库，找到刚上传的demo1镜像。如图点击复制pull命令
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d7e7a1650c57ad59.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在服务器上执行命令即可
~~~
docker pull 192.168.10.11:81/test/demo1:latest
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-42c8ed78550078c0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用docker images 查看镜像
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d26cd8bd6d780452.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

拉取成功~
