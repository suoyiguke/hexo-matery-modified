---
title: 打包某次commit到压缩文件.md
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
title: 打包某次commit到压缩文件.md
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
打包某次commit：
git diff-tree -r --no-commit-id --name-only f4710c4a32975904b00609f3145c709f31392140 | xargs tar -rf update_201800001.tar
