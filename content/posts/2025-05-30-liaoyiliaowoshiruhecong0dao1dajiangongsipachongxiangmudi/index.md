---
date: 2025-05-30T14:12:00+00:00
categories: ["后端"]
title: 聊一聊我是如何从0到1搭建公司爬虫项目的
slug: liaoyiliaowoshiruhecong0dao1dajiangongsipachongxiangmudi
#description: 一前言在工作的这么多年中，其实有很少能接触到挑战自我的项目。
tags: ["python", "scrapy", "scrapy-redis", "selenium", "爬虫"]
featured: false
draft: false
excerpt: 一前言在工作的这么多年中，其实有很少能接触到挑战自我的项目。在小公司当个小组长，无非就是curd部署项目搭建gitlabreview同事代码等繁琐的工作，偶尔写写前端。大公司的话，工作内容其实就没这么
---

## 一、前言



在工作的这么多年中，其实有很少能接触到挑战自我的项目。在小公司当个小组长，无非就是curd、部署项目、搭建gitlab、review同事代码等繁琐的工作，偶尔写写前端。大公司的话，工作内容其实就没这么繁琐了，部署项目有运维，页面有前端同事，review有部门leader，工作中80%的时间都是curd，当然会有一些小型的基于需求的项目来做，但都是能力范围之内的。



在我这短暂的开发生涯中，还真就遇到过那么一次让我觉得非常有挑战性的事，那就是从php转python，从0到1实现爬虫架构。从结果上来说，虽然达不到100%的爬取成功率，但整个过程也可以说是倾尽了全力，当然这也是我为数不多的我绞尽脑汁想完成的项目（主要是这个项目完成之后的绩效比较诱人，咳咳咳~），而且我对新东西、新事物都有种想挑战一下的心态。



今天就来讲一下我是怎么从0到1实现整个爬虫架构的。



> 首先声明：我是主导者、也是参与者，当然后期还有更专业的python同事一起加入，帮我调优，给我优化意见，最终才合力完成的这个项目，不是我一个人的功劳。





<!--more-->





## 二、起因



在加入C公司一年后，到了年终总结阶段，项目经理要找团队的每个人聊过去的一年中主要的业绩和贡献，其实就是谈绩效了。在对话中我清晰的记得，当项目经理问到我



：“对自身有什么规划或者对自己在团队内的职责有什么想说的”



的时候，我脑海中一个想法已经酝酿了好久，我说



：“我想多做一些有挑战性的事情”



其实不太敢明说，目前在工作中的事情太顺风顺水了，不怎么用点脑子就能完成（因为主要负责的是公司内部系统的开发，所以高并发、分布式什么的几乎接触不到）



就是这样一句话在不久后起了波澜



公司主要是做跨境电商的，在亚马逊平台销售自己的产品。既然是电商行业，那就少不了要爬取竞品数据，分析对手的产品、评价、销量等，这时候就需要爬虫出马了。上层有了这个决定之后，落实下来就到了我们小组身上了。



最开始是计划用php做爬虫的，但是后面了解到爬虫不是php的长处，python才是。而且python提供非常完整的生态链来处理爬虫。下面我列举下我当时了解到python为什么适合爬虫的原因，而且也是我后面说服leader用python做爬虫的理由：



## 三、Python优势



### 1、语言层面的优势



#### 字符串处理能力



原生支持正则表达式（re模块），举个例子：



python中获取页面中的单价



```python

import re

re.findall(r'price:(\d+)', html)  # 一行代码提取价格

```



#### 开发效率



动态类型 + 丰富的内置数据结构（字典/列表/集合），可以更快的编写爬虫代码



再举个例子，python提取a标签中的href



```python

links = [a['href'] for a in soup.select('a')]

```



php实现



```php

$doc = new DOMDocument();

@$doc->loadHTML($html); // @抑制解析警告



$links = array();

$anchorTags = $doc->getElementsByTagName('a');



foreach ($anchorTags as $a) {

    $href = $a->getAttribute('href');

    if (!empty($href)) {

        $links[] = $href;

    }

}



// 输出结果

print_r($links);

```



python一行解决的问题，php需要8行。哪个便利一目了然吧



### 2、生态工具链









| 工具          | 作用           | 优势                             |

| ------------- | -------------- | -------------------------------- |

| Requests      | HTTP请求       | 人类友好的API，会话保持自动处理  |

| BeautifulSoup | HTML解析       | 容错性强，find_all比xpath更直观  |

| Scrapy        | 全功能爬虫框架 | 内置异步、中间件、管道等完整架构 |

| Selenuim      | 动态页面渲染   | 模拟浏览器行为                   |

| PyQuery       | JQuery式选择器 | 对前端开发者更友好               |



#### 应对爬虫的灵活性



快速切换解析方案



```python

# 应对网站改版，快速更换解析方式

def parse(html):

    try:

        return css_select(html)

    except ParseError:

        return xpath_parse(html)  # 备用方案

```



#### 动态执行js



```python

# 使用PyExecJS执行加密算法

import execjs

ctx = execjs.compile("""

    function decrypt(t) {

        return CryptoJS.AES.decrypt(t, 'key').toString();

    }

""")

decrypted = ctx.call("decrypt", encrypted_str)

```



#### IP轮换便捷性



```python

# 使用代理中间件示例（Scrapy）

class ProxyMiddleware:

    def process_request(self, request, spider):

        request.meta['proxy'] = random.choice(proxy_pool)

```



### 3、大数据处理



#### 分布式扩展



- Scrapy-Redis 实现分布式爬虫

- celery调度异步任务



#### 无缝对接数据管道



```python

# 爬取后直接进入分析流程

import pandas as pd

data = pd.DataFrame(scraped_items)

data.groupby('category').sum().plot(kind='bar')

```



基于以上优势，在当时做爬虫用python可以说是最好的选择了。



## 四、学习



那确定了语言，现在就开始准备了，团队内没有会python的咋整？ 



学呗！



我和团队内的另外一个php同事开始自学起了python，首先确定学习路线



1. python语法

2. python爬虫框架scrapy

3. Xpath语法

4. 反爬

5. 代理



就这样用了一个月时间，基本上把这些东西都过了一遍，一个月之间我总结了一些关于python及爬虫的知识：



- [Python scrapy框架学习笔记及简单实战 - 命中水](https://www.cxiansheng.cn/server/550)

- [Python学习笔记（基础） - 命中水](https://www.cxiansheng.cn/server/561)

- [Python学习笔记（常用扩展） - 命中水](https://www.cxiansheng.cn/server/563)



后面又整理了反爬的套路及应对措施：[Python爬虫研究 - 命中水](https://www.cxiansheng.cn/server/569)



以上都是接口爬虫，后面了解到需要爬页面，然后又学习了页面爬虫



- [Python如何爬取动态网站？ - 命中水](https://www.cxiansheng.cn/server/580)



在学习的过程中，尝试爬了自己的网站，源码在[Python scrapy demo: Python scrapy框架实战demo](https://gitee.com/mingzhongshui/Python-scrapy-demo)



这一个月中走到哪都是我学习爬虫的身影，地铁上刷B站视频、晚上回家学习python语法、周末自己练习爬爬简书啥的，甚至做梦都梦到爬虫成功了。现在回忆起来真是佩服我自己



## 五、简单实战



接下来，产品经理需求下来了，根据亚马逊商品ASIN爬评论，看看学习成果咋样（一个月中另一个php同事没啥进展，后面就我自己开发了）



1. 基于scrapy开发的爬虫脚本

2. 初始化爬取链接

3. xpath获取关键数据

4. 数据通过管道写入mongodb



基于scrapy我很快完成了ASIN评论的爬取，但是因为评论过多，有时候爬取到一两页就显示爬取失败了，因为我没加代理，然后选择了快代理作为我们最开始的代理方（没有建立自己的代理ip库是因为当时自己参考过一版别人的源码，做出来的效果发现那些免费的代理ip质量都不太高，所以后面就选择了收费的），快代理有多种模式可选择，具体可以去官网参考下[快代理 - 企业级HTTP代理IP云服务_专注IP代理11年](https://www.kuaidaili.com/)



既然方案没问题，那就开始大刀阔斧的干了



## 六、着手开发



需求是提前往内部系统里录ASIN，然后每天定时根据这些ASIN爬取评论数据，重复的替换掉



OK，既然需求定了，那就开始整理下设计架构了（这时候公司招的专业的python同事入场了）经过了多次的沟通，整理架构如下：



![爬虫架构图.png](https://cxiansheng.cn/usr/uploads/2026/01/3396164285.png)



于此，框架基本完成，主要增加：



1. 使用scrapy-redis分布式爬虫增加爬取效率

2. 接口API使用Flask框架

3. 接口采用celery异步队列



### 关键问题



过了一段时间， 此架构基本落地了，但是遇到个问题，就算使用了专业的ip代理工具，但是有时候爬取质量和效率还不是那么好。不得不说，亚马逊的反爬机制还是挺厉害的。基于此前提下，我们产生了更换ip代理商的想法，于是我们发现了scrapy_crawlera。



### Scrapy-Crawlera



Scrapy-Crawlera 是一个 **Scrapy 中间件**，用于与 Crawlera（Smart Proxy）服务集成，帮助爬虫开发者高效处理反爬机制（如 IP 封禁、验证码、动态渲染等）。Crawlera 是 Zyte（原 Scrapinghub）提供的 **智能代理服务**，可以自动管理代理池、处理请求头、执行 JavaScript 渲染等



#### Crawlear的核心功能



##### 智能代理轮换



- 自动切换 **全球代理 IP**（覆盖 100+ 国家）



- 避免 IP 被封，支持高并发请求

- 自动重试失败的请求



##### 自动反反爬



- 动态调整请求头（User-Agent、Referer、Cookies）

- 处理 JavaScript 渲染（类似无头浏览器）

- 绕过 Cloudflare、Akamai 等防护



##### 请求优化



- 自动管理会话（Session）

- 支持 HTTP/HTTPS/SOCKS5

- 提供 **请求统计**（成功率、延迟、封禁率）



#### 安装与配置



```shell

pip install scrapy-crawlera

```



###### scrapy配置



```

# 启用 Crawlera 中间件

DOWNLOADER_MIDDLEWARES = {

    'scrapy_crawlera.CrawleraMiddleware': 300

}



# 设置 Crawlera API Key（需注册 Zyte 获取）

CRAWLERA_ENABLED = True

CRAWLERA_APIKEY = '你的API_KEY'



# 调整爬虫并发（Crawlera 默认限制 5 并发）

CONCURRENT_REQUESTS = 32

CONCURRENT_REQUESTS_PER_DOMAIN = 32

AUTOTHROTTLE_ENABLED = False  # 关闭自动限速

```



#### 适用场景



- **企业级爬虫**（需要高稳定性）

- **反爬严格的网站**（如电商、社交媒体）

- **不想管理代理池**（减少运维成本）



使用scrapy-clawlera的前提，就是需要去[Zyte](https://dash.scrapinghub.com/account/signup)注册一个用户（我之前用的时候叫scrapyinghub，现在改名了），然后购买付费，按请求收费。比如200W个请求，**400美刀**，我记得我们巅峰时期一个月的代理费都干到过**4000多**人民币。但是这钱花的也值，爬取效率杠杠的！



scrapy-clawlear除了贵几乎没有缺点。



## 七、需求升级



过了没多久，新需求又来了，公司在亚马逊有店铺，运营同学每次都要去亚马逊后台下载报表数据，我们有7、8个店铺的数据，亚马逊要求又很严格，每个店铺、站点都只能在同一个IP登录，如果不同IP登录了店铺后台，亚马逊可能会封禁账号，到时候申诉就会很麻烦。



所以需要这不就来了，要求爬虫自动抓取后台报表数据。保存在数据库，运营在同学在内部系统直接查看即可。



因为这个是需要登录账号之后进行的操作，所以接下来的处理就是需要模仿浏览器用户行为了，也就是页面爬虫。



说起页面爬虫，那就不得不提到selenimu了



### selenium



> **Selenium** 是一个用于 **自动化 Web 浏览器操作** 的开源工具集，主要用于 **Web 应用程序测试** 和 **浏览器自动化**。它支持多种编程语言（如 Python、Java、C#、JavaScript 等），可以模拟用户在浏览器中的操作，如点击、输入、导航等。



通俗点来讲就是你可以编写程序来模仿浏览器的用户行为，比如有个网站有个签到功能，每天签到可以得积分，然后你就可以用程序模拟这个动作，每天打开网页，在指定位置，点击签到。这个行为用户可以是无感知的，用户就算在操作电脑，也不会发现你运行了脚本，打开了网页。因为这些动作都是后台运行的。



python使用selenium代码如下：



```

# -*- coding: utf-8 -*-



# 引入selenium webdriver类

from selenium import webdriver



# 引入火狐浏览器配置类

from selenium.webdriver import FirefoxOptions

# 实例化一个配置项

options = FirefoxOptions()

# 设置无需打开浏览器（如何想调试就把这个配置注释掉）

options.add_argument('--headless')



# 设置浏览器类型为火狐

browser = webdriver.Firefox(firefox_options=options)



# 打开一个网址

browser.get('https://item.jd.com/100008348542.html')

# 获取网页源码

source = browser.page_source



print(source)

```



具体如何使用详情参考我之前的文章：[Python如何爬取动态网站？ - 命中水](https://www.cxiansheng.cn/server/580)



除了selenium之外呢，python还有另外一种方式也可以获取页面上的数据



### Splash



> **Splash** 是一个基于 **Lua** 的轻量级 JavaScript 渲染服务，由 Scrapy 团队开发，主要用于 **动态网页的抓取**。它通过 **HTTP API** 或 **Scrapy-Splash 中间件** 与爬虫集成，能够执行 JavaScript 并返回渲染后的页面内容。



#### 核心功能



- 渲染 JavaScript 动态内容（如 React、Vue 生成的页面）。

- 支持截图、延迟加载、自定义 Lua 脚本。

- 通过 Docker 快速部署，资源占用较低。



那我们到底该如何选择呢？请看下面splash和selenium的对比



#### Splash 和 Selenium 的区别



| **特性**            | **Splash**                        | **Selenium**                       |

| :------------------ | :-------------------------------- | :--------------------------------- |

| **定位**            | 专为爬虫设计的轻量级渲染服务      | 浏览器自动化工具，兼顾测试和爬虫   |

| **架构**            | 基于 HTTP API 的无头浏览器服务    | 直接控制本地/远程浏览器实例        |

| **性能**            | 更高（无图形界面，资源占用少）    | 较低（启动完整浏览器）             |

| **编程语言支持**    | 通过 Lua 脚本或 HTTP 请求交互     | 支持多语言（Python/Java/C#等）     |

| **JavaScript 执行** | 高效，但功能有限（依赖 Lua 脚本） | 完整支持，可模拟用户操作           |

| **部署复杂度**      | 需 Docker 或独立服务              | 需浏览器驱动（如 chromedriver）    |

| **适用场景**        | 大规模爬虫（高并发、无交互需求）  | 需要交互的测试或爬虫（如点击登录） |



通过以上表格我们可以看出：



- **爬虫优先 Splash**：轻量、高效、适合大规模数据采集

- **交互优先 Selenium**：功能全面、适合测试或复杂操作

- **反爬严格时**：Selenium 更接近真实用户，但 Splash 可通过 Lua 脚本伪装请求头。



以我们那个场景为例，涉及到用户交互的动作（登录），最终我们选择了selenium。



### 后续



后续就是这个需求以selenium登录，然后拿到登录用户信息，再调用报表接口查询数据。



然后将这个脚本放在windows任务计划中，每天定时去执行。数据上传到接口，保存到数据库中。



建立异常机制，页面改变或接口报错，发邮件到负责人或开发人邮箱中。



#### 坑



哦对了，这里还有一个坑，我记得当时我离职前也都没有解决。



因为亚马逊后台登录地址的限制，每个账号只能在同一个IP登录，所以我们是部署了跟站点数量相对应的虚拟机，比如我们有8个站点账号，就部署了8个windows虚拟机。每次都要从远程桌面中登录进去，一旦代码有什么地方要调整或者定时任务要调整，那就要耗费大量的时间去一个一个登录进去操作，windows远程桌面有时候还很卡，所以每次操作都很痛苦。



至于为什么要搭建远程windows虚拟主机，是因为运营同学也是用这个方式登录后台的。



## 八、不足之处



虽然项目已经成功上线，并运行了一年多，但是还是有不足的。针对这个项目来说



1. 亚马逊页面有时候会变化，过一两个月就会调整，所以有时候爬取失败了我们是后知后觉

2. 后台页面爬虫，维护是个硬伤



针对问题1，现在来看的话我觉得可以引入以下几点：



- 设置警报当关键元素获取失败率超过阈值时通知

- 保留详细的错误日志和页面快照

- 定期运行测试爬虫检查关键元素是否存在

- 训练模型识别页面各元素位置

- 使用视觉定位(如Selenium截图后分析)



前几个还好说，就是费点力，代码调整+人工。后两个的话，就要再花费一番功夫了。



针对问题2，我记得当时是没有在虚拟机上搭建git的，原因也不记得了，如果要调整的话



1. 虚拟主机搭建git，远程仓库代码更新时，自动同步更新虚拟主机代码



## 九、总结



以上就是我当时在接触到爬虫项目的全部过程了，真的是参与感满满了。上线的时候就是那种看着自己的孩子一步一步长大成人的感觉。



好了，以上就是本文的全部内容了，下次再见吧！~



---



**作者**：命中水 

**版权声明**：转载请注明出处，欢迎技术交流
