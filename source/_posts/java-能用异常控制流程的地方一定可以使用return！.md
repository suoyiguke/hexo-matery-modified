---
title: java-能用异常控制流程的地方一定可以使用return！.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
1、在构造函数里也可以使用return的方式

将返回包装类GbmResult声明到类的成员变量中：
然后

2、构造函数{
        if (StringUtils.isEmpty(stringStringMap)) {
            this.gbmResult = GbmResultGenerator.genFailResult("未找到对应模板信息");
            return;
        }
}


3、在上层可以这样使用：
~~~
       /**
         * 构造
         */
        ImportOrderByExcelListener listener = new ImportOrderByExcelListener(templateNo, customerCode, platformCode, importDate, importBatch,templateService, relationshipService,excelFieldService, originalOrderService, customerGoodsRelationshipService, codeGenerator);
        GbmResult gbmResult = listener.getGbmResult();
        if(ToolUtil.isNotEmpty(gbmResult)){
            return gbmResult;
        }
~~~
