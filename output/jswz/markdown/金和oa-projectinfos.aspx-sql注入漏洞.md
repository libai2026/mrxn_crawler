---
title: "金和OA ProjectInfos.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ProjectInfos-sqli.html
asset_dir: assets/金和oa-projectinfos.aspx-sql注入漏洞
---

# 金和OA ProjectInfos.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/13 13:15
- 321浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

云安全解决方案

Docker加速服务

代码安全审计

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ProjectInfos.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ProjectInfos.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **ProjectInfos** 的处理逻辑

深入探索

编程语言教程

SQL注入防护

技术文章订阅

```
protected void Page_Load(object sender, EventArgs e)
{
  this.projid = this.Request["projid"];
  if (((Control) this).Page.IsPostBack)
    return;
  DataSet projectinfos = this.ch.GetProjectinfos(this.projid);
```

跟进`GetProjectinfos`方法

```
public DataSet GetProjectinfos(string projid)
{
  return this.db.ExecSQLReDataSet($"{$"{$"select top 1 * from vw_hyz_project where 项目主键={projid}; "}select distinct 自定义名称,自定义值 from vw_hyz_project where 项目主键={projid}; "}select distinct 项目成员 from vw_hyz_project where 项目主键={projid}; ");
}
```

至此，就非常明了了，参数`projid`被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/BudgetExecution/ProjectInfos.aspx/?projid=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ProjectInfos.aspx SQL注入漏洞](images/img-001-6f9301c3c60c.webp)](https://image.mrxn.net/5d48e4c6c926441a9a11841d02b0d4ae.webp)

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
