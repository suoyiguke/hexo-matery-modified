---
title: api.md
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
title: api.md
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

###字符串
1、拼接
~~~
Dialog.Notify("共抓到"&抓取总数&"条数据\n开始写入Excel", "UiBot", "0")
~~~

2、字符串是否包含
~~~
 InStr(arrayData[index],"条记录",0,true) =
~~~
###数组
1、简单的value遍历
~~~
For Each value In arrayData
 
 Log.Info(value)
 
Next
~~~

2、复杂的遍历，可以使用循环计数器i，和设置步长。初始值和结束值
~~~
For index = 0 To Len(arrayData) step 1
Log.Error(arrayData[index])
Next

~~~

3、长度
~~~
抓取总数=Len(arrayData)
~~~

###数据类型
转int
pageNumber = CInt( DigitFromStr(arrRet[1]))


###json
Dim zz=  JSON.Parse(sRet)
