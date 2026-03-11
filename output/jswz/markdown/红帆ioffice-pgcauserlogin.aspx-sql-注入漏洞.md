---
title: "红帆ioffice PgcaUserLogin.aspx SQL 注入漏洞"
source: https://mrxn.net/jswz/ioffice-Identity-PgcaUserLogin-sqli.html
asset_dir: assets/红帆ioffice-pgcauserlogin.aspx-sql-注入漏洞
---

# 红帆ioffice PgcaUserLogin.aspx SQL 注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/26 16:30
* 782浏览
* [0评论](#comment)
* 1小时阅读

深入探索

数据库

Active Server Pages

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

红帆iOffice的/ioffice/Identity/PgcaUserLogin.aspx接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可通过构造恶意SQL语句，未经身份验证地获取数据库敏感信息，影响范围包括红帆iOffice系统的数据访问权限。

脚本语言

# 影响版本

# fofa语法

> (title="iOffice.net" || body="/iOffice/js" || (body="iOffice.net" && header!="couchdb" && header!="drupal") || body="iOfficeOcxSetup.exe" || body="Hongfan. All Rights Reserved")

# 漏洞分析

先看下`PgcaUserLogin.aspx` 里引用的代码在哪里（Inherits）

```
<%@ Page Language="vb" AutoEventWireup="false" CodeBehind="PgcaUserLogin.aspx.vb"
    Inherits="iden.PgcaUserLogin" %>
```

去bin目录找到`iden.dll`后编译打开，看`PgcaUserLogin`它的实现逻辑

SQL注入防护

```
public class PgcaUserLogin : WebPageBase
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
  private HtmlAnchor _ReConnect;

......
```

最开始的一些变量定义，前端按钮**btVerify**

代码安全审计

```
function doLogin() {
    //document.getElementById("txthidIsLogin").value = "1";
    try {
        var CertID = document.getElementById("CertID").value;
        if (CertID == "") {
            alert("没有读取到key信息，请检查key是否运行正常！");
            return false;
        }
        else {
            document.all.lblSerialNum.value = CertID;
            var obj = document.getElementById("btVerify");
            obj.click();
            return true;
        }

......
<form id="form1" runat="server">
<uc1:ioScriptManager ID="ioScriptManager1" runat="server" />
<ioctl:ioUpdatePanel ID="updatePanel1" UpdateMode="Conditional"
    runat="server">
    <ContentTemplate>
        <asp:Button ID="btVerify" runat="server" Style="display: none" />
        <asp:TextBox ID="txthidIsLogin" runat="server" Style="display: none"></asp:TextBox>
        <asp:Button ID="btSetVisitBefore" runat="server" Style="display: none" />
        <table id="Table1" cellspacing="0" cellpadding="0"
            width="100%" align="center" border="0">
            <tr>
                <td height="100px">
                </td>
            </tr>
            <tr>
                <td class="td" valign="top" align="center">
                    <table id="Table5" cellspacing="0" cellpadding="0"
                        border="0" style="width: 480px; height: 220px">
                        <tr>
                            <td align="right" style="font-size: 12px;">
                                请选择用户证书：
                            </td>
                            <td>
                                <select name="CertID"  id="CertID" style="width: 150px">

                                </select>
                        </tr>
                        <tr style="display: none">
                            <td align="right" style="font-size: 12px;">
                                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户PIN码：
                            </td>
                            <td>
                                <input type="password" size="10" name="UserPIN" style="width: 150px"
                                    onkeypress="if(event.keyCode==13) {doLogin();return false;}" />
                        </tr>
                        <tr>
                            <td align="center" colspan="2">
                            </td>
                            <asp:TextBox ID="lblSerialNum" runat="server" Width="0px" Style="display:none"></asp:TextBox>
                        </tr>
                        <tr>
```

对应后端的**btVerify**

漏洞修复方案

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

跟进**btVerify\_Click**看下

```
protected void btVerify_Click(object sender, EventArgs e)
{
  if (Operators.CompareString(this.lblSerialNum.Text.Trim(), "", false) == 0)
    return;
  iden.iden.PGCA pgca = new iden.iden.PGCA();
  pgca.EmpID = checked ((int) Math.Round(Conversion.Val(this.Emp.EmpID)));
  pgca.SubjectName = "PGCA";
  pgca.Serial = this.lblSerialNum.Text;
  switch (pgca.Verify())
  {
```

在判断`lblSerialNum`不为空后带入`iden.iden.PGCA()` 方法，跟进看下

编程

```
public class PGCA : iden.iden.Identity
{
  public string SubjectName;
  public string Issuer;

  public PGCA()
  {
    this.p_Hardware = nameof (PGCA);
    this.ConfigPage = "/ioffice/identity/PgcaConfig.aspx";
    this.LoginPage = "/ioffice/identity/PgcaUserLogin.aspx";
  }

  public override void Addup()
  {
    this.IdentityAddUp(this.EmpID, this.Serial, this.Hardware, this.SubjectName, sIssuer: this.Issuer);
  }

  public override int Verify()
  {
    if (Operators.CompareString(this.SubjectName, "", false) != 0)
      this.LookupEmpAndLogin(this.Serial);
    return Operators.ConditionalCompareObjectGreater(SqlData.ExecuteScalar(Globals.ConnectString, (CommandType) 1, $"{"select count(*) " + " from ssIdentity " + " where "}  Serial='{this.Serial}' and empid={Conversions.ToString(this.EmpID)}"), (object) 0, false) ? 1 : 0;
  }

  protected override int LookupEmp(string SearchKey)
  {
    object objectValue = RuntimeHelpers.GetObjectValue(SqlData.ExecuteScalar(Globals.ConnectString, (CommandType) 1, $"select b.empid from ssIdentity a join mrbaseinf b on a.SubjectName=b.loginid where a.Serial='{SearchKey}'"));
    return objectValue == DBNull.Value ? 0 : Conversions.ToInteger(objectValue);
  }
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

ok,到这里，漏洞成因就非常明了了，从前端`TextBox`获取的**lblSerialNum**最终经过一系列赋值传递后被直接拼接进`$"select empid from ssIdentity where Serial='{SearchKey}'"` sql语句里，全程无过滤或者校验，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

> 漏洞复现需要打开漏洞文件页面获取一些其他必要参数如\_\_VIEWSTATE之类
>
> 网络安全

```
POST /ioffice/Identity/PgcaUserLogin.aspx HTTP/1.1
Host: ioffice.mrxn.ent
Content-Type: application/x-www-form-urlencoded

__EVENTTARGET=btVerify&__EVENTARGUMENT=&__VIEWSTATE=YOUR___VIEWSTATE&__VIEWSTATEGENERATOR=YOUR___VIEWSTATEGENERATOR&btVerify=&CertID=SQLI_POC&lblSerialNum=SQLI_POC&txthidIsLogin=1&UserPIN=123456
```

[![红帆ioffice PgcaUserLogin.aspx SQL 注入漏洞](images/img-001-5a7702b8071a.webp)](https://image.mrxn.net/47f1a72398444b73867fbfc34ea1ffaf.webp)

成功利用[报错注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)在响应回显当前数据库用户信息

漏洞修复方案

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#asp.net](https://mrxn.net/tag/asp.net)

---


// 获取当前脚本所在的父容器
const parentContainer = document.currentScript.parentElement;
let searchContainer = parentContainer.querySelector('article') || parentContainer;
if (searchContainer) {
// 优先在 class 名为 prose 或 markdown 的容器内搜索 img 图片
let images = [];
const containers = searchContainer.querySelectorAll('.prose, .markdown');
containers.forEach(function(container) {
images = images.concat(Array.from(container.querySelectorAll('img')));
});
if (images.length === 0) {
images = searchContainer.querySelectorAll('img');
}
images.forEach(function(img) {
if (img.getAttribute('data-action') === 'zoom') {
const parentLink = img.parentNode;
if (parentLink.tagName === 'A') {
parentLink.setAttribute('data-fancybox', 'gallery');
}
} else {
const link = document.createElement('a');
link.setAttribute('data-fancybox', 'gallery');
link.setAttribute('href', img.getAttribute('src'));
img.parentNode.insertBefore(link, img);
link.appendChild(img);
}
});
// 初始化 Fancybox
Fancybox.bind("[data-fancybox]", {
// 您的自定义选项
});
}

文章目录
×

* [1.漏洞简介](#toc-1-)
* [2.影响版本](#toc-2-)
* [3.fofa语法](#toc-3-)
* [4.漏洞分析](#toc-4-)
* [5.漏洞复现](#toc-5-)



.x\_nav\_toc {
position: fixed;
top: 0;
right: -300px;
width: 280px;
height: 100%;
background-color: white;
box-shadow: -2px 0 15px rgba(0, 0, 0, 0.1);
z-index: 1000;
transition: right 0.3s ease;
display: flex;
flex-direction: column;
overflow: hidden;
padding-top: 10px;
}
.x\_nav\_toc.active {
right: 0;
}
.x\_toc\_header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 15px 20px;
height: 48px;
border-bottom: 1px solid #eee;
}
.x\_toc\_title {
font-size: 18px;
font-weight: bold;
color: #333;
}
.x\_toc\_close {
background: none;
border: none;
font-size: 24px;
cursor: pointer;
color: #777;
transition: color 0.2s;
}
.x\_toc\_close:hover {
color: #333;
}
.x\_toc\_content {
flex: 1;
overflow-y: auto;
padding: 15px 20px;
padding-right: 10px;
}
.x\_anchor-list {
list-style-type: none;
padding: 0;
margin: 0;
}
/\* 减小目录项间距 \*/
.x\_anchor-list li {
margin-bottom: 4px; /\* 间距从8px减小到4px \*/
}
.x\_anchor-list a {
text-decoration: none;
color: #555;
display: block;
padding: 6px 10px; /\* 减少内边距 \*/
transition: all 0.2s;
font-size: 14px;
border-radius: 4px;
line-height: 1.4; /\* 减小行高 \*/
}
.x\_anchor-list a:hover,
.x\_anchor-list a:focus {
background-color: #f8f9fa;
color: #0068d6;
}
.toc-number {
font-weight: 600;
margin-right: 8px;
color: #495057;
display: inline-block;
min-width: 25px;
}
/\* 减小各级标题间距 \*/
.toc-h1 {
font-weight: 600;
font-size: 15px;
margin-top: 10px; /\* 上边距从15px减小到10px \*/
padding-left: 5px !important;
}
.toc-h2 {
font-size: 14px;
padding-left: 15px !important; /\* 缩进从20px减小到15px \*/
}
.toc-h3 {
font-size: 13px;
padding-left: 25px !important; /\* 缩进从30px减小到25px \*/
}
.toc-h4 {
font-size: 12px;
padding-left: 35px !important; /\* 缩进从40px减小到35px \*/
}
/\* 修改后的切换按钮样式 - 使用图标且位置下移 \*/
.x\_toc\_toggle {
position: fixed;
bottom:120px; right: 17px;width:40px;height:40px;background-color:white;
border-radius: 50%;
border: none;
cursor: pointer;
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
z-index: 999;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
padding: 0;
}
.x\_toc\_toggle svg {
width:24px;height:24px;stroke:#3d9bff;
}
.x\_toc\_toggle:hover {
#background-color: #0081f8;
transform: translateY(-3px);
box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
.x\_nav\_toc {
width: 280px;
}
.x\_toc\_toggle {
bottom: 100px; /\* 手机端也下移位置 \*/
right: 30px;
width: 40px;
height: 40px;
}
.x\_toc\_toggle svg {
width: 20px;
height: 20px;
}
}

document.addEventListener('DOMContentLoaded', function() {
// 获取所有标题元素
var className = ".line-numbers";
var selectors = [];
for (var i = 1; i <= 6; i++) {
selectors.push(className + ' h' + i);
}
var headings = document.querySelectorAll(selectors.join(', '));
// 获取DOM元素
var tocContainer = document.querySelector('.x\_nav\_toc');
var toggleButton = document.querySelector('.x\_toc\_toggle');
var tocList = document.querySelector('.x\_anchor-list');
var closeButton = document.querySelector('.x\_toc\_close');
var currentHighlight = null;
// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// 如果没有标题，隐藏所有元素
if (headings.length === 0) {
tocContainer.style.display = 'none';
toggleButton.style.display = 'none';
return;
}
// 初始化层级计数器
var counters = [0, 0, 0, 0, 0, 0]; // h1-h6
var currentLevel = 0;
// 生成带数字编号的目录
headings.forEach(function(heading, index) {
var level = parseInt(heading.tagName[1]);
// 更新计数器
counters[level - 1] += 1; // 增加当前级别计数器
// 重置更低级计数器
for (var i = level; i < 6; i++) {
counters[i] = 0;
}
// 生成编号字符串（如"1.2.3"）
var numberParts = [];
for (var i = 0; i < level; i++) {
if (counters[i] > 0) {
numberParts.push(counters[i]);
}
}
var numberText = numberParts.join('.')+'.';
// 创建唯一ID
var id = 'toc-' + numberText.replace(/\./g, '-');
heading.id = id;
var listItem = document.createElement('li');
var anchor = document.createElement('a');
var numberSpan = document.createElement('span');
numberSpan.className = 'toc-number';
numberSpan.textContent = numberText;
anchor.appendChild(numberSpan);
anchor.innerHTML += heading.textContent;
anchor.href = '#' + id;
anchor.classList.add('toc-h' + level);
listItem.appendChild(anchor);
tocList.appendChild(listItem);
// 添加点击事件（不关闭目录）
anchor.addEventListener('click', function(e) {
e.preventDefault();
// 更新高亮状态
if (currentHighlight) {
currentHighlight.classList.remove('active');
}
this.classList.add('active');
currentHighlight = this;
// 滚动到对应位置
var targetId = this.getAttribute('href').substring(1);
var targetElement = document.getElementById(targetId);
if (targetElement) {
var header = document.querySelector("header");
var headerHeight = header ? header.offsetHeight : 0;
var elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
var offsetPosition = elementPosition - headerHeight - 20;
window.scrollTo({
top: offsetPosition,
behavior: 'smooth'
});
// 滚动到目录项的可视区域
this.scrollIntoView({behavior: 'smooth', block: 'nearest'});
// 点击事件中
if (isMobile) {
closeToc(); // 移动端点击后关闭目录
}
}
});
});
// 切换按钮点击事件
toggleButton.addEventListener('click', function() {
tocContainer.classList.add('active');
});
// 关闭按钮点击事件
closeButton.addEventListener('click', function(e) {
e.stopPropagation();
closeToc();
});
// 滚动时更新高亮状态
window.addEventListener('scroll', function() {
var fromTop = window.scrollY;
var header = document.querySelector("header");
var headerHeight = header ? header.getBoundingClientRect().height : 0; // 更精确的header高度
//console.log(headerHeight);
// 精准计算标题文档位置
var activeSection = null;
headings.forEach(function(heading) {
var section = document.getElementById(heading.id);
if (!section) return;
// 使用getBoundingClientRect获取精确位置
var rect = section.getBoundingClientRect();
var sectionTop = rect.top + fromTop; // 转换为文档顶部绝对位置
var sectionBottom = rect.bottom + fromTop + headerHeight;
// 增加20px激活区域缓冲
if (fromTop + headerHeight + 20 >= sectionTop && fromTop < sectionBottom) {
activeSection = heading;
}
});
// 更新高亮状态（新增精确边界判断）
if (activeSection) {
var tocLink = tocList.querySelector('a[href="#' + activeSection.id + '"]');
if (tocLink && currentHighlight !== tocLink) {
if (currentHighlight) {
currentHighlight.blur();
currentHighlight.classList.remove('active');
}
tocLink.classList.add('active');
tocLink.focus();
currentHighlight = tocLink;
// 平滑滚动到可视区域（改进触发条件）
var tocRect = tocLink.getBoundingClientRect();
var tocContainerRect = tocContainer.getBoundingClientRect();
if (tocRect.bottom > tocContainerRect.bottom || tocRect.top < tocContainerRect.top) {
tocLink.scrollIntoView({behavior: 'auto', block: 'nearest'});
}
}
}
});
// 关闭目录面板
function closeToc() {
tocContainer.classList.remove('active');
}
});

/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
#qrcode-right {
display: none;
}
}

版权所有：[Mrxn's Blog](https://mrxn.net/)  
文章标题：[红帆ioffice PgcaUserLogin.aspx SQL 注入漏洞](https://mrxn.net/jswz/ioffice-Identity-PgcaUserLogin-sqli.html)  
文章链接：<https://mrxn.net/jswz/ioffice-Identity-PgcaUserLogin-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ioffice-Identity-PgcaUserLogin-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

  

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
* [深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)
* [深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)
* [深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)
* [深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)
* [深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)
* [深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)
* [深信服运维安全管理系统 del\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html)
* [深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)
* [九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)

编程

  

/\* 底部展示样式 \*/
.qrcode-bottom-box {
margin: 40px auto;
text-align: center;
}
.qrcode-title {
font-size: 16px;
color: #666;
margin-bottom: 0px;
font-weight: bold;
text-align: center;
}
.qrcode-bottom-box img {
display: inline-block;
padding: 10px;
background: #fff;
border-radius: 8px;
margin: 10px auto;
}
/\* 悬浮展示样式 \*/
.qrcode-float {
position: fixed;
z-index: 9999;
background: rgba(255,255,255,0.98);
padding: 20px;
border-radius: 12px;
}
.qrcode-float:hover {
transform: scale(1.05);
}
/\* 移动端适配 \*/
@media (max-width: 1440px) {
.qrcode-float {
right: 2%;
transform: none;
}
}
/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
.qrcode-float {
display: none;
}
}

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALd0lEQVR4Aeyci5Ljtg5EffL//5y7mN4jixBpeR537KpoKkgT3Q2QS0g7481W/rndbv9+Jf79oa++d2/b9Wdye3Sv/Ar1q/dcvmP3mX8FayB/6q5/3uUGtoH8mfrtmegHB25Apz84uPPAxgEHv3sDT/n07xvJQXqY64HwEOy8fhj17oPoEFTvaL8z3NdtA9mT1/p1N3AYCGTqMOLqiE6/65/lIfv1PuZn/UrXK0J6ljYLiH7mh/h6D+vOEFIPI87qDgOZmS7u927gxwYC4/RhzH26YM73X7J+sevmcO8nJ65qITXdpx/mOox8rzf/Dv7YQL5ziKv2fgM/PhCfso5uKW8O41O30iE+GNE+hRCt1vuAkV/tYU3XV/zKp/8r+OMD+cohrpr7DRwG4tQ73kvGFeTp0w/c+BOj655B/DLWmUN0CMp3tG6GemHeA0beHqs6GP0w5tat0P4dZ/7DQGami/u9G9gGApk6PMbPHg3Sr9f5tEB0c31nuT5IPSC1Ye+xCX8X6sDHnw78pT8NMK+H8PAY9xtuA9mT1/p1N/CPT8lncXVk+6ibQ56SnusTu95zfaJ6oZwI8z3LWwHR9YulVfQcPuevHp+N6w3x1t8ETwcCeSpgjj4B/dcDo7/7zEXrIXXm4soH8cMdew1Ek4cxlxdh1GHMuw9GHZJDUH9HOOqnA+lNrvz/ewP/QKYEc+zb+6SKkLpnfRA/zNG+IsRnf3nzPaqJMK9VF/c9ai0P8/ry7ONZP6QfBK3b97rekP1tvMH6MBCnJvYzQqYrrw9GXr2j/hXC2Eff7XYbWq34MkF66BFLq4DoECyuAsa8uIpeX1zFii/tq3EYyFcbXXU/cwOHgUCeEgj2bfpTAfF1vtf1HFLX+VUfmPv39RCPPSA5jKje0V4Qv7kIn+N7nfvJi5C+wO0wkNv19dIb+PRAINP01Kupq4srH4z9IDkEez2Eh6B9C/XCqMl3hPg6X70qOn+WV03Fme+R/umBPGp2ad+/gcOfZdmyJl3R8+Iq5GF8yiA5PMbqUdH7FLcP9Y564L6PnAjRzMXeC0af+sqvLuqD9JHvCHPd+sLrDem39uJ8GwjMp+f5IDqM2PWacoW8WFyFOaSPuQjhYUT1jtXTWGkw9oLk1onWQ/Se6xNh9Mlbt8JHvm0gq+KL/90b2P4sa7Wt0zxD6yFPjf4zXl9H676CkDNA8GHvPxtAfH+WH//oh5GH5BD8MO/+BeGt30kfyxUPqQOuzyG3N/ta/pYF96kB27GB4b8/w5hvxr8LnwoR4u/5X/sG6uIm/F1A+vxNPwDCrWo+TE/8C9JnZT3rD4/rV32LXw6kxCt+/wa2zyGrrX0aIFPvuXXy5hA/BOW7zxxGH4x5r7dOfoZ6YN4Lwp/57K3v2Xzlg+zb9ep/vSHeypvgNpCaToXnqnUFZJq1roAxL67COrG4CvMVQvqpQ/KqrYDk6s8gpAaC1kDy6lsh/12E9LVP9a6A8DCivhluA5mJF/f7N3D4HFKTrVgdpbQKyNT1wZjLd4T4IFi9ZgGjDslhje4167fn9K1w7621Ppjv3XXzjtWrQh6O/a43xNt5Ezz8lAWZmueriVaYQ/TiKuRrXWH+WYT0heCqvvaoUK+1IQdjD5jn1kF081Uf9Y765YGPz2rm6pB9zEV9hdcb4q28CR4GUlOqgHGakLy0CkgOQX89pVXAyKufYdXuo/shffXsdTkR4t17aq1e6wpzGP3y5amA6DCiPghf3goY8+Iq9IvFGYeBKFz4mhs4DAQyVacHyT0ejLm8CNGtFyG8Pvmew+hT7wjxwRpXNZ0/yz2rqN8ccgb5FT7jPwxk1ezif+cGnv4c4nQ79mOqw/ypUe91EH/XYc7rm6G91cxFSE8IyuuH8DCiPhGim1vfUb0jpB7ueL0h/ZZenC8/h0Cm1s8Hc14fzHWfGn0ijH5IDkF9K4T4gIMFmH4e6GeB+A4NGgHx9fpm+9gT6PSSt1/h9YYcru21xDWQ197/YffDQOq1MQp7RXEVnTcvbR/yIvDx6pqL1qxyeFxX9dausDwVkF61rtAPc15dhPjMO1bPis6bl1ZhDukHXH/J4fZmX9uPvXCfEtzXnhfuHNzX6iuEeLsOc76enAr9td6HPKQejqjHOnOIt/M919/xzAfpDyPax3qI3vnSD79labrwNTdw+LG3plTRj1Pco+h+c2sgT4V5180hPvOOq/ri9da6wlwsrgLme5RW0f3mkLryVMjXeh/yohqkvvPmhdcbUrfwRrF9D/FMkCk6VbHr5iuE9FG3D4y8uqjPXITHdeVb1ZZWAemx8kH08lbAmBdXAeFXfToPj/0QHbh+yrq92df2PcSpip4T7tMDtv/ZMoTXt0KID4L2F62D6DCi+gph9AObFfj4zANBBUgOQfkzXJ15Vadf1LfKi7++h3hLb4LL7yGer6a2D3juqdrX1Np+t1tWkD4QLM8s4r5tb+Yqly+E9Kz1MwHxuz+M+VkPiH/lg1GHMd/XXW/I/jbeYL19D4FMrT8lEN6zqosw6vpWCHM/hIdgr4c5v/d5JnGvzdb6RD3mkD173n3q8pA6CMo/g9cb8swt/aLndCCr6fczwvg0QHII6refKC+e8bDuB9Eg2HvaW1QXYayTF60T5SF1EJQX9UN0c3UID1yfQ25v9rV8Q5wi3KcH988hz/467NP9kL7qoj6IDkH57pPfY/fA2AOSQ3Bfu1/3Pmowr+t+c4i/5/aTL1wORPOFv3sD2+eQmk4FZJoQ9DilVcCcL60CRv2sXl2Esb56Vqx0iB/uby+Eq7qKXltcxRnfdXMR5vtU7wp9n8HrDfnMbf2C9/A5xD1rwhXmYnEVkKcDRtTXEeKTrx4V5mJx+4CxTh+E11sII6dXLE8FxNd5845VUwGP6yA6jGg/CG8uQnjg+inr9mZf229Z9QRU9PMVVyEPmab5Z7F6VcDYB5LDiPaH8OYihIfj9xA9ZwjpoQ8e53X+ipVfvjyzUIdxn+K3gVRyxetvYPspa3UUyBQhOJv4I27V1xpI35VPXr+5KF8I6VXriu7peXkq5CH1q7y8FV0vrkK+I4x9y7uK6w3pt/fi/PBTlpPzXD2HTBuC+iA5BOVF+0B0CMrrEzsP8XcdwsP9e4geuGtwX6uLfS958UzvPv2QPc31QXjzPV5vyP423mB9GAhkehD0jE5ZlH8WIf1W9fIixN/7q8ubF8rBWFtahboI8UFQviPM9epZAaMOY24/mPPqhYeBFHnF625g+VNWTb6iHw3mUy7vPiA+CKrZzxyiy8OY6+s6xAdH1Nux9+q5/jsvMyJkz5G9bX/D5da+YPQ/6n+9Ie3yXp1uP2U5NXF1MHURxulbp27eEeZ13Wfe+5nP0JoVwrh379Hr1GGsgzHX17H3e5Rfb8ij23mBtn0PgUwbnsNnz+rT0v3yYtfNYTyPvAh3XU7svSHezusX4bHPetE6EVJv3hHW+vWG9Nt6cb4NxGmf4VfPC3kqYET7QfjV/vo67v1dW+WQvdRhzO250iF+COoTe/2Kh9TDHbeBWHTha2/gMBC4Twvu67NjQrzdB+F9akR9MOqQvOvmIsQHR9QjQjzm/QzyIsQPQXnrOqpD/DBi183Ffb/DQDRd+Job+PZAnK7Hh/nT0fVVXefNRfvMUI8IOYteeXMYdfnukxdhrDvzWyc+8n97IG5y4c/cwI8N5NHU66iQp0ofJC9tHzDykByCeu1jvkd47IXo9hAh/L7XV9b2s7bnsN7nxwbi5hd+7wYOA3GaHc+2gUzdOv09h9GnLloH8ZmL+mCu63uE9tAD6SUPydVFGHkYc+v1fwUPA/lKk6vm525gGwhk2vAYV1v7dEDqzVd+iA9GtE5c1T/iey2Me0DyRz1mmn1FPTDv13097/XA9TcXb2/2tb0hb3au/+xx/gcAAP//6IlSbwAAAAZJREFUAwBLjlnFkatS+gAAAABJRU5ErkJggg==)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ioffice-Identity-PgcaUserLogin-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 