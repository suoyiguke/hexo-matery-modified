---
title: 提交某个commit到指定分支下.md
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
title: 提交某个commit到指定分支下.md
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
git log  //查看提交的日志，复制要合并的那个分支的commit id</span>
git checkout 要合并的分支  // 切换到要合并的分支上
git cherry-pick 上面复制的那个要合并的commit id  // 提交该commit到当前分支


git cherry-pick  2a52511857138eb930b4446acc84a3c2de3f391f
