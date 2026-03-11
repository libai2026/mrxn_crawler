---
title: "金和OA Budget_CostApply.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-Budget_CostApply-sqli.html
asset_dir: assets/金和oa-budget_costapply.aspx-sql注入漏洞
---

# 金和OA Budget\_CostApply.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/11 13:30
- 305浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

漏洞扫描器

网络安全培训

防火墙软件

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `Budget_CostApply.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `Budget_CostApply.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.CostControl.dll` 将其进行反编译后找到 **Budget\_CostApply** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  Utility.RegisterTypeForAjax(typeof (Budget_CostApply));
  this.KeyCtrl("JHCostControl");
  ((HtmlInputControl) this.hidShowKyMoney).Value = this.cc.GetCkKyMoney();
  this.ToolBar1.IdeaUrl = "../../Control/";
  if (this.Request.QueryString["From"] != null && string.op_Equality(this.Request.QueryString["From"].ToString(), "GiveOutShow"))
  {
    this.ToolBar1.Style["display"] = "none";
    this.UploadFile1.ButtonAdd.Disabled = true;
    this.UploadFile1.ButtonDel.Disabled = true;
    this.UploadFile1.ButtonEditor.Disabled = true;
  }
  if (this.Request.QueryString["Projid"] != null)
  {
    string str = this.Request.QueryString["Projid"].ToString();
    this.ProName = this.costManager.GetProjName(str);
    DataRow row = this.costManager.GetProjPeriod(str).Rows[0];
```

深入探索

恶意软件分析工具

文本剥离工具

在线安全工具

跟进`GetProjName`方法

```
public string GetProjName(string pid)
{
  return this.db.ExecSQLReobject($"select projname from ProjectList  where ProjID='{pid}'").ToString();
}
```

至此，就非常明了了，参数**Projid**是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/JHSoft.Web.CostControl/BudgetExecution/Budget_CostApply.aspx/?Projid=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA Budget_CostApply.aspx SQL注入漏洞](images/img-001-7c81b39a37ce.webp)](https://image.mrxn.net/3ebed55abb984390ac1e58516b8100b8.webp)

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
