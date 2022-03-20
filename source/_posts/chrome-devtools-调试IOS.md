---
title: chrome-devtools-调试IOS.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: IOS
categories: IOS
---
---
title: chrome-devtools-调试IOS.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: IOS
categories: IOS
---
1、windows 安装 itunes 软件，将会安装ios的usb驱动

2、下载ios_webkit_debug_proxy.exe
~~~
https://github.com/google/ios-webkit-debug-proxy/releases/tag/v1.8.6
~~~

3、ios 开启 web inter


4、执行
~~~
D:\搜狗高速下载\ios-webkit-debug-proxy-1.8.6-win64-bin>ios_webkit_debug_proxy.exe -f chrome-devtools://devtools/bundled/inspector.html
Listing devices on :9221
Connected :9222 to iPhone (4e576154ee7a5ea80fb679026bfb0c7ae2022666)
~~~

5、访问  http://localhost:9221/ 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3cee8d12f41cba39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
