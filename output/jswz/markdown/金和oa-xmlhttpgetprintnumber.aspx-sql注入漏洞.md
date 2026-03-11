---
title: "金和OA XmlHttpGetPrintNumber.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-XmlHttpGetPrintNumber-sqli.html
asset_dir: assets/金和oa-xmlhttpgetprintnumber.aspx-sql注入漏洞
---

# 金和OA XmlHttpGetPrintNumber.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/22 13:35
- 297浏览
- [0评论](#comment)
- 22分钟阅读

深入探索

文件大小转换

安全运维咨询

漏洞修复方案

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `XmlHttpGetPrintNumber.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

编码转换工具

防火墙软件

物流软件安全

根据 `XmlHttpGetPrintNumber.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **XmlHttpGetPrintNumber** 的处理逻辑

代码安全审计

```
protected void Page_Load(object sender, EventArgs e)
{
  if (((Control) this).Page.IsPostBack)
    return;
  string strModelCode = this.Request["tid"];
  string strFileId = this.Request["gfid"];
  if (string.IsNullOrEmpty(strModelCode) || string.IsNullOrEmpty(strFileId))
  {
    this.Response.Write("");
    this.Response.End();
  }
  else
  {
    this.Response.Write($"{GovType.getFilePrintNum(strModelCode, strFileId)}|{GovType.getFileSourcePrintNum(strModelCode, strFileId)}");
    this.Response.End();
  }
}
```

参数`strModelCode`、`strFileId`被带入`getFilePrintNum`或`getFileSourcePrintNum`方法

```
public static string getFilePrintNum(string strModelCode, string strFileId)
{
  string QueryString = "";
  if (string.op_Equality(strModelCode, "IOA_Send"))
    QueryString = $"{QueryString} select (convert(int,SendFs)) - (convert(int,SendFsResult)) as strPrintNum from SendDoc where SendID = '{strFileId}' ";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
  return ((InternalDataCollectionBase) dataTable.Rows).Count <= 0 ? "0" : dataTable.Rows[0]["strPrintNum"].ToString();
}
```

```
public static string getFileSourcePrintNum(string strModelCode, string strFileId)
{
  string QueryString = "";
  if (string.op_Equality(strModelCode, "IOA_Send"))
    QueryString = $"{QueryString} select SendFs as strPrintNum from SendDoc where SendID = '{strFileId}' ";
  DataTable dataTable = DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(QueryString);
  return ((InternalDataCollectionBase) dataTable.Rows).Count <= 0 ? "0" : dataTable.Rows[0]["strPrintNum"].ToString();
}
```

至此，就非常明了了，当**`tid`**`=`**`IOA_Send`** 时**，gfid**参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/XmlHttpGetPrintNumber.aspx/?tid=IOA_Send&gfid=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA XmlHttpGetPrintNumber.aspx SQL注入漏洞](images/img-001-546d1a27e457.webp)](https://image.mrxn.net/f07b8d356312409b87430e183f332aaf.webp)

成功延时 8 秒

漏洞预警服务

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
