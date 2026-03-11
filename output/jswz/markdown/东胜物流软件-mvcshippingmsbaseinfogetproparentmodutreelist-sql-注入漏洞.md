---
title: "东胜物流软件 /MvcShipping/MsBaseInfo/GetProParentModuTreeList SQL 注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsBaseInfo-GetProParentModuTreeList-sqli.html
asset_dir: assets/东胜物流软件-mvcshippingmsbaseinfogetproparentmodutreelist-sql-注入漏洞
---

# 东胜物流软件 /MvcShipping/MsBaseInfo/GetProParentModuTreeList SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/30 15:31
- 275浏览
- [0评论](#comment)
- 43分钟阅读

深入探索

身份验证

软件

数据库

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 MvcShipping/MsBaseInfo/GetProParentModuTreeList 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

根据.NET MVC框架特点找到DSWeb.MvcShipping中对于路由的定义

```
using System.Web.Mvc;

#nullable disable
namespace DSWeb.MvcShipping;

public class MvcShippingRegistration : AreaRegistration
{
  public override string AreaName => "MvcShipping";

  public override void RegisterArea(AreaRegistrationContext context)
  {
    context.MapRoute("MvcShipping_default", "MvcShipping/{controller}/{action}/{id}", (object) new
    {
      action = "Index",
      id = UrlParameter.Optional
    });
  }
}
```

深入探索

恶意软件分析工具

云安全解决方案

网络安全培训

## `GetProParentModuTreeList`

在DSWeb.MvcShipping.Controllers下找到MsBaseInfoController里的**GetProParentModuTreeList()**方法

```
public ContentResult GetProParentModuTreeList(string PARENTID)
{
  List<CustomDbParamter> dbparams = new List<CustomDbParamter>();
  CustomDbParamter customDbParamter1 = new CustomDbParamter();
  ((DbParameter) customDbParamter1).ParameterName = "@oper";
  ((DbParameter) customDbParamter1).DbType = (DbType) 16 /*0x10*/;
  ((DbParameter) customDbParamter1).Direction = (ParameterDirection) 1;
  ((DbParameter) customDbParamter1).Value = (object) Convert.ToString(this.Session["USERID"]);
  dbparams.Add(customDbParamter1);
  CustomDbParamter customDbParamter2 = new CustomDbParamter();
  ((DbParameter) customDbParamter2).ParameterName = "@strCondition";
  ((DbParameter) customDbParamter2).DbType = (DbType) 16 /*0x10*/;
  ((DbParameter) customDbParamter2).Direction = (ParameterDirection) 1;
  ((DbParameter) customDbParamter2).Value = (object) $" and PARENTID='{PARENTID}'";
  dbparams.Add(customDbParamter2);
  string str = Convert.ToString(this.Session["LANGUAGES"]);
  string prcName = "P_userRight";
  if (string.op_Equality(str, "en-us"))
    prcName = "P_userRight_Ename";
  string rptJsonResult = RptHelper.GetRptJsonResult(0, 100, PubSysDAL.GetMsSqlPrcDataSet(prcName, dbparams, "Result_Set"), "Result_Set", false);
  return new ContentResult() { Content = rptJsonResult };
}
```

深入探索

SQL注入检测工具

安全运维咨询

Windows安全工具

非常明显的[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞：参数`PARENTID`被直接拼接进SQL语句中`$" and PARENTID='{PARENTID}'";`执行，从而导致的注入漏洞。

SQL注入防护

当然，此Controller下的多个方法也存在类似的SQL注入漏洞

## `GetCustomerRefList`

```
// MsBaseInfoDAL.cs
public static List<CustomerRefModel> GetCustomerRefList(string strCondition) {
    // ...
    if (!string.IsNullOrEmpty(strCondition))
        strSql.Append(" and " + strCondition); // 直接拼接外部输入
    // ...
    using (IDataReader idataReader = DatabaseFactory.CreateDatabase().ExecuteReader((CommandType) 1, strSql.ToString())) 
    // CommandType 1 是 CommandType.Text，直接执行拼接后的字符串
}
```

`condition` 参数完全受控于用户，攻击者可以构造恶意 SQL 语句，绕过正常的业务逻辑。由于是 MSSQL 环境，攻击者可以利用 `UNION SELECT` 获取其他表（如 `[user]`）的数据，或者利用 `WAITFOR DELAY` 进行时间盲注。

代码安全审计

## `GetModuTreeRefList`

```
// MsBaseInfoController.cs
public ContentResult GetModuTreeRefList(string PARENTID) {
    string strCondition = $"PARENTID='{PARENTID}'"; // 字符串插值拼接
    // 后续逻辑中虽然有 if else 判断 PARENTID 的值，但如果传入的值不匹配任何 if 条件，
    // strCondition 依然保持初始的拼接结果，并传入 DAL。
    List<ModuTreeRefModel> moduTreeRefList = DSWeb.MvcShipping.DAL.MsBaseInfoDAL.MsBaseInfoDAL.GetModuTreeRefList(strCondition, ...);
}
```

虽然代码中有针对特定 GUID 的 `if` 判断，但攻击者只需传入一个不符合这些条件的恶意字符串，即可绕过逻辑。

## `SaveUserQuerySetting`

```
// MsBaseInfoDAL.cs
public static DBResult SaveUserQuerySetting(..., string userid, string formname, ...) {
    // 虽然部分参数使用了参数化查询，但 Delete 语句是拼接的：
    DbCommand sqlStringCommand2 = database.GetSqlStringCommand($"Delete from user_query_setting where formname='{formname}' and userid='{userid}' ");
    database.ExecuteNonQuery(sqlStringCommand2, transaction);
}
```

攻击者可以通过 `formname` 参数注入恶意 SQL。由于紧接着会执行删除操作，这可能导致 `user_query_setting` 表中的数据被全部清空（通过 `1' OR '1'='1`）。

以及其他接口均存在类似的 `condition` 拼接问题，分析逻辑一致：

漏洞预警服务

- `GetPortRefList`
- `GetOurPortRefList`
- `GetOpEdiLog`
- `GetGoodsRefList`
- `GetStlModeList`
- `GetAllBANKList`
- `GetCodeRptFeeGroup`
- `GetCwAccitemsCurrencyList`

# 漏洞复现

```
GET /MvcShipping/MsBaseInfo/GetProParentModuTreeList?PARENTID=SQLI_POC&&_dc=1678901234567&page=1&start=0&limit=25 HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 /MvcShipping/MsBaseInfo/GetProParentModuTreeList SQL 注入漏洞](images/img-001-b3f4a1ee994d.webp)](https://image.mrxn.net/40d2a866e39444f98dab740acbba4193.webp)

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
- [4.1.GetProParentModuTreeList](#toc-4-1-)
- [4.2.GetCustomerRefList](#toc-4-2-)
- [4.3.GetModuTreeRefList](#toc-4-3-)
- [4.4.SaveUserQuerySetting](#toc-4-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
