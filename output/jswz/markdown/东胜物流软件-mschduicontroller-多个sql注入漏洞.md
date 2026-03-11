---
title: "东胜物流软件 MsChDuiController 多个SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html
asset_dir: assets/东胜物流软件-mschduicontroller-多个sql注入漏洞
---

# 东胜物流软件 MsChDuiController 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/26 08:37
* 223浏览
* [0评论](#comment)
* 6分钟阅读

深入探索

软件

服务器

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 MsChDuiController 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

安全研究工具

Windows安全工具

漏洞扫描器

看下`MsChDuiController`方法下的**GetDetailList** action是如何实现的

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-001-4eb191aef8fa.webp)](https://image.mrxn.net/2c40b55a880048c98af70b2e2430d4d0.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-002-e077a638a6dc.webp)](https://image.mrxn.net/f860ab4535004999886c242674edc762.webp)

如上图所示，参数**condition**是被直接拼接进SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

深入探索

网页浏览器

编码转换工具

安全

其他action也是差不多的问题

SQL注入防护

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-003-0bfaa520ac39.webp)](https://image.mrxn.net/01065d33afcd406bab883bb244d6e2be.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-004-65a8d41d2023.webp)](https://image.mrxn.net/6fe32ec172434ade9cc3732fcabd501e.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-005-7532b06cac65.webp)](https://image.mrxn.net/34fc9320a5e54072a6af4e7f458d289f.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-006-4c487a12fbbe.webp)](https://image.mrxn.net/cab15652d7724365a599ff76915b4f02.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-007-0a85c0820d59.webp)](https://image.mrxn.net/3ac64409038d4d41892543c8aa45769f.webp)

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-008-8b1286fa3aac.webp)](https://image.mrxn.net/5000011f31e143cea5d4d2054acae850.webp)

# 漏洞复现

```
GET /MvcShipping/MsChDui/GetDetailList?condition=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 MsChDuiController 多个SQL注入漏洞](images/img-009-88a374feebff.webp)](https://image.mrxn.net/2daad20d262b453280fe0b55db0e6be1.webp)

成功利用报错注入在响应里回显数据库版本信息

代码安全审计

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
文章标题：[东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html"),
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
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

漏洞预警服务

  

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
text: encodeURI("https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 