---
title: "东胜物流软件 StorageController 多个SQL注入漏洞"
source: https://mrxn.net/jswz/dongsheng-StorageController-sqli.html
asset_dir: assets/东胜物流软件-storagecontroller-多个sql注入漏洞
---

# 东胜物流软件 StorageController 多个SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/22 08:41
* 209浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

数据库

身份验证

木马


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

东胜物流软件是青岛东胜伟业软件有限公司一款集订单管理、仓库管理、运输管理等多种功能于一体的物流管理软件。东胜物流信息管理系统 StorageController 接口存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞，未经身份验证的远程攻击者除了可以利用SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

物流软件安全

# 影响版本

# fofa语法

> body="FeeCodes/CompanysAdapter.aspx" || body="dhtmlxcombo\_whp.js" || body="dongshengsoft" || body="theme/dhtmlxcombo.css"

# 漏洞分析

根据**Storage**路由下的mvc的定义

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-001-b1858e652564.webp)](https://image.mrxn.net/64e0bad691f249e48695998110eb43cd.webp)

比如找到**StorageController**下的action方法**DQStorageData**

SQL注入检测工具

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-002-b6a24a6a7661.webp)](https://image.mrxn.net/e61627b40bfa4f37afea38bfb24288a3.webp)

`openid`参数带入`GetDQKuCunDataList`方法中

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-003-56e08b3a8c88.webp)](https://image.mrxn.net/3432764c679a46079dac4cf0da3daa96.webp)

可以看到`openid`参数被直接拼接进SQL语句中，从而造成了SQL注入漏洞。

代码安全审计

其他action也是一样的

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-004-5f92b0c85be6.webp)](https://image.mrxn.net/a69ceb885fe048bf920db23ef0bd6caa.webp)

看下`GetIndoDataList`方法的实现

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-005-e21262140f87.webp)](https://image.mrxn.net/c8d8fa2030dd48fc94e547e7c8efebb9.webp)

参数**mblno**也是被直接拼接进SQL语句中导致[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞。

其他的action如**OutDoListData**、**StorageInDetailData**、**StorageOutDetailData**一样

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-006-954dac02c4e6.webp)](https://image.mrxn.net/3dce2fe803fd49c5985bcfb902de7829.webp)

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-007-c49ce8b37f10.webp)](https://image.mrxn.net/4a7dfd325ca54a75aa9594ad7ee6c508.webp)

StorageInDetailData

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-008-e666004f20b2.webp)](https://image.mrxn.net/6f746b649b7b44018fe365bd85c30c8c.webp)

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-009-d30920293eff.webp)](https://image.mrxn.net/1f007c6bb82f4756b4bd2f18bdd8c43c.webp)

StorageOutDetailData

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-010-e6c21983ae7a.webp)](https://image.mrxn.net/f3b0a8cea3154290b8204934a1f65a5d.webp)

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-011-6ae9cbbafce0.webp)](https://image.mrxn.net/fb83bd34a15e44eb918a616ce2fcc525.webp)

# 漏洞复现

```
GET /Storage/Storage/DQStorageData?openid=SQLI_POC&mblno=111&page=1&pageSize=10 HTTP/1.1
Host: dongsheng.mrxn.net
```

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-012-6a20871f653a.webp)](https://image.mrxn.net/f715bc4bbca94b1b8dde49a8ea3b2c39.webp)

成功通过报错注入在响应中回显数据库版本信息。

漏洞扫描服务

[![东胜物流软件 StorageController 多个SQL注入漏洞](images/img-013-ed23e34a81c9.webp)](https://image.mrxn.net/31da42f94112463d968e50162dc75954.webp)

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
文章标题：[东胜物流软件 StorageController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-StorageController-sqli.html)  
文章链接：<https://mrxn.net/jswz/dongsheng-StorageController-sqli.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/dongsheng-StorageController-sqli.html"),
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
text: encodeURI("https://mrxn.net/jswz/dongsheng-StorageController-sqli.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 