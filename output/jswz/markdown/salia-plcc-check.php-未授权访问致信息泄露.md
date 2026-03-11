---
title: "Salia PLCC check.php 未授权访问致信息泄露"
source: https://mrxn.net/jswz/salia-check-unauth-data-leak.html
asset_dir: assets/salia-plcc-check.php-未授权访问致信息泄露
---

# Salia PLCC check.php 未授权访问致信息泄露

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/31 08:20
* 712浏览
* [0评论](#comment)
* 2分钟阅读

深入探索

安全认证考试

Docker加速服务

安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Salia PLCC 的 eCHARGE 系列提供适用于家庭、企业和公共场所的智能电动汽车充电解决方案，具备高效充电、动态负载管理和光伏系统集成等功能的充电站。其充电管理系统 `check.php` 存在信息泄露漏洞，[未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83 "未授权")攻击者可利用该漏洞获取系统敏感信息。

漏洞修复方案

# 影响版本

2.2.0（最新版）

# fofa语法

> `"Salia PLCC"`

# 漏洞分析

深入探索

网页浏览器

防火墙软件

Windows安全工具

# 漏洞复现

```
GET /check.php HTTP/1.1
Host: salia.mrxn.net
```

比如硬编码的账户和密码

[![Salia PLCC check.php 未授权访问致信息泄露](images/img-001-7b828d417daf.webp)](https://image.mrxn.net/507d63e95cad4279b33380a45aad1ac9.webp)

版本号

[![Salia PLCC check.php 未授权访问致信息泄露](images/img-002-d03f083bdb24.webp)](https://image.mrxn.net/dc7bf27c45294e3297f53c58042eace9.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#未授权](https://mrxn.net/tag/%E6%9C%AA%E6%8E%88%E6%9D%83)

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
文章标题：[Salia PLCC check.php 未授权访问致信息泄露](https://mrxn.net/jswz/salia-check-unauth-data-leak.html)  
文章链接：<https://mrxn.net/jswz/salia-check-unauth-data-leak.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

安全运维咨询

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/salia-check-unauth-data-leak.html"),
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
text: encodeURI("https://mrxn.net/jswz/salia-check-unauth-data-leak.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 