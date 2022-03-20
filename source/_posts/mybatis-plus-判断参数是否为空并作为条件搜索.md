---
title: mybatis-plus-判断参数是否为空并作为条件搜索.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: mybatis-plus-判断参数是否为空并作为条件搜索.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---

~~~
        Page<MgbConsignmentOrderDto> subsidiaryPage = this.baseMapper.selectPage(page,
                new LambdaQueryWrapper<MgbConsignmentOrderDto>()
                        .eq(ToolUtil.isNotEmpty(mgbConsignmentOrderVo.getOrderNo()),MgbConsignmentOrderDto::getOrderNo, mgbConsignmentOrderVo.getOrderNo())
                        .eq(ToolUtil.isNotEmpty(mgbConsignmentOrderVo.getGoodsName()),MgbConsignmentOrderDto::getGoodsName, mgbConsignmentOrderVo.getGoodsName())
                        .eq(ToolUtil.isNotEmpty(mgbConsignmentOrderVo.getConsignee()),MgbConsignmentOrderDto::getConsignee, mgbConsignmentOrderVo.getConsignee())
                        .eq(ToolUtil.isNotEmpty(mgbConsignmentOrderVo.getConsigneeMobile1()),MgbConsignmentOrderDto::getConsigneeMobile1, mgbConsignmentOrderVo.getConsigneeMobile1())
                        .eq(ToolUtil.isNotEmpty(mgbConsignmentOrderVo.getOrderStatus()),MgbConsignmentOrderDto::getOrderStatus, mgbConsignmentOrderVo.getOrderStatus())
                        .eq(ToolUtil.isNotEmpty(mgbConsignmentOrderVo.getDeliverGoodsStatus()),MgbConsignmentOrderDto::getDeliverGoodsStatus, mgbConsignmentOrderVo.getDeliverGoodsStatus())
                        .eq(ToolUtil.isNotEmpty(mgbConsignmentOrderVo.getSafterSaleStatus()),MgbConsignmentOrderDto::getSafterSaleStatus, mgbConsignmentOrderVo.getSafterSaleStatus())
                        .eq(ToolUtil.isNotEmpty(mgbConsignmentOrderVo.getSafterSaleNo()),MgbConsignmentOrderDto::getSafterSaleNo, mgbConsignmentOrderVo.getSafterSaleNo())

                        .between(ToolUtil.isNotEmpty(mgbConsignmentOrderVo.getDeliveryTimeBegin()),MgbConsignmentOrderDto::getDeliveryTime, mgbConsignmentOrderVo.getDeliveryTimeBegin(),mgbConsignmentOrderVo.getDeliveryTimeEnd())
                        .between(ToolUtil.isNotEmpty(mgbConsignmentOrderVo.getOrderPushTimeBegin()),MgbConsignmentOrderDto::getOrderPushTime, mgbConsignmentOrderVo.getOrderPushTimeBegin(),mgbConsignmentOrderVo.getOrderPushTimeEnd())

                        .orderByAsc(MgbConsignmentOrderDto::getId));
~~~
