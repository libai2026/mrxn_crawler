---
title: "金和OA ArchivesShowAcceptAip.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-ArchivesShowAcceptAip-sqli.html
asset_dir: assets/金和oa-archivesshowacceptaip.aspx-sql注入漏洞
---

# 金和OA ArchivesShowAcceptAip.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/11/15 13:30
- 1851浏览
- [0评论](#comment)
- 21分钟阅读

深入探索

Windows安全工具

授权

Web安全书籍

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `ArchivesShowAcceptAip.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

VPN服务

安全

在线安全工具

根据 `ArchivesShowAcceptAip.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.Archives.dll` 将其进行反编译后找到 **ArchivesShowAcceptAip** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.htc = ((CultureInfo) this.Session["culture"]).Name + ".css";
  if (this.Request["id"] == null)
    return;
  this.strArchID = this.Request["id"].ToString();
  this.GetInstanceId();
  string UserID = "";
  if (this.Session["UserCode"] != null)
    UserID = this.Session["UserCode"].ToString();
  this.strDeptList = new Role(UserID, "IOA_Distribute").GetRoleDepts();
  this.ReadLocal();
  this.GetList();
```

参数`id`被带入`GetInstanceId`方法

```
private void GetInstanceId()
{
  if (string.IsNullOrEmpty(this.strArchID))
    return;
  this.strInstanceId = JHSoft.Archives.ArchivesDoc.GetAcceptInstanceId(this.strArchID);
```

跟进`GetAcceptInstanceId`方法

```
public static string GetAcceptInstanceId(string strArchivesId)
{
  string acceptInstanceId = "";
  DBOperator dbOperator = DBOperatorFactory.GetDBOperator();
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append(" select  DISTINCT(JHOA_Approve.Instance_ID) from ");
  stringBuilder.Append(" AcceptDoc INNER JOIN JHOA_Approve ");
  stringBuilder.Append(" on AcceptDoc.AcceptId = JHOA_Approve.AppO_ID ");
  stringBuilder.Append(" where AcceptDoc.ArchivesID =  " + strArchivesId);
  stringBuilder.Append(" and JHOA_Approve.AppT_ID = 'IOA_Accept' ");
  DataTable dataTable = dbOperator.ExecSQLReDataTable(stringBuilder.ToString());
  if (dataTable != null && ((InternalDataCollectionBase) dataTable.Rows).Count > 0)
    acceptInstanceId = dataTable.Rows[0][0].ToString();
  return acceptInstanceId;
}
```

至此，就非常明了了，参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.Archives/ArchivesShowAcceptAip.aspx/?id=SQLI_POC HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA ArchivesShowAcceptAip.aspx SQL注入漏洞](images/img-001-730ee8e688b4.webp)](https://image.mrxn.net/9bc03078ee6a42fba27450c39e6638c2.webp)

成功延时 2 秒

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
