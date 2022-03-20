---
title: Jeecg-Boot-数据字典的应用.md
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
title: Jeecg-Boot-数据字典的应用.md
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
>一定要用力的活下去啊！

###使用数据字典给表单下拉框设置选择项
如下，我们需要实现在新增记录和修改记录时有这种下拉框选择项
![image.png](https://upload-images.jianshu.io/upload_images/13965490-2b099aaa35d6fca0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果不配置`数据字典` 那么这种下拉框则是空的，没有选择项。

换言之，配置数据字典就能够配置下拉选择项



######配置数据字典

点击数据字典，再点击右侧的新增数据字典按钮
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cc60117bdd2da7bf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注意这个`字典编码` ，这个就是该数据字典的核心
![image.png](https://upload-images.jianshu.io/upload_images/13965490-43a7f77121e1a02c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
创建数据字段后，点击这个字典配置。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0e8486b4772de4d8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

给数据字典配置子项，如下 正常值为0，异常值为1
![设置](https://upload-images.jianshu.io/upload_images/13965490-b343d94ac63e4b2e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######在实体类中指定数据字典
这个cart_status标识就是咱们的之前创建的数据字典标识

>	`@Dict(dicCode = "cart_status")`
	@Excel(name = "卡状态", width = 15)
    @ApiModelProperty(value = "卡状态")
    private java.lang.Integer status;

######在前端vue页面文件中指定数据字典
><a-form-item label="卡状态" :labelCol="labelCol" :wrapperCol="wrapperCol">
<j-dict-select-tag type="list" v-decorator="['status', validatorRules.status]" :trigger-change="true" `dictCode="cart_status"` placeholder="请选择卡状态"/>
        </a-form-item>

配置完成后重启工程就能看到上面的效果了！

######使用数据字典给报表的字段设置业务值
我们希望报表显示的卡状态是 正常和异常 而不是0和1 。具体效果如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-be8a01d1ee7f2c74.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
找打定义表格的vue文件修改之，这个dataIndex 就是 `字段名_dictText`
>  {
            title:'卡状态',
            align:"center",
            dataIndex: 'status_dictText'
}


######使用数据字典在线开发中表单下拉框取值
表单配置中的`字典Code`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3634bf93da38f99f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

配置数据字典
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c23e2fc8d6644b80.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

最终效果如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b683ca0330a2a50a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######使用数据字典给报表`关联表`字段设置业务值
比如，需要实现下面功能：显示关联的所属单位名而不是显示机构编码
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d6181e6ff22407eb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1、实体类中添加注解如下
~~~
    /**
     * 所属部门
     */
    @Excel(name = "所属部门", width = 15, dictTable = "sys_depart", dicText = "depart_name", dicCode = "org_code")
    @Dict(dictTable = "sys_depart", dicText = "depart_name",dicCode = "org_code")
    @ApiModelProperty(value = "所属部门")
    private java.lang.String sysOrgCode;
~~~

注意报错： 这个问题是因为dicText 和dicCode 搞反了
> select sys_org_code as "text" from sys_depart where depart_name= ?
4.MySQLSyntaxErrorException: Unknown column 'sys_org_code' in 'field list'

  >@Dict(dictTable = "sys_depart", dicText = "depart_name",dicCode = "org_code") 属性说明：
> 1、dictTable：被注解申明的sysOrgCode类变量 关联的表
   2、dicText： 需要得到dictTable 中的业务字段
   3、dicCode ： dictTable 中该子段和被注解申明的sysOrgCode类变量相关联
  4、dicText、dicCode 字段都属于dictTable表




2、前端表字段修改如下，需要加上`_dictText`
~~~
{
            title: '所属单位',
            align: 'center',
            dataIndex: 'sysOrgCode_dictText'
          }
~~~

看看返回字段
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0a8465f1b6ca6541.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
