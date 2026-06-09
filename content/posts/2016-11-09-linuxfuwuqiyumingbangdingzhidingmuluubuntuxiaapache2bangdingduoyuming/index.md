---
date: 2016-11-09T20:24:00+00:00
categories: ["后端"]
title: Linux服务器域名绑定指定目录(ubuntu下apache2绑定多域名)
slug: linuxfuwuqiyumingbangdingzhidingmuluubuntuxiaapache2bangdingduoyuming
#description: nbspnbspnbspnbsp前阵子买了域名，好不容易等到
tags: ["apache2", "linux", "域名绑定"]
featured: false
draft: false
excerpt: nbspnbspnbspnbsp前阵子买了域名，好不容易等到管局审核通过，结果在域名绑定到服务器上的时候又出现了些许问题，百度无果，无奈之下请教了大神，弄通了软硬链接，了解了apache2的目录结构及
---

&nbsp;&nbsp;&nbsp;&nbsp;前阵子买了域名，好不容易等到管局审核通过，结果在域名绑定到服务器上的时候又出现了些许问题，百度无果，无奈之下请教了大神，弄通了软、硬链接，了解了apache2的目录结构及特性，才得以解决。





<!--more-->



## 前言 ##

&nbsp;&nbsp;&nbsp;&nbsp;自己的服务器是通用的文件结构，一键安装的**lamp**集成环境，具体是什么，不记得了，遇到问题的时候就去百度，网上大多数说的是和**window**下配置虚拟域名的方法是差不多的，但是我的服务器是**apache2**的，没有httpd.conf这个文件，因为第一次弄这个，所以有点难办。但值得庆幸的是，最后还是搞定了。此文就简单介绍下，我遇到的问题及解决方法.



## 几个知识点 ##

### 软链接和硬链接 ###

#### 简介 ####

&nbsp;&nbsp;&nbsp;&nbsp;**软链接**文件有点像`Windows`的快捷方式。它实际上是一个特殊的文件。在符号连接中，文件实际上是一个文本文件，其中包含的有另一文件的位置信息。

&nbsp;&nbsp;&nbsp;&nbsp;**硬连接**是指通过索引节点来进行连接。在`Linux`的文件系统中，保存在磁盘分区中的文件不管是什么类型都给它分配一个编号，称为索引节点号(`Inode Index`)。在`Linux`中，多个文件名指向同一索引节点是存在的。硬连接的作用是允许一个文件拥有多个有效路径名，这样用户就可以建立硬连接到重要文件，以防止“误删”的功能。



#### 命令参数 ####

必要参数:

````

ln -b 删除，覆盖以前建立的链接

ln -d 允许超级用户制作目录的硬链接

ln -f 强制执行

ln -i 交互模式，文件存在则提示用户是否覆盖

ln -n 把符号链接视为一般目录

ln -s 软链接(符号链接)

ln -v 显示详细的处理过程

````



#### 特点 ####

软链接

 1. 以路径的形式存在，类似于Windows操作系统中的快捷方式

 2. 跨文件系统 

 3. 对一个不存在的文件名进行链接

 4. 对目录进行链接

 5. 保持每一处链接文件的同步性



硬链接



 1. 以文件副本的形式存在，但不占用实际空间

 2. 不允许给目录创建硬链接

 3. 硬链接只有在同一个文件系统中才能创建

 4. 保持每一处链接文件的同步性





#### 注意 ####



 1. `ln命令`会保持每一处链接文件的同步性，也就是说，不论改动了哪一处，其它的文件都会发生相同的变化

 2. `ln的链接`又分软链接和硬链接两种，软链接就是**ln –s 源文件 目标文件**，它只会在你选定的位置上生成一个文件的镜像，不会占用磁盘空间，硬链接 **ln 源文件 目标文件**，没有参数-s， 它会在你选定的位置上生成一个和源文件大小相同的文件，无论是软链接还是硬链接，文件都保持同步变化。



### apache2目录结构 ###

 ![apache2目录结构](http://cxiansheng.cn/usr/uploads/2016/11/2103702455.jpg)





 * `apache2.conf` `apache`配置文件

 * `conf-available、conf-enabled` `apache`配置目录

 * `sites-available、sites-enabled` `apache`配置域名站点目录

 * `mods-available、mods-enabled` `apache`功能模块目录

 * `ports.conf` `apache`配置端口





## 多域名绑定实现 ##

&nbsp;&nbsp;&nbsp;&nbsp;假设绑定`cxiansheng.cn`和`demo.cxiansheng.cn`到服务器上

### 准备工作 ###



 - 将`https://www.cxiansheng.cn` 与 `http://www.demo.cxiansheng.cn` 的DNS解析到服务器IP上。

 - 在`/etc/apache2/sites-available/`目录，创建2个文件,文件名分别用`cxiansheng.conf`和 `demo.conf`

### 配置文件 ###

在`cxiansheng.conf`文件中输入以下内容(**不要真的自己输入啊喂！~**)

```

<VirtualHost *:80>

 	 ServerAdmin webmaster@localhost

	 ServerName cxiansheng.cn

	 DocumentRoot /var/www/cxiansheng

	 <Directory />

		 Options FollowSymLinks

	 	 DirectoryIndex index.php index.html index.htm

 		 AllowOverride None

	 </Directory>

	 <Directory /var/www/cxiansheng>  

		# Options Indexes FollowSymLinks MultiViews

		Options FollowSymLinks

		RewriteEngine On

		RewriteCond %{REQUEST_FILENAME} !-f

		RewriteCond %{REQUEST_FILENAME} !-d

		RewriteRule . index.php

  		AllowOverride All

		Order allow,deny

		allow from all

	</Directory>



	ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/

	<Directory "/usr/lib/cgi-bin">

		AllowOverride None

		Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch

		Order allow,deny

		Allow from all

	</Directory>



	ErrorLog ${APACHE_LOG_DIR}/error.log



	# Possible values include: debug, info, notice, warn, error, crit,

	# alert, emerg.

	LogLevel warn



	CustomLog ${APACHE_LOG_DIR}/access.log combined



	Alias /doc/ "/usr/share/doc/"

	<Directory "/usr/share/doc/">

		Options Indexes MultiViews FollowSymLinks

		AllowOverride None

		Order deny,allow

		Deny from all

		Allow from 127.0.0.0/255.0.0.0 ::1/128

	</Directory>

</VirtualHost>

```

#### 提示 ####

 - `ServerName` 后面输入域名



 - `DocumentRoot`  写目录在服务器相对路径



 - `Directory` 第二段的这里也要写目录的相对路径



 - `demo.conf`  同上，修改相应的位置即可



### 建立软链接 ###

&nbsp;&nbsp;&nbsp;&nbsp;在`/etc/apache2/sites_enabled/`中创建`ln`链接：

```

ln -s /etc/apache2/sites-available/cxiansheng.conf /etc/apache2/sites-enabled/cxiansheng.conf

ln -s /etc/apache2/sites-available/demo.conf /etc/apache2/sites-enabled/demo.conf

```

### 重启apache ###



    /etc/init.d/apache2 restart



### 输入网址 ###

![链接成功](http://cxiansheng.cn/usr/uploads/2016/11/3543322545.jpg)



## 总结 ##

&nbsp;&nbsp;&nbsp;&nbsp;linux系统是个`big guy`，要快速入坑才行啊！！！



## 资源 ##

 1. [硬链接和软连接][3]
