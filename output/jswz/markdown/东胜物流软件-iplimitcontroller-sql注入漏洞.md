---
title: "东胜物流软件 IPLimitController SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-IPLimit-UpdateIPAddress-sqli.html
asset_dir: assets/东胜物流软件-iplimitcontroller-sql注入漏洞
---

# 东胜物流软件 IPLimitController SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/2/24 08:32
- 276浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

SQL

信息管理

身份验证

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 IPLimitController 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

安全工具开发

授权

云安全解决方案

看下`IPLimitController`方法下的**UpdateIPAddress** action是如何实现的

[![东胜物流软件 IPLimitController SQL注入漏洞](images/img-001-02fbf5de6e52.webp)](https://image.mrxn.net/c02510f495e94a708074c16d4de77e98.webp)

如上图所示，参数name是被直接拼接进SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /MvcShipping/IPLimit/UpdateIPAddress HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

name=SQLI_POC
```

[![东胜物流软件 IPLimitController SQL注入漏洞](images/img-002-8dd7ca8c7745.webp)](https://image.mrxn.net/9183fb368f67420f80ecfa53a7468dbc.webp)

成功延时 3 秒

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
