---
title: javax-validation和hibernate-validator参数校验.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
---
title: javax-validation和hibernate-validator参数校验.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java-三方库学习
categories: java-三方库学习
---
###@Validated和@Valid的区别
**在Controller中校验方法参数时，使用@Valid和@Validated并无特殊差异（若不需要分组校验的话）**
@Valid：标准JSR-303规范的标记型注解，用来标记验证属性和方法返回值，进行级联和递归校验
@Validated：Spring的注解，是标准JSR-303的一个变种（补充），提供了一个分组功能，可以在入参验证时，根据不同的分组采用不同的验证机制

方法级别：
**@Validated注解可以用于类级别**，用于支持Spring进行方法级别的参数校验。**@Valid可以用在属性级别约束，用来表示级联校验。**
@Validated只能用在类、方法和参数上，而@Valid可用于方法、字段、构造器和参数上

###如何使用
这两个包要同时导入！
~~~
   <dependency>
        <groupId>javax.validation</groupId>
        <artifactId>validation-api</artifactId>
        <version>2.0.1.Final</version>
      </dependency>
      <dependency>
        <groupId>org.hibernate.validator</groupId>
        <artifactId>hibernate-validator</artifactId>
        <version>6.0.7.Final</version>
      </dependency>
~~~

~~~
    @PostMapping("/tabletSign/pushInfo/patient")
    public AjaxResult pushInfoPatient(@Valid @RequestBody BizPatient bizPatient) {
    }
~~~

~~~
public class BizPatient {
    private static final long serialVersionUID = 1L;
    @NotNull(message = "id不能为空")
    private Long patientId;
}
~~~

###如何分组校验？
有时候我们需要在不同的Controller中校验不同的字段

Controller
~~~
    @PostMapping("/tabletSign/pushInfo/patient")
    public AjaxResult pushInfoPatient(
        @Validated(BizPatient.SaveGroup.class) @RequestBody BizPatient bizPatient) {
    }

    @PostMapping("/tabletSign/patient/signerInfo")
    public AjaxResult getSignerInfo(
        @Validated(BizPatient.SelectGroup.class) @RequestBody BizPatient bizPatient) {
    }

~~~
javaBean
~~~
public class BizPatient {
    private static final long serialVersionUID = 1L;
    /**
     * $column.columnComment
     */
    //非空判断
    @NotNull(groups = {SaveGroup.class, SelectGroup.class}, message = "patientId 不能为空")
    private Long patientId
}

~~~
###如何校验关联对象？
~~~
    @PostMapping(value = "/saveOrUpdate")
    public GbmResult saveOrUpdate(@RequestBody @Validated GdVo gdVo) {
    }


@Data
public class GdVo {
    @Valid
    private GdAfterSalesDto gdAfterSalesDto;
    @Valid
    private List<GdProcessRecordDto> gdProcessRecordDto;
}

~~~

###手动校验工具类
有时候注解不生效，我们可以手动校验
~~~
import org.springframework.validation.BindingResult;
import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;
import java.util.Set;
import java.util.stream.Collectors;
public class ValidParameterUtils {
    private static Validator validator;

    static {
        validator = Validation.buildDefaultValidatorFactory().getValidator();
    }

    public static void validParameter(BindingResult validResult){
        if (validResult.hasErrors()){
            throw new GBMException(validResult.getFieldError().getDefaultMessage(),GbmResultCode.PARAMETER_EXCEPTION.code());
        }
    }
    public static void validateEntity(Object object, Class<?>... groups)
            throws GBMException {
        Set<ConstraintViolation<Object>> constraintViolations = validator.validate(object, groups);
        if (!constraintViolations.isEmpty()) {
            StringBuilder msg = new StringBuilder();
            for(ConstraintViolation<Object> constraint:  constraintViolations){
                msg.append(constraint.getMessage()).append("  ");
            }
            throw new GBMException(msg.toString(),GbmResultCode.FAIL.code());
        }
    }



    /**
     * @Des 返回错误信息
     * @Author yinkai
     * @Date 2022/2/28 9:24
     */
    public static String validateEntityRString(Object object, Class<?>... groups) {
        Set<ConstraintViolation<Object>> constraintViolations = validator.validate(object, groups);
        return constraintViolations.stream().map(ConstraintViolation::getMessage).collect(Collectors.joining("  "));
    }
}

~~~


使用
~~~
public class ZskQuestionsAndAnswersVo {

    @NotNull(groups = {AddGroup.class}, message = "knowledgeId为空")
    private Long knowledgeId;

    @Length(max = 100, min = 1, message = "问题必须在1-100字符之间")
    @NotBlank(groups = {AddGroup.class}, message = "problemContent为空")
    private String problemContent;
    @Length(max = 500, min = 1, message = "回答必须在1-500字符之间")
    @NotBlank(groups = {AddGroup.class}, message = "answer为空")
    private String answer;

}

~~~
~~~
    @PostMapping(value = "/addQuestionsAndAnswers")
    public GbmResult addQuestionsAndAnswers(@RequestParam("img") MultipartFile[] img,
                                            @RequestParam("vedio") MultipartFile[] vedio,
                                            @Valid ZskQuestionsAndAnswersVo zskQuestionsAndAnswersVo) {
        ValidParameterUtils.validateEntity(zskQuestionsAndAnswersVo,AddGroup.class);
    }
~~~

还需定义全局异常处理器
~~~
@RestControllerAdvice
@Order(100)
public class GBMExceptionHandler {
	private Logger logger = LoggerFactory.getLogger(getClass());


	//处理Get请求中 使用@Valid 验证路径中请求实体校验失败后抛出的异常
	@ExceptionHandler(org.springframework.validation.BindException.class)
	@ResponseBody
	public GbmResult BindExceptionHandler(BindingResult e) {
		String message = e.getAllErrors().stream().map(DefaultMessageSourceResolvable::getDefaultMessage).collect(Collectors.joining());
		return GbmResult.error(GbmResultCode.PARAMETER_EXCEPTION.getCode(),message);
	}
~~~

###校验List
Controller类上加@Validated
~~~
@Validated
public class ZskKnowledgeController {
~~~
handel方法上加
~~~
@PostMapping(value = "/saveOrUpdateZskAccessories")
    public GbmResult saveOrUpdateZskAccessories(@RequestBody @Valid List<ZskAccessoriesListType> zskKnowledgeVoList) {
~~~

###注解含义

@Pattern(regexp = "1[3|4|5|7|8][0-9]\\d{8}",message = "手机号码格式不正确")
	@NotEmpty(message ="returnAndExchangeInformation 不能为空")
@NotNull(message ="knowledgeId 不能为空")
    @Digits(integer = 10, fraction = 2, message = "补发运费格式错误")
    @Length(max = 50, min = 1, message = "配件名称必须在1-50字符之间")


Constraint	详细信息
@AssertFalse	该值必须为False
@AssertTrue	该值必须为True
@DecimalMax(value，inclusive)	被注释的元素必须是一个数字，其值必须小于等于指定的最大值 ，inclusive表示是否包含该值
@DecimalMin(value，inclusive)	被注释的元素必须是一个数字，其值必须大于等于指定的最小值 ，inclusive表示是否包含该值
@Digits	限制必须为一个小数，且整数部分的位数不能超过integer，小数部分的位数不能超过fraction
@Email	该值必须为邮箱格式
@Future	被注释的元素必须是一个将来的日期
@FutureOrPresent	被注释的元素必须是一个现在或将来的日期
@Max(value)	被注释的元素必须是一个数字，其值必须小于等于指定的最大值
@Min(value)	被注释的元素必须是一个数字，其值必须大于等于指定的最小值
@Negative	该值必须小于0
@NegativeOrZero	该值必须小于等于0
@NotBlank	该值不为空字符串，例如“ ”
@NotEmpty	该值不为空字符串
@NotNull	该值不为Null
@Null	该值必须为Null
@Past	被注释的元素必须是一个过去的日期
@PastOrPresent	被注释的元素必须是一个过去或现在的日期
@Pattern(regexp)	匹配正则
@Positive	该值必须大于0
@PositiveOrZero	该值必须大于等于0
@Size(min,max)	数组大小必须在[min,max]这个区间


###自定义注解
手动实现一个自定义注解，做到灵活指定字符串字段只包含数字、字母、特殊符号、中文的校验
~~~

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.*;

@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Constraint(
        validatedBy = {ContainCharValidator.class}
)
public @interface ContainChar {
    String message() default "";

    Class<?>[] groups() default {};

    //必须包含这个，否则报错
    //javax.validation.ConstraintDefinitionException: HV000074: com.gbm.cloud.treasure.entity.zsk.ContainChar contains Constraint annotation, but does not contain a payload parameter.
    Class<? extends Payload>[] payload() default {};

    ContainCharEnum[] value() default {ContainCharEnum.CHINESE, ContainCharEnum.NUMBER, ContainCharEnum.LETTER, ContainCharEnum.SYMBOL};

}
~~~
~~~

/**
 * @Des
 * @Author yinkai
 * @Date 2022/3/1 14:38
 */
public class ContainCharValidator implements ConstraintValidator<ContainChar, String> {
    private String message;
    private ContainCharEnum[] values;
    private Class<?>[] groups;

    @Override
    public void initialize(ContainChar constraintAnnotation) {
        this.message = constraintAnnotation.message();
        this.values = constraintAnnotation.value();
        this.groups = constraintAnnotation.groups();
    }

    /**
     * @Des 遍历，全都不包含才返回false
     * @Author yinkai
     * @Date 2022/3/1 13:49
     */
    public boolean isValid2(String value, ConstraintValidatorContext context) {
        for (ContainCharEnum containCharEnum : values) {
            switch (containCharEnum) {
                case CHINESE:
                    if (!CHINESE.getPattern().matcher(value).find()) {
                        //禁止默认消息返回
                        context.disableDefaultConstraintViolation();
                        //自定义返回消息
                        context.buildConstraintViolationWithTemplate(message+"不包含"+containCharEnum).addConstraintViolation();
                        return false;
                    }
                    break;
                case NUMBER:
                    if (!NUMBER.getPattern().matcher(value).find()) {
                        //禁止默认消息返回
                        context.disableDefaultConstraintViolation();
                        //自定义返回消息
                        context.buildConstraintViolationWithTemplate(message+"不包含"+containCharEnum).addConstraintViolation();
                        return false;
                    }
                    break;
                case SYMBOL:
                    if (!SYMBOL.getPattern().matcher(value).find()) {
                        //禁止默认消息返回
                        context.disableDefaultConstraintViolation();
                        //自定义返回消息
                        context.buildConstraintViolationWithTemplate(message+"不包含"+containCharEnum).addConstraintViolation();
                        return false;
                    }
                    break;
                case LETTER:
                    if (!LETTER.getPattern().matcher(value).find()) {
                        //禁止默认消息返回
                        context.disableDefaultConstraintViolation();
                        //自定义返回消息
                        context.buildConstraintViolationWithTemplate(message+"不包含"+containCharEnum).addConstraintViolation();
                        return false;
                    }
                    break;
                default:
                    break;
            }
        }
        return true;
    }


    //遍历，全都不包含才返回false || 包含之外的就返回false
    // !(包含一个 && 只包含内部)
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        HashSet<Boolean> booleans = new HashSet<>(2);
        StringBuilder stringBuilder = new StringBuilder();
        for (ContainCharEnum containCharEnum : values) {
            booleans.add(containCharEnum.getPattern().matcher(value).find());
            stringBuilder.append(containCharEnum);
        }
        //不包含true-->全都是false-->全都不包含
        if (!booleans.contains(Boolean.TRUE)) {
            //禁止默认消息返回
            context.disableDefaultConstraintViolation();
            //自定义返回消息
            context.buildConstraintViolationWithTemplate(message + value + "不包含 " + stringBuilder).addConstraintViolation();
            return false;
        }
        Set<ContainCharEnum> noFindSet = Arrays.stream(values()).filter(m -> !ArrayUtil.contains(values, m)).collect(Collectors.toSet());
        for (ContainCharEnum containCharEnum : noFindSet) {
            if (containCharEnum.getPattern().matcher(value).find()) {
                //禁止默认消息返回
                context.disableDefaultConstraintViolation();
                //自定义返回消息
                context.buildConstraintViolationWithTemplate(message + value + "不能包含 " + containCharEnum).addConstraintViolation();
                return false;
            }
        }
        return true;
    }
}

~~~

~~~
public enum ContainCharEnum {
    CHINESE(0, "中文",Pattern.compile("[\u4E00-\u9FA5|\\！|\\，|\\。|\\（|\\）|\\《|\\》|\\“|\\”|\\？|\\：|\\；|\\【|\\】]")),
    NUMBER(1, "数字", Pattern.compile("[0-9]")),
    LETTER(2, "字母",Pattern.compile(".*[a-zA-Z]+.*")),
    SYMBOL(3, "特殊符号",Pattern.compile(".*[`~!@#$%^&*()+=|{}':;',\\[\\]·.<>/?~！@#￥%……&*（）——+|{}【】‘；：”“’。，、？\\\\]+.*"));

    @EnumValue//标记数据库存的值是code
    private Integer code;
    @JsonValue
    private String desc;
    private Pattern pattern;


    ContainCharEnum(Integer code, String desc,Pattern pattern) {
        this.code = code;
        this.desc = desc;
        this.pattern = pattern;
    }

    @Override
    public String toString() {
        return desc;
    }

    public int getValue() {
        return code;
    }

    public Pattern getPattern() {
        return pattern;
    }
}
~~~
