---
title: "金和OA ReportSetting.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ReportSetting-sqli.html
asset_dir: assets/金和oa-reportsetting.aspx-sql注入漏洞
---

# 金和OA ReportSetting.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/28 13:31
- 314浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

软件

SQL

数据库

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ReportSetting.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `ReportSetting.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.BIframe.dll` 将其进行反编译后找到 **ReportSetting** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitParam();
  Utility.RegisterTypeForAjax(typeof (ReportSetting), ((Control) this).Page);
  if (!this.IsPostBack)
  {
    this.InitControl();
    this.RptID = string.Empty;
    if (this.Request.QueryString["Reportid"] != null)
    {
      this.strAddFlag = "1";
      DataTable setinglist = this.cmd.getSetinglist($" and BIno='{this.Request.QueryString["Reportid"].ToString()}'");
      ((HtmlInputControl) this.txtName).Value = setinglist.Rows[0]["CNname"].ToString();
```

参数`Reportid`被带入`getSetinglist`方法

```
public DataTable getSetinglist(string condition)
{
  return this.db.ExecSQLReDataTable("select a.*,a.reporttype,b.typename from BI_ReportInfo a left join BI_ReportType b on a.typecode = b.typecode where a.delflag =0 " + condition);
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.BIframe/ReportSetting.aspx/?Reportid=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ReportSetting.aspx SQL注入漏洞](images/img-001-d9183359d1af.webp)](https://image.mrxn.net/a00e2f42d65041f6b6ea8cff5dcdf979.webp)

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
