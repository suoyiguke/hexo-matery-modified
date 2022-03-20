---
title: kafka-三种生产信息的方式：同步生产、异步生产和-oneway.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mq-kafka
categories: mq-kafka
---
---
title: kafka-三种生产信息的方式：同步生产、异步生产和-oneway.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mq-kafka
categories: mq-kafka
---
同步；
get()方法会让当前线程阻塞，直到有回调结果时才继续执行。
~~~
    @Resource
    private KafkaTemplate<Object, Object> kafkaTemplate;

    @GetMapping("/testSyncSend")
    public void testSyncSend() {
        int id = (int) (System.currentTimeMillis() / 1000);
        Demo01Message message = new Demo01Message();
        message.setId(id);
        // 同步发送消息
        SendResult<Object, Object> sendResult = null;
        try {
            sendResult = kafkaTemplate
                .send(Demo01Message.TOPIC, message).get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        logger.info("同步收到结果", id, sendResult);

    }

  


~~~

异步；
addCallback()方法传入ListenableFutureCallback接口实例。实现两个回调。
~~~
   @Resource
   private KafkaTemplate<Object, Object> kafkaTemplate;
   @GetMapping("/testASyncSend")
   public void testASyncSend() {
        int id = (int) (System.currentTimeMillis() / 1000);
        Demo01Message message = new Demo01Message();
        message.setId(id);
        // 异步发送消息
        kafkaTemplate.send(Demo01Message.TOPIC, message).addCallback(
            new ListenableFutureCallback<SendResult<Object, Object>>() {
                @Override
                public void onFailure(Throwable e) {
                    logger.error("异步生产失败回调", e);
                }

                @Override
                public void onSuccess(SendResult<Object, Object> result) {
                    logger.info("异步生产回调成功");
                    logger.info("id={},result={}", id, result);
                }
            });
    }
~~~

###oneway 

