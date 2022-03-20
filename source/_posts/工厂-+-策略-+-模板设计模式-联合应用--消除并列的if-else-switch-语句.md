---
title: 工厂-+-策略-+-模板设计模式-联合应用--消除并列的if-else-switch-语句.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 设计模式
categories: 设计模式
---
---
title: 工厂-+-策略-+-模板设计模式-联合应用--消除并列的if-else-switch-语句.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 设计模式
categories: 设计模式
---
有下面代码，name取值不同时走不同逻辑。这样并列的if-else一多是不是代码就显得臃肿？我们来使用工厂 + 策略 + 模板设计模式消除它
~~~
	@Test
	String noDesign2() {
		String name = "张三";

		if (name.equals("张三")) {

			// 业务逻辑B
			return "张三完成任务BBB";

		} else if (name.equals("李四")) {

			// 业务逻辑B
			return "李四完成任务BBB";

		} else if (name.equals("王五")) {

			// 业务逻辑B
			return "王五完成任务BBB";

		} else if (name.equals("赵六")) {

			// 业务逻辑A
			System.out.println("赵六完成任务AAA");

		} else if (name.equals("田七")) {

			// 业务逻辑A
			System.out.println("田七完成任务AAA");

		} else if (name.equals("亢八")) {

			// 业务逻辑A
			System.out.println("亢八完成任务AAA");

		}
		return "end";
	}
~~~
1、工厂类，定义一个Map。key存入条件标识，value存入Handler 
~~~
/**
 * 工厂设计模式
 */
public class Factory {
    private static Map<String, Handler> strategyMap = Maps.newHashMap();

    public static Handler getInvokeStrategy(String name) {
        return strategyMap.get(name);
    }

    public static void register(String name, Handler handler) {
        if (StringUtils.isEmpty(name) || null == handler) {
            return;
        }
        strategyMap.put(name, handler);
    }
}

~~~

2、定义抽象类 AbstractHandler。里面实现下AAA、BBB方法。不支持的方法抛出UnsupportedOperationException异常；
实现InitializingBean接口，那么继承AbstractHandler的类就必须实现afterPropertiesSet方法
~~~
/**
 * 模板方法设计模式
 */
public abstract class AbstractHandler implements InitializingBean {

    public void AAA(String name) {
        throw new UnsupportedOperationException();
    }

    public String BBB(String name) {
        throw new UnsupportedOperationException();
    }

    public String say() {
        throw new UnsupportedOperationException();
    }
}
~~~

3、定义逻辑类ZhangSanHandler2、LiSiHandler2.... 每一个这种类就代表一种if下面的业务逻辑代码；
afterPropertiesSet方法会在spring加载后执行，将自身判断标识和实例都设置到Map中。
~~~
@Component
public class YkHandler extends AbstractHandler {

    @Override
    public String say() {
        System.out.println("我定义的方法");
        return "my";
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        Factory2.register("yk", this);
    }
}
~~~


4、测试代码
~~~

	// 工厂 + 策略 + 模板设计模式
	@Test
	void design2() {
		String name = "李四";
		AbstractHandler strategy = Factory2.getInvokeStrategy(name);
		if(ObjectUtils.isEmpty(strategy)){
			System.out.println("没找到条件对应的业务逻辑");
		}
		try {
			strategy.AAA(name);
		}catch (Exception e ){
			System.out.println(e.toString());
		}
		String str = strategy.BBB(name);
		System.out.println(str);
	}
~~~
