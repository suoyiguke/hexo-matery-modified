---
title: docker-常用操作.md
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
title: docker-常用操作.md
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
1、进入容器
先使用docker ps 查看容器id
进入容器：docker exec -it 容器id bash

2、docker-compose down会导致数据丢失，数据库数据库实例即使挂载了也会被干掉；千万小心使用！

3、拉取镜像
docker pull hub.cyzxs.cn/xsh/cms:0725-1

4、启动容器组
docker-compose up  监视日志
docker-compose up -d  跳过日志

5、查看容器组日志
docker-compose logs -f

6、查看容器状态
docker-compose ps

7、干掉容器组
docker-compose down
警惕使用这个

8、重启容器组
docker-compose restart

9、查看容器详细信息
docker inspect 容器id/容器名

10、查看容器ip

~~~
docker inspect --format='{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aq)
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1f51d489c081df83.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

或者先进入容器，然后执行cat /etc/hosts查看即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a9ce3988aa0f895f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

11、停止容器
docker stop 容器名/容器id

12、查看容器日志
docker logs -f 容器名/容器id

13、搜索镜像
docker search 镜像名
~~~
docker search mysql
~~~

14、重启docker
~~~
systemctl restart docker
~~~

15、删除none镜像

使用docker images 命令查看到很多none镜像，占空间无作用。可以删除之
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0fe9e174c39e6f70.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
docker stop $(docker ps -a | grep "Exited" | awk '{print $1 }') //停止容器
docker rm $(docker ps -a | grep "Exited" | awk '{print $1 }') //删除容器
docker rmi $(docker images | grep "none" | awk '{print $3}') //删除镜像
~~~

16、重命名镜像
>- 1fea588994f9 为镜像id
>- 192.168.10.11:81/test/demo1:latest 为目标镜像名
~~~
docker tag 1fea588994f9 192.168.10.11:81/test/demo1:latest
~~~

17、推送镜像到docker私服
~~~
 docker push 192.168.10.11:81/test/demo1:latest
~~~


18、查看所有容器（包括up和exit）
docker ps -a

19、删除容器
docker rm xxx

20、删除镜像
docker rmi xxx
