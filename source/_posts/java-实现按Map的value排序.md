---
title: java-实现按Map的value排序.md
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
> 自弃者天弃之

如果要实现按value排序，不能采用SortedMap结构比如TreeMap，因为SortedMap是按key排序的Map，而不是按value排序

可以使用ArrayList做排序过渡，然后构建一个LinkedHashMap
~~~
package com.springboot.study.demo1;

import java.util.*;

public class Test {
    public static void main(String[] args) {

        Map<String, String> map = new HashMap<String, String>() {{
            put("3", "1");
            put("1", "2");
            put("2", "3");

        }};


        Map sorted1 = sortByValue(map, true);
        Map sorted2 = sortByValue(map, false);
        System.out.println(sorted1);
        System.out.println(sorted2);


    }

    /**
     * 实现map的value排序
     *
     * @param map
     * @param reverse
     * @return
     */

    public static Map sortByValue(Map map, final boolean reverse) {
        //将Map转为 List<Map.Entry>
        List list = new ArrayList(map.entrySet());
        //在 List<Map.Entry> 内部按元素getValue大小排序
        Collections.sort(list, new Comparator() {

            public int compare(Object o1, Object o2) {
                if (reverse) {
                    return -((Comparable) ((Map.Entry) (o1)).getValue())
                            .compareTo(((Map.Entry) (o2)).getValue());
                }
                return ((Comparable) ((Map.Entry) (o1)).getValue())
                        .compareTo(((Map.Entry) (o2)).getValue());
            }
        });

        //将有序的List转为 LinkedHashMap，使用LinkedHashMap做插入顺序排序
        Map result = new LinkedHashMap(map.size());
        for (Iterator it = list.iterator(); it.hasNext(); ) {
            Map.Entry entry = (Map.Entry) it.next();
            result.put(entry.getKey(), entry.getValue());
        }

        list = null;
        return result;
    }


}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-aeac6b12e3b914a8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


