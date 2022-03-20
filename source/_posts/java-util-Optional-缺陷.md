---
title: java-util-Optional-缺陷.md
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
在这种时候使用新写法就有些鸡肋了。不要为了使用而使用。反而原来的写法可读性更好

~~~
        Set<String> keySet = map.keySet();
        for (String s : keySet) {
            String[] split1 = s.split(Constant.COLON);
            String value = split1[Constant.NUMBER_ONE];
            String[] split = value.split(Constant.COMMA);
            if (ArrayUtils.contains(split, key)) {
                return s;
            }
        }
~~~


改写

~~~
        String[] re = new String[1];
        boolean b = map.keySet().stream().map(s -> {
                    re[0] = s;
                    return s.split(Constant.COLON);
                }).flatMap(Arrays::stream).skip(1).limit(1).map(s -> s.split(Constant.COMMA))
                .anyMatch(split -> ObjectUtil.contains(split, key));
        if (b) {
            return re[0];
        }
~~~

在执行 s.split(Constant.COMMA)时我想拿到前面执行后的数据只能使用 re[0]来记录
