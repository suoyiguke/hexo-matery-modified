---
title: nginx-配置https.md
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
title: nginx-配置https.md
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


    # HTTPS server
    server {
        listen 443 ssl;
        server_name   172.18.5.70;
        ssl_certificate 192.168.111.124.cer;
        ssl_certificate_key nginx_cert.key;
        ssl_session_cache    shared:SSL:1m;
        ssl_session_timeout  5m;
        server_tokens off;
        fastcgi_param   HTTPS               on;
        fastcgi_param   HTTP_SCHEME         https;
        location / {

             
            proxy_pass http://172.18.5.70:8085/; #代理转发的路径
            proxy_redirect default;
            proxy_ssl_session_reuse off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-for $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            error_page 502 = /500.html;
        }

    }

    server {
        listen       8085;
        server_name  172.18.5.70;
        location / {
            root   D:\ca\dingtalkh5;
            index  index.html;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

      
    }


}

~~~
