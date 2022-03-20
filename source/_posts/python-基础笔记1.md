---
title: python-基础笔记1.md
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
title: python-基础笔记1.md
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
######打印对象的所有属性,类似于java的tostring
使用对象的`__dict__`属性

或者使用这个
~~~
list = []
print(dir(list))
~~~


######判断对象是否有对应属性，非常重要！开发工具和编译器不会告诉我们具体的变量类型。导致调用不存在的属性程序报错
~~~
list = []
if hasattr(list, 'remove'):
    print("ok")
else:
    print("no")
~~~

######判断list里边的dict是否包含具体元素 
注意这个方法和hasattr区分开！这个是dict字典专用的，上面的是对象使用的
~~~
obj1 = {'name':'yinkai','sex':'man'}
obj2 = {'sex':'man'}
list = []
list.append(obj1)
list.append(obj2)

for item in list:
    if 'name' in item:
        print(item['name']) #yinkai
~~~

######查看某个函数的用法
~~~
help(range(0, 1))
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-75b5f77047f38367.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######py定义一个类，使用面向对象的思想来构造对象
定义构造函数`__init__()`



 需要显示的给属性赋值，非常不方便。于是我们可以使用构造函数 __init__()
~~~
class Video(Base):
    __tablename__ = 'video'
    video_id = Column(Integer, primary_key=True)
    video_title = Column(String)
    video_pic = Column(String)
    video_url = Column(String)
    video_date = Column(String)
    category_id = Column(Integer)

    #構造函數
    def __init__(self, video_id, video_title,video_pic,video_url,video_date,category_id):
        self.video_id = video_id
        self.video_title = video_title
        self.video_pic = video_pic
        self.video_url = video_url
        self.video_date = video_date
        self.category_id = category_id
        print(self.__dict__)

    # 構造函數
    def __init__(self,video_item):
        self.video_id = video_item['video_id']
        self.video_title = video_item['video_title']
        self.video_pic = video_item['video_pic']
        self.video_url = video_item['video_url']
        self.video_date = video_item['video_date']
        self.category_id = video_item['category_id']
        print(self.__dict__)

    # 定义类方法必须要加上self形参
    def tostring(self):
        print(self.__dict__)
~~~

定义了构造函数的话，可以这样使用， 构造一个对象可以这样：
~~~
 VideoA= Video( video_id=14,video_title='ff', video_pic='18012345678', video_url='2000.00', video_date='2019-03-07 18:04:29', category_id=2)
~~~

######对象唯一id
~~~
list = []
print(id(list))
~~~

######判断变量的数据类型


isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。

isinstance() 与 type() 区别：
- type() 不会认为子类是一种父类类型，不考虑继承关系。
- isinstance() 会认为子类是一种父类类型，考虑继承关系。
- 如果要判断两个类型是否相同推荐使用 isinstance()。



对于基本类型来说 classinfo 可以是：
int，float，bool，complex，str(字符串)，list，dict(字典)，set，tuple
要注意的是，classinfo 的字符串是 str 而不是 string，字典也是简写 dict。

使用isinstance
~~~
arg=123
isinstance(arg, int)    #输出True
isinstance(arg, str)    #输出False
isinstance(arg, string) #报错
~~~
使用type
~~~
list = []
print(type(list))
~~~



######url字符串转dict对象
~~~
from urllib import parse
cookie_str = "pgv_pvi=8857950208; pgv_si=s284531712; _qpsvr_localtk=0.18972080698488325; ptisp=ctc; ptui_loginuin=489277624; uin=o0489277624; skey=@XqhUWo6W1; RK=yaB9HxZpeO; ptcz=f9d80edce989e1467cf35b596a7901c19b0edf315be94f768f9e8fb144a644a0; p_uin=o0489277624; pt4_token=9rP1mk4KGMZkcO5L-ve8Kwp5ov-HRtzu4YoQvZ39m60_; p_skey=MnhPb94fnLu0IECSUIuYydZVEYR0F5GwcHgMq91CYuw_; pgg_pvid=8132141056; pgg_ssid=1200547840"
cookie_dict = dict(parse.parse_qsl(cookie_str))
for item in cookie_dict:
    print(item+'==>'+cookie_dict[item])
~~~

######多返回值
~~~
#查询视频
def selectVideo():
    arrList = []
    # 执行SQL
    cur = _instance.execute(
        "SELECT video_id,video_url FROM `video` WHERE `state` = 1 "
    )
    list  = cur.fetchall()
    for item in list:
        object = {}
        object['id'] = item.values()[0]
        object['url'] = item.values()[1]
        arrList.append(object)

    return arrList,len(list)
~~~

######生成随机数
1、闭区间，生成1到20之间包过节点的随机数
~~~
import random
print(random.randint(1,20))
~~~

2、从字符串中随机选取一个字符元素
~~~
import random
print( random.choice('tomorrow'))
~~~
3、从list中随机区一个元素
~~~
import random
list = [1,2,3,4]
print(random.choice(list))
~~~

######py读取系统环境变量
~~~
import os
environ = os.environ
print(environ['JAVA_HOME'])
~~~
######判断环境变量是否定义
~~~
import os

if "JAVA_HOME" in os.environ:
    print('ok')
else:
    print('no')
~~~

环境变量最好以下划线连接，不要用点. 点最后也会转为下划线_

######导入数字文件名的py文件
比如这里是 56.py 文件
~~~
wl=importlib.import_module("56")
from apscheduler.schedulers.blocking import BlockingScheduler
~~~

######指定递归深度
默认超过递归深度报错： 
scan_1  | RecursionError: maximum recursion depth exceeded while calling a Python object
~~~
sys.setrecursionlimit(1000000)
~~~

###几种数据直接作为if条件

~~~
   if '':
        print(True) False
    else:
        print(False)

    if None:
        print(True) False
    else:
        print(False)

    if ' FF':
        print(True)  True
    else:
        print(False)

    if []:
        print(True) False
    else:
        print(False)

    if {}:
        print(True) False
    else:
        print(False)
~~~

###数组按下标判断是否存在
这种方式如果不存在就会报list range异常
    list =[1,2,4]
    if list[2]:
        print(list[2])

这样做
~~~
def vali(list, i):
    if list:
        if i or i == 0:
            size = len(list)
            if size == 0:
                return False
            elif size - 1 >= i:
                return True

    return False


if __name__ == '__main__':
    list =[1,2,4]
    if vali(list,5):
        print(list[5])

~~~
