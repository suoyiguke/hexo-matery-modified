---
title: python+pandas-保存list到本地excel.md
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
title: python+pandas-保存list到本地excel.md
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
pandas 这个库来操作大量数据存excel非常好用

1. 一维列表
~~~
import pandas as pd

def deal():
	# 列表
    company_name_list = ['腾讯', '阿里巴巴', '字节跳动', '腾讯']
    
    # list转dataframe
    df = pd.DataFrame(company_name_list, columns=['company_name'])
    
    # 保存到本地excel
    df.to_excel("company_name_li.xlsx", index=False)


if __name__ == '__main__':
    deal()
~~~
结果：

2. 二维列表
~~~
import pandas as pd
# python+pandas 保存list到本地
def deal():
    # 二维list
    company_name_list = [['腾讯', '北京'], ['阿里巴巴', '杭州'], ['字节跳动', '北京']]

	# list转dataframe
    df = pd.DataFrame(company_name_list, columns=['company_name', 'local'])

	# 保存到本地excel
    df.to_excel("company_name_li.xlsx", index=False)
if __name__ == '__main__':
    deal()
~~~
