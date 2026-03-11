---
title: "东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-SeaiInfoLCL-WmsRateLCLGridSource-sqli.html
asset_dir: assets/东胜物流软件-wmsratelclgridsource.aspx-sql注入漏洞
---

# 东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/20 15:26
- 569浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

计算机安全

漏洞扫描服务

Web安全课程

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 WmsRateLCLGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `WmsRateLCLGridSource.aspx` 的代码引用 `DSWeb.SeaiInfoLCL.WmsRateLCLGridSource`，在dll中找到它的逻辑实现

主要就是根据`read`参数的值来进行处理不同的分支逻辑

SQL注入防护

[![东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](images/img-001-4f6bd67c3345.webp)](https://image.mrxn.net/9680137af95d4d7db94289d5135a4390.webp)

用户通过 `Request.QueryString` 控制 `handle`, `tb`, `linkgid` 等参数，根据`handle`的不同值 进入不同的方法，

漏洞扫描服务

当**handle=getiswmsin**时，进入**getiswmsin**方法

[![东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](images/img-002-d6f737296031.webp)](https://image.mrxn.net/d04c1982bc5b406784db43947917d56c.webp)

`str`的值被直接拼接在`strSQL`语句里，而`str`又来自**gids**请求参数

[![东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](images/img-003-a8a39743789c.webp)](https://image.mrxn.net/580bba09ae70476c9e1dd71ec8b9a8d4.webp)

然后用**GetStrSQL**进行执行，全程无过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

同时其他多个方法也是存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

[![东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](images/img-004-135401039f15.webp)](https://image.mrxn.net/c1f54443ef5b488a82c410a3e648b5c9.webp)

# 漏洞复现

```
GET /SeaiInfoLCL/WmsRateLCLGridSource.aspx?handle=getiswmsin&gids=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 WmsRateLCLGridSource.aspx SQL注入漏洞](images/img-005-e14c264949cf.webp)](https://image.mrxn.net/5347762623ee47f8927acf6d79e5ae8d.webp)

通过报错注入在响应里回显数据库版本信息。

网络安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
