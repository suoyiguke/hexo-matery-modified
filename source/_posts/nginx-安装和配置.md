---
title: nginx-安装和配置.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: nginx
categories: nginx
---
---
title: nginx-安装和配置.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: nginx
categories: nginx
---
docker-compose.yml
~~~
version: "2"
services:
  https-nginx-server:
    image: nginx
    container_name: "https-nginx-server"
    ports:
      - 80:80
    volumes:
      - ./conf.d:/etc/nginx/conf.d
      - ./conf/nginx.conf:/etc/nginx/nginx.conf
      - ./log:/var/log/nginx
      - ./www:/var/www
      - /etc/letsencrypt:/etc/letsencrypt

    network_mode: 'host'
    restart: always

~~~


![image.png](https://upload-images.jianshu.io/upload_images/13965490-e98394d1879c22dd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>  root   /var/www; 项目资源目录为 /var/www; 默认是 `/etc/nginx/html`
~~~
worker_processes  1;
events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    gzip  on;
    server {
        listen       80;
        server_name  localhost;
        location / {
            root   /var/www;
            index  index.html;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

      
    }


}

~~~
