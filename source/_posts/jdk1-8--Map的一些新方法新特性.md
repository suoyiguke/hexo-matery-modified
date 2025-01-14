---
title: jdk1-8--Map的一些新方法新特性.md
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
前面提到过，Map 类型不支持 streams，不过Map提供了一些新的有用的方法来处理一些日常任务。Map接口本身没有可用的 stream（）方法，但是你可以在键，值上创建专门的流或者通过 map.keySet().stream(),map.values().stream()和map.entrySet().stream()。

此外,Maps 支持各种新的和有用的方法来执行常见任务。

putIfAbsent 返回最新value，原value为空则覆盖新值
~~~
Map<Integer, String> map = new HashMap<>();
for (int i = 0; i < 10; i++) {
    map.putIfAbsent(i, "val" + i);
}
~~~
forEach接受一个 consumer 来对 map 中的每个元素操作。
~~~
map.forEach((id, val) -> System.out.println(val));//val0 val1 val2 val3 val4 val5 val6 val7 val8 val9
~~~


此示例显示如何使用函数在 map 上计算代码：
~~~
map.computeIfPresent(3, (num, val) -> val + num);
map.get(3);             // val33

map.computeIfPresent(9, (num, val) -> null);
map.containsKey(9);     // false

map.computeIfAbsent(23, num -> "val" + num);
map.containsKey(23);    // true

map.computeIfAbsent(3, num -> "bam");
map.get(3);             // val33
~~~
接下来展示如何在Map里删除一个键值全都匹配的项：
~~~
map.remove(3, "val3");
map.get(3);             // val33
map.remove(3, "val33");
map.get(3);             // null
~~~

指定Default的value：
~~~
map.getOrDefault(42, "not found");  // not found
~~~


对Map的元素做合并也变得很容易了：
~~~
map.merge(9, "val9", (value, newValue) -> value.concat(newValue));
map.get(9);             // val9
map.merge(9, "concat", (value, newValue) -> value.concat(newValue));
map.get(9);             // val9concat
~~~
Merge 做的事情是如果键名不存在则插入，否则对原键对应的值做合并操作并重新插入到map中。Merge 和put 覆盖是不同的。
