---
title: Vim.md
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
title: Vim.md
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
###编辑模式
1、i 进入编辑模式，ESC 退出编辑模式
2、退出编辑模式后 wq:保存文件 :wq! 强制保存 
3、 退出编辑模式后 :q! 丢弃变更退出vim


###移动光标
1、HJKL 移动光标；H左L右 J下K上
2、输入:n，代表跳转到第n行，如:79，就跳转到第79行。


###搜索
 退出编辑模式后 /搜索关键词+回车 搜索文件内容；继续按n 下一个匹配内容

###编辑快捷键
在编辑模式之内 ctrl+u恢复撤销
退出编辑模式后  U 撤销操作
退出编辑模式后 DD删除光标所在一行



### 翻屏
shift + G 跳到文件末尾
ctrl+f: 下翻一屏。
ctrl+b: 上翻一屏。
ctrl+d: 下翻半屏。
 ctrl+u: 上翻半屏。
ctrl+e: 向下滚动一行。
ctrl+y: 向上滚动一行。
n%: 到文件n%的位置。
zz: 将当前行移动到屏幕中央。
zt: 将当前行移动到屏幕顶端。
zb: 将当前行移动到屏幕底端。
