---
title: spring-设计模式应用一，选择注入实现类.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
---
title: spring-设计模式应用一，选择注入实现类.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: spring
categories: spring
---
一个接口对应多个实现类，通过配置文件或者请求参数来决定选择注入哪个实现类。

接口中定义静态方法，根据hospital变量获取具体实现
~~~
package com.ruoyi.business.hospital.service;

import com.ruoyi.business.hospital.service.impl.Etyy;
import com.ruoyi.business.hospital.service.impl.Sey;

public interface HospitalSerive {

    static HospitalSerive getHospitalSerive(String hospital) {
        if("SEY".equalsIgnoreCase(hospital)){
            return Sey.getInstant();
        }else if("ETYY".equalsIgnoreCase(hospital)){
            return Etyy.getInstant();
        }
        return null;
    }

    void getData();

}

~~~

实现类Etyy；单例模式+ @Resource 静态实例注入
~~~
package com.ruoyi.business.hospital.service.impl;

import com.ruoyi.business.hospital.service.HospitalSerive;
import javax.annotation.Resource;
import org.springframework.stereotype.Service;

@Service("Etyy")
public class Etyy implements HospitalSerive {
    private static HospitalSerive hospitalSerive;

    public static HospitalSerive getInstant() {
        return Etyy.hospitalSerive;
    }

    @Resource(name="Etyy")
    public void setHospitalSerive(HospitalSerive hospitalSerive) {
        Etyy.hospitalSerive = hospitalSerive;
    }
    @Override
    public void getData() {

    }
}

~~~


实现类Sey
~~~
package com.ruoyi.business.hospital.service.impl;

import com.alibaba.fastjson.JSON;
import com.ewell.sdk.business.EwellServiceTool;
import com.ewell.sdk.domain.MessageEntity;
import com.ewell.sdk.exception.SDKException;
import com.ruoyi.business.domain.entity.BizPatient;
import com.ruoyi.business.hospital.service.HospitalSerive;
import com.ruoyi.business.hospital.entity.sey.HZResponst;
import com.ruoyi.business.hospital.entity.sey.HZResponst.ESBEntryBean.MsgInfoBean;
import com.ruoyi.business.hospital.entity.sey.HZResponst.ReBean;
import com.ruoyi.business.hospital.entity.sey.HZResponst.ReBean.MsgBean.BodyBean.RowBean;
import com.ruoyi.business.hospital.utils.Cover;
import com.ruoyi.business.service.IBizPatientService;
import com.ruoyi.common.exception.CustomException;
import com.ruoyi.common.utils.StringUtils;
import java.util.List;
import javax.annotation.Resource;
import org.json.XML;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service("Sey")
public class Sey implements HospitalSerive {

    private static final Logger log = LoggerFactory.getLogger(Sey.class);
    public static String msgbody = "<ESBEntry><AccessControl><SysFlag>1</SysFlag><UserName>CA</UserName><Password>123456</Password><Fid>BS10003</Fid><OrderNo>BS10003S16001</OrderNo></AccessControl><MessageHeader><Fid>BS10003</Fid><OrderNo>BS10003S16001</OrderNo><SourceSysCode>S16</SourceSysCode><TargetSysCode>S00</TargetSysCode><HospCode>GH01</HospCode><MsgDate>2021-03-25 15:44:55</MsgDate></MessageHeader><RequestOption><triggerData>0</triggerData><dataAmount>500</dataAmount></RequestOption><MsgInfo flag=\"1\" ><Msg/><distinct value=\"0\"/><query item=\"INHOSP_INDEX_NO\" compy=\"=\" value=\"'351372'\" splice=\"AND\"/></MsgInfo><GroupInfo flag=\"0\"><AS ID=\"\" linkField=\"\"/></GroupInfo></ESBEntry>";
    public static String queueManagerName = "QMGR.S16";
    public static Integer waitInterval = 2000;
    private static HospitalSerive hospitalSerive;

    @Resource(name = "Sey")
    public void setHospitalSerive(HospitalSerive hospitalSerive) {
        Sey.hospitalSerive = hospitalSerive;
    }

    public static HospitalSerive getInstant() {
        return Sey.hospitalSerive;
    }

    private static IBizPatientService iBizPatientService;

    @Autowired
    public void setiBizPatientService(IBizPatientService iBizPatientService) {
        Sey.iBizPatientService = iBizPatientService;
    }


    public void getData() {

        String err = "";
        EwellServiceTool ewellServiceTool = new EwellServiceTool();
        MessageEntity msg = null;
        try {
            String cid = ewellServiceTool.connect(queueManagerName);
            String msgid = ewellServiceTool.putMsg(cid, null, msgbody);
            msg = ewellServiceTool
                .getMsgById(cid, null, waitInterval, msgid);
        } catch (SDKException e) {
            err = String.format("获取SEY数据失败，连接异常 %s", e.toString());
            throw new CustomException(err);
        } finally {
            try {
                ewellServiceTool.disconnect();
            } catch (SDKException e) {
                err = String.format("SEY连接关闭异常 %s", e.toString());
                throw new CustomException(err);
            }
        }

        String response = msg.getMsg();
        if (StringUtils.isBlank(response)) {
            err = "获取SEY数据失败，返回消息为空";
            throw new CustomException(err);
        }
        HZResponst hzResponst = JSON
            .parseObject(XML.toJSONObject(response).toString(), HZResponst.class);
        MsgInfoBean msgInfo = hzResponst.getESBEntry().getMsgInfo();
        List<String> msgInfoMsgList = msgInfo.getMsg();
        for (String msgInfoMsg : msgInfoMsgList) {
            String s1 = XML.toJSONObject(msgInfoMsg).toString();
            ReBean reBean = JSON
                .parseObject(s1, ReBean.class);
            RowBean row = reBean.getMsg().getBody().getRow();
            BizPatient bizPatient = new BizPatient();
            bizPatient.setPatientId(String.valueOf(row.getINHOSP_INDEX_NO()));
            bizPatient.setPatientName(row.getPAT_NAME());
            bizPatient
                .setPatientAge(Cover.getAge(String.valueOf(row.getDATE_BIRTH()), "yyyyMMdd"));
            bizPatient.setPatientGender(Cover.getSex(row.getPHYSI_SEX_NAME()));
            bizPatient.setPatientBedNo(String.valueOf(row.getADMIT_BED_CODE()));
            bizPatient.setPatientIdentityType(1);
            bizPatient.setPatientIdentityNumber(String.valueOf(row.getID_NUMBER()));
            bizPatient.setMobile(String.valueOf(row.getPHONE_NO()));
            try {
                iBizPatientService.insertBizPatient(bizPatient);
            } catch (Exception e) {
                log.error("Sey 数据保存异常 {}", e.getMessage());
            } finally {
                log.error(JSON.toJSONString(reBean));
            }

        }
    }
}

~~~

controller注入
~~~
package com.ruoyi.web.controller.business;

import com.alibaba.nacos.api.config.annotation.NacosValue;
import com.ruoyi.business.hospital.service.HospitalSerive;
import com.ruoyi.common.core.domain.AjaxResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 患者数据
 */
@RestController
@RequestMapping("/patient/hospital")
public class DateGetController {

    @NacosValue(value = "${business.patientSign.hospital}", autoRefreshed = true)
    private String hospital;


    @GetMapping("/getData")
    public AjaxResult getData() {
        HospitalSerive hospitalSerive = HospitalSerive.getHospitalSerive(hospital);
        hospitalSerive.getData();
        return AjaxResult.success();
    }

}

~~~


注意：
1、为什么用 @Resource不用  @Autowired？
    @Autowired按类类型注入，而 @Resource按照Bean Name注入；HospitalSerive 接口有多个实现类

2、为什么使用单例模式？
防止出现多个实例浪费服务器资源

3、既然用到了单例模式，那么实现类为啥需要加上@Service()？
为了能够在类中注入其它类对象！

但是这样会不会导致出现多实例？验证一下！

~~~
    @Autowired
    Sey sey;

    @Autowired
    com.ruoyi.business.hospital.service.impl.Etyy etyy;

    @GetMapping("/getData")
    public AjaxResult getData() {
        HospitalSerive hospitalSerive = HospitalSerive.getHospitalSerive(hospital);
        System.out.println(sey.equals(hospitalSerive));
        System.out.println(etyy.equals(hospitalSerive));

        hospitalSerive.getData();
        return AjaxResult.success();
    }

~~~

直接注入sey 和通过getHospitalSerive 的equals返回true


答案是不会出现多个实例！
