---
title: python-tkinter-pc跨平台UI.md
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
title: python-tkinter-pc跨平台UI.md
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
1、对话框
~~~
from tkinter.simpledialog import *
root = Tk()
#仅显示对话框，隐藏主窗口
root.withdraw()
i = askinteger('请输入', prompt='输入一个整数：', initialvalue=100, maxvalue=1000, minvalue=1)

print(i)
#
#root.destroy() #关闭GUI窗口，释放资源
~~~



2、如何隐藏左边的窗口
![image.png](https://upload-images.jianshu.io/upload_images/13965490-681d3c77871118a2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

~~~
import tkinter as tk
import tkinter.messagebox
tip = tk.Tk()
tip.withdraw()
tkinter.messagebox.showinfo('提示', '请手动输入验证码，输入完点确定！注意不要自己点登录！')
tip.destroy()
~~~

3、输入对话框
~~~
import tkinter as tk
from tkinter.simpledialog import *

root = tk.Tk()
root.geometry('300x100+600+400')


def enput_passwd():
    passwd = askstring(title="密码输入框", prompt="请输入密码", initialvalue="123456")
    passwd_label['text'] = "You passwd is: " + passwd


tk.Button(root, text="密码", command=enput_passwd).pack()

passwd_label = tk.Label(root)
passwd_label.pack()

root.mainloop()
~~~
