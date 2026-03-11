---
title: "红海云eHR StWasAssessDept SQL注入漏洞"
source: https://mrxn.net/jswz/redseaplatform-submitStWasAssessDept-StWasAssessDept-sqli.html
asset_dir: assets/红海云ehr-stwasassessdept-sql注入漏洞
---

# 红海云eHR StWasAssessDept SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/2 08:28
- 359浏览
- [0评论](#comment)
- 7分钟阅读

深入探索

SQL

身份验证

软件

---

# 漏洞简介

红海云eHR系统中的StWasAssessDeptController（submitStWasAssessDept/StWasAssessDept.mob）模块存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL查询语句，绕过系统认证，实现对数据库的非法访问，获取敏感信息（如用户凭证、个人数据等），甚至在特定条件下可能导致数据库被完全控制，影响范围包括数据访问权限和系统控制权限。

# 影响版本

# fofa语法

> body="/RedseaPlatform/skins/images/favicon.ico"

# 漏洞分析

> 鉴权相关看之前的 [红海云eHR BossIndex SQL注入漏洞](https://mrxn.net/jswz/redseaplatform-BossIndex-sqli.html) 分析鉴权部分

进入本文的正题 `StWasAssessDeptController` ，看下它的 **submitStWasAssessDept/StWasAssessDept** 方法实现逻辑

深入探索

企业安全咨询

编程语言教程

授权

[![红海云eHR StWasAssessDept SQL注入漏洞](images/img-001-ceabda68abf1.webp)](https://image.mrxn.net/b75b308825944ef9a3f76e01e78f7a8d.webp)

如图所示，参数 `String userId = req.getParameter("userId");` 被直接拼接进 `"SELECT USER_NAME FROM PT_USERS WHERE USER_ID='" + userId + "'";` SQL语句中执行，无任何过滤或校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，朴实无华。

# 漏洞复现

```
POST /RedseaPlatform/submitStWasAssessDept/StWasAssessDept.mob HTTP/1.1
Host: redseaplatform.mrxn.net
Content-Type: application/x-www-form-urlencoded

userId=SQLI_POC
```

[![红海云eHR StWasAssessDept SQL注入漏洞](images/img-002-20ff06eff68f.webp)](https://image.mrxn.net/7584ab3e759745bab375004ba5d367c0.webp)

成功延 2 秒

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
