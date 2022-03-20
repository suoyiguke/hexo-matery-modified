---
title: jquery-中修改Headers.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: web
categories: web
---
---
title: jquery-中修改Headers.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: web
categories: web
---
修改jq源码
~~~
 var token = localStorage.getItem("token")
                    if(token){
                        requestHeadersNames['token'] = 'token'
                        requestHeaders['token'] = token
                        console.log(requestHeadersNames,requestHeaders)
                    }
~~~

客户端
~~~
$(function() {
   //设置token

      localStorage.setItem("token",123456)

   $('#loadObj').load('http://192.168.10.106:8080/test/user/list?cPage=2&pSize=20')

});
~~~

后端
~~~
   response.setHeader("Access-Control-Allow-Headers", "content-type,x-requested-with,Authorization, x-ui-request,lang,token");
~~~
