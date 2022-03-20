---
title: spring-生命周期大盘点.md
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
title: spring-生命周期大盘点.md
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
###java static之间
java static之间也是有顺序的。若A声明在B签签名。A就先于B执行。
但是有时候A要依赖B的结果才能执行。这个时候就要将B调整到A之前：
~~~
     private static ISysDictDataService iSysDictDataService = SpringUtils
        .getBean(ISysDictDataService.class);//B
    private static SelfSmsImpl selfSmsImpl = new SelfSmsImpl();//A

    public SelfSmsImpl() {
        init();
    }

    public void init() {
        List<SysDictData> list = iSysDictDataService.selectDictLabelAndDictValue("sms");
        for (SysDictData sysDictData : list) {
            String dictValue = sysDictData.getDictValue();
            switch (sysDictData.getDictLabel()) {
                case "business.sms.effectiveTime":
                    effectiveTime = Integer.valueOf(dictValue);
                    break;
                case "business.sms.self.server":
                    server = dictValue;
                    break;
                case "business.sms.self.tId":
                    tId = dictValue;
                    break;
                case "business.sms.self.aId":
                    aId = dictValue;
                    break;
                case "business.sms.self.sId":
                    sId = dictValue;
                    break;
                case "business.sms.self.token":
                    token = dictValue;
                    break;
                case "business.sms.self.isTest":
                    isTest = Boolean.valueOf(dictValue);
                    break;
                default:
                    break;
            }

        }
    }


~~~

###spring 实现按需选择初始化接口的实例
>@Component注解只要被扫描到了就会被创建Bean

方法一、如果想实现按需加载。我这里有一种方法：放弃使用spring ioc @Component等容器注解

1、使用单例模式，new实例。在构造函数里初始化参数。
2、接口里定义根据配置标识初始化具体某个实现

~~~
public interface SmsInterface {
    static SmsInterface defaultGetInstant(ISysDictDataService iSysDictDataService) {
        String sms = iSysDictDataService.selectValueByKey("sms", "business.sms.choice");
        if ("SEY".equalsIgnoreCase(sms)) {
            return SeySmsImpl.getInstant();
        } else  {
            return SelfSmsImpl.getInstant();
        }

    }
    Integer sendSms(String round, String mobile);
}
~~~

方法二、使用@Conditional 类的注解如@ConditionalOnExpression 结合@Component等容器读取配置
但是这种方法做不到：读取数据库中的标识来决定使用哪个实现。

方法三、自定义@Conditional 类注解。实现在db中读取配置


###spring实现使用容器内bean的getInstant获取单例
接口
~~~
public interface HospitalSerive {

    static HospitalSerive getHospitalSerive(String hospital) {
        if (Hospital.SEY.equalsIgnoreCase(hospital)) {
            return Sey.getInstant();
        } else if (Hospital.ETYY.equalsIgnoreCase(hospital)) {
            return Etyy.getInstant();
        } else {
            return null;
        }
    }

    void getData();

}
~~~

实现类
~~~
@ConditionalOnExpression("'${business.patientSign.hospital}'.equalsIgnoreCase('ETYY')")
@Service("Etyy")
public class Etyy implements HospitalSerive {

    private static final Logger logger = LoggerFactory.getLogger(Etyy.class);

    private static HospitalSerive hospitalSerive;

    public static HospitalSerive getInstant() {
        return Etyy.hospitalSerive;
    }

    @Resource(name = "Etyy")
    public void setHospitalSerive(HospitalSerive hospitalSerive) {
        Etyy.hospitalSerive = hospitalSerive;
    }

~~~
