---
title: "金和OA KpiWhetherExistTemplateKpiXml.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-KpiWhetherExistTemplateKpiXml-sqli.html
asset_dir: assets/金和oa-kpiwhetherexisttemplatekpixml.aspx-sql注入漏洞
---

# 金和OA KpiWhetherExistTemplateKpiXml.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/29 13:30
- 533浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

安全研究报告

漏洞扫描服务

编码转换工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `KpiWhetherExistTemplateKpiXml.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `KpiWhetherExistTemplateKpiXml.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Appraise.dll` 将其进行反编译后找到 **KpiWhetherExistTemplateKpiXml** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  StreamReader streamReader = new StreamReader(this.Request.InputStream);
  if (this.Request["SelectValue"] == null)
    return;
  this.strSelectValue = this.Request["SelectValue"].ToString().Trim();
  this.Response.Write((object) this.m_AppraiseKip.GetTemplateKpiCount(this.strSelectValue));
  this.Response.End();
}
```

深入探索

Docker加速服务

云安全解决方案

传输层安全性协议

参数 `SelectValue` 被带入`GetTemplateKpiCount`方法

```
public int GetTemplateKpiCount(string SelectValueKpiID)
{
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  string str = $"Select count(*) AS TemplateKpiCount  From  TemplateKPI where TemplateKPI in (select KPICode From KPI Where DelFlag=0 AND KPIID in ({SelectValueKpiID})) ";
  int templateKpiCount = 0;
  DataTable dataTable1 = new DataTable();
  DataTable dataTable2 = dbOperator.ExecSQLReDataTable(str);
```

至此，就非常明了了，`SelectValue` 参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Appraise/KpiWhetherExistTemplateKpiXml.aspx/?SelectValue=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA KpiWhetherExistTemplateKpiXml.aspx SQL注入漏洞](images/img-001-e5dcb93eb83a.webp)](https://image.mrxn.net/85f43a75541e481da2a3dcaab13923b1.webp)

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
