---
title: uibot-开发遇到的问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: uibot
categories: uibot
---
---
title: uibot-开发遇到的问题.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: uibot
categories: uibot
---
1、遍历list下的按钮/链接。点击一个按钮/链接 又切换回原来的浏览器tab页
~~~
//点击a标签打开信tab链接，签到后返回贴吧主页tab
// Mouse.Action(value,"left","click",10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"bSetForeground":true,"sCursorPosition":"Center","iCursorOffsetX":0,"iCursorOffsetY":0,"sKeyModifiers":[],"sSimulate":"simulate"})
// bRet = WebBrowser.SwitchTab(hWeb,"title",title,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
~~~

2、获取select目标元素下面的所有option
~~~
#icon("@res:8jkj64sq-i48u-8hh2-e0sl-5j9rq8evtpv6.png")
arrElement = UiElement.GetChildren({"html":[{"id":"comPlace","tag":"SELECT"}],"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
For Each value In arrElement
 
#icon("@res:default.png")
sRet = UiElement.GetAttribute(value,"aaname",{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
TracePrint(sRet)
Next
~~~
