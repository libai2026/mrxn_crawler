---
title: "巧用七牛CDN的镜像功能使百度分享支持HTTPS"
source: https://mrxn.net/jswz/https-share-cdn.html
asset_dir: assets/巧用七牛cdn的镜像功能使百度分享支持https
---

# 巧用七牛CDN的镜像功能使百度分享支持HTTPS

[Mrxn](https://mrxn.net/author/1)- 发表于2015/10/14 10:05
- 16293浏览
- [3评论](#comment)
- 23分钟阅读

深入探索

ssl

传输层安全性协议

搜索引擎

---

最近搞了个 HTTPS 证书，像以前一样给博客添加了个百度分享（<http://share.baidu.com/>）的组件，但发现百度分享不支持 HTTPS（百度分享图标出不来，console 会提示页面有不安全的[脚本](#)元素）。看了其它几家也都不支持，[搜索](#)了下发现有人建议把百度分享所需的 js 都保存到自己本地就行了。这也是个办法，分享功能大多是抓取这个页面的 title、摘要、图片等然后起调一个页面完成分享，这些都是本地 js 文件能完成的。

技术文章订阅

看了下从百度分享获取的代码，里面主要加载了这个：http://bdimg.share.baidu.com/static/api/js/share.js，访问了一下果然还是不支持 HTTPS。然后我就天真的把 share.js 上传到了七牛 CDN（七牛是支持 HTTPS的，在空间设置-域名配置里面设置下就行），然而百度分享的图标还是没出来。看了下控制台，卧槽，又加载了一堆 js，作为一个全栈工程师，我非常灵性的瞅了眼代码里面有一段：domain:{staticUrl:”http://bdimg.share.baidu.com/”}，原来是模块化加载，把链接替换成七牛 CDN  的链接后有些请求 404 了，我又天真的以为把这几个 js 文件补全就行，但是补完几个，又有几个文件 404 了，我可没耐心一个个文件补齐呀。

作为一个灵性码农，我马上想到七牛不是有个镜像存储功能嘛，设置一发：

[[![巧用七牛CDN的镜像功能使百度分享支持HTTPS](images/img-001-c611d2bedb2e.png)](https://mrxn.net/content/uploadfile/201510/996e3f6bfadf81199bf8babebc6a39e020151014031036.png)](https://dn-iyaozhen.qbox.me/wp-content/uploads/2015/08/20150817003746.png)

故事就这么结束了吗？怎么可能。百度“幺蛾子”还是比较多。百度分享不光是分享功能，还有分享的数据分析。数据哪里来呢？前端埋点统计的呀，原理简单说就是监控分享时的点击事件，发送数据到后台。这其中的核心就是 http://nsclick.baidu.com/v.gif，需要统计的参数和值都以 GET 参数的形式附在链接后面。然后后端再清洗请求日志或者获取请求的时候就直接把数据入库了。但这个统计小图片也不支持 HTTPS。没办法，只能去掉了，方法也很简单，static/api/js/trans/logger.js 文件为空就行（上传个空文件、占个位）。到此才算大功告成。

文件大小转换

上面是授之以渔，不想自己弄的，可以直接抓鱼，当然希望你也能明白其中的风险，文件是我这边的（可能有后门，当然我没有），而且哪天我流量没了可能会把文件删了。

深入探索

SQL注入检测工具

Windows安全工具

授权

```
<div class="bdsharebuttonbox"><a href="#" class="bds_weixin" data-cmd="weixin" title="分享到微信"></a><a href="#" class="bds_qzone" data-cmd="qzone" title="分享到QQ空间"></a><a href="#" class="bds_sqq" data-cmd="sqq" title="分享到QQ好友"></a><a href="#" class="bds_tsina" data-cmd="tsina" title="分享到新浪微博"></a><a href="#" class="bds_tqq" data-cmd="tqq" title="分享到腾讯微博"></a></div>
<script>window._bd_share_config={"common":{"bdSnsKey":{},"bdText":"","bdMini":"2","bdMiniList":false,"bdPic":"","bdStyle":"0","bdSize":"16"},"share":{}};with(document)0[(getElementsByTagName('head')[0]||body).appendChild(createElement('script')).src='https://dn-iyz-file.qbox.me/static/api/js/share.js?v=89860593.js?cdnversion='+~(-new Date()/36e5)];</script>
```

  
一点后话：一直感觉百度分享没人维护了，在群里打听了下。应该是有人（部门）维护着（至于不支持 HTTPS 那是百度 CDN 的锅），但是现在不流行打社交牌了，公司也不重视这块了，还是 200 亿糯米 O2O 更实在，而且百度首页貌似也不显示[搜索](#)结果页面的分享次数了。

当然 ，emlog可以使用简爱的这个分享插件：http://www.emlog.net/plugin/174，也支持https，但是得需要jquery的支持，如果模板没有加载，需要自己添加，不然是不会起作用的。

脚本语言

原文地址：https://iyaozhen.com/use-qiniu-image-storage-allow-baidu-share-support-https.html

- 标签：
- [#编程](https://mrxn.net/tag/%E7%BC%96%E7%A8%8B)
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
- [#百度](https://mrxn.net/tag/%E7%99%BE%E5%BA%A6)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
