---
title: java-8中使用Optional-避免空指针.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
>Optional 类的引入要求程序员强制处理和避免空指针。Optional 需要使用在可能为null的变量上。很多时候，程序员都是不判空的，这些BUG就像定时炸弹一样，使用Optional 类等于强迫程序员做好判空处理，减少可能的损失。

Optional 类的设计是十分必要的，提前处理可能发生的错误，而不是等到逻辑处理完了再报告错误。
如果返回的null不会终止代码逻辑的运行，比如Java的Map的get方法传了错误类型的key返回null，那么开发者可能会花大量的时间去定位错误的原因，尤其是对于那些庞大的系统来说，无疑是大海捞针。
Scala、lisp、hashshell、erlang等函数式编程语言无一例外地，都对NullPointerException进行了处理，都有Optional的概念，Java8是借鉴了他们。 

###阿里手册中也提到我们需要使用 Optional 类
【推荐】防止 NPE，是程序员的基本修养，注意 NPE 产生的场景：
1）  返回类型为基本数据类型，return 包装数据类型的对象时，自动拆箱有可能产生 NPE。
 反例：
public int f() { return Integer 对象}， 如果为 null，自动解箱抛 NPE。
2） 数据库的查询结果可能为 null。
3） 集合里的元素即使 isNotEmpty，取出的数据元素也可能为 null。
4） 远程调用返回对象时，一律要求进行空指针判断，防止 NPE。
5） 对于 Session 中获取的数据，建议进行 NPE 检查，避免空指针。
6） 级联调用 obj.getA().getB().getC()；一连串调用，易产生 NPE。
正例：使用 JDK8 的 Optional 类来防止 NPE 问题。

###Optional 使用思路
解决办法就是3个步骤：
• 包装value：of(x)传入的对象不能为null，而ofNullable(x)是支持传入null的对象，一般用使用`Optional.ofNullable()`。
• 逐层安全地拆解value：map()。
• 最终返回：orElse()/orElseGet()/orElseThrow()。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d4b848d63b4ec476.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###使用示例
Person 类
~~~
public class Person {
    private String name;
    private Integer age;
    public void setName(String name) {
        this.name = name;
    }
    public void setAge(Integer age) {
        this.age = age;
    }
    @Override
    public String toString() {
        return "Person{" +
            "name='" + name + '\'' +
            ", age=" + age +
            '}';
    }
}
~~~

**用法1、使用内部的ofNullable去掉if的写法，将返回值set到其它对象**
我比喜欢用这个方法，毕竟不要写if xx!=null 。可以直接在ifPresent() 小括号里写各种逻辑。
~~~
    public static void main(String[] args) {
        HashMap<Object, Object> objectObjectHashMap = new HashMap<>();
        objectObjectHashMap.put("name", "kawai");
        objectObjectHashMap.put("age", 18);
        Person a = new Person();
        //TODO 使用内部的ifPresent避免了空指针异常
        Optional.ofNullable(objectObjectHashMap.get("name1"))
            .ifPresent(name -> a.setName(name.toString().toUpperCase()));
        Optional.ofNullable(objectObjectHashMap.get("age1"))
            .ifPresent(age -> a.setAge(Integer.valueOf(age.toString()) + 18));
        System.out.println(a);
    }
~~~

**用法2、链式调用map()方法。消除多重if xxx!=null; 嵌套**
想要实现a、b、c三个变量的加法乘法的组合运算。但是三个变量都有可能为null。所以需要加三层if判断：
~~~
Integer a = getA(); 
if (a != null) {
  Integer b = getB();
  if ( b != null) {
    Integer c = getC();
    if ( c != null) {
      return (a + b) * c;
    } else return null;
  } else return null;
} else return null;

~~~

改写成这样，是不是简洁很多了？
~~~
Optional<Integer> result = Optional.ofNullable(getA())
                             .flatMap(a   -> Optional.ofNullable(getB()).map( b -> a + b ))
                             .flatMap(sum -> Optional.ofNullable(getC()).map( c -> sum * c ))

~~~


**用法3、使用orElse，为null则返回默认值** 
~~~
    static class UserMapper {
        public static BizUser selectBizUserByEmployeeNum(String employeeNum) {
            return null;
        }
    }
    public static Integer run() {
        BizUser user = UserMapper.selectBizUserByEmployeeNum("3306");
        return Optional.ofNullable(user).map(BizUser::getDeptId)
            .filter(deptId -> deptId.intValue() != 0).orElse(1122);

    }
    public static void main(String[] args) {
        Integer run = run();
        System.out.println(run);
    }
~~~

**用法4、使用orElseThrow，为null则抛出异常到上层中断执行**
~~~
    static class UserMapper{
        public static BizUser selectBizUserByEmployeeNum(String employeeNum) {
            return null;
        }
    }
    public static void main(String[] args) {
        BizUser user = UserMapper.selectBizUserByEmployeeNum("3306");
        Optional.ofNullable(user).map(BizUser::getDeptId).filter(deptId -> deptId.intValue() != 0)
            .orElseThrow(() -> new CustomException("查询到的user为空！"));

    }
~~~
**用法5、使用filter完成除非空判断以外的其它判断**
另外，如果你需要对返回值进行判断，比如结果是否大于某个值等，可以使用Optional的filter方法。
~~~
        HashMap<Object, Object> objectObjectHashMap = new HashMap<>();
        objectObjectHashMap.put("name", "kawai");
        objectObjectHashMap.put("age", 19);
        //TODO 使用内部的ifPresent避免了空指针异常
        Object a = Optional.ofNullable(objectObjectHashMap.get("age"))
            .filter(age -> Integer.parseInt(age.toString()) >= 18).orElse(18);
        System.out.println(a);

~~~


###来看看错误用法（滥用Optional）

**错误用法1、把if xx！=null 换成了 name1.isPresent()**
这种方法和if xx！=null 差不多，还有if条件。不好用！把isPresent()当做判断空指针的方法，又回归以前的if嵌套，毫无意义 。 个人觉得isPresent()不应该暴露出来，放在Optional内部使用更好。

~~~
public static void main(String[] args) {
        HashMap<Object, Object> objectObjectHashMap = new HashMap<>();
        objectObjectHashMap.put("name", "小明");
        objectObjectHashMap.put("age", 18);
        Person a = new Person();
        Optional<Object> name1 = Optional.ofNullable(objectObjectHashMap.get("name1"));
        if (name1.isPresent()) {
            a.setName(name1.get().toString().toUpperCase());
        }
        Optional<Object> age = Optional.ofNullable(objectObjectHashMap.get("age1"));
        if (age.isPresent()) {
            a.setAge(Integer.valueOf(age.get().toString()) + 18);
        }
        System.out.println(a);
    }
}
~~~
**错误用法2、这样还是会出现空指针，因为get()后返回的就是裸露的值**
~~~
    public static void main(String[] args) {
        HashMap<Object, Object> objectObjectHashMap = new HashMap<>();
        objectObjectHashMap.put("name", null);
        objectObjectHashMap.put("age", 18);
        Person a = new Person();
        //TODO 下面的语句还是会报空指针NoSuchElementException，get()方法返回的是裸露的值。
        String name = Optional.ofNullable(objectObjectHashMap.get("name")).get().toString()
            .toUpperCase();

        a.setName(name);
        Optional.ofNullable(objectObjectHashMap.get("age"))
            .ifPresent(age -> a.setAge(Integer.valueOf(age.toString()) + 18));
        System.out.println(a);

    }
~~~
>注意：请不要直接使用get()方法获得值，因为它还是会造成空指针。

**错误用法3、被Optional.ofNullable()包装的表达式这样写照样出现空指针**
~~~
Optional.ofNullable(((Integer) null).toString()).orElse("123");
~~~
请使用map()函数把toString()方法单独提出来。
~~~
Optional.ofNullable(((Integer) null)).map(m->m.toString()).orElse("123");
~~~

###orElse和orElseGet有什么区别？

对比下面代码的执行结果：
eg1

~~~
    private static Integer query(){
        System.out.println("查询值");
        return 1122;
    }
    public static void main(String[] args) {
        HashMap<String, Integer> map = new HashMap<>(1);
        map.put("age1",1);
        System.out.println(Optional.ofNullable(map.get("age1")).orElse(query())) ;
    }

~~~
>查询值
1122

eg2
~~~
    private static Integer query(){
        System.out.println("查询值");
        return 1122;
    }
    public static void main(String[] args) {
        HashMap<String, Integer> map = new HashMap<>(1);
        map.put("age1",1);
        System.out.println(Optional.ofNullable(map.get("age1")).orElseGet(()->query())) ;
    }
~~~
>1

显然，当ofNullable内部参数非空时，不会去调用默认值里的方法去获取默认值。这也算是一个优化。若query()方法实现是一个网络请求或者数据库操作这样的耗时操作。那么这里请使用orElseGet而不是orElse！
当然若默认值只是一个常量，那么使用orElse语法更简洁。




###使用注意
**不能使用Optional到java bean的属性中**
由于Optional并没有实现Serializable接口，所以不推荐直接作为pojo字段使用。

**不推荐将方法返回值设置为Optional**
虽然Optional能够防止空指针，有些类里的方法强制把返回值都定为Optional类型。
1、比如java8的stream流api
java.util.stream.Stream
~~~
    Optional<T> max(Comparator<? super T> comparator);
~~~
2、JPA返回值就是Optional。

3、但是我们平时工作还是不用使用他为返回值比较好。作为内部方法的返回值，免去调用时手动包装，但这意味着强制调用者使用Optional，但不是所有人都会用这个东西。

应该把Optional当做一个简单的工具类，是一个纯主观意愿的。想用就用吧，咱也不强制别人用。

###其它三个类OptionalDouble、OptionalInt、OptionalLong
自己用的比较少。
它们的of方法形参是基本类型的，也就是说传null会报空指针：
~~~
    /**
     * Return an {@code OptionalInt} with the specified value present.
     *
     * @param value the value to be present
     * @return an {@code OptionalInt} with the value present
     */
    public static OptionalInt of(int value) {
        return new OptionalInt(value);
    }
~~~

主要了解它们的getAsInt()、getAsDouble()、getAsLong() 方法。
~~~
    public static void main(String[] args) {
        OptionalInt op = OptionalInt.of(0);
        if (op.isPresent()){
            //获得OptionalInt对象里面的值，输出1
            System.out.println(op.getAsInt());
        }
        op.ifPresent((value) -> System.out.println("value：" + value));

        //创建一个空值对象
        OptionalInt opint = OptionalInt.empty();
        if (opint.isPresent()) {
            //和Optional一样，输出No value present
            System.out.println(opint.getAsInt());
        } else {
            //如果没有值，赋初始值
            System.out.println(opint.orElse(222));
            //如果没有值，赋初始函数
            System.out.println(opint.orElseGet(() -> 333));
        }
        //如果没有值则抛出异常
        opint.orElseThrow(NullPointerException::new);

    }
~~~


###实践

1、解析json
~~~

    public static void main(String[] args) {
        String json = "{\n"
            + "    \"responseResult\": {\n"
            + "        \"status\": 0,\n"
            + "        \"msg\": \"成功\"\n"
            + "    },\n"
            + "    \"contents\": {\n"
            + "        \"total\": 1,\n"
            + "        \"currentRowsSize\": 1,\n"
            + "        \"rows\": [\n"
            + "            {\n"
            + "                \"id\": 551,\n"
            + "                \"name\": \"学生二\",\n"
            + "                \"phone\": \"15099955982\"\n"
            + "            }\n"
            + "        ]\n"
            + "    }\n"
            + "}";

        final String[] msg = {""};
        JSONObject jsonObject = JSONObject.parseObject(json);
        Optional.ofNullable(jsonObject)
            .map(m1 -> m1.getJSONObject("responseResult"))
            .filter(m2 -> {
                msg[0] = m2.getString("msg");
                return m2.getInteger("status") == 0;
            })
            .orElseThrow(() -> new RuntimeException(String.format("netca 获取授权list失败，%s", msg[0])));

        JSONArray objects = Optional.ofNullable(jsonObject).map(m -> m.getJSONObject("contents"))
            .map(m -> m.getJSONArray("rows"))
            .orElseThrow(() -> new RuntimeException("netca 获取授权list失败，miss contents.rows"));

        System.out.println(objects);

    }
~~~

2、下面demo展示如何在流获取时兼顾多个字段。这里有：m.getString("msg")和 m.getInteger("status")
在map内部得到json返回值的msg字段，并见它赋值给 msg[0]。随后在Throw Exception中用到。


> 还有可以注意的是判断json返回状态码的写法
~~~
        jsonObject = Optional.ofNullable(JSON.parseObject(respResult))
            .map(m -> m.getJSONObject("responseResult")).map(m -> {
                msg[0] = m.getString("msg");
                return m;
            })
            .filter(m -> m.getInteger("status") == 0)
            .orElseThrow(
                () -> new CloudsignException(-15,
                    String.format("netca授权签名获得授权人userToken失败,%s", msg[0])));
~~~




3、Optional.map()，只能一条路走到黑，顶多使用 m->{return m } 获取同级别的节点。但是绝对不能回头。如果想走两条路，那么请用两个 Optional.ofNullable。暂时我也没找到更好的办法。
下面有两条路。一条路拿responseResult.status/responseResult.msg；一条路拿contents.signCert；
所以用了两次 `Optional.ofNullable`
~~~
        JSONObject jsonObject = JSONObject.parseObject(respResult);
        Optional.ofNullable(jsonObject)
            .map(m -> m.getJSONObject("responseResult")).map(m -> {
                msg[0] = m.getString("msg");
                return m;
            })
            .filter(m -> m.getInteger("status") == 0).orElseThrow(
                () -> new CloudsignException(-12,
                    String.format("netca 获取base64cert失败,%s", msg[0])));

        String signCert = Optional
            .ofNullable(jsonObject)
            .map(m -> m.getJSONArray("contents")).map(m -> m.getJSONObject(0))
            .map(m -> m.getString("signCert"))
            .orElseThrow(
                () -> new CloudsignException(-13, "netca 获取base64cert失败，miss contents.signCert"));

~~~

4、
~~~
    public static String getDescByCode(Integer code, UserEnum userEnum) {

        final Map<Integer, SignedReturnOption> all = getAll();
        if (all.keySet().contains(code)) {
            final SignedReturnOption signedReturnOption = all.get(code);
            return Optional.ofNullable(signedReturnOption).map(m -> m.userEnum.equals(userEnum) ? signedReturnOption.desc : Constant.NOT_ME).orElse(null);

        }
        return null;
    }
~~~
