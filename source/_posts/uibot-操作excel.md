---
title: uibot-操作excel.md
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
title: uibot-操作excel.md
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
1、二维数组arrayData 写入excel
~~~

objExcelWorkBook = Excel.OpenExcel(@res"test1.xlsx",true)
Dialog.Notify("将数据写入Excel", "UiBot", "0")
抓取总数=Len(arrayData)
Dialog.Notify("共抓到"&抓取总数&"条数据\n开始写入Excel", "UiBot", "0")
//Excel.SetColumnWidth(objExcelWorkBook,"Sheet1","A1",120,true)
SunExcel.AutoFitActiveSheet()
Excel.WriteRange(objExcelWorkBook,"Sheet1","A1",arrayData)

Excel.InsertRow(objExcelWorkBook,"Sheet1","A1",["证书用户","证书类型","业务类型","密码卡号","组织机构代码","计算机代码","统一社会信用代码","纳税人识别码","证书有效期","应收金额","实收金额","业务审核时间","业务状态","申请方式","服务渠道","受理点","操作员","备注","一级单位","二级单位","外部交易号","办理情况备注","显示发票信息","产品服务退货"])
Excel.Save(objExcelWorkBook)
Dialog.Notify("写入数据完成", "UiBot", "0")

~~~
