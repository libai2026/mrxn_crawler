---
title: "金和OA TaskCreate.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/jhsoft-TaskCreate-sqli.html
asset_dir: assets/金和oa-taskcreate.aspx-sql注入漏洞
---

# 金和OA TaskCreate.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/6 12:15
* 593浏览
* [0评论](#comment)
* 17分钟阅读

深入探索

漏洞预警服务

恶意软件分析工具

安全研究工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `TaskCreate.aspx` 接口处存在[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)，攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

先看下 TaskCreate.aspx 的代码定义区域

深入探索

网络安全课程

计算机安全

Docker加速服务

```
<%@ Page Language="c#" CodeBehind="TaskCreate.aspx.cs" AutoEventWireup="True" Inherits="JHSoft.Web.DailyTaskManage.TaskCreate" %>

<%@ Register TagPrefix="cc1" Namespace="JHSoft.UserControl" Assembly="JHSoft.UserControl" %>
<%@ Register TagPrefix="cc2" Namespace="HBControls" Assembly="HBControls" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <title>TaskCreate</title>
.....
```

在 `bin` 目录下查找 `JHSoft.Web.DailyTaskManage.dll` 将其进行反编译后找到 `TaskCreate` 的处理逻辑

[![金和OA TaskCreate.aspx SQL注入漏洞](images/img-001-697e38376f9b.webp)](https://image.mrxn.net/7dfba764b42844649f190a54b6fd234c.webp)

跟进 `GetTaskSuperior` 方法

深入探索

网络安全会议

安全研究报告

数据库

```
public void GetTaskSuperior()
{
  this.strSuperiorTaskID = this.Request["taskID"].ToString();
  string QueryString1 = $" select top 1 TaskID,TaskName,TaskNumber,TaskRootScale,TaskContent,OriginModule,OriginID from TaskManage where TaskID = '{this.strSuperiorTaskID}'";
  string QueryString2 = $" select FileID,FilePath from Files where ModuleID = 'ProjectTaskNew' and ModuleMessageID = '{this.strSuperiorTaskID}' ";
  DataTable dataTable = this.dbop.ExecSQLReDataTable(QueryString1);
  DataTable dt = this.dbop.ExecSQLReDataTable(QueryString2);
  if (((InternalDataCollectionBase) dataTable.Rows).Count > 0)
```

多个参数 **taskID** 被直接拼接进SQL语句中后执行，无任何过滤或校验，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /c6/Jhsoft.Web.dailytaskmanage/TaskCreate.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net
Content-Type: application/x-www-form-urlencoded

taskID='SQLI_POC
```

[![金和OA TaskCreate.aspx SQL注入漏洞](images/img-002-08a6abf8e690.webp)](https://image.mrxn.net/5973e13d8bfb423db2ff40f317f57e6d.webp)

延时 8 秒（执行两次）

[![金和OA TaskCreate.aspx SQL注入漏洞](images/img-003-dd89d49d8ebd.webp)](https://image.mrxn.net/12cd813a59494b5282b4e63ed77b8486.webp)

以及延时 4 秒（执行两次）

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
文章标题：[金和OA TaskCreate.aspx SQL注入漏洞](https://mrxn.net/jswz/jhsoft-TaskCreate-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-TaskCreate-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-TaskCreate-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/jhsoft-TaskCreate-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 