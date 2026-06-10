---
date: 2020-03-09T20:33:00+00:00
categories: ["后端"]
title: Python爬虫研究
slug: pythonpachongyanjiu
#description: 最近一直在研究爬虫相关的内容，对于各个知识点，都有所实践，以
tags: ["python", "反爬", "爬虫"]
featured: false
draft: false
excerpt: 最近一直在研究爬虫相关的内容，对于各个知识点，都有所实践，以下是研究的结果。反爬虫常见套路1.判断useragent2.校验referer头3.校验cookie4.同一ip访问次数限制5.jsajax
---





最近一直在研究爬虫相关的内容，对于各个知识点，都有所实践，以下是研究的结果。





<!--more-->

![python 爬虫](./3015729754.jpg)



## 反爬虫常见套路



1. 判断user-agent

2. 校验referer头

3. 校验cookie

4. 同一ip访问次数限制

5. js/ajax动态渲染页面





## 反反爬虫应对策略

### 1、user-agent头校验

每次请求设置随机user-agent头。可以引入`fake_useragent`模块或从[http://useragentstring.com/pages/useragentstring.php?typ=browser](http://useragentstring.com/pages/useragentstring.php?typ=browser)获取最新请求头。





通过scrapy框架实现，`download_middleware`中间件，`process_request`方法。示例：

```

# 自定义User-Agent列表

request.headers['User-Agent'] = random.choice(USER_AGENTS)



# fake_useragent方式实现

from fake_useragent import UserAgent

request.headers['User-Agent'] = str(UserAgent().random)

```

### 2、校验referer头

1. 设置referer为网站主域名

2. 通过selenium爬取，selenium会自动为每次请求增加referer头



### 3、校验cookie

对方的网站的cookie规则无法分析/破解难度太大。可以通过`selenium/splash`处理对cookie的操作，建立cookie池



### 4、同一ip访问次数限制



如果同一个ip在某个时间段访问频次过高，会被认为是爬虫，封掉ip。解决办法：

#### 1.使用代理ip



    1) 批量获取ip，构成ip池

    2) 分次请求代理ip接口，每次请求一条ip，获取ip和过期时间



scrapy实现方式，`download_middleware`中间件，`process_request`方法。示例：

```

request.meta['proxy'] = proxy

```

#### 2.设置抓取频率

修改scrapy settings文件

```

# 设置下载延迟 3s

DOWNLOAD_DELAY = 3

```



#### 代理平台对比



指标\平台 | 芝麻代理 | 快代理| ...

---|---|---|---

稳定性 | 中（测试过程中，未发现代理不能用的情况） | 未使用，不明确 | ...

灵活性 | 高（参数配置灵活，通过url调用） | 未使用，不明确 | ...







### 5、js/ajax动态渲染页面



此类网站可以通过`selenium`或者`splash`工具来进行处理。各自优缺点对比：



指标\工具 | selenium | splash

---|---|---

性能 | 低(每次请求需页面加载完才能进行下一步处理) | 高（Twisted和QT，发挥webkit并发能力）

效率 | 低(模拟浏览器，浏览器底层初始化一些流程) | 高（Twisted和QT，发挥webkit并发能力）

运维成本 | 低（作为scrapy一个类库调用） | 高（需配合docker使用，开启docker-splash服务）

内存| 高（随时间推移，占用内存越高）| 待测试...

灵活性| 中 | 高（参数配置方便）

使用范围| 浏览器测试自动化工具 | 异步渲染页面



综上所述，爬取动态页面数据，在效率以及爬取性能上，splash会有明显优势。







## &Question



### 1、如何确保100%爬取？



1、代理ip稳定



2、建立失败请求重试机制



### 2、代理ip被对方网站封掉如何处理？（重试机制？）



通过scrapy框架`download_middleware`中间件，`process_response`方法来判断返回参数进行处理。示例：

```

    def process_response(self, request, response, spider):

        

        # 判断response状态码 或 返回内容为验证码，则获取新的代理ip

        if response.status != 200:

            self.logger.info('ip被拉黑')

            

            # 更新代理ip

            self.update_proxy()

            

            # 返回request对象 重新发起请求

            return request



        # 返回response到爬虫脚本

        return response

```

也可以作为重试机制之一。





### 3、selenium代理设置问题及替代方案



通过资料查找以及实践踩坑发现selenium对于代理ip的设置不太友好，而且如何动态切换代理ip也是个问题（也可以实现）。



splash设置动态ip比较方便。示例：



1. 中间件实现



```

class ProxyMiddleware(object):

      def process_request(self, request, spider):

	      request.meta['splash']['args']['proxy'] = proxyServer

	      proxy_user_pass = "USERNAME:PASSWORD"

	      encoded_user_pass = base64.encodestring(proxy_user_pass)

	      request.headers["Proxy-Authorization"] = 'Basic ' + encoded_user_pass



```

2. spider实现

```

def start_requests(self):

    for url in self.start_urls:

        yield SplashRequest(url,

            url=url,

            callback=self.parse,

            args={

            	   'wait': 5,

                   'proxy': 'http://proxy_ip:proxy_port'

            }



```

### 4、验证码问题

1. 手动认证（效率太低... 需要人工

1. 更换ip (方便

2. 打码平台 (一般的识别验证码类库不稳定，打码平台一般都需要收费

3. ...



选择哪个，哪种方式更适合，需要测试以及项目需求才能确定。





### 5、如何高效抓取



1. 破解对方ajax请求，通过ajax请求获取数据，不走页面

2. mysql连接池（Twisted、adbapi）

3. Redis分布式爬虫（Spider.Redis）

4. 数据写入redis或MongoDB，异步读入mysql

5. ...



### 6、Splash

这里以亚马逊为例，爬取亚马逊，使用Splash没有用selenium好，使用splash总是会出现响应丢失的情况，估计是响应时间太长了，后续还需要更加完善的测试。



## scrapy实践项目地址



[https://gitee.com/mingzhongshui/Python-scrapy-demo](https://note.youdao.com/)



1. jianshu分支 实现对简书所有文章详情的爬取，以selenium或者代理ip的方式

2. amazon分支 实现对亚马逊整站商品的爬取，以selenium或者代理ip的方式





## 预选方案



splash + 代理ip + 随机user_agent + cookie池 + 分布式爬虫
