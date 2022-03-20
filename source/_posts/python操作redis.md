---
title: python操作redis.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
---
title: python操作redis.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
~~~
import redis


class TestRedis(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='192.168.10.104',port=6379, db=2,password='123456')

    # String Key

    def  test_set(self):
        """set -- 设置单个键值"""
        rest = self.r.set('user1', 'Amy')
        return rest # 返回True or Flase

    def test_get(self):
        """get -- 获取单个键值"""
        rest = self.r.get('user1')
        return rest

    def test_mset(self):
        """mset -- 设置多个键值 ,传入dict"""
        d = {
            'user2': 'James',
            'user3': 'Sakura',
            'user4': 'Gaara'
        }
        rest = self.r.mset(d)
        return rest # 返回True or Flase

    def test_mget(self):
        """mget -- 获取多个键值,传入list或者tuple"""
        t=('user2', 'user3', 'user4')
        rest = self.r.mget(t)
        return rest

    def test_del(self):
        """del -- 删除单个键值"""
        rest = self.r.delete(('user1'))
        return rest # 返回1 or 0

    def test_incr(self):
        """incr -- 键值增加1"""
        self.r.set('age1',33)
        rest = self.r.incr('age1')
        return rest # 但会增加后键值结果

    # List
    def test_push(self):
        """lpush/rpush -- 从左/右插入数据 names1:['Amy', 'Jhon]"""
        # rest = self.r.lpush('names1', 'Amy', 'Jhon')
        t = ('Amy1', 'Jhon1')
        rest = self.r.lpush('names1', *t)
        return rest

    def test_lrange(self):
        """lrange -- 查询List"""
        rest = self.r.lrange('names1', 0, -1)
        return rest

    def test_pop(self):
        """lpop/rpop -- 删除最左/右边的元素，并返回该元素"""
        rest = self.r.lpop('names1')
        return rest

    # Set
    def  test_sadd(self):
        """sadd -- 添加元素 zoo1:{'Dog', 'Cat'}"""
        # return self.r.sadd('zoo1', 'Cat', 'Dog', 'Cat1', 'Dog1', 'Cat2', 'Dog2')    # 返回添加元素数
        t = ('Cat', 'Dog', 'Cat1', 'Dog1', 'Cat2', 'Dog2')
        return self.r.sadd('zoo2', *t)


    def test_smembers(self):
        """smembers -- 查询元素"""
        return self.r.smembers('zoo2')

    def test_srem(self):
        """ srem 删除元素"""
        # return self.r.srem('zoo1', 'Dog2', 'Dog1')   # 返回删除元素数
        list = ['Dog2', 'Dog1']
        return self.r.srem('zoo2', *list)

    def test_sinter(self):
        """ sinter集合交集"""
        return self.r.sinter('zoo1', 'zoo2')    # 返回集合交集


    def test_sunion(self):
        """sunion集合并集"""
        arg = ['zoo1', 'zoo2']
        return self.r.sunion(*arg)    # 返回集合并集

    def test_sdiff(self):
        """ sdiff 返回集合直接与其他集合的差异"""
        return self.r.sdiff('zoo1', 'zoo2') # 返回 zoo1中zoo2没有的集合

    # Hash 散列
    def test_hset(self):
        """hset 设置散列"""
        return self.r.hset('news:id_001', 'title', 'The News!') # 返回0/1

    def test_hget(self):
        """hget 获取散列结果,hexists 判断是否有键值"""
        if self.r.hexists('news:id_001', 'title'):
            return self.r.hget('news:id_001', 'title')  # 返回结果

    def test_hmset(self):
        """hmset 设置散列"""
        m = {
            'title': 'The News1 !',
            'content': 'The News1 content',
            'aurth': 'Sakura'
        }
        return self.r.hmset('news:id_0002',m)   # 返回True or False

    def test_hmget(self):
        """hmget 获取散列"""
        return self.r.hmget('news:id_0002', 'title', 'content') # 返回List

    def test_hvals(self):
        """hvals获取散列"""
        if self.r.hkeys('news:id_0002'):    # hkeys：如果散列存在
            return self.r.hvals('news:id_0002') # 返回List


if __name__ == "__main__":
    obj = TestRedis()
    # obj.test_sadd()
    #String Key
    print(obj.test_set())
    # print(obj.test_get())
    # print(obj.test_mset())
    # print(obj.test_mget())
    # print(obj.test_del())
    # print(obj.test_incr())
    #
    # #List
    # print(obj.test_push())
    # print(obj.test_lrange())
    # print(obj.test_pop())
    #
    # #Set
    # print(obj.test_sadd())
    # print(obj.test_smembers())
    # print(obj.test_srem())
    # print(obj.test_sinter())
    # print(obj.test_sunion())
    # print(obj.test_sdiff())
    #
    # #Hash
    # print(obj.test_hset())
    # print(obj.test_hget())
    # print(obj.test_hmset())
    # print(obj.test_hmget())
    # print(obj.test_hvals())

~~~
