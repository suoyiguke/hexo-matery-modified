---
title: 返回json.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: strut2
categories: strut2
---
---
title: 返回json.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: strut2
categories: strut2
---
注意返回值是void，只返回json就不需要添加配置文件了
~~~

public void addUser()  {

      response.setContentType("application/json;charset=UTF-8");
        HashMap<String, String> hashMap = new HashMap<>();
        hashMap.put("name","haha");
        hashMap.put("age","22");
        String s = JSON.toJSONString(hashMap);
        response.getWriter().write(s);

    }
~~~
