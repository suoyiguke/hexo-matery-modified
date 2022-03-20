---
title: 同一个Nginx服务器同一端口配置多个代理服务.md
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
title: 同一个Nginx服务器同一端口配置多个代理服务.md
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
~~~
 #HTTP服务器
   server {
        #监听80端口，80端口是知名端口号，用于HTTP协议
        listen       80;
        
        #定义使用www.xx.com访问
        server_name  nginx.test.com;
        
        
        #编码格式
        charset utf-8;
        
        #代理配置参数
        proxy_connect_timeout 180;
        proxy_send_timeout 180;
        proxy_read_timeout 180;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarder-For $remote_addr;
        
       
 
        #默认指向product的server
        location / {
            proxy_pass http://product_server;
        }
 
		#使用location对不同请求做相应处理
        location /product/{
            proxy_pass http://product_server;
        }
 
        location /order/ {
            proxy_pass http://order_server;
        }
        
    }
~~~
