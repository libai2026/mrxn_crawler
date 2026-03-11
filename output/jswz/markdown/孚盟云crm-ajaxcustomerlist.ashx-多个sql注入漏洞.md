---
title: "孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞"
source: https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerList-sqli.html
asset_dir: assets/孚盟云crm-ajaxcustomerlist.ashx-多个sql注入漏洞
---

# 孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/1/16 08:31
* 256浏览
* [0评论](#comment)
* 13分钟阅读

深入探索

企业安全咨询

编码转换工具

安全运维咨询


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

上海孚盟软件有限公司是一家专业的外贸SaaS服务和行业解决方案提供商。其旗下产品孚盟云AjaxCustomerList.ashx接口存在多个[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞获取数据库中的信息(例如，管理员后台密码、站点的用户个人信息)之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入检测工具

# 影响版本

# fofa语法

> app="孚盟软件-孚盟云"

# 漏洞分析

深入探索

云安全解决方案

漏洞预警服务

数据库

直接看 `AjaxCustomerList.ashx` 对应的dll文件 `FumaCRM_BS.NewWeb.dll` 里有关 **AjaxCustomerList** 方法的实现如下

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-001-c4987d3f81f5.webp)](https://image.mrxn.net/e1f1f36bb9f442c19065f6d3104c8e19.webp)

当**method**=**showFocused**时，看下`showFocused`方法的实现

代码安全审计

```
  private void showFocused(HttpContext context, string empID)
  {
    DataTable mouldFieldList = new CreatePageManager().GetMouldFieldList("BF001", empID);
    DataTable structPanel = new CreatePageManager().GetStructPanel("BF001", empID, 1);
    DataTable mouldTableLinks = new CreatePageManager().GetMouldTableLinks("BF001");
    string sql = $"M.FID in (select custFID from tmFocusedCustomer where EmpID='{empID}') AND 1=1  AND  1=1";
    DataTable Sourcedd = new DataTable();
```

参数**empID**未经过任何过滤或校验就被直接拼接进SQL语句中进行执行，从而造成[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

当**method=GetEmpCanViewRightType**时，一样的存在SQL注入漏洞

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-002-a4e434593671.webp)](https://image.mrxn.net/c2e3bc4c0d2742f89a45b1886ec19bf0.webp)

method=GetCustomerInfoByFid

漏洞扫描服务

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-003-7ec1e26bfa7e.webp)](https://image.mrxn.net/a23c150f3fcd4129b00d12ba0a08aaa2.webp)

method=lerevnClick

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-004-9bae2ff7c1e8.webp)](https://image.mrxn.net/5a8eec86987b46319e078fd8d73f8596.webp)

method=VersionCheck

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-005-9a3c7010634e.webp)](https://image.mrxn.net/36948f9202da4ce1b5a711425d003d30.webp)

method=EditCustomer

物流软件安全

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-006-d73aa49cdb2c.webp)](https://image.mrxn.net/173b03113d264573b0e18ba705edf237.webp)

method=SaveCust

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-007-a228292cf959.webp)](https://image.mrxn.net/fd0c3cc2abf4405fb3437600d379f04d.webp)

method=lingshi

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-008-d48ce8f8c279.webp)](https://image.mrxn.net/97f7db055b844b92b02796632e9fc821.webp)

method=updateversion

编程

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-009-cc084819921e.webp)](https://image.mrxn.net/b62d692933184bf6abd561445bfb2db1.webp)

method=AddContact

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-010-a88121ec9ad2.webp)](https://image.mrxn.net/10fa2892abc54ba5826246fb19969d1e.webp)

太多了 不一一列举了...

SQL注入检测工具

# 漏洞复现

```
POST /m/Dingding/Ajax/AjaxCustomerList.ashx HTTP/1.1
Host: fumacrm.mrxn.net
Cookie: UserCookie={"empId":"')SQLI_POC--"}
Content-Type: application/x-www-form-urlencoded

method=showFocused
```

[![孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](images/img-011-5d64d6a2aae5.webp)](https://image.mrxn.net/68df298e0ea54cd58a3b8398a177fc6b.webp)

通过报错注入在响应里回显数据库版本信息

代码安全审计

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
* [#asp.net](https://mrxn.net/tag/asp.net)

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
文章标题：[孚盟云CRM AjaxCustomerList.ashx 多个SQL注入漏洞](https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerList-sqli.html)  
文章链接：<https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerList-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

漏洞扫描服务

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerList-sqli.html"),
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

代码安全审计

  

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
text: encodeURI("https://mrxn.net/jswz/fumacrm-Dingding-Ajax-AjaxCustomerList-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 