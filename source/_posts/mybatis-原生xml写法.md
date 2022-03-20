---
title: mybatis-原生xml写法.md
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
title: mybatis-原生xml写法.md
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
###插入时若参数为NULL则插入为空字符串
因为mysql同时设置了默认值和非空时。insert 参数为NULL的记录是会报错的！只有当insert没有指定具体的字段时，该字段上的默认值才会起作用！

当然这种方式是最简单的但不是最方便的。若需要大规模使用，请使用 mybatis的 typehandel机制

~~~
    @Insert(
        "INSERT INTO tlk_signed_data_master(id,authority,business_org_code,business_system_code,business_type_code,detach,data_digest,cert_info_id) " +
            "VALUES(" +
            "#{signedDataPO.id}," +
            "#{signedDataPO.authority}," +
            "#{signedDataPO.businessOrgCode}," +
            "#{signedDataPO.businessSystemCode}," +
            "#{signedDataPO.businessTypeCode}," +
            "#{signedDataPO.detach}," +
            "IF(ISNULL(#{signedDataPO.dataDigest}),'',#{signedDataPO.dataDigest})," +
            "IF(ISNULL(#{signedDataPO.certInfoId}),'',#{signedDataPO.certInfoId}))" )
    void insertMaster(@Param("signedDataPO") TlkSignedDataMaster tlkSignedDataMaster);
~~~

###in的写法
~~~
    @Select({"<script>",
        "SELECT 1 from  BIZ_CERT_INFO WHERE serial_number IN ",
        "<foreach collection='snList' item='item' index='index' open='(' separator=',' close=')'>",
        "#{item}",
        "</foreach> LIMIT 1",
        "</script>"})
    Integer existUkeyCertBySn(@Param("snList") List<String> snList);
~~~

###批量插入

~~~
  <insert id="insertBatch" parameterType="java.util.List" useGeneratedKeys="true" keyProperty="id">

    INSERT INTO `biz_patient_signer` (`role`, `name`, `identity_type`, `identity_number`,
    `mobile`,`patient_id` )
    VALUES
    <foreach collection="list" item="item" index="index" separator=",">
      (
      #{item.role},
      #{item.name},
      #{item.identityType},
      #{item.identityNumber},
      #{item.mobile},
      #{item.patientId}
      )
    </foreach>

  </insert>

~~~
~~~
   int insertBatch(List<BizPatientSigner> list);
~~~


###列为空则忽略插入
~~~
    public int insertBizPatient(BizPatient bizPatient);
~~~
~~~
    <insert id="insertBizPatient" parameterType="BizPatient" useGeneratedKeys="true" keyProperty="id">
        insert into biz_patient
        <trim prefix="(" suffix=")" suffixOverrides=",">
            <if test="patientId != null and patientId != ''">patient_id,</if>
            <if test="patientName != null and patientName != ''">patient_name,</if>
            <if test="patientAge != null  and patientAge != ''">patient_age,</if>
            <if test="patientGender != null and patientGender != ''">patient_gender,</if>
            <if test="patientBedNo != null and patientBedNo != ''">patient_bed_no,</if>
            <if test="patientIdentityType != null and patientIdentityType != ''">patient_identity_type,</if>
            <if test="patientIdentityNumber != null and patientIdentityNumber != ''">patient_identity_number,</if>
            <if test="mobile != null and mobile != ''">mobile,</if>
        </trim>
        <trim prefix="values (" suffix=")" suffixOverrides=",">
            <if test="patientId != null and patientId != ''">#{patientId},</if>
            <if test="patientName != null and patientName != ''">#{patientName},</if>
            <if test="patientAge != null and patientAge != ''">#{patientAge},</if>
            <if test="patientGender != null  and patientGender != ''">#{patientGender},</if>
            <if test="patientBedNo != null and patientBedNo != ''">#{patientBedNo},</if>
            <if test="patientIdentityType != null and patientIdentityType != ''">#{patientIdentityType},</if>
            <if test="patientIdentityNumber != null and patientIdentityNumber != ''">#{patientIdentityNumber},</if>
            <if test="mobile != null and mobile != ''">#{mobile},</if>
        </trim>
    </insert>
~~~


>注意数值类型得字段不需要判断!=''，，若设置了mybatis会认同于!=0；所以请进行非空判断。
        <if test="patientAge != null">`patient_age` = #{patientAge},</if>



###批量插入+忽略为空字段
jdbc连接需要添加属性
~~~
&allowMultiQueries=true
~~~
~~~
    int insertBatch(List<BizPatientSigner> list);
~~~

~~~
  <insert id="insertBatch" parameterType="java.util.List" >

    <foreach collection="list" item="item" index="index" separator =";">
      INSERT INTO biz_patient_signer
      <trim prefix="(" suffix=")" suffixOverrides=",">
        <if test="item.role != null and item.role != ''">`role`,</if>
        <if test="item.name != null and item.name != ''">`name`,</if>
        <if test="item.identityType != null and item.identityType != ''">`identity_type`,</if>
        <if test="item.identityNumber != null and item.identityNumber != ''">`identity_number`,</if>
        <if test="item.mobile != null and item.mobile != ''">`mobile`,</if>
        <if test="item.patientId != null and item.patientId != ''">`patient_id`,</if>
      </trim>
      values
      <trim prefix="(" suffix=")" suffixOverrides=",">
        <if test="item.role != null and item.role != ''">#{item.role},</if>
        <if test="item.name != null and item.name != ''">#{item.name},</if>
        <if test="item.identityType != null and item.identityType != ''">#{item.identityType},</if>
        <if test="item.identityNumber != null and item.identityNumber != ''">#{item.identityNumber},</if>
        <if test="item.mobile != null and item.mobile != ''">#{item.mobile},</if>
        <if test="item.patientId != null and item.patientId != ''">#{item.patientId},</if>
      </trim>
    </foreach>
  </insert>
~~~

###delete的in
~~~
    <delete id="deleteBizPatientByIds" parameterType="String">
        delete from biz_patient where patient_id in
        <foreach item="patientId" collection="array" open="(" separator="," close=")">
            #{patientId}
        </foreach>
    </delete>
~~~

###INSERT INTO    ON DUPLICATE KEY UPDATE 语句
1、patient_id为唯一索引
2、useGeneratedKeys对ON DUPLICATE KEY UPDATE是无效的，更新时不会返回主键id。需要自己手动查询了。
~~~
    <insert id="insertBizPatient" parameterType="com.ruoyi.business.domain.entity.BizPatient" useGeneratedKeys="true" keyProperty="id">
        INSERT INTO biz_patient
        <trim prefix="(" suffix=")" suffixOverrides=",">
            <if test="patientId != null and patientId != ''">patient_id,</if>
            <if test="patientName != null and patientName != ''">patient_name,</if>
            <if test="patientAge != null">patient_age,</if>
            <if test="patientGender != null">patient_gender,</if>
            <if test="patientBedNo != null and patientBedNo != ''">patient_bed_no,</if>
            <if test="patientIdentityType != null">patient_identity_type,</if>
            <if test="patientIdentityNumber != null and patientIdentityNumber != ''">patient_identity_number,</if>
            <if test="mobile != null and mobile != ''">mobile,</if>
        </trim>
        <trim prefix="values (" suffix=")" suffixOverrides=",">
            <if test="patientId != null and patientId != ''">#{patientId},</if>
            <if test="patientName != null and patientName != ''">#{patientName},</if>
            <if test="patientAge != null">#{patientAge},</if>
            <if test="patientGender != null">#{patientGender},</if>
            <if test="patientBedNo != null and patientBedNo != ''">#{patientBedNo},</if>
            <if test="patientIdentityType != null">#{patientIdentityType},</if>
            <if test="patientIdentityNumber != null and patientIdentityNumber != ''">#{patientIdentityNumber},</if>
            <if test="mobile != null and mobile != ''">#{mobile},</if>
        </trim>
        ON DUPLICATE KEY UPDATE
        <trim suffixOverrides=",">
        <if test="patientId != null and patientId != ''">`patient_id` = #{patientId},</if>
        <if test="patientName != null and patientName != ''">`patient_name` = #{patientName},</if>
        <if test="patientAge != null">`patient_age` = #{patientAge},</if>
        <if test="patientGender != null">`patient_gender` = #{patientGender},</if>
        <if test="patientBedNo != null and patientBedNo != ''">`patient_bed_no` = #{patientBedNo},</if>
        <if test="patientIdentityType != null">`patient_identity_type` = #{patientIdentityType},</if>
        <if test="patientIdentityNumber != null and patientIdentityNumber != ''">`patient_identity_number` = #{patientIdentityNumber},</if>
        <if test="mobile != null and mobile != ''">`mobile` = #{mobile},</if>
        </trim>


    </insert>
~~~


###insertOrUpdate 批量
~~~
  <insert id="saveHomeDeliveryExtension"  parameterType="list">
    INSERT INTO `home_delivery_extension`(`subItem_name`, `subItem_code`, `merchant_code`, `custom_id`)
    VALUES
    <foreach collection="list" item="item" index="index" separator=",">
      (#{item.subitemName},#{item.subitemCode},#{item.merchantCode},#{item.customId})
    </foreach>
    ON DUPLICATE KEY UPDATE
    subItem_name = values(subItem_name),
    subItem_code = values(subItem_code),
    merchant_code = values(merchant_code),
    custom_id = values(custom_id)
  </insert>
~~~

###in查询

