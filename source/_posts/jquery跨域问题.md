---
title: jquery跨域问题.md
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
title: jquery跨域问题.md
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
###只在后端解决
前端
~~~
  $.get('http://192.168.10.106:8080/test/user/list?cPage=2&pSize=20',{},function(e) {
      alert(e)
  },'json');
~~~

后端使用springboot，添加    @CrossOrigin注解即可
~~~
    @CrossOrigin
    @RequestMapping("/list")
    @Cacheable(value={"cache_cache1","cache_cache2"}, key = "#root.methodName+':'+#root.args[0]+':'+#root.args[1]")
    public R list(Integer cPage,Integer pSize){
        IPage<User> userIPage = userService.selectPage(cPage, pSize);
        return R.ok(userIPage);
    }

~~~
