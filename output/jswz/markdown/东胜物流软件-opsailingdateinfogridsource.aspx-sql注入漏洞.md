---
title: "东胜物流软件 OpSailingDateInfoGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateInfoGridSource-sqli.html
asset_dir: assets/东胜物流软件-opsailingdateinfogridsource.aspx-sql注入漏洞
---

# 东胜物流软件 OpSailingDateInfoGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/16 08:50
* 198浏览
* [0评论](#comment)
* 7分钟阅读

深入探索

SQL

服务器

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 OpSailingDateInfoGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `OpSailingDateInfoGridSource.aspx` 的代码引用 `DSWeb.PriceCarrier.OpSailingDateInfoGridSource`，在dll中找到它的逻辑实现

[![东胜物流软件 OpSailingDateInfoGridSource.aspx SQL注入漏洞](images/img-001-f2cb50d09d2c.webp)](https://image.mrxn.net/4de4b8730a9b407580815d4ca67c9e85.webp)

当`handle=delete`时，进入`setDel`方法后，参数`gids`经过逗号分割后被直接拼接进SQL语句中，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

深入探索

服务器安全服务

企业安全咨询

VPN服务

# 漏洞复现

```
GET /PriceCarrier/OpSailingDateInfoGridSource.aspx?handle=delete&gids=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 OpSailingDateInfoGridSource.aspx SQL注入漏洞](images/img-002-14da6ea171eb.webp)](https://image.mrxn.net/20e25d345fd845b6ba31f4345e54cc1e.webp)

通过报错注入在响应里回显数据库版本信息。

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
文章标题：[东胜物流软件 OpSailingDateInfoGridSource.aspx SQL注入漏洞](https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateInfoGridSource-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateInfoGridSource-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateInfoGridSource-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateInfoGridSource-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 