---
title: mybatis-plus-填充策略FieldFill应用.md
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
title: mybatis-plus-填充策略FieldFill应用.md
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
~~~
package com.gbm.cloud.common.config;

import com.baomidou.mybatisplus.core.handlers.MetaObjectHandler;
import com.gbm.cloud.common.util.AuthorizationUtil;
import org.apache.ibatis.reflection.MetaObject;
import org.springframework.stereotype.Component;

import java.util.Date;

@Component
public class MetaHandler implements MetaObjectHandler {


    /**
     * 新增数据执行
     * @param metaObject
     */
    @Override
    public void insertFill(MetaObject metaObject){
        this.setFieldValByName("createTime", new Date(), metaObject);
        this.setFieldValByName("createDate", new Date(), metaObject);
        this.setFieldValByName("createUser", AuthorizationUtil.getUserName(), metaObject);
    }

    @Override
    public void updateFill(MetaObject metaObject) {
        this.setFieldValByName("updateTime", new Date(), metaObject);
        this.setFieldValByName("updateDate", new Date(), metaObject);
        this.setFieldValByName("updateUser", AuthorizationUtil.getUserName(), metaObject);
    }
}

~~~

~~~
   @Bean
    public GlobalConfig globalConfig() {
        GlobalConfig globalConfig = new GlobalConfig();
        globalConfig.setMetaObjectHandler(new MetaHandler());
        return globalConfig;
    }
~~~

定义基类
~~~
package com.gbm.cloud.treasure.entity.gd;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.extension.activerecord.Model;
import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import org.springframework.format.annotation.DateTimeFormat;

import java.util.Date;


@Data
public abstract class BaseEntity<T extends Model> extends Model {
    @JsonFormat(timezone = "GMT+8",pattern = "yyyy-MM-dd HH:mm:ss")
    @DateTimeFormat(pattern="yyyy-MM-dd HH:mm:ss")
    @TableField(value = "create_date", fill = FieldFill.INSERT)
    private Date createDate;

    @TableField(value = "create_user", fill = FieldFill.INSERT)
    private String createUser;

    @JsonFormat(timezone = "GMT+8",pattern = "yyyy-MM-dd HH:mm:ss")
    @DateTimeFormat(pattern="yyyy-MM-dd HH:mm:ss")
    @TableField(value = "update_Date", fill = FieldFill.INSERT_UPDATE)
    private Date updateDate;

    @TableField(value = "update_user", fill = FieldFill.INSERT_UPDATE)
    private Date updateUser;

}
~~~

使用
~~~
package com.gbm.cloud.treasure.entity.gd;

import java.util.Date;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.hibernate.validator.constraints.Length;
import org.springframework.format.annotation.DateTimeFormat;

import javax.validation.constraints.NotNull;

/**
 * @Description: gd_process_record
 * @Author: yinkai
 * @Date:   2022-03-18
 * @Version: V1.0
 */
@Data
@TableName("gd_process_record")
@EqualsAndHashCode(callSuper = false)
@Accessors(chain = true)
@Builder
public class GdProcessRecordDto extends BaseEntity{

	/**id*/
	@TableId(type = IdType.AUTO)
	private Long id;
	/**处理人（下拉选项）只能选择客服中心的*/
	@NotNull(message="处理人不能为空")
	private String handlerUser;
	/**客户订单号，带出其它信息*/
	@NotNull(message="客户订单号不能为空")
	private String orderNo;
	/**处理人（下拉选项）只能选择客服中心的*/
	@NotNull(message="处理人不能为空")
	private Integer customerComplaintSource;
	/**客诉原因描述及客户诉求（需要指定长度）500*/
	@Length(max = 500, min = 1, message = "客诉原因必须在1-500字符之间")
	private String customerComplaintReason;
	/**客诉处理描述（需要指定长度）500*/
	@Length(max = 500, min = 1, message = "客诉处理描述必须在1-500字符之间")
	private String customerComplaintDescribe;

	/**客诉类别（数据字典）*/
	@NotNull(message="客诉类别不能为空")
	private Integer customerComplaintType;
	/**责任判定 （数据字典）*/
	@NotNull(message="责任判定不能为空")
	private Integer liabilityJudgment;
	/**责任判定类别（数据字典）*/
	@NotNull(message="责任判定类别不能为空")
	private Integer liabilityJudgmentType;
	/**客诉处理结果（数据字典）*/
	@NotNull(message="客诉处理结果不能为空")
	private Integer customerComplaintResult;
	/**客诉状态  0 跟进中 1客户沟通完成 2客诉最终关闭*/
	@NotNull
	private CustomerComplaintState customerComplaintState;
	/**客诉备注*/
	private String customerRemark;
}

~~~
