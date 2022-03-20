---
title: jquery-不同版本兼容.md
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
title: jquery-不同版本兼容.md
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
jquery 不同版本兼容
<script src = "js/jquery.min.js"></script>

<script>
    //这里，添加你的插件，把jquery中的$换成jq,
    var jq=$.noConflict();
    //插件的主体中，所有的$,全部换成jq代替。
    jq("#a").click(function(){
        jq(this).html("aaaa");
    })
</script>
 
<script src = "js/jquery.js"></script>
<script>
    //重新加载的这个jquery，这个使用原来的$方法。
    $("#b").click(function(){
        $(this).html("bbbb");
    })
</script>
