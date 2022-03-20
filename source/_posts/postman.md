---
title: postman.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开发工具
categories: 开发工具
---
---
title: postman.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开发工具
categories: 开发工具
---
###环境变量
![image.png](https://upload-images.jianshu.io/upload_images/13965490-9806ed1ae40aae4d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用：
>{{sd}}/client/security/loginIp?username=大雄&password=Foonsu2021

###传multipartFile文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-398ce1027f0437ed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###将浏览器中的请求导入postman

1、将请求导出为curl命令
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a18cfa5f3821ed84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
~~~
curl 'http://192.168.1.54:9010/t1/treasureSystem/mbUndertakesOrder/supplierQueryPageList' \
  -H 'Connection: keep-alive' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'page-token: ef724b6d40517ebe1e6e07dcb523ab93' \
  -H 'Authorization: bearer 6fa47f36-e3b1-43be-92ea-c0c60305ba65' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36' \
  -H 'Content-Type: application/json' \
  -H 'Origin: http://192.168.1.54:8010' \
  -H 'Referer: http://192.168.1.54:8010/' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' \
  --data-raw '{"orderNo":"CT202111240133100006","supplierNo":"SP1631527145585"}' \
  --compressed \
  --insecure
~~~

2、导入postman
![image.png](https://upload-images.jianshu.io/upload_images/13965490-413d4201b9783560.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7e76ab61df578865.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



###postman脚本 Postman Script 

![image](https://upload-images.jianshu.io/upload_images/13965490-a45944b320ed5f8b?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240 "image") 

*   `pre-request`脚本，是在对API进行请求之前的脚本，一般用于动态生成参数、JSON数据包、链接地址等。
*   `test`脚本，其实更应该叫`post-request`，实在完成API访问并得到其response回应之后运行的脚本，一般用于获取response的内容，用于之后对于别的资源的请求，如获取页面标题和内容等。


1、全局变量
pm.globals.set("Authorization",__access_token);
console.log(pm.globals.get('Authorization'))

2、普通变量
var nm = pm.variables.get("普通变量名");


3、获取响应
var respData = JSON.parse(responseBody);
var __access_token = respData.data.access_token


4、 环境变量
// 获取环境变量
var v = pm.environment.get("变量名称");
 
// 设置环境变量 只能存储字符串，如果是对象的话则无法在下次运行时获取到内容
// 如需要存储JSON数据，可以用JSON.stringify(..)存储，再用JSON.parse(..)转化为对象使用
pm.environment.set("变量名称", 变量内容);
 
// 清除某个环境变量
pm.environment.unset("环境变量名");
 

 



###在请求头的auth2 token 中使用环境变量
1、login方法的testscript里面写上代码
~~~
var respData = JSON.parse(responseBody);
var __access_token = respData.data.access_token;
pm.globals.set("Authorization",__access_token);
~~~
2、在查询列表等接口里面添加上这个
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8c41dbcab9ccbf62.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


之后直接请求login接口，再也不用手动刷新token了
