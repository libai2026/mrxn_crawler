---
title: "金和OA GetTreeDate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-GetTreeDate-sqli.html
asset_dir: assets/金和oa-gettreedate.aspx-sql注入漏洞
---

# 金和OA GetTreeDate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/25 13:34
- 478浏览
- [0评论](#comment)
- 17分钟阅读

深入探索

数据库

软件

服务器

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `GetTreeDate.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `GetTreeDate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Appraise.dll` 将其进行反编译后找到 **GetTreeDate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
  this.InitText();
  if (this.Session["UserCode"] != null)
    this.strUser = this.Session["UserCode"].ToString();
  if (this.Request["id"] != null)
    this.loadDeptChild(this.Request["id"].ToString());
```

参数 `id` 被带入`loadDeptChild`方法

深入探索

SQL

传输层安全性协议

服务器安全服务

```
public void loadDeptChild(string deptID)
{
  DataTable firstSubDeptByDeptId = new Role().GetFirstSubDeptByDeptID(deptID);
```

跟进`GetFirstSubDeptByDeptID`

```
public DataTable GetFirstSubDeptByDeptID(string deptID)
{
  DataTable firstSubDeptByDeptId = (DataTable) null;
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append("select  a.DeptID, a.DeptName,case when exists(select * from dbo.department where deptparentid=a.deptid and deptdelflag=0) then 1 else 0 end as haschild ");
  stringBuilder.Append("   from dbo.Department  a left outer join dbo.Sort b on a.DeptID =b.SortObjectID  ");
  stringBuilder.Append($" where  a.deptparentid={deptID} and b.SortType = 'Dept' and a.DeptDelFlag = 0");
  stringBuilder.Append(" order by sortid ");
```

至此，就非常明了了，`id` 参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Appraise/GetTreeDate.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA GetTreeDate.aspx SQL注入漏洞](images/img-001-21ae55bb63b4.webp)](https://image.mrxn.net/dfa571224d0b42bda8d69f8c8a935475.webp)

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
