---
title: linux安装docker、docker-compose、harbor.md
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
title: linux安装docker、docker-compose、harbor.md
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
> 注意docker最好安装在centeros7中，如果安装在centeros6.5则需要升级内核版本！非常麻烦，就算升级了在安装docker时也会出现依赖版本过低问题，如 `container-selinux >= 2.9` 要解决这些问题就需要到指定的镜像网站下载安装。所以不如直接使用centeros7

**版本关系**
- Docker版本
~~~
root@localhost redis]# docker -v
Docker version 18.06.1-ce, build e68fc7a
~~~
- Docker-compose版本
~~~
[root@localhost ~]# docker-compose -v
docker-compose version 1.18.0, build 8dd22a9
~~~
- Harbor版本
harbor-offline-installer-v1.9.0.tgz


**Docker**

- 安装之前的准备
~~~
sudo yum install -y yum-utils \
device-mapper-persistent-data \
lvm2
~~~

- 添加源

~~~
sudo yum-config-manager \
--add-repo \
http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
~~~

- 查看可安装的docker版本
~~~
sudo yum list docker-ce --showduplicates
~~~

![image.png](https://upload-images.jianshu.io/upload_images/13965490-1b9d61ab62ef9ab5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- 开始安装
~~~
sudo yum install docker-ce-18.06.1.ce
~~~
- 查看版本
~~~
[root@localhost docker]# docker -v

Docker version 18.06.1-ce, build e68fc7a
~~~
- 开启远程访问


vim /lib/systemd/system/docker.service

找到ExecStart行，修改成下边这样
~~~
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock  
~~~
用浏览器访问查看是否成功

http://192.168.10.104/version，我ip是这个。如果是别的ip换下即可

![image.png](https://upload-images.jianshu.io/upload_images/13965490-5935409bbb95ffcc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


远程访问成功~

- 更改docker镜像源

vim /etc/docker/daemon.json
~~~
{
  "registry-mirrors": ["http://hub-mirror.c.163.com"]
}
~~~
然后重启守护进程：

sudo systemctl daemon-reload
sudo systemctl restart docker

**docker-compose**


- 安装docker-compose
需要安装1.18.0版本的docker-compose
~~~
curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
~~~
~~~
chmod +x /usr/local/bin/docker-compose
~~~
- docker-compose卸载
~~~
sudo rm /usr/local/bin/docker-compose
~~~



**harbors安装**
- harbors的项目主页：
https://github.com/goharbor/harbors

![image.png](https://upload-images.jianshu.io/upload_images/13965490-4b8c09645bf28a2a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 下载安装包
![image.png](https://upload-images.jianshu.io/upload_images/13965490-bad8fb3b500adbbf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 下载太慢了，可以用这个
https://storage.googleapis.com/harbor-releases/release-1.9.0/harbor-offline-installer-v1.9.0.tgz
- 解压
~~~
tar -xvf harbor-offline-installer-v1.9.0.tgz
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c7250c81fd1f603a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- 修改harbor.yml

hostname 这里设置本机的ip
harbor_admin_password 登录密码
port 端口号
![image.png](https://upload-images.jianshu.io/upload_images/13965490-90a9339c70e2b80f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 运行
~~~
sh ./install.sh
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2a964a2f4b55d782.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 访问
http://192.168.10.104:80/

![image.png](https://upload-images.jianshu.io/upload_images/13965490-c0849838b865563f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

