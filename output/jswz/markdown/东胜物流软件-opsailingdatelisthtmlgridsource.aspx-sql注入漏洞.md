---
title: "东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateListHtmlGridSource-sqli.html
asset_dir: assets/东胜物流软件-opsailingdatelisthtmlgridsource.aspx-sql注入漏洞
---

# 东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/15 08:45
* 246浏览
* [0评论](#comment)
* 9分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 OpSailingDateListHtmlGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据 `OpSailingDateListHtmlGridSource.aspx` 的代码引用 `DSWeb.PriceCarrier.OpSailingDateListHtmlGridSource`，在dll中找到它的逻辑实现

[![东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞](images/img-001-a47838f6a1d1.webp)](https://image.mrxn.net/dc537bc0c0314c53a40e36e3e039734e.webp)

[![东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞](images/img-002-644efcf25192.webp)](https://image.mrxn.net/7053fcc26652482ab37df2d80a68acb4.webp)

当`handle=list`时，进入`GetLogContent`方法

[![东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞](images/img-003-e81843594700.webp)](https://image.mrxn.net/400600be11ad494181b0ca88d83480da.webp)

1. 程序获取 `TITLE` 参数的值，并使用 `Regex.Unescape` 进行处理。此函数非安全函数，它仅对转义序列（如 `\n`, `\t`）进行解码，并不会对[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)相关的特殊字符（如 `'`, `;`, `-`）进行过滤或转义。
2. 处理后的字符串 `str` 被直接拼接到一个 `LIKE` 查询子句中。

`TITLE` 参数在未经过任何过滤或参数化处理的情况下，被直接使用字符串拼接的方式嵌入到 SQL 查询语句中。

SQL注入防护

# 漏洞复现

```
GET /PriceCarrier/OpSailingDateListHtmlGridSource.aspx?handle=list&cur_page=1&show_page=10&TITLE=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞](images/img-004-bb339bd5dfbc.webp)](https://image.mrxn.net/a9de541f054a4484bdf9908d7dd9e536.webp)

通过报错注入在响应里回显数据库版本信息。

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
文章标题：[东胜物流软件 OpSailingDateListHtmlGridSource.aspx SQL注入漏洞](https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateListHtmlGridSource-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateListHtmlGridSource-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateListHtmlGridSource-sqli.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/dongsheng-PriceCarrier-OpSailingDateListHtmlGridSource-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 