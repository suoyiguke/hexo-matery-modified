---
title: linux-服务器-请求超时-Connection-timed-out--connect,.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
---
title: linux-服务器-请求超时-Connection-timed-out--connect,.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
![image.png](https://upload-images.jianshu.io/upload_images/13965490-690d86585bf30eff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/13965490-47b63c5ff245cc12.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###解决
sysct1.conf
~~~
net.ipv4.tcp_fin_timeout = 2
net.ipv4.tcp_tw_reuse = 0
net.ipv4.tcp_tw_recycle = 0
~~~

net.ipv4.tcp_tw_reuse = 0 表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭 

 net.ipv4.tcp_tw_recycle = 0 表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭  

net.ipv4.tcp_fin_timeout = 60 表示如果套接字由本端要求关闭，这个参数决定了它保持在FIN-WAIT-2状态的时间（可改为30，一般来说FIN-WAIT-2的连接也极少）

