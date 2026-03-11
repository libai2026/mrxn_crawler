---
title: "金和OA AttendWorkAttendance.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AttendWorkAttendance-sqli.html
asset_dir: assets/金和oa-attendworkattendance.aspx-sql注入漏洞
---

# 金和OA AttendWorkAttendance.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/12 13:31
- 235浏览
- [0评论](#comment)
- 15分钟阅读

深入探索

软件

SQL

服务器

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AttendWorkAttendance.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `AttendWorkAttendance.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.ExamineNod.dll` 将其进行反编译后找到 **AttendWorkAttendance** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.KeyCtrl("IndDiary");
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.Request.QueryString["UserID"] != null)
    this.UserID = this.Request.QueryString["UserID"].ToString();
  else if (this.Session["UserCode"] != null)
    this.UserID = this.Session["UserCode"].ToString();
  this.UserName = new JHSoft.ExamineNod.ExamineNod().GetUserNameByUserID(this.UserID);
  this.GetSearchLimit();
  this.InitData();
  if (((Control) this).Page.IsPostBack)
    ;
}
```

深入探索

技术文章订阅

安全

企业安全咨询

跟进`GetUserNameByUserID`方法

```
public string GetUserNameByUserID(string UserCode)
{
  string userNameByUserId = "";
  if (string.op_Equality(UserCode.ToString().Trim(), ""))
    return "";
  string str = $"select top 1 UserName from users where userid = '{UserCode}'";
  try
  {
    DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
    DataTable dataTable = dbOperator.ExecSQLReDataTable(str);
```

参数`UserID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.examinenod/AttendWorkAttendance.aspx/?UserID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA AttendWorkAttendance.aspx SQL注入漏洞](images/img-001-475214b8d7b1.webp)](https://image.mrxn.net/7b245661e3064f6587e26b23f665a0f4.webp)

成功延时 4 秒

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
