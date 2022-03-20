---
title: selenium-等待.md
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
title: selenium-等待.md
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
~~~
from selenium import webdriver

import time

browser = webdriver.Chrome()
browser.get("http://oa.jztech.top:43500/SystemFrameWorkV3/Role/User.aspx")
input_str = browser.find_element_by_id('LoginUsername')
input_str.send_keys("username")
time.sleep(1)
input_str = browser.find_element_by_id('LoginPassword')
input_str.send_keys("password")
time.sleep(1)
button = browser.find_element_by_class_name('NewLoginButtonDIV')
button.click()
~~~




1、Python  time sleep()函数
推迟调用线程的运行，可通过参数secs指秒数，表示进程挂起的时间。
用法：
import time
time.sleep(10)
缺点：
固定等待时间，导致测试用例执行时间长

 

2、隐式等待
全局性设定
 每个半秒查询一次元素，直到超出最大时间
 后面所有选择元素的代码不需要单独指定周期定等待了
用法：
driver.implicitly_wait(10)



### 3、等待元素出现
1、By.CLASS_NAME 用classname，不能有空格
2、By.CSS_SELECTOR 直接使用css选择器允许有空格
3、By.ID
4、By.XPATH
5、
~~~

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
ele = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-pagination-total-text')))
~~~

click也可以这样用
~~~
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='ant-btn login-button ant-btn-primary ant-btn-lg ant-btn-two-chinese-chars']"))).click()
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-menu-submenu-title'))).click()
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="ant-menu-item menu-item"]'))).click()
~~~

















###WebDriverWait与expected_conditions结合使用
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

wait = WebDriverWait(driver,10,0.5)
element =wait.until(EC.presence_of_element_located((By.ID,"kw")),message="")
# 此处注意，如果省略message=“”，则By.ID外面是三层()
1
2
3
4
5
6
https://www.huaweicloud.com/articles/1062364abeceecae4cc1cd91a71f415f.html
最初执行的代码一开始是这样写：presence_of_element_located(By.ID,“su”)，这样相当于取到了3个参数(self, By.ID, “su”)
而presence_of_element_located类中__init__()方法取的确实是2个参数(self, locator)，其中locator调用的是一个tuple（元组）
该元组(By.ID,“su”)作为一个整体，对应相当于1个参数，加上类实例化代表自身的self参数，正好就是2个参数
因此，执行代码正确的写法为：presence_of_element_located((By.ID,“su”))，即需要嵌套两层英文圆括号

expected_conditions类提供的预期条件判断的方法

方法	说明
title_is	判断当前页面的 title 是否完全等于（==）预期字符串，返回布尔值
title_contains	判断当前页面的 title 是否包含预期字符串，返回布尔值
presence_of_element_located	判断某个元素是否被加到了 dom 树里，并不代表该元素一定可见
visibility_of_element_located	判断元素是否可见（可见代表元素非隐藏，并且元素宽和高都不等于 0）
visibility_of	同上一方法，只是上一方法参数为locator，这个方法参数是 定位后的元素
presence_of_all_elements_located	判断是否至少有 1 个元素存在于 dom 树中。举例：如果页面上有 n 个元素的 class 都是’wp’，那么只要有 1 个元素存在，这个方法就返回 True
text_to_be_present_in_element	判断某个元素中的 text 是否 包含 了预期的字符串
text_to_be_present_in_element_value	判断某个元素中的 value 属性是否包含 了预期的字符串
frame_to_be_available_and_switch_to_it	判断该 frame 是否可以 switch进去，如果可以的话，返回 True 并且 switch 进去，否则返回 False
invisibility_of_element_located	判断某个元素中是否不存在于dom树或不可见
element_to_be_clickable	判断某个元素中是否可见并且可点击
staleness_of	等某个元素从 dom 树中移除，注意，这个方法也是返回 True或 False
element_to_be_selected	判断某个元素是否被选中了,一般用在下拉列表
element_selection_state_to_be	判断某个元素的选中状态是否符合预期
element_located_selection_state_to_be	跟上面的方法作用一样，只是上面的方法传入定位到的 element，而这个方法传入 locator
alert_is_present	判断页面上是否存在 alert
————————————————
版权声明：本文为CSDN博主「腰椎间盘没你突出」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/sinat_41774836/article/details/88965281
