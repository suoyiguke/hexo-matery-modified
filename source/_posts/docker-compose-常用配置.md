---
title: docker-compose-常用配置.md
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
title: docker-compose-常用配置.md
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
### 常用
1、docker-compose中容器设置上海时区
~~~
 environment:
      TZ: "Asia/Shanghai"
~~~
2、总是重启容器
~~~
restart: always
~~~
3、端口映射
~~~
    ports:
      - 6379:6379
~~~
4、开启容器特权
~~~
privileged: true
~~~
5、使用Dockerfile的形式，重新bulid
docker-compose up --build
~~~
 build:
    context: .
    dockerfile: ./Dockerfile
~~~
6、docker-compose.yml目录挂载
~~~
volumes:
    - "./slave/crontab:/etc/crontab"
~~~
ps: 修改crontab文件不能马上刷新到容器里，需要重启容器

7、容器启动失败，进入容器排查问题
进入容器不了，一下子就停止。让容器不退出的方法：
command:  sleep 999999
![image.png](https://upload-images.jianshu.io/upload_images/13965490-59e2c7745c567a58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

多个命令
~~~
    command: bash -c "sleep 9999 && java -jar -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 /ias/identityauthsrv-1.0.0-base-linux-release.jar"

~~~

8、java环境
~~~
version: "3"
services:
  jdk:
    image: java:8
    volumes:
      - ./work:/work
    ports:
      - "8080:8080"
    command: java -jar /work/demo1-4.jar

~~~

###docker-compose 的网络配置
######设置容器自定义ip

###指定容器的虚拟ip
这里的11.11.11.11就是指定的ip
~~~
version: "2"
services:
  redis:
    image: redis
    ports:
      - 6379:6379
    command:
      redis-server /usr/local/etc/redis/redis.conf
    volumes:
      - ./data:/data
      - ./redis.conf:/usr/local/etc/redis/redis.conf
      - /etc/localtime:/etc/localtime
    restart: always
    networks:
      hx_net:
        ipv4_address: 11.11.11.11


networks:
  hx_net:
    driver: bridge
    ipam:
      config:
        - subnet: 11.11.11.0/16

~~~

启动时输出：
Creating network "redis_hx_net" with driver "bridge"
Creating redis_redis_1 ... 
### 直接使用宿主机的网络
network_mode: host

~~~
version: "2"
services:
  redis:
    image: redis
    network_mode: host
    command:
      redis-server /usr/local/etc/redis/redis.conf
    volumes:
      - ./data:/data
      - ./redis.conf:/usr/local/etc/redis/redis.conf
      - /etc/localtime:/etc/localtime
    restart: always
~~~
