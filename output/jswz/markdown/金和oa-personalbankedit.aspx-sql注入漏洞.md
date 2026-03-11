---
title: "金和OA PersonalBankEdit.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-PersonalBankEdit-sqli.html
asset_dir: assets/金和oa-personalbankedit.aspx-sql注入漏洞
---

# 金和OA PersonalBankEdit.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/9 13:30
- 438浏览
- [0评论](#comment)
- 11分钟阅读

深入探索

编码转换工具

JSON处理工具

服务器安全服务

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `PersonalBankEdit.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

编程语言教程

安全认证考试

Nessus

根据 `PersonalBankEdit.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **PersonalBankEdit** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.IsPostBack)
    return;
  CostManager costManager = new CostManager();
  DataTable dataTable = new DataTable();
  if (this.Request["ID"] == null)
    return;
  ((HtmlInputControl) this.HiddID).Value = this.Request["ID"].ToString();
  DataTable info = costManager.Budget_Bank_GetInfo(this.Request["ID"].ToString());
```

跟进`Budget_Bank_GetInfo`方法

```
public DataTable Budget_Bank_GetInfo(string ID)
{
  return this.db.ExecSQLReDataTable($"select * from Budget_Bank where  BankID='{ID}'");
}
```

至此，就非常明了了，参数**ID**是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.CostControl/PersonalBankEdit.aspx/?ID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

深入探索

Web安全课程

网络安全培训

VPN服务

[![金和OA PersonalBankEdit.aspx SQL注入漏洞](images/img-001-b2a97f38d8ab.webp)](https://image.mrxn.net/19365347427646869fb6984a41b6e50d.webp)

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
