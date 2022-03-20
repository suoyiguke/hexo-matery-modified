---
title: git-忽略本地修改，不将修改提交到远程.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: git
categories: git
---
---
title: git-忽略本地修改，不将修改提交到远程.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: git
categories: git
---
本地项目的配置文件自己修改了不想提交到仓库，每次都要rollback非常不方便。可以试下这个方法：


忽略：
~~~
git update-index --assume-unchanged ./sd-schedule/src/main/resources/properties/redis.properties
~~~

那么这个redis.properties就会被忽略，提交时检测不到修改：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2bc65cce78f26387.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


恢复：
~~~
$ git update-index --no-assume-unchanged ./sd-schedule/src/main/resources/properties/redis.properties
~~~

执行后就能正常提交修改了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-337b32e018cae40f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
