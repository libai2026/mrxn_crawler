---
title: "东胜物流软件 MsOpSeaeController 多个SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-MsOpSeaeController-sqli.html
asset_dir: assets/东胜物流软件-msopseaecontroller-多个sql注入漏洞
---

# 东胜物流软件 MsOpSeaeController 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/23 08:41
* 223浏览
* [0评论](#comment)
* 7分钟阅读

深入探索

服务器

鉴权

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 MsOpSeaeController 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

深入探索

Docker加速服务

安全

Web安全课程

找到**MsOpSeaeController**下的action方法**GetMblIsRepeat**

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-001-77a38b565af7.webp)](https://image.mrxn.net/b8e54ba668cc4b25bf552118353df490.webp)

`bsno` 和 `mblno` 参数被直接拼接进SQL语句中，从而造成了[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

其他action也是一样的

SQL注入防护

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-002-4077ea230e1e.webp)](https://image.mrxn.net/3034205615194228bee9b7aef2401b03.webp)

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-003-f0905e994dc1.webp)](https://image.mrxn.net/e99270e7ab464656954291be9812abb0.webp)

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-004-527bb9072553.webp)](https://image.mrxn.net/1da949b495104c979e46c22ad96dd043.webp)

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-005-7aa18cb34633.webp)](https://image.mrxn.net/a783c814a6f244aaad57082572d9f9f2.webp)

# 漏洞复现

```
POST /MvcShipping/MsOpSeae/GetMblIsRepeat HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

bsno=1&mblno=SQLI_POC
```

[![东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](images/img-006-290118d59e39.webp)](https://image.mrxn.net/610e45fb5ce243499f4221386e6bc2ce.webp)

成功通过报错注入在响应中回显数据库版本信息。

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
文章标题：[东胜物流软件 MsOpSeaeController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsOpSeaeController-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-MsOpSeaeController-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-MsOpSeaeController-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/dongsheng-MsOpSeaeController-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 