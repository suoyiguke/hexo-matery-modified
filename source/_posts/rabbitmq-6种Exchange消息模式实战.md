---
title: rabbitmq-6种Exchange消息模式实战.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mq
categories: mq
---
---
title: rabbitmq-6种Exchange消息模式实战.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mq
categories: mq
---


###1、简单模式Simple
![在这里插入图片描述](https://upload-images.jianshu.io/upload_images/13965490-73addf515868e1cc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###2、工作模式Work
>topic 模式多个消费者对一个队列，不可以重复消费；消费者定义是一样的。会轮训消费者list进行消费 `相同的队列，相同的交换机`
![在这里插入图片描述](https://upload-images.jianshu.io/upload_images/13965490-4d8e4b6eb17870a5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

消费者
~~~

    /**
     * 若存在多个消费者，则queue名必须唯一（若queue名相同则只有一个消费者能收到消息）
     * exchange需与生产者定义的exchange保持一致
     * routing key根据需要，若生产者发送多种消息，则可以使用*或#通配符
     */
    @RabbitHandler
    @RabbitListener(
            bindings = @QueueBinding(
                    value = @Queue(value = "MyQueue", autoDelete = "true"),
                    exchange = @Exchange(value = "MyExchange2", type = ExchangeTypes.TOPIC)
            )
    )
    public void handleMessageA(Message message, Channel channel) {
        System.out.println(Thread.currentThread().getName());

        String s = new String(message.getBody());
        System.out.println(s);
    }
    @RabbitHandler
    @RabbitListener(
            bindings = @QueueBinding(
                    value = @Queue(value = "MyQueue", autoDelete = "true"),
                    exchange = @Exchange(value = "MyExchange2", type = ExchangeTypes.TOPIC)
            )
    )
    public void handleMessageB(Message message, Channel channel) {
        System.out.println(Thread.currentThread().getName());

        String s = new String(message.getBody());
        System.out.println(s);
    }
~~~
生产者，指定exchange，routingKey设置为空字符串
~~~
 rabbitTemplate.send("MyExchange2","", message1);
~~~



###3、发布订阅模式Publish/Subscribe
> 多个消费者之间可以重复消费; `不同的队列，相同的交换机`
![在这里插入图片描述](https://upload-images.jianshu.io/upload_images/13965490-f0a9b0cc89acbf5f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

生产者
>这里指定routingKey 为"" 空字符串
~~~
 rabbitTemplate.send("MyExchange","", message1);
~~~


消费者
~~~

    @RabbitHandler
    @RabbitListener(
            bindings = @QueueBinding(
                    value = @Queue(value = "handleMessageA", autoDelete = "true"),
                    exchange = @Exchange(value = "MyExchange", type = ExchangeTypes.FANOUT)
            )
    )
    public void handleMessageA(Message message, Channel channel) {

        String s = new String(message.getBody());
        System.out.println(s);
    }

    @RabbitHandler
    @RabbitListener(
            bindings = @QueueBinding(
                    value = @Queue(value = "handleMessageB", autoDelete = "true"),
                    exchange = @Exchange(value = "MyExchange", type = ExchangeTypes.FANOUT)
            )
    )
    public void handleMessageB(Message message, Channel channel) {
        String s = new String(message.getBody());
        System.out.println(s);
    }
~~~


4、路由模式Routing
![在这里插入图片描述](https://upload-images.jianshu.io/upload_images/13965490-d3b269f690d78b30.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

路由模式需要指定接收队列的名称，而统配模式可以认为是路由模式的扩展，支持队列名称的匹配模式。




5、通配符模式Topics
![在这里插入图片描述](https://upload-images.jianshu.io/upload_images/13965490-48aff99760f5b7ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

6、远程调用模式RPC


