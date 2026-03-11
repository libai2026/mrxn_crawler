---
title: "天锐绿盾审批系统 findPropertyPage.do SQL注入漏洞"
source: https://mrxn.net/jswz/trwfe-invoker-findPropertyPage-sqli.html
asset_dir: assets/天锐绿盾审批系统-findpropertypage.do-sql注入漏洞
---

# 天锐绿盾审批系统 findPropertyPage.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/26 08:26
* 416浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

软件

数据库

身份验证


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，旨在为企业提供从文件创建、流转到归档的全生命周期安全管控，并常作为OA系统中的加密软件，实现审批流程的自动化和信息化。

SQL注入防护

天锐绿盾审批系统的 `findPropertyPage.do` 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可以通过构造恶意的SQL查询参数，直接操控数据库查询语句，从而绕过身份验证，获取未授权的数据、修改数据库内容或执行其他恶意操作。该漏洞可能导致敏感信息泄露，例如用户数据或系统配置信息，严重影响系统的数据完整性和机密性，进而降低整体系统安全性。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

深入探索

计算机安全

鉴权

SQL

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 代码安全审计

# 漏洞分析

先看`findPropertyPage.do`的实现

[![天锐绿盾审批系统 findPropertyPage.do SQL注入漏洞](images/img-001-04f3bc4eb540.webp)](https://image.mrxn.net/6b7cd61a0d0f4bc2afa32e010c84c19b.webp)

看下PageVo对象的定义

漏洞预警服务

深入探索

安全

文件大小转换

VPN服务

[![天锐绿盾审批系统 findPropertyPage.do SQL注入漏洞](images/img-002-10f4667a058b.webp)](https://image.mrxn.net/26157ebbe994462e947fcfaed8513fbe.webp)

在 `getPageSql()` 方法中，来自用户请求的 `sort` 和 `order` 成员变量被直接拼接到 `pageSql` 字符串中。由于这两个变量的值完全由用户控制且未经过任何安全处理，攻击者可以构造恶意的 SQL 片段。

再跟进`findAllStartFormPropertyPage` 方法，看下`findAllStartFormPropertyPage`最终的**MyBatis 映射文件内容**

[![天锐绿盾审批系统 findPropertyPage.do SQL注入漏洞](images/img-003-e5897399b750.webp)](https://image.mrxn.net/b6a327134bb24577aa2b5dba329d12ee.webp)

[![天锐绿盾审批系统 findPropertyPage.do SQL注入漏洞](images/img-004-86dadeb9e1c5.webp)](https://image.mrxn.net/f4f2741f8b994b128cbda5ccad76b11d.webp)

此处的 `${pageVo.pageSql}` 语法在 MyBatis 中表示直接进行字符串替换，而不是使用预编译的参数化查询（`#{...}`）。这意味着 `pageSql` 变量的内容将作为原始 SQL 代码的一部分被执行，这是导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的直接原因。

该代码段提供了一个分页查询租户信息（Tenant）的功能。前端通过调用 `/findPropertyPage.do` 接口，并传递 `page`、`rows`、`sort`、`order` 等参数来控制分页和排序逻辑。后端接收到参数后，通过 `PageVo` 对象进行封装，并最终调用 MyBatis 执行数据库查询。

由于后端在处理排序参数 `sort` 和 `order` 时，未进行任何安全校验或过滤，直接将这些参数拼接到 SQL 语句中，造成了 **[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞**。攻击者可以利用此漏洞执行任意数据库操作，例如窃取数据、篡改信息，甚至在特定数据库和权限配置下获取服务器控制权。

Windows安全工具

# 漏洞复现

```
POST /trwfe/login.jsp/.%2e/invoker/findPropertyPage.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded

tenantId=1&categoryId=1&sort=SQLI_POC&order=asc
```

成功延时 5 秒

[![天锐绿盾审批系统 findPropertyPage.do SQL注入漏洞](images/img-005-8975f47344dd.webp)](https://image.mrxn.net/966c6c4dc77d446482a80943a72ae1d5.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)

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
文章标题：[天锐绿盾审批系统 findPropertyPage.do SQL注入漏洞](https://mrxn.net/jswz/trwfe-invoker-findPropertyPage-sqli.html)  
文章链接：<https://mrxn.net/jswz/trwfe-invoker-findPropertyPage-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-invoker-findPropertyPage-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/trwfe-invoker-findPropertyPage-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 