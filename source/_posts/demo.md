---
title: demo.md
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
title: demo.md
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
###1、抓取简书，存入excel
~~~
dim iRet = ""
dim hWeb = ""
dim objExcelWorkBook = ""
dim 抓取总数 = ""
dim arrayData = ""
hWeb = WebBrowser.Create("chrome","https://www.jianshu.com/u/807abe8ee897",10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"sBrowserPath":"","sStartArgs":""})
iRet = WebBrowser.WaitPage(hWeb,"",60000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
arrayData = UiElement.DataScrap({"html":{"attrMap":{"id":"list-container","tag":"DIV"},"index":0,"tagName":"DIV"},"wnd":[{"app":"chrome","cls":"Chrome_WidgetWin_1","title":"*"},{"cls":"Chrome_RenderWidgetHostHWND","title":"Chrome Legacy Window"}]},{"Columns":[{"props":["text"],"selecors":[{"className":"note-list","index":0,"prefix":"","tag":"ul","value":"ul.note-list"},{"index":0,"prefix":">","tag":"li","value":"li"},{"className":"content ","index":0,"prefix":">","tag":"div","value":"div.content"},{"className":"title","index":0,"prefix":">","tag":"a","value":"a.title"}]},{"props":["text"],"selecors":[{"className":"note-list","index":0,"prefix":"","tag":"ul","value":"ul.note-list"},{"index":0,"prefix":">","tag":"li","value":"li"},{"className":"content ","index":0,"prefix":">","tag":"div","value":"div.content"},{"className":"abstract","index":0,"prefix":">","tag":"p","value":"p.abstract"}]},{"props":["text"],"selecors":[{"className":"note-list","index":0,"prefix":"","tag":"ul","value":"ul.note-list"},{"index":0,"prefix":">","tag":"li","value":"li"},{"className":"content ","index":0,"prefix":">","tag":"div","value":"div.content"},{"className":"meta","index":0,"prefix":">","tag":"div","value":"div.meta"},{"className":"jsd-meta","index":0,"prefix":">","tag":"span","value":"span.jsd-meta"}]},{"props":["text"],"selecors":[{"className":"note-list","index":0,"prefix":"","tag":"ul","value":"ul.note-list"},{"index":0,"prefix":">","tag":"li","value":"li"},{"className":"content ","index":0,"prefix":">","tag":"div","value":"div.content"},{"className":"meta","index":0,"prefix":">","tag":"div","value":"div.meta"},{"className":"","index":2,"prefix":">","tag":"a","value":"a:nth-child(2)"}]},{"props":["text"],"selecors":[{"className":"note-list","index":0,"prefix":"","tag":"ul","value":"ul.note-list"},{"index":0,"prefix":">","tag":"li","value":"li"},{"className":"content ","index":0,"prefix":">","tag":"div","value":"div.content"},{"className":"meta","index":0,"prefix":">","tag":"div","value":"div.meta"},{"className":"","index":3,"prefix":">","tag":"a","value":"a:nth-child(3)"}]},{"props":["text"],"selecors":[{"className":"note-list","index":0,"prefix":"","tag":"ul","value":"ul.note-list"},{"index":0,"prefix":">","tag":"li","value":"li"},{"className":"content ","index":0,"prefix":">","tag":"div","value":"div.content"},{"className":"meta","index":0,"prefix":">","tag":"div","value":"div.meta"},{"className":"","index":4,"prefix":">","tag":"span","value":"span:nth-child(4)"}]},{"props":["text"],"selecors":[{"className":"note-list","index":0,"prefix":"","tag":"ul","value":"ul.note-list"},{"index":0,"prefix":">","tag":"li","value":"li"},{"className":"content ","index":0,"prefix":">","tag":"div","value":"div.content"},{"className":"meta","index":0,"prefix":">","tag":"div","value":"div.meta"},{"className":"time","index":0,"prefix":">","tag":"span","value":"span.time"}]}],"ExtractTable":0},{"objNextLinkElement":{"html":{"attrMap":{"css-selector":"body>div>div","tag":"DIV"},"index":0,"tagName":"DIV"},"wnd":[{"app":"chrome","cls":"Chrome_WidgetWin_1","title":"*"},{"cls":"Chrome_RenderWidgetHostHWND","title":"Chrome Legacy Window"}]},"iMaxNumberOfPage":5,"iMaxNumberOfResult":-1,"iDelayBetweenMS":1000,"bContinueOnError":false})
objExcelWorkBook = Excel.OpenExcel(@res"简书.xlsx",true)
Dialog.Notify("将数据写入Excel", "UiBot", "0")
抓取总数=Len(arrayData)
Dialog.Notify("共抓到"&抓取总数&"条数据\n开始写入Excel", "UiBot", "0")
Excel.SetColumnWidth(objExcelWorkBook,"Sheet1","A1",120,true)
Excel.WriteRange(objExcelWorkBook,"Sheet1","A1",arrayData)
Excel.InsertRow(objExcelWorkBook,"Sheet1","A1",["标题","摘要","钻石","浏览","评论","喜欢","时间"])
Excel.Save(objExcelWorkBook)
Dialog.Notify("写入数据完成", "UiBot", "0")

~~~
###2、工作demo，抓取表格
1、
~~~
dim iRet = ""
dim hWeb = ""
hWeb = WebBrowser.BindBrowser("ie",10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
iRet = WebBrowser.GoURL(hWeb,"http://raweb.bjca.org.cn/bossraweb/WebLogin.aspx",true,"",30000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
#icon("@res:mc6v7vjh-a34u-of6s-qsv9-7drff3hrkds8.png")
Keyboard.InputText({"html":{"attrMap":{"id":"txtPass","tag":"INPUT"},"index":0,"tagName":"INPUT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},"111111",true,10,10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"sKeyModifiers":[],"sSimulate":"message"})
#icon("@res:81i162om-uu11-qhiv-h17o-o6rrba0anlj2.png")
Mouse.Action({"html":{"attrMap":{"id":"Image1","tag":"INPUT"},"index":0,"tagName":"INPUT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},"left","click",10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"bSetForeground":true,"sCursorPosition":"Center","iCursorOffsetX":0,"iCursorOffsetY":0,"sKeyModifiers":[],"sSimulate":"simulate"})
#icon("@res:kouou9vv-8nq6-tt9d-0agt-rm5d90rfddgo.png")
UiElement.SetSelect({"html":{"attrMap":{"tag":"SELECT"},"index":0,"tagName":"SELECT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},12,"index",{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
#icon("@res:lsmutema-63kv-bs9q-8m2q-sdtuhg4h36dl.png")
Mouse.Action({"html":{"attrMap":{"id":"btNext","tag":"INPUT"},"index":0,"tagName":"INPUT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},"left","click",10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"bSetForeground":true,"sCursorPosition":"Center","iCursorOffsetX":0,"iCursorOffsetY":0,"sKeyModifiers":[],"sSimulate":"simulate"})


~~~


2、
~~~

#icon("@res:vkkfq9tn-ljs3-tkid-3i5a-s65g8iol7jc1.png")
Mouse.Action({"html":{"attrMap":{"id":"TreeView1t37","tag":"A"},"index":0,"tagName":"A"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},"left","click",10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"bSetForeground":true,"sCursorPosition":"Center","iCursorOffsetX":0,"iCursorOffsetY":0,"sKeyModifiers":[],"sSimulate":"simulate"})

//选择 服务渠道名称为 深圳市卫生渠道
//选择 受理点名称 为 第二人民医院受理点
#icon("@res:km710vbr-n9e8-a4e5-n6sc-5h7rl020pc8e.png")
UiElement.SetSelect({"html":{"attrMap":{"id":"comChannel","tag":"SELECT"},"index":0,"tagName":"SELECT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},5,"index",{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
#icon("@res:m9fet8dl-n6lu-me49-r94h-qkpmvf2f9j0k.png")
UiElement.SetSelect({"html":{"attrMap":{"id":"comPlace","tag":"SELECT"},"index":0,"tagName":"SELECT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},11,"index",{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})

//选择日期
#icon("@res:6p8u7gi9-nnbl-pnte-r1be-lhtgptpmehu9.png")
UiElement.SetAttribute({"html":{"attrMap":{"id":"txtStart","tag":"INPUT"},"index":0,"tagName":"INPUT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},"value","2013-01-01",{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
#icon("@res:cc67u5os-e7rp-54u8-nk82-gdbjp0eskvpr.png")
UiElement.SetSelect({"html":{"attrMap":{"id":"comType","tag":"SELECT"},"index":0,"tagName":"SELECT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},1,"index",{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})
#icon("@res:4fcokhhk-4t2k-5f7q-kldf-78vob4nukpos.png")
Mouse.Action({"html":{"attrMap":{"id":"Button3","tag":"INPUT"},"index":0,"tagName":"INPUT"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},"left","click",10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200,"bSetForeground":true,"sCursorPosition":"Center","iCursorOffsetX":0,"iCursorOffsetY":0,"sKeyModifiers":[],"sSimulate":"simulate"})
#icon("@res:5i9bf8ja-ako7-ofmf-95g9-82naknl7d7r0.png")
UiElement.Wait({"html":{"attrMap":{"css-selector":"body>form>table>tbody>tr>td","parentid":"form1","tableCol":"1","tableRow":"1","tag":"TD"},"index":5,"tagName":"TD"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},"show",10000,{"bContinueOnError":false,"iDelayAfter":300,"iDelayBefore":200})


~~~

3、
~~~
dim iRet = ""
dim hWeb = ""
dim objExcelWorkBook = ""
dim 抓取总数 = ""
dim arrayData = ""

//数据抓取
//分页时间间隔，10秒的反应时间。因为系统实在是太慢
arrayData = UiElement.DataScrap({"html":{"attrMap":{"id":"GridView1","tag":"TABLE"},"index":0,"tagName":"TABLE"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},{"Columns":[],"ExtractTable":1},{"objNextLinkElement":{"html":{"attrMap":{"href":"http://raweb.bjca.org.cn/bossraweb/images/next.gif","parentid":"GridView1","tag":"IMG"},"index":0,"tagName":"IMG"},"wnd":[{"app":"iexplore","cls":"IEFrame","title":"*"},{"cls":"Internet Explorer_Server"}]},"iMaxNumberOfPage":205,"iMaxNumberOfResult":-1,"iDelayBetweenMS":10000,"bContinueOnError":false})

objExcelWorkBook = Excel.OpenExcel(@res"test.xlsx",true)
Dialog.Notify("将数据写入Excel", "UiBot", "0")
抓取总数=Len(arrayData)
Dialog.Notify("共抓到"&抓取总数&"条数据\n开始写入Excel", "UiBot", "0")
Excel.SetColumnWidth(objExcelWorkBook,"Sheet1","A1",120,true)
Excel.WriteRange(objExcelWorkBook,"Sheet1","A1",arrayData)
Excel.InsertRow(objExcelWorkBook,"Sheet1","A1",["证书用户","证书类型","业务类型","密码卡号","组织机构代码","计算机代码","统一社会信用代码","纳税人识别码","证书有效期","应收金额","实收金额","业务审核时间","业务状态","申请方式","服务渠道","受理点","操作员","备注","一级单位","二级单位","外部交易号","办理情况备注","显示发票信息","产品服务退货"])
Excel.Save(objExcelWorkBook)
Dialog.Notify("写入数据完成", "UiBot", "0")


~~~
