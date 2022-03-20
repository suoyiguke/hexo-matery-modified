---
title: java-集合容器常用操作.md
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

1、快速构建集合容器
- List
~~~
List<Integer> sList = Arrays.asList(1, 2, 3);
~~~
`这样构建出来的不是真正的List，不可以add；`
或者可以这样
~~~
ArrayList<String> arrayList = new ArrayList();
Collections.addAll(arrayList, "1", "2", "3", "4", "5");
~~~
- Map
~~~
Map<Integer, Integer> newsEventMap = new HashMap() {{
    for (int i = 0; i < 100; i++) {
        put(i, i);
    }

}};
~~~

2、集合容器的非空判断
`需要判断集合是否为null和集合内容的size是否为0`

- List验证不为空：
~~~
List list = null;
if(null != list && list.size() > 0 ){
    System.out.println("list is not empty");
}else{
    System.out.println("list is empty");
}
~~~
或者使用工具类
~~~
List list = new ArrayList();
if (org.apache.commons.collections.CollectionUtils.isNotEmpty(list)) {
    System.out.println("list is not empty");
} else {
    System.out.println("list is empty");
}
~~~
- Map验证不为空：
~~~
Map hashMap = null;
if( null != hashMap && hashMap.size() > 0 ){
    System.out.println("map is not empty");
}else{
    System.out.println("map is empty");
}
~~~
或者使用工具类
~~~
if(org.apache.commons.collections.MapUtils.isNotEmpty(new HashMap())){
    System.out.println("list is not empty");
}else{
    System.out.println("list is empty");
}
~~~

3、List转数组
- 错误的写法，会报错
~~~
String[] arr = (String[]) arrayList.toArray();
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-851633f890b46fff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 正确的写法
~~~
String[] arr = arrayList.toArray(new String[arrayList.size()]);
~~~

4、数组转List
~~~
Integer[] arr = {1,2,3,4,5};
ArrayList arrayList = new ArrayList(Arrays.asList(arr));
~~~

5、List截取
- 按下标截取subList
~~~
ArrayList<String> arrayList = new ArrayList();
Collections.addAll(arrayList, "1", "2", "3", "4", "5");
List<String> subList = arrayList.subList(0, 3);
//其中subList(0, 3)取得的是下标为0到3的元素
System.out.println(subList);//[1, 2, 3]
~~~

6、容器元素排序
- Array
~~~
Integer[] arr = {23,44,1,2,3,43,54,};
Arrays.sort(arr, new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return o1-o2;
    }
});
System.out.println(Arrays.asList(arr));
~~~
- List

正序
~~~
List<Integer> intList = Arrays.asList(2, 3, 1);
Collections.sort(intList);
System.out.println(intList);
~~~
倒序
~~~
List<Integer> intList = Arrays.asList(2, 3, 1);
Collections.sort(intList, new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        // 返回值为int类型，大于0表示正序，小于0表示逆序
        return o2 - o1;
    }
});
System.out.println(intList);
~~~

7、List<Object> 转 List<String>
	List<String> strs = (List<String>)(List)objects;
