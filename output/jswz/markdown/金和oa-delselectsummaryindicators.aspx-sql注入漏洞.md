---
title: "金和OA DelSelectSummaryIndicators.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-DelSelectSummaryIndicators-sqli.html
asset_dir: assets/金和oa-delselectsummaryindicators.aspx-sql注入漏洞
---

# 金和OA DelSelectSummaryIndicators.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/9 13:31
- 217浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

Windows安全工具

JSON处理工具

软件

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GetTreeDate.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

安全研究报告

安全研究工具

防火墙软件

根据 `GetTreeDate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.dossier.dll` 将其进行反编译后找到 **DelSelectSummaryIndicators** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.FilterID = this.Request.QueryString["ID"].Trim();
  if (string.op_Inequality(this.FilterID, ""))
  {
    if (new JHSoft.Dossier().DeleteCountFilterByFilterID(this.Request.QueryString["ID"].Trim()))
    {
      this.Response.Write("OK");
      this.Response.End();
    }
    else
    {
      this.Response.Write("Error");
      this.Response.End();
    }
  }
```

深入探索

网络安全课程

漏洞扫描器

VPN服务

跟进`DeleteCountFilterByFilterID`方法

```
public bool DeleteCountFilterByFilterID(string FilterID)
{
  int num = this.dboperator.ExecSQLReInt($" Delete Filter Where FilterID in ({FilterID})");
  if (this.dboperator.IsError)
    this.strErrMessage = this.dboperator.ErrorMessage;
  return num > 0;
}
```

参数`ID`被直接拼接进SQL语句执行，从而造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.dossier/DelSelectSummaryIndicators.aspx/?ID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA DelSelectSummaryIndicators.aspx SQL注入漏洞](images/img-001-323b072113fe.webp)](https://image.mrxn.net/99857d360c7c43fbb19462e5949a5fc3.webp)

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
