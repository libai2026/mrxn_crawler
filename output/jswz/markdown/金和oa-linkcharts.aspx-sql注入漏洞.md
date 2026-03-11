---
title: "金和OA LinkCharts.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-LinkCharts-sqli.html
asset_dir: assets/金和oa-linkcharts.aspx-sql注入漏洞
---

# 金和OA LinkCharts.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/7 13:31
- 260浏览
- [0评论](#comment)
- 19分钟阅读

深入探索

物流软件安全

企业安全咨询

网络安全会议

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `LinkCharts.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `LinkCharts.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CrmWorkFlat.dll` 将其进行反编译后找到 **LinkCharts** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.strChartArea = this.CustomerDistribute(this.Request["DeptID"]);
}

public string CustomerDistribute(string strDept)
{
  this.fc.ChartDivID = nameof (CustomerDistribute);
  this.fc.Position = "static";
  this.fc.ChartHeight = "100%";
  this.fc.ChartWidth = "100%";
  this.fc.ChartPath = "../FusionCharts/Column2D.swf";
  DataSet dataSet = new DataSet();
  StringBuilder stringBuilder = new StringBuilder();
  DataSet customerDistribute = this.an.GetCustomerDistribute(strDept);
```

深入探索

授权

文件大小转换

漏洞扫描器

跟进`GetCustomerDistribute`方法

```
public DataSet GetCustomerDistribute(string strDept)
{
  return this.dbo.ExecSQLReDataSet($"select d.deptid,deptname,deptparentid,s.sortlevel from department d inner join sort s on d.deptid=s.sortobjectid where s.sorttype = 'dept' and deptparentid='{strDept}'" + " select sum(isnull(a.c,0)) c,sum(isnull(b.s,0)) s,a.deptid from(select count(customer_id) c,customer_manager,r.deptid from jhbj_crm_customer c inner join relationshipusers r on c.customer_manager = r.userid where customer_state <3 and isfromcompany = 0 group by customer_manager,r.deptid) a left join (select count(customer_id) s,customer_manager,r.deptid from jhbj_crm_customer c inner join relationshipusers r on c.customer_manager = r.userid where customer_state <3 and isfromcompany = 1 group by customer_manager,r.deptid) b on a.customer_manager=b.customer_manager group by a.deptid");
}
```

参数`DeptID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CrmWorkFlat/LinkCharts.aspx/?DeptID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA LinkCharts.aspx SQL注入漏洞](images/img-001-19474f6cda41.webp)](https://image.mrxn.net/7470b4c96e4940d8a0454ea79827430c.webp)

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
