---
title: "金和OA MenuSort.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-MenuSort-sqli.html
asset_dir: assets/金和oa-menusort.aspx-sql注入漏洞
---

# 金和OA MenuSort.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/16 11:49
- 573浏览
- [0评论](#comment)
- 13分钟阅读

深入探索

恶意软件分析工具

漏洞扫描器

文本剥离工具

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `MenuSort.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `MenuSort.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 **MenuSort** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request["level"] != null)
    this.level = this.Request["level"].ToString();
  if (this.Request["Code"] != null)
    this.Code = this.Request["Code"].ToString();
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.IsPostBack)
    return;
  this.GetMenuSortList();
}
```

深入探索

企业安全咨询

云安全解决方案

传输层安全性协议

当 `level` 和 `Code` 参数存在且**不等于 null** 时，进入 `GetMenuSortList`

```
private void GetMenuSortList()
{
  this.dsDeptSort = this.dalSql.ExecSQLReDataSet($"select * from  NavigationBar where LEN(nodecode)={(int.Parse(this.level) * 4).ToString()} and NodeCode like '{this.Code}%'" + " order by sort ,nodecode ");
```

至此，就非常明了了，参数 `Code` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddMenu/MenuSort.aspx/?Code=SQLI_POC&level=1 HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA MenuSort.aspx SQL注入漏洞](images/img-001-1042fe2dc723.webp)](https://image.mrxn.net/cef08e1eba4042a0b3ad697574caf06c.webp)

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

编程
