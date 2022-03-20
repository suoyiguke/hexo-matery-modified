---
title: uibot-之浏览器模拟操作.md
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
title: uibot-之浏览器模拟操作.md
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

###鼠标的模拟移动和模拟点击
想页面上的下拉框是没办法使用元素分析器分析到的。我们可以通过鼠标的模拟移动，相对位置来完成！

![image.png](https://upload-images.jianshu.io/upload_images/13965490-9797ae78009038d2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
选相对位置，这样是相对鼠标的位置。然后慢慢调整纵坐标的值即可。直到选到我们需要的元素！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0d098d7cb05c1682.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这里也需要使用模拟点击，而不是使用正常的点击。因为正常的点击需要选择目标页面元素。模拟点击不需要，模拟点击的意思直接点击一下鼠标左键，没有移动

~~~
//选择 服务渠道名称为 深圳市卫生渠道
#icon("@res:tlgss1o4-efhf-gjav-tkma-730ofku7efsg.png")
Mouse.Action({"html":{"attrMap":{"id":"comChannel","tag":"SELECT"},"index":0,"tagName":"SELECT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},"left","click",10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"bSetForeground":true,"sCursorPosition":"Center","iCursorOffsetX":0,"iCursorOffsetY":0,"sKeyModifiers":[],"sSimulate":"simulate"})
Mouse.Move(0, 80, true,{"iDelayAfter":300,"iDelayBefore":200})
Mouse.Click("left", "click", [],{"iDelayAfter":300,"iDelayBefore":200})

~~~
>这种方式来选择下拉框存在很大的弊端！若浏览器没有全屏，而代码是在全屏下测试通过的。那么最终点击的y轴坐标将不能达到目的！

###uibot其实有提供这个设置元素选择
直接使用这个设置元素选择就行了，上面使用鼠标模拟移动和模拟点击可以换成这个方式更快捷
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e7ab86bb49af3a3f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以按value、顺序选择。我这里按option下拉列表的顺序选择。选择第5个
![image.png](https://upload-images.jianshu.io/upload_images/13965490-918055bc8b47c1f5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-e3271c5ef100fea0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

我们还来可以根据指定文本或者value属性来选择下拉框。如
![image.png](https://upload-images.jianshu.io/upload_images/13965490-605c281061bd0cab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###操作时间控件选择时间
我们根本不需要去模拟鼠标点击时间控件，因为这是一个非常麻烦的流程。其实我们可以直接设置input的value属性。设置为具体的时间
![image.png](https://upload-images.jianshu.io/upload_images/13965490-07d1e89980640a89.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e2abf242c328ab50.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
//选择日期
#icon("@res:6p8u7gi9-nnbl-pnte-r1be-lhtgptpmehu9.png")
UiElement.SetAttribute({"html":{"attrMap":{"id":"txtStart","tag":"INPUT"},"index":0,"tagName":"INPUT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},"value","2013-01-01",{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
~~~
