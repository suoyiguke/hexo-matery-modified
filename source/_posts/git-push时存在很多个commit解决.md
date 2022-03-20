---
title: git-push时存在很多个commit解决.md
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
title: git-push时存在很多个commit解决.md
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

###在idea中直接 fetch一下就行了

![image.png](https://upload-images.jianshu.io/upload_images/13965490-fcdf59f4d9d3399c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###命令中新开分支，直接复制指定的commit代码
1、先创建分支并切换之
~~~
git checkout -b test3  remotes/origin/develop
git branch 
~~~

2、拉去指定commit到当前分支
~~~
 git cherry-pick bb4e5c0cf4cf8fd8656902adbb14fcb4e15ede33
~~~

###idea中push时可以push到指定分支上

![image.png](https://upload-images.jianshu.io/upload_images/13965490-85836f9d7ebf9004.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后在也页面上提pull requests时可以指定  原分支为之前push的分支
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5bbed26e1f4ae525.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###idea中可以直观的添加编辑remote
![image.png](https://upload-images.jianshu.io/upload_images/13965490-14a0ed0cf61eea7a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###idea中直观的查看当前分支，和所有分支情况
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e808e56a41d9f783.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
