---
title: docker-script启动.md
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
title: docker-script启动.md
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
总用量 133328
-rw-r--r--. 1 root root       128 12月  6 11:52 Dockerfile
-rwxr-xr-x. 1 root root        38 12月  6 11:51 make.sh
-rw-r--r--. 1 root root 136509486 12月  6 11:44 mgb_treasure_system-0.0.1-SNAPSHOT-1.jar
-rwxr-xr-x. 1 root root       226 12月  6 11:51 run.sh
-rwxr-xr-x. 1 root root        93 12月  6 11:51 stop.sh





rest.sh
~~~
cd /home/cloud/mgb_treasure_system
docker stop mgb_treasure_system

docker rm mgb_treasure_system
docker rmi mgb_treasure_system
docker build -t mgb_treasure_system .

docker run -d -p 8081:8081 --restart=always --name mgb_treasure_system mgb_treasure_system
docker network connect eureka mgb_treasure_system

~~~

>docker network connect eureka mgb_treasure_system  mgb_treasure_system 容器连上eureka 的网络！！

Dockerfile
~~~

FROM java:8
VOLUME /tmp
ADD mgb_treasure_system-0.0.1-SNAPSHOT-1.jar app.jar
EXPOSE 8081
ENTRYPOINT ["java","-jar","./app.jar"]
~                                                                                                                                                                                                                  
~~~
