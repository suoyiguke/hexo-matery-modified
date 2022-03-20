---
title: java-util-stream-Collectors#minBy-返回的Optional本身可能会空指针.md
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
所以拿出这个 Optional对象也记得要判空！

   public static <T> Collector<T, ?, Optional<T>>
    minBy(Comparator<? super T> comparator) {
        return reducing(BinaryOperator.minBy(comparator));
    }

     //分组计算最小id
                        Map<Long, Optional<ZskAccessoriesListDo>> zskQuestionsAndAnswersDoMap = saveZskAccessoriesListDoList.stream()
                                .filter(m -> ToolUtil.isNotEmpty(m.getId())).collect(Collectors.groupingBy(ZskAccessoriesListDo::getKnowledgeId,
                                        Collectors.minBy(Comparator.comparingInt(o -> ObjectUtil.defaultIfNull(o.getId(), 0).intValue()))));
