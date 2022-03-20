---
title: java-lang-System-arraycopy()方法使用说明.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 观源码心得
categories: 观源码心得
---
---
title: java-lang-System-arraycopy()方法使用说明.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 观源码心得
categories: 观源码心得
---

java.lang.System为标准的输入输出，加载文件和类库，访问外部定于属性提供了一些十分有用的方法。 java.lang.System.arraycopy()方法是从一个源数组的指定开始位置拷贝元素到目标数组提到的位置。被拷贝的参数的数目由参数len决定。

从source_Position到source_Position + length – 1的元素拷贝到目标数组的destination_Position到destination_Position + length – 1的位置处。

语法说明：
public static void arraycopy(Object source_arr, int sourcePos, Object dest_arr, int destPos, int len)
参数: 
source_arr : 源数组
    sourcePos : 源数组拷贝元素的起始位置
dest_arr : 目标数组
destPos : 目标数组接收拷贝元素的起始位置
len : 拷贝的元素的数目


使用
~~~
        System.arraycopy(array, 0, arrayNew, 0, array.length);
~~~
