---
title: Spring-Security-OAuth2.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 权限
categories: 权限
---
---
title: Spring-Security-OAuth2.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 权限
categories: 权限
---
~~~		
<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-oauth2</artifactId>
		</dependency>
~~~


Authorization 就是OAuth2生成的token
~~~
curl 'http://192.168.1.54:9010/t1/rbac/sys/menu/getMenus' \
  -H 'Connection: keep-alive' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Authorization: bearer 1eb3f21d-f393-4a7d-a714-2140e0e3695c' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36' \
  -H 'Origin: http://192.168.1.54:8010' \
  -H 'Referer: http://192.168.1.54:8010/' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' \
  --compressed \
  --insecure
~~~
