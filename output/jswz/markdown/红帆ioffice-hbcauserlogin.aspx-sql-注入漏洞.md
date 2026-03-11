---
title: "红帆ioffice HbcaUserLogin.aspx SQL 注入漏洞"
source: https://mrxn.net/jswz/ioffice-Identity-HbcaUserLogin-sqli.html
asset_dir: assets/红帆ioffice-hbcauserlogin.aspx-sql-注入漏洞
---

# 红帆ioffice HbcaUserLogin.aspx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/2 08:24
- 883浏览
- [2评论](#comment)
- 1小时阅读

深入探索

数据库

鉴权

软件

---

# 漏洞简介

红帆iOffice的/ioffice/Identity/HbcaUserLogin.aspx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，未经身份验证地获取数据库敏感信息，影响范围包括红帆iOffice系统的数据访问权限。

脚本语言

# 影响版本

# fofa语法

> (title="iOffice.net" || body="/iOffice/js" || (body="iOffice.net" && header!="couchdb" && header!="drupal") || body="iOfficeOcxSetup.exe" || body="Hongfan. All Rights Reserved")

# 漏洞分析

先看下`HbcaUserLogin.aspx` 里引用的代码在哪里（Inherits）

```
<%@ Page Language="vb" AutoEventWireup="false" Inherits="iden.HbcaUserLogin" CodeBehind="HbcaUserLogin.aspx.vb"  %>
```

去bin目录找到`iden.dll`后编译打开，看`HbcaUserLogin`它的实现逻辑

SQL注入防护

```
public class HbcaUserLogin : WebPageBase
{
  [AccessedThroughProperty("Head1")]
  private HtmlHead _Head1;
  [AccessedThroughProperty("form1")]
  private HtmlForm _form1;
  [AccessedThroughProperty("ioScriptManager1")]
  private ioScriptManager _ioScriptManager1;
  [AccessedThroughProperty("updatePanel1")]
  private ioUpdatePanel _updatePanel1;
  [AccessedThroughProperty("btVerify")]
  private Button _btVerify;
  [AccessedThroughProperty("txthidIsLogin")]
  private TextBox _txthidIsLogin;
  [AccessedThroughProperty("btSetVisitBefore")]
  private Button _btSetVisitBefore;
  [AccessedThroughProperty("lblSerialNum")]
  private TextBox _lblSerialNum;
  [AccessedThroughProperty("ReConnect")]
......
private void Page_Load(object sender, EventArgs e)
{
  this.Response.Expires = -1;
  this.Response.Buffer = true;
  this.Response.ExpiresAbsolute = DateTime.Now.AddSeconds(-1.0);
  this.Response.Expires = 0;
  this.Response.CacheControl = "no-cache";
}

protected void btVerify_Click(object sender, EventArgs e)
{
  if (Operators.CompareString(this.lblSerialNum.Text.Trim(), "", false) == 0)
    return;
  iden.iden.HBCA hbca = new iden.iden.HBCA();
  hbca.EmpID = checked ((int) Math.Round(Conversion.Val(this.Emp.EmpID)));
  hbca.SubjectName = "HBCA";
  hbca.Serial = this.lblSerialNum.Text;
  switch (hbca.Verify())
  {
    case 0:
      Page pgeParent1 = (Page) this;
      pf.ShowMessage(ref pgeParent1, "这个证书没有分配给当前用户，认证无效！");
      Page pgeParent2 = (Page) this;
      pf.RunScript(ref pgeParent2, "retry()");
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

深入探索

安全运维咨询

传输层安全性协议

JSON处理工具

最开始的一些变量定义，前端按钮btVerify

代码安全审计

```
    <form id="form1" runat="server">
 <uc1:ioScriptManager ID="ioScriptManager1" runat="server" />
                    <ioctl:ioUpdatePanel ID="updatePanel1" UpdateMode="Conditional" runat="server">
                    <ContentTemplate>
        <asp:Button ID="btVerify" runat="server" Style="display: none" />
                <asp:TextBox ID="txthidIsLogin" runat ="server" style="display:none"></asp:TextBox>
        <asp:Button ID="btSetVisitBefore" runat="server" Style="display: none" />
        <table id="Table1" cellspacing="0" cellpadding="0" width="100%" align="center" border="0">
            <tr>
                <td height="100px">
                </td>
            </tr>
            <tr>
                <td class="td" valign="top" align="center">
                    <table id="Table5" cellspacing="0" cellpadding="0" border="0" style="width: 480px;
                        height: 220px">

                        <tr>
                            <td align="right"style="font-size:12px;">
                            请选择用户证书：</td>
                            <td>
                             <select name="CertID" style="width:150px">
                               <option value="">未取到用户证书</option>
        </select>
                        </tr>
                                <tr>
                            <td align="right"  style="font-size:12px;">
                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户PIN码：
                            </td>
                            <td>
                                <input type="password" size="10" name="UserPIN"  style="width:150px" onkeypress="if(event.keyCode==13) {doLogin();return false;}" />
                        </tr>

                        <tr>
                            <td align="center" colspan="2">

<%--                                <img src="/ioffice/img/logo1.gif" border="0"/>--%></td>
<asp:TextBox ID="lblSerialNum"  runat="server" Width="0px"></asp:TextBox>
                        </tr>
                        <tr>
                            <td valign="top" align="right" >
                                <img src="../img/ikeylogo.gif" border="0" /></td>
                            <td valign="middle" align="left"  >
                                <img alt="" src="/ioffice/img/ProgressSmall.gif" /></td>
                        </tr>
                        <tr>
                            <td valign="top" align="center" colspan="2">
                                <a id="ReConnect" runat ="server"  onclick="doLogin();" href="#">[登录]</a>
                                    &nbsp; &nbsp;<a onclick="closewin()" href="#">[关闭窗口]</a></font>&nbsp; &nbsp;<a onclick="relogin()" href="#">[手动输入登录]</a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
```

对应的后端的

漏洞预警服务

```
protected void btVerify_Click(object sender, EventArgs e)
{
  if (Operators.CompareString(this.lblSerialNum.Text.Trim(), "", false) == 0)
    return;
  iden.iden.HBCA hbca = new iden.iden.HBCA();
  hbca.EmpID = checked ((int) Math.Round(Conversion.Val(this.Emp.EmpID)));
  hbca.SubjectName = "HBCA";
  hbca.Serial = this.lblSerialNum.Text;
  switch (hbca.Verify())
  {
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

在判断`lblSerialNum`不为空后带入`iden.iden.HBCA()` 方法，跟进看下

编程

```
public override int Verify()
{
  if (Operators.CompareString(this.SubjectName, "", false) != 0)
    this.LookupEmpAndLogin(this.Serial);
  return Operators.ConditionalCompareObjectGreater(SqlData.ExecuteScalar(Globals.ConnectString, (CommandType) 1, $"{"select count(*) " + " from ssIdentity " + " where "}  Serial='{this.Serial}'"), (object) 0, false) ? 1 : 0;
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

ok,到这里，漏洞成因就非常明了了，从前端TextBox获取的**lblSerialNum**最终经过一系列赋值传递后被直接拼接进`$"select empid from ssIdentity where Serial='{SearchKey}'"` sql语句里，全程无过滤或者校验，从而造成了[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

> 漏洞复现需要打开漏洞文件页面获取一些其他必要参数如\_\_VIEWSTATE之类
>
> 网络安全

```
POST /ioffice/Identity/HbcaUserLogin.aspx HTTP/1.1
Host: ioffice.mrxn.net
Content-Type: application/x-www-form-urlencoded

__EVENTTARGET=btVerify&__EVENTARGUMENT=&__VIEWSTATE=xxxxxx&__VIEWSTATEGENERATOR=xxxxx&btVerify=&lblSerialNum=SQLI_POC
```

[![红帆ioffice HbcaUserLogin.aspx SQL 注入漏洞](images/img-001-8e9ecf6dd453.webp)](https://image.mrxn.net/05f905f18a2148bc91abfaeaaa82063b.webp)

成功利用报错注入在响应回显当前数据库用户信息

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
