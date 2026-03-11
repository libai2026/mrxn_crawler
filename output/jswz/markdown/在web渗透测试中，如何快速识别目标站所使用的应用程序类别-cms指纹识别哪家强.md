---
title: "在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强"
source: https://mrxn.net/jswz/detect-cms-online-tools.html
asset_dir: assets/在web渗透测试中，如何快速识别目标站所使用的应用程序类别-cms指纹识别哪家强
---

# 在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强

[Mrxn](https://mrxn.net/author/1)- 发表于2019/5/10 21:42
- 10654浏览
- [2评论](#comment)
- 22分钟阅读

深入探索

Web安全课程

技术文章订阅

在线安全工具

---

**前言：**  
  
 在**Web**[**渗透测试**](https://mrxn.net/tag/渗透)当中的信息收集环节，对于目标站的指纹收集是很重要的一个环节，同时收集的指纹准确与否在很大程度上对我们[渗透](https://mrxn.net/tag/渗透)测试的快慢和结果有着莫大的关系，今天我就我日常使用的[**cms识别**](https://mrxn.net/tag/CMS识别)方法、国内外的常见的公开的在线cms指纹识别网站、和开源/闭源工具以及一些[扫描](https://mrxn.net/tag/扫描)器等方面来说一下如何在web渗透测试实战中快速的判断出目标站所使用的程序类型。  
  
 注：以下测试排名不分前后，其中也包括我自己的一些手动测试方法！  
  
 首先说一下针对我国的基本国情来说，因为**GFW**的存在，国外的在线网站cms指纹识别几乎对国内的**CMS**识别不出来的！故我主要讲国内的几个流行的cms指纹识别网站。  
  
 一：  
  
 名称：云悉WEB资产梳理|在线CMS指纹识别平台  
  
 官网：<http://www.yunsee.cn/>   
  
 简介：云悉安全专注于网络资产自动化梳理，cms检测**web指纹识别**，让网络资产更清晰。  
  
 简评：国内后起之秀，目前指纹特征量：6394，云溪比较全面，在识别指纹的同时会收集操作系统，服务器，web容器,数据库，程序语言等基本web信息；域名信息：备案单位，邮箱，域名所有者，备案号，DNS，域名注册商；ip信息：IDC，IP(支持查看同IP域名网站，同网段IP及域名---即C段查询)；常见子域名挖掘等功能模块，**支持API调用**，不过需要你提供指纹申请，通过了后会发放邀请码，注册就可以使用。PS:单独的指纹识别还支持**CDN**，**WAF**识别。  
  
 下图所示为我测试一个网站的时候用云溪识别的，但是没有识别出来，我用第二个即将介绍的识别出来了，第三种也没有识别出来，最后介绍手工判断出来的方法。 [[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-001-1c78e5966c79.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/8e821557497818.png)](https://mrxn.net/content/uploadfile/201905/8e821557497818.png)  
  
 二：  
  
 名称：bugscaner博客出品，在线指纹识别,在线**cms识别**小插件--在线工具  
  
 官网：<http://whatweb.bugscaner.com/look/>  
  
 简介：一款简洁快速的在线指纹,网站源码识别工具,目前已支持**2000多种**cms的识别!  
  
 简评：这个是bugscaner博主自己写的线上工具，出来的时间也比较久了，速度比较快！支持种类多，支持批量cms识别（每次最多100个，一天1000次）**支持API接口**，支持同IP网站查询，ICP备案查询等功能，博主最近又更新了这个工具，增加了几百种源码正则，增加了对https网址的识别，增加批量**cms识别**，重新优化了识别代码,减去了大部分命中率低的path路径,识别速度更快，增加通过查询历史,来统计互联网常见的cms建站系统所占使用比例,哪些cms最受欢迎,结果仅供参考,并不准确（仅通过历史查询计算）；  
  
 下图就是刚刚云溪没有识别到的，但是在这里秒识别！ [[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-002-fa090f4baef2.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/d86c1557497819.png)](https://mrxn.net/content/uploadfile/201905/d86c1557497819.png)   
  
 三：  
  
名称：TideFinger 潮汐指纹  
  
官网：<http://finger.tidesec.net/>  
  
简介：Tide 安全团队(山东新潮信息技术有限公司)出品的开源**cms指纹识别工具**  
  
简评：**开源！**但是只是后端开源，如果有需求做成web版的，需要自己又板砖实力，自己搭建前端。详细的介绍，cms指纹识别相关技术实现细节，后端源码等等在**GitHub**，地址：<https://github.com/TideSec/TideFinger>  
  
下图是同上两个图一样的网站识别结果，但是等了好久**cms信息**一直在转圈，也没有结果。。。但是其他的像网站标题,Banner，IP地址，CDN信息,操作系统,其他的信息显示还是很快的。  
  
[[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-003-be58d5f5e8c5.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/5ffa1557497819.png)](https://mrxn.net/content/uploadfile/201905/5ffa1557497819.png)  
  
 四：  
  
 手工判断cms类型：   
  
下图所示是同上面三个在线cms指纹识别网站的同一个域名,通过简单的手工也可以快速识别处cms类型，看图，我们可以通过更改目标url的参数名或者参数值来进行**fuzz测试**，往往会有意想不到的记结果！这也是**fuzz**这门技术的魅力所在！  
  
通常fuzz除了一些专门的工具：  
  
<https://github.com/xmendez/wfuzz>  
  
<https://github.com/google/oss-fuzz>  
  
fuzz相关文章介绍：  
  
<https://github.com/wcventure/FuzzingPaper>  
  
<https://www.zhihu.com/question/28303982>  
  
<https://zhuanlan.zhihu.com/p/43432370>  
  
 我还推荐使用[**burpsuite**](https://mrxn.net/tag/burpsuite)配合这些工具或者是burp插件来进行fuzz测试，也很顺手！相关**burpsuite汉化**、**burpsuite**[**破解**](https://mrxn.net/tag/破解)可以在博客搜索[burp](https://mrxn.net/tag/burpsuite)关键词查看相关文章。  
  
  
  
[[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-004-d623d0ef5eb1.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/b50d1557497818.png)](https://mrxn.net/content/uploadfile/201905/b50d1557497818.png)  
  
  
  
[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-005-f540fb792d65.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/0ceb1557497818.png)[[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-006-5000d3b20027.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/a3631557497819.png)](https://mrxn.net/content/uploadfile/201905/a3631557497819.png)[[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-007-568678fd4ef3.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/1c771557497820.png)](https://mrxn.net/content/uploadfile/201905/1c771557497820.png)  
  
  
  
[![在Web渗透测试中，如何快速识别目标站所使用的应用程序类别---cms指纹识别哪家强](images/img-008-6e1031d8d221.png "点击查看原图")](https://mrxn.net/content/uploadfile/201905/673f1557497817.png)  
  
五：  
  
借助扫描器，特别是DIR扫描器这些，比如御剑，Arachni，XssPy，w3af，Nikto，OWASP ZAP，Grabber，Nmap，Netsparker，Acunetix.Web.Vulnerability.Scanner(AWS)等工具进行扫描，同时也可以使用类似JavaScript源码提取分析工具，往往能从JavaScript源码当中发现一些隐藏的子域名，文件内容等等。  
  
六：  
  
国外在线cms指纹识别网站：  
  
<https://whatcms.org>  
  
<http://cmsdetect.com/>  
  
<https://itrack.ru/whatcms/>  
  
不过由于你懂的原因，对于国内程序识别不怎么友好。

计算机安全

- 标签：
- [#渗透测试](https://mrxn.net/tag/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95)
- [#黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
- [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
