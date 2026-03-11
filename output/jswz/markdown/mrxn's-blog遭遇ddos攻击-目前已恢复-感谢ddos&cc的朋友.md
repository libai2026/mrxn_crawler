---
title: "Mrxn's Blog遭遇DDoS攻击-目前已恢复-感谢DDoS&CC的朋友"
source: https://mrxn.net/jswz/ddos-cc-protect.html
asset_dir: assets/mrxn's-blog遭遇ddos攻击-目前已恢复-感谢ddos&cc的朋友
---

# Mrxn's Blog遭遇DDoS攻击-目前已恢复-感谢DDoS&CC的朋友

[Mrxn](https://mrxn.net/author/1)* 发表于2015/11/8 22:05
* 8780浏览
* [8评论](#comment)
* 6分钟阅读

深入探索

服务器

电子计算机

数据库


(adsbygoogle = window.adsbygoogle || []).push({});

---

今晚吃完饭不久，邮箱就收到服务器发来的邮件，报告大量可疑请求，当时没有回家，没有电脑，等我赶回家的时候，服务器就已经自动关闭了。。。

技术文章订阅

[[![Mrxn's Blog遭遇DDoS攻击-目前已恢复-感谢DDoS&CC的朋友](images/img-001-0bb2d1c407dc.png "点击查看原图")](https://mrxn.net/content/uploadfile/201511/thum-1c951446995272.png)](https://mrxn.net/content/uploadfile/201511/1c951446995272.png)

回家后，第一件事就是关闭服务器所有非必要端口和服务，下载日志到本地分析，找可疑的攻击源，从日志中分析得到大概如下内容：

conntrack table (truncated)的记录中记录大量的443端口请求和80端口请求，导致443端口和80端口被占用，一般没有使用https加密的网站不会使用443端口（估计是因为使用https访问，一般的扫描软件不能扫描到啥有用的信息），使正常访问者不能访问，其实我就是想说就是大量DDoS+CC攻击，一看就是小学生之手！真是无聊。不过的感谢这些小学生啊，让我又重新配置了服务器，提升服务器的安全性。现在CC和少量ddos基本上没作用了的哈！欢迎压力测试！当然，大流量攻击连用了上百台高档服务器做了负载均衡的新浪都扛不住，何况我这个个小小的普通服务器呢！高手就请放过小站，感激不尽！

最后呢，希望做独立站的站长朋友们，一定要做好安全措施，修改常用端口，屏蔽不用的端口，文件夹权限设置严密，别给小学生骚扰的机会，烦死了！至于分析日志这些东西，自己百度吧，多得是，也不是一两句话就可以说清楚的。欢迎各位站长一起交流服务器攻防，运维！

* 标签：
* [#攻击](https://mrxn.net/tag/%E6%94%BB%E5%87%BB)
* [#分享](https://mrxn.net/tag/%E5%88%86%E4%BA%AB)
* [#DDOS](https://mrxn.net/tag/DDOS)
* [#nginx](https://mrxn.net/tag/nginx)
* [#运维](https://mrxn.net/tag/%E8%BF%90%E7%BB%B4)

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
文章标题：[Mrxn's Blog遭遇DDoS攻击-目前已恢复-感谢DDoS&amp;CC的朋友](https://mrxn.net/jswz/ddos-cc-protect.html)  
文章链接：<https://mrxn.net/jswz/ddos-cc-protect.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

计算机服务器

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/ddos-cc-protect.html"),
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

计算机硬件

  

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
text: encodeURI("https://mrxn.net/jswz/ddos-cc-protect.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 