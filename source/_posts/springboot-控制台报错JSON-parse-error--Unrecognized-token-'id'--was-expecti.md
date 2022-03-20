---
title: springboot-控制台报错JSON-parse-error--Unrecognized-token-'id'--was-expecti.md
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
title: springboot-控制台报错JSON-parse-error--Unrecognized-token-'id'--was-expecti.md
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
springboot 控制台报错JSON parse error: Unrecognized token 'id': was expecting ('true', 'false' or 'null')


前端
~~~
function deldate(did){
$.ajax({  
            type: "POST",   //提交的方法
			dataType: "json",
			//contentType : 'application/json',
            url:"http://ip:8090/id/", //提交的地址    
			data:{
                        "id":did
                    },       
         });
} 
~~~
返回数据格式不规范.当dataType指定为json后,1.4+以上的jquery版本对json格式要求更加严格.如果不是严格的json格式,就不能正常执行success回调函数.

JSON格式:　 
1）键名称：用双引号 括起 　　 
2）字符串：用使用双引号 括起 
3）数字，布尔类型不需要 使用双引号 括起

代码的data的json格式不对所以代码改成了 
~~~
function deldate(did){
var str={"id":sid};
$.ajax({  
            type: "POST",   //提交的方法
			dataType: "json",
			//contentType : 'application/json',
            url:"http://ip:8090/id/", //提交的地址    
			data:JSON.stringify(str),       
         });
} 
~~~
