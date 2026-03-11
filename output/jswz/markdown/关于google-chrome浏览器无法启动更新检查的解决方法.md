---
title: "关于Google chrome浏览器无法启动更新检查的解决方法"
source: https://mrxn.net/jswz/chrome-update-error-code-4-0x80070005-system-level.html
asset_dir: assets/关于google-chrome浏览器无法启动更新检查的解决方法
---

# 关于Google chrome浏览器无法启动更新检查的解决方法

[Mrxn](https://mrxn.net/author/1)* 发表于2016/11/25 12:38
* 7601浏览
* [0评论](#comment)
* 4分钟阅读

深入探索

安装程序

安装

chrome


(adsbygoogle = window.adsbygoogle || []).push({});

---

因为自己的身体原因，几个月没有使用电脑，今天开机使用的时候想更新一下chrome浏览器，结果就出现这个错误：[[![关于Google chrome浏览器无法启动更新检查的解决方法](images/img-001-b1bce337fa86.png "点击查看原图")](https://mrxn.net/content/uploadfile/201611/02a21480049339.png)](https://mrxn.net/content/uploadfile/201611/02a21480049339.png)

检查更新时出错：无法启动更新检查（错误代码为 4: [0x80070005](https://support.google.com/chrome/answer/6315198?visit_id=1-636156446874269825-3305065930&rd=1) -- system level）。

网络浏览器

先说第一种解决方法：直接点击这串蓝色的数字，会自动跳转到Google的官方帮助站点，直接下载离线安装版，跟着操作就OK。

第二种，我们从提示出错的字面意思去理解它：无法启动更新检查，那么就有可能是检查更新服务没有启动，验证一下就好了：

```
win+R
services.msc
```

查看结果如下：

[[![关于Google chrome浏览器无法启动更新检查的解决方法](images/img-002-774ce1ba1156.png "点击查看原图")](https://mrxn.net/content/uploadfile/201611/29d21480049339.png)](https://mrxn.net/content/uploadfile/201611/29d21480049339.png)

果然是Google的更新服务被禁用了，我想可能是在使用优化软件优化的时候做的负优化 -\_-|| ，

计算机硬件

深入探索

安全认证考试

漏洞扫描服务

编码转换工具

直接右键--属性--启动改为手动就OK了，在前往<chrome://help/> 更新就好了。

* 标签：
* [#google](https://mrxn.net/tag/google)

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
文章标题：[关于Google chrome浏览器无法启动更新检查的解决方法](https://mrxn.net/jswz/chrome-update-error-code-4-0x80070005-system-level.html)  
文章链接：<https://mrxn.net/jswz/chrome-update-error-code-4-0x80070005-system-level.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/chrome-update-error-code-4-0x80070005-system-level.html"),
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

物流软件安全

  

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
text: encodeURI("https://mrxn.net/jswz/chrome-update-error-code-4-0x80070005-system-level.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 