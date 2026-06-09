---
date: 2025-12-23T10:59:00+00:00
categories: ["前端"]
title: 聊一聊我第一个由 AI 深度参与完成的真实项目
slug: liaoyiliaowodiyigeyou_ai_shenducanyuwanchengdezhenshixiangmu
#description: 我不是前端工程师。但这次，我一个人完成了一个包含聊天窗口We
tags: ["AI", "前端", "客服系统"]
featured: false
draft: false
excerpt: 我不是前端工程师。但这次，我一个人完成了一个包含聊天窗口WebSocket实时推送多语言翻译复杂UI状态管理的前端项目。说实话，如果没有AI，这个项目我大概率会延期，甚至放弃一些体验上的细节。一前言前
---

> 我不是前端工程师。

>

> 但这次，我一个人完成了一个包含**聊天窗口、WebSocket 实时推送、多语言翻译、复杂 UI 状态管理**的前端项目。

>

> 说实话，如果没有 AI，这个项目我大概率会延期，甚至放弃一些体验上的细节。



## 一、前言



前端时间接了一个前端聊天+后端管理后台的项目，两个项目都是我自己一个人完成。



说起来后端还好，但是前端html+css那套我最开始入行的时候学了一点，但是后面正式工作后主要还是围绕后端语言来展开，前端的那套样式语法就渐渐地放下了；



但这次是一个全新的机会，也是一个新的挑战，需要自己写前端。那如何快速写前端项目，并快速交付呢？于是我想到了AI这个帮手，之前总拿它来排查问题，但是写一个项目行不行呢？ 我抱着怀疑的态度开始了这项“挑战”，并最终“有惊无险”的落地完成，顺利完成交付；



本篇文章，我想详细的复盘下这次经历：如何与AI沟通？ 如何合理利用AI完成代码的实现？以及举例一些聊天系统中实现的业务关键点！





<!--more-->





在使用前，要先想一下：



**AI 到底能帮我们做到什么？我们又该如何与 AI 协作，才能真的提高生产力，而不是制造技术债？**



------



## 二、与AI对话



### 2.1 为什么我会把 AI 真正引入一个“正经项目”？



先说结论：

**不是因为“新技术”，而是因为“现实问题”。**



我的真实情况



这个项目是一个 **客服聊天系统**，核心特点包括：



- Laravel 后端处理接口数据

- jQuery + Bootstrap 前端（我比较熟悉的是这套组合拳）

- 多账号、多好友

- WebSocket 实时推送

- 消息类型复杂（文本 / 图片 / 视频 / 语音）

- SaaS 场景（多租户）



我面临的真实问题是：



- 后端我非常熟

- 但前端交互复杂、状态多、样式细

- 每一个“小交互”都很耗时间

- 而项目又在持续迭代，**不能停下来重构**



👉 这时，AI 不再是“锦上添花”，而是**降低边际成本的工具**。



------



### 2.2 AI 开发入门：不要幻想“全自动”，要追求“人机协作”



#### 2.2.1  AI 最适合做什么？



在这次项目中，我给 AI 的定位非常清晰：



> **AI = 前端协作工程师**



基于我当时的情况，我给它的定时是，辅助帮我写前端代码，包括但不限于以下：



- UI 结构拆解

- JS 事件逻辑补全

- CSS 微调与重构

- 复杂 DOM 操作的示例实现

- 重复性、模式化代码生成



结合我使用之后的感觉，我认为他可能**不太适合**：



- 定业务边界

- 定核心数据结构

- 决定架构选型

- 性能极限设计



**这些必须由人来做。**



------



#### 2.2.2 心态非常重要：你不是“用 AI”，而是在“带 AI”



如果你把 AI 当成：



- “自动写代码工具”

- “一句话生成系统”



那你一定会失望。



但如果你把 AI 当成：



- 一个不抱怨的工程师

- 一个愿意反复改的搭子

- 一个可以随时请教的助手



你会发现它**非常好用**。



------



### 2.3 如何与 AI 沟通，才能真的把前端项目做出来？



这一节，是我整篇文章里最想聊的部分。



#### 2.3.1 关键原则一：给 AI “现有代码”，而不是“空需求”



❌ 错误方式：



> 帮我写一个聊天窗口



✅ 正确方式：



> 这是我现有的 HTML 结构

> 这是我的 JS 方法

> 这是我的业务规则

> 请在不破坏现有结构的前提下，实现功能 X



AI 的代码质量，**严重依赖上下文完整度**。



**PS：如果你是从0开始让AI帮你完成项目，那最好在同一个人聊天窗口下，如果切换了聊天窗口，那可能会导致以前的消息可能无法产生关联；如果要优化，最好贴上之前的代码！**



------



#### 2.3.2 关键原则二：需求要“具象”，不要“抽象”



比如我会这样描述 UI：



> 聊天窗口顶部：

> 左侧是头像 + 昵称

> 右侧是三个点按钮

> 点击后，从“聊天窗口右侧”滑出信息面板

> 而不是整个页面



你会发现：**我描述的是“画面”，不是“功能名词”。**



------



#### 2.3.3 关键原则三：有问题就“精准反馈”，不要一句否定



我在项目中经常这样和 AI 互动：



- “三个点按钮没有靠右”

- “事件绑定不到，因为是动态元素”

- “滑出层相对于 body 了，不是 chat-panel”



这种反馈，会让 AI **快速修正，而不是推倒重来**。



#### 2.3.4 一个我踩过的坑：AI 会“自信地写错”



AI不是万能的，它也有可能出错，你的描述词不清晰，代码未提供完整，就可能导致：



- CSS 看起来对，但层级错了

- JS 逻辑跑得通，但状态没覆盖

- WebSocket 示例是 Demo 级，不是生产级



所以我后来形成了一个习惯：**AI负责“给方案”，我负责“兜底校验”！**



## 三、项目功能关键点拆解示例



### 3.1 关键功能点一：前后端聊天消息推送



#### 3.1.1 后端整体设计思路



我采用的是：



- **Workerman / GatewayWorker**

- 后端消息统一入库

- 再推送 WebSocket 给前端



核心原则是：



> **消息以“后端为准”，前端只是展示层**



------



我设计的流程是，后端采用脚本监听第三方消息服务，监听到有消息之后推送到job，job中处理消息，代码如下：



```php

<?php



namespace App\Jobs;



use App\Repositories\YkAccountFriendChatRecordRepository;

use App\Repositories\YkAccountFriendRepository;

use App\Repositories\YkAccountRepository;

use App\Services\GatewayService;

use App\Services\InstagramMessageService;

use App\Services\TranslateService;

use Illuminate\Bus\Queueable;

use Illuminate\Contracts\Queue\ShouldQueue;

use Illuminate\Foundation\Bus\Dispatchable;

use Illuminate\Queue\InteractsWithQueue;

use Illuminate\Queue\SerializesModels;

use Illuminate\Support\Facades\DB;

use Illuminate\Support\Facades\Log;



/**

 * 处理mqtt消息

 */

class ProcessIncomingMqttMessage implements ShouldQueue

{

    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;



    protected $payload;



    /**

     * Create a new job instance.

     *

     * @return void

     */

    public function __construct(array $payload)

    {

        $this->payload = $payload;

    }



    /**

     * Execute the job.

     *

     * @return void

     */

    public function handle()

    {

        try {

            if (!$this->payload['PK']) {

                throw new \Exception('缺少PK！');

            }

            $accountKey = $this->payload['PK'];

            $account = app(YkAccountRepository::class)->firstWhere(['account_key' => $accountKey, 'status' => YkAccountRepository::STATUS_ENABLE]);

            if (empty($account)) {

                throw new \Exception("account_key：{$accountKey}对应的account数据不存在");

            }



            if (!is_array($this->payload['Payload']) || !count($this->payload['Payload'])) {

                throw new \Exception('payload数据异常！');

            }

            foreach ($this->payload['Payload'] as $value) {

                /**

                 * UserId 发送方id

                 * RealTimeOp 类型

                 * Text 文本类型是内容字段

                 * Media 媒体类型时字段

                 */

                if (empty($value['UserId'])) {

                    Log::info('payload中没有UserId：'  . json_encode($value));

                    continue;

                }



                $friend = app(YkAccountFriendRepository::class)->firstWhere(['pks' => $value['UserId'], 'account_id' => $account['id']]);

                if (empty($friend)) {

                    Log::info("pks：{$value['UserId']}在好友表中不存在！");

                    continue;

                }



                $contentType = InstagramMessageService::transContentType($value);

                if (empty($contentType)) {

                    Log::warning('ProcessIncomingMqttMessage - handle 未知的消息类型' . json_encode($value));

                    continue;

                }



                $sendTime = transMicrosecondTimestamp($value['TimeStampUnix']);



                $data = [

                    'customer_id'       => $account['belong_customer_id'],

                    'account_id'        => $account['id'],

                    'friend_id'         => $friend['id'],

                    'content'           => $value['Text'] ?? null,

                    'content_type'      => $contentType,

                    'attachment'        => InstagramMessageService::getAttachment($contentType, $value),

                    'item_id'           => $value['ItemId'],

                    'send_time'         => transMicrosecondTimestamp($value['TimeStampUnix']),

                    'send_status'       => YkAccountFriendChatRecordRepository::STATUS_SUCCESS

                ];

                

				// 如果是文本类型 获取翻译之后的数据

                if ($contentType == YkAccountFriendChatRecordRepository::CONTENT_TYPE_TEXT) {

                    $transContent = TranslateService::getChatMessageTranslate($account['belong_customer_id'], $value['Text']);

                    if ($transContent && ($transContent != $value['Text'])) {

                        $data['is_translate'] = YkAccountFriendChatRecordRepository::CONTENT_TRANSLATE;

                        $data['content_translate'] = $transContent;

                    }

                }



                DB::beginTransaction();

                try {

                    $record = app(YkAccountFriendChatRecordRepository::class)->updateOrCreate(['item_id' => $data['item_id']], $data);

                    app(YkAccountFriendRepository::class)->updateLastChatTime($friend['id'], $sendTime);

                    app(YkAccountRepository::class)->updateLastChatTime($account['id'], $sendTime);

                    DB::commit();

                } catch (\Exception $e) {

                    DB::rollBack();

                    Log::info('ProcessIncomingMqttMessage handle 落库失败，异常原因：' . $e->getMessage());

                    continue;

                }

                $data['message_id'] = $record->id;



                GatewayService::pushMessageToClient($data, $friend);

                // 自动回复消息

                dispatch(new SendAutoReplyMessageJob($record->id))->onConnection('redis')->onQueue('SendAutoReplyMessageSqs');

            }

        } catch (\Throwable $e) {

            Log::error('ProcessIncomingMqttMessage fail line:' . $e->getLine() . ' 报错信息：' . $e->getMessage(), ['payload' => $this->payload]);

        }

    }

}

```



`GatewayService`类的`pushMessageToClient`方法代码如下：



```

public static function pushMessageToClient($data, $friend)

{

    $gatewayHost = config('services.gateway.host', '127.0.0.1');

    $gatewayPort = config('services.gateway.port', '1238');



    Gateway::$registerAddress = sprintf('%s:%s', $gatewayHost, $gatewayPort);



    $sendData = [

        'account_id'    => $data['account_id'],

        'friend_id'     => $data['friend_id'],

        'friend_name'   => $friend['username'],

        'friend_avatar' => $friend['avatar'],

        'send_time'     => format_time($data['send_time']),

        'timestamp'     => format_time(null),

        'content'       => $data['content'],

        'attachment'    => $data['attachment'],

        'content_type'  => $data['content_type'],

        'message_id'    => $data['message_id'],

        'is_me'         => $data['is_me'] ?? false,

        'is_auto_reply' => $data['is_auto_reply'] ?? false,

    ];



    if (!$sendData['is_me']) {

        // 不管客服有没有在线 先标记账号和好友 有未读数据（从前端去处理已读）

        app(YkAccountFriendRepository::class)->update(['is_have_un_read_msg' => YkAccountFriendRepository::HAVE_UN_READ_MSG], $friend['id']);

        app(YkAccountRepository::class)->update(['is_have_un_read_msg' => YkAccountFriendRepository::HAVE_UN_READ_MSG], $data['account_id']);

    }



    // 判断当前客服是否在线

    if (Gateway::isUidOnline($data['customer_id'])) {

        Log::info('推送到客户端信息', ['customer_id' => $data['customer_id'], 'data' => json_encode([

            'type' => 'new_message',

            'data' => $sendData

        ])]);

        // 发送消息给客服

        Gateway::sendToUid($data['customer_id'], json_encode([

            'type' => 'new_message',

            'data' => $sendData

        ]));

    } else {

        Log::info("客服id：{$data['customer_id']}，未在线~", ['send_data' => $sendData]);

    }

}

```



这个方法多个地方都可以调用，比如：



- 接收到消息推送到前端

- 前端发送消息，后端推送到第三方成功，发送到前端回显

- 自动回复消息成功，发送到前端回显

- ...



#### 3.1.2 后端推送的数据结构



```json

{

    "account_id": 123456,

    "friend_id": 789012,

    "friend_name": "张三",

    "friend_avatar": "https://example.com/avatar.jpg",

    "send_time": "2023-10-15 14:30:25",

    "timestamp": "2023-10-15 16:45:10",

    "content": "你好，最近怎么样？",

    "attachment": "image_001.jpg",

    "content_type": "text",

    "message_id": "msg_20231015143025_123456",

    "is_me": false,

    "is_auto_reply": false

}

```



------



#### 3.1.3 前端接收消息



绑定并监听websocket



```js

// 绑定 WebSocket

function connectWebSocket() {

    if (!CUSTOMER_ID) {

        console.error('未设置客服ID，无法连接WebSocket');

        return;

    }

    // 清除之前的重连定时器

    if (reconnectTimer) {

        clearTimeout(reconnectTimer);

        reconnectTimer = null;

    }



    ws = new WebSocket(window.WEBSECKET_HOST); // 改成你的服务地址



    ws.onopen = function () {

        console.log('WebSocket 已连接');

        lastPongTime = Date.now(); // 连接建立时重置时间

        reconnectAttempts = 0; // 重置计数器



        // 绑定客服登录用户ID

        ws.send(JSON.stringify({

            type: 'bind',

            uid: CUSTOMER_ID

        }));

        // 启动心跳检测

        startHeartbeatCheck();

    };



    ws.onmessage = function (event) {

        console.log('收到消息：', event.data);

        let msg = {};

        try {

            msg = JSON.parse(event.data);

        } catch (e) {

            console.warn('收到非法消息', event.data);

            return;

        }



        if (msg.type === 'ping') {

            // 服务器心跳包，更新最后活跃时间并回复pong

            lastPongTime = Date.now();

            // 服务器心跳包，回复pong

            ws.send(JSON.stringify({type: 'pong'}));

            return;

        }



        if (msg.type === 'new_message') {

            console.log('收到new_message消息：', msg.data);

            handleIncomingMessage(msg.data);

        }



        if (msg.type === 'account_online_status') {

            const data = msg.data;

            console.log('收到account_online_status消息：', msg.data);

            updateAccountOnlineStatus(data);

        }



        if (msg.type === 'send_message_status') {

            console.log('收到send_message_status消息：', msg.data);

            const data = msg.data;

            // updateFriendOnlineStatus(data);



            updateMessageSendStatus(data)

        }

    };



    ws.onclose = function () {

        reconnectAttempts++;



        // 渐进式重连：前3次快速重连，后续采用退避策略

        const delay = reconnectAttempts <= 3 ?

            BASE_DELAY :

            Math.min(BASE_DELAY * Math.pow(1.5, reconnectAttempts - 3), MAX_DELAY);



        console.warn(`[第${reconnectAttempts}次重连] ${delay}ms后尝试...`);

        setTimeout(connectWebSocket, delay);

    };



    ws.onerror = function (e) {

        console.error('WebSocket 发生错误');

        console.error('WS错误代码:', e.code);

        console.error('WS错误原因:', e.reason);

        ws.close();

    };

}



/**

 * 新消息处理

 * @param msg

 */

function handleIncomingMessage(msg) {

    console.log('handleIncomingMessage', msg);

    const currentAccountId = state.currentAccountId;

    const currentFriendId = state.currentFriendId;



    if (msg.account_id === currentAccountId) {

        if (msg.friend_id === currentFriendId) {

            // 当前聊天窗口好友，追加消息

            appendMessage({

                me: msg.is_me || false,

                auto_reply: msg.is_auto_reply || false,

                name: msg.friend_name,

                avatar: msg.friend_avatar,

                timestamp: msg.timestamp,

                send_time: msg.send_time,

                content: msg.content,

                attachment: msg.attachment,

                id: msg.message_id,

                type: getContentType(msg.content_type)

            });

            // 如果当前消息是当前聊天好友的，标记好友状态为已读

            setFriendUnReadStatus(msg.friend_id, 0);

            translateVisibleMessages($('select[name="input_target_lang"]').val(), 'left');

        } else {

            // 当前账号的其他好友，标红点

            markFriendUnreadDot(msg.friend_id, msg.account_id);

        }

    } else {

        // 非当前账号，账号头像标红点

        markAccountUnreadDot(msg.account_id);

    }

}

```



这个这段逻辑主要包括：



- 当前聊天窗口实时追加消息

- 非当前好友 → 好友红点

- 非当前账号 → 账号红点



这里之所以要在前端判断account_id /friend_id，而不是后端分多钟类型推是因为：



- 降低后端推送负责度，而且我觉得在前端判断会更好

- 保证前端状态一致性

- 方便后续扩展更多UI状态



------



### 3.2 关键功能点二：中英文切换与“批量翻译”的实现思路



这是一个让我非常满意、也非常适合 AI 协作的功能。



#### 3.2.1 我的需求不是“翻译一条消息”



而是：



- 聊天窗口已有历史消息

- 切换语言后

- **原文不变**

- 原文下方显示译文

- 支持再次切换目标语言



------



#### 3.2.2 前端结构设计（AI 协助）



```html

<div class="original-text">Hello

    你好

</div>

```



AI 在这里给了我一个很重要的建议：



> 翻译内容不要覆盖原文，而是“附加”



如果一开始就让 AI 覆盖原文，后期做多语言切换、撤销翻译、重新翻译，都会非常痛苦。这让体验和可维护性都好很多。



------



#### 3.2.3 切换语言时的 JS 逻辑



```js

// Tab 切换事件

$("#collapseTranslate").on('change', '.translate-select', function () {

    let name = $(this).attr('name');

    let value;

    if (name === 'chat_message_auto_translate' || name === 'input_auto_translate') {

        const isChecked = $(this).is(':checked');

        value = isChecked ? 1 : 0;

    } else {

        value = $(this).val();

    }



    if (name === 'input_target_lang') {

        translateVisibleMessages(value);

    }



    if (name === 'chat_message_target_lang') {

        translateVisibleMessages(value, 'left');

    }



    $.post('/chat/change_translate_config', {

        name: name,

        value: value

    }, function (res) {

        if (res.code !== 0) {

            layer.msg(res.msg)

        }

    });

});



/**

 * 聊天框内容翻译

 * @param targetLang

 * @param trans_message_type

 */

function translateVisibleMessages(targetLang = 'en', trans_message_type = 'right') {

    const messagesToTranslate = [];

    const selector = '.chat-message-wrapper.chat-message-' + trans_message_type;

    console.log('selector', selector); // 输出拼接的选择器

    console.log('匹配到元素数量:', $(selector).length);

    $(selector).each(function () {

        const $wrapper = $(this);

        const messageId = $wrapper.data('id');



        const $bubble = $wrapper.find('.chat-message-bubble');

        const content = $wrapper.find('.chat-message-bubble .original-text').text().trim();

        const cacheKey = `${messageId}_${targetLang}`;



        if (!messageId || !content) return;



        // 若已缓存则直接渲染

        if (translationCache[cacheKey]) {

            applyTranslatedMessage(messageId, translationCache[cacheKey]);

        } else {

            // 显示 loading 占位

            insertLoadingPlaceholder($bubble);



            // 准备发送的内容

            messagesToTranslate.push({ message_id: messageId, content });

        }

    });



    console.log('messagesToTranslate', messagesToTranslate);

    if (messagesToTranslate.length === 0) return;



    $.ajax({

        url: '/chat/translate/batch',

        type: 'POST',

        contentType: 'application/json',

        data: JSON.stringify({

            messages: messagesToTranslate,

            target_lang: targetLang

        }),

        success: function (res) {

            if (res.code === 0 && Array.isArray(res.data)) {

                res.data.forEach(item => {

                    const cacheKey = `${item.message_id}_${targetLang}`;

                    translationCache[cacheKey] = item.translate;

                    applyTranslatedMessage(item.message_id, item.translate);

                });

            }

        }

    });

}



/**

 * 翻译内容显示

 * @param messageId

 * @param translation

 */

function applyTranslatedMessage(messageId, translation) {

    const $wrapper = $(`.chat-message-wrapper[data-id="${messageId}"]`);

    const $bubble = $wrapper.find('.chat-message-bubble');



    const $translated = $bubble.find('.translated-text');

    if ($translated.length) {

        $translated.text(translation);

    } else {

        $bubble.append(`

            

            ${translation}

        `);

    }

}

```



这段代码是 AI 在我给出 DOM 结构后帮我补全的。



### 3.3 关键功能点三：复杂 UI 交互（微信式体验）如何落地？



比如：



- 消息气泡宽度

- 时间显示位置

- 自己 / 对方对齐方式

- 动态按钮事件绑定



#### 3.3.1 动态元素事件绑定问题



我一开始写的是：



```js

$('#toggle-friend-info').on('click', ...)

```



AI 很快指出问题：



> **这是动态生成的 DOM，需要事件委托**



修正后：



```js

$(document).on('click', '#toggle-friend-info', function () {

    $('#friend-info-panel').toggleClass('show');

});

```



这是一个**非常典型的“AI 帮你查漏补缺”场景**。



------



#### 3.3.2 滑出面板相对聊天窗口，而不是页面



AI 在我反馈问题后，帮我调整为：



```css

.chat-panel {

    position: relative;

    overflow: hidden;

}

.friend-info-panel {

    position: absolute;

    right: -260px;

    transition: right .3s;

}

.friend-info-panel.show {

    right: 0;

}

```



#### 3.3.3 发送消息、接收消息左右分隔



```css

.chat-message-wrapper {

    display: flex;

    align-items: flex-start;

    margin-bottom: 12px;

    width: 100%;

}



.chat-message-left {

    flex-direction: row;

}



.chat-message-right {

    flex-direction: row-reverse;

}



.message-block {

    display: inline-flex;

    flex-direction: column;

    max-width: 75%;   /* 让消息区最大占75%宽 */

    word-wrap: break-word;

}



/* 自己发的消息（右侧） */

.chat-message-right .message-block {

    display: flex;

    flex-direction: column;

    align-items: flex-end; /* 时间右对齐 */

}



/* 对方的消息（左侧） */

.chat-message-left .message-block {

    display: flex;

    flex-direction: column;

    align-items: flex-start; /* 时间左对齐 */

}



.chat-message-bubble {

    max-width: 95%;

    padding: 10px 14px;

    border-radius: 16px;

    word-wrap: break-word;

    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);

    line-height: 1.5;

}

```



以上这些，基本上都是AI帮我完成调优的。



------







**除了以上几个功能点之外，我还实现了**



1. 退出登录聊天窗记忆功能：退出登录，记录上次聊天的对象，再次登录后自动打开最后一次聊天对象所在的分组、tab、聊天窗口、聊天记录

2. 多语言切换：通过配置切换当前要展示的语言

3. 快捷回复：添加（文本、图片、视频、语音）、删除、快捷发送

4. 自动回复：接收到消息自动回复

5. 翻译配置：支持发送出去的消息和接收到的消息，可以分别配置源语言、翻译为目标语言。比如发出去的是中文，实际对方接收到的是英文；接收到的是英文、韩文，聊天窗显示中文

6. 未读分组、tab、好友红点标记等



太多了，具体细节就不一一介绍了，光聊天一个窗口交互就复杂的一批（感觉要钱要少了，orz...



## 四、效果展示



登录

![image-20251223114030780.png](https://cxiansheng.cn/usr/uploads/2026/01/972399472.png)





聊天首页

![image-20251223114119055.png](https://cxiansheng.cn/usr/uploads/2026/01/2065645332.png)



翻译配置

![image-20251223114155843.png](https://cxiansheng.cn/usr/uploads/2026/01/3702242519.png)



自动回复配置

![image-20251223114232951.png](https://cxiansheng.cn/usr/uploads/2026/01/1781166712.png)







## 五、总结



### 5.1 AI写代码的优缺点



基于我这次和AI对话的实战来看，优点是非常明显的



- 前端效率提升巨大

- UI 微调不再痛苦

- 可以快速试错

- 非前端工程师也能做出“像样界面”



但是**缺点也很明显**：



- 不会主动考虑性能极限

- 容易“写得能用，但不够优雅”

- 架构必须你来定

- 需要你具备基本判断能力



### 5.2 其他



AI的使用远不限于此，如果你愿意学习如何使用：



- 描述需求

- 提供上下文

- 精准反馈

- 与 AI 协作



你会发现：**一个人，可以完成过去一个小团队才能完成的事情。**



## 六、写到最后



对我来说，AI 并不是让我“变成前端工程师”，而是让我在有限时间内，把一个本来可能妥协的项目，**做到自己满意为止**。



从某些方面来说，AI让我变的更高效，从之前排查问题靠百度、靠在社区提问，到现在有问题问AI，AI的准确率还不错；从之前靠自己经验写出一段逻辑代码，到现在请AI帮我优化，大大提高了我代码的质量；AI是个好东西，咱们程序员还是要擅于利用它为自己服务才是！



---



**作者**：命中水 

**版权声明**：转载请注明出处，欢迎技术交流
