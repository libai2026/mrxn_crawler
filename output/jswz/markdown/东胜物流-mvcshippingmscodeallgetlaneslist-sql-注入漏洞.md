---
title: "东胜物流 /MvcShipping/MsCodeAll/GetLanesList SQL 注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsCodeAll-GetLanesList-sqli.html
asset_dir: assets/东胜物流-mvcshippingmscodeallgetlaneslist-sql-注入漏洞
---

# 东胜物流 /MvcShipping/MsCodeAll/GetLanesList SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/4 15:31
- 329浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

云安全解决方案

漏洞预警服务

计算机安全

---

# 漏洞简介

东胜物流[软件](#)是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 /MvcShipping/MsCodeAll/GetLanesList 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

根据.NET MVC特性找到MsCodeAllController下的GetLanesList方法，看下它的实现

```
public ContentResult GetLanesList(string condition, string sort)
{
  List<Code_lanesmb> lanesList = MsCodeAllDAL.GetLanesList(condition, sort);
  string str = JsonConvert.Serialize(new
  {
    Success = true,
    Message = "查询成功",
    totalCount = lanesList.Count,
    data = Enumerable.ToList<Code_lanesmb>((IEnumerable<Code_lanesmb>) lanesList)
  });
  return new ContentResult() { Content = str };
}
```

深入探索

数据库

Docker加速服务

授权

参数condition、sort被带入MsCodeAllDAL.GetLanesList，跟进看下

代码安全审计

```
public static List<Code_lanesmb> GetLanesList(string strCondition, string companyid, string sort = null)
{
  StringBuilder strSql = new StringBuilder();
  strSql.Append(" SELECT ");
  strSql.Append(" GID,LANEID,LANE,LANEEN,EDICODE,OP,DOC,CUSTSERVICE");
  strSql.Append(" from code_lanes ");
  if (!string.IsNullOrEmpty(strCondition))
    strSql.Append(" WHERE " + strCondition);
  string str = DatasetSort.Getsortstring(sort);
  if (!string.IsNullOrEmpty(str))
    strSql.Append(" order by " + str);
  else
    strSql.Append(" order by LANEID");
  return MsCodeAllDAL.SetLanesData(strSql);
}
```

深入探索

防火墙软件

安全研究报告

文本剥离工具

至此[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞成因就非常明显了：

漏洞扫描服务

- 在 `MsCodeAllDAL.GetLanesList` 方法中，程序通过字符串拼接的方式构建 SQL 查询语句。
- 参数 `strCondition` 直接来源于控制器 `MsCodeAllController.GetLanesList` 的输入参数 `condition`。该参数未经过任何参数化处理、类型转换或白名单过滤，直接拼接到 SQL 字符串中。
- 虽然使用了 `DatasetSort.Getsortstring` 转换，但如果该工具类未进行严格的字段白名单过滤，攻击者可以通过 `sort` 参数注入 SQL 片段（如基于报错的注入或时间盲注）。
- 使用了 `DatabaseFactory.CreateDatabase().ExecuteReader` 执行原始 SQL 字符串。

# 漏洞复现

```
GET /MvcShipping/MsCodeAll/GetLanesList?condition=SQLI_POC&sort=LANEID HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流 /MvcShipping/MsCodeAll/GetLanesList SQL 注入漏洞](images/img-001-f4b3be9a1b51.webp)](https://image.mrxn.net/baa40d4e91494d13995ae8ae19e39743.webp)

通过联合注入，成功在响应回显当前数据库版本信息

物流软件安全

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
