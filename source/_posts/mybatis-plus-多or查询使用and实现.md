---
title: mybatis-plus-多or查询使用and实现.md
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
title: mybatis-plus-多or查询使用and实现.md
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
使用函数方法消费者Consumer

~~~
        Map<String, Object> reMap = iMgbConsignmentOrderDtoService.getMap(new QueryWrapper<MbUndertakesOrderDto>().select("1").eq("platform_order_no", data.getPlatformOrderNo()).eq(ToolUtil.isNotEmpty(data.getK3Code()),"k3_Code", data.getK3Code()).and(ToolUtil.isEmpty(data.getK3Code()), new Consumer<QueryWrapper<MbUndertakesOrderDto>>() {
            @Override
            public void accept(QueryWrapper<MbUndertakesOrderDto> mbUndertakesOrderDtoQueryWrapper) {
                mbUndertakesOrderDtoQueryWrapper.isNull("k3_code").or().eq("k3_code",StringUtils.EMPTY);
            }
        }).last("limit 1"));
~~~

改写lambada
~~~
   Map<String, Object> reMap = iMgbConsignmentOrderDtoService.getMap(new QueryWrapper<MbUndertakesOrderDto>().select("1").eq("platform_order_no", data.getPlatformOrderNo()).eq(ToolUtil.isNotEmpty(data.getK3Code()),"k3_Code", data.getK3Code()).and(ToolUtil.isEmpty(data.getK3Code()), mbUndertakesOrderDtoQueryWrapper -> 
                mbUndertakesOrderDtoQueryWrapper.isNull("k3_code").or().eq("k3_code",StringUtils.EMPTY)).last("limit 1"));
~~~

生成如下
> SELECT 1
 FROM mgb_undertakes_order
 WHERE (platform_order_no = '371****586959' AND (k3_code IS NULL OR k3_code = ''));
