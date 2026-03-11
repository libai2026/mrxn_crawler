---
title: "东胜物流软件 MsChDuiController 多个SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html
asset_dir: assets/东胜物流软件-mschduicontroller-多个sql注入漏洞
---

# 东胜物流软件 MsChDuiController 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/26 08:37
- 227浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

Nessus

文件大小转换

Web安全课程

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 MsChDuiController 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

看下`MsChDuiController`方法下的**GetDetailList** action是如何实现的

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-001-4eb191aef8fa.webp)](https://image.mrxn.net/2c40b55a880048c98af70b2e2430d4d0.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-002-e077a638a6dc.webp)](https://image.mrxn.net/f860ab4535004999886c242674edc762.webp)

如上图所示，参数**condition**是被直接拼接进SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

深入探索

JSON处理工具

漏洞扫描服务

恶意软件分析工具

其他action也是差不多的问题

SQL注入检测工具

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-003-0bfaa520ac39.webp)](https://image.mrxn.net/01065d33afcd406bab883bb244d6e2be.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-004-65a8d41d2023.webp)](https://image.mrxn.net/6fe32ec172434ade9cc3732fcabd501e.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-005-7532b06cac65.webp)](https://image.mrxn.net/34fc9320a5e54072a6af4e7f458d289f.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-006-4c487a12fbbe.webp)](https://image.mrxn.net/cab15652d7724365a599ff76915b4f02.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-007-0a85c0820d59.webp)](https://image.mrxn.net/3ac64409038d4d41892543c8aa45769f.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-008-8b1286fa3aac.webp)](https://image.mrxn.net/5000011f31e143cea5d4d2054acae850.webp)

# 漏洞复现

```
GET /MvcShipping/MsChDui/GetDetailList?condition=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-009-88a374feebff.webp)](https://image.mrxn.net/2daad20d262b453280fe0b55db0e6be1.webp)

成功利用报错注入在响应里回显数据库版本信息

代码安全审计

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
