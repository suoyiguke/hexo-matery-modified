---
title: ###hutool---Convert.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: ###hutool---Convert.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
可以将任意基本类型数组转为其它类型

~~~
        //Convert
        int a = 1;
         //aStr为"1"
        String aStr = Convert.toStr(a);

        long[] b = {1,2,3,4,5};
        //bStr为："[1, 2, 3, 4, 5]"
        String bStr = Convert.toStr(b);
        String[] c = { "1", "2", "3", "4" };
        //结果为Integer数组
        Integer[] intArray = Convert.toIntArray(c);

        long[] d = {1,2,3,4,5};
         //结果为Integer数组
        Integer[] intArray2 = Convert.toIntArray(d);
        String e = "2017-05-06";
        Date value = Convert.toDate(e);
        Object[] f = {"a", "你", "好", "", 1};
        List<?> list1 = Convert.convert(List.class, f);
        //从4.1.11开始可以这么用
        List<?> list2 = Convert.toList(a);


~~~
