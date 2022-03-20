---
title: selenium-选择器.md
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
title: selenium-选择器.md
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
1、input_str = browser.find_element_by_css_selector("[class='ant-input ant-input-lg']")

2、soup.select_one("tbody[class='ant-table-tbody']").find("td")
3、proA = soup.select("div[class='item-desc']").find_one("a")

Selenium之find_element_by_css_selector()的使用方法
2020-05-07阅读 1.9K0
以百度搜索首页为例，我们要定位到搜索输入框的话，应该如何写呢？

单属性查找
# 1.用 标签名 定位查找
driver.find_element_by_css_selector("input")

# 2.用 id 属性定位查找 
driver.find_element_by_css_selector("kw")

# 3.用 class 属性定位查找
driver.find_element_by_css_selector("s_ipt")

# 4.其他属性定位
driver.find_element_by_css_selector("[name="wd"]")
组合属性查找
# 1. 标签名及id属性值组合定位

driver.find_element_by_css_selector("input#kw")

# 2.  标签名及class属性值组合定位

driver.find_element_by_css_selector("input.s_ipt")

# 3. 标签名及属性（含属性值）组合定位

driver.find_element_by_css_selector("input[name="wd"]")

# 4. 标签及属性名组合定位

driver.find_element_by_css_selector("input[name]")

# 5. 多个属性组合定位

driver.find_element_by_css_selector("[class="s_ipt"][name="wd"]")
模糊匹配示例 ， 如需匹配下图中的class
# 1. class拥有多个属性值，只匹配其中一个时
driver.find_element_by_css_selector("input[class ~= "bg"]")

# 2. 匹配以字符串开头的属性值
driver.find_element_by_css_selector("input[class ^= "bg"]")

# 3. 匹配以字符串结尾的属性值
driver.find_element_by_css_selector("input[class $= "s_btn"]")

# 4. 匹配被下划线分隔的属性值
driver.find_element_by_css_selector("input[class |= "s"]")
层级查找
# 1.直接子元素层级关系，如上图的 百度一下 ，input为span的直接子元素(用 > 表示)
driver.find_element_by_css_selector(".bg.s_btn_wr > input")
# class为bg和s_btn_wr 的span标签的子元素input

# 2.只要元素包含在父元素里面，不一定是直接子元素，用空格隔开，如图一所示，form 下面的 span 里面的input
driver.find_element_by_css_selector("#form input")
# id是form的form标签里面的input标签

# 3.多级关系
driver.find_element_by_css_selector("#form > span > input")
# id是form的form标签下面的span标签的下面的input标签

#其他
p:nth-child(1)             # 选择第一个p标签，还可写为 p:first-child
p:nth-last-child(1)             # 选择倒数第一个p标签（要保证最后一个标签是p）
p:only-child        #唯一的p标签
