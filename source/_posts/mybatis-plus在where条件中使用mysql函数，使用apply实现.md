---
title: mybatis-plus在where条件中使用mysql函数，使用apply实现.md
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
title: mybatis-plus在where条件中使用mysql函数，使用apply实现.md
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
使用 apply
~~~
        /**
         * 预警状态过滤
         */
        WarningState warningState = mbUndertakesOrderVo.getWarningState();
        if (WarningState.NO_DELIVERY_WITHIN_24_HOURS.equals(warningState)) {
            //24小时未发货
            whereWrapper.apply("  push_time <= date_add(now(), interval -24 HOUR) ");

        } else if (WarningState.NO_DELIVERY_WITHIN_48_HOURS.equals(warningState)) {
            //48小时未发货
            whereWrapper.apply("  push_time <= date_add(now(), interval -48 HOUR) ");

        } else if (WarningState.LOGISTICS_NOT_UPDATED_AFTER_10_DAYS.equals(warningState)) {
            //10天后未更新物流
            whereWrapper.in(MbUndertakesOrderDto::getOrderState,OrderState.TO_BE_SHIPPED,OrderState.IN_SHIPMENT_PROCESSING,OrderState.SHIPPED,OrderState.CANCELLED_ORDERS);
            whereWrapper.apply(" push_time <= date_add(now(), interval -10 day) ");
        }
~~~
