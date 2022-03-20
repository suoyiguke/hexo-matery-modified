---
title: python-容器-字典-dict.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
---
title: python-容器-字典-dict.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
# [python之字典（dict)基础篇](https://www.cnblogs.com/shuaiyuan/p/14986518.html)

**字典：dict**

**特点：**

1>,可变容器模型，且可存储任意类型对象,字符串，列表，元组，集合均可；

2>，以key-value形式存在，每个键值 用冒号 : 分割，每个键值对之间用逗号 , 分割；

3>，通过key访问value；key与value是对应的，一个字典中每个key是唯一的，但value则没有现在；

4>，有序的，但在python3.6版本之前，字典是无序的。

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**1、定义空字典** 
name_dict = {}
name_dict = dict() # 一般用数据类型之间的转换 </pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**2、定义一个非空字典** 
name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"}

key--name,  value --dasb,   key:value-->"name":"dasb"; **3,****通过key访问value** </pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": ["love sb", "love mlt", "love mlasb"]}
print(name_dict["name"])
hobby_list = name_dict["hobby"]
print(hobby_list)
print(hobby_list[0])</pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**![image](https://upload-images.jianshu.io/upload_images/13965490-e27493924538b7a1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)** </pre>

** 4,增加一个元素**

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">说明：如果key不存在，则新增。如果key存在则修改 </pre>

[![复制代码](https://upload-images.jianshu.io/upload_images/13965490-282f788d66e465f7.gif?imageMogr2/auto-orient/strip)](javascript:void(0); "复制代码") 

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": ["love sb", "love mlt", "love mlasb"]}
# key不存在新增
name_dict["sex"] = "zx" print(name_dict)
# key存在则修改
name_dict["name"] = "csb" print(name_dict)</pre>

[![复制代码](https://upload-images.jianshu.io/upload_images/13965490-5cf53375d6e6c91c.gif?imageMogr2/auto-orient/strip)](javascript:void(0); "复制代码") 

![image](https://upload-images.jianshu.io/upload_images/13965490-065675216e951b13.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 5,字典中常用的方法之

**clear（）：**清空字典中所有元素

同样可使用此方法 类型的还有**列表（list），集合（set）**

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": ["love sb", "love mlt", "love mlasb"]}
name_dict.clear()
print(name_dict)</pre>

 6,字典中常用的方法之

**formkeys():  **初始化一个字典

说明：如果一个列表用foemkers转化为字典时，列表中的元素则转化为key键，如果转化时不加value，则key键对应的value为None，如果添加，value则为同一个添加的值，

例如：

[![复制代码](https://upload-images.jianshu.io/upload_images/13965490-684340a50d578e69.gif?imageMogr2/auto-orient/strip)](javascript:void(0); "复制代码") 

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = dict()
name_list = ["name", "age"]
name1_dict = dict.fromkeys(name_list)
print(name1_dict)
name2_dict = dict.fromkeys(name_list, 35)
print(name2_dict)</pre>

[![复制代码](https://upload-images.jianshu.io/upload_images/13965490-d35396fd5311e3a7.gif?imageMogr2/auto-orient/strip)](javascript:void(0); "复制代码") 

![image](https://upload-images.jianshu.io/upload_images/13965490-6cc49db6ef8e31f5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果列表中的元素是以元组tuple的方式存在的，则可以直接用dict转化；

例如：

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_list = [("name", "dasb"), ("age", 35), ("hobby", ["love sb", "love mlt"])]
name_dict = dict(name_list)
print(name_dict)</pre>

![image](https://upload-images.jianshu.io/upload_images/13965490-eb26f2f144a666ad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

  7,字典中常用的方法之

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**get(key**)：通过key 获取value值，如果key不存在则返回None</pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": ["love sb", "love mlt", "love mlasb"]}
name_value = name_dict.get("name")  # 存在的key
name_value = name_dict.get("sex")  # 不存在key，返回None
name_value = name_dict["sex"]  # 不存在key，则会报：KeyError: 'sex' print(name_value)</pre>

 8,字典中常用的方法之

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**items()：**把字典中每一对key 和value 以元组的形式保存在列表中
例如：</pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"}
print(name_dict.items())</pre>

利用for循环，获取key和value

第一种方法：

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"} for name in name_dict.items():
    key, value = name
    print(key, value)</pre>

第二种方法：

[![复制代码](https://upload-images.jianshu.io/upload_images/13965490-e31165299007e2ce.gif?imageMogr2/auto-orient/strip)](javascript:void(0); "复制代码") 

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"} for name in name_dict.items():

     key = name[0]
     value = name[1]

     print(key, value)</pre>

[![复制代码](https://upload-images.jianshu.io/upload_images/13965490-c90a748701bc4ab2.gif?imageMogr2/auto-orient/strip)](javascript:void(0); "复制代码") 

![image](https://upload-images.jianshu.io/upload_images/13965490-34630182b64fadb2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 9，字典中常用的方法之

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**keys()：**把字典中所有的key，保存在一个序列中</pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"}
print(name_dict.keys())</pre>

也可以利用循环，通过Key键获取value

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"}
print(name_dict.keys()) for key in name_dict.keys():
    value = name_dict.get(key)
    print(key,value)</pre>

10，字典中常用的方法之

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**pop(key)**：通过key删除字典中的元素</pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"}
name_dict.pop("name")
print(name_dict)</pre>

![image](https://upload-images.jianshu.io/upload_images/13965490-f6b7546ed0f73ac9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 11，字典中常用的方法之

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**popitem()：**默认删除字典中最后一个元素 </pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"}
name_dict.popitem()
print(name_dict)</pre>

12，字典中常用的方法之

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**setdefault()：**以元组的方式新增一个元素**，**key不存在则新增元素，key存在则不做任何修改</pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"}
name_dict.setdefault("sex", "中性")
name_dict.setdefault("name", "csb")
print(name_dict)</pre>

![image](https://upload-images.jianshu.io/upload_images/13965490-9c9e8fb9b3abc684.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 13，字典中常用的方法之

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**update()：**新增多个元素，如果key存在则更新，如果不存在则新增 </pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; overflow-wrap: break-word; font-family: &quot;Courier New&quot; !important; font-size: 12px !important; white-space: pre-wrap;">name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"}
teacher_dict = {"age": 23, "eat": "sb", "phone": "123456789"}
name_dict.update(teacher_dict)
print(name_dict)</pre>

![image](https://upload-images.jianshu.io/upload_images/13965490-ee4dc79938b61354.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 14，字典中常用的方法之

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">**values()：**把字典中所有value值保存在一个序列中，用法同keys 
例如： </pre>

<pre style="margin: 0px; padding: 0px; overflow: auto; white-space: pre-wrap;">
name_dict = {"name": "dasb", "age": 35, "hobby": "love sb"}
print(name_dict.values())</pre>
