---
title: python-变量作用域笔记.md
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
title: python-变量作用域笔记.md
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
######python中奇怪的变量作用域
- ①处定义的变量在def定义的函数中不可见；main块执行打印str变量是①
- def函数中定义的str变量只在该函数范围内有效
~~~
str = 'yinkai' # ①
print(str) # yinkai

def function1():
    str = 'ggg'  # ②
    print(str) # ggg

if __name__ == '__main__':
    function1()
    print(str) #yinkai
~~~

再来看这个代码，只是在上面代码的基础上加了一个 print(str) #③ 
运行报错 UnboundLocalError: local variable 'str' referenced before assignment；可以得出结论
- 如果def函数内有与函数外定义的变量重名的变量str，py执行器会先去找def内有没有定义，没有定义则报以上错误；有定义则访问的是def内申明的str变量
~~~
str = 'yinkai'
print(str)

def function1():
    print(str) #③
    str = 'ggg'
    print(str)

if __name__ == '__main__':
    function1()
    print(str)
~~~


######那应该如何在def函数外面定义一个变量，让它在当前py文件中所有def函数里面有效？
`使用global关键字`
- 在def函数内使用global 先申明一个变量，表示这个表量是全局的；那么该变量就指向def外申明的str变量了
- 在def函数内部对str全局变量修改对所有地方都可见
~~~
str = 'yinkai'
print(str) # yinkai

def function1():
    global str
    print(str) #③ # yinkai
    str = 'ggg'
    print(str) # ggg

if __name__ == '__main__':
    function1()
    print(str) # ggg
~~~

######global关键字与main块
main块与def函数不同，这样做会报错 SyntaxError: name 'str' is assigned to before global declaration

~~~
str = 'yinkai'

if __name__ == '__main__':
    global str
    str = 'ggg'
    print(str)
~~~

 `main块里可以直接访问全局变量str，不需要使用global关键字`
~~~
str = 'yinkai'

if __name__ == '__main__':
    str = 'ggg'
    print(str)
~~~

######global关键字与list列表
 `list对象，不需要使用global关键字`，直接可以在def函数内读取、添加元素和迭代
~~~
list = ['yinkai','yinxuan']

def zz():
    print(list)
    list.append('haha')
    for item in list:
        print(item)

if __name__ == '__main__':
    zz()
~~~

但是不能改变list变量的引用。④行代码处，将[]赋值给了list。这里的引用修改对def外的list变量不可见
~~~
list = ['yinkai','yinxuan']

def zz():
    list = [] # ④
    print(list) # []

if __name__ == '__main__':
    print(list) # ['yinkai','yinxuan']
    zz()
    print(list) # ['yinkai', 'yinxuan']

~~~

`如果还是要修改引用，请使用global关键字！`
~~~
list = ['yinkai','yinxuan']

def zz():
    global list
    list = []  
    print(list)  # []

if __name__ == '__main__':
    print(list) # ['yinkai','yinxuan']
    zz()
    print(list) # []
~~~
