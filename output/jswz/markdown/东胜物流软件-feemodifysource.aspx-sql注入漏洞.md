---
title: "东胜物流软件 FeeModifySource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-Shipping-FeeModifySource-sqli.html
asset_dir: assets/东胜物流软件-feemodifysource.aspx-sql注入漏洞
---

# 东胜物流软件 FeeModifySource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/4 08:26
- 359浏览
- [0评论](#comment)
- 40分钟阅读

深入探索

计算机安全

数据库

身份验证

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 Shipping/FeeModifySource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"
>
> SQL注入检测工具

# 漏洞分析

根据 Shipping/FeeModifySource.aspx 的代码引用`<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="FeeModifySource.aspx.cs" Inherits="DSWeb.Shipping.FeeModifySource" %>`，在dll中找到`DSWeb.Shipping.FeeModifySource`的逻辑实现

代码安全审计

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request.QueryString["handle"] != null)
    this.strHandle = this.Request.QueryString["handle"].ToString().Trim().ToLower();
  if (this.Request.QueryString["oplb"] != null)
    this.stroplb = this.Request.QueryString["oplb"].ToString();
  if (this.Request.QueryString["id"] != null)
    this.strFeeID = this.Request.QueryString["id"].ToString().Trim().ToLower();
  if (this.Request.QueryString["applytype"] != null)
    this.iApplyType = int.Parse(this.Request.QueryString["applytype"].ToString().Trim());
  if (this.Request.QueryString["applystate"] != null)
    this.iApplyState = int.Parse(this.Request.QueryString["applystate"].ToString().Trim());
  if (this.Request.QueryString["checkstate"] != null)
    this.iCheckState = int.Parse(this.Request.QueryString["checkstate"].ToString().Trim());
  if (this.strHandle.Equals("apply"))
  {
    string cells = this.GetCells(this.strFeeID, this.iApplyType, this.iApplyState, this.iCheckState);
    this.Response.ContentType = "text/xml";
    cells.Replace("&", "&amp;");
    this.Response.Write(cells);
  }
  else if (this.strHandle.Equals("exist"))
  {
    this.Response.Write(this.IsExistFee(this.strFeeID));
  }
  else
  {
    this.Response.ContentType = "text/xml";
    this.Response.Write("-2");
  }
}
```

深入探索

安全运维咨询

网络安全会议

网络安全培训

当**handle=apply且applystate=0**时，跟进`GetCells`方法

```
private string GetCells(
  string tempFeeID,
  int tempApplyType,
  int tempApplyState,
  int tempCheckState)
{
  FeeDA feeDa = new FeeDA();
  FeeModifyDA feeModifyDa = new FeeModifyDA();
  if (tempApplyState == 0)
  {
    DataTable dataTable = new DataTable();
    string strSql = $" SELECT {""} GID, FEESTATUS, FEENAME, CUSTOMERNAME, UNIT, UNITPRICE, QUANTITY,COMMISSIONRATE,AMOUNT, CURRENCY,  EXCHANGERATE,FEEFRT,REMARK,ISADVANCEDPAY  FROM ch_fee WHERE 1> 0 {$" AND GID = '{tempFeeID}'"} {" ORDER BY ENTERDATE ASC "}";
    DataTable statusNameTable = this.getStatusNameTable(feeDa.GetExcuteSql(strSql).Tables[0]);
......
```

参数`tempFeeID`即外部用户可控参数**id**被直接拼接在`string strSql = $" SELECT {""} GID, FEESTATUS, FEENAME, CUSTOMERNAME, UNIT, UNITPRICE, QUANTITY,COMMISSIONRATE,AMOUNT, CURRENCY, EXCHANGERATE,FEEFRT,REMARK,ISADVANCEDPAY FROM ch_fee WHERE 1> 0 {$" AND GID = '{tempFeeID}'"} {" ORDER BY ENTERDATE ASC "}";`SQL语句中执行，无任何过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

以及**当 applystate!=0 时的多个分支**

漏洞修复方案

例如 `applytype=1, checkstate=1` 时：

```
strSql1 = $"SELECT GID,APPLYSTATUS, FEENAME, CUSTOMERNAME, UNIT, UNITPRICE, QUANTITY,COMMISSIONRATE,AMOUNT, CURRENCY,EXCHANGERATE,FRT,REMARK,ISADVANCEDPAY FROM ch_fee_modify WHERE FEEID = '{tempFeeID}' AND APPLYTYPE = {tempApplyType} AND APPLYSTATUS = {1} ";
```

1. **参数类型确认**：`tempFeeID` 为字符串类型（在SQL中使用单引号包裹）
2. **过滤机制缺失**：仅进行了 `.Trim().ToLower()` 处理，未做SQL注入防护
3. **拼接方式**：使用字符串插值 `$"{tempFeeID}"` 直接拼接，未使用参数化查询
4. **执行方式**：通过 `feeDa.GetExcuteSql(strSql)` 直接执行拼接的SQL

根据代码逻辑，触发不同SQL注入需要满足以下条件：

| 场景 | handle | applystate | applytype | checkstate | 触发位置 |
| --- | --- | --- | --- | --- | --- |
| 场景1 | apply | 0 | 任意 | 任意 | ch\_fee表查询 |
| 场景2 | apply | 非0 | 1 | 1 | ch\_fee\_modify表(APPLYSTATUS=1) |
| 场景3 | apply | 非0 | 1 | 2 | ch\_fee\_modify表(APPLYSTATUS=2或3) |
| 场景4 | apply | 非0 | 1 | 3 | ch\_fee\_modify表(所有记录) |
| 场景5 | apply | 非0 | 2 | 1 | ch\_fee\_modify表(APPLYSTATUS=1) |
| 场景6 | apply | 非0 | 2 | 2 | ch\_fee\_modify表(APPLYSTATUS=2或3) |
| 场景7 | apply | 非0 | 2 | 3 | ch\_fee\_modify表(所有记录) |

# 漏洞复现

```
GET /Shipping/FeeModifySource.aspx?handle=apply&applystate=1&checkstate=1&applytype=1&oplb=1&id=SQLI_POC&val=b9733091-e978-4cb5-a845-765a82ca1217 HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 FeeModifySource.aspx SQL注入漏洞](images/img-001-71080ebcb63a.webp)](https://image.mrxn.net/6635ba5969ac4949b74f432bfeda5ed0.webp)

成功延时 5 秒

网络安全

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
