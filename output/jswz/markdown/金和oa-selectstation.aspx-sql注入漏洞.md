---
title: "金和OA SelectStation.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-SelectStation-sqli.html
asset_dir: assets/金和oa-selectstation.aspx-sql注入漏洞
---

# 金和OA SelectStation.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/31 13:30
- 445浏览
- [0评论](#comment)
- 17分钟阅读

深入探索

SQL

软件

木马

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SelectStation.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `SelectStation.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Appraise.dll` 将其进行反编译后找到 **SelectStation** 的处理逻辑

深入探索

计算机安全

漏洞修复方案

安全研究工具

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  Localization.SessionCulture((Page) this);
  this.InitText();
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  string AppraiseType = "";
  if (this.Request.QueryString["AppraiseType"] != null)
    AppraiseType = this.Request.QueryString["AppraiseType"].ToString();
  if (((Control) this).Page.IsPostBack)
    return;
  this.InitPage(AppraiseType);
}
```

参数 `AppraiseType` 被带入`InitPage`方法

```
private void InitPage(string AppraiseType)
{
  DataSet stationData = new JHSoft.Appraise.AppraiseSet().GetStationData(AppraiseType);
```

跟进`GetStationData`

```
public DataSet GetStationData(string AppraiseType)
{
  DataSet stationData = this.db.ExecSQLReDataSet($"select StaID,StaName from Station Where DelFlag=0 and StaID not in (select AppraiseStation from appraiseSet where AppraiseType = '{AppraiseType}' and DelFlag=0 and AppraiseStation is not null)  order by StaName Asc  ");
  if (this.db.IsError)
    this.strErrMessage = this.db.ErrorMessage;
  return stationData;
}
```

至此，就非常明了了，`AppraiseType` 参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Appraise/SelectStation.aspx/?AppraiseType=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA SelectStation.aspx SQL注入漏洞](images/img-001-823f5e3abd57.webp)](https://image.mrxn.net/52d81751e5d844ffb439a9a9df1d43b4.webp)

成功延时 5 秒

代码安全审计

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
