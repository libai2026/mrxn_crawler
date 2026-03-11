---
title: "东胜物流软件 ModuleGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-Modules-ModuleGridSource-sqli.html
asset_dir: assets/东胜物流软件-modulegridsource.aspx-sql注入漏洞
---

# 东胜物流软件 ModuleGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/20 08:42
* 218浏览
* [0评论](#comment)
* 6分钟阅读

深入探索

服务器

数据库

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 ModuleGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `ModuleGridSource.aspx` 的代码引用 `DSWeb.Modules.ModuleGridSource`，在dll中找到它的逻辑实现

[![东胜物流软件 ModuleGridSource.aspx SQL注入漏洞](images/img-001-cab6fb0390b5.webp)](https://image.mrxn.net/2a65567ae9c542a78c6824d204920b79.webp)

[![东胜物流软件 ModuleGridSource.aspx SQL注入漏洞](images/img-002-87f2b5d9a518.webp)](https://image.mrxn.net/b690853a26f94ceca5710d59fb7bcc6f.webp)

当`handle=list`时

深入探索

编码转换工具

JSON处理工具

文件大小转换

[![东胜物流软件 ModuleGridSource.aspx SQL注入漏洞](images/img-003-9448cb23f1a9.webp)](https://image.mrxn.net/6a2d7d2d1a5b45f09ec303309c137040.webp)

参数`search`被直接带入sql语句中，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /Modules/ModuleGridSource.aspx?handle=list&search=name:a%'SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 ModuleGridSource.aspx SQL注入漏洞](images/img-004-1f3383a42d48.webp)](https://image.mrxn.net/14d2cfd03e664c458691af1dae1d56ca.webp)

成功通过报错注入在响应中回显数据库版本信息。

SQL注入防护

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
文章标题：[东胜物流软件 ModuleGridSource.aspx SQL注入漏洞](https://mrxn.net/jswz/dongsheng-Modules-ModuleGridSource-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-Modules-ModuleGridSource-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-Modules-ModuleGridSource-sqli.html"),
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

代码安全审计

  

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
text: encodeURI("https://mrxn.net/jswz/dongsheng-Modules-ModuleGridSource-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 