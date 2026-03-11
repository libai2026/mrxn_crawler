---
title: "金和OA AppraiseScoreUpdate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AppraiseScoreUpdate-sqli.html
asset_dir: assets/金和oa-appraisescoreupdate.aspx-sql注入漏洞
---

# 金和OA AppraiseScoreUpdate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/22 13:24
- 544浏览
- [0评论](#comment)
- 16分钟阅读

深入探索

安全

在线安全工具

SQL注入防护

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AppraiseScoreUpdate.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

漏洞扫描器

漏洞修复方案

服务器安全服务

根据 `AppraiseScoreUpdate.aspx` 的源码，在 `bin` 目录下查找 `JHBase.Web.Appraise.dll` 将其进行反编译后找到 **AppraiseScoreUpdate** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  this.InitText();
  if (this.Request["id"] != null && string.op_Inequality(this.Request["id"].ToString().Trim(), ""))
    this.strAppraiseID = this.Request["id"].ToString().Trim();
  if (!this.IsPostBack)
  {
    if (this.Request["id"] != null && string.op_Inequality(this.Request["id"].ToString().Trim(), ""))
    {
      this.strAppraiseID = this.Request["id"].ToString().Trim();
      this.m_ds = this.m_Appraise.GetAppraiseInfo(this.strAppraiseID);
```

深入探索

文件大小转换

编码转换工具

企业安全咨询

参数 `id` 被带入`GetAppraiseInfo`方法

```
public DataSet GetAppraiseInfo(string AppraiseID)
{
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  if (string.op_Equality(AppraiseID.ToString().Trim(), ""))
    return (DataSet) null;
  string str = $"select AppraiseID,convert(numeric(18,2),round(appraisescore,2)) as appraisescore ,AppraiseRemark,appraiseDateTime1,appraiseDateTime2,regcode from Appraise Where AppraiseID='{AppraiseID}'";
  DataSet dataSet = new DataSet();
```

至此，就非常明了了，`id` 参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Appraise/AppraiseScoreUpdate.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA AppraiseScoreUpdate.aspx SQL注入漏洞](images/img-001-f28ada6d27c9.webp)](https://image.mrxn.net/f48051f3d7934241807ebfcebed72613.webp)

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
