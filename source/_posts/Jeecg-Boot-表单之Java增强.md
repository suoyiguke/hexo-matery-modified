---
title: Jeecg-Boot-表单之Java增强.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---
---
title: Jeecg-Boot-表单之Java增强.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 开源项目
categories: 开源项目
---

Jeecg-Boot 提供了类似于aop面向切面编程的配置方案。名为`java增强` 。具体操作如下：

表单开发==> 选择指定表单===>点击java增强按钮
![image.png](https://upload-images.jianshu.io/upload_images/13965490-83d3ce9b10425b7d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
弹出窗口如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-095183c40090b664.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>1、 页面按钮 ：可以指定 增删改查和导入导出操作

![image.png](https://upload-images.jianshu.io/upload_images/13965490-39668b6b6b4b8415.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 2、事件状态： 指定`增强代码`在具体操作之前还是之后执行

> 3、类型： 指定spring-key即是spring bean name 或者 java-class即类的全限定名

>4、内容：具体spring bean name / 类的全限定名

>5、是否生效


我们来试下，定义一个增强类如下：
> 需使用@Component("testJavaAdd")注解并定义噶好bean name
> 实现CgformEnhanceJavaInter 接口重写execute方法

~~~
package org.jeecg.modules.demo.test.component;
import com.alibaba.fastjson.JSONObject;
import org.jeecg.modules.online.cgform.enhance.CgformEnhanceJavaInter;
import org.jeecg.modules.online.config.exception.BusinessException;
import org.springframework.stereotype.Component;
import java.util.Map;

/**
 *@program: jeecg-boot
 *@description:
 *@author: yinkai
 *@create: 2020-03-29 16:57
 */

@Component("testJavaAdd")
public class TestJavaAdd implements CgformEnhanceJavaInter {

    @Override
    public int execute(String s, Map<String, Object> map) throws BusinessException {

        return 0;
    }

    /**
     *
     * @param s  表名
     * @param jsonObject 请求参数
     * @return
     * @throws BusinessException
     */
    @Override
    public int execute(String s, JSONObject jsonObject) throws BusinessException {
        System.out.println("java增强！");
        System.out.println(s+"==>"+jsonObject);

        return 0;
    }
}
~~~
配置好后重启工程，点击在该表单中点击新增时：打印日志如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-e4c19bb2097217cf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

