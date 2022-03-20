---
title: uibot-之元素定位之使用UI分析器.md
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
title: uibot-之元素定位之使用UI分析器.md
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
元素定位是 uibot中核心，特别强大的功能。当需要获页面元素的文本时可以和 UiElement.GetValue 配合使用。
我们可以直接使用uibot中自带的`页面元素分析器`：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3eee91696ed2b55b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
在浏览器中定位元素也是非常方便的。比如现在我想定位这个：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-95fa5dd15988c7db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这是分页的总数目，我要得到这个总数目，进行分页抓取数据。

使用页面元素分析器如下：
1、首先选择到这个
![image.png](https://upload-images.jianshu.io/upload_images/13965490-355d77a709102140.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
已经得到了这个元素位置信息。但是这个信息却只能定位 124/124。出现不同的数值就不行了。
我们可以玩外面再挪一层。操作如下：
2、右键SAPN的外面一层 TD，将之copy出来。放到获得元素文本的代码里做参数即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5d716923da3baa13.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


3、如下：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-9b0010e806eb27cd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~

#icon("@res:r5jt3uib-53g0-m0d2-ct53-fdn112o72c92.png")
sRet = UiElement.GetValue({"html":{"attrMap":{"css-selector":"body>form>table>tbody>tr>td>div>div>table>tbody>tr>td>table>tbody>tr>td","parentid":"GridView1","tableCol":"4","tag":"TD"},"index":0,"tagName":"TD"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
TracePrint(sRet)
~~~
