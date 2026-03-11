---
title: "破解shc加密过的二进制脚本,此处以破解一个云免脚本为例"
source: https://mrxn.net/jswz/unshc-the-shc-decrypter.html
asset_dir: assets/破解shc加密过的二进制脚本,此处以破解一个云免脚本为例
---

# 破解shc加密过的二进制脚本,此处以破解一个云免脚本为例

[Mrxn](https://mrxn.net/author/1)* 发表于2017/1/23 20:23
* 8661浏览
* [0评论](#comment)
* 5分钟阅读

深入探索

脚本

Bash

脚本语言


(adsbygoogle = window.adsbygoogle || []).push({});

---

首先简单的介绍一下shc:

脚本语言

shc是一个专业的加密shell[脚本](#)的工具.它的作用是把shell脚本转换为一个可执行的二进制文件，这个办法很好的解决了脚本中含有IP、密码等不希望公开的问题.

今天逛一个博客看见了他的一篇文章说的关于破解云免脚本的,评论里面很多人说破解不了骚逼汪的云免脚本,我就是试试而已.哈哈

Google一下就找到了在youtube上的一个视频: [UnSHc - decrypt shc \*.sh.x bash script](https://www.youtube.com/watch?v=tmHVhMuG-Vg)

然后在作者的博客和github找到了:Unshc脚本.一键破解,很方便,在此记录一下:

首先未破解时是二进制打开是这样:[[![破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](images/img-001-1b8a978dba9e.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201701/d42c1485174326.jpg)](https://mrxn.net/content/uploadfile/201701/d42c1485174326.jpg)

然后克隆Unshc脚本到本地:[[![破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](images/img-002-6dce7d259453.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201701/927a1485174326.jpg)](https://mrxn.net/content/uploadfile/201701/927a1485174326.jpg)

然后赋予脚本的执行权限后就可以看到相应使用方法:[[![破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](images/img-003-e0be2d5c0951.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201701/323f1485174326.jpg)](https://mrxn.net/content/uploadfile/201701/323f1485174326.jpg)

直接破解:[[![破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](images/img-004-efe6b5bb1989.png "点击查看原图")](https://mrxn.net/content/uploadfile/201701/02561485174325.png)](https://mrxn.net/content/uploadfile/201701/02561485174325.png)

破解后的:[[![破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](images/img-005-bd33e2f0ef60.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201701/89841485174326.jpg)](https://mrxn.net/content/uploadfile/201701/89841485174326.jpg)

Unshc 作者github和博客:

脚本语言

<https://github.com/yanncam/UnSHc>

<https://www.asafety.fr/unshc-the-shc-decrypter/>

利用好搜索.事半功倍! 下回见!

* 标签：
* [#shell](https://mrxn.net/tag/shell)
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#Linux](https://mrxn.net/tag/Linux)

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
文章标题：[破解shc加密过的二进制脚本,此处以破解一个云免脚本为例](https://mrxn.net/jswz/unshc-the-shc-decrypter.html)  
文章链接：<https://mrxn.net/jswz/unshc-the-shc-decrypter.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/unshc-the-shc-decrypter.html"),
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

技术文章订阅

  

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
text: encodeURI("https://mrxn.net/jswz/unshc-the-shc-decrypter.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 