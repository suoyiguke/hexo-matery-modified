---
title: python-容器-列表-list笔记.md
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
title: python-容器-列表-list笔记.md
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
######获得list长度
~~~
list = [1,2,3,4,3,4,5,6,7,8,89,555,6,7,99,45,6,656,88]
print(len(list))
~~~

######快速生成一个list
~~~
a=list(range(0,30))
print(a)
~~~
区间左开右闭；生成包含0到29的list

######list去重
1、for循环实现
~~~
def main(list):
  
    arrayList = []
    for item in list:
        if item not in arrayList:
               arrayList.append(item)

return arrayList
~~~

2、列表的元素是不可变对象的话可以使用set
有时候合并完列表，我们需要对新列表的元素进行去重，此时可以使用set()。
~~~
list = list(set(list))
~~~

3、list元素为dict，去除重复数据的方法
指定dict key值，去重
~~~
def _remove_duplicate( dict_list):
    seen = set()
    new_dict_list = []
    for dict in dict_list:
        t_dict = {'cur': dict['cur']}
        t_tup = tuple(t_dict.items())
        if t_tup not in seen:
            seen.add(t_tup)
            new_dict_list.append(dict)
    return new_dict_list


zz = [{'refer':'12311111','cur':'1234'},{'refer':'123','cur':'1234'}]
duplicate = _remove_duplicate(zz)
print(duplicate)
~~~

######拼接list
列表自带的extend()也是就地执行，`即它会修改原来的列表，直接在原来的列表后面拼接新列表`。
~~~
list1 = [1, 2, 3, 4]
list2 = [5,6]
list1.extend(list2)
# [1, 2, 3, 4, 5, 6]
print(list1)
~~~

######按数量等分list
~~~
def div_list(ls,n):
   result = []
   cut = int(len(ls)/n)
   if cut == 0:
       ls = [[x] for x in ls]
       none_array = [[] for i in range(0, n-len(ls))]
       return ls+none_array
   for i in range(0, n-1):
       result.append(ls[cut*i:cut*(1+i)])
   result.append(ls[cut*(n-1):len(ls)])
   return result

list = div_list([1,2,3,4,3,4,5,6,7,8,89,555,6,7,99,45,6,656,88],3)
print(list)
~~~


######`重要`list元素的remove操作
~~~
a=list(range(0,10))
for i in a :
    if i%4!=0:
        a.remove(i)
print(a)
~~~
上面的代码意思是干掉不能被4整除的元素，显然这个执行结果：[0, 2, 4, 6, 8]是不正确的


想要对list的元素进行remove操作，推荐先使用深copy；得到list的copy对象，然后遍历原list，对copy对象进行remove
`深copy  b = copy.deepcopy(a);`
~~~
import copy
a=list(range(0,10))
b = copy.deepcopy(a);
for i in a :
    if i%4!=0:
        b.remove(i)
print(b)
~~~
[0, 4, 8]
