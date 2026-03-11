---
title: "天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞"
source: https://mrxn.net/jswz/trwfe-identity-user-data-leak.html
asset_dir: assets/天锐绿盾审批系统-identityuser{userid}、identityinformationuser{userid}-未授权访问致敏感信息泄露漏洞
---

# 天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/12 08:27
* 424浏览
* [0评论](#comment)
* 7分钟阅读

深入探索

鉴权

软件

加密


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

天锐绿盾审批系统是一款专注于企业数据安全与合规管理的智能审批平台，深度融合文档加密、权限管控与流程自动化，为企业提供从文件创建、流转到归档的全生命周期安全管控。该系统旨在从源头上保障数据安全，防止[信息泄露](https://mrxn.net/tag/data-leak)。

漏洞存在于天锐绿盾审批系统，攻击者可以未经授权访问 `/identity/user/{userId}` 路径。利用此未授权访问漏洞，未经身份验证的攻击者能够获取系统内的[敏感信息](https://mrxn.net/tag/data-leak)。

# 影响版本

> 可通过访问 /trwfe/exports/config.ini 获取版本信息
>
> 漏洞扫描服务

V3.53.240913

深入探索

SQL注入检测工具

网页浏览器

数据库

V7.05.240904

# fofa语法

> app="TIPPAY-绿盾审批系统"

# 漏洞分析

先看`/user/{userId}`路由实现

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-001-c1269c7864fd.webp)](https://image.mrxn.net/687e980a25aa4e08a07ce2fa22619608.webp)

直接将`userId`带入查询将结果响应在body里，从而导致敏感信息泄露。

安全工具开发

`/identity/information/user/{userId}` 亦如此

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-002-bda34886e7b0.webp)](https://image.mrxn.net/8f47b75388d2423482e45cae72e40307.webp)

`/identity/information/dept/{deptId}` 亦如此

深入探索

漏洞修复方案

SQL注入防护

网络安全课程

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-003-a047568bdd09.webp)](https://image.mrxn.net/f31f572eb8124ff594d468a74cd8a031.webp)

`/identity/information/group/{groupId}` 亦如此

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-004-de3740f851c6.webp)](https://image.mrxn.net/928dc7d63ff245c79a0fd97f356bcab1.webp)

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-005-a9e3e201fe3c.webp)](https://image.mrxn.net/ce86ff721bb244218943fe6dc8cd2417.webp)

# 漏洞复现

```
GET /trwfe/ws/identity/user/admin HTTP/1.1
Host: trwfe.mrxn.net
```

即可获取到admin账户相关的信息如邮箱、姓名、密码等

网络安全

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-006-55934c0891ff.webp)](https://image.mrxn.net/67534c270c1c4c90be8798a8f9c04827.webp)

md5解密即可得到对应账号的密码

[![天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](images/img-007-cf92635f7fae.webp)](https://image.mrxn.net/04cc6a0a30ec4630afd2b424d6b9c9d2.webp)

其他用户如sysadmin、secadmin、logadmin 同样如此

漏洞扫描服务

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#data-leak](https://mrxn.net/tag/data-leak)

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
文章标题：[天锐绿盾审批系统 /identity/user/{userId}、/identity/information/user/{userId} 未授权访问致敏感信息泄露漏洞](https://mrxn.net/jswz/trwfe-identity-user-data-leak.html)  
文章链接：<https://mrxn.net/jswz/trwfe-identity-user-data-leak.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/trwfe-identity-user-data-leak.html"),
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
text: encodeURI("https://mrxn.net/jswz/trwfe-identity-user-data-leak.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 