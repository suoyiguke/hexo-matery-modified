---
title: shell功能代码.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: shell
categories: shell
---
---
title: shell功能代码.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: shell
categories: shell
---
1、查看内存使用百分比
~~~
free | sed -n '2p' | gawk 'x = int(( $3 / $2 ) * 100) {print x}' | sed 's/$/%/'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7efc5f55015bfb31.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
2、查看磁盘实用百分比
~~~
df -h /dev/sda1 | sed -n '/% \//p' | gawk '{ print $5 }'
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7493c7403df75f09.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、获取活跃用户连接数
~~~
uptime | sed 's/user.*$//' | gawk '{print $NF}'
~~~

4、查看僵尸进程
~~~
ps -al | gawk '{print $2,$4}' | grep Z
~~~
5、查看最近登录的ip和登录次数
~~~
last | awk '{S[$3]++} END{for(a in S ) {print S[a],a}}' |uniq| sort -rh
~~~
