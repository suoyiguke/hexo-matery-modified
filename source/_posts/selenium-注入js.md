---
title: selenium-注入js.md
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
title: selenium-注入js.md
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
注入js，引入jquery，使用jq的api对时间控件进行赋值
js="var script=document.createElement(\"script\");script.type=\"text/javascript\";  script.src=\"https://ajax.aspnetcdn.com/ajax/jquery/jquery-2.1.4.min.js\";  document.getElementsByTagName('head')[0].appendChild(script);  jQuery(jQuery('input[class=\"ant-calendar-range-picker-input\"]')[0]).val('2022-01-01 00:00:00');jQuery(jQuery('input[class=\"ant-calendar-range-picker-input\"]')[1]).val('2022-01-31 23:59:59');"
browser.execute_script(js)
