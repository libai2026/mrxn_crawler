---
title: "下载谷歌浏览器(Chrome)扩展离线安装包crx文件的简单方法"
source: https://mrxn.net/jswz/crx.html
asset_dir: assets/下载谷歌浏览器(chrome)扩展离线安装包crx文件的简单方法
---

# 下载谷歌浏览器(Chrome)扩展离线安装包crx文件的简单方法

[Mrxn](https://mrxn.net/author/1)* 发表于2015/5/11 11:25
* 21780浏览
* [2评论](#comment)
* 10分钟阅读

深入探索

安装

Google扩展

Chrome Web Store


(adsbygoogle = window.adsbygoogle || []).push({});

---

因为天朝屏蔽Google,所以在[博主](https://mrxn.net)安装Google扩展的时候总是失败,于是[查资料](https://mrxn.net/?keyword=%E7%BF%BB%E5%A2%99) (想要[翻](https://mrxn.net/?keyword=%E7%BF%BB%E5%A2%99)墙,请在本博客搜索"[查资料](https://mrxn.net/?keyword=%E7%BF%BB%E5%A2%99)")在Google里找到了如下方法:

如果不会使用，请看下面的操作步骤



**引言**（可以不看）：

网络浏览器

下面介绍一下，下载谷歌浏览器(Google Chrome)扩展的离线安装包crx文件最简单的方法！真的是再简单不过了！  
[谷歌浏览器](https://www.google.com/chrome)(Google Chrome)的扩展功能让谷歌浏览器变的无比强大，需要特殊功能的时候去[Chrome Web Store](https://chrome.google.com/webstore)找一下，基本都可以找到合适的扩展。但是随着Chrome浏览器使用的时间越来越长，积累下来的扩展也越来越多，备份这些扩展就成了一个新的问题。  
比如出于由于某些众所周知的原因，在给MM(或朋友、爸妈等)装机的时候可能上不去扩展安装页面。有时候一个一个安装、同步又显得比较耗时。当然还有很多其他的原因。  
那么我们如果提前将扩展下载好放在U盘里，那样就可以在需要的时候安全快捷的安装上。  
在Chrome Web Store里面点击安装以后，扩展默认是下载完毕后立即删除，不给你时间保存安装包，要保存扩展就成了一个难题，以下提供一个保存扩展的简便方法！

**操作步骤**：

深入探索

网络安全课程

VPN服务

安全运维咨询

1.**打开扩展介绍页面** (在 三道杠图标>工具>扩展程序 里相应扩展的"访问网站"处也可以获得)  
比如："https://chrome.google.com/webstore/detail/gighmmpiobklfepjocnamgkkbiglidom"

2.**复制扩展ID**(扩展地址里面的那个32位的字符串，比如第一步地址里面↑红颜色↑的那部分)

3.进入 [mrxn.net/code/crx/index.php](https://mrxn.net/code/crx/index.php) **粘贴扩展ID，点击生成按钮**。

4.**右键另存为**下面那行暗红色连接即可(不要直接点击，防止谷歌浏览器直接安装)。

免费软件与共享软件

怎么样，很简单吧？

附上**安装离线.crx扩展包**的方法：

等到以后重装系统或者其他原因，需要重新安装扩展时，在谷歌浏览器中**打开扩展管理页面**，然后直接把那个后缀是.crx的扩展安装包**拖拽到扩展管理页面**里就可以了。

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
文章标题：[下载谷歌浏览器(Chrome)扩展离线安装包crx文件的简单方法](https://mrxn.net/jswz/crx.html)  
文章链接：<https://mrxn.net/jswz/crx.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/crx.html"),
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
text: encodeURI("https://mrxn.net/jswz/crx.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 