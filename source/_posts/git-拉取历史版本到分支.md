---
title: git-拉取历史版本到分支.md
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
title: git-拉取历史版本到分支.md
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


> １．使用gitbash进入git命令行，查看commit记录。操作如下：

```
git log
```

[图片上传失败...(image-bdca21-1603332972392)]

> ２．找到你想提取的目标版本，复制对应的SHA值。

> ３．新建一个分支，操作如下：

```
git branch 新分支名 SHA值
```

[图片上传失败...(image-742005-1603332972392)]

> ４．切换到新的分支，操作如下：

```
git checkout 新分支名
```
