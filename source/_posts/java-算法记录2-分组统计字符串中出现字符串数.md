---
title: java-算法记录2-分组统计字符串中出现字符串数.md
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
直接使用HashMap解决
~~~
package GGG.COM.class1;

import java.util.HashMap;

public class GGGA {

    public static void main(String[] args) {

        String str = "yinkaiyinkai";
        char[] chars = str.toCharArray();

        HashMap<Object, Integer> objectObjectHashMap = new HashMap<>();


        for (int i = 0; i < chars.length; i++) {
            char c = chars[i];
            Integer o = objectObjectHashMap.get(c);
            if(o==null){
                objectObjectHashMap.put(c,1);
            }else{
                objectObjectHashMap.put(c,o+1);
            }
        }
        System.out.println(objectObjectHashMap);

    }

}

~~~


java8写法

~~~
package GGG.COM.class1;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class GGGA {

    public static void main(String[] args) {

        String str = "yinkaiyinkai";
        Character[] charObjectArray =
            str.chars().mapToObj(c -> (char)c).toArray(Character[]::new);



        Map<Character, Long> collect = Stream.of(charObjectArray)

            .collect(
                Collectors.groupingBy(
                    Function.identity(), Collectors.counting()
                )
            );

        System.out.println(collect);
    }

}

~~~
