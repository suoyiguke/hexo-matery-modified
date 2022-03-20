---
title: fastjson.md
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
title: fastjson.md
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
###判断json还是array
~~~
//字符串的话会报错
        Object o = JSON.parse("{\"rotation\":0,\"scale\":0,\"fontSizeLarge\":0,\"textScale\":0,\"bold\":0,\"type\":\"text\",\"italic\":0,\"lineSpacing\":0,\"halignment\":2,\"fontName\":\"黑体\",\"lineStyle\":0,\"top\":142,\"valignment\":0,\"left\":24,\"textLengthLarge\":0,\"transparency\":0,\"underLine\":0,\"width\":25,\"fontSize\":14,\"value\":\"\",\"height\":6}");
        if(o instanceof JSONObject){
            System.out.println(o);
        }else if(o instanceof JSONArray){
            System.out.println(o);

        }else {
            
        }
~~~

~~~
//字符串时不会报错
        Object json = new org.json.JSONTokener("[{\"rotation\":0,\"scale\":0,\"fontSizeLarge\":0,\"textScale\":0,\"bold\":0,\"type\":\"text\",\"italic\":0,\"lineSpacing\":0,\"halignment\":2,\"fontName\":\"黑体\",\"lineStyle\":0,\"top\":142,\"valignment\":0,\"left\":24,\"textLengthLarge\":0,\"transparency\":0,\"underLine\":0,\"width\":25,\"fontSize\":14,\"value\":\"\",\"height\":6},{\"id\":\"ysf_icon\",\"rotation\":0,\"scale\":0,\"fontSizeLarge\":0,\"textScale\":0,\"bold\":0,\"type\":\"text\",\"italic\":0,\"lineSpacing\":0,\"halignment\":2,\"fontName\":\"黑体\",\"lineStyle\":0,\"top\":142,\"valignment\":0,\"left\":0.9,\"textLengthLarge\":0,\"transparency\":0,\"underLine\":0,\"width\":8,\"fontSize\":14,\"value\":\"预\",\"height\":6}]").nextValue();
        if (json instanceof org.json.JSONObject) {
            org.json.JSONObject jsonObject = (org.json.JSONObject) json;
            System.out.println(jsonObject);
            //自行解析即可
        } else if (json instanceof org.json.JSONArray) {
            org.json.JSONArray jsonArray = (org.json.JSONArray) json;
            System.out.println(jsonArray);

        }

~~~

###Fastjson的SerializerFeature序列化属性
~~~
QuoteFieldNames———-输出key时是否使用双引号,默认为true 
WriteMapNullValue——–是否输出值为null的字段,默认为false 
WriteNullNumberAsZero—-数值字段如果为null,输出为0,而非null 
WriteNullListAsEmpty—–List字段如果为null,输出为[],而非null 
WriteNullStringAsEmpty—字符类型字段如果为null,输出为”“,而非null 
WriteNullBooleanAsFalse–Boolean字段如果为null,输出为false,而非null
~~~

~~~
public enum SerializerFeature {
    QuoteFieldNames,
    /**
     * 
     */
    UseSingleQuotes,
    /**
     * 
     */
    WriteMapNullValue,
    /**
     * 用枚举toString()值输出
     */
    WriteEnumUsingToString,
    /**
     * 用枚举name()输出
     */
    WriteEnumUsingName,
    /**
     * 
     */
    UseISO8601DateFormat,
    /**
     * @since 1.1
     */
    WriteNullListAsEmpty,
    /**
     * @since 1.1
     */
    WriteNullStringAsEmpty,
    /**
     * @since 1.1
     */
    WriteNullNumberAsZero,
    /**
     * @since 1.1
     */
    WriteNullBooleanAsFalse,
    /**
     * @since 1.1
     */
    SkipTransientField,
    /**
     * @since 1.1
     */
    SortField,
    /**
     * @since 1.1.1
     */
    @Deprecated
    WriteTabAsSpecial,
    /**
     * @since 1.1.2
     */
    PrettyFormat,
    /**
     * @since 1.1.2
     */
    WriteClassName,

    /**
     * @since 1.1.6
     */
    DisableCircularReferenceDetect, // 32768

    /**
     * @since 1.1.9
     */
    WriteSlashAsSpecial,

    /**
     * @since 1.1.10
     */
    BrowserCompatible,

    /**
     * @since 1.1.14
     */
    WriteDateUseDateFormat,

    /**
     * @since 1.1.15
     */
    NotWriteRootClassName,

    /**
     * @since 1.1.19
     * @deprecated
     */
    DisableCheckSpecialChar,

    /**
     * @since 1.1.35
     */
    BeanToArray,

    /**
     * @since 1.1.37
     */
    WriteNonStringKeyAsString,
    
    /**
     * @since 1.1.42
     */
    NotWriteDefaultValue,
    
    /**
     * @since 1.2.6
     */
    BrowserSecure,
    
    /**
     * @since 1.2.7
     */
    IgnoreNonFieldGetter,
    
    /**
     * @since 1.2.9
     */
    WriteNonStringValueAsString,
    
    /**
     * @since 1.2.11
     */
    IgnoreErrorGetter,

    /**
     * @since 1.2.16
     */
    WriteBigDecimalAsPlain,

    /**
     * @since 1.2.27
     */
    MapSortField;
}
~~~

使用测试
~~~
public class Test {

    public static class Model {
        public Integer id;
        public String name;
        public Integer sex;
        public Boolean aBoolean;
        public List list;


        public Integer getId() {
            return id;
        }

        public void setId(Integer id) {
            this.id = id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public Integer getSex() {
            return sex;
        }

        public void setSex(Integer sex) {
            this.sex = sex;
        }

        public Boolean getaBoolean() {
            return aBoolean;
        }

        public void setaBoolean(Boolean aBoolean) {
            this.aBoolean = aBoolean;
        }

        public List getList() {
            return list;
        }

        public void setList(List list) {
            this.list = list;
        }
    }

    public static void main(String[] args) {
        Model model = new Model();
        model.setId(1);
        //{{"id":1}
        System.out.println(JSON.toJSONString(model,SerializerFeature.QuoteFieldNames));
        //{'id':1}
        System.out.println(JSON.toJSONString(model,SerializerFeature.UseSingleQuotes));

        //{"aBoolean":null,"id":1,"list":null,"name":null,"sex":null}
        System.out.println(JSON.toJSONString(model,SerializerFeature.WriteMapNullValue));


        model.setSex(null);
        //{"id":1,"sex":0}
        System.out.println(JSON.toJSONString(model,SerializerFeature.WriteNullNumberAsZero));

        model.setaBoolean(null);
        //{"aBoolean":false,"id":1}
        System.out.println(JSON.toJSONString(model,SerializerFeature.WriteNullBooleanAsFalse));

        model.setName(null);
        //{"id":1,"name":""}
        System.out.println(JSON.toJSONString(model,SerializerFeature.WriteNullStringAsEmpty));

        //{"id":1,"list":[]}
        model.setList(null);
        System.out.println(JSON.toJSONString(model,SerializerFeature.WriteNullListAsEmpty));


    }
}

~~~
###编程方式
1、转json指定日期格式
~~~
String json = JSON.toJSONString(map, SerializerFeature.DisableCircularReferenceDetect,SerializerFeature.WriteDateUseDateFormat);
~~~







 

 ###注解方式
####@JSONField

3、 @JSONField(jsonDirect=true) 解决属性值也是json字符串而导致的转义问题
~~~
public class Test {
    public static class Model {
        public int id;
        @JSONField(jsonDirect=true)
        public String value;
    }
    public static void main(String[] args) {
        AESUtilsTest.Model model = new AESUtilsTest.Model();
        model.id = 1001;
        model.value = "{\"tradeNo\": \"AOAOA\"}";
        String json = JSON.toJSONString(model);
        //{"id":1001,"value":{"tradeNo":"AOAOA"}}
        System.out.println(json);
    }
}
~~~

 
4、在实体类上的字段使用@JSONField定制序列化：
~~~
//配置序列化的时候,不序列化id 
@JSONField(serialize=false) 
private int id; 
private String name;// 姓名 
private int age; //年龄 
// 配置序列化的名称 
@JSONField(name="gender") 
public String sex;
~~~

####JSONType
5、在类上通过@JSONType定制序列化：
~~~
//配置序列化的时候,不序列化id  sex
@JSONType(ignores ={"id", "sex"}) 
public class Uoimplements Serializable {}
// 配置序列化的时候,序列化name 和sex
@JSONType(includes={"name","sex"}) 
public class Uo1implements Serializable {}
~~~
 





 

###使用SerializeFilter定制序列化：
https://github.com/alibaba/fastjson/wiki/SerializeFilter
通过SerializeFilter可以使用扩展编程的方式实现定制序列化。fastjson提供了多种SerializeFilter：

PropertyPreFilter： 根据PropertyName判断是否序列化；
PropertyFilter： 根据PropertyName和PropertyValue来判断是否序列化；
NameFilter： 修改Key，如果需要修改Key,process返回值则可；
ValueFilter： 修改Value；
BeforeFilter： 序列化时在最前添加内容；
AfterFilter： 序列化时在最后添加内容；
以上的SerializeFilter在JSON.toJSONString中可以使用。

 
1、PropertyPreFilter 定制序列化

实现类SimplePropertyPreFilter  ,只序列化一部分字段,将需要序列化的字段名,配置到数组中。如果什么都不配置,则序列化全部字段
~~~

    public static class Model {
        public int id;
        public String name;
        public int sex;

        public int getId() {
            return id;
        }

        public void setId(int id) {
            this.id = id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public int getSex() {
            return sex;
        }

        public void setSex(int sex) {
            this.sex = sex;
        }
    }

    public static void main(String[] args) {
        Model user = new Model();
        user.setId(1);
        user.setName("lanjingling");
        user.setSex(4);
        //定制序列化,只序列化一部分字段,将需要序列化的字段名,配置到数组中 如果什么都不配置,则序列化全部字段
        SimplePropertyPreFilter filter = new SimplePropertyPreFilter(Model.class, new String[]{"name"});
        String jsonString = JSON.toJSONString(user, filter);
        System.out.println(jsonString);

    }
~~~
 

2、PropertyFilter 根据key和value判断是否需要序列化： 
~~~
    public static void main(String[] args) {
        Model model = new Model();
        model.setId(1);
        model.setName("lanjingling");
        model.setSex(1);
        PropertyFilter filter = new PropertyFilter() {
            @Override
            public boolean apply(Object object, String key, Object value) {
                if (key.equals("sex")) {
                    if ((Integer) value == 1) {
                        return true;
                    }
                }
                return false;
            }
        };
        String jsonString = JSON.toJSONString(model, filter);
        System.out.println(jsonString);
    }
~~~
 

3、NameFilter ：

PascalNameFilter 输出驼峰风格的key
~~~
public class Test {

    public static class Model {
        public int id;
        public String value;
    }
    public static void main(String[] args) {
        AESUtilsTest.Model model = new AESUtilsTest.Model();
        model.id = 1001;
        model.value = "{\"tradeNo\":\"AOAOA\"}";
        String jsonStr = JSON.toJSONString(model, new PascalNameFilter());
        System.out.println(jsonStr);
    }
}

~~~

 
4、ValueFilter 序列化时修改value：
~~~
    public static void main(String[] args) {
        Model model = new Model();
        model.setId(1);
        model.setName("lanjingling");
        model.setSex(4);
        ValueFilter filter = new ValueFilter() {
            @Override
            public Object process(Object object, String name, Object value) {
                if (name.equals("name")) {
                    return "张三";
                }
                return value;
            }
        };
        String jsonStr = JSON.toJSONString(model, filter);
        System.out.println(jsonStr);

    }
~~~
 

5、BeforeFilter 序列化时在最前添加内容  :
~~~
    public static void main(String[] args) {
        Model model = new Model();
        model.setId(1);
        model.setName("lanjingling");
        model.setSex(4);
        BeforeFilter filter = new BeforeFilter() {
            @Override
            public void writeBefore(Object object) {
                writeKeyValue("start","bofore");
            }
        };
        String jsonStr = JSON.toJSONString(model, filter);
        //{"start":"bofore","id":1,"name":"lanjingling","sex":4}
        System.out.println(jsonStr);

    }
~~~
 

6、AfterFilter 序列化之时在最后添加内容  ：
~~~
    public static void main(String[] args) {
        Model model = new Model();
        model.setId(1);
        model.setName("lanjingling");
        model.setSex(4);
        AfterFilter filter = new AfterFilter() {
            @Override
            public void writeAfter(Object object) {
                writeKeyValue("end", "after");
            }
        };
        String jsonStr = JSON.toJSONString(model, filter);
        //{"id":1,"name":"lanjingling","sex":4,"end":"after"}
        System.out.println(jsonStr);
    }
~~~


####提供的封装类
PropertyPreFilters封装了SimplePropertyPreFilter，可以更灵活的控制字段是否输出
~~~
    public static void main(String[] args) {
   Model model = new Model();
        model.setId(1);
        model.setName("lanjingling");
        model.setSex(1);
        PropertyPreFilters propertyPreFilters = new PropertyPreFilters();
        PropertyPreFilters.MySimplePropertyPreFilter mySimplePropertyPreFilter = propertyPreFilters.addFilter("id");
        System.out.println(JSON.toJSONString(model, mySimplePropertyPreFilter));
        //{"id":1}
        mySimplePropertyPreFilter.addIncludes("sex");
        //{"id":1,"sex":1}
        System.out.println(JSON.toJSONString(model, mySimplePropertyPreFilter));

        mySimplePropertyPreFilter.addIncludes("name");
        //{"id":1,"name":"lanjingling","sex":1}
        System.out.println(JSON.toJSONString(model, mySimplePropertyPreFilter));

        mySimplePropertyPreFilter.addExcludes("id");
        //{"name":"lanjingling","sex":1}
        System.out.println(JSON.toJSONString(model, mySimplePropertyPreFilter));
    }
~~~




###问题
1、自定义SerializeFilter用法，编程式

~~~
    public static void main(String[] args) {

        ExtItem extItem = new ExtItem();
        extItem.setMaxValue(100);
        String s = JSON.toJSONString(extItem, new PropertyFilter() {
            @Override
            public boolean apply(Object object, String name, Object value) {
                if (null == value) {
                    return false;
                }
                return true;
            }
        });
        System.out.println(s);
    }
~~~

2、自定义SerializeFilter用法，注解式
~~~
    @JSONType(serialzeFilters= ExtItem.MyPropertyFilter.class)
    public static class ExtItem {
     }


   public static void main(String[] args) {

        ExtItem extItem = new ExtItem();
        extItem.setMaxValue(100);
        String s = JSON.toJSONString(extItem);
        System.out.println(s);
    }

~~~

