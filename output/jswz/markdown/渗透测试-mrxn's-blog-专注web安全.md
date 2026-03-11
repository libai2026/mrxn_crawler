---
title: "渗透测试 - Mrxn's Blog - 专注Web安全"
source: https://mrxn.net/jswz/Infiltration
asset_dir: assets/渗透测试-mrxn's-blog-专注web安全
---

(adsbygoogle = window.adsbygoogle || []).push({});

* [![利用 Windows Defender 的文件夹重定向与符号链接技术干翻它自己](images/img-001-9ee58c3ce2b4.webp)](https://mrxn.net/Infiltration/Break-Protective-Shell-Windows-Defender-Folder-Redirect-Technique-Symlink.html)

  + 2025/9/13
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [利用 Windows Defender 的文件夹重定向与符号链接技术干翻它自己](https://mrxn.net/Infiltration/Break-Protective-Shell-Windows-Defender-Folder-Redirect-Technique-Symlink.html)

  简介
  在渗透测试或红队活动中，反病毒和端点检测与响应 (EDR) 系统会不断追击攻击者。攻击者总是有两个选择：要么想办法躲开杀毒软件和 EDR 的镰刀，要么想办法阻止这些防御系统正常运行。(说到这里，有些人可能已经想到了 "自带漏洞驱动程序"...

  + 815阅读
  + [0评论](https://mrxn.net/Infiltration/Break-Protective-Shell-Windows-Defender-Folder-Redirect-Technique-Symlink.html#comment)
* [![渗透测试中58+用于权限绕过的XFF类header头分享](images/img-002-4f3e5762d242.png)](https://mrxn.net/Infiltration/bypass-permission-with-header-xff.html)

  + 2024/9/2
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [渗透测试中58+用于权限绕过的XFF类header头分享](https://mrxn.net/Infiltration/bypass-permission-with-header-xff.html)

  在一些渗透测试报告或相关文章中，我们经常可以看到某些突破口就是通过权限绕过，最常见的权限绕过是URL path部分，如多个斜杠/ 或者 分号; 亦或是二者结合配合目录穿越进行权限绕过，这部分大部分是由于后端系统的鉴权逻辑有错误，其次是header头部分，如XF...

  + 3591阅读
  + [0评论](https://mrxn.net/Infiltration/bypass-permission-with-header-xff.html#comment)

深入探索

漏洞修复方案

编码转换工具

安全

网络安全培训

企业安全咨询

SQL注入检测工具

软件

网络安全会议

Windows安全工具

计算机安全

* [![渗透测试技巧之通过SQL Server函数判断MSSQL数据库是否站库分离](images/img-003-d4f66562dcd7.png)](https://mrxn.net/Infiltration/731.html)

  + 2024/8/16
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [渗透测试技巧之通过SQL Server函数判断MSSQL数据库是否站库分离](https://mrxn.net/Infiltration/731.html)

  简介 在现代应用程序架构中，站库分离是一种常见的设计模式，旨在提高系统的可扩展性、安全性和性能。然而，在实际操作中，如何有效判断应用服务器和数据库服务器是否真正分离并运行在不同的物理或虚拟机上，在一些渗透测试中尝试通过SQL注入来写入文件却失败的场景就需要考虑...

  + 3740阅读
  + [2评论](https://mrxn.net/Infiltration/731.html#comment)
* [![使用正则快速从 js 文件里提取处 API  path](images/img-004-cdaf83108582.png)](https://mrxn.net/Infiltration/689.html)

  + 2022/3/17
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [使用正则快速从 js 文件里提取处 API path](https://mrxn.net/Infiltration/689.html)

  前言
  在渗透测试的时候，遇到前后分离的站点，多数与后端通信的 API path 就在 js 文件里，且大多数名称为 app.xxxx.js 这类以 app 开头的 js 文件里面。
  而且这类 js 文件大多数是混淆过的，或者压缩过，又臭又长！
  正则提取 API...

  + 7150阅读
  + [0评论](https://mrxn.net/Infiltration/689.html#comment)
* [![蓝队技巧：查找被隐藏的Windows服务项](images/img-005-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/506.html)

  + 2020/10/23
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [蓝队技巧：查找被隐藏的Windows服务项](https://mrxn.net/Infiltration/506.html)

  在上篇，我们说过红队技巧：隐藏windows服务，今天抽空来更新下，如何查找这类隐藏的Windows服务项。 首先看下效果，使用powershell远程下载执行直接获得隐藏的Windows服务名称：
  通过远程下载执行无文件落地查看隐藏Windows...

  + 9794阅读
  + [0评论](https://mrxn.net/Infiltration/506.html#comment)
* [![红队技巧：隐藏windows服务](images/img-006-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/503.html)

  + 2020/10/16
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [红队技巧：隐藏windows服务](https://mrxn.net/Infiltration/503.html)

  在后渗透测试中，我们拿到了目标机器的权限后，要想办法维持权限，保持持久，嗯，很重要，不管生活还是工作都需要持久！
  利用windows服务来植入我们的后门也是一种常见的利用方式，但是往往一般植入的服务很容易被管理员在任务管理器看到。如果可以...

  + 9510阅读
  + [0评论](https://mrxn.net/Infiltration/503.html#comment)
* [![零组镜像打包下载 零组文章下载（截止到2020年3月的版本和2020年09月19日版本）](images/img-007-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/449.html)

  + 2020/10/14
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [零组镜像打包下载 零组文章下载（截止到2020年3月的版本和2020年09月19日版本）](https://mrxn.net/Infiltration/449.html)

  web安全
  74cms
  ActiveMQ
  Adminer
  Adobe ColdFusion
  Apache
  Apache Dubbo
  Apache F...

  + 10301阅读
  + [4评论](https://mrxn.net/Infiltration/449.html#comment)
* [![fastadmin(V1.0.0.20200506_beta)前台getshell(文件上传解析)漏洞分析](images/img-008-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/415.html)

  + 2020/9/21
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [fastadmin(V1.0.0.20200506\_beta)前台getshell(文件上传解析)漏洞分析](https://mrxn.net/Infiltration/415.html)

  0x1.简介
  FastAdmin是一款基于ThinkPHP和Bootstrap的极速后台开发框架。
  补天平台介绍：近日，补天漏洞响应平台监测到互联网上出现Fastadmin文件上传漏洞，exp被公开。该漏洞源于网络系统或产品...

  + 8438阅读
  + [0评论](https://mrxn.net/Infiltration/415.html#comment)

深入探索

VPN服务

文本剥离工具

网络安全课程

网络安全会议

文件大小转换

Web安全课程

在线安全工具

JSON处理工具

网络安全培训

服务器安全服务

* [![深信服VPN 修改任意账户绑定手机号](images/img-009-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/382.html)

  + 2020/9/18
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [深信服VPN 修改任意账户绑定手机号](https://mrxn.net/Infiltration/382.html)

  https://路径/por/changetelnum.csp?apiversion=1newtel=TARGET\_PHONE&sessReq=clusterd&username=TARGET\_USERNAME&grpid=0...

  + 7121阅读
  + [0评论](https://mrxn.net/Infiltration/382.html#comment)
* [![CVE-2020-1472: NetLogon特权提升漏洞（接管域控制器）](images/img-010-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/342.html)

  + 2020/9/15
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [CVE-2020-1472: NetLogon特权提升漏洞（接管域控制器）](https://mrxn.net/Infiltration/342.html)

  0x01 更新概览
  2020年09月14日，360CERT监测发现 secura 公开了针对该漏洞研究报告及PoC，可造成 权限提升影响。本次更新标识该漏洞的利用工具公开，并可能在短时间内出现攻击态势。
  具体更新详情可参考:...

  + 5574阅读
  + [0评论](https://mrxn.net/Infiltration/342.html#comment)
* [![泛微OA云桥任意文件读取漏洞](images/img-011-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/323.html)

  + 2020/9/12
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [泛微OA云桥任意文件读取漏洞](https://mrxn.net/Infiltration/323.html)

  泛微0A的这个漏洞利用/wxjsapi/saveYZJFile接口获取filepath,返回数据包内出现了程序的绝对路径,攻击者可以通过返回内容识别程序运行路径从而下载数据库配置文件危害可见。
  1、downloadUrl参数修...

  + 7103阅读
  + [0评论](https://mrxn.net/Infiltration/323.html#comment)
* [![天融信数据防泄漏系统越权修改管理员密码](images/img-012-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/317.html)

  + 2020/9/12
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [天融信数据防泄漏系统越权修改管理员密码](https://mrxn.net/Infiltration/317.html)

  无需登录权限,由于修改密码处未校验原密码,且/?module=auth\_user&action=mod\_edit\_pwd
  接口未授权访问,造成直接修改任意用户密码。:默认superman账户uid为1...

  + 5389阅读
  + [2评论](https://mrxn.net/Infiltration/317.html#comment)
* [![齐治堡垒机前台远程命令执行漏洞](images/img-013-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/297.html)

  + 2020/9/12
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [齐治堡垒机前台远程命令执行漏洞](https://mrxn.net/Infiltration/297.html)

  齐治堡垒机前台远程命令执行漏洞（CNVD-2019-20835）
  未授权无需登录。
  1、访问 http://10.20.10.11/listener/cluster\_manage.php  :返回 "OK".
  ...

  + 6250阅读
  + [0评论](https://mrxn.net/Infiltration/297.html#comment)
* [![用友GRP-u8 注入+天融信TopApp-LB 负载均衡系统sql注入](images/img-014-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/292.html)

  + 2020/9/11
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [用友GRP-u8 注入+天融信TopApp-LB 负载均衡系统sql注入](https://mrxn.net/Infiltration/292.html)

  用友GRP-U8R10行政事业财务管理软件是用友公司专注于国家电子政务事业，基于云计算技术所推出的新一代产品，是我国行政事业财务领域最专业的政府财务管理软件。
  该系统被曝存在命令执行漏洞，当用户可以控制命令执行函...

  + 6142阅读
  + [0评论](https://mrxn.net/Infiltration/292.html#comment)
* [![绿盟UTS综合威胁探针管理员任意登录复现](images/img-015-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/276.html)

  + 2020/9/11
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [绿盟UTS综合威胁探针管理员任意登录复现](https://mrxn.net/Infiltration/276.html)

  背景：
  绿盟全流量威胁分析解决方案针对原始流量进行采集和监控，对流量信息进行深度还原、存储、查询和分析，可以及时掌握重要信息系统相关网络安全威胁风险，及时检测漏洞、病毒木马、网络攻击情况，及时发现网络安全事件线索，及时通报预警重大网络安全...

  + 6906阅读
  + [0评论](https://mrxn.net/Infiltration/276.html#comment)
* [![HW礼盒：深信服edr RCE，天融信dlp unauth和通达OA v11.6版本RCE](images/img-016-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/671.html)

  + 2020/8/20
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [HW礼盒：深信服edr RCE，天融信dlp unauth和通达OA v11.6版本RCE](https://mrxn.net/Infiltration/671.html)

  HW礼盒，请查收：
  深信服edr RCE：
  https://ip+端口/tool/log/c.php?strip\_slashes=system&host=id 即可执行命令，
  除上面之外，还有任意文件读取，验证码绕过，还有就是rce。
  任意...

  + 5351阅读
  + [0评论](https://mrxn.net/Infiltration/671.html#comment)
* [![绕过AMSI执行powershell脚本](images/img-017-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/667.html)

  + 2020/7/2
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [绕过AMSI执行powershell脚本](https://mrxn.net/Infiltration/667.html)

  简单的演示下从老外哪里学来的bypass AMSI 的姿势，看下效果图: 
   
  绕过AMSI执行powershell脚本
  AMSI的全称是反恶意软件扫描接口（Anti-Malware Scan In...

  + 3084阅读
  + [3评论](https://mrxn.net/Infiltration/667.html#comment)
* [![ThinkCMF5.x以下漏洞合集](images/img-018-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/644.html)

  + 2019/10/28
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [ThinkCMF5.x以下漏洞合集](https://mrxn.net/Infiltration/644.html)

  前台SQL注入:
  需要普通用户权限，默认可注册
  paylaod:
  POST /ThinkCMFX/index.php?g=portal&m=article&a=ed...

  + 9810阅读
  + [0评论](https://mrxn.net/Infiltration/644.html#comment)
* [![ThinkCMF2.2.2前台直接getshell+任意文件包含漏洞](images/img-019-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/642.html)

  + 2019/10/25
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [ThinkCMF2.2.2前台直接getshell+任意文件包含漏洞](https://mrxn.net/Infiltration/642.html)

  0x00 简介
      ThinkCMF是一款基于ThinkPHP+MySQL开发的开源中文内容管理框架。ThinkCMF提出灵活的应用机制，框架自身提供基础的管理功能，而开发者可以根据自身的需求以应用的形式进行扩展。每...

  + 7650阅读
  + [0评论](https://mrxn.net/Infiltration/642.html#comment)
* [![WinRAR 5.80 XML 注入漏洞和拒绝服务攻击漏洞](images/img-020-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/641.html)

  + 2019/10/23
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [WinRAR 5.80 XML 注入漏洞和拒绝服务攻击漏洞](https://mrxn.net/Infiltration/641.html)

  0x00背景介绍 
  WinRAR，是Windows标配的压缩软件，大家都不陌生。
  0x01漏洞描述 
  但是最近这两天winrar 5.80爆出了两个漏洞，一个是XML注入漏洞，一个是拒绝服务攻击漏洞。
  0x02漏洞复现POC&nbs...

  + 4213阅读
  + [0评论](https://mrxn.net/Infiltration/641.html#comment)
* [![CNVD-C-2019-48814 Weblogic wls9_async_response 反序列](images/img-021-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/638.html)

  + 2019/10/17
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [CNVD-C-2019-48814 Weblogic wls9\_async\_response 反序列](https://mrxn.net/Infiltration/638.html)

  0x1.背景
  首先，CNVD收录了由中国民生银行股份有限公司报送的Oracle WebLogic wls9-async反序列化远程命令执行漏洞（CNVD-C-2019-48814）。
  0x2.漏洞描述
  攻击者利用该漏洞，可在未授权的情况下远程执行命令。从相关...

  + 5151阅读
  + [1评论](https://mrxn.net/Infiltration/638.html#comment)
* [![CVE-2019-17624-X.Org X Server 1.20.4 - Local Stack Overflow-Linux图形界面X Server本地栈溢出POC](images/img-022-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/636.html)

  + 2019/10/16
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [CVE-2019-17624-X.Org X Server 1.20.4 - Local Stack Overflow-Linux图形界面X Server本地栈溢出POC](https://mrxn.net/Infiltration/636.html)

  0x1 简单介绍：
  X Server 是绝大对数Linux发行版和Unix系统的基础图形界面程序，是系统标配。而此程序也是以Root权限启动的，因而成功溢出它而获得的shell，也是root权限。
  0x2 漏洞相关信息：
  # 时间: 2019-10-1...

  + 2706阅读
  + [0评论](https://mrxn.net/Infiltration/636.html#comment)
* [![从朋友圈XX中奖getshell到提权服务器过程简单记录](images/img-023-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/632.html)

  + 2019/10/13
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [从朋友圈XX中奖getshell到提权服务器过程简单记录](https://mrxn.net/Infiltration/632.html)

  注意：所有的过程仅供渗透学习研究参考，禁止用于他途。
  建议学习渗透的朋友搜索一些非法网站的关键词来进行实战练习！干爆他们！
  0x1 背景：
  在朋友圈发现小姨转发了一篇XXX中奖,打开一开是XX彩票,其实就是菠菜的皮，果断先劝小姨删掉这条朋友圈，就有...

  + 4187阅读
  + [2评论](https://mrxn.net/Infiltration/632.html#comment)
* [![某站禁用各种函数情况下的 Thinkphp5.x 绕过 Getshell](images/img-024-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/618.html)

  + 2019/6/11
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [某站禁用各种函数情况下的 Thinkphp5.x 绕过 Getshell](https://mrxn.net/Infiltration/618.html)

  ThinkPHP 的站，且存在 ThinkPHP 5.0.x 远程命令执行漏洞，并且开了 debug 模式，但是⽬标用的是ThinkPHP5.0.20，⼀开始⽤网络上的 poc 打怎么都不成功。
  第一个问题是，目标 PHP 禁⽤了命令执行的函数，比如执行...

  + 11082阅读
  + [3评论](https://mrxn.net/Infiltration/618.html#comment)
* [![分分钟干死你的WordPress网站或者任意网站](images/img-025-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/dos-all-wordpressite-under4-9-2-and-other-websites.html)

  + 2018/3/2
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [分分钟干死你的WordPress网站或者任意网站](https://mrxn.net/Infiltration/dos-all-wordpressite-under4-9-2-and-other-websites.html)

  今天到处逛博客看到一个新（旧）闻：WordPress4.9.2（含）以前的网站含有DoS漏洞，可以用一台电脑轻松down掉网站。来源链接； CVE；PoC （这个POC只适合python2.7+，python3，并不适合，我作了修改使其能在...

  + 4139阅读
  + [8评论](https://mrxn.net/Infiltration/dos-all-wordpressite-under4-9-2-and-other-websites.html#comment)
* [![Linux下利用SUID提权](images/img-026-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/lunix-suid-improve-purview.html)

  + 2017/11/1
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [Linux下利用SUID提权](https://mrxn.net/Infiltration/lunix-suid-improve-purview.html)

  今天给大家带来的是linux下的提权技巧。SUID是Linux的一种权限机制，具有这种权限的文件会在其执行时，使调用者暂时获得该文件拥有者的权限。如果拥有SUID权限，那么就可以利用系统中的二进制文件和工具来进行root提权。已知的可用来提权的linux可行性...

  + 6589阅读
  + [2评论](https://mrxn.net/Infiltration/lunix-suid-improve-purview.html#comment)
* [![【奇技淫巧】利用mimikatz破解远程终端凭据，获取服务器密码](images/img-027-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/mimikatz-get-serverpassword.html)

  + 2017/10/21
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [【奇技淫巧】利用mimikatz破解远程终端凭据，获取服务器密码](https://mrxn.net/Infiltration/mimikatz-get-serverpassword.html)

  测试环境：windows 10
  道友们应该碰到过管理在本地保存远程终端的凭据，凭据里躺着诱人的胴体(服务器密码)，早已让我们的XX饥渴难耐了。但是，胴体却裹了一身道袍(加密)，待老衲操起法器将其宽衣解带。
  0x01 凭据管理器中查看Windows凭...

  + 5633阅读
  + [2评论](https://mrxn.net/Infiltration/mimikatz-get-serverpassword.html#comment)
* [![MySQL注入绕过新思路](images/img-028-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/569.html)

  + 2017/5/11
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [MySQL注入绕过新思路](https://mrxn.net/Infiltration/569.html)

  哈哈哈哈嘿嘿嘿嘿 今天带来MySQL的新姿势,姿势对不对,你们指教-\_-
  1.带内/带外
  传统的Insert、Update是带内注入方式，直接从返回中提取到有用信息，例如时间盲注获取数据；带外注入则是间接的从外部服务...

  + 3727阅读
  + [0评论](https://mrxn.net/Infiltration/569.html#comment)
* [![0day来袭WordPress Core <= 4.7.4全版本密码重置漏洞](images/img-029-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/566.html)

  + 2017/5/4
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [0day来袭WordPress Core <= 4.7.4全版本密码重置漏洞](https://mrxn.net/Infiltration/566.html)

  这两天的wordpress总是不平静....今天刚刚爆出0day....
  漏洞概述
  漏洞编号：CVE-2017-8295
  漏洞发现者：dawid\_golunski
  漏洞危害：中/高...

  + 3191阅读
  + [2评论](https://mrxn.net/Infiltration/566.html#comment)
* [![WordPress<4.7.1 远程代码执行漏洞（非插件无需认证，附Poc,演示视频）](images/img-030-aa724e5cc05a.gif)](https://mrxn.net/Infiltration/565.html)

  + 2017/5/4
  + [渗透测试](https://mrxn.net/jswz/Infiltration)

  [WordPress<4.7.1 远程代码执行漏洞（非插件无需认证，附Poc,演示视频）](https://mrxn.net/Infiltration/565.html)

  漏洞概述
  漏洞编号：CVE-2016-10033
  漏洞发现者：dawid\_golunski
  漏洞危害：严重
  影响版本：WordPress <4.7.1
  漏洞描述：远程攻击者可以利用该漏...

  + 3895阅读
  + [0评论](https://mrxn.net/Infiltration/565.html#comment)

1 [2](https://mrxn.net/jswz/Infiltration/page/2)

(adsbygoogle = window.adsbygoogle || []).push({});