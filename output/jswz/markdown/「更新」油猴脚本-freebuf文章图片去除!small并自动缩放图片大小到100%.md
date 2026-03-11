---
title: "「更新」油猴脚本---freebuf文章图片去除!small并自动缩放图片大小到100%"
source: https://mrxn.net/jswz/updaet_modify_freebuf_pic.html
asset_dir: assets/「更新」油猴脚本-freebuf文章图片去除!small并自动缩放图片大小到100%
---

# 「更新」油猴脚本---freebuf文章图片去除!small并自动缩放图片大小到100%

[Mrxn](https://mrxn.net/author/1)* 发表于2019/5/1 16:38
* 3284浏览
* [6评论](#comment)
* 5分钟阅读

深入探索

身份验证

授权

技术文章订阅


(adsbygoogle = window.adsbygoogle || []).push({});

---

我之前写过一篇文章是关于freebuf文章图片去除!small得，地址在这里:<https://mrxn.net/jswz/modify_freebuf_pic.html>，但是后来我发现有一个BUG，很严重得那种：因为我当时在写插件的时候是在文章全部浏览完后直接写得，这也就导致了我当时忽略了 freebuf 的图片是懒加载的，这样的话如果还是像我之前那样直接去除图片 src 末尾的 !small ，会导致没有在第一屏内的图片不会被渲染出来！so ，趁着这次五一国际劳动节放假当天，我就来更新来了！本次更新重新设计了一下，就是取消掉了那个小标签添加，在文章页面禁用了lazyload加载，当你读文章慢慢往下滚动的时候就可以自动去除图片末尾的 !small 了，而且回自动修改图片的宽度属性到 100% (受父节点限制，不会撑爆的)，尽可能的显示图片大小从而方便阅读。[![「更新」油猴脚本---freebuf文章图片去除!small并自动缩放图片大小到100%](images/img-001-2f1e8a64c823.gif "脚本演示")](https://raw.githubusercontent.com/Mr-xn/modify_freebuf_pic/master/%E5%8E%BB%E9%99%A4!small.gif)

### [Greasy Fork 在线下载安装](https://greasyfork.org/zh-CN/scripts/381845-freebuf%E6%96%87%E7%AB%A0%E5%9B%BE%E7%89%87%E5%8E%BB%E9%99%A4-small)

深入探索

Web安全书籍

漏洞预警服务

网络安全培训

Github地址：<https://github.com/Mr-xn/modify_freebuf_pic>

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

* [1.
  Greasy Fork 在线下载安装](#toc-1-)



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
文章标题：[「更新」油猴脚本---freebuf文章图片去除!small并自动缩放图片大小到100%](https://mrxn.net/jswz/updaet_modify_freebuf_pic.html)  
文章链接：<https://mrxn.net/jswz/updaet_modify_freebuf_pic.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

文件大小转换

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/updaet\_modify\_freebuf\_pic.html"),
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
text: encodeURI("https://mrxn.net/jswz/updaet\_modify\_freebuf\_pic.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 