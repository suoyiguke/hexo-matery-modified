---
title: 什么时候使用-java-util-Optional？.md
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
- map.get()
- list.get()
- xxx.get()


非常厉害的用法：
把Map的元素value转Boolean，转File
~~~
    public static void configure(Map<String, String> options) {
        Boolean useCache = Optional.ofNullable(options.get("cache")).map(Boolean::parseBoolean).orElse(true);
        File fileRoot = Optional.ofNullable(options.get("fileRoot")).map(File::new).orElse(null);
    }
~~~

~~~
private Double calculateAverageGrade(Map<String, List<Integer>> gradesList, String studentName)
      throws Exception {
    return Optional.ofNullable(gradesList.get(studentName))
        .map(list -> list.stream().collect(Collectors.averagingDouble(x -> x)))
        .orElseThrow(() -> new Exception("Student not found - " + studentName));
  }
~~~


~~~

            @Override
            public OptionalDouble getValueFromAggregationQueryResult(Object value)
            {
                return Optional.ofNullable(value)
                        .map(Number.class::cast)
                        .map(Number::doubleValue)
                        .map(OptionalDouble::of)
                        .orElseGet(OptionalDouble::empty);
            }

~~~


自己的用法：
改写前：
~~~
       String areaDetail = jgOriginalOrder.getAreaDetail();
        if (ToolUtil.isNotEmpty(areaDetail)) {
            List<Map<String, String>> mList = AddressResolutionUtil.addressResolution(areaDetail);
            if (ToolUtil.isNotEmpty(mList)) {
                Map<String, String> stringStringMap = mList.get(0);
                if (ToolUtil.isNotEmpty(stringStringMap)) {
                    jgOriginalOrder.setProvince(stringStringMap.get(ImportOrderByExcelListener.PROVINCE));
                    jgOriginalOrder.setCity(stringStringMap.get(ImportOrderByExcelListener.CITY));
                    jgOriginalOrder.setArea(stringStringMap.get(ImportOrderByExcelListener.COUNTY));
                }

            }
        }
~~~
改写后
~~~
        Optional.ofNullable(jgOriginalOrder.getAreaDetail()).filter(ToolUtil::isNotEmpty)
                .map(AddressResolutionUtil::addressResolution).filter(ToolUtil::isNotEmpty)
                .map(list -> list.get(0)).ifPresent(map -> {
                    jgOriginalOrder.setProvince(map.get(ImportOrderByExcelListener.PROVINCE));
                    jgOriginalOrder.setCity(map.get(ImportOrderByExcelListener.CITY));
                    jgOriginalOrder.setArea(map.get(ImportOrderByExcelListener.COUNTY));
                });
~~~
