---
title: "金和OA AppraiseStationSetUpdate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AppraiseStationSetUpdate-sqli.html
asset_dir: assets/金和oa-appraisestationsetupdate.aspx-sql注入漏洞
---

# 金和OA AppraiseStationSetUpdate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/23 13:26
- 563浏览
- [4评论](#comment)
- 20分钟阅读

深入探索

服务器

数据库

SQL

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AppraiseStationSetUpdate.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AppraiseStationSetUpdate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Appraise.dll` 将其进行反编译后找到 **AppraiseStationSetUpdate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  Localization.SessionCulture((Page) this);
  this.InitText();
  ((HtmlControl) this.txt_BehaveCodeName).Attributes.Add("title", this.SelectPerson);
  if (!((Control) this).Page.IsPostBack)
  {
    this.ToolsBar1.Buttons.Add("../images/ico_28.gif", this.btnCreateColl);
    this.ToolsBar1.Buttons.Add("../images/ico_26.gif", this.btnDelColl);
  }
  ((HtmlControl) this.txt_BehaveCodeName).Disabled = true;
  if (this.Request["id"] != null)
  {
    ((HtmlInputControl) this.txt_BehaveCode).Value = this.Request["id"].ToString().Trim();
    ((HtmlInputControl) this.txt_BehaveCodeName).Value = this.Request["Name"].ToString().Trim();
    this.m_dss = this.m_AppraiseTemplate.GetAppraiseStationInfo(((HtmlInputControl) this.txt_BehaveCode).Value);
```

参数 `id` 被带入`GetAppraiseStationInfo`方法

```
public DataSet GetAppraiseStationInfo(string regCode)
{
  if (string.op_Equality(regCode.ToString().Trim(), ""))
    return (DataSet) null;
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  DataSet dataSet = new DataSet();
  string str = $"Select * From  AppraiseStation Where regCode ='{regCode}'";
  DataSet appraiseStationInfo = dbOperator.ExecSQLReDataSet(str);
```

至此，就非常明了了，`id` 参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Appraise/AppraiseStationSetUpdate.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA AppraiseStationSetUpdate.aspx SQL注入漏洞](images/img-001-393ae449d073.webp)](https://image.mrxn.net/c8496455fdef4503bfc4fcdee1bd1c63.webp)

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
