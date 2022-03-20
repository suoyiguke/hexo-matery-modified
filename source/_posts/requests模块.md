---
title: requests模块.md
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
title: requests模块.md
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
1、指定headers 

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'pragma': 'no-cache',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': 'application/json',
    'x-requested-with': 'XMLHttpRequest',
}

requests.post('https://mall-sop.cgbchina.com.cn/api/trade/order/management/seller/processing',
                              data=json.dumps({'orderId': order[0]}), headers=headers)
