---
title: "东胜物流软件 CompanysAccountGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-Shipping-CompanysAccountGridSource-sqli.html
asset_dir: assets/东胜物流软件-companysaccountgridsource.aspx-sql注入漏洞
---

# 东胜物流软件 CompanysAccountGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2026/1/29 15:31
- 244浏览
- [0评论](#comment)
- 36分钟阅读

深入探索

身份验证

软件

SQL

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 Shipping/CompanysAccountGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

# fofa语法

> (body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css") && body="东胜"

# 漏洞分析

根据 Shipping/CompanysAccountGridSource.aspx 的代码引用`<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="CompanysAccountGridSource.aspx.cs" Inherits="DSWeb.Shipping.CompanysAccountGridSource" %>`，在dll中找到`DSWeb.Shipping.CompanysAccountGridSource`的逻辑实现

```
protected void Page_Load(object sender, EventArgs e)
{
  if (this.Request.QueryString["read"] != null)
    this.strReadXmlType = this.Request.QueryString["read"].ToString().Trim();
  if (this.Request.QueryString["showcount"] != null)
    this.iShowCount = int.Parse(this.Request.QueryString["showcount"].ToString());
  if (this.Request.QueryString["LINKID"] != null)
    this.strLINKID = this.Request.QueryString["LINKID"].ToString();
  if (!this.strReadXmlType.Equals(""))
  {
    if (this.strReadXmlType.Equals("delete") || this.strReadXmlType.Equals("recover"))
    {
      this.strAccountGid = this.Request.QueryString["gid"];
      this.strHandle = this.Request.QueryString["read"];
      if (this.strAccountGid == null || this.strHandle == null)
        this.Response.Write((object) -99);
      else
        this.Response.Write(this.DoExcute(this.strAccountGid, this.strHandle));
    }
    else
    {
      string cells = this.GetCells(this.iShowCount, this.strReadXmlType);
      this.Response.ContentType = "text/xml";
      cells.Replace("&", "&amp;");
      this.Response.Write(cells);
    }
  }
  else
  {
    this.Response.ContentType = "text/xml";
    this.Response.Write("-2");
  }
}
```

1. 用户输入从 `Request.QueryString["LINKID"]` 获取（第 21 行）
2. 直接赋值给成员变量 `strLINKID`，未经任何过滤
3. 在构建 SQL 语句时使用字符串插值 `$"..."` 直接拼接到 WHERE 子句
4. `LINKID` 字段为**字符串类型**（SQL 中使用单引号包围：`'{this.strLINKID}'`）

当参数read满足以下条件

1. `read` 参数不能为空字符串
2. `read` 参数不能是 "delete" 或 "recover"

进入`GetCells`方法

深入探索

防火墙软件

网络安全课程

Nessus

```
private string GetCells(int iShowCount, string readXmlType)
{
  AccountEntity accountEntity1 = new AccountEntity();
  AccountDA accountDa = new AccountDA();
  AccountEntity accountEntity2 = new AccountEntity();
  AccountEntity accountByLinkidAndType = accountDa.GetAccountByLINKIDAndType(this.strLINKID);
  if (accountByLinkidAndType != null && !this.strReadXmlType.Equals("exist"))
  {
    DataTable dataTable = new DataTable();
    string strSql = $" SELECT GID,LINKID,CODENAME,CURRENCY,BANKNAME,ACCOUNT,SubjectCode,FINANCESOFTCODE,REMARK,CREATEUSER,CREATETIME,MODIFIEDUSER,MODIFIEDTIME  FROM sys_bank WHERE LINKID = '{this.strLINKID}' ORDER BY CODENAME ASC";
    DataTable statusNameTable = this.getStatusNameTable(accountDa.GetExcuteSql(strSql).Tables[0]);
```

跟进GetSysDeptByLINKIDAndType方法

```
public SysDeptEntity GetSysDeptByLINKIDAndType(string strLINKID)
{
  SysDeptEntity deptByLinkidAndType = (SysDeptEntity) null;
  string cmdText = $" SELECT top 1 GID,LINKID,DEPTNO,DEPTNAME,MANAGE1,MANAGE2,REMARK,CREATEUSER,CREATETIME,MODIFIEDUSER,MODIFIEDTIME,FINANCESOFTCODE  FROM sys_dept WHERE LINKID = '{strLINKID}'";
  using (SqlDataReader sqlDataReader = SqlHelper.ExecuteReader(SqlHelper.ConnectionStringLocalTransaction, (CommandType) 1, cmdText, (SqlParameter[]) null))
```

参数`strLINKID`即外部用户可控参数**LINKID**被直接拼接在SQL语句中执行，无任何过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /Shipping/CompanysAccountGridSource.aspx?read=1&LINKID=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 CompanysAccountGridSource.aspx SQL注入漏洞](images/img-001-dc07b87b81a9.webp)](https://image.mrxn.net/da67d1e03ac14804b15608867d8426b1.webp)

成功延时 5 秒

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
