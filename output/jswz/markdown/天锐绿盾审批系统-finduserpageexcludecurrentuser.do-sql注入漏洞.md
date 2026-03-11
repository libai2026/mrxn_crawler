---
title: "天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞"
source: https://mrxn.net/jswz/trwfe-findUserPageExcludeCurrentUser-sqli.html
asset_dir: assets/天锐绿盾审批系统-finduserpageexcludecurrentuser.do-sql注入漏洞
---

# 天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/10 08:30
* 401浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

软件

计算机安全

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，旨在为企业提供从文件创建、流转到归档的全生命周期安全管控，并常作为OA系统中的加密软件，实现审批流程的自动化和信息化。

SQL注入防护

天锐绿盾审批系统的 `findUserPageExcludeCurrentUser.do` 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可以通过构造恶意的SQL查询参数，直接操控数据库查询语句，从而绕过身份验证，获取未授权的数据、修改数据库内容或执行其他恶意操作。该漏洞可能导致敏感信息泄露，例如用户数据或系统配置信息，严重影响系统的数据完整性和机密性，进而降低整体系统安全性。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 代码安全审计

# 漏洞分析

先看`findUserPageExcludeCurrentUser.do`的实现

[![天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](images/img-001-eb7b95748042.webp)](https://image.mrxn.net/b3eca8bc72654510b69371288cfd0bb1.webp)

看下PageVo对象的定义

深入探索

网络安全课程

安全研究报告

在线安全工具

[![天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](images/img-002-292dea5afb65.webp)](https://image.mrxn.net/378e8c5797ac428fb80b7a5ddd2c0bf2.webp)

在 `getPageSql()` 方法中，来自用户请求的 `sort` 和 `order` 成员变量被直接拼接到 `pageSql` 字符串中。由于这两个变量的值完全由用户控制且未经过任何安全处理，攻击者可以构造恶意的 SQL 片段。

漏洞修复方案

再跟进`findDeptUser` 方法，看下`findDeptUser`最终的**MyBatis 映射文件内容**

[![天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](images/img-003-28ca18fa7eda.webp)](https://image.mrxn.net/e0c85ea74dcf4a40a52a4ab30b57368c.webp)

[![天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](images/img-004-b570664f1541.webp)](https://image.mrxn.net/412f1aae164441d1b3ada9f2760feeb4.webp)

此处的 `${pageVo.pageSql}` 语法在 MyBatis 中表示直接进行字符串替换，而不是使用预编译的参数化查询（`#{...}`）。这意味着 `pageSql` 变量的内容将作为原始SQL代码的一部分被执行，这是导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的直接原因。

Windows安全工具

该代码段提供了一个分页查询租户信息（Tenant）的功能。前端通过调用 `/findUserPageExcludeCurrentUser.do` 接口，并传递 `page`、`rows`、`sort`、`order` 等参数来控制分页和排序逻辑。后端接收到参数后，通过 `PageVo` 对象进行封装，并最终调用 MyBatis 执行数据库查询。

由于后端在处理排序参数 `sort` 和 `order` 时，未进行任何安全校验或过滤，直接将这些参数拼接到 SQL 语句中，造成了 **[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞**。攻击者可以利用此漏洞执行任意数据库操作，例如窃取数据、篡改信息，甚至在特定数据库和权限配置下获取服务器控制权。

# 漏洞复现

```
POST /trwfe/login.jsp/.%2e/user/findUserPageExcludeCurrentUser.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded

deptId=1&sort=a.ID_SQLI_POC
```

成功延时 5 秒

物流软件安全

[![天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](images/img-005-810586842da2.webp)](https://image.mrxn.net/4148fafe01a645ea90db23d75c0c3db6.webp)

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
文章标题：[天锐绿盾审批系统 findUserPageExcludeCurrentUser.do SQL注入漏洞](https://mrxn.net/jswz/trwfe-findUserPageExcludeCurrentUser-sqli.html)  
文章链接：<https://mrxn.net/jswz/trwfe-findUserPageExcludeCurrentUser-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

编程

![](data:image/png;base64,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)

设备上扫码阅读

Windows安全工具


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-findUserPageExcludeCurrentUser-sqli.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/trwfe-findUserPageExcludeCurrentUser-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 