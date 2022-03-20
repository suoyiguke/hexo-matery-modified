---
title: sqlalchemy笔记一：进行原生sql的增删改查.md
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
title: sqlalchemy笔记一：进行原生sql的增删改查.md
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
### pip安装sqlalchemy和pymysql
pip install sqlalchemy
pip install pymysql
![image.png](https://upload-images.jianshu.io/upload_images/13965490-dccafb9859825178.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>这个pymysql好像没用到，但是不安装它程序就报错


###创建表
~~~
CREATE TABLE `sqlalchemy_test`.`user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `age` int(4) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;
~~~
###数据准备
~~~
INSERT INTO `sqlalchemy_test`.`user`(`id`, `username`, `age`) VALUES (2, 'yin.kai', 23);
INSERT INTO `sqlalchemy_test`.`user`(`id`, `username`, `age`) VALUES (3, 'hello word', 24);
INSERT INTO `sqlalchemy_test`.`user`(`id`, `username`, `age`) VALUES (4, 'wudi', 25);

~~~
###sqlalchemy进行原生sql的增删改查
~~~
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

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



# 插入一条入口
def create_one(id, username, age):
    execute = _instance.execute("INSERT INTO `user`(`id`, `username`, `age`) VALUES (%(id)s, %(username)s,%(age)s);",
                                id=id, username=username, age=age)
    execute.close()

# 查询所有
def selectAll():
    execute = _instance.execute("SELECT * FROM user;")
    list = execute.fetchall()
    execute.close()
    return list

# 根据id查询
def selectById(id):
    execute = _instance.execute("SELECT * FROM user WHERE id = %(id)s;",id=id)
    user = execute.first()
    execute.close();
    return user


# 修改
def updateById(id,username,age):
    execute = _instance.execute("UPDATE `user` SET `username` = %(username)s, `age` = %(age)s WHERE `id` = %(id)s;",username=username,age=age,id=id)
    execute.close()

# 删除
def deleteById(id):
    execute = _instance.execute("DELETE FROM user WHERE id = %(id)s",id=id)
    execute.close()

# 测试
if __name__ == '__main__':

    # 插入一条数据
    create_one(5, 'wudi', 25)

    #根据id查询
    user = selectById(5)
    for key, value in user.items():
        print(str(key) + " ===> " + str(value))


    #修改
    updateById(5,'update ok',11)

    #删除
    deleteById(5)


    #查询
    select_list = selectAll()
    for user in select_list:
        for key,value in user.items():
            print(str(key)+" ===> "+ str(value))
~~~
