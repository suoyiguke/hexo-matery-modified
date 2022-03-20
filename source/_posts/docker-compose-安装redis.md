---
title: docker-compose-安装redis.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
---
title: docker-compose-安装redis.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
1、目录结构
![image.png](https://upload-images.jianshu.io/upload_images/13965490-62e5b43ee92d9ec7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、docker-compose.yml
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

3、redis.conf
copy一份配置文件即可
