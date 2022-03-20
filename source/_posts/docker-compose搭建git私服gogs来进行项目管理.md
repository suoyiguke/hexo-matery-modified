---
title: docker-compose搭建git私服gogs来进行项目管理.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: git
categories: git
---
---
title: docker-compose搭建git私服gogs来进行项目管理.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: git
categories: git
---
### 什么是 Gogs?

Gogs 是一款极易搭建的自助 Git 服务。

Gogs 的目标是打造一个最简单、最快速和最轻松的方式搭建自助 Git 服务。使用 Go 语言开发使得 Gogs 能够通过独立的二进制分发，并且支持 Go 语言支持的 **所有平台**，包括 Linux、Mac OS X、Windows 以及 ARM 平台

###贴下gogs的官网
https://gogs.io/

###搭建gogs
1、先上docker-compose.yml文件
~~~

version: '3'
services:
 gogs:
   image: docker.io/gogs/gogs:latest
   links:
     - mysql-gogs:mysql
   ports:
     - "10022:22"
     - "3000:3000"
   volumes:
     - /opt/docker/gogs/:/data/docker/gogs
   restart: always

 mysql-gogs:
   image: docker.io/mysql:5.7
   ports:
     - "3300:3306"
   volumes:
     - ./mysql-gogs/mysql:/var/lib/mysql
     - ./mysql-gogs/conf.d:/etc/mysql/conf.d:rw
   environment:
     - MYSQL_DATABASE=gogs
     - MYSQL_USER=gogs
     - MYSQL_PASSWORD=gogs
     - MYSQL_ROOT_PASSWORD=gogs
   command: mysqld --lower_case_table_names=1 --character-set-server=utf8mb4 --collation-server=utf8mb4_general_ci
   restart: always
~                  

~~~
注意：我在这配置的端口将影响到下面进一步的配置
- gogs的web服务端口是 3000
- gogs的mysql端口是3300
- gogs的ssh端口是10022

2、启动容器组
docker-compose up

3、访问

http://192.168.10.11:3000

4、配置
- 数据库配置
![image.png](https://upload-images.jianshu.io/upload_images/13965490-86bfafb76f23f423.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这些都在docker-compose.yml文件里有设置，直接填上就可以了

- 应用基本设置
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f404106d897f69b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意
1、ip都填上搭建的服务器的ip，我这里是192.168.10.11
2、http和ssh端口要注意别写错了，不然影响后面的使用

- 管理员账号设置
![image.png](https://upload-images.jianshu.io/upload_images/13965490-29a9966e4b8e11a9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 可选设置
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d92a758dc858857f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果有`邮键通知、禁止自主注册`这方面需求可以在这里配置

5、配置完毕点击立即安装
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a6805e5643bc4be2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

6、再次访问
http://192.168.10.11:3000
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ca80a260b123cf0e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这样就大功告成了，是不是很简单~~

###gogs使用示例
1、点击右上角+号，选择创建新的仓库
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9ca190bb94951163.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、填写相关项目信息

![image.png](https://upload-images.jianshu.io/upload_images/13965490-973c3ac94bbe1d05.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击创建仓库后，页面跳转成这样，上面有推送命令的提示
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d767f45d75f30ec9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


3、在安装了git的前提下，找到待上传的项目根目录

![image.png](https://upload-images.jianshu.io/upload_images/13965490-4e4349803e900c36.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

4、copy上面的命令，git add README.md改为git add . ；表示添加文件夹下所有的文件
~~~
touch README.md
git init
git add .
git commit -m "first commit"
git remote add origin http://192.168.10.11:3000/yinkai/project_yk.git
git push -u origin master
~~~
运行到最后一步push的时候弹出对话框，填上账号密码即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b0504b10d64699ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-dd544eb34f7e3ece.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

F5刷新页面,仓库中已经存在文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-46d6a99c1bb6d4a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

推送成功！

以上就是gogs搭建过程和上传项目示例，喜欢就点个赞吧
