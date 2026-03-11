---
title: "金和OA OpenGroupOpen.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-OpenGroupOpen-sqli.html
asset_dir: assets/金和oa-opengroupopen.aspx-sql注入漏洞
---

# 金和OA OpenGroupOpen.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/10/18 08:23
- 478浏览
- [0评论](#comment)
- 21分钟阅读

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `OpenGroupOpen.aspx` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，攻击者除了可以利用SQL注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

根据 `OpenGroupOpen.aspx` 的源码，在 bin 目录下查找 `JHBase.Web.AddMenu.dll` 将其进行反编译后找到 **OpenGroupOpen** 的处理逻辑

```
protected void Page_Load(object sender, EventArgs e)
{
  this.InitTxt();
  if (this.IsPostBack)
    return;
  if (this.Request.Params["GroupID"] != null)
    ((HtmlInputControl) this.hidGroupID).Value = this.Request.Params["GroupID"];
  string str;
  if (this.Request.Params["op"] == null || (str = this.Request.Params["op"]) == null)
    return;
  if (!string.op_Equality(str, "set"))
  {
    if (!string.op_Equality(str, "view"))
      return;
    this.InitGridView();
    ((Control) this.btnOK).Visible = false;
    this.strTitle = "公开组公开范围状态查看";
  }
  else
  {
    ((Control) this.btnOK).Visible = true;
    this.strTitle = "公开组公开范围设置";
    this.InitGridSet();
  }
}
```

当 `GroupID` 参数存在不等于 null 且 `op=view` 时，进入 `InitGridView` 方法

```
private void InitGridView()
{
  string str1 = "<root>{0}</root>";
  string str2 = "";
  int num = 0;
  string str3 = $"<record><SystemName ColumnName='{this.strSystemName}' Width='1.0'><![CDATA[{{0}}]]></SystemName><Flag ColumnName='成功标识'>{{1}}</Flag></record>";
  DataTable systemTableByGroupId = new OpenGroup().GetGroupOpenSystemTableByGroupID(((HtmlInputControl) this.hidGroupID).Value);
```

跟进 `GetGroupOpenSystemTableByGroupID` 方法

```
public DataTable GetGroupOpenSystemTableByGroupID(string GroupID)
{
  GroupID = GroupID.Replace(",", "','");
  string str = $"select a.*, b.System_ID, b.System_Name from outerreceipt a inner join OuterSystem b on a.ToSystemID = b.System_ID where moduletype='opengroups'  and deleteFlag=0 and a.recordid in ('{GroupID}')";
  return DBOperatorFactory.GetDBOperator().ExecSQLReDataTable(str);
}
```

至此，就非常明了了，参数 `GroupID` 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /c6/Jhsoft.Web.AddMenu/OpenGroupOpen.aspx/?GroupID=SQLI_POC&op=view HTTP/1.1
Host: jhsoft.mrxn.net
```

[![金和OA OpenGroupOpen.aspx SQL注入漏洞](images/img-001-28a25fe56091.webp)](https://image.mrxn.net/663ab0e7f6524d36a4db4a2fe4203bf4.webp)

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
