---
title: 撤销到某个commitid-push.md
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
title: 撤销到某个commitid-push.md
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


###remote操作
1、查看所有remote
 git remote -v

2、切换远程仓库地址：
①、修改远程仓库地址

【git remote set-url origin URL】 更换远程仓库地址，URL为新地址。

②、先删除远程仓库地址，然后再添加

【git remote rm origin】 删除现有远程仓库 
【git remote add origin url】添加新远程仓库


###分支操作

1、查看当前分支 git branch -a


~~~
$ git branch -a
  develop
* master
  remotes/origin/HEAD -> origin/develop
  remotes/origin/develop
  remotes/origin/master

~~~

2、 切换分支
git checkout -b  remotes/origin/develop

3、删除本地分支

分享一个小技巧，我们在很多时候需要删除一些本地无用分支，假如我们想要删除具体分支，我们可以这么做：

git branch -D branchName

但是有些时候我们要删除很多分支，比如除了master外的所有分支，那么我们可以这么做：

git checkout master
git branch | grep -v 'master' | xargs git branch -D
复制代码
具体执行步骤是：

切换到master分支
将git branch的结果进行筛选，除去master
将处理后的结果作为git branch -D的参数来进行删除分支


###撤销push
git log


1. git log

2. git reset --soft 43dc0de914173a1a8793a7eac31dbb26057bbee4

3. git push origin master --force (强制提交)


![image.png](https://upload-images.jianshu.io/upload_images/13965490-3db560014be978aa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


 

