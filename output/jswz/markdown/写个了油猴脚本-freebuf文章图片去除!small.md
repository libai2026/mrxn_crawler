---
title: "写个了油猴脚本-freebuf文章图片去除!small"
source: https://mrxn.net/jswz/modify_freebuf_pic.html
asset_dir: assets/写个了油猴脚本-freebuf文章图片去除!small
---

# 写个了油猴脚本-freebuf文章图片去除!small

[Mrxn](https://mrxn.net/author/1)* 发表于2019/4/14 22:38
* 3888浏览
* [2评论](#comment)
* 3分钟阅读

深入探索

Google Chrome

chrome

Firefox


(adsbygoogle = window.adsbygoogle || []).push({});

---

写这个[脚本](https://mrxn.net/tag/%E8%84%9A%E6%9C%AC)的原因就是我发现freebuf的文章里的图片后缀都会跟一个 !small 后缀，我想网站初心可能是为了对付爬虫吧，恶意爬虫爬去文章文字和图片，但是对于我这种懒虫，不喜欢点击一下放大去看图，而是比较喜欢文章的图片就是页面最佳尺寸，简单的研究了一下，发现去掉文章里的图片的 !small 后缀后，文章图片默认就会显示最佳尺寸了！简直Nice啊！但是每次这么去手动修改太麻烦了，如果文章图片太多，那岂不是要累死？于是这个[脚本](#)就出来了！效果如下的动图演示：  
[![写个了油猴脚本-freebuf文章图片去除!small](images/img-001-2f1e8a64c823.gif "去除 freebuf 文章!small 演示动图")](https://raw.githubusercontent.com/Mr-xn/modify_freebuf_pic/master/%E5%8E%BB%E9%99%A4!small.gif)  
  
**使用：**前提是在油猴脚本支持的浏览器(比如chrome，Firefox这些现代浏览器)，在油猴插件里面自己粘贴我发布在[GitHub](https://github.com/Mr-xn/modify_freebuf_pic)仓库的代码或者是从[Greasy Fork 在线下载安装](https://greasyfork.org/zh-CN/scripts/381845-freebuf%E6%96%87%E7%AB%A0%E5%9B%BE%E7%89%87%E5%8E%BB%E9%99%A4-small) （强烈推荐）

* 标签：
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#脚本](https://mrxn.net/tag/%E8%84%9A%E6%9C%AC)
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#JavaScript](https://mrxn.net/tag/JavaScript)

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
文章标题：[写个了油猴脚本-freebuf文章图片去除!small](https://mrxn.net/jswz/modify_freebuf_pic.html)  
文章链接：<https://mrxn.net/jswz/modify_freebuf_pic.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

免费软件与共享软件

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/modify\_freebuf\_pic.html"),
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

脚本语言

  

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
text: encodeURI("https://mrxn.net/jswz/modify\_freebuf\_pic.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 