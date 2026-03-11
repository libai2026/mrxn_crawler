---
title: "金和OA ReportParaList.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ReportParaList-sqli.html
asset_dir: assets/金和oa-reportparalist.aspx-sql注入漏洞
---

# 金和OA ReportParaList.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/27 13:31
- 374浏览
- [0评论](#comment)
- 10分钟阅读

深入探索

技术文章订阅

漏洞扫描服务

安全研究工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ReportParaList.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

Web安全课程

SQL注入检测工具

安全工具开发

根据 `ReportParaList.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.BIframe.dll` 将其进行反编译后找到 **ReportParaList** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitParam();
  if (!this.IsPostBack)
  {
    if (this.Request.QueryString["Reportid"] != null)
    {
      this.Reportid = this.Request.QueryString["Reportid"].ToString();
      this.getParaList(this.Reportid);
```

参数`Reportid`被带入`getParaList`方法

```
public DataTable getparalist(string Reportid)
{
  return this.db.ExecSQLReDataTable($"select * from BI_paras where ReportId ='{Reportid}'");
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.BIframe/ReportParaList.aspx/?Reportid=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

深入探索

授权

恶意软件分析工具

服务器安全服务

[![金和OA ReportParaList.aspx SQL注入漏洞](images/img-001-c81d499ce60c.webp)](https://image.mrxn.net/70a265d4b9364e55959078f5ed538be6.webp)

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
