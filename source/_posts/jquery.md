---
title: jquery.md
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
title: jquery.md
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
**1、全选和取消全选checkbox**

~~~
$("#checkboxInput").change(function(){
			if(this.checked){
				$("#main-tab").find("input[name='choose']").prop("checked",true);
			}else{
				$("#main-tab").find("input[name='choose']").prop("checked",false);
			}
})

~~~

**关于下拉框select-option**
~~~
比如<select class="selector"></select>

1、设置value为pxx的项选中

     $(".selector").val("pxx");

2、设置text为pxx的项选中

    $(".selector").find("option[text='pxx']").attr("selected",true);

    这里有一个中括号的用法，中括号里的等号的前面是属性名称，不用加引号。很多时候，中括号的运用可以使得逻辑变得很简单。

3、获取当前选中项的value

    $(".selector").val();

4、获取当前选中项的text

    $(".selector").find("option:selected").text();

    这里用到了冒号，掌握它的用法并举一反三也会让代码变得简洁。


很多时候用到select的级联，即第二个select的值随着第一个select选中的值变化。这在jquery中是非常简单的。

如：$(".selector1").change(function(){

     // 先清空第二个

      $(".selector2").empty();

     // 实际的应用中，这里的option一般都是用循环生成多个了

      var option = $("<option>").val(1).text("pxx");

      $(".selector2").append(option);

});
~~~
