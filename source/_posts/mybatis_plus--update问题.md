---
title: mybatis_plus--update问题.md
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
title: mybatis_plus--update问题.md
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
mybatis_plus 如何做到
批量更新 set 和in 同时都是批量的？
现在只能是in 是批量


updateBatchById 直接更新list可以做到。但是会去更新所有值而不是我只想更新的值

1、批量更新不同的属性值时还是得写循环单条更新

不要这样写！
~~~
   /**
                         * 这种写法跟危险，只要模型类字段上加了注解。那么null会被复制
                         * 而且这种update操作在数据库层面上本来就不能批量更新
                         */
                        saveQuestionsAndAnswersList.forEach(m -> m.setProblemIndex(problemIndexInt[0]++)
                                .setKnowledgeId(null).setAnswer(null).setSku(null).setSpu(null).setUserType(null).setProblemContent(null));
                        qestionsAndAnswersService.updateBatchById(saveQuestionsAndAnswersList);
~~~

2、还是一条一条的为好，不要觉得这样性能不好。其实批量update不同的值本身也是一条一条的执行。并不是真正的批量
~~~
          if (ToolUtil.isNotEmpty(dataList)) {
                dataList.stream().forEach(order ->
                        warehouseOrderService.lambdaUpdate()
                                .set(JgWarehouseOrder::getUnapprovedReason, order.getUnapprovedReason())
                                .eq(JgWarehouseOrder::getPlatformOrderNo, order.getPlatformOrderNo()));
            }
~~~
