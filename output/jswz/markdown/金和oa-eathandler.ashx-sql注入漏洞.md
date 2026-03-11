---
title: "金和OA EatHandler.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-EatHandler-sqli.html
asset_dir: assets/金和oa-eathandler.ashx-sql注入漏洞
---

# 金和OA EatHandler.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/3 13:31
- 291浏览
- [0评论](#comment)
- 14分钟阅读

深入探索

数据库

木马

服务器

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `EatHandler.ashx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `EatHandler.ashx` 的源码，在 `bin` 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **EatHandler** 的处理逻辑

```
public void ProcessRequest(HttpContext context)
{
  string empty = string.Empty;
  string state = this.State;
  string str = state == null || !string.op_Equality(state, "code") ? this.GetCodeList() : this.GetCodeList();
  context.Response.ContentType = "application/json";
  context.Response.Buffer = true;
  context.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  context.Response.Expires = 0;
  context.Response.CacheControl = "no-cache";
  context.Response.Write(str);
  context.Response.End();
}

private string GetCodeList()
{
  StringBuilder stringBuilder = new StringBuilder();
  DataTable codeList = this._costManager.GetCodeList(this.SubjectNo);
```

深入探索

授权

网络安全培训

计算机安全

跟进`GetCodeList`方法

```
public DataTable GetCodeList(string subjectNo)
{
  string name = new Config().GetName();
  return this.db.ExecSQLReDataTable($"select * from Budget_Subject where SubjectNo like '{subjectNo}%'  and FromFlag='{name}'and [DelFlag] ='0' ");
}
```

参数`subjectNo`被直接拼接到SQL语句中执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostU8/EAI/EatHandler.ashx?SubjectNo=SQLI_POC&State=code HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA EatHandler.ashx SQL注入漏洞](images/img-001-739ce8c7fd86.webp)](https://image.mrxn.net/77a431398ff4473493fc722a2be6c292.webp)

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
