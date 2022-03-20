---
title: docker-compose-部署springboot.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
---
title: docker-compose-部署springboot.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: springboot
categories: springboot
---
~~~
version: "3"
services:
  box:
    image: java:8
    volumes:
      - ./work:/work
    ports:
      - "8080:8080"
    environment:
      TZ: "Asia/Shanghai"
    command: java -jar /work/box-25.jar --weixinapp.appid=wx1b4d0120312076d6 --weixinapp.secret=7d21f8dd1193f3688d6c16918bad60a6 --server.ssl.key-store=classpath:hdwl.51js.net.cn.jks --server.ssl.key-store-password=b6865p939674dyl

~~~
