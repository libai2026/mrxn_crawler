---
title: "天锐绿盾审批系统 findTenantPage.do SQL注入漏洞"
source: https://mrxn.net/jswz/trwfe-findTenantPage-sqli.html
asset_dir: assets/天锐绿盾审批系统-findtenantpage.do-sql注入漏洞
---

# 天锐绿盾审批系统 findTenantPage.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/21 08:31
* 378浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

加密

计算机安全

SQL


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，旨在为企业提供从文件创建、流转到归档的全生命周期安全管控，并常作为OA系统中的加密软件，实现审批流程的自动化和信息化。

SQL注入防护

天锐绿盾审批系统的 `findTenantPage.do` 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。攻击者可以通过构造恶意的SQL查询参数，直接操控数据库查询语句，从而绕过身份验证，获取未授权的数据、修改数据库内容或执行其他恶意操作。该漏洞可能导致敏感信息泄露，例如用户数据或系统配置信息，严重影响系统的数据完整性和机密性，进而降低整体系统安全性。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 代码安全审计

# 漏洞分析

先看`findTenantPage.do`的实现

[![天锐绿盾审批系统 findTenantPage.do SQL注入漏洞](images/img-001-7a1e1f4072cb.webp)](https://image.mrxn.net/c5e7b6efb810497f9d904bf2cb0e483e.webp)

看下PageVo对象的定义

漏洞扫描服务

深入探索

防火墙软件

服务器安全服务

网络安全课程

[![天锐绿盾审批系统 findTenantPage.do SQL注入漏洞](images/img-002-63173bdcdabe.webp)](https://image.mrxn.net/de76b53066a3431bba15f666517e57df.webp)

在 `getPageSql()` 方法中，来自用户请求的 `sort` 和 `order` 成员变量被直接拼接到 `pageSql` 字符串中。由于这两个变量的值完全由用户控制且未经过任何安全处理，攻击者可以构造恶意的 SQL 片段。

安全运维咨询

再跟进`findAllTenantPage` 方法，看下`findAllTenantPage`最终的**MyBatis 映射文件内容**

[![天锐绿盾审批系统 findTenantPage.do SQL注入漏洞](images/img-003-1db6e20e64aa.webp)](https://image.mrxn.net/7d2f486d897d4584ac42d2f2934e7f83.webp)

此处的 `${pageSql}` 语法在 MyBatis 中表示直接进行字符串替换，而不是使用预编译的参数化查询（`#{...}`）。这意味着 `pageSql` 变量的内容将作为原始 SQL 代码的一部分被执行，这是导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的直接原因。

该代码段提供了一个分页查询租户信息（Tenant）的功能。前端通过调用 `/findTenantPage.do` 接口，并传递 `page`、`rows`、`sort`、`order` 等参数来控制分页和排序逻辑。后端接收到参数后，通过 `PageVo` 对象进行封装，并最终调用 MyBatis 执行数据库查询。

物流软件安全

由于后端在处理排序参数 `sort` 和 `order` 时，未进行任何安全校验或过滤，直接将这些参数拼接到 SQL 语句中，造成了 **[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞**。攻击者可以利用此漏洞执行任意数据库操作，例如窃取数据、篡改信息，甚至在特定数据库和权限配置下获取服务器控制权。

计算机科学

# 漏洞复现

```
POST /trwfe/login.jsp/.%2e/invoker/findTenantPage.do HTTP/1.1
Host: trwfe.mrxn.net
Content-Type: application/x-www-form-urlencoded

sort=SQLI_POC&order=asc
```

成功延时 5 秒

编程

[![天锐绿盾审批系统 findTenantPage.do SQL注入漏洞](images/img-004-e3cf7c8d799c.webp)](https://image.mrxn.net/08aaa3f44f7044ffa57f2c9a8010283f.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)

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
文章标题：[天锐绿盾审批系统 findTenantPage.do SQL注入漏洞](https://mrxn.net/jswz/trwfe-findTenantPage-sqli.html)  
文章链接：<https://mrxn.net/jswz/trwfe-findTenantPage-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-findTenantPage-sqli.html"),
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

安全运维咨询

  

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

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKGUlEQVR4Aeyci3YbNwxEffP//9wKiwwBkViKiiWtm7LHyIAzA3BNLP1Ie/rr6+vrn+/GPwv/5D0qu/SsiRPONHmeQfV7VFP5xAkf9VjVbSA37/74KSfQBnKb9NczUX0CwBfcR+V7BffMs5q32hP8WU1XVL6KA6+tNPVaxdyjDSSTO7/uBIaBgE8eapw9avVGgPfJdeAcBKoWRq7Scr8+h+gBnqtHRtWBe4Dyq4R8Va20CiH6wphXNcNAKtPmPncCeyCfO+ulnd4+kHzNlevJtDYEv9KWK8C5mR/cA4Gqz6geGbOuHKIP3Oe59l352wfyrgf/W/teMhC9jflQVziIN7byqx+Er+e0zgijP+tVPtu/8q9y7xnI6u7bN5zAHshwJNcSw0B0Fc9w9rgQVx88X/XLB14HI8pjCK7n5zT+mYDzHrmvcnA/BM72U90ZVrXDQCrT5j53Am0gEFOHx/nsEfMbAd4r+8G5ypc51YjT2lAceC+I37JNf2WA76E9DWf9wf2whrlXG0gmd37dCeyBXHf25c6/7Pp9N/rOEFdVGgSn/aRlhDWfatTLcIWTJyOMe0Jw2XuW2/6viH1Dzk74In5pIBBvC5znekOqz0WaIXiPyldxcO4H16BG9YNRl/YI7ZktIHr0NRAaeN57+jWMvqWB9I0uWv8vth0GAj41CKxOwt4YRa+LzwjzfupR1WROOXg/rc8Qzn3aMyOMfunVHtIqBO8FgdmnfhD6MJBcsPPPn8AeyOfPfLrjL4jrAvHbrl2nqtJ4C4g6+cA5rQ3BOatRGL8SvR+8F9DKgY/9ly5t01sC9/vqWR/hrXT6sW/I9Hg+L7ZfDLU1xOSraYPrlSZOvc6w8okD7w+0cuC4BY24JfJXCO4Hbs77D+DoBfdfDfo+ED51gJFb0cwDXmv5LPYNmZ3OBdoeyAWHPtuyfVOXKV9dOL9m4BrMUX0hfOJWUc+06l/1QTwTeD6r1XMY9j7jFDD2ktbX2Vqa4b4hdiI/KNpAbDoW4NOF+KYHI2dehT6ffm18xYH3M/2ZUC9D+H4P69MHeN/M6xnBNUBUQ6D9sCASnufaQNRk47UnsAdy7fkPuw+/h+SrCn7lKg5cg/jSNnS/EeC+3ONGL32A187M4B4IzH7tC6GD59nX5+AeoEnqlbGJKZGeqJZKM2xkSvYNSYfxE9Lhx16gfXOyKVrkB7V1H1nvc3kh+soDwYHn0gxVa/lZyJOx8kqvtMyt+sCfV/6MMGp5j1m+b8jsdC7Q9kAuOPTZlksDAb+CQOsFtC9t4LnEfH0rLuvK5Zsh+D4QP0hAcCu12s9QfljrIb+h1VtYvhLgezzyLg3kUZOtDyfwx8QwEJu6AsapgnPyZATX8tPAGpf7KIexNve2XF5DW/cB5z3gXLN+Cjj3gWsQqGeA4NRLmiG4brliGIiEjdecQPvFEMZp6ZE0XUNx4H4INN0C5tysh7QKrbdCOsRe4Lk8GSu/uArBe0F8v6p82mOmmUc6zPvuG6KT+iG4B/JDBqHHaAOxa2UhwdDWFpYrbH0WlUdcxqpeOoxXGoKD+1x1hupreR8zrff2a7jfE2Itr/obissIXmO6IuvK20BEbLz2BKYDAZ9qfkRwDgKlg3NanyGc+/T2GIL7LLfI/WxtkTlwP4yYfcqtvo9KqzjVge8lj6E0y2cBXiu/4XQgs2Zbe88J7IG851z/uOv0r9/tClmAXy2In8mNV4Drs6eQ11A+8DpAVInA8fdmlWj9FNK1zgjeI3Pyg2uAqDtUzR3ZLYDjGaHGqoc4iJp9Q7qDvXrZBgI+pfxA4JwmaSgdXANEtf/5VyNuCXC8Obe0fVifPiSC+wFR077A0R9o/irRfkDzg+eV/xEHXqu+GR/VzvQ2kJlpa587gT2Qz5310k5tIPnK9Tn49YTA7Ol3gtHXe2wNoy/3VQ7usxqFNK0fIXgP1WWsasH9QJOB9uVOJDintaF6W66A0Qcj1waiwo3XnkD763c9BvjUIFBaRgi9fyO0NlQNhB88N10BzslfobyG8Nhf9QCvg0Drp6hqxMljKG6G5lOs+vYNmZ3UBdrwi2F+Bk03o/TMQbxtgCwHAsfX3exXDq5B/MIJwR0Nbn/M/NIy3kraB3g/EdmnHNwDyNZ+1DZPI4vEdAvg+DyhRvNYQOhqB8FdcEP0GBurE9gDqU7lQm4YiF0rhZ4L4kpVXO+XJyOMPVRnCK6f1UB8WTN/9s1y8+YA3wcoy4DjS08WYeSyfpbnfeXJnHJphsNAjNxx3QksDUSTPEPwN0g6+Bru32rp1acrLaN84iD6SoPgYMx7n3oZSrO8D4he8sE5J4+helmuAK/VOqP8hksDycU7f+8J7IG893yf7v70QMCvHgT2u9rVU4D7eo+twTWocdYDvEYeQ+tpYbnC1jnA64BGA8c3cghs4i1Rr4w3+u4ja+B9skF65qr86YFUTTb3uhNoAwGfKgTOttHEDXsfRA/TLbIHXM+ceSwyB+4z3iJrsxy8Dmg2q7doREqMnwVw3KBUcvebvNWCe4BmA446oHFVAjRfG0hl/C9xf8uz7oH8sEm2v363a9fH7FkhrtnMJw3W/PkZVLuKqs1+iH2BLLUvE0DLZYDgVvrKY6geGSH6gedZV75viE7ih+AwEPDpQY32BvShzwW8JuvSKsw+8FoI7Guyv9dsDV6bfcpNt9A6o/EK8B5aG8LIGf8nkfcF75u5YSB/ssmued0J7IG87ixf0qn9G0Pw6/OoK7gPAvsaCA08z9ey9z9ag/fIPvV7xIHXyg++BlqptIxNvCXib+npBzD8YHBqngj7hkwO5wpp+mOv3oxV1CeQ/eIg3iDp0s5w5gPvd1YrftZDHvBeECjNEIIHz423UP8KTVdIB6+H+FcTENy+ITqxEj9PDt9DIKYFa3n/2BB1ejOyB0IHz+XLqBpx4F6o3y4IHTxXD6F6GYrLaHwfWT/LwfcDziwHn3sfRPfHviHdgVy93AO5egLd/m0g+Sqt5F2fh8tHPYHjx8aHjTpD7ttJd0vw/jDiox7S7xp2C3kMO+lYgu97LH7/Ac5ZjaIN5Ldnw8UnMAwEfGpQ47PPC3UfuOdnfcG92QPOQaDesozgurjc4xU5eH8YMffX/hA+6RDcMBCZNl5zAnsg15z76a4vHYiuZbWbNMNKFwdxfcFzaasIXgcslQDHDxQwR3t2hRprnbHSwHtXPvkNXzoQa7jj8QnMHG8fiN4I8DcEaM8j7QxlrPRKA443Pfvl+w6qX+4hDnzPSsvcav72gaw+yPb5CeyB+Dn8mD+HgegqnuHKk+da+SsO/LpDjaoF17U2VD/L+wD3A00Chi9n6lFhKzxJwPtVMoya9qj8mRsGksWdf/4E2kDApwprOHtUiB7yQXB6WyqUv0KIHtJh5KQZag/Lvxsw7qX+MGoQHHhePYN6GLaBVMbNff4E9kA+f+bTHf8FAAD//xPEiWAAAAAGSURBVAMAQ1tqqvY7lDcAAAAASUVORK5CYII=)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-findTenantPage-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 