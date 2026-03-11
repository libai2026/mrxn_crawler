---
title: "金和OA SubjectHandler.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-SubjectHandler-sqli.html
asset_dir: assets/金和oa-subjecthandler.ashx-sql注入漏洞
---

# 金和OA SubjectHandler.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/31 13:20
- 261浏览
- [0评论](#comment)
- 20分钟阅读

深入探索

数据库

软件

服务器

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `SubjectHandler.ashx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `SubjectHandler.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **SubjectHandler** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  string str = string.Empty;
  if (!string.IsNullOrEmpty(this.Action))
  {
    string action;
    str = (action = this.Action) == null || !string.op_Equality(action, "updateactive") ? "{\"result\":false}" : str + this.UpdateActive();
  }
  context.Response.ContentType = "application/json";
  context.Response.Write(str);
  context.Response.Expires = 0;
  context.Response.Buffer = true;
  context.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  context.Response.AddHeader("pragma", "no-cache");
  context.Response.CacheControl = "no-cache";
}

private string UpdateActive()
{
  string empty = string.Empty;
  return this.Budget_Subject.UpdateActive(this.SubjectCode, this.IsActive) <= 0 ? "{\"result\":false}" : "{\"result\":true}";
}
```

深入探索

安全工具开发

漏洞扫描服务

Web安全书籍

当 `Action=updateactive` 时，**SubjectCode**、**IsActive** 被带入`UpdateActive`方法

```
public int UpdateActive(string subjectCode, int IsActive)
{
  StringBuilder stringBuilder = new StringBuilder();
  if (IsActive == 0)
  {
    stringBuilder.Append("update Budget_Subject set IsActive=" + (object) IsActive);
    stringBuilder.Append($" where SubjectCode='{subjectCode}' or ParentID='{subjectCode}'");
    return this.dblib.ExecSQLReInt(stringBuilder.ToString());
  }
  stringBuilder.Append("update Budget_Subject set IsActive=" + (object) IsActive);
  stringBuilder.Append($" where SubjectCode='{subjectCode}'");
  return this.dblib.ExecSQLReInt(stringBuilder.ToString());
}
```

深入探索

云安全解决方案

安全研究工具

Nessus

参数`subjectCode`被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/subClass/Handlers/SubjectHandler.ashx?SubjectCode=SQLI_POC&Action=updateactive HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA SubjectHandler.ashx SQL注入漏洞](images/img-001-7e3958c1224b.webp)](https://image.mrxn.net/0de29e53786641d89a36600ef279e94d.webp)

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
