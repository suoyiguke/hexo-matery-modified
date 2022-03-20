---
title: Nginx问题.md
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
title: Nginx问题.md
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
###post请求body过大
Nginx代理请求转发，出现` nginx 413 request too large` 原因是post请求的body过大。可以通过调整client_max_body_size解决

这个属性可以配置在http节点下（http全局），可以配置在server节点下（server全局），也可以配置在location节点下（单应用）。要注意的是，这个属性在不配置的情况下默认值是1m，也就是限制了请求实体的大小为1m。

http节点下：
~~~
http {
    # 将Nginx代理的所有请求实体的大小限制为20m
    client_max_body_size 20m;
}
~~~
server节点下：
~~~
server {
    # 将该服务下的所有请求实体的大小限制为20m
    client_max_body_size 20m;
}
~~~
location节点下：
~~~
location /yanggb {
    # 将此路由请求的实体大小限制为20m
    client_max_body_size 20m;
}
~~~
保存之后要记得重启Nginx使修改后的配置生效。

service nginx restart


###请求超时

504 Gateway Time-out


调整 proxy_read_timeout 3000s;
