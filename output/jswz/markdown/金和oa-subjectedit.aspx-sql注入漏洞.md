---
title: "金和OA SubjectEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/Jhsoft-Web-accept-SubjectEdit-sqli.html
asset_dir: assets/金和oa-subjectedit.aspx-sql注入漏洞
---

# 金和OA SubjectEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/30 16:26
- 696浏览
- [0评论](#comment)
- 12分钟阅读

深入探索

安全研究工具

网络安全培训

编程语言教程

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SubjectEdit.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 SubjectEdit.aspx 的源码，在 bin 目录下查找 JHBase.Web.accept.dll 将其进行反编译后找到 **SubjectEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  this.InitText();
  this.but_Save.Text = this.QD;
  this.id = this.Request.QueryString["id"].ToString();
  if (((Control) this).Page.IsPostBack)
    return;
  this.txt_id.Text = subject.GetSubject(this.id).Rows[0]["name"].ToString();
}
```

当不为POST请求时，参数 `id` 带入 `GetSubject` 方法中

跟进 `GetSubject` 方法

```
public static DataTable GetSubject(string id)
{
  string QueryString = $"select *  from subject where id=({id}) ";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
}
```

参数 `id` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.accept/SubjectEdit.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA SubjectEdit.aspx SQL注入漏洞](images/img-001-6b83ca4cc23b.webp)](https://image.mrxn.net/794a032295bf472abcf5ac0563b677bd.webp)

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
