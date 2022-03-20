---
title: jquery-每次参数请求带上token.md
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
title: jquery-每次参数请求带上token.md
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
~~~
   // 封装jq的ajax函数
  function sendData(url,data,func,type){

      //设置token
      data['token'] = 123456;

    return $.get(url,data,func,type);
  }

  //发起请求
  sendData('http://192.168.10.106:8080/test/user/list?cPage=2&pSize=20',{},function(e) {
                 alert(e)
             },'json')

~~~
