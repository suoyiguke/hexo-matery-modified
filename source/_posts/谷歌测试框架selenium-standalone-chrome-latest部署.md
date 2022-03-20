---
title: 谷歌测试框架selenium-standalone-chrome-latest部署.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
---
title: 谷歌测试框架selenium-standalone-chrome-latest部署.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
###docker-compose.yml
~~~
version: '2'
services:
  chrome-flow:
    image: selenium/standalone-chrome:latest
    container_name: py_pachon_chrome
    shm_size: 2g
    restart: always

  py_pachon:
    build:
      context: .
      dockerfile: ./Dockerfile
    image: py_app:3
    container_name: py_pachon
    environment:
      dblink: /code/dblink-prod.properties
      access_token: 68518eaa2d7012fc0bf9e0bb0eea9466090c7ef5547423f0ef4c537ea77b376e
      flag: True
    restart: always

~~~


###Dockerfile
~~~
FROM python:3.7

ADD / /code

WORKDIR /code

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

CMD ["python3", "/code/job.py"]
~~~



### 进阶
- 指定容器别名 links:
      - py_pachon_chrome:py_pachon_chrome_1  左边表示程序中指定的host(别名)，右边映射上面“selenium/standalone-chrome:latest”的容器名


~~~
[root@tianyi video-crawler]# cat docker-compose.yml 
version: '2'
services:
  py_pachon_chrome:
    image: selenium/standalone-chrome:latest
    container_name: py_pachon_chrome_1
    shm_size: 2g
    restart: always

  pypachon:
  #  build:
  #    context: .
   #   dockerfile: ./Dockerfile
    image: py_app:4
    #container_name: pypachon
    environment:
      dblink: /code/dblink-prod.properties
      access_token: 68518eaa2d7012fc0bf9e0bb0eea9466090c7ef5547423f0ef4c537ea77b376e
      flag: f
    restart: always
    links:
      - py_pachon_chrome:py_pachon_chrome_1
    volumes:
      - ./py:/code
    # 执行命令
    command: python3 -u job.py

~~~

-
