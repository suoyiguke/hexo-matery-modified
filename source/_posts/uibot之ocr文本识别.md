---
title: uibot之ocr文本识别.md
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
title: uibot之ocr文本识别.md
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
社区版的uibot在ocr上提供了三个操作模块
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5af43262b32c3b9f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###1、使用ORC
1、屏幕ORC，可以识别指定屏幕范围内的文字
~~~
dim sText = ""
dim iRet = ""
dim sRet = ""
dim objPoint = ""
#icon("@res:81bet5rg-mcvm-mmmr-okh1-bbtd35v7g8gd.png")
sText = OCR.ScreenOCREx({"wnd":[{"cls":"QWidget","title":"MySQL技术内幕  InnoDB存储引擎  第2版.pdf - WPS Office","app":"wps"}]},{"x":815,"y":165,"width":669,"height":837},false,10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"bSetForeground":true})
iRet = Dialog.MsgBox(sText,"UiBot","0","1",0)

~~~

2、图像ORC识别，指定图片进行ORC识别文字

~~~
dim sText = ""
dim iRet = ""
dim sRet = ""
dim objPoint = ""
#icon("@res:81bet5rg-mcvm-mmmr-okh1-bbtd35v7g8gd.png")
sText = OCR.ScreenOCREx({"wnd":[{"cls":"QWidget","title":"MySQL技术内幕  InnoDB存储引擎  第2版.pdf - WPS Office","app":"wps"}]},{"x":815,"y":165,"width":669,"height":837},false,10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"bSetForeground":true})
iRet = Dialog.MsgBox(sText,"UiBot","0","1",0)

~~~
###3、使用智能识别
~~~
dim sText = ""
dim iRet = ""
dim sRet = ""
dim objPoint = ""

#icon("@res:4go9ji9q-ebmt-cd46-e34b-4ktmndlejq78.png")
UiDetect Scope("3v3ji49m-gh5u-t890-0j2v-rrfo9lo8oqbb",{"wnd":[{"cls":"QWidget","title":"MySQL技术内幕  InnoDB存储引擎  第2版.pdf - WPS Office","app":"wps"}],"cv_engine_version":1},{"x":727,"y":113,"width":793,"height":830},10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})

#icon("@res:c329klbf-glgg-8tv6-du1i-8bo4ubhpm917.png")
text = UiDetection.Get({"wnd":[{"cls":"QWidget","title":"MySQL技术内幕  InnoDB存储引擎  第2版.pdf - WPS Office","app":"wps"}],"cv_engine_version":1,"cv_region":{"x":727,"y":113,"width":793,"height":830},"cv_descriptor":{"cv_handle":"\"3v3ji49m-gh5u-t890-0j2v-rrfo9lo8oqbb\"","match_version":0,"target":{"cls_type":200,"height":411,"icon_path":"3DB6311F-B84D-410b-A90A-49931A5EE249.png","width":660,"x":95,"y":10}}},"OCR",10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"bSetForeground":true})
iRet = Dialog.MsgBox(text,"UiBot","0","1",0)
End UiDetect


~~~
