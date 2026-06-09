---
date: 2020-03-08T18:01:00+00:00
title: Python学习笔记（常用扩展）
slug: pythonxuexibijichangyongkuozhan
#description: Python常用扩展使用笔记，包括mysql连接池Excel
tags: ["python"]
categories: ["后端"]
featured: false
draft: false
excerpt: Python常用扩展使用笔记，包括mysql连接池Excel日志等。数据库连接池importpymysqlfromtwisted.enterpriseimportadbapifrompymysqlim
---

![python](./15201244.png)



Python常用扩展使用笔记，包括mysql连接池、Excel、日志等。





<!--more-->





### 数据库连接池



```

import pymysql

from twisted.enterprise import adbapi

from pymysql import cursors



# 连接池方式保存数据库

class JianshuTwistedPipeline(object):



    def __init__(self):

        dbparams = {

            'host': '127.0.0.1',

            'port': 3306,

            'user': 'root',

            'password': '',

            'database': 'python',

            'charset': 'utf8',

            'cursorclass': cursors.DictCursor

        }

        # 建立连接池

        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)



    # 插入数据

    def insert_item(self, cursor, item):



        sql = """INSERT INTO jianshu(article_id,article_title,article_content,origin_url) VALUES (%s, %s, %s, %s)"""



        # 游标执行sql

        cursor.execute(sql, (item['article_id'],item['article_title'],item['article_content'], item['origin_url']))



    # 异常处理

    def handle_error(self, error, item, spider):

        print('**********error**********')

        print(error)



    # 执行

    def process_item(self, item, spider):

        # 运行

        defer = self.dbpool.runInteraction(self.insert_item, item)



        # 增加异常处理函数

        defer.addErrback(self.handle_error, item, spider)



        return item

```



### 日志

```



import logging



self.logger = logging.getLogger('jianshuspider')



handle = logging.FileHandler('log.txt')



self.logger.addHandler(handle)



self.logger.info()

```



### pyexcel

```

import pyexcel



pyexcel.save_as(data, 'xxx.xls')

```



### html读入可以xpath操作



```

# 打开一个文件

f = open('xxx.html')



# 文件内容赋值给一个变量

text = f.read()



# 引入包

import lxml import etree



# 用html方式读取内容

selector = etree.HTML(text)



# xpath规则

selector.xpath('****')

```



### urllib库



```

from urllib import request



# r = request.urlopen('https://www.amazon.com/product-reviews/B07211W6X2?sortBy=recent&filterByStar=three_star')



r = request.urlopen('https://www.baidu.com')



print(r.read())

```



- `read()` 读取全部

- `readline()` 读取一行

- `readlines()` 每行以列表数组的形式展示

- `getcode()` 获取状态码



#### urlretrieve

`urlretrieve(url, filename)`指定url并保存到本地



#### url编码解码



`urlencode` 对数据编码



`parse_qs` 对数据解码



```

from urllib import parse



params = {'name': '王二小', 'age': 19}



# 编码

res = parse.urlencode(params)



print(res)



# 解码

res = parse.parse_qs(res)



print(res)

```



#### url拆分



- `parse.urlparse`

- `parse.urlsplit`



urlparse与urlsplit区别是：urlparse解析会有一个params的参数，urlsplit则没有



#### parsel

```

import parsel



response = requests.get(url, proxies=proxy, headers=headers)



selector = parsel.Selector(response.text)



selector.xpath()

```



### celery



```

celery -A app.celeries.listing_celery worker -l info -P eventlet



# centos后台运行

nohup celery -A app.celeries.listing_celery worker -l info &

```





### gunicorn 

```

gunicorn -b 0.0.0.0:5000 api:app



gunicorn -w 4 -b 0.0.0.0:5000 --threads 16 -k gevent -t 1000 --access-logfile ./log/gun.log -D api:app

```
