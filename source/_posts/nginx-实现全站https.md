---
title: nginx-实现全站https.md
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
title: nginx-实现全站https.md
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
方法一、使用rewrite  类似于浏览器重定向。url会被改变
~~~
  server {
        listen       80;
        server_name  xxx;#访问的路径
        rewrite ^(.*)$   https://$host:8080$1 permanent;
    }

~~~

方法一、或者使用  return 301。url会被改变
~~~
 server {
        listen       80;
        server_name  xxx;#访问的路径
        return 301 https://$host:8080$1;
    }

~~~
