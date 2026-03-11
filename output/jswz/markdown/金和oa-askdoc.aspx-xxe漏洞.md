---
title: "金和OA AskDoc.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-AskDoc-xxe.html
asset_dir: assets/金和oa-askdoc.aspx-xxe漏洞
---

# 金和OA AskDoc.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/24 13:31
- 342浏览
- [0评论](#comment)
- 8分钟阅读

深入探索

SQL注入检测工具

安全

Web安全书籍

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AskDoc.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `AskDoc.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Ask.dll` 将其进行反编译后找到 **AskDoc** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (((Control) this).Page.IsPostBack)
    return;
  this.ReadGlobal();
  if (this.Request.QueryString["GovFieldNormal"] != null)
  {
    string xml = this.Request.QueryString["GovFieldNormal"];
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(xml);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

深入探索

漏洞预警服务

授权

漏洞修复方案

# 漏洞复现

## XXE

```
GET /c6/Jhsoft.Web.Ask/AskDoc.aspx/?GovFieldNormal=XXE_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

在DNSLOG平台成功收到HTTP请求

网络安全

[![金和OA AskDoc.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#XXE](https://mrxn.net/tag/XXE)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [5.1.XXE](#toc-5-1-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
