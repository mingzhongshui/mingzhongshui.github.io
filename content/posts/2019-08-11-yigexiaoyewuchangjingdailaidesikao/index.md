---
date: 2019-08-11T17:37:00+00:00
categories: ["后端"]
title: 一个小业务场景带来的思考
slug: yigexiaoyewuchangjingdailaidesikao
#description: 最近在用layui做后台，有遇到这么个场景，就是上传图片，并
tags: ["思考"]
featured: false
draft: false
excerpt: 最近在用layui做后台，有遇到这么个场景，就是上传图片，并保存到oss的，很简单也很常见的一个小功能。但即使是这么个小功能也有点费脑筋，主要有以下几点1.对layui上传文件插件的不熟悉2.对业务场
---

最近在用layui做后台，有遇到这么个场景，就是上传图片，并保存到oss的，很简单也很常见的一个小功能。但即使是这么个小功能也有点费脑筋，主要有以下几点：



 1. 对layui上传文件插件的不熟悉

 2. 对业务场景的想象不够严谨

 3. 对自身服务器配置状况的无视



本篇博文就来说一下，就是这么个小问题，也让我有点伤脑筋的原因。





<!--more-->





## 小场景 ##

上传图片，保存到oss。服务器1核2G。两种方式，一种是在表单提交的时候，再上传；一种是选择完图片时时上传。两种各有优缺点。

## 不同上传方式的优缺点 ##

第一种：表单提交，再上传。优点是，在表单提交的时候，做图片上传，免去了前端对图片上传的进一步处理。缺点是，如果图片过多的时候，那么在保存表单的时候，保存图片可能很会耗时，网络有可能延迟。

第二种：选择图片时时上传。优点差不多跟第一种相反，选择的时候就上传，在表单提交保存数据的时候，就避免了对图片上传到oss的处理。缺点也很明显，如果处理不当，也有可能造成oss空间的浪费，可能上传的图片，并不是最终就需要的图片。



## 初始考虑 ##

一开始觉得，为了oss不必要的资源浪费，还是在表单保存的时候，在上传图片好一点儿（**注意：这里我没有考虑到其他层面的东西：服务器配置，上传速度，服务器带宽等**），搞起来，代码：

```

var uploadInst = layupload.render({

            elem: '#banner' //绑定元素

            ,url: '<?=base_url($viewPath . 'goods/upload')?>' //上传接口

            ,accept: 'images'

            ,acceptMime: 'image/jpg, image/png, image/jpeg'

            ,multiple: true

            ,auto: false

            ,choose: function(obj){



                //预读本地文件示例，不支持ie8

                obj.preview(function(index, file, result){



                    files[index] = file;



                    var img_html = '<li  id="'+index+'_id">';

                        img_html += '';

                        img_html += '';

                        img_html += '<a href="javascript:;" data-fileid="'+index+'" onclick="del_banner_file()">删除</a>';

                        img_html += '';

                        img_html += '</li>';

                        img_html += "<input id='"+index+"_hidden' type='hidden' name='banner[]' value='"+result+"'>";



                    $('#banner_list').append(img_html)

                });



            }

            ,done: function(res){

                //上传完毕回调

            }

            ,error: function(){

                //请求异常回调

            }

        });

```

上面的做法是，前端上传插件，选择完图片后获取到图片的base64格式，然后在页面上显示出来，并用隐藏域保存base64数据。

(ps:尝试过保存文件对象，在表单中，但是这种做法貌似不行

后端代码就很简单了，就是获取到base64然后上传oss；



### 结果 ###

做好之后，尝试提交表单，竟然出奇的慢，很慢很慢那种，我以为是程序出了问题，后来追踪到问题。发现保存数据都很快，几乎不占用什么时间，问题就卡在上传到oss这里。于是单张图片上传oss尝试了一下，发现在4-5s左右，慢的离奇，在想什么原因呢，后来慢慢考虑到可能是自己服务器的带宽不够，导致上传到oss的过程漫长，那多张图片的情况下，就更慢了。再换另一种思路尝试：



## 改变 ##

经过一番改造，第二种方式，选择时就将图片上传，代码也已经差不多了，如下：

**前端**

```

var uploadInst = layupload.render({

    elem: '#banner' //绑定元素

    ,url: '<?=base_url($viewPath . 'goods/upload')?>' //上传接口

    ,field: 'file'

    ,accept: 'images'

    ,acceptMime: 'image/jpg, image/png, image/jpeg'

    ,multiple: true

    ,choose: function(obj){



    }

    ,before: function(obj){ //obj参数包含的信息，跟 choose回调完全一致，可参见上文。

        layer.load(); //上传loading

    }

    ,done: function(res){



        //上传完毕回调

        if (res.code == 0) {



            var id = "banner_num_" + banner_num;



            var img_html = '<li  id="'+id+'">';

                img_html += '';

                img_html += '';

                img_html += '<a href="javascript:;" data-id="'+id+'" class="delete_banner" >删除</a>';

                img_html += "<input type='hidden' name='banner[]' value='"+res.src+"' >"

                img_html += '';

                img_html += '</li>';



            $('#banner_list').append(img_html);



            banner_num++;



            // 删除

            var tr = $("#"+id);

            tr.find('.delete_banner').on('click', function () {

                tr.remove();

            })



        } else {

            layer.msg(res.msg, {icon: 7});

        }

    }

    ,error: function(){

        //请求异常回调

    }

    ,allDone: function () {

        layer.closeAll();

    }

});

```



**php**

```

public function upload()

{

    try {

        $file = $_FILES['file'];



        if ($file) {



            $path = 'images/goods/' . $file['name'];

            $stream = file_get_contents($file['tmp_name']);



            $this->load->library('AliOSS', []);

            if (!($result = $this->alioss->uploadStream($path, $stream))) {

                throw new Exception('上传失败');

            }



            $this->ajaxReturn(['code' => 0, 'msg' => '上传成功', 'src' => $result['sourcePath']]);

        }



    } catch (Exception $e) {

        $this->ajaxReturn(['code' => -1, 'msg' => $e->getMessage()]);

    }

}

```





上面的代码分为这么几步:



 1. 前端选择文件之后，立马上传到oss，然后返回oss图片地址，用于前端展示

 2. 前端在上传之前，发起一个等待的东西`layer.load()`，表明图片在上传中

 3. 全部图片上传完毕之后关闭这个load，在allDone里可以找到



通过这种方式上传图片，明显比第一种方式好很多。最重要的是，在保存的时候无需等待太久，保存的时候只需要做一下数据对比然后插入到数据库就好了。

### 有个问题 ###

如果时时上传到oss的图片不是最终时候需要的，岂不是造成了oss空间的浪费？在前端预览的时候，用户可以点击删除，把当前图片在页面上去掉，这时候再请求一下后端接口，提供一下url或者其他什么参数，然后根据参数删除oss上的图片资源即可。



## 思考 ##

### 问题所在 ###

就这么个小功能，折腾了快3个小时的时间，实在是不值。如果自己在做之前就把业务场景想清楚，把服务器配置、上传速度、等待时长等都考虑清楚，结合这些东西再来选择合适的方式来解决，也不至于换2、3种方式来搞。



在某些时候也曾有过这样的感叹。比如一个模块，需要设计数据表结构，而且往往不是两三张表能搞定的，在设计初期，觉得挺好的，但是越往后做，接触真正的业务场景，业务核心结构逐渐清晰起来，才感觉，自己当初的设计不够理想，虽说还是可以用，但是发现可以用更好更合适的方式来实现它。这个时候，往往已经到了业务末尾，即使再想改变，也要花费大量的时间。



现在只是一个小小的业务场景，如果将来自己亲手设计一套架构，等架构落地，开发已到后期，才发觉自己的架构与当前业务场景不符，那就不是说一句抱歉能解决的了。



### 反一 ###

在下次的开发过程中，敲代码之前首先要理清需求，虽然产品同事会出ui和关键点备注，但是很多时候，有些问题他们也没有想到，只有在开发过程中，开发人员遇到了问题，才会发现，原来还有一些并发性的问题。这个时候，如果是小问题，只需要把逻辑稍稍改一下即可。如果事关业务结果的，可能就会牵连到之前写好的代码。比如在做特卖商品时候，特价活动期间，如果某个商品总库存（所有规格的库存之后）卖光了，那是否可以继续以原价的形式购买？又或者是商品的某个规格的库存卖光了，当前规格的价格是否可以以原价购买，下单的时候就会有特价商品和非特价商品。像等等类似的问题，如果事先不考虑清楚，后续改动将是无尽的烦恼。所以，这些问题，如果在需求会上想到的，最好提出来，然后想办法搞清。如果暂时没发现，后续开发过程中发现了，也要及时沟通，不能自以为...所以，首先，弄清需求很重要。



### 反二 ###



搞清需求之后，我们在心里对业务场景相必应该清楚不少了。这时候我们要思考业务复杂度，如果业务场景很简单，就是一个增删查改，那么我们在做之前要考虑是否除了这些还会有其他问题，比如说有些要求名称不能重复，那我们是否应该考虑并发时候的问题，把关键字段设置唯一索引等。如果关键位置的业务逻辑复杂，最好画出流程图来，我曾经因为对逻辑考虑不周被组长吐槽的情况（羞愧...），如果当时把业务形成一条一条的流程图出来，那么在写代码的时候不用再思考其他，跟着自己的流程逻辑走即可。即使过程中遇到了问题，也能很快发现是在哪个位置。



### 反三 ###

弄清需求和业务复杂度之后，就是关于主要数据表设计和开发工作了。之前在上一个公司有一个很好的习惯就是，在设计数据表结构的时候，首先会先写出表关联结构图和数据字典，后续在创建表结构的时候也会快很多，省去了纠结字段类型和起名的烦恼。然后在敲代码的时候，选择合适的工具和敲出不冗余可扩展的代码也很重要，方便后续的调整和优化。



## 总结 ##

不管是当前的业务开发工作还是未来的架构设计，都需要对当前手上的资源有一个比较全面性的掌握，清楚的知道自己拥有哪些资源，最高可以做到哪一步，然后跟业务场景相结合，找到最合适的那一套实现方式，才是一名合格的开发者。
