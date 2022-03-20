---
title: sqlalchemy笔记二：进行ORM的增删改查.md
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
title: sqlalchemy笔记二：进行ORM的增删改查.md
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

from sqlalchemy import create_engine, Column, Integer, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
# 定义实体
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    age = Column(Integer)


    # # 構造函數
    def __init__(self, id,username,age):
        self.id = id
        self.username = username
        self.age = age

    def __str__(self):
        return 'id: %d 姓名：%s  年龄：%d' % (self.id,self.username, self.age)


_instance = create_engine(
    'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(user='root', password='123456',
                                                                        host='localhost',
                                                                        port='3306',
                                                                        database='sqlalchemy_test'),
    max_overflow=int(1),  # 超过连接池大小外最多创建的连接
    pool_size=int(5),  # 连接池大小,默认是5
    pool_timeout=int(1),  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=int(0)  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)


def getSession():
    DBsession = sessionmaker(bind=_instance)
    session = DBsession()
    return session




# 插入一条入口
def create_one(user):
    session = getSession()
    session.add(user)
    session.commit()

# 根据id查询
def selectById(id):
    session = getSession()
    user = session.query(User).filter(User.id == id).one()
    return user


# 查询所有
def selectAll():
    session = getSession()
    user__all = session.query(User).all()
    return user__all

# 修改
def updateById(id,username,age):
    session = getSession()
    user = session.query(User).filter(User.id == id).first()
    # 在内存中修改
    user.username = username
    user.age = age
    # 持久化到库中
    session.commit()



# 删除
def deleteById(id):
    session = getSession()
    session.query(User).filter(User.id == id).delete()
    session.commit()


if __name__ == '__main__':

    # 插入一条数据
    user = User(12, '123',18)
    create_one(user)

    #根据id查询
    user = selectById(12)
    print(user)


    #修改
    updateById(12,'update ok',11)

    #删除
    deleteById(12)


    #查询
    select_list = selectAll()
    for user in select_list:
        print(user)
~~~
