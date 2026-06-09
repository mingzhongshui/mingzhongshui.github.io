---
date: 2016-10-19T15:56:00+00:00
categories: ["后端"]
title: windows下批处理定时备份MySql数据库
slug: windowsxiapichulidingshibeifenmysqlshujuku
#description: nbspnbspnbspnbsp数据库是我们项目的一个存储器
tags: ["mysql", "windows定时任务", "批处理"]
featured: false
draft: false
excerpt: nbspnbspnbspnbsp数据库是我们项目的一个存储器，我们项目中绝大多数信息都会保存在数据库中，如果我们的数据库某一天遭到破坏了，如何解决和恢复？这时候我们就要用到批处理定时任务了，在每天某一
---

&nbsp;&nbsp;&nbsp;&nbsp;数据库是我们项目的一个存储器，我们项目中绝大多数信息都会保存在数据库中，如果我们的数据库某一天遭到破坏了，如何解决和恢复？这时候我们就要用到批处理+定时任务了，在每天某一个时间段自动备份数据库信息。





<!--more-->



## 写在前面 ##



&nbsp;&nbsp;&nbsp;&nbsp;本文用到的就是windows系统下的，定时任务+批处理。





## 批处理 ##

```

@echo off

set "Ymd=%date:~,4%%date:~5,2%%date:~8,2%"  //设置Ymd变量的值(当天日期)

mkdir E:\crontab\mysql\sql\%Ymd%            //创建Ymd的值为文件名

D:\wamp\bin\mysql\mysql5.5.24\bin\mysqldump --opt -u root --password=123456 anna > E:\crontab\mysql\sql\%Ymd%\anna.sql         //利用mysqldump导出数据库信息

@echo on

```



## 创建定时任务 ##



### 新建任务 ###

&nbsp;&nbsp;&nbsp;&nbsp;定时任务在win图标，附件->系统工具->定时任务

![打开定时.png](http://cxiansheng.cn/usr/uploads/2016/10/1504715844.png)





![XBN56X2(Z435C8$~F~IFQFN.png](http://cxiansheng.cn/usr/uploads/2016/10/612270033.png)



### 常规 ###



![常规.png](http://cxiansheng.cn/usr/uploads/2016/10/3476344242.png)



### 触发器 ###



![触发器.png](http://cxiansheng.cn/usr/uploads/2016/10/197817638.png)



### 操作 ###



![操作.png](http://cxiansheng.cn/usr/uploads/2016/10/3554479068.png)



### 填写管理员密码 ###

&nbsp;&nbsp;&nbsp;&nbsp;后面两项条件和设置，根据需求填写，这里略过。然后点击确定，会弹出一个填写管理员密码的对话框，填入，确定，任务创建成功



![输入密码.png](http://cxiansheng.cn/usr/uploads/2016/10/343284940.png)



### 查看定时任务 ###

&nbsp;&nbsp;&nbsp;&nbsp;回到定时任务主页，打开`任务计划程序库`，便可以找到自己新建的定时任务



![任务计划程序库2.png](http://cxiansheng.cn/usr/uploads/2016/10/1478568755.png)



## 启动测试 ##

&nbsp;&nbsp;&nbsp;&nbsp;如果想看任务是否能运行，可以采用手动启动的方法进行测试，看对应的文件夹下有没有生成文件



 1. 任务计划程序库，运行



![任务计划程序库3.png](http://cxiansheng.cn/usr/uploads/2016/10/1261784752.png)



 2. .bat文件运行

&nbsp;&nbsp;&nbsp;&nbsp;找到.bat文件，双击，查看生成文件目录

![展示.png](http://cxiansheng.cn/usr/uploads/2016/10/1998409220.png)





## 总结 ##



 1. 写批处理脚本的时候一定要注意，稍微一个不小心写错字符都可能造成批处理执行失败

 2. 这只是一个简单的批处理任务，留作记录，以备不时之需。
