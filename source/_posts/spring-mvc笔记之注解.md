---
title: spring-mvc笔记之注解.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
---
title: spring-mvc笔记之注解.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: javaweb
categories: javaweb
---
###控制方法注解
1、@RequestMapping

>1、 value， method
value：     指定请求的实际地址，指定的地址可以是URI Template 
method：  指定请求的method类型， GET、POST、PUT、DELETE等；

>2、consumes
consumes： 指定处理请求的提交内容类型（Content-Type），例如application/json, text/html;
produces:    指定返回的内容类型，仅当request请求头中的(Accept)类型中包含该指定类型才返回；

>3、params
params： 指定request中必须包含某些参数
headers： 指定request中必须包含某些指定的header值

>4、produces
指定 produces = "application/json; charset=utf-8" 解决返回json ??乱码问题
    @RequestMapping(value = "CaLogin", produces = "application/json; charset=utf-8")


2、@PostMapping

3、@PutMapping

4、@DeleteMapping

5、@GetMapping


###参数注解
1、@RequestBody注解
> 使用RequestBody注解，那么前端发起 post 请求请将参数放到body里面

![image.png](https://upload-images.jianshu.io/upload_images/13965490-287f98ea06598543.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

后端可以这样接接收：

使用@RequestBody 注解，注意这个注解只能用在实体类上，实体类里面就用具体字段接受。且只能用一次：
~~~
 @RequestMapping(value = "/warehousing", method = RequestMethod.POST)
    public Result<?> warehousing(@RequestBody TbBox tbBox) {
        Result<Object> result = new Result<>();
        if (StringUtils.isBlank(tbBox.getId())) {
            return result.error500("参数为空！");
        }
        iTbPointService.warehousing(tbBox.getId());
        result.setSuccess(true);
        result.setResult("回收成功");
        return result;
    }

~~~

如果实体中不存在接收字段，则可以使用Map来接收参数，如下：
~~~
@RequestBody Map map
~~~



2、@RequestParam注解
>@RequestParam 一般使用在get请求中，可以获取在url中?和&拼接的参数

参数如下：
>1、value/name 请求参数中的名称 （必写参数）
2、required 请求参数中是否必须提供此参数，默认值是true，true为必须提供
3、defaultValue 默认值

@RequestParam的required参数 可以用来指定是否必传，这样就不用自己手动在controller方法中进行非空判断了！但是service接口还是需要进行参数的非空判断的！
如果设置了defaultValue 那么required就强制为false了


使用如下：
~~~
    @RequestMapping(value = "/getPointPageQ", method = RequestMethod.GET)
    public Result<?> getPointPageQ(
            HttpServletRequest request,
            @RequestParam(name = "name", defaultValue = "") String name,
            @RequestParam(name = "pageNo", defaultValue = "1") Integer pageNo,
            @RequestParam(name = "pageSize", defaultValue = "10") Integer pageSize) {
~~~


3、 @PathVariable注解

这个注解一般用来拿到url中以{}占位符表达的参数
