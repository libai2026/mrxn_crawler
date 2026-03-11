---
title: "金和OA OuterAppTIDSave.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-OuterAppTIDSave-sqli.html
asset_dir: assets/金和oa-outerapptidsave.aspx-sql注入漏洞
---

# 金和OA OuterAppTIDSave.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/19 08:31
- 490浏览
- [0评论](#comment)
- 18分钟阅读

深入探索

漏洞预警服务

传输层安全性协议

文件大小转换

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `OuterAppTIDSave.aspx` 接口处存在SQL注入漏洞，攻击者除了可以利用[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `OuterAppTIDSave.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 **OuterAppTIDSave** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.strOuterAppTID = this.Request.QueryString["OuterAppTID"].ToString();
  this.strSystemID = this.Request.QueryString["SystemID"].ToString();
  this.strOwnerAppTID = this.Request.QueryString["AppTID"].ToString();
  int num = new OuterOpenGroup().OuterAppTIDSave(this.strSystemID, this.strOuterAppTID, this.strOwnerAppTID);
  if (num > 0)
    this.Response.Write("true");
  else if (num == int.MinValue)
    this.Response.Write("error");
  else
    this.Response.Write("false");
}
```

深入探索

服务器安全服务

漏洞扫描器

安全研究工具

参数`OuterAppTID`、`SystemID`和`AppTID`被带入`OuterAppTIDSave`方法

```
public int OuterAppTIDSave(string SystemID, string OuterAppTID, string OwnerAppTID)
{
  StringBuilder stringBuilder = new StringBuilder();
  stringBuilder.Append(" select count(*) from JHOA_Approve_OuterProcess");
  stringBuilder.Append($" where System_ID='{SystemID}' ");
  stringBuilder.Append($" and ModuleTemplate_ID='{OwnerAppTID}'");
  object obj = this.dbo.ExecSQLReobject(stringBuilder.ToString());
  if ((obj == null ? -1 : Convert.ToInt32(obj)) > 0)
    return int.MinValue;
  return this.dbo.ExecSQLReInt($"update JHOA_Approve_OuterProcess set ModuleTemplate_ID='{OwnerAppTID}' where System_ID='{SystemID}' and Template_ID='{OuterAppTID}'");
}
```

至此，就非常明了了，三个参数均是被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddMenu/OuterAppTIDSave.aspx/?SystemID=SQLI_POC&OuterAppTID=1&AppTID=1 HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA OuterAppTIDSave.aspx SQL注入漏洞](images/img-001-56fba3ce9443.webp)](https://image.mrxn.net/9fb0f99a3f94423d9fcd9530d598eb8c.webp)

成功延时 10 秒（执行两次）

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
