---
title: "金和OA CertificateModify.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-CertificateModify-sqli.html
asset_dir: assets/金和oa-certificatemodify.aspx-sql注入漏洞
---

# 金和OA CertificateModify.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/12/3 13:30
- 377浏览
- [0评论](#comment)
- 17分钟阅读

深入探索

木马

SQL

软件

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `CertificateModify.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

在线安全工具

技术文章订阅

Nessus

根据 `CertificateModify.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Certificate.dll` 将其进行反编译后找到 **CertificateModify** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request.QueryString["ID"] != null)
  {
    this.strCertID = this.Request.QueryString["ID"].ToString();
    if (string.op_Equality(this.strCertID, ""))
      ((Control) this.btnApply).Visible = true;
    else
      ((Control) this.btnApply).Visible = false;
  }
  this.InitTxt();
  if (!((Control) this).Page.IsPostBack && string.op_Inequality(this.strCertID, ""))
  {
    JHSoft.Certificate.Entity.Certificate certificateByCaid = this.certificate.GetCertificateByCAID(this.strCertID);
```

深入探索

Web安全书籍

物流软件安全

网络安全培训

跟进`GetCertificateByCAID`方法

```
public JHSoft.Certificate.Entity.Certificate GetCertificateByCAID(string certID)
{
  JHSoft.Certificate.Entity.Certificate certificateByCaid = new JHSoft.Certificate.Entity.Certificate();
  string str = $"SELECT CAID,UserID,UserName,CASerialNumber,convert(varchar(10),CAValidFrom,120) as CAValidFrom, convert(varchar(10),CAValidTo,120) AS CAValidTo,CAIsUsed,UKeyNumber,UKeyName  FROM UsersCA WHERE CAID='{certID}'";
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  DataTable dataTable = dbOperator.ExecSQLReDataTable(str);
```

至此，就非常明了了，参数**ID**是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Certificate/CertificateModify.aspx/?ID=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA CertificateModify.aspx SQL注入漏洞](images/img-001-d4d19a3c344d.webp)](https://image.mrxn.net/0f14a531ccc146d4b1fe83d2928ce69c.webp)

成功延时 4 秒

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
