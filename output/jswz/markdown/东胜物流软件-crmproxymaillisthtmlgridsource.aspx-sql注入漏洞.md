---
title: "东胜物流软件 CrmProxyMailListHtmlGridSource.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-PriceCarrier-CrmProxyMailListHtmlGridSource-sqli.html
asset_dir: assets/东胜物流软件-crmproxymaillisthtmlgridsource.aspx-sql注入漏洞
---

# 东胜物流软件 CrmProxyMailListHtmlGridSource.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/18 08:41
* 180浏览
* [0评论](#comment)
* 7分钟阅读

深入探索

SQL注入检测工具

Web安全书籍

Web安全课程


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 CrmProxyMailListHtmlGridSource.aspx 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

网络安全会议

漏洞扫描器

文本剥离工具

根据 `CrmProxyMailListHtmlGridSource.aspx` 的代码引用 `DSWeb.PriceCarrier.CrmProxyMailListHtmlGridSource`，在dll中找到它的逻辑实现

[![东胜物流软件 CrmProxyMailListHtmlGridSource.aspx SQL注入漏洞](images/img-001-4bb6693bfe73.webp)](https://image.mrxn.net/a3d9357f1a63485a933b598a13a38c27.webp)

当`handle=list`时，参数`TITLE`被直接带入sql语句中，导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

深入探索

技术文章订阅

数据库

编码转换工具

# 漏洞复现

```
GET /PriceCarrier/CrmProxyMailListHtmlGridSource.aspx?handle=list&cur_page=1&show_page=10&TITLE=SQLI_POC HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 CrmProxyMailListHtmlGridSource.aspx SQL注入漏洞](images/img-002-c8247c9a2da7.webp)](https://image.mrxn.net/71091f2d49304fd79f3c38266f709997.webp)

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
文章标题：[东胜物流软件 CrmProxyMailListHtmlGridSource.aspx SQL注入漏洞](https://mrxn.net/jswz/dongsheng-PriceCarrier-CrmProxyMailListHtmlGridSource-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-PriceCarrier-CrmProxyMailListHtmlGridSource-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-PriceCarrier-CrmProxyMailListHtmlGridSource-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/dongsheng-PriceCarrier-CrmProxyMailListHtmlGridSource-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 