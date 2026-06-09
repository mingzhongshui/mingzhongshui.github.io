---
date: 2025-01-08T22:31:00+00:00
categories: ["后端"]
title: 聊聊redis在电商系统中的实战应用
slug: liaoliaorediszaidianshangxitongzhongdeshizhanyingyong
#description: 一前言在我从事的工作经历中，其实接触的电商行业还挺多的，大概
tags: ["redis", "电商系统", "项目实战"]
featured: false
draft: false
excerpt: 一前言在我从事的工作经历中，其实接触的电商行业还挺多的，大概占经历的670左右。而在电商项目中，用到缓存的场景就很多了，像数据缓存CDN缓存页面缓存等等，redis是最常用的keyvalue数据库了，
---

## 一、前言



在我从事的工作经历中，其实接触的电商行业还挺多的，大概占经历的6、70%左右。



而在电商项目中，用到缓存的场景就很多了，像数据缓存、CDN缓存、页面缓存等等，redis是最常用的key-value数据库了，memechache虽然和redis同样都是内存数据库，但是使用的最多的还是redis。



在使用redis之前，先简单了解下redis的特点和数据结构吧；





<!--more-->





## 二、什么是redis



redis是一种是一种开源的内存数据结构存储系统，它支持多种数据结构存储，如字符串、哈希、列表、集合、有序集合等。



它可以用作数据库、缓存和消息中间件。



### 2.1 特性



#### 2.1.1 内存存储和高性能



redis把数据放在内存中，读写性能高达10万+/秒 QPS



redis是单线程模型，避免多线程竞争，所有操作都是原子性的



基于epoll和kqueue的异步非阻塞I/O，轻松实现高并发连接



#### 2.1.2 丰富的数据结构



5种核心数据结构：字符串（String）、哈希（Hash）、列表（List）、集合（Set）、有序集合（ZSet）



4种高级数据结构：位图（Bitmaps）、基数统计（HyperLogLogs）、地理空间（Geospatial）、流（Streams）



针对每种数据结构优化操作效率



#### 2.1.3 持久化能力



redis通常情况下都把数据放在内存中，开启持久化的时候才会将数据同步保存到硬盘中。有两种持久化方式：



RDB快照：定时备份全量数据，二进制压缩存储（操作指令：save和bgsave，save指令**生产环境慎用**，回阻塞线程；`bgsave`会fork一个子进程来写入RDB文件）



AOF日志：记录所有写操作，支持每秒/每次操作同步



4.0引入混合持久化



#### 2.1.4 高可用架构



支持主从复制、哨兵模式（监控、故障检测、转移）、集群模式（数据分片，16384个槽，支持水平扩展）



## 三、常见场景



在了解了redis的特性之后，我们就能知道redis具体有什么用，在什么场景可以使用了。



下面我就来列举下在我所经历的电商系统中，我用到redis的几个常见场景。



### 3.1 秒杀活动



在电商系统中，很常见的一个场景就是秒杀了。秒杀意味着短时间内可能会有大量用户涌入系统，对极个别的商品进行抢购下单。



如果用户量过大，就会产生并发问题，并发问题处理不好，一旦导致制定好的商品库存出现超卖了，那就会造成损失了。



那么如何避免这种库存超卖的情况呢？那就要用到分布式锁了。在我之前的文章中有提到过生成订单的问题，订单号重复。其实这两个问题核心是相通的，都是要保证一个操作只能有一个服务在进行，不能多个服务同时进行一个操作，这样就会导致意料之外的情况发生。



秒杀活动涉及的点很多，比如html静态文件上CDN、nginx配置、服务器主从等，这里就不过多展开，直接聊redis



如何实现分布式锁呢，参考我之前的文章



[工作回顾之账单号怎么重复了？]: https://www.cxiansheng.cn/server/619



伪代码如下：



```php

$redis = new Redis();

$redis->connect('127.0.0.1', 6379); // 连接 Redis



$script = 'return redis.call("SET", KEYS[1], ARGV[1], "NX", "PX", ARGV[2])';



// 设定重试次数

$number = 5;



while($number--) {

    // 获取商品库存锁

    if ($redis->eval($script, ['lock:stock:{goodsId}', 1, 5000], 1)) {

        try {

            	// 扣减库存业务执行...

                

            } catch (\Exception $e) {

                \Yii::error("库存扣减失败:" . $e->getMessage());

            } finally {

                // 释放锁（需校验value）

                $unlockScript = '

                    if redis.call("GET", KEYS[1]) == ARGV[1] then

                        return redis.call("DEL", KEYS[1])

                    else

                        return 0

                    end

                ';

                $redis->eval($unlockScript, ['lock:stock:{goodsId}', 1], 1);

            }

    } else {

        // 获取失败 睡2s

        sleep(2);

    }

}

```



上面的代码可以保证在同一时间只有一个服务可以对指定商品进行库存扣减动作，当然保险起见数据库库存字段，也要设置为int无符号（不能为负数）类型。这样最坏的情况下，业务代码没拦住，到数据库这层也能防住。



在抢购这种场景下，redis不仅可以作为分布式锁使用，还可以



- 缓存商品库存数据，不需要每次都要查数据库库存数据

- 缓存商品详情页html，设置定时任务主动或被动更新html的动态数据

- 将请求放入redis队列，后台按队列先后执行抢购下单动作



### 3.2 订单超时关闭



只要是电商系统，都会涉及到下单的动作，下单到真正完成支付之间还有一系列动作，只要下单了就会涉及到锁库存。如果系统中的未支付订单过多，导致库存不足，影响到了真正想购买的客户，那就是我们的损失了。



所以我们要及时关闭那些，在支付中但是还未真正下单的用户。那就要设计一个订单超时时间了，如果超过这个时间，我们就把这个订单关闭，释放库存。



同样也可以使用redis来实现，redis实现的方式有两种：



#### 3.2.1 zset有序集合



zset是一个有序集合，每一个元素都关联一个score，通过score排序来取集合中的值。



我们要使用ZADD命令添加有序集合，基本用法如下：



ZADD



ZADD命令是用于将一个或多个成员元素及其分数值加入到有序集合中。如果成员已经是有序集的一部分，该命令将更新成员的分数值，并重新插入成员以确保其在正确的位置上。分数值可以是整数或双精度浮点数。如果有序集合不存在，则会创建一个空的有序集合并执行 ZADD 操作。如果键存在但不是有序集类型，则返回错误。



> ZADD key [NX|XX] [CH] [INCR] score member [score member ...]



- key：有序集合的键

- NX：可选参数，仅添加新成员

- XX：可选参数，仅更新已存在成员

- CH：可选参数，修改返回值为变更成员的数量

- INCR：可选参数，用于递增分数

- score：分数

- member：成员



了解用法之后，那假如说我们要设置订单生成30分钟后未支付关闭订单。那我们在下单时：



```shell

# 下单时加入延迟队列

# current_timestamp 下单时间

# current_timestamp + 1800 下单时间+1800 表示超时时间

# order:123456 123456b表示订单号

ZADD order:delay {current_timestamp + 1800} "orderId:123"

```



获取超时订单的话，可以使用定时任务扫描订单延迟队列，获取集合的用法如下



ZRANGEBYSCORE



ZRANGEBYSCORE命令来查询指定分数范围内的元素。



> ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]



- key：有序集合的键

- min和max：指定分数的最小值和最大值。可以使用-inf和+inf表示无穷小和无穷大。

- WITHSCORES：可选参数，表示同时返回成员的分数



代码如下：



```

# 定时任务扫描

# ZRANGEBYSCORE 用于返回有序集合中指定分数区间的成员列表

expired_orders = ZRANGEBYSCORE order:delay 0 {current_timestamp}

for order in expired_orders:

    cancel_order(order)

    // 删除集合

    ZREM order:delay order

```



这样就可以用延时队列实现订单超时关闭了。同样redis还有另一种方式也可以用来实现，那就是键过期事件



#### 3.2.2 键过期事件



> 键过期事件故名思议就是key在失效（过期）的时候，提供一个回调，给客户端发送一个key失效的事件。客户端监听到键失效之后，可以展开其他动作。



通过键过期事件实现订单超时关闭，在创建订单的时候，往redis写一条数据，并设置过期时间



```shell

SET order:{orderId} 1 EX 1800

```



然后在redis.conf配置文件中开启键失效监听



```shell

notify-keyspace-events Ex

```



重启redis生效。



##### 1、一个完整的PHP示例



###### 1.1 创建订单时写入redis



```php

/**

* 订单创建逻辑

*/

$redis = new Redis();

$redis->connect('127.0.0.1', 6379);



function createOrder($userId, array $items) {

    global $redis;

    

    $orderId = uniqid('order_');

    

    // 数据库创建订单（伪代码）

    $db->insert('orders', [

        'order_id' => $orderId,

        'user_id' => $userId,

        'status' => 'unpaid',

        'created_at' => time()

    ]);

    

    // 设置Redis过期键（30分钟）

    $redis->setex("order:{$orderId}:status", 1800, 'unpaid');

    

    // 记录实际状态（持久化）

    $redis->set("order:{$orderId}:actual_status", 'unpaid');

    

    return $orderId;

}

```



###### 1.2 PHP脚本监听键过期事件



```php

<?php

$redis = new Redis();

$redis->connect('127.0.0.1', 6379);



// 订阅过期事件频道

$redis->psubscribe(['__keyevent@*__:expired'], function ($redis, $pattern, $channel, $key) {

    $prefix = 'order:';

    $suffix = ':status';

    

    // 检查是否是订单key

    if (strpos($key, $prefix) === 0 && strpos($key, $suffix) === strlen($key) - strlen($suffix)) {

        $orderId = substr($key, strlen($prefix), -strlen($suffix));

        

        // 获取订单实际状态（防止误处理）

        $orderStatus = $redis->get("order:{$orderId}:actual_status");

        

        if ($orderStatus === 'unpaid') {

            // 处理订单关闭

            cancelOrder($orderId);

            $redis->set("order:{$orderId}:status", 'cancelled');

            

            // 记录日志

            $redis->lpush('order:cancelled:logs', 

                json_encode([

                    'order_id' => $orderId,

                    'time' => time(),

                    'reason' => 'timeout'

                ])

            );

        }

    }

});



function cancelOrder($orderId) {

    // 实现实际的订单关闭逻辑

    // 如更新数据库、释放库存等

    echo "处理订单超时关闭: {$orderId}\n";

}

```



### 3.3 排行榜



电商系统中往往存在很多商品，有些时候运营同学会需要一些数据做支撑，比如你可能会接到一个列出最近一个月或者最近一年的商品销售额排名top100的需求，然后运营同学会以此数据为基础提出类似但是更新的新产品（商品）。



传统的做法你可能会想到直接查库，如果商品数量不多的情况下，那还好说。如果商品数量巨多，而且设计前期没有保留商品销售总额的字段，那就要从订单来算出每个商品的销售额了，这个时候，就复杂了。



那用redis就简单多了，在商品交易成功的时候，往redis有序集合写入一条数据



```shell

Zadd goods:sales:rank amount goodsId

```



php代码：



```php

// 使用商品ID而不是完整名称作为成员

$redis->zAdd('goods:sales:rank', $sales, "goods_{$goodsId}"); // 而不是 "product_name"

```



每当有此商品售出时，就更新这个销售额字段。



后续有需要时，就将`goods:sales:rank`这个集合按照规则排序取出即可



完整伪代码如下



```php

$redis = new Redis();

$redis->connect('127.0.0.1', 6379);





// 更新单独商品销售额记录到redis

function addProductSale($goodsId, $saleAmount) {

    global $redis;

    // 金额转为分（整数）

    $amountInCents = intval($saleAmount * 100);

    // 增量更新销售额

    $redis->zIncrBy('goods:sales:rank', $amountInCents, "goods_".$goodsId);

}



// 按时间维度分片存储

function addTimeBasedSale($goodsId, $amount, $timeType = 'daily') {

    global $redis;

    $key = "goods:sales:rank:" . date('Ymd'); // daily

    if ($timeType == 'monthly') {

        $key = "goods:sales:rank:" . date('Ym');

    } elseif ($timeType == 'yearly') {

        $key = "goods:sales:rank:" . date('Y');

    }

    $redis->zIncrBy($key, $amount * 100, "goods_".$goodsId);

}





// 支付成功更新商品销售额

function paySuccessUpdateGoodsSale($orderId)

{

    // 获取订单商品列表

    $orderGoodsItems = getOrderItems($orderId);

    

    foreach ($orderGoodsItems as $item) {

        addProductSale($item['goods_id'], $item['price'] * $item['quantity']);

        

        // 同时更新日榜、月榜

        addTimeBasedSale($item['goods_id'], $item['price'] * $item['quantity'], 'daily');

        addTimeBasedSale($item['goods_id'], $item['price'] * $item['quantity'], 'monthly');

    }

}

```



按照销售额排序取出



```php

// 获取销售额排行榜（降序）

function getSalesRanking($limit = 10) {

    global $redis;

    return $redis->zRevRange('goods:sales:rank', 0, $limit - 1, true);

}

```



其他信息取出示例：



```php

// 获取单个商品排名

function getProductRank($goodsId) {

    global $redis;

    // 排名从0开始，所以+1得到实际名次

    return $redis->zRevRank('goods:sales:rank', "goods_".$goodsId) + 1;

}



// 获取单个商品销售额

function getProductSales($goodsId) {

    global $redis;

    $score = $redis->zScore('goods:sales:rank', "goods_".$goodsId);

    return $score / 100; // 转回元

}

```



## 四、总结



以上差不多就是电商系统中常见的业务场景以及redis使用了，当然电商系统中的场景远不止于此，redis的用途也还有很多，这里就不一一列举了。

相信只要了解了redis的数据结构以及特点之后，在具体场景就可以代入使用redis来实现了。



本期就到这里，下次再见啦~
