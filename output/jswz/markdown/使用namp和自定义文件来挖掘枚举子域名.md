---
title: "使用namp和自定义文件来挖掘/枚举子域名"
source: https://mrxn.net/jswz/subdomain-discovery-with-nmap-and-custom-subdomain-files.html
asset_dir: assets/使用namp和自定义文件来挖掘枚举子域名
---

# 使用namp和自定义文件来挖掘/枚举子域名

[Mrxn](https://mrxn.net/author/1)* 发表于2016/12/6 10:24
* 4982浏览
* [2评论](#comment)
* 11分钟阅读

深入探索

安全工具开发

服务器安全服务

漏洞扫描器


(adsbygoogle = window.adsbygoogle || []).push({});

---

下面将介绍如何使用nmap的dns-brute脚本和自定义子域文件来扫描或者是枚举域的子域。

nmap的dns-brute脚本只包括了127个常见的子域，因此我们可以用自己搜集或者是制作的自定义子域文件来枚举，这些文件包括最常见的1000个，10000个，100000个和1000000个子域。

下面配合namp的命令：

```
nmap --script dns-brute --script-args dns-brute.domain=amazon.com,dns-brute.threads=6,dns-brute.hostlist=./sub1000.lst
```

```
nmap --script dns-brute --script-args dns-brute.domain=amazon.com,dns-brute.threads=6,dns-brute.hostlist=./sub10000.lst
```

```
nmap --script dns-brute --script-args dns-brute.domain=amazon.com,dns-brute.threads=6,dns-brute.hostlist=./sub100000.lst
```

```
nmap --script dns-brute --script-args dns-brute.domain=amazon.com,dns-brute.threads=6,dns-brute.hostlist=./sub1000000.lst
```

深入探索

安全研究工具

在线安全工具

编码转换工具

下载子域名文件：download [sub1000.lst](https://drive.google.com/open?id=0B0h-Dh0Oss1zOGFqVVl1bTVpdWc) [sub10000.lst](https://drive.google.com/open?id=0B0h-Dh0Oss1zTTdmQnZsQ0JCYzA) [sub100000.lst](https://drive.google.com/open?id=0B0h-Dh0Oss1zdDBFT1dCc08ya0U) [sub1000000.lst](https://drive.google.com/open?id=0B0h-Dh0Oss1zODNfSG1sbVJ1WE0)

例如枚举亚马逊的子域名：

[[![使用namp和自定义文件来挖掘/枚举子域名](images/img-001-17427b7edddc.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201612/f9991480991790.jpg)](https://mrxn.net/content/uploadfile/201612/f9991480991790.jpg)

子域名文件来源博客：

技术文章订阅

深入探索

VPN服务

Docker加速服务

网络安全培训

<https://bitquark.co.uk/blog/2016/02/29/the_most_popular_subdomains_on_the_internet>

namp的dns-brute官方文档介绍：

<https://nmap.org/nsedoc/scripts/dns-brute.html>

原文：http://blog.x1622.com/2016/11/subdomain-discovery-with-nmap-and.html

* 标签：
* [#黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)

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
文章标题：[使用namp和自定义文件来挖掘/枚举子域名](https://mrxn.net/jswz/subdomain-discovery-with-nmap-and-custom-subdomain-files.html)  
文章链接：<https://mrxn.net/jswz/subdomain-discovery-with-nmap-and-custom-subdomain-files.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/subdomain-discovery-with-nmap-and-custom-subdomain-files.html"),
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
text: encodeURI("https://mrxn.net/jswz/subdomain-discovery-with-nmap-and-custom-subdomain-files.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 