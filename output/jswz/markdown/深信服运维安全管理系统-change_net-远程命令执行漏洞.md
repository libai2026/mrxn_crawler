---
title: "深信服运维安全管理系统 change_net 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html
asset_dir: assets/深信服运维安全管理系统-change_net-远程命令执行漏洞
---

# 深信服运维安全管理系统 change\_net 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/3/2 08:35
* 472浏览
* [0评论](#comment)
* 8分钟阅读

深入探索

SQL

软件

脚本


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 change\_net 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。影响范围包括所有运行存在该漏洞版本的深信服运维安全管理系统的服务器。

文件大小转换

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

看下 `com.sbr.fort.web.controller.system.netconfig.NetConfigController#changeNet`的实现逻辑

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-001-390ca7892232.webp)](https://image.mrxn.net/a166418764d44f7483f2690261d39cad.webp)

从请求获取多个参数如ethnum、address、netmask、bnum等等，然后对这些参数进行拼接

漏洞扫描服务

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-002-f0b33e01111c.webp)](https://image.mrxn.net/6786384d3e514fdc87e61a92d1e07fbb.webp)

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-003-fc27580cc958.webp)](https://image.mrxn.net/3a8a8e45cab54e83ae80e487fdf6e84d.webp)

拼接完成后

计算机服务器

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-004-ac1acc73d434.webp)](https://image.mrxn.net/3c621d40dad24d5397dda09dc4dfa3d2.webp)

调用`ShellExecutor`类的`exe`方法进行执行shell[脚本](#)，从而造成[命令执行](https://mrxn.net/tag/rce)漏洞。

漏洞修复的版本在命令执行时，增加了一个`clean`方法对特殊字符的替换操作

脚本语言

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-005-02494ba0d448.webp)](https://image.mrxn.net/fbb1aa7dc3134624b8f7de62a341767e.webp)

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-006-1cf8bb27a6c3.webp)](https://image.mrxn.net/24f3ebc925ab4adc9624c3601e608feb.webp)

紧接着的 `change_gate_way` 亦如此，参数**ethnum**与**gateway**直接拼接进`cmd`中后调用`executor.exe`执行

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-007-d5288974dc96.webp)](https://image.mrxn.net/3e4b75b60e1741f58d235ee58d3934cc.webp)

# 漏洞复现

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-008-95edf58edb9c.webp)](https://image.mrxn.net/4c6f5f6e3a4f4370a520ceda847556a4.webp)

## POC

> 多个参数均存在命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，这里以ethnum为例
>
> 漏洞扫描服务

```
POST /fort/system;help/netConfig/change_net HTTP/1.1
Host: sangfor_osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

sta=static&ipv=4&ethnum=RCE_POC &address=1.1.1.1&netmask=2.2.2.2&gateWay=3.3.3.3
```

访问命令执行结果文件

[![深信服运维安全管理系统 change_net 远程命令执行漏洞](images/img-009-f9f9f9d5337d.webp)](https://image.mrxn.net/075fd8c3f77047d99ba8c31646218c8f.webp)

成功得到[命令执行](https://mrxn.net/tag/rce)结果

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#0day](https://mrxn.net/tag/0day)
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
* [5.1.POC](#toc-5-1-)



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
文章标题：[深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-netConfig-change\_net-rce.html"),
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
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

文件大小转换

  

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
text: encodeURI("https://mrxn.net/jswz/sangfor\_osm-netConfig-change\_net-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 