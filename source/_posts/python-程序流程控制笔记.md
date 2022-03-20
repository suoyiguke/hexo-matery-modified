---
title: python-程序流程控制笔记.md
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
title: python-程序流程控制笔记.md
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
######python 的if else的写法

~~~
if category_id.find('英雄联盟') != -1:
    category_id = 1
elif category_id.find('王者荣耀') != -1:
    category_id = 2
~~~

######可以做if条件的
因为python把True、False、None、空字符串、空list、0 看成false
~~~
if True:
    print("ok")

if not False:
    print("ok")

if not None:
    print("ok")

if not '':
    print("ok")

if not ():
    print("ok")

if not []:
    print("ok")

if not {}:
    print("ok")

if not 0:
    print("0 ok")
~~~
######跳出多层循环
使用 for...else...语句 + break+ continue 的方式
1、跳出二层循环
~~~
for j in range(5):
    for k in range(5):
        if j == k == 3:
            print('程序即将break跳出一层')
            break
        else:
            print(j, '----', k)
    else:  # else1
        continue
    print('程序即将break跳出二层')
    break  # break1
~~~

2、跳出三层循环
~~~
for i in range(5):
    for j in range(5):
        for k in range(5):
            if i == j == k == 3:
                break
            else:
                print (i, '----', j, '----', k)
        else:        # else1
            continue
        break        # break1
    else:            # else2
        continue
    break
~~~

######逻辑运算
~~~
True and True   # ==> True
True and False   # ==> False
False and True   # ==> False
False and False   # ==> False
True or True   # ==> True
True or False   # ==> True
False or True   # ==> True
False or False   # ==> False
not True   # ==> False
not False   # ==> True
~~~

######py的异常捕获机制
1、捕获异常和打印异常
~~~

try:
    browser = webdriver.Chrome()
except BaseException as err:
    log.error(err)
    browser = webdriver.Remote(
        command_executor="http://172.28.0.2:4444/wd/hub",
        desired_capabilities=DesiredCapabilities.CHROME
    )
finally:
    log.error('请检查好Chrome环境！')
~~~

2、将异常输出到日志文件
~~~
import traceback
import logging

logging.basicConfig(filename='log.log')


def error_func():
    b = 1 / 0


if __name__ == '__main__':
    try:
       error_func()
    except:
        s = traceback.format_exc()
        logging.error(s)
~~~

###三目运算
x，y中取大值赋值给zz
zz=  x if(x>y) else y
