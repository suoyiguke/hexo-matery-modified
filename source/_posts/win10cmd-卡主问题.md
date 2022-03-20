---
title: win10cmd-卡主问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
---
title: win10cmd-卡主问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: windows
categories: windows
---
windows10 cmd命令提示符/批处理/终端 快速编辑模式bug 程序运行被阻塞 顶部标题栏提示选择 需要回车才能继续执行

为什么出现这种情况？

> 这是快速编辑模式的功能。当程序不断滚动控制台窗口的内容时，用户无法合理地选择文本。因此，控制台主机程序只是停止读取stdout/stderr输出，程序将挂起，直到用户完成操作。这可以更改，您需要关闭启用快速编辑模式选项。
> 请注意，这个“挂起”与程序以远高于控制台主机可以使用的速率生成stdout输出时得到的执行暂停没有本质区别。尽管这些延误是有限的。
> 而且这并不是用户停止程序的唯一方法，他也可以简单地按ctrl+s。按ctrl+q将再次恢复程序。

解决方法：（如果有其他方法，欢迎留言）

## 手动设置法

windows cmd->右键->属性->选项->编辑选项

或

单击左上角图标->属性->选项->编辑选项

取消 快速编辑模式

但是我将cmd设置之后，cmd是禁用了，但运行一个exe终端，发现它还是启动快速编辑模式

所以每个新exe都需手动设置。




###cmder


是啊 愚蠢的bug 可能是控制台因为误操作，导致他等待输入了吧
请更换cmder，无此类bug；
https://www.jianshu.com/p/5b7c985240a7
