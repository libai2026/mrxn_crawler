---
title: "东胜物流软件 IPLimitController SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-IPLimit-UpdateIPAddress-sqli.html
asset_dir: assets/东胜物流软件-iplimitcontroller-sql注入漏洞
---

# 东胜物流软件 IPLimitController SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/24 08:32
* 273浏览
* [0评论](#comment)
* 6分钟阅读

深入探索

VPN服务

Web安全课程

编程语言教程


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 IPLimitController 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

看下`IPLimitController`方法下的**UpdateIPAddress** action是如何实现的

[![东胜物流软件 IPLimitController SQL注入漏洞](images/img-001-02fbf5de6e52.webp)](https://image.mrxn.net/c02510f495e94a708074c16d4de77e98.webp)

如上图所示，参数name是被直接拼接进SQL语句中执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /MvcShipping/IPLimit/UpdateIPAddress HTTP/1.1
Host: dongsheng.mrxn.net
Content-Type: application/x-www-form-urlencoded

name=SQLI_POC
```

深入探索

Windows安全工具

计算机安全

安全工具开发

[![东胜物流软件 IPLimitController SQL注入漏洞](images/img-002-8dd7ca8c7745.webp)](https://image.mrxn.net/9183fb368f67420f80ecfa53a7468dbc.webp)

成功延时 3 秒

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
文章标题：[东胜物流软件 IPLimitController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-IPLimit-UpdateIPAddress-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-IPLimit-UpdateIPAddress-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-IPLimit-UpdateIPAddress-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/dongsheng-IPLimit-UpdateIPAddress-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 