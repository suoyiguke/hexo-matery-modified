---
title: 动态注入jq.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: web
categories: web
---
---
title: 动态注入jq.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: web
categories: web
---

var script=document.createElement("script");
script.type="text/javascript"; 
script.src="https://ajax.aspnetcdn.com/ajax/jquery/jquery-2.1.4.min.js"; 
document.getElementsByTagName('head')[0].appendChild(script); 
jQuery(jQuery('input[class="ant-calendar-range-picker-input"]')[0]).val('2022-04-01 17:11:39');
jQuery(jQuery('input[class="ant-calendar-range-picker-input"]')[1]).val('2022-04-01 17:11:39');


var script=document.createElement("script");script.type="text/javascript";  script.src="https://ajax.aspnetcdn.com/ajax/jquery/jquery-2.1.4.min.js";  document.getElementsByTagName('head')[0].appendChild(script);  jQuery(jQuery('input[class="ant-calendar-range-picker-input"]')[0]).val(1);jQuery(jQuery('input[class="ant-calendar-range-picker-input"]')[1]).val(2);
