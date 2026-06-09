---
date: 2019-09-12T15:52:00+00:00
categories: ["其他", "后端"]
title: "【转】centos通过yum源快速搭建lnmp环境"
slug: zhuancentostongguoyumyuankuaisudajianlnmphuanjing
#description: 原文地址LinuxCentOS7下安装LNMP环境笔记ncs
tags: ["centos", "lnmp", "php环境"]
featured: false
draft: false
excerpt: 原文地址LinuxCentOS7下安装LNMP环境笔记ncsb11.设置yum源PHP源官方地址httpswebtatic.com2mysql源官方地址httpsdev.mysql.comdownlo
---

> 原文地址：[Linux-CentOS7下安装LNMP环境笔记--ncsb][1]



## 1. 设置yum源



PHP源官方地址: [https://webtatic.com/][2]



mysql源官方地址: [https://dev.mysql.com/downloads/repo/yum/][3]



```

rpm -Uvh https://dl.Fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm



rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm



rpm -Uvh  http://dev.mysql.com/get/mysql57-community-release-el7-9.noarch.rpm

```





<!--more-->





## 2.安装nginx1.1 php7.1 mysql5.7



安装之前先



清除yum缓存： `yum clean all`

生成yum缓存 ： `yum makecache`



```

// 安装nginx

yum -y install nginx



// 安装mysql

yum -y install mysql-community-server



// 安装php

yum -y install php71w-devel php71w php71w-cli php71w-common php71w-gd php71w-ldap php71w-mbstring php71w-mcrypt  php71w-pdo  php71w-mysqlnd  php71w-fpm php71w-opcache php71w-pecl-redis  php71w-bcmath

```





## 3.启动软件

```

systemctl start nginx



systemctl start mysql  |  systemctl start mysqld



systemctl start php-fpm

```



具体的nginx，php-fpm的配置这里省略，下面只重点说一下mysql的配置



### mysql5.7 初始密码获取



启动mysql之后，通过命令 `grep 'temporary password' /var/log/mysqld.log` 可以拿到root用户的初始密码



### 修改初始密码

root用户首次登录mysql是需要修改初始密码才能进行后续的操作的,初始密码必须包括数字、大小写字母且长度不能小于8位

```

set password = password('ryUl1_33au_n0krQ')

```

### 创建用户且授权



下面命令会自动创建dbsb用户且授权db_sb库的所有表的权限



```

grant all privileges on db_sb.* to "dbsb"@"%" identified by "ryUl1_33au_n0krQ"

```





## 4.设置开机自启动

```

systemctl enable mysqld



systemctl enable nginx



systemctl enable php-fpm

```

Created symlink from /etc/systemd/system/multi-user.target.wants/nginx.service to /usr/lib/systemd/system/nginx.service.





查看软件安装相关目录或者文件：　　 `rpm nginx -ql`



## 5.结

以上都是在关闭了系统的防火墙和selinux下操作的
