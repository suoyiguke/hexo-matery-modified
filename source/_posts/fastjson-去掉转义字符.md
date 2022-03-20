---
title: fastjson-去掉转义字符.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: fastjson-去掉转义字符.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
fastjson 去掉转义字符，直接使用to Object而不是to string


Object json = JSONObject.toJSON(/*需要序列化的对象*/);
//String json = JSONObject.toJSON(/*需要序列化的对象*/); //产生反斜杠"\"\""

~~~
		jsonObject = JSONObject.toJSONString(JSONObject.parse(jsonObject));
~~~
