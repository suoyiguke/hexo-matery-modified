---
title: mybatis--一对多.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
---
title: mybatis--一对多.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java持久化框架
categories: java持久化框架
---
> 积土成山，风雨兴焉


需求：分页查询TbPoint（一的一方），且将它下面的List<TbBox> （多的一方）也一并查出；实现如下形式的查询
~~~
TbPoint1
    TbBox1
    TbBox2
    TbBox3
TbPoint2
    TbBox4
    TbBox5
    TbBox6
~~~

######实体类
TbBox　实体如下：
它是多的一方，里面有pointId做外键
> /**投放点id*/
    private java.lang.String pointId;
~~~
package org.jeecg.modules.app.entity;

import java.io.Serializable;
import java.io.UnsupportedEncodingException;
import java.util.Date;
import java.math.BigDecimal;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.jboss.logging.Field;
import org.springframework.format.annotation.DateTimeFormat;
import org.jeecgframework.poi.excel.annotation.Excel;
import org.jeecg.common.aspect.annotation.Dict;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

/**
 * @Description: 箱子
 * @Author: jeecg-boot
 * @Date:   2020-03-30
 * @Version: V1.0
 */
@Data
@TableName("tb_box")
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = false)
@ApiModel(value="tb_box对象", description="箱子")
public class TbBox implements Serializable {
    private static final long serialVersionUID = 1L;

	/**主键*/
	@TableId(type = IdType.ID_WORKER_STR)
    @ApiModelProperty(value = "主键")
    private java.lang.String id;
	/**创建人*/
	@Excel(name = "创建人", width = 15, dictTable = "sys_user", dicText = "realname", dicCode = "username")
	@Dict(dictTable = "sys_user", dicText = "realname", dicCode = "username")
    @ApiModelProperty(value = "创建人")
    private java.lang.String createBy;
	/**创建日期*/
	@Excel(name = "创建日期", width = 15, format = "yyyy-MM-dd")
	@JsonFormat(timezone = "GMT+8",pattern = "yyyy-MM-dd")
    @DateTimeFormat(pattern="yyyy-MM-dd")
    @ApiModelProperty(value = "创建日期")
    private java.util.Date createTime;
	/**更新人*/
	@Excel(name = "更新人", width = 15, dictTable = "sys_user", dicText = "realname", dicCode = "username")
	@Dict(dictTable = "sys_user", dicText = "realname", dicCode = "username")
    @ApiModelProperty(value = "更新人")
    private java.lang.String updateBy;
	/**更新日期*/
	@Excel(name = "更新日期", width = 15, format = "yyyy-MM-dd")
	@JsonFormat(timezone = "GMT+8",pattern = "yyyy-MM-dd")
    @DateTimeFormat(pattern="yyyy-MM-dd")
    @ApiModelProperty(value = "更新日期")
    private java.util.Date updateTime;
	/**所属部门*/
	@Excel(name = "所属部门", width = 15, dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
	@Dict(dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
    @ApiModelProperty(value = "所属部门")
    private java.lang.String sysOrgCode;
	/**状态*/
	@Excel(name = "状态", width = 15, dicCode = "box_status")
	@Dict(dicCode = "box_status")
    @ApiModelProperty(value = "状态")
    private java.lang.Integer status;
	/**编号*/
	@Excel(name = "编号", width = 15)
    @ApiModelProperty(value = "编号")
    private java.lang.String number;
	/**设备id*/
	@Excel(name = "设备id", width = 15)
    @ApiModelProperty(value = "设备id")
    private java.lang.String sbNumber;
	/**自编号*/
	@Excel(name = "自编号", width = 15)
    @ApiModelProperty(value = "自编号")
    private java.lang.String ziNumber;
	/**仓库地址*/
	@Excel(name = "仓库地址", width = 15)
    @ApiModelProperty(value = "仓库地址")
    private java.lang.String houseAddress;
	/**投放点*/
	@Excel(name = "投放点", width = 15)
    @ApiModelProperty(value = "投放点")
    private java.lang.String launchPoint;
	/**投放点id*/
	@Excel(name = "投放点id", width = 15)
    @ApiModelProperty(value = "投放点id")
    private java.lang.String pointId;
	/**设备*/
	@Excel(name = "设备", width = 15)
    @ApiModelProperty(value = "设备")
    private java.lang.String sb;



	/**开关*/
	@ApiModelProperty(value = "开关")
	@TableField(exist = false)
	private Integer isOpen = 0;

	/**温度*/
	@ApiModelProperty(value = "温度")
	@TableField(exist = false)
	private String wd = "30";

	/**sd*/
	@ApiModelProperty(value = "湿度")
	@TableField(exist = false)
	private String sd = "30%-60%";

}

~~~


TbPoint 实体如下：
它是一的一方，且有有个boxs属性它是list类型的，表示对应多个TbBox
>   @TableField(exist = false)
    private List<TbBox> boxs;

~~~
package org.jeecg.modules.app.entity;
import java.io.Serializable;
import java.io.UnsupportedEncodingException;
import java.util.Date;
import java.math.BigDecimal;
import java.util.List;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.springframework.format.annotation.DateTimeFormat;
import org.jeecgframework.poi.excel.annotation.Excel;
import org.jeecg.common.aspect.annotation.Dict;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

/**
 * @Description: 箱子投放点
 * @Author: jeecg-boot
 * @Date:   2020-03-30
 * @Version: V1.0
 */
@Data
@TableName("tb_point")
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = false)
@ApiModel(value="tb_point对象", description="箱子投放点")
public class TbPoint implements Serializable {
    private static final long serialVersionUID = 1L;


	/**主键*/
	@TableId(type = IdType.ID_WORKER_STR)
	@ApiModelProperty(value = "主键")
	private java.lang.String id;
	/**创建人*/
	@Excel(name = "创建人", width = 15, dictTable = "sys_user", dicText = "realname", dicCode = "username")
	@Dict(dictTable = "sys_user", dicText = "realname", dicCode = "username")
	@ApiModelProperty(value = "创建人")
	private java.lang.String createBy;
	/**创建日期*/
	@Excel(name = "创建日期", width = 15, format = "yyyy-MM-dd")
	@JsonFormat(timezone = "GMT+8",pattern = "yyyy-MM-dd")
	@DateTimeFormat(pattern="yyyy-MM-dd")
	@ApiModelProperty(value = "创建日期")
	private java.util.Date createTime;
	/**更新人*/
	@Excel(name = "更新人", width = 15, dictTable = "sys_user", dicText = "realname", dicCode = "username")
	@Dict(dictTable = "sys_user", dicText = "realname", dicCode = "username")
	@ApiModelProperty(value = "更新人")
	private java.lang.String updateBy;
	/**更新日期*/
	@Excel(name = "更新日期", width = 15, format = "yyyy-MM-dd")
	@JsonFormat(timezone = "GMT+8",pattern = "yyyy-MM-dd")
	@DateTimeFormat(pattern="yyyy-MM-dd")
	@ApiModelProperty(value = "更新日期")
	private java.util.Date updateTime;
	/**所属部门*/
	@Excel(name = "所属部门", width = 15, dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
	@Dict(dictTable = "sys_depart", dicText = "depart_name", dicCode = "id")
	@ApiModelProperty(value = "所属部门")
	private java.lang.String sysOrgCode;
	/**投放点*/
	@Excel(name = "投放点", width = 15)
	@ApiModelProperty(value = "投放点")
	private java.lang.String name;
	/**地址*/
	@Excel(name = "地址", width = 15)
	@ApiModelProperty(value = "地址")
	private java.lang.String address;
	/**联系人*/
	@Excel(name = "联系人", width = 15)
	@ApiModelProperty(value = "联系人")
	private java.lang.String contacts;
	/**联系方式*/
	@Excel(name = "联系方式", width = 15)
	@ApiModelProperty(value = "联系方式")
	private java.lang.String phoneNumber;


	/**投放点中的箱子数量*/
	@ApiModelProperty(value = "投放点中的箱子数量")
	@TableField(exist = false)
	private java.lang.String boxCount;


	@TableField(exist = false)
	private List<TbBox> boxs;

}

~~~

######mapper
TbPointMapper中定义了一个  getPointPageQHasBoxAll 接口，我需要它将TbPoint分页返回，且TbPoint中关联的多的一方TbBox列表也要被返回。

> 1、使用@Results注解定义一个 resultMap， 里面的boxId属性对应boxs列表。
2、getPointPageQHasBoxAll()这个mapper中将TbPoint的关联的TbBox的id以逗号分隔查询出来，并使用boxId别名输出。
3、getPointPageQHasBoxAll中需要进行 TbPoint的名称搜索查询和 TbBox的编号搜索查询。
4、使用org.jeecg.modules.app.mapper.TbBoxMapper.getBoxListById这个mapper根据逗号分隔的id查询box列表

~~~
    @Select("SELECT GROUP_CONCAT(b.id)  boxId, a.id, a.NAME, count( b.id ) boxCount\n" +
            " FROM tb_point a\n" +
            " LEFT JOIN tb_box b\n" +
            " ON a.id = b.point_id\n" +
            " WHERE ( b.number LIKE concat( '%', #{keyword}, '%' ) OR a.NAME LIKE concat( '%', #{keyword}, '%' )) GROUP BY a.id ORDER BY boxCount DESC\n" +
            " "
    )
    @Results({
            @Result(column="id",property="id"),
            @Result(column="name",property="name"),
            @Result(column="boxCount",property="boxCount"),
            @Result(column="boxId",property="boxs",
                    many=@Many(
                            select="org.jeecg.modules.app.mapper.TbBoxMapper.getBoxListById"
                    )
            )
    })
    IPage<TbPoint> getPointPageQHasBoxAll(Page<TbPoint> page,  @Param("keyword") String keyword);

~~~

为了方便清晰的看出这个sql的作用，我将之单独列出查询下：
~~~
SELECT
	GROUP_CONCAT( b.id ) boxId,
	a.id,
	a.NAME,
	count( b.id ) boxCount 
FROM
	tb_point a
	LEFT JOIN tb_box b ON a.id = b.point_id 
WHERE
	( b.number LIKE concat( '%', '', '%' ) OR a.NAME LIKE concat( '%', '', '%' ) )
GROUP BY
	a.id 
ORDER BY
	boxCount DESC 
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-03981b78ee45288f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>boxId即是该TbPoint关联的TbBox列表的id集合，接下来只需要根据这个id集合查询List<TbBox> 了。


TbBoxMapper中定义了之前指定的org.jeecg.modules.app.mapper.TbBoxMapper.getBoxListByPointId接口如下：
> 注意这个mapper是根据逗号分隔的id来查询List<TbBox>的，所以使用到了mysql的FIND_IN_SET()函数
~~~
/**
 * @Description: 箱子
 * @Author: jeecg-boot
 * @Date:   2020-03-30
 * @Version: V1.0
 */
public interface TbBoxMapper extends BaseMapper<TbBox> {

  /**
     * 根据逗号分隔的id列表，查询 List<TbBox>
     */
    @Select("SELECT * FROM tb_box WHERE FIND_IN_SET(id, #{id} ) ")
    List<TbBox> getBoxListById(@Param("id") String id);


}
~~~
同样为了清晰的看出这个sql的作用，我将之单独列出查询：

~~~
 SELECT * FROM tb_box WHERE FIND_IN_SET(id, '1249601566097281025,1249602136052862977' )
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-84ab19aca7844846.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
最终的查询果，通过debug的方式查看如下：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-78763cc71a2ee942.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




######我们再来看一对多中，多的一方mapper需要传多个参数

> 特别注意 ：
  column="{pointId=id,userId=userId}"  其中pointId、userId是被调用mapper的2个参数；id、userId必须在TbPoint这个实体中存在（当然数据库中可以没有），其实这里还定义了一个看似多余的 @Result(column="userId",property="userId")，然后在TbPoint中添加userId属性，sql中还需定义`'${userId}' userId `的select；这样才能保证将调用者mapper中的userId参数传到被调用者mapper中去


我们先来看一的一方的mapper（调用者mapper）
~~~
 @Select("SELECT\n" +
            "	a.id,\n" +
            "	a.NAME,\n" +
            "	count( b.id ) boxCount, \n" +
            "	'${userId}' userId \n" +
            "FROM\n" +
            "	tb_point a\n" +
            "	LEFT JOIN tb_box b ON a.id = b.point_id \n" +
            "WHERE\n" +
            "	a.sys_org_code IN ( SELECT DISTINCT org_code FROM sys_depart WHERE id IN ( SELECT DISTINCT dep_id FROM sys_user_depart WHERE user_id = #{userId} ) )  AND b.sys_org_code IN ( SELECT DISTINCT org_code FROM sys_depart WHERE id IN ( SELECT DISTINCT dep_id FROM sys_user_depart WHERE user_id = #{userId} ) )  \n" +
            "	AND ( b.number LIKE concat( '%', #{keyword}, '%' ) OR a.NAME LIKE concat( '%', #{keyword}, '%' )) \n" +
            "GROUP BY\n" +
            "	a.id,\n" +
            "	a.NAME,\n" +
            "	a.address ORDER BY boxCount DESC \n"
    )
    @Results({
            @Result(column="id",property="id"),
            @Result(column="name",property="name"),
            @Result(column="boxCount",property="boxCount"),
            @Result(column="userId",property="userId"),
            @Result(column="{pointId=id,userId=userId}",property="boxs",
                    many=@Many(
                            select="org.jeecg.modules.app.mapper.TbBoxMapper.getBoxListByPointId"
                    )
            )
    })
    IPage<TbPoint> getPointPageQHasBox(Page<TbPoint> page, @Param("userId") String userId,  @Param("keyword") String keyword);

~~~

多的一方的mapper（被调用者mapper）
~~~
   /**
     * 根据point_id 查找list
     */
    @Select("SELECT\n" +
            "	* \n" +
            "FROM\n" +
            "	tb_box \n" +
            "WHERE\n" +
            "	point_id = #{pointId} \n" +
            "	AND sys_org_code IN ( SELECT DISTINCT org_code FROM sys_depart WHERE id IN ( SELECT DISTINCT dep_id FROM sys_user_depart WHERE user_id = #{userId} ) ) \n" +
            "ORDER BY\n" +
            "	create_time DESC")
    List<TbBox>  getBoxListByPointId(@Param("pointId") String pointId,@Param("userId") String userId);

~~~
