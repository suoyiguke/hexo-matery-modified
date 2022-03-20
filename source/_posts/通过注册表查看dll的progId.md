---
title: 通过注册表查看dll的progId.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
---
title: 通过注册表查看dll的progId.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
找到jsp中的调用代码
~~~


方法定义
function $LoadControl(CLSID, ctlName, testFuncName, addEvent) 

调用
var bOK = $LoadControl("3F367B74-92D9-4C5E-AB93-234F8A91D5E6", "XTXAPP", "SOF_GetVersion()", true);




~~~

这个CLSID是3F367B74-92D9-4C5E-AB93-234F8A91D5E6。打开注册表后搜索3F367B74-92D9-4C5E-AB93-234F8A91D5E6这个字符串。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8fd592862cf30328.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


搜索结果如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f4541e35d5314c8b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


可以得到dll名字和路径：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-81c078725548dd9a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


还有它的ProgID：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-db99ad05561b9b30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这个`XTXAppCOM.XTXApp.1` 就是用在javascript代码或者java代码中调用com组件的。

