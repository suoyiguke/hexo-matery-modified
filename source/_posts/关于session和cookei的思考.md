---
title: 关于session和cookei的思考.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
---
title: 关于session和cookei的思考.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
session是基于cookie实现的。浏览器会自动生成一个JSESSIONID，传到后端做标识
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2387f56295bdeedb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

若在一个浏览器上保存了session，那么到另一个浏览器上将get 不到指定的session

保存如下session，通过debug可以看到，这里的JSESSIONID=083E0A07E1D76F5AFDB62356DBD36772
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d0b5a790779d6fc0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

因为另一个浏览器会生成另一个不同的JSESSIONID，所以是获取不到之前保存的session的。我们可以将之前的JSESSIONID  copy到这个浏览器里。这样也能得到之前的session。

那web是如何将这个JSESSIONID  传到后端的呢？
我们可以通过抓包得到，请求头如下。有一个`Cookie: JSESSIONID=083E0A07E1D76F5AFDB62356DBD36772`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-72be2f5267b1fafa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
